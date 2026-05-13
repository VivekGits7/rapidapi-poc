"""Phase 3 — Deep Crawl (DFS).

Walks each (manufacturer × vehicle_type) row to FULL depth before moving on:
  MVT → models (API 5) → vehicles (API 8) → categories (API 10)

Resume mechanism: `*_fetched_at` columns on parent rows act as cursors.
Anything with NULL is "still to do." Partial indexes make next-work-item O(1).

DFS preference is enforced by always grabbing the DEEPEST pending work first:
1. Pending vehicle → fetch categories
2. Pending model   → fetch vehicles
3. Pending MVT     → fetch models
4. Nothing pending → done.
"""

from datetime import date, datetime
from typing import Any, Awaitable, Callable, Optional

import asyncpg

from config import settings
from logger import get_logger
from dumper.http_client import api_get
from dumper.id_utils import new_id
from services.db import execute_command, execute_query_one

logger = get_logger("dumper.phase3")

# A predicate the runner passes in; returns True if a graceful stop has been requested.
StopCheck = Callable[[], Awaitable[bool]]


# ==================== ENTRY POINT ====================
async def run(job_id: str, check_stop: StopCheck) -> dict:
    logger.info("Phase 3 — Deep Crawl (DFS)")
    await execute_command(
        "UPDATE rapid_api_dump_jobs SET current_phase = 'deep_crawl', updated_at = NOW() WHERE job_id = $1",
        job_id,
    )

    iteration = 0
    while True:
        if await check_stop():
            logger.info("Stop requested — leaving deep_crawl_done = FALSE for resume")
            return await _refresh_counts(job_id)

        # 1. Pending vehicle (deepest pending work)
        v = await _find_pending_vehicle()
        if v:
            await _fetch_categories(v)
            iteration += 1
            if iteration % 50 == 0:
                await _refresh_counts(job_id)
            continue

        # 2. Pending model
        m = await _find_pending_model()
        if m:
            await _fetch_vehicles(m)
            continue

        # 3. Pending MVT (top of the tree)
        mvt = await _find_pending_mvt()
        if mvt:
            await _fetch_models(mvt)
            continue

        # Nothing pending — done!
        break

    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET deep_crawl_done = TRUE,
            current_phase   = 'completed',
            completed_at    = NOW(),
            updated_at      = NOW()
        WHERE job_id = $1
        """,
        job_id,
    )
    counts = await _refresh_counts(job_id)
    logger.info(f"Phase 3 done — {counts['models']} models, {counts['vehicles']} vehicles, "
                f"{counts['categories']} categories, {counts['vehicle_categories']} junctions")
    return counts


# ==================== "FIND NEXT WORK ITEM" QUERIES ====================
async def _find_pending_mvt() -> Optional[asyncpg.Record]:
    return await execute_query_one(
        """
        SELECT mvt.mvt_id,
               mvt.manufacturer_id, mvt.vehicle_type_id,
               m.external_id  AS api_mfg_id,
               m.manufacturer_name,
               vt.external_id AS api_type_id,
               vt.type_code
        FROM rapid_api_manufacturer_vehicle_types mvt
        JOIN rapid_api_manufacturers   m  ON m.manufacturer_id   = mvt.manufacturer_id
        JOIN rapid_api_vehicle_types   vt ON vt.vehicle_type_id  = mvt.vehicle_type_id
        WHERE mvt.models_fetched_at IS NULL
        ORDER BY mvt.mvt_id
        LIMIT 1
        """
    )


async def _find_pending_model() -> Optional[asyncpg.Record]:
    return await execute_query_one(
        """
        SELECT m.model_id, m.external_id AS api_model_id,
               m.manufacturer_id, m.vehicle_type_id,
               vt.external_id AS api_type_id, vt.type_code
        FROM rapid_api_models m
        JOIN rapid_api_vehicle_types vt ON vt.vehicle_type_id = m.vehicle_type_id
        WHERE m.vehicles_fetched_at IS NULL
        ORDER BY m.model_id
        LIMIT 1
        """
    )


async def _find_pending_vehicle() -> Optional[asyncpg.Record]:
    return await execute_query_one(
        """
        SELECT v.vehicle_id, v.external_id AS api_vehicle_id,
               v.vehicle_type_id,
               vt.external_id AS api_type_id, vt.type_code
        FROM rapid_api_vehicles v
        JOIN rapid_api_vehicle_types vt ON vt.vehicle_type_id = v.vehicle_type_id
        WHERE v.categories_fetched_at IS NULL
        ORDER BY v.vehicle_id
        LIMIT 1
        """
    )


# ==================== API 5 — Models for an MVT ====================
async def _fetch_models(mvt: asyncpg.Record) -> None:
    mvt_id = mvt["mvt_id"]
    api_mfg_id = int(mvt["api_mfg_id"])
    api_type_id = int(mvt["api_type_id"])
    type_code = mvt["type_code"]
    manufacturer_id = mvt["manufacturer_id"]
    vehicle_type_id = mvt["vehicle_type_id"]
    name = mvt["manufacturer_name"]

    logger.info(f"Models: {mvt_id} ({name} × {type_code})")

    path = (
        f"/models/list/type-id/{api_type_id}"
        f"/manufacturer-id/{api_mfg_id}"
        f"/lang-id/{settings.DEFAULT_LANG_ID}"
        f"/country-filter-id/{settings.DEFAULT_COUNTRY_FILTER_ID}"
    )
    data = await api_get(path)

    if data is None:
        # API call failed (after retries) — leave fetched_at NULL so we retry later
        logger.error(f"Models fetch FAILED for {mvt_id} — will retry on next iteration")
        return

    items: list = data.get("models", []) if isinstance(data, dict) else []

    inserted = 0
    for item in items:
        ext_raw = item.get("modelId")
        try:
            ext_model_id = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            continue
        if ext_model_id is None:
            continue

        existing = await execute_query_one(
            """
            SELECT 1 FROM rapid_api_models
            WHERE external_id = $1 AND manufacturer_id = $2 AND vehicle_type_id = $3
              AND lang_id = $4 AND country_filter_id = $5
            """,
            ext_model_id,
            manufacturer_id,
            vehicle_type_id,
            settings.DEFAULT_LANG_ID,
            settings.DEFAULT_COUNTRY_FILTER_ID,
        )
        if existing:
            continue

        model_id = await new_id("models", type_code)
        await execute_command(
            """
            INSERT INTO rapid_api_models
              (model_id, external_id, model_name, manufacturer_id, vehicle_type_id,
               lang_id, country_filter_id, year_from, year_to)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (external_id, manufacturer_id, vehicle_type_id, lang_id, country_filter_id) DO NOTHING
            """,
            model_id,
            ext_model_id,
            item.get("modelName", "") or "",
            manufacturer_id,
            vehicle_type_id,
            settings.DEFAULT_LANG_ID,
            settings.DEFAULT_COUNTRY_FILTER_ID,
            _parse_date(item.get("modelYearFrom")),
            _parse_date(item.get("modelYearTo")),
        )
        inserted += 1

    # Mark this MVT done — even if 0 rows returned (legitimate empty result)
    await execute_command(
        "UPDATE rapid_api_manufacturer_vehicle_types SET models_fetched_at = NOW() WHERE mvt_id = $1",
        mvt_id,
    )
    logger.info(f"  Models inserted: {inserted} (of {len(items)} returned)")


# ==================== API 8 — Engine variants (vehicles) for a model ====================
async def _fetch_vehicles(model: asyncpg.Record) -> None:
    model_id = model["model_id"]
    api_model_id = int(model["api_model_id"])
    api_type_id = int(model["api_type_id"])
    type_code = model["type_code"]
    vehicle_type_id = model["vehicle_type_id"]

    path = (
        f"/types/type-id/{api_type_id}"
        f"/list-vehicles-types/{api_model_id}"
        f"/lang-id/{settings.DEFAULT_LANG_ID}"
        f"/country-filter-id/{settings.DEFAULT_COUNTRY_FILTER_ID}"
    )
    data = await api_get(path)

    if data is None:
        logger.error(f"Vehicles fetch FAILED for {model_id} — will retry on next iteration")
        return

    items: list = data.get("modelTypes", []) if isinstance(data, dict) else []

    inserted = 0
    for item in items:
        ext_raw = item.get("vehicleId")
        try:
            ext_vid = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            continue
        if ext_vid is None:
            continue

        if await execute_query_one(
            "SELECT 1 FROM rapid_api_vehicles WHERE external_id = $1", ext_vid
        ):
            continue

        vehicle_id = await new_id("vehicles", type_code)
        await execute_command(
            """
            INSERT INTO rapid_api_vehicles
              (vehicle_id, external_id, model_id, vehicle_type_id, lang_id, country_filter_id,
               manufacturer_name, model_name, type_engine_name,
               construction_start, construction_end,
               power_kw, power_ps, capacity_tax, fuel_type, body_type, number_of_cylinders,
               capacity_lt, capacity_tech, engine_codes, eng_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
            ON CONFLICT (external_id) DO NOTHING
            """,
            vehicle_id,
            ext_vid,
            model_id,
            vehicle_type_id,
            settings.DEFAULT_LANG_ID,
            settings.DEFAULT_COUNTRY_FILTER_ID,
            item.get("manufacturerName") or None,
            item.get("modelName") or None,
            item.get("typeEngineName") or None,
            _parse_date(item.get("constructionIntervalStart")),
            _parse_date(item.get("constructionIntervalEnd")),
            _parse_decimal(item.get("powerKw")),
            _parse_decimal(item.get("powerPs")),
            item.get("capacityTax"),
            item.get("fuelType"),
            item.get("bodyType"),
            _parse_int(item.get("numberOfCylinders")),
            _parse_decimal(item.get("capacityLt")),
            _parse_decimal(item.get("capacityTech")),
            item.get("engineCodes"),
            _parse_int(item.get("engId")),
        )
        inserted += 1

    await execute_command(
        "UPDATE rapid_api_models SET vehicles_fetched_at = NOW() WHERE model_id = $1",
        model_id,
    )
    logger.info(f"  Vehicles for {model_id}: {inserted} inserted (of {len(items)} returned)")


# ==================== API 10 — Categories tree for a vehicle ====================
async def _fetch_categories(vehicle: asyncpg.Record) -> None:
    vehicle_id = vehicle["vehicle_id"]
    api_vid = int(vehicle["api_vehicle_id"])
    api_type_id = int(vehicle["api_type_id"])
    type_code = vehicle["type_code"]
    vehicle_type_id = vehicle["vehicle_type_id"]
    lang_id = settings.DEFAULT_LANG_ID

    path = (
        f"/category/type-id/{api_type_id}"
        f"/products-groups-variant-2/{api_vid}"
        f"/lang-id/{lang_id}"
    )
    data = await api_get(path)

    if data is None:
        logger.error(f"Categories fetch FAILED for {vehicle_id} — will retry on next iteration")
        return

    cats: dict = data.get("categories", {}) if isinstance(data, dict) else {}

    # Per-vehicle cache to dedup category lookups within this tree.
    cache: dict[int, str] = {}

    # Sort_order across roots: rank by insertion order from the API
    sort = 0
    for root_name, root_node in cats.items() if isinstance(cats, dict) else []:
        if not isinstance(root_node, dict):
            continue
        await _walk_category_tree(
            node=root_node,
            parent_category_id=None,
            root_category_id=None,
            vehicle_type_id=vehicle_type_id,
            type_code=type_code,
            lang_id=lang_id,
            vehicle_id=vehicle_id,
            cache=cache,
            sort_order=sort,
            parent_path="",
        )
        sort += 1

    await execute_command(
        "UPDATE rapid_api_vehicles SET categories_fetched_at = NOW() WHERE vehicle_id = $1",
        vehicle_id,
    )


async def _walk_category_tree(
    node: dict,
    parent_category_id: Optional[str],
    root_category_id: Optional[str],
    vehicle_type_id: str,
    type_code: str,
    lang_id: int,
    vehicle_id: str,
    cache: dict[int, str],
    sort_order: int,
    parent_path: str,
) -> None:
    ext_raw = node.get("categoryId")
    name = node.get("categoryName", "") or ""
    try:
        ext_cat_id = int(ext_raw) if ext_raw is not None else None
    except (TypeError, ValueError):
        return
    if ext_cat_id is None:
        return

    children = node.get("children")
    is_leaf = not children or (isinstance(children, (list, dict)) and len(children) == 0)
    level = int(node.get("level", 1)) if node.get("level") is not None else 1
    full_path = f"{parent_path} > {name}" if parent_path else name

    # Look up or insert this category
    category_id = cache.get(ext_cat_id)
    if not category_id:
        existing = await execute_query_one(
            """
            SELECT category_id FROM rapid_api_categories
            WHERE external_id = $1 AND vehicle_type_id = $2 AND lang_id = $3
            """,
            ext_cat_id,
            vehicle_type_id,
            lang_id,
        )
        if existing:
            category_id = existing["category_id"]
        else:
            category_id = await new_id("categories", type_code)
            actual_root = root_category_id or category_id  # self-reference for roots
            await execute_command(
                """
                INSERT INTO rapid_api_categories
                  (category_id, external_id, category_name, parent_category_id, root_category_id,
                   level, path, is_leaf, sort_order, vehicle_type_id, lang_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (external_id, vehicle_type_id, lang_id) DO NOTHING
                """,
                category_id,
                ext_cat_id,
                name,
                parent_category_id,
                actual_root,
                level,
                full_path,
                is_leaf,
                sort_order,
                vehicle_type_id,
                lang_id,
            )
            # Re-fetch in case ON CONFLICT skipped (rare concurrent insert)
            row = await execute_query_one(
                """
                SELECT category_id FROM rapid_api_categories
                WHERE external_id = $1 AND vehicle_type_id = $2 AND lang_id = $3
                """,
                ext_cat_id,
                vehicle_type_id,
                lang_id,
            )
            if row:
                category_id = row["category_id"]
            else:
                logger.warning(
                    f"Failed to upsert category external_id={ext_cat_id} for vehicle {vehicle_id}"
                )
                return
        cache[ext_cat_id] = category_id

    # Junction: this vehicle ↔ this category
    vca_id = await new_id("vca", type_code)
    await execute_command(
        """
        INSERT INTO rapid_api_vehicle_categories (vca_id, vehicle_id, category_id)
        VALUES ($1, $2, $3)
        ON CONFLICT (vehicle_id, category_id) DO NOTHING
        """,
        vca_id,
        vehicle_id,
        category_id,
    )

    # Recurse into children
    if isinstance(children, dict) and children:
        child_sort = 0
        for child_node in children.values():
            if isinstance(child_node, dict):
                await _walk_category_tree(
                    node=child_node,
                    parent_category_id=category_id,
                    root_category_id=root_category_id or category_id,
                    vehicle_type_id=vehicle_type_id,
                    type_code=type_code,
                    lang_id=lang_id,
                    vehicle_id=vehicle_id,
                    cache=cache,
                    sort_order=child_sort,
                    parent_path=full_path,
                )
                child_sort += 1


# ==================== HELPERS ====================
def _parse_date(value: Any) -> Optional[date]:
    """API returns dates like '1991-09-01'. Returns None on bad input."""
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _parse_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_decimal(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# ==================== STATUS COUNTERS ====================
async def _refresh_counts(job_id: str) -> dict:
    row = await execute_query_one(
        """
        SELECT
          (SELECT COUNT(*) FROM rapid_api_models)             AS models,
          (SELECT COUNT(*) FROM rapid_api_vehicles)           AS vehicles,
          (SELECT COUNT(*) FROM rapid_api_categories)         AS categories,
          (SELECT COUNT(*) FROM rapid_api_vehicle_categories) AS vca
        """
    )
    counts = {
        "models": int(row["models"]) if row else 0,
        "vehicles": int(row["vehicles"]) if row else 0,
        "categories": int(row["categories"]) if row else 0,
        "vehicle_categories": int(row["vca"]) if row else 0,
    }
    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET models_count             = $2,
            vehicles_count           = $3,
            categories_count         = $4,
            vehicle_categories_count = $5,
            updated_at               = NOW()
        WHERE job_id = $1
        """,
        job_id,
        counts["models"],
        counts["vehicles"],
        counts["categories"],
        counts["vehicle_categories"],
    )
    return counts

"""Phase 2 — Manufacturers + MVT junctions (API 4).

BFS, 11 calls (one per vehicle_type). Idempotent.
- Same external manufacturerId shared across types reuses one `rapid_api_manufacturers` row.
- A row is added to `rapid_api_manufacturer_vehicle_types` for every (mfg, type) pair seen.
"""

from logger import get_logger
from dumper.http_client import api_get
from dumper.id_utils import new_id
from services.db import execute_command, execute_query, execute_query_one

logger = get_logger("dumper.phase2")


async def run(job_id: str) -> dict:
    logger.info("Phase 2 — Manufacturers + MVT")

    types = await execute_query(
        """
        SELECT vehicle_type_id, external_id AS api_type_id, type_code
        FROM rapid_api_vehicle_types
        ORDER BY external_id
        """
    )

    for vt in types:
        await _fetch_manufacturers_for_type(
            api_type_id=int(vt["api_type_id"]),
            vehicle_type_id=vt["vehicle_type_id"],
            type_code=vt["type_code"],
        )

    counts = await _final_counts()

    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET manufacturers_done    = TRUE,
            current_phase         = 'deep_crawl',
            manufacturers_count   = $2,
            mvt_count             = $3,
            updated_at            = NOW()
        WHERE job_id = $1
        """,
        job_id,
        counts["manufacturers"],
        counts["mvt"],
    )

    logger.info(f"Phase 2 done — {counts['manufacturers']} manufacturers, {counts['mvt']} MVT pairs")
    return counts


async def _fetch_manufacturers_for_type(
    api_type_id: int, vehicle_type_id: str, type_code: str
) -> None:
    logger.info(f"Manufacturers for type {api_type_id} ({type_code})")
    data = await api_get(f"/manufacturers/list/type-id/{api_type_id}")
    if not isinstance(data, dict):
        logger.warning(f"Manufacturers API for type {api_type_id} returned: {type(data).__name__}")
        return
    items = data.get("manufacturers", []) or []
    logger.info(f"  → {data.get('countManufactures', len(items))} manufacturers reported")

    for item in items:
        ext_raw = item.get("manufacturerId")
        name = item.get("manufacturerName", "")
        try:
            ext_id = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            continue
        if ext_id is None or not name:
            continue

        manufacturer_id = await _upsert_manufacturer(ext_id, name)
        if manufacturer_id is None:
            continue

        # Junction row (skip if already exists)
        if not await execute_query_one(
            """
            SELECT 1 FROM rapid_api_manufacturer_vehicle_types
            WHERE manufacturer_id = $1 AND vehicle_type_id = $2
            """,
            manufacturer_id,
            vehicle_type_id,
        ):
            mvt_id = await new_id("mvt", type_code)
            await execute_command(
                """
                INSERT INTO rapid_api_manufacturer_vehicle_types (mvt_id, manufacturer_id, vehicle_type_id)
                VALUES ($1, $2, $3)
                ON CONFLICT (manufacturer_id, vehicle_type_id) DO NOTHING
                """,
                mvt_id,
                manufacturer_id,
                vehicle_type_id,
            )


async def _upsert_manufacturer(external_id: int, name: str) -> str | None:
    """Return the manufacturer_id (existing or newly created)."""
    existing = await execute_query_one(
        "SELECT manufacturer_id FROM rapid_api_manufacturers WHERE external_id = $1",
        external_id,
    )
    if existing:
        return existing["manufacturer_id"]

    new_mfg_id = await new_id("manufacturers")
    await execute_command(
        """
        INSERT INTO rapid_api_manufacturers (manufacturer_id, external_id, manufacturer_name)
        VALUES ($1, $2, $3)
        ON CONFLICT (external_id) DO NOTHING
        """,
        new_mfg_id,
        external_id,
        name,
    )
    # Re-fetch in case ON CONFLICT skipped (rare concurrent insert)
    row = await execute_query_one(
        "SELECT manufacturer_id FROM rapid_api_manufacturers WHERE external_id = $1",
        external_id,
    )
    return row["manufacturer_id"] if row else None


async def _final_counts() -> dict:
    mfg = await execute_query_one("SELECT COUNT(*) AS n FROM rapid_api_manufacturers")
    mvt = await execute_query_one("SELECT COUNT(*) AS n FROM rapid_api_manufacturer_vehicle_types")
    return {
        "manufacturers": int(mfg["n"]) if mfg else 0,
        "mvt": int(mvt["n"]) if mvt else 0,
    }

"""Dump runner — crawls Auto Parts Catalog API and stores data into PostgreSQL.

Exercises all 17 RapidAPI endpoints (everything except VIN, which needs a real VIN).

Crawl chain (type_id=1, Passenger Cars) — 13 sequential phases:
  0. Reference          — languages, countries, vehicle types, full category tree (4 calls)
  1. Manufacturers      — 1 call, all manufacturers
  2. Models             — 1 call per manufacturer (up to DUMP_MAX_MANUFACTURERS)
  3. Vehicles (lite)    — 1 call per model (lightweight variant IDs)
  4. Engine Variants    — 1 call per model (full vehicle specs, separate endpoint)
  5. Categories         — 1 call per vehicle
  6. Articles           — 1 call per vehicle+category (POST endpoint)
  7. Article Details    — 1 call per article (full specs, OEM, compatible cars)
  8. Article Media      — 1 call per article (images)
  9. OEM Batch          — 1 call for ALL articles (batch OEM lookup)
  10. Fitment           — 1 call per article (compatible cars by article_no)
  11. Cross-References  — 1 call per article (equivalent parts)
  12. Search            — 2 calls per article (by article_no AND by OEM)

Budget tracked globally. Progress saved to dump_jobs table per phase.
"""

import asyncio
import json
from typing import Optional

import httpx

from app.config import settings
from app.dumper.state import DumpPhase, DumpStatus
from app.logger import get_logger
from app.services.api_key_manager import api_key_manager
from app.services.db import (
    execute_command,
    execute_command_with_return,
    execute_many,
    execute_query,
    execute_query_one,
)

logger = get_logger(__name__)

_dump_task: Optional[asyncio.Task] = None
_stop_requested: bool = False

# Cooldown for HTTP 403 (likely daily/monthly quota exhausted, not transient)
_QUOTA_COOLDOWN_SEC = 3600


# ==================== HTTP HELPERS ====================

async def _make_request(
    method: str,
    path: str,
    params: Optional[dict] = None,
    json_body: Optional[dict] = None,
    tried_keys: Optional[set[str]] = None,
) -> Optional[dict]:
    if tried_keys is None:
        tried_keys = set()

    await asyncio.sleep(settings.DUMP_DELAY_MS / 1000)
    key = await api_key_manager.wait_for_available_key()
    tried_keys.add(key)

    url = f"{settings.RAPIDAPI_BASE_URL}{path}"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(method, url, headers=headers, params=params, json=json_body)

            if resp.status_code in (429, 403):
                body = resp.text[:300]
                logger.warning(
                    f"HTTP {resp.status_code} on {path} | key=...{key[-8:]} | body={body}"
                )
                cooldown = _QUOTA_COOLDOWN_SEC if resp.status_code == 403 else 60
                api_key_manager.mark_rate_limited(key, cooldown_sec=cooldown)

                total_keys = len(settings.rapidapi_keys)
                if len(tried_keys) >= total_keys:
                    logger.error(
                        f"All {total_keys} keys exhausted for {path} — giving up on this call"
                    )
                    return None
                return await _make_request(method, path, params, json_body, tried_keys)

            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            body = e.response.text[:300] if e.response is not None else ""
            logger.error(f"HTTP {e.response.status_code} on {path} | body={body}")
            return None
        except Exception as e:
            logger.error(f"Request error on {path}: {e}")
            return None


async def _api_get(path: str, params: Optional[dict] = None) -> Optional[dict]:
    return await _make_request("GET", path, params=params)


async def _api_post(path: str, json_body: Optional[dict] = None) -> Optional[dict]:
    return await _make_request("POST", path, json_body=json_body)


# ==================== JOB STATE ====================

async def _create_job() -> int:
    row = await execute_command_with_return(
        """
        INSERT INTO dump_jobs (status, current_phase, budget_limit, started_at)
        VALUES ($1, $2, $3, NOW())
        RETURNING id
        """,
        DumpStatus.RUNNING,
        DumpPhase.REFERENCE,
        settings.DUMP_BUDGET,
    )
    return row["id"]


async def _update_job(job_id: int, **kwargs) -> None:
    if not kwargs:
        return
    sets = ", ".join(f"{k} = ${i + 2}" for i, k in enumerate(kwargs))
    values = list(kwargs.values())
    await execute_command(
        f"UPDATE dump_jobs SET {sets}, updated_at = NOW() WHERE id = $1",
        job_id,
        *values,
    )


async def _get_latest_job() -> Optional[dict]:
    row = await execute_query_one("SELECT * FROM dump_jobs ORDER BY id DESC LIMIT 1")
    return dict(row) if row else None


def _check_stop() -> bool:
    return _stop_requested or api_key_manager.remaining_budget() <= 0


# ==================== PHASE 0: REFERENCE ====================

async def _phase_reference(job_id: int) -> None:
    logger.info("Phase: reference (languages, countries, vehicle types, category tree)")
    await _update_job(job_id, current_phase=DumpPhase.REFERENCE)

    langs = await _api_get("/languages/list")
    lang_count = 0
    if isinstance(langs, list):
        rows = [(str(l.get("lngId", "")), l.get("lngIso2"), l.get("lngDescription", "")) for l in langs if l.get("lngId")]
        if rows:
            await execute_many(
                "INSERT INTO languages (lng_id, lng_iso2, lng_description) VALUES ($1, $2, $3) ON CONFLICT (lng_id) DO NOTHING",
                rows,
            )
            lang_count = len(rows)

    countries = await _api_get("/countries/list")
    country_count = 0
    if isinstance(countries, dict):
        items = countries.get("countries", []) or []
        rows = [(c.get("id"), c.get("couCode"), c.get("countryName", "")) for c in items if c.get("id")]
        if rows:
            await execute_many(
                "INSERT INTO countries (id, cou_code, country_name) VALUES ($1, $2, $3) ON CONFLICT (id) DO NOTHING",
                rows,
            )
            country_count = len(rows)

    vt = await _api_get("/types/list-vehicles-type")
    vt_count = 0
    if isinstance(vt, list):
        rows = [(v.get("id"), v.get("vehicleType", "")) for v in vt if v.get("id")]
        if rows:
            await execute_many(
                "INSERT INTO vehicle_types (id, vehicle_type) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING",
                rows,
            )
            vt_count = len(rows)

    tree = await _api_get(
        f"/category/type-id/{settings.DEFAULT_TYPE_ID}"
        f"/list-category-tree-structure/lang-id/{settings.DEFAULT_LANG_ID}"
    )
    if tree:
        await execute_command(
            """
            INSERT INTO category_tree (id, type_id, lang_id, tree_data, fetched_at)
            VALUES (1, $1, $2, $3, NOW())
            ON CONFLICT (id) DO UPDATE SET type_id = $1, lang_id = $2, tree_data = $3, fetched_at = NOW()
            """,
            settings.DEFAULT_TYPE_ID,
            settings.DEFAULT_LANG_ID,
            json.dumps(tree),
        )

    await _update_job(
        job_id,
        reference_done=True,
        languages_count=lang_count,
        countries_count=country_count,
        vehicle_types_count=vt_count,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Reference: {lang_count} langs, {country_count} countries, {vt_count} vehicle types, tree stored")


# ==================== PHASE 1: MANUFACTURERS ====================

async def _phase_manufacturers(job_id: int) -> list[dict]:
    logger.info("Phase: manufacturers")
    await _update_job(job_id, current_phase=DumpPhase.MANUFACTURERS)

    data = await _api_get(f"/manufacturers/list/type-id/{settings.DEFAULT_TYPE_ID}")
    if not data:
        return []

    manufacturers = data.get("manufacturers", []) or []
    rows = [(m["manufacturerId"], m["manufacturerName"], settings.DEFAULT_TYPE_ID) for m in manufacturers]
    if rows:
        await execute_many(
            """
            INSERT INTO manufacturers (manufacturer_id, manufacturer_name, type_id)
            VALUES ($1, $2, $3)
            ON CONFLICT (manufacturer_id) DO NOTHING
            """,
            rows,
        )

    await _update_job(
        job_id,
        manufacturers_done=True,
        manufacturers_count=len(rows),
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Manufacturers stored: {len(rows)}")
    return manufacturers


# ==================== PHASE 2: MODELS ====================

async def _phase_models(job_id: int, manufacturers: list[dict]) -> list[dict]:
    logger.info("Phase: models")
    await _update_job(job_id, current_phase=DumpPhase.MODELS)

    all_models: list[dict] = []
    for mfg in manufacturers[: settings.DUMP_MAX_MANUFACTURERS]:
        if _check_stop():
            break
        mfg_id = mfg["manufacturerId"]
        data = await _api_get(
            f"/models/list/type-id/{settings.DEFAULT_TYPE_ID}"
            f"/manufacturer-id/{mfg_id}"
            f"/lang-id/{settings.DEFAULT_LANG_ID}"
            f"/country-filter-id/{settings.DEFAULT_COUNTRY_ID}"
        )
        if not data:
            continue
        models = data.get("models", []) or []
        rows = [
            (m["modelId"], m["modelName"], mfg_id, m.get("modelYearFrom"), m.get("modelYearTo"))
            for m in models
        ]
        if rows:
            await execute_many(
                """
                INSERT INTO models (model_id, model_name, manufacturer_id, year_from, year_to)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (model_id) DO NOTHING
                """,
                rows,
            )
            all_models.extend(models)

    await _update_job(
        job_id,
        models_done=True,
        models_count=len(all_models),
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Models stored: {len(all_models)}")
    return all_models


# ==================== PHASE 3: VEHICLES (LIGHTWEIGHT) ====================

async def _phase_vehicles(job_id: int, models: list[dict]) -> list[dict]:
    logger.info("Phase: vehicles (lightweight)")
    await _update_job(job_id, current_phase=DumpPhase.VEHICLES)

    all_vehicles: list[dict] = []
    for model in models[: settings.DUMP_MAX_MODELS]:
        if _check_stop():
            break
        model_id = model["modelId"]
        data = await _api_get(
            f"/types/type-id/{settings.DEFAULT_TYPE_ID}"
            f"/list-vehicles-id/{model_id}"
            f"/lang-id/{settings.DEFAULT_LANG_ID}"
            f"/country-filter-id/{settings.DEFAULT_COUNTRY_ID}"
        )
        if not data:
            continue
        vts = data.get("modelTypes", []) or []
        rows = [
            (
                v["vehicleId"],
                model_id,
                v.get("manufacturerName", ""),
                v.get("modelName", ""),
                v.get("typeEngineName", ""),
            )
            for v in vts
        ]
        if rows:
            await execute_many(
                """
                INSERT INTO vehicles (vehicle_id, model_id, manufacturer_name, model_name, engine_name)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (vehicle_id) DO NOTHING
                """,
                rows,
            )
            all_vehicles.extend(vts)

    await _update_job(
        job_id,
        vehicles_done=True,
        vehicles_count=len(all_vehicles),
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Vehicles stored: {len(all_vehicles)}")
    return all_vehicles


# ==================== PHASE 4: ENGINE VARIANTS (FULL SPECS) ====================

async def _phase_engine_variants(job_id: int, models: list[dict]) -> None:
    logger.info("Phase: engine variants (full specs)")
    await _update_job(job_id, current_phase=DumpPhase.ENGINE_VARIANTS)

    total = 0
    for model in models[: settings.DUMP_MAX_MODELS]:
        if _check_stop():
            break
        model_id = model["modelId"]
        data = await _api_get(
            f"/types/type-id/{settings.DEFAULT_TYPE_ID}"
            f"/list-vehicles-types/{model_id}"
            f"/lang-id/{settings.DEFAULT_LANG_ID}"
            f"/country-filter-id/{settings.DEFAULT_COUNTRY_ID}"
        )
        if not data:
            continue
        variants = data.get("modelTypes", []) or []
        rows = []
        for v in variants:
            cylinders = v.get("numberOfCylinders")
            try:
                cylinders = int(cylinders) if cylinders else None
            except (TypeError, ValueError):
                cylinders = None
            rows.append((
                v.get("vehicleId"),
                v.get("manufacturerName"),
                v.get("modelName"),
                v.get("typeEngineName"),
                v.get("constructionIntervalStart"),
                v.get("constructionIntervalEnd"),
                v.get("powerKw"),
                v.get("powerPs"),
                v.get("fuelType"),
                v.get("bodyType"),
                cylinders,
                v.get("capacityLt"),
                v.get("capacityTech"),
                v.get("engineCodes"),
            ))
        rows = [r for r in rows if r[0]]
        if rows:
            await execute_many(
                """
                INSERT INTO engine_variants
                  (vehicle_id, manufacturer_name, model_name, type_engine_name,
                   construction_start, construction_end, power_kw, power_ps,
                   fuel_type, body_type, number_of_cylinders, capacity_lt,
                   capacity_tech, engine_codes)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
                ON CONFLICT (vehicle_id) DO NOTHING
                """,
                rows,
            )
            total += len(rows)

    await _update_job(
        job_id,
        engine_variants_done=True,
        engine_variants_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Engine variants stored: {total}")


# ==================== PHASE 5: CATEGORIES PER VEHICLE ====================

async def _phase_categories(job_id: int, vehicles: list[dict]) -> list[tuple]:
    logger.info("Phase: categories per vehicle")
    await _update_job(job_id, current_phase=DumpPhase.CATEGORIES)

    combos: list[tuple] = []
    total = 0
    for vehicle in vehicles[: settings.DUMP_MAX_VEHICLES]:
        if _check_stop():
            break
        vehicle_id = vehicle["vehicleId"]
        data = await _api_get(
            f"/category/type-id/{settings.DEFAULT_TYPE_ID}"
            f"/products-groups-variant-1/{vehicle_id}/lang-id/{settings.DEFAULT_LANG_ID}"
        )
        if not data:
            continue
        cats = data.get("categories", []) or []
        rows = []
        for c in cats:
            cat_id = c.get("categoryId4") or c.get("categoryId3") or c.get("categoryId2") or c.get("categoryId1")
            cat_name = c.get("categoryName4") or c.get("categoryName3") or c.get("categoryName2") or c.get("categoryName1")
            if cat_id:
                rows.append((vehicle_id, cat_id, cat_name))
                combos.append((vehicle_id, cat_id))
        if rows:
            await execute_many(
                """
                INSERT INTO vehicle_categories (vehicle_id, category_id, category_name)
                VALUES ($1, $2, $3)
                ON CONFLICT (vehicle_id, category_id) DO NOTHING
                """,
                rows,
            )
            total += len(rows)

    await _update_job(
        job_id,
        categories_done=True,
        vehicle_categories_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Vehicle-category pairs stored: {total}")
    return combos


# ==================== PHASE 6: ARTICLES ====================

async def _phase_articles(job_id: int, combos: list[tuple]) -> list[dict]:
    logger.info("Phase: articles (GET /articles/list/...)")
    await _update_job(job_id, current_phase=DumpPhase.ARTICLES)

    all_articles: list[dict] = []
    for vehicle_id, category_id in combos[: settings.DUMP_MAX_ARTICLE_COMBOS]:
        if _check_stop():
            break
        data = await _api_get(
            f"/articles/list/type-id/{settings.DEFAULT_TYPE_ID}"
            f"/vehicle-id/{vehicle_id}"
            f"/category-id/{category_id}"
            f"/lang-id/{settings.DEFAULT_LANG_ID}"
        )
        if not data:
            continue
        articles = data.get("articles", []) or []
        rows = [
            (
                a["articleId"],
                a.get("articleNo", ""),
                a.get("supplierId"),
                a.get("supplierName", ""),
                a.get("articleProductName", ""),
                vehicle_id,
                category_id,
            )
            for a in articles
        ]
        if rows:
            await execute_many(
                """
                INSERT INTO articles
                    (article_id, article_no, supplier_id, supplier_name, product_name, vehicle_id, category_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (article_id, vehicle_id, category_id) DO NOTHING
                """,
                rows,
            )
            all_articles.extend(articles)

    await _update_job(
        job_id,
        articles_done=True,
        articles_count=len(all_articles),
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Articles stored: {len(all_articles)}")
    return all_articles


# ==================== PHASE 7: ARTICLE DETAILS ====================

async def _phase_article_details(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: article details (full specs, OEM, compatible cars)")
    await _update_job(job_id, current_phase=DumpPhase.ARTICLE_DETAILS)

    sample = articles[: settings.DUMP_MAX_ARTICLES_DEEP]
    details_count = 0
    for art in sample:
        if _check_stop():
            break
        article_id = art["articleId"]
        data = await _api_get(
            f"/articles/article-complete-details/type-id/{settings.DEFAULT_TYPE_ID}",
            params={
                "articleId": article_id,
                "langId": settings.DEFAULT_LANG_ID,
                "countryFilterId": settings.DEFAULT_COUNTRY_ID,
            },
        )
        if not data or not isinstance(data, dict):
            continue
        article = data.get("article", {}) or {}
        if not article.get("articleId"):
            continue

        ean = ""
        if isinstance(article.get("eanNo"), dict):
            ean = article["eanNo"].get("eanNumbers", "") or ""

        await execute_command(
            """
            INSERT INTO article_details
              (article_id, article_no, article_product_name, supplier_id, supplier_name, ean_no, s3image, raw_response)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (article_id) DO UPDATE SET raw_response = $8, fetched_at = NOW()
            """,
            article.get("articleId"),
            article.get("articleNo", ""),
            article.get("articleProductName", ""),
            article.get("supplierId"),
            article.get("supplierName", ""),
            ean,
            article.get("s3image"),
            json.dumps(article),
        )

        specs = article.get("allSpecifications") or []
        if specs:
            await execute_command("DELETE FROM article_specs WHERE article_id = $1", article_id)
            spec_rows = [(article_id, s.get("criteriaName"), s.get("criteriaValue")) for s in specs]
            if spec_rows:
                await execute_many(
                    "INSERT INTO article_specs (article_id, criteria_name, criteria_value) VALUES ($1, $2, $3)",
                    spec_rows,
                )

        oems = article.get("oemNo") or []
        if oems:
            await execute_command(
                "DELETE FROM article_oem_refs WHERE article_id = $1 AND source = $2",
                article_id,
                "details",
            )
            oem_rows = [(article_id, o.get("oemBrand"), o.get("oemDisplayNo"), "details") for o in oems]
            await execute_many(
                "INSERT INTO article_oem_refs (article_id, oem_brand, oem_display_no, source) VALUES ($1, $2, $3, $4)",
                oem_rows,
            )

        compats = article.get("compatibleCars") or []
        if compats:
            await execute_command("DELETE FROM article_compatible_cars WHERE article_id = $1", article_id)
            cc_rows = [
                (
                    article_id,
                    c.get("vehicleId"),
                    c.get("modelId"),
                    c.get("manufacturerName"),
                    c.get("modelName"),
                    c.get("typeEngineName"),
                    c.get("constructionIntervalStart"),
                    c.get("constructionIntervalEnd"),
                )
                for c in compats
            ]
            await execute_many(
                """
                INSERT INTO article_compatible_cars
                  (article_id, vehicle_id, model_id, manufacturer_name, model_name,
                   type_engine_name, construction_start, construction_end)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
                """,
                cc_rows,
            )

        details_count += 1

    await _update_job(
        job_id,
        article_details_done=True,
        article_details_count=details_count,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Article details stored: {details_count}")


# ==================== PHASE 8: ARTICLE MEDIA ====================

async def _phase_article_media(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: article media")
    await _update_job(job_id, current_phase=DumpPhase.ARTICLE_MEDIA)

    sample = articles[: settings.DUMP_MAX_ARTICLES_DEEP]
    total = 0
    for art in sample:
        if _check_stop():
            break
        article_id = art["articleId"]
        data = await _api_get(
            "/articles/article-all-media-info",
            params={"articleId": article_id, "langId": settings.DEFAULT_LANG_ID},
        )
        if not isinstance(data, list) or not data:
            continue
        rows = [
            (
                article_id,
                m.get("articleMediaType"),
                m.get("articleMediaFileName"),
                m.get("supplierId"),
                m.get("mediaInformation"),
                m.get("s3image"),
            )
            for m in data
        ]
        if rows:
            await execute_command("DELETE FROM article_media WHERE article_id = $1", article_id)
            await execute_many(
                """
                INSERT INTO article_media
                  (article_id, article_media_type, article_media_file_name,
                   supplier_id, media_information, s3image)
                VALUES ($1,$2,$3,$4,$5,$6)
                """,
                rows,
            )
            total += len(rows)

    await _update_job(
        job_id,
        article_media_done=True,
        article_media_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Article media stored: {total}")


# ==================== PHASE 9: OEM BATCH ====================

async def _phase_oem_batch(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: OEM numbers (batch)")
    await _update_job(job_id, current_phase=DumpPhase.OEM_BATCH)

    sample_ids = [a["articleId"] for a in articles[: settings.DUMP_MAX_ARTICLES_DEEP]]
    total = 0
    if sample_ids and not _check_stop():
        data = await _api_post(
            "/articles/get-oems-by-list-of-articles-ids",
            json_body={"articleIds": sample_ids},
        )
        if isinstance(data, dict):
            for entry in data.get("articles", []) or []:
                aid = entry.get("articleId")
                oems = entry.get("oemNo") or []
                if aid and oems:
                    await execute_command(
                        "DELETE FROM article_oem_refs WHERE article_id = $1 AND source = $2",
                        aid,
                        "batch",
                    )
                    oem_rows = [(aid, o.get("oemBrand"), o.get("oemDisplayNo"), "batch") for o in oems]
                    await execute_many(
                        "INSERT INTO article_oem_refs (article_id, oem_brand, oem_display_no, source) VALUES ($1, $2, $3, $4)",
                        oem_rows,
                    )
                    total += len(oem_rows)

    await _update_job(
        job_id,
        oem_batch_done=True,
        oem_refs_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"OEM refs stored (batch): {total}")


# ==================== PHASE 10: FITMENT ====================

async def _phase_fitment(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: fitment (compatible cars by article_no)")
    await _update_job(job_id, current_phase=DumpPhase.FITMENT)

    sample = articles[: settings.DUMP_MAX_ARTICLES_DEEP]
    total = 0
    for art in sample:
        if _check_stop():
            break
        article_no = art.get("articleNo")
        supplier_id = art.get("supplierId")
        if not article_no or not supplier_id:
            continue
        data = await _api_get(
            f"/articles/get-compatible-cars-by-article-number/type-id/{settings.DEFAULT_TYPE_ID}",
            params={
                "articleNo": article_no,
                "supplierId": supplier_id,
                "langId": settings.DEFAULT_LANG_ID,
                "countryFilterId": settings.DEFAULT_COUNTRY_ID,
            },
        )
        if not data:
            continue
        count = data.get("countArticles", 0) if isinstance(data, dict) else 0
        await execute_command(
            "DELETE FROM article_fitment WHERE article_id = $1",
            art["articleId"],
        )
        await execute_command(
            """
            INSERT INTO article_fitment (article_no, supplier_id, article_id, compatible_count, raw_response)
            VALUES ($1, $2, $3, $4, $5)
            """,
            article_no,
            supplier_id,
            art["articleId"],
            count,
            json.dumps(data),
        )
        total += 1

    await _update_job(
        job_id,
        fitment_done=True,
        fitment_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Fitment lookups stored: {total}")


# ==================== PHASE 11: CROSS-REFERENCES ====================

async def _phase_cross_refs(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: cross-references")
    await _update_job(job_id, current_phase=DumpPhase.CROSS_REFS)

    sample = articles[: settings.DUMP_MAX_ARTICLES_DEEP]
    total = 0
    for art in sample:
        if _check_stop():
            break
        article_id = art["articleId"]
        data = await _api_get(
            f"/artlookup/select-article-cross-references/article-id/{article_id}/lang-id/{settings.DEFAULT_LANG_ID}"
        )
        if data is None:
            continue
        await execute_command("DELETE FROM article_cross_refs WHERE article_id = $1", article_id)
        await execute_command(
            "INSERT INTO article_cross_refs (article_id, raw_response) VALUES ($1, $2)",
            article_id,
            json.dumps(data),
        )
        total += 1

    await _update_job(
        job_id,
        cross_refs_done=True,
        cross_refs_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Cross-references stored: {total}")


# ==================== PHASE 12: SEARCH ====================

async def _phase_search(job_id: int, articles: list[dict]) -> None:
    logger.info("Phase: search (by article number + by OEM)")
    await _update_job(job_id, current_phase=DumpPhase.SEARCH)

    sample = articles[: settings.DUMP_MAX_ARTICLES_DEEP]
    total = 0

    for art in sample:
        if _check_stop():
            break
        article_no = art.get("articleNo")
        if not article_no:
            continue
        data = await _api_get(
            "/artlookup/search-articles-by-article-no",
            params={
                "articleNo": article_no,
                "articleType": "ArticleNumber",
                "langId": settings.DEFAULT_LANG_ID,
            },
        )
        if data is None:
            continue
        count = data.get("countArticles", 0) if isinstance(data, dict) else 0
        await execute_command(
            "DELETE FROM article_search_results WHERE search_type = $1 AND search_no = $2",
            "ArticleNumber",
            article_no,
        )
        await execute_command(
            """
            INSERT INTO article_search_results (search_type, search_no, results_count, raw_response)
            VALUES ($1, $2, $3, $4)
            """,
            "ArticleNumber",
            article_no,
            count,
            json.dumps(data),
        )
        total += 1

    oem_rows = await execute_query(
        """
        SELECT DISTINCT oem_display_no
        FROM article_oem_refs
        WHERE oem_display_no IS NOT NULL AND oem_display_no <> ''
        LIMIT $1
        """,
        settings.DUMP_MAX_ARTICLES_DEEP,
    )
    for row in oem_rows:
        if _check_stop():
            break
        oem_no = row["oem_display_no"]
        data = await _api_get(
            "/artlookup/search-articles-by-article-no",
            params={
                "articleNo": oem_no,
                "articleType": "OENumber",
                "langId": settings.DEFAULT_LANG_ID,
            },
        )
        if data is None:
            continue
        count = data.get("countArticles", 0) if isinstance(data, dict) else 0
        await execute_command(
            "DELETE FROM article_search_results WHERE search_type = $1 AND search_no = $2",
            "OENumber",
            oem_no,
        )
        await execute_command(
            """
            INSERT INTO article_search_results (search_type, search_no, results_count, raw_response)
            VALUES ($1, $2, $3, $4)
            """,
            "OENumber",
            oem_no,
            count,
            json.dumps(data),
        )
        total += 1

    await _update_job(
        job_id,
        search_done=True,
        search_count=total,
        total_api_calls=api_key_manager.total_calls(),
    )
    logger.info(f"Search results stored: {total}")


# ==================== MAIN RUNNER ====================

async def run_dump() -> None:
    global _stop_requested
    _stop_requested = False

    job_id = await _create_job()
    logger.info(f"Dump job #{job_id} started — budget: {settings.DUMP_BUDGET} calls")

    try:
        await _phase_reference(job_id)

        manufacturers = await _phase_manufacturers(job_id)
        if not manufacturers:
            raise RuntimeError("Manufacturers phase returned no data")

        models = await _phase_models(job_id, manufacturers)
        vehicles = await _phase_vehicles(job_id, models)
        await _phase_engine_variants(job_id, models)
        combos = await _phase_categories(job_id, vehicles)
        articles = await _phase_articles(job_id, combos)

        if articles:
            await _phase_article_details(job_id, articles)
            await _phase_article_media(job_id, articles)
            await _phase_oem_batch(job_id, articles)
            await _phase_fitment(job_id, articles)
            await _phase_cross_refs(job_id, articles)
            await _phase_search(job_id, articles)

        final_status = DumpStatus.PAUSED if _stop_requested else DumpStatus.COMPLETED
        await _update_job(
            job_id,
            status=final_status,
            current_phase=DumpPhase.COMPLETED,
            total_api_calls=api_key_manager.total_calls(),
        )
        await execute_command("UPDATE dump_jobs SET completed_at = NOW() WHERE id = $1", job_id)
        logger.info(
            f"Dump job #{job_id} {final_status} — total calls used: {api_key_manager.total_calls()}"
        )

    except asyncio.CancelledError:
        await _update_job(job_id, status=DumpStatus.PAUSED, current_phase=DumpPhase.PAUSED)
        logger.info(f"Dump job #{job_id} cancelled")
    except Exception as e:
        logger.error(f"Dump job #{job_id} failed: {e}")
        await _update_job(
            job_id,
            status=DumpStatus.FAILED,
            current_phase=DumpPhase.FAILED,
            error_message=str(e),
        )


# ==================== PUBLIC CONTROLS ====================

def is_running() -> bool:
    return _dump_task is not None and not _dump_task.done()


async def start() -> dict:
    global _dump_task
    if is_running():
        return {"started": False, "reason": "Dump already running"}
    api_key_manager.setup()
    _dump_task = asyncio.create_task(run_dump())
    return {"started": True, "budget": settings.DUMP_BUDGET}


async def stop() -> dict:
    global _stop_requested, _dump_task
    if not is_running():
        return {"stopped": False, "reason": "No dump is running"}
    _stop_requested = True
    if _dump_task:
        _dump_task.cancel()
    return {"stopped": True}


async def get_status() -> dict:
    job = await _get_latest_job()
    if not job:
        return {"status": "idle", "message": "No dump has been run yet"}
    return {
        "job_id": job["id"],
        "status": job["status"],
        "current_phase": job["current_phase"],
        "budget_limit": job["budget_limit"],
        "total_api_calls": job["total_api_calls"],
        "remaining_budget": max(0, job["budget_limit"] - job["total_api_calls"]),
        "calls_per_key": api_key_manager.calls_per_key(),
        "counts": {
            "languages": job["languages_count"],
            "countries": job["countries_count"],
            "vehicle_types": job["vehicle_types_count"],
            "manufacturers": job["manufacturers_count"],
            "models": job["models_count"],
            "vehicles": job["vehicles_count"],
            "engine_variants": job["engine_variants_count"],
            "vehicle_categories": job["vehicle_categories_count"],
            "articles": job["articles_count"],
            "article_details": job["article_details_count"],
            "article_media": job["article_media_count"],
            "oem_refs": job["oem_refs_count"],
            "fitment": job["fitment_count"],
            "cross_refs": job["cross_refs_count"],
            "search": job["search_count"],
        },
        "phases_done": {
            "reference": job["reference_done"],
            "manufacturers": job["manufacturers_done"],
            "models": job["models_done"],
            "vehicles": job["vehicles_done"],
            "engine_variants": job["engine_variants_done"],
            "categories": job["categories_done"],
            "articles": job["articles_done"],
            "article_details": job["article_details_done"],
            "article_media": job["article_media_done"],
            "oem_batch": job["oem_batch_done"],
            "fitment": job["fitment_done"],
            "cross_refs": job["cross_refs_done"],
            "search": job["search_done"],
        },
        "started_at": job["started_at"].isoformat() if job["started_at"] else None,
        "completed_at": job["completed_at"].isoformat() if job["completed_at"] else None,
        "error_message": job["error_message"],
    }

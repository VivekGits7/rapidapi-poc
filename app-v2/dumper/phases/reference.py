"""Phase 1 — Reference data (Languages, Countries, Vehicle Types).

BFS, 3 fixed API calls. Idempotent: re-running is safe (existence checks + ON CONFLICT DO NOTHING).
"""

from logger import get_logger
from dumper.http_client import api_get
from dumper.id_utils import new_id
from dumper.state import API_NAME_TO_CODE
from dumper.unparsed import UnparsedEntity, UnparsedReason, log_unparsed
from services.db import execute_command, execute_query_one

logger = get_logger("dumper.phase1")


async def run(job_id: str) -> dict:
    logger.info("Phase 1 — Reference (Languages, Countries, Vehicle Types)")

    await _fetch_languages()
    await _fetch_countries()
    await _fetch_vehicle_types()

    counts = await _final_counts()

    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET reference_done       = TRUE,
            current_phase        = 'manufacturers',
            languages_count      = $2,
            countries_count      = $3,
            vehicle_types_count  = $4,
            updated_at           = NOW()
        WHERE job_id = $1
        """,
        job_id,
        counts["languages"],
        counts["countries"],
        counts["vehicle_types"],
    )

    logger.info(
        f"Phase 1 done — {counts['languages']} languages, "
        f"{counts['countries']} countries, {counts['vehicle_types']} vehicle types"
    )
    return counts


# ==================== API 1 — Languages ====================
async def _fetch_languages() -> None:
    path = "/languages/list"
    data = await api_get(path)
    if not isinstance(data, list):
        logger.warning(f"Languages API returned unexpected: {type(data).__name__}")
        await log_unparsed(path, UnparsedEntity.LANGUAGE, data, UnparsedReason.NON_LIST_RESPONSE)
        return
    for item in data:
        if not isinstance(item, dict):
            await log_unparsed(path, UnparsedEntity.LANGUAGE, item, UnparsedReason.NON_DICT_ITEM)
            continue

        ext_raw = item.get("lngId")
        try:
            ext_id = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            await log_unparsed(path, UnparsedEntity.LANGUAGE, item, UnparsedReason.UNPARSEABLE_EXTERNAL_ID)
            continue
        if ext_id is None:
            await log_unparsed(path, UnparsedEntity.LANGUAGE, item, UnparsedReason.MISSING_EXTERNAL_ID)
            continue

        if await execute_query_one(
            "SELECT 1 FROM rapid_api_languages WHERE external_id = $1", ext_id
        ):
            continue

        lang_id = await new_id("languages")
        await execute_command(
            """
            INSERT INTO rapid_api_languages (language_id, external_id, iso_code, description)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (external_id) DO NOTHING
            """,
            lang_id,
            ext_id,
            item.get("lngIso2"),
            item.get("lngDescription", ""),
        )


# ==================== API 2 — Countries ====================
async def _fetch_countries() -> None:
    path = "/countries/list"
    data = await api_get(path)
    if not isinstance(data, dict):
        logger.warning(f"Countries API returned unexpected: {type(data).__name__}")
        await log_unparsed(path, UnparsedEntity.COUNTRY, data, UnparsedReason.NON_LIST_RESPONSE)
        return
    items = data.get("countries", []) or []
    if not isinstance(items, list):
        await log_unparsed(path, UnparsedEntity.COUNTRY, items, UnparsedReason.NON_LIST_RESPONSE)
        items = []
    for item in items:
        if not isinstance(item, dict):
            await log_unparsed(path, UnparsedEntity.COUNTRY, item, UnparsedReason.NON_DICT_ITEM)
            continue

        ext_raw = item.get("id")
        try:
            ext_id = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            await log_unparsed(path, UnparsedEntity.COUNTRY, item, UnparsedReason.UNPARSEABLE_EXTERNAL_ID)
            continue
        if ext_id is None:
            await log_unparsed(path, UnparsedEntity.COUNTRY, item, UnparsedReason.MISSING_EXTERNAL_ID)
            continue

        if await execute_query_one(
            "SELECT 1 FROM rapid_api_countries WHERE external_id = $1", ext_id
        ):
            continue

        cou_id = await new_id("countries")
        await execute_command(
            """
            INSERT INTO rapid_api_countries (country_id, external_id, country_code, country_name)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (external_id) DO NOTHING
            """,
            cou_id,
            ext_id,
            item.get("couCode"),
            item.get("countryName", ""),
        )


# ==================== API 3 — Vehicle Types ====================
async def _fetch_vehicle_types() -> None:
    path = "/types/list-vehicles-type"
    data = await api_get(path)
    if not isinstance(data, list):
        logger.warning(f"Vehicle types API returned unexpected: {type(data).__name__}")
        await log_unparsed(path, UnparsedEntity.VEHICLE_TYPE, data, UnparsedReason.NON_LIST_RESPONSE)
        return
    for item in data:
        if not isinstance(item, dict):
            await log_unparsed(path, UnparsedEntity.VEHICLE_TYPE, item, UnparsedReason.NON_DICT_ITEM)
            continue

        ext_raw = item.get("id")
        name = item.get("vehicleType", "")
        try:
            ext_id = int(ext_raw) if ext_raw is not None else None
        except (TypeError, ValueError):
            await log_unparsed(path, UnparsedEntity.VEHICLE_TYPE, item, UnparsedReason.UNPARSEABLE_EXTERNAL_ID)
            continue
        if ext_id is None:
            await log_unparsed(path, UnparsedEntity.VEHICLE_TYPE, item, UnparsedReason.MISSING_EXTERNAL_ID)
            continue
        if not name:
            await log_unparsed(
                path, UnparsedEntity.VEHICLE_TYPE, item, UnparsedReason.MISSING_EXTERNAL_ID,
                parent_ref={"note": "missing vehicleType name"},
            )
            continue

        type_code = API_NAME_TO_CODE.get(name)
        if not type_code:
            logger.warning(f"Unknown vehicleType name from API: {name!r} (id={ext_id}) — capturing as unparsed")
            await log_unparsed(
                path, UnparsedEntity.VEHICLE_TYPE, item, UnparsedReason.MISSING_EXTERNAL_ID,
                parent_ref={"note": f"unknown vehicleType name {name!r}"},
            )
            continue

        if await execute_query_one(
            "SELECT 1 FROM rapid_api_vehicle_types WHERE external_id = $1", ext_id
        ):
            continue

        vty_id = await new_id("vehicle_types")
        await execute_command(
            """
            INSERT INTO rapid_api_vehicle_types (vehicle_type_id, external_id, name, type_code)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (external_id) DO NOTHING
            """,
            vty_id,
            ext_id,
            name,
            type_code,
        )


async def _final_counts() -> dict:
    lang = await execute_query_one("SELECT COUNT(*) AS n FROM rapid_api_languages")
    cou = await execute_query_one("SELECT COUNT(*) AS n FROM rapid_api_countries")
    vty = await execute_query_one("SELECT COUNT(*) AS n FROM rapid_api_vehicle_types")
    return {
        "languages": int(lang["n"]) if lang else 0,
        "countries": int(cou["n"]) if cou else 0,
        "vehicle_types": int(vty["n"]) if vty else 0,
    }

"""dump_main() — top-level orchestrator for the RapidAPI Auto Parts dump.

Architecture:
  - Phase 1 (BFS, 3 calls):   reference data
  - Phase 2 (BFS, 11 calls):  manufacturers + MVT
  - Phase 3 (DFS, ~440k):     deep crawl of models → vehicles → categories

Resumability:
  - dump_main() picks up an in-flight job if one exists (status in running/paused/failed)
  - Otherwise creates a new one.
  - Per-phase done flags + per-row `*_fetched_at` columns make resume O(1).

Graceful failure modes:
  - AllKeysExhaustedError → mark job 'paused' + exit clean (exit 0).
  - Other exceptions → mark job 'failed' + re-raise.
  - SIGINT / stop signal → check `stop_requested` between iterations + mark paused.
"""

from typing import Any

from logger import get_logger
from error import AllKeysExhaustedError, NoResumableJobError
from dumper.id_utils import new_id
from dumper.key_manager import api_key_manager
from dumper.phases import deep_crawl as phase3
from dumper.phases import manufacturers as phase2
from dumper.phases import reference as phase1
from services.db import (
    close_db_pool,
    create_db_pool,
    execute_command,
    execute_query,
    execute_query_one,
    transaction,
)

logger = get_logger("dumper.runner")


# ==================== JOB LIFECYCLE ====================

async def _get_or_create_job(mode: str) -> str:
    """Return the job_id to use.

    mode='run'    — resume an unfinished job if one exists, else create new
    mode='resume' — resume an unfinished job; raise NoResumableJobError if none
    """
    existing = await execute_query_one(
        """
        SELECT job_id, status, current_phase
        FROM rapid_api_dump_jobs
        WHERE status IN ('running', 'paused', 'failed')
          AND (reference_done = FALSE OR manufacturers_done = FALSE OR deep_crawl_done = FALSE)
        ORDER BY created_at DESC
        LIMIT 1
        """
    )

    if existing:
        if existing["status"] == "running":
            logger.warning(
                f"Job {existing['job_id']} found in status='running' — "
                f"assuming previous process crashed without marking paused. Resuming."
            )
        logger.info(
            f"Resuming job {existing['job_id']} "
            f"(was status={existing['status']}, phase={existing['current_phase']})"
        )
        await execute_command(
            """
            UPDATE rapid_api_dump_jobs
            SET status = 'running',
                stop_requested = FALSE,
                error_message = NULL,
                updated_at = NOW()
            WHERE job_id = $1
            """,
            existing["job_id"],
        )
        return existing["job_id"]

    if mode == "resume":
        raise NoResumableJobError("No paused or failed job to resume")

    job_id = await new_id("dump_jobs")
    await execute_command(
        """
        INSERT INTO rapid_api_dump_jobs (job_id, status, current_phase, started_at)
        VALUES ($1, 'running', 'reference', NOW())
        """,
        job_id,
    )
    logger.info(f"Created new dump job {job_id}")
    return job_id


async def _make_stop_check(job_id: str):
    """Returns an async callable that returns True if a stop has been requested."""

    async def _check() -> bool:
        row = await execute_query_one(
            "SELECT stop_requested FROM rapid_api_dump_jobs WHERE job_id = $1",
            job_id,
        )
        return bool(row and row["stop_requested"])

    return _check


async def _mark_paused(job_id: str, reason: str) -> None:
    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET status = 'paused',
            current_phase = 'paused',
            error_message = $2,
            updated_at = NOW()
        WHERE job_id = $1
        """,
        job_id,
        reason[:500],
    )
    logger.info(f"Job {job_id} → paused: {reason}")


async def _mark_failed(job_id: str, error: str) -> None:
    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET status = 'failed',
            current_phase = 'failed',
            error_message = $2,
            updated_at = NOW()
        WHERE job_id = $1
        """,
        job_id,
        error[:500],
    )


async def _mark_completed(job_id: str) -> None:
    await execute_command(
        """
        UPDATE rapid_api_dump_jobs
        SET status = 'completed',
            current_phase = 'completed',
            completed_at = COALESCE(completed_at, NOW()),
            stop_requested = FALSE,
            updated_at = NOW()
        WHERE job_id = $1
        """,
        job_id,
    )


# ==================== TOP-LEVEL ORCHESTRATION ====================

async def dump_main(mode: str = "run", manage_pool: bool = True) -> dict:
    """Run the dump start-to-end (or resume in-flight).

    manage_pool=True (CLI): creates + closes the DB pool itself.
    manage_pool=False (FastAPI): assumes the pool is already created by the app lifespan
                                  and leaves it open on exit.

    Returns the final job summary dict.
    Raises NoResumableJobError if mode='resume' and no resumable job.
    AllKeysExhaustedError is caught internally → marks job paused → returns normally.
    Other exceptions mark the job failed and re-raise.
    """
    if manage_pool:
        await create_db_pool()
    await api_key_manager.setup()

    job_id = await _get_or_create_job(mode)
    check_stop = await _make_stop_check(job_id)

    try:
        # ---- Phase 1: Reference ----
        job = await execute_query_one(
            "SELECT reference_done FROM rapid_api_dump_jobs WHERE job_id = $1", job_id
        )
        if not job or not job["reference_done"]:
            await execute_command(
                "UPDATE rapid_api_dump_jobs SET current_phase = 'reference', updated_at = NOW() WHERE job_id = $1",
                job_id,
            )
            await phase1.run(job_id)
        else:
            logger.info("Phase 1 (reference) already done — skipping")

        if await check_stop():
            await _mark_paused(job_id, "stop requested after phase 1")
            return await _summary(job_id)

        # ---- Phase 2: Manufacturers ----
        job = await execute_query_one(
            "SELECT manufacturers_done FROM rapid_api_dump_jobs WHERE job_id = $1", job_id
        )
        if not job or not job["manufacturers_done"]:
            await execute_command(
                "UPDATE rapid_api_dump_jobs SET current_phase = 'manufacturers', updated_at = NOW() WHERE job_id = $1",
                job_id,
            )
            await phase2.run(job_id)
        else:
            logger.info("Phase 2 (manufacturers) already done — skipping")

        if await check_stop():
            await _mark_paused(job_id, "stop requested after phase 2")
            return await _summary(job_id)

        # ---- Phase 3: Deep Crawl ----
        job = await execute_query_one(
            "SELECT deep_crawl_done FROM rapid_api_dump_jobs WHERE job_id = $1", job_id
        )
        if not job or not job["deep_crawl_done"]:
            await phase3.run(job_id, check_stop)
        else:
            logger.info("Phase 3 (deep crawl) already done — skipping")

        # ---- Done? ----
        job = await execute_query_one(
            """
            SELECT reference_done, manufacturers_done, deep_crawl_done
            FROM rapid_api_dump_jobs WHERE job_id = $1
            """,
            job_id,
        )
        if job and job["reference_done"] and job["manufacturers_done"] and job["deep_crawl_done"]:
            await _mark_completed(job_id)
            logger.info(f"Dump job {job_id} COMPLETED")
        else:
            await _mark_paused(job_id, "partial completion — see *_done flags")

        return await _summary(job_id)

    except AllKeysExhaustedError as e:
        logger.error(f"All keys exhausted: {e.detail}")
        await _mark_paused(job_id, f"all keys exhausted: {e.detail}")
        return await _summary(job_id)

    except NoResumableJobError:
        raise

    except Exception as e:
        logger.error(f"Dump job {job_id} FAILED: {e}", exc_info=True)
        await _mark_failed(job_id, str(e))
        raise

    finally:
        if manage_pool:
            await close_db_pool()


# ==================== STATUS / CONTROL ====================

async def request_stop(manage_pool: bool = True) -> dict:
    """Set stop_requested=TRUE on the latest running job. Idempotent."""
    if manage_pool:
        await create_db_pool()
    try:
        row = await execute_query_one(
            """
            SELECT job_id FROM rapid_api_dump_jobs
            WHERE status = 'running'
            ORDER BY created_at DESC LIMIT 1
            """
        )
        if not row:
            return {"stopped": False, "message": "No running job to stop"}
        await execute_command(
            "UPDATE rapid_api_dump_jobs SET stop_requested = TRUE, updated_at = NOW() WHERE job_id = $1",
            row["job_id"],
        )
        return {"stopped": True, "job_id": row["job_id"]}
    finally:
        if manage_pool:
            await close_db_pool()


async def get_status(manage_pool: bool = True) -> dict:
    """Return the latest job's state for CLI / API status responses."""
    if manage_pool:
        await create_db_pool()
    try:
        row = await execute_query_one(
            "SELECT * FROM rapid_api_dump_jobs ORDER BY created_at DESC LIMIT 1"
        )
        if not row:
            return {"status": "idle", "message": "No dump has been run yet"}
        keys_summary = await api_key_manager.summary()
        return _row_to_summary(row, keys_summary)
    finally:
        if manage_pool:
            await close_db_pool()


async def get_api_counts(manage_pool: bool = True) -> dict:
    """Return RapidAPI call accounting across all keys.

    Three buckets per key (and aggregated):
      success_calls  — HTTP 200 responses
      failed_calls   — non-200 (429 / 403 / 5xx / other 4xx)
      total_calls    — success + failed

    Also returns a best-effort `pending_estimate` derived from the DFS state
    (rows with NULL `*_fetched_at` cursors) — useful to gauge how much work
    is left vs. done.

    Safe to call any time. If the dumper has never been initialized, returns
    zero-filled totals and an empty `per_key` list.
    """
    if manage_pool:
        await create_db_pool()
    try:
        totals_row = await execute_query_one(
            """
            SELECT COALESCE(SUM(success_calls), 0) AS success,
                   COALESCE(SUM(failed_calls),  0) AS failed,
                   COALESCE(SUM(total_calls),   0) AS total
            FROM rapid_api_api_key_state
            """
        )
        totals = {
            "success_calls": int(totals_row["success"]) if totals_row else 0,
            "failed_calls":  int(totals_row["failed"])  if totals_row else 0,
            "total_calls":   int(totals_row["total"])   if totals_row else 0,
        }

        per_key_rows = await execute_query(
            """
            SELECT key_id, success_calls, failed_calls, total_calls,
                   last_status, last_used_at, cooldown_until
            FROM rapid_api_api_key_state
            ORDER BY key_id
            """
        )
        per_key = [
            {
                "key_id": r["key_id"],
                "success_calls": int(r["success_calls"]),
                "failed_calls":  int(r["failed_calls"]),
                "total_calls":   int(r["total_calls"]),
                "last_status":   r["last_status"],
                "last_used_at":  r["last_used_at"].isoformat() if r["last_used_at"] else None,
                "cooldown_until": r["cooldown_until"].isoformat() if r["cooldown_until"] else None,
            }
            for r in per_key_rows
        ]

        # Best-effort pending estimate from the DFS cursors. Each pending
        # row corresponds to exactly one API call in the deep crawl phase.
        models_pending     = await execute_query_one(
            "SELECT COUNT(*) AS n FROM rapid_api_manufacturer_vehicle_types WHERE models_fetched_at IS NULL"
        )
        vehicles_pending   = await execute_query_one(
            "SELECT COUNT(*) AS n FROM rapid_api_models WHERE vehicles_fetched_at IS NULL"
        )
        categories_pending = await execute_query_one(
            "SELECT COUNT(*) AS n FROM rapid_api_vehicles WHERE categories_fetched_at IS NULL"
        )
        mp = int(models_pending["n"]) if models_pending else 0
        vp = int(vehicles_pending["n"]) if vehicles_pending else 0
        cp = int(categories_pending["n"]) if categories_pending else 0

        pending_estimate = {
            "models_pending":     mp,
            "vehicles_pending":   vp,
            "categories_pending": cp,
            "total_pending":      mp + vp + cp,
        }

        return {
            "totals": totals,
            "per_key": per_key,
            "pending_estimate": pending_estimate,
        }
    finally:
        if manage_pool:
            await close_db_pool()


async def reset_dump(manage_pool: bool = True) -> dict:
    """DANGEROUS: truncate all dump tables + restart sequences. Idempotent."""
    if manage_pool:
        await create_db_pool()
    try:
        async with transaction() as conn:
            tables = [
                "rapid_api_vehicle_categories",
                "rapid_api_categories",
                "rapid_api_vehicles",
                "rapid_api_models",
                "rapid_api_manufacturer_vehicle_types",
                "rapid_api_manufacturers",
                "rapid_api_vehicle_types",
                "rapid_api_countries",
                "rapid_api_languages",
                "rapid_api_dump_jobs",
                "rapid_api_api_key_state",
            ]
            for t in tables:
                await conn.execute(f"TRUNCATE TABLE {t} CASCADE")

            sequences = await conn.fetch(
                "SELECT sequencename FROM pg_sequences WHERE sequencename LIKE 'seq\\_%' ESCAPE '\\'"
            )
            for s in sequences:
                await conn.execute(f"ALTER SEQUENCE {s['sequencename']} RESTART WITH 1")

        logger.warning("Reset complete — all dumped data wiped")
        return {"reset": True, "tables_truncated": len(tables)}
    finally:
        if manage_pool:
            await close_db_pool()


# ==================== INTERNAL: summary builder ====================

async def _summary(job_id: str) -> dict:
    row = await execute_query_one("SELECT * FROM rapid_api_dump_jobs WHERE job_id = $1", job_id)
    if not row:
        return {}
    keys_summary = await api_key_manager.summary()
    return _row_to_summary(row, keys_summary)


def _row_to_summary(row: Any, keys_summary: list[dict]) -> dict:
    return {
        "job_id": row["job_id"],
        "status": row["status"],
        "current_phase": row["current_phase"],
        "stop_requested": row["stop_requested"],
        "phases_done": {
            "reference": row["reference_done"],
            "manufacturers": row["manufacturers_done"],
            "deep_crawl": row["deep_crawl_done"],
        },
        "counts": {
            "languages": row["languages_count"],
            "countries": row["countries_count"],
            "vehicle_types": row["vehicle_types_count"],
            "manufacturers": row["manufacturers_count"],
            "mvt": row["mvt_count"],
            "models": row["models_count"],
            "vehicles": row["vehicles_count"],
            "categories": row["categories_count"],
            "vehicle_categories": row["vehicle_categories_count"],
        },
        "keys": keys_summary,
        "total_api_calls": row["total_api_calls"],
        "started_at": row["started_at"].isoformat() if row["started_at"] else None,
        "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
        "error_message": row["error_message"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
    }

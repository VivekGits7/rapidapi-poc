from fastapi import APIRouter, HTTPException, Request

from app.dumper import runner
from app.error import AppException
from app.limiter import limiter
from app.logger import get_logger
from app.schema.response import COMMON_ERROR_RESPONSES, BadGatewayResponse, BadRequestResponse
from app.schema.schemas import DumpStartResponse, DumpStatusResponse, DumpStatusData, DumpCountsData, DumpPhasesDoneData

logger = get_logger(__name__)

router = APIRouter(prefix="/api/dump", tags=["Dump"])


@router.post(
    "/start",
    response_model=DumpStartResponse,
    summary="Start the catalog dump",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": DumpStartResponse, "description": "Dump started or already running"},
        400: {"model": BadRequestResponse, "description": "Dump already running"},
        502: {"model": BadGatewayResponse, "description": "Failed to start dump"},
    },
)
@limiter.limit("5/minute")
async def start_dump(request: Request) -> DumpStartResponse:
    """
    Start the background catalog dump.

    - Crawls type_id=1 (Passenger Cars): manufacturers → models → vehicles → categories → articles
    - Respects DUMP_BUDGET (300 calls across 3 rotating API keys)
    - Safe to call again if already running — returns current state instead of starting a second job
    - Use GET /api/dump/status to monitor progress
    """
    try:
        if runner.is_running():
            return DumpStartResponse(
                success=True,
                message="Dump is already running",
                data={"running": True},
            )
        result = await runner.start()
        return DumpStartResponse(
            success=True,
            message="Dump started" if result["started"] else result.get("reason", "Not started"),
            data=result,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"start_dump error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/stop",
    response_model=DumpStartResponse,
    summary="Stop (pause) the running dump",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": DumpStartResponse, "description": "Dump stopped or was not running"},
    },
)
@limiter.limit("5/minute")
async def stop_dump(request: Request) -> DumpStartResponse:
    """
    Stop the running dump gracefully.

    - Sets a stop flag — the runner finishes the current API call then halts
    - Progress is saved to the database so the next /start resumes cleanly
    - If no dump is running, returns a safe no-op response
    """
    try:
        result = await runner.stop()
        return DumpStartResponse(
            success=True,
            message="Dump stopped" if result["stopped"] else result.get("reason", "Not stopped"),
            data=result,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"stop_dump error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/status",
    response_model=DumpStatusResponse,
    summary="Get current dump status and progress",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": DumpStatusResponse, "description": "Current dump job status"},
    },
)
@limiter.limit("30/minute")
async def dump_status(request: Request) -> DumpStatusResponse:
    """
    Return the latest dump job's progress.

    - **status**: idle | running | paused | completed | failed
    - **current_phase**: which crawl phase is active (manufacturers/models/vehicles/categories/articles)
    - **total_api_calls**: how many RapidAPI calls have been made
    - **remaining_budget**: calls left before the budget is exhausted
    - **counts**: rows stored per table so far
    - **calls_per_key**: how many calls each of the 3 keys has handled
    """
    try:
        raw = await runner.get_status()

        if "message" in raw and "job_id" not in raw:
            return DumpStatusResponse(
                success=True,
                message=raw["message"],
                data=DumpStatusData(
                    job_id=None,
                    status="idle",
                    current_phase="idle",
                    budget_limit=0,
                    total_api_calls=0,
                    remaining_budget=0,
                    calls_per_key={},
                    counts=DumpCountsData(),
                    phases_done=DumpPhasesDoneData(),
                    started_at=None,
                    completed_at=None,
                    error_message=None,
                ),
            )

        return DumpStatusResponse(
            success=True,
            message=f"Dump {raw['status']}",
            data=DumpStatusData(
                job_id=raw["job_id"],
                status=raw["status"],
                current_phase=raw["current_phase"],
                budget_limit=raw["budget_limit"],
                total_api_calls=raw["total_api_calls"],
                remaining_budget=raw["remaining_budget"],
                calls_per_key=raw["calls_per_key"],
                counts=DumpCountsData(**raw["counts"]),
                phases_done=DumpPhasesDoneData(**raw["phases_done"]),
                started_at=raw["started_at"],
                completed_at=raw["completed_at"],
                error_message=raw["error_message"],
            ),
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"dump_status error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

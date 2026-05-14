"""Pydantic schemas for the /api/dump/* control-surface endpoints."""

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from schema.response import BaseResponse


# ==================== NESTED DATA MODELS ====================

class PhasesDone(BaseModel):
    reference: bool = Field(..., description="API 1/2/3 (Languages, Countries, Vehicle Types) complete")
    manufacturers: bool = Field(..., description="API 4 across all 11 vehicle types complete")
    deep_crawl: bool = Field(..., description="DFS crawl of all models/vehicles/categories complete")


class PhaseCounts(BaseModel):
    languages: int = Field(..., examples=[42])
    countries: int = Field(..., examples=[283])
    vehicle_types: int = Field(..., examples=[11])
    manufacturers: int = Field(..., examples=[698])
    mvt: int = Field(..., examples=[2200], description="manufacturer_vehicle_types junction rows")
    models: int = Field(..., examples=[40000])
    vehicles: int = Field(..., examples=[400000])
    categories: int = Field(..., examples=[3500])
    vehicle_categories: int = Field(..., examples=[50000000])


class KeySummary(BaseModel):
    key_id: str = Field(..., examples=["KEY_1"])
    cooldown_until: Optional[str] = Field(None, description="ISO-8601 datetime; null if available now")
    calls_today: int = Field(..., examples=[1240], description="Legacy success-only daily bucket")
    calls_month: int = Field(..., examples=[18450], description="Legacy success-only monthly bucket")
    success_calls: int = Field(..., examples=[103950], description="HTTP 200 responses")
    failed_calls:  int = Field(..., examples=[32],     description="Non-200 responses (429, 403, 5xx, other 4xx)")
    total_calls:   int = Field(..., examples=[103982], description="success_calls + failed_calls")
    last_used_at: Optional[str] = None
    last_status: Optional[int] = Field(None, examples=[200])


# ==================== API-CALL COUNTS ENDPOINT ====================

class ApiCallTotals(BaseModel):
    """Aggregated call counts across every RapidAPI key."""

    success_calls: int = Field(..., examples=[442150], description="Calls returning HTTP 200")
    failed_calls:  int = Field(..., examples=[37],     description="Non-200 responses (429, 403, 5xx, other 4xx)")
    total_calls:   int = Field(..., examples=[442187], description="success_calls + failed_calls — every call that reached RapidAPI")


class KeyApiCounts(BaseModel):
    """Per-key call counts + most-recent state."""

    key_id: str = Field(..., examples=["KEY_1"])
    success_calls: int = Field(..., examples=[110540])
    failed_calls:  int = Field(..., examples=[8])
    total_calls:   int = Field(..., examples=[110548])
    last_status: Optional[int] = Field(None, examples=[200])
    last_used_at: Optional[str] = Field(None, description="ISO-8601 datetime")
    cooldown_until: Optional[str] = Field(None, description="ISO-8601 datetime; null if available now")


class PendingEstimate(BaseModel):
    """Best-effort estimate of API calls still to make, derived from DFS cursors.

    Each pending row corresponds to exactly one API call in the deep-crawl
    phase. Reference + manufacturers phases are excluded — they're tiny (14
    total) and only relevant for the very first run.
    """

    models_pending:     int = Field(..., examples=[5],     description="MVT rows with models_fetched_at IS NULL")
    vehicles_pending:   int = Field(..., examples=[1200],  description="Models with vehicles_fetched_at IS NULL")
    categories_pending: int = Field(..., examples=[45000], description="Vehicles with categories_fetched_at IS NULL")
    total_pending:      int = Field(..., examples=[46205], description="Sum of the three buckets above")


class ApiCountsData(BaseModel):
    totals:           ApiCallTotals
    per_key:          List[KeyApiCounts]
    pending_estimate: PendingEstimate


class ApiCountsResponse(BaseResponse):
    data: ApiCountsData

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "API call counts",
            "data": {
                "totals": {
                    "success_calls": 442150,
                    "failed_calls":  37,
                    "total_calls":   442187,
                },
                "per_key": [
                    {
                        "key_id": "KEY_1",
                        "success_calls": 110540, "failed_calls": 8, "total_calls": 110548,
                        "last_status": 200,
                        "last_used_at": "2026-05-14T01:23:45+00:00",
                        "cooldown_until": None,
                    },
                    {
                        "key_id": "KEY_2",
                        "success_calls": 110603, "failed_calls": 12, "total_calls": 110615,
                        "last_status": 429,
                        "last_used_at": "2026-05-14T01:23:42+00:00",
                        "cooldown_until": "2026-05-14T01:33:42+00:00",
                    },
                ],
                "pending_estimate": {
                    "models_pending": 0,
                    "vehicles_pending": 1200,
                    "categories_pending": 45000,
                    "total_pending": 46200,
                },
            },
        }
    })


# ==================== ENDPOINT REQUESTS ====================

class StartDumpRequest(BaseModel):
    mode: Literal["run", "resume"] = Field(
        default="run",
        description=(
            "`run` — pick up an in-flight job if one exists, else create new. "
            "`resume` — error if no job to resume."
        ),
    )


# ==================== ENDPOINT RESPONSES ====================

class DumpJobSummary(BaseModel):
    """Single-job state. Used by start/status/stop/resume."""

    job_id: Optional[str] = Field(None, examples=["JOB_001"])
    status: str = Field(..., examples=["running"], description="idle | running | paused | completed | failed")
    current_phase: str = Field(..., examples=["deep_crawl"])
    stop_requested: Optional[bool] = Field(None, description="True if a graceful stop has been signalled")
    phases_done: Optional[PhasesDone] = None
    counts: Optional[PhaseCounts] = None
    keys: Optional[List[KeySummary]] = None
    total_api_calls: Optional[int] = Field(None, examples=[442187])
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    message: Optional[str] = Field(None, description="Set when status='idle' or no job has run yet")


class StartDumpResponse(BaseResponse):
    job: DumpJobSummary

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "Dump started in the background. Poll GET /api/dump/status for progress.",
            "job": {
                "job_id": "JOB_001",
                "status": "running",
                "current_phase": "reference",
                "stop_requested": False,
                "phases_done": {"reference": False, "manufacturers": False, "deep_crawl": False},
                "counts": {
                    "languages": 0, "countries": 0, "vehicle_types": 0,
                    "manufacturers": 0, "mvt": 0, "models": 0,
                    "vehicles": 0, "categories": 0, "vehicle_categories": 0,
                },
                "total_api_calls": 0,
                "started_at": "2026-05-14T01:23:45Z",
            },
        }
    })


class StatusDumpResponse(BaseResponse):
    job: DumpJobSummary

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "Latest job state",
            "job": {
                "job_id": "JOB_001",
                "status": "running",
                "current_phase": "deep_crawl",
                "stop_requested": False,
                "phases_done": {"reference": True, "manufacturers": True, "deep_crawl": False},
                "counts": {
                    "languages": 42, "countries": 283, "vehicle_types": 11,
                    "manufacturers": 698, "mvt": 2200, "models": 13420,
                    "vehicles": 87231, "categories": 980, "vehicle_categories": 12450000,
                },
                "keys": [
                    {"key_id": "KEY_1", "cooldown_until": None, "calls_today": 1240,
                     "calls_month": 18450, "success_calls": 103950, "failed_calls": 32,
                     "total_calls": 103982,
                     "last_used_at": "2026-05-14T01:23:45Z", "last_status": 200}
                ],
                "total_api_calls": 442187,
                "started_at": "2026-05-14T00:00:00Z",
            },
        }
    })


class StopDumpResponse(BaseResponse):
    job_id: Optional[str] = Field(None, examples=["JOB_001"])
    stopped: bool = Field(..., description="True if a running job was successfully signalled")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "Stop signal sent — dump will pause at next checkpoint.",
            "job_id": "JOB_001",
            "stopped": True,
        }
    })


class ResetDumpResponse(BaseResponse):
    reset: bool
    tables_truncated: int = Field(..., examples=[11])

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "All dump data wiped. Sequences restarted at 1.",
            "reset": True,
            "tables_truncated": 11,
        }
    })

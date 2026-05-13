import json
from typing import Any

from fastapi import APIRouter, HTTPException, Path, Request

from app.error import AppException
from app.limiter import limiter
from app.logger import get_logger
from app.schema.response import (
    BadGatewayResponse,
    BadRequestResponse,
    COMMON_ERROR_RESPONSES,
)
from app.schema.schemas import VinDecodeResponse
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/vin", tags=["VIN"])


def _parse_vin_response(raw: Any) -> Any:
    """The VIN decoder v5 returns `content` as JSON strings — parse them to nested dicts."""
    if not isinstance(raw, dict):
        return raw
    parsed = {}
    for key, sub in raw.items():
        if isinstance(sub, dict) and "content" in sub:
            content = sub.get("content")
            try:
                parsed[key] = json.loads(content) if isinstance(content, str) else content
            except (json.JSONDecodeError, TypeError):
                parsed[key] = content
        else:
            parsed[key] = sub
    return parsed


@router.get(
    "/decode/{vin}",
    response_model=VinDecodeResponse,
    summary="Decode a VIN",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": VinDecodeResponse, "description": "VIN decoded successfully"},
        400: {"model": BadRequestResponse, "description": "Invalid VIN format"},
        502: {"model": BadGatewayResponse, "description": "VIN decoder upstream error"},
    },
)
@limiter.limit("30/minute")
async def decode_vin(
    request: Request,
    vin: str = Path(
        ...,
        min_length=17,
        max_length=17,
        description="17-character VIN",
        examples=["WDBFA68F42F202731"],
    ),
) -> VinDecodeResponse:
    """
    Decode a Vehicle Identification Number using the all-in-one decoder (v1+v2+v3 combined).

    - **vin** (path, required): 17-character VIN
    - Returns make, model, year, engine, transmission, and more
    """
    try:
        raw = await rapidapi_service.get(f"/vin/decoder-v5/{vin}")
        parsed = _parse_vin_response(raw)
        return VinDecodeResponse(
            success=True,
            message="VIN decoded successfully",
            data=parsed,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"decode_vin error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

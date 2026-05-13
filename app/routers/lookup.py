from fastapi import APIRouter, HTTPException, Request

from app.error import AppException
from app.limiter import limiter
from app.logger import get_logger
from app.schema.response import (
    BadGatewayResponse,
    COMMON_ERROR_RESPONSES,
)
from app.schema.schemas import CountriesResponse, LanguagesResponse
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/lookup", tags=["Lookup"])


@router.get(
    "/languages",
    response_model=LanguagesResponse,
    summary="List all supported languages",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": LanguagesResponse, "description": "Languages fetched"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("30/minute")
async def list_languages(request: Request) -> LanguagesResponse:
    """
    List every language supported by the catalog.
    Use the `lngId` value as the `lang_id` query param on other endpoints.

    - No parameters required
    - Common IDs: `4` = English (GB), `37` = English (USA), `42` = Arabic, `6` = French
    """
    try:
        data = await rapidapi_service.get("/languages/list")
        return LanguagesResponse(
            success=True,
            message=f"Fetched {len(data) if isinstance(data, list) else 0} languages",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_languages error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/countries",
    response_model=CountriesResponse,
    summary="List all supported countries/regions",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": CountriesResponse, "description": "Countries fetched"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("30/minute")
async def list_countries(request: Request) -> CountriesResponse:
    """
    List every country and regional grouping supported by the catalog.
    Use the `id` value as the `country_id` query param on other endpoints.

    - No parameters required
    - Common IDs: `63` = Germany, `261` = USA, `259` = UAE, `93` = Great Britain
    - `couCode` uses the catalog's own scheme — NOT always ISO 3166 (e.g., `D` = Germany)
    """
    try:
        data = await rapidapi_service.get("/countries/list")
        count = len(data.get("countries", [])) if isinstance(data, dict) else 0
        return CountriesResponse(
            success=True,
            message=f"Fetched {count} countries",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_countries error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
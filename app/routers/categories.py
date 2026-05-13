from fastapi import APIRouter, HTTPException, Query, Request

from app.config import settings
from app.error import AppException
from app.limiter import limiter
from app.logger import get_logger
from app.schema.response import (
    BadGatewayResponse,
    BadRequestResponse,
    COMMON_ERROR_RESPONSES,
)
from app.schema.schemas import (
    CategoriesAllResponse,
    CategoriesByVehicleResponse,
)
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get(
    "/",
    response_model=CategoriesAllResponse,
    summary="List full category tree",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": CategoriesAllResponse, "description": "Full category tree fetched"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("30/minute")
async def list_all_categories(
    request: Request,
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> CategoriesAllResponse:
    """
    Return the full parts category tree for a vehicle type.

    - **type_id** (query, optional): Vehicle type ID. Default: config `1` (Passenger Car)
    - **lang_id** (query, optional): Language ID. Default: config `4`
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        path = f"/category/type-id/{type_id}/list-category-tree-structure/lang-id/{lang_id}"
        data = await rapidapi_service.get(path)
        return CategoriesAllResponse(
            success=True,
            message="Fetched full category tree",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_all_categories error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/by-vehicle",
    response_model=CategoriesByVehicleResponse,
    summary="List categories available for a specific vehicle",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": CategoriesByVehicleResponse, "description": "Vehicle-scoped categories fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid vehicle_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_categories_by_vehicle(
    request: Request,
    vehicle_id: int = Query(..., ge=1, description="Vehicle ID", examples=[19942]),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> CategoriesByVehicleResponse:
    """
    Return the category tree filtered to a specific vehicle — only categories
    with available parts for that vehicle are included.

    - **vehicle_id** (query, required): Vehicle ID from `/api/vehicles/variants`
    - **type_id** (query, optional): Default: config `1`
    - **lang_id** (query, optional): Default: config `4`
    - Returns flat breadcrumb rows with levels 1-4 encoded in numbered columns
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        path = (
            f"/category/type-id/{type_id}"
            f"/products-groups-variant-1/{vehicle_id}"
            f"/lang-id/{lang_id}"
        )
        data = await rapidapi_service.get(path)
        count = len(data.get("categories", [])) if isinstance(data, dict) else 0
        return CategoriesByVehicleResponse(
            success=True,
            message=f"Fetched {count} category rows for vehicle {vehicle_id}",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_categories_by_vehicle error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
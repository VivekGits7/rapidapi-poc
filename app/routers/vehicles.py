from fastapi import APIRouter, HTTPException, Query, Request, status

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
    EngineVariantsResponse,
    ManufacturersResponse,
    ModelsResponse,
    VehicleTypesResponse,
    VehicleVariantsResponse,
)
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])


@router.get(
    "/types",
    response_model=VehicleTypesResponse,
    summary="List vehicle types",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": VehicleTypesResponse, "description": "Vehicle types fetched"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_vehicle_types(request: Request) -> VehicleTypesResponse:
    """
    List all vehicle type categories (PC, CV, LCV, Motorcycle, etc.).

    - No parameters required
    - Use returned `id` in subsequent manufacturer/model calls
    """
    try:
        data = await rapidapi_service.get("/types/list-vehicles-type")
        return VehicleTypesResponse(
            success=True,
            message=f"Fetched {len(data)} vehicle types",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_vehicle_types error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/makes",
    response_model=ManufacturersResponse,
    summary="List manufacturers by vehicle type",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ManufacturersResponse, "description": "Manufacturers fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid type_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_manufacturers(
    request: Request,
    type_id: int = Query(
        default=None,
        ge=1,
        description="Vehicle type ID (defaults to config DEFAULT_TYPE_ID=1 = Passenger Car)",
        examples=[1],
    ),
) -> ManufacturersResponse:
    """
    List all manufacturers (makes) for a given vehicle type.

    - **type_id** (query, optional): Vehicle type ID. Default: `1` (Passenger Car)
    - Returns all brands available for that type (e.g., TOYOTA, HYUNDAI)
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        data = await rapidapi_service.get(f"/manufacturers/list/type-id/{type_id}")
        return ManufacturersResponse(
            success=True,
            message=f"Fetched {data.get('countManufactures', 0)} manufacturers",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_manufacturers error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/models",
    response_model=ModelsResponse,
    summary="List models for a manufacturer",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ModelsResponse, "description": "Models fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid manufacturer_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_models(
    request: Request,
    manufacturer_id: int = Query(..., ge=1, description="Manufacturer ID from /makes", examples=[111]),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
    country_id: int = Query(default=None, ge=1, description="Country filter ID (defaults to config)"),
) -> ModelsResponse:
    """
    List all models for a given manufacturer, scoped to type/language/country.

    - **manufacturer_id** (query, required): Manufacturer ID (e.g., `111` = TOYOTA)
    - **type_id** (query, optional): Vehicle type ID. Default: config `1`
    - **lang_id** (query, optional): Language ID. Default: config `4`
    - **country_id** (query, optional): Country filter ID. Default: config `63`
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        country_id = country_id or settings.DEFAULT_COUNTRY_ID
        path = (
            f"/models/list/type-id/{type_id}"
            f"/manufacturer-id/{manufacturer_id}"
            f"/lang-id/{lang_id}"
            f"/country-filter-id/{country_id}"
        )
        data = await rapidapi_service.get(path)
        return ModelsResponse(
            success=True,
            message=f"Fetched {data.get('countModels', 0)} models",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_models error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/engines",
    response_model=EngineVariantsResponse,
    summary="List engine variants for a model",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": EngineVariantsResponse, "description": "Engine variants fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid model_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_engine_variants(
    request: Request,
    model_id: int = Query(..., ge=1, description="Model ID from /models", examples=[5626]),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
    country_id: int = Query(default=None, ge=1, description="Country filter ID (defaults to config)"),
) -> EngineVariantsResponse:
    """
    List all engine/trim variants for a model with full technical specs.

    - **model_id** (query, required): Model ID from `/models`
    - **type_id** (query, optional): Vehicle type ID. Default: config `1`
    - **lang_id** (query, optional): Language ID. Default: config `4`
    - **country_id** (query, optional): Country filter ID. Default: config `63`
    - Returns power, fuel type, displacement, engine codes per variant
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        country_id = country_id or settings.DEFAULT_COUNTRY_ID
        path = (
            f"/types/type-id/{type_id}"
            f"/list-vehicles-types/{model_id}"
            f"/lang-id/{lang_id}"
            f"/country-filter-id/{country_id}"
        )
        data = await rapidapi_service.get(path)
        return EngineVariantsResponse(
            success=True,
            message=f"Fetched {data.get('countModelTypes', 0)} engine variants",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_engine_variants error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/variants",
    response_model=VehicleVariantsResponse,
    summary="List vehicle variant IDs for a model (lightweight)",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": VehicleVariantsResponse, "description": "Vehicle variants fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid model_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_vehicle_variants(
    request: Request,
    model_id: int = Query(..., ge=1, description="Model ID from /models", examples=[5626]),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
    country_id: int = Query(default=None, ge=1, description="Country filter ID (defaults to config)"),
) -> VehicleVariantsResponse:
    """
    Lightweight list of all vehicle variants (trim IDs + engine labels) for a model.
    Faster than /engines when you only need vehicleId values for parts lookups.

    - **model_id** (query, required): Model ID from `/models`
    - **type_id** (query, optional): Default: config `1`
    - **lang_id** (query, optional): Default: config `4`
    - **country_id** (query, optional): Default: config `63`
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        country_id = country_id or settings.DEFAULT_COUNTRY_ID
        path = (
            f"/types/type-id/{type_id}"
            f"/list-vehicles-id/{model_id}"
            f"/lang-id/{lang_id}"
            f"/country-filter-id/{country_id}"
        )
        data = await rapidapi_service.get(path)
        return VehicleVariantsResponse(
            success=True,
            message=f"Fetched {data.get('countModelTypes', 0)} vehicle variants",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_vehicle_variants error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
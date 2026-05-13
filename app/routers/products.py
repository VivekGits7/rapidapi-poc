from fastapi import APIRouter, HTTPException, Query, Request

from app.config import settings
from app.error import AppException, NotFoundException
from app.limiter import limiter
from app.logger import get_logger
from app.schema.response import (
    BadGatewayResponse,
    BadRequestResponse,
    COMMON_ERROR_RESPONSES,
    NotFoundResponse,
)
from app.schema.schemas import (
    ArticleDetailsRequest,
    ArticleDetailsResponse,
    ArticleListResponse,
    ArticleMediaResponse,
    CrossReferencesResponse,
    FitmentResponse,
    OEMNumbersRequest,
    OEMNumbersResponse,
)
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get(
    "/",
    response_model=ArticleListResponse,
    summary="List articles (parts) by vehicle and category",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ArticleListResponse, "description": "Article list fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid vehicle_id or category_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def list_articles(
    request: Request,
    vehicle_id: int = Query(..., ge=1, description="Vehicle ID", examples=[19942]),
    category_id: int = Query(..., ge=1, description="Category ID", examples=[100260]),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
) -> ArticleListResponse:
    """
    List all compatible articles (parts) for a vehicle + category combo.
    This is the core "browse parts for my car" endpoint.

    - **vehicle_id** (query, required): Vehicle ID
    - **category_id** (query, required): Category ID
    - **lang_id** (query, optional): Default: config `4`
    - **type_id** (query, optional): Default: config `1`
    """
    try:
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        type_id = type_id or settings.DEFAULT_TYPE_ID
        path = (
            f"/articles/list/type-id/{type_id}"
            f"/vehicle-id/{vehicle_id}"
            f"/category-id/{category_id}"
            f"/lang-id/{lang_id}"
        )
        data = await rapidapi_service.get(path)
        return ArticleListResponse(
            success=True,
            message=f"Fetched {data.get('countArticles', 0)} articles",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"list_articles error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/details",
    response_model=ArticleDetailsResponse,
    summary="Get full article details by article ID",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ArticleDetailsResponse, "description": "Full article details fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_id"},
        404: {"model": NotFoundResponse, "description": "Article not found in catalog"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def get_article_details(
    request: Request,
    body: ArticleDetailsRequest,
) -> ArticleDetailsResponse:
    """
    Return the most complete article record — specs, EAN, OEM, image, compatible cars.

    - **articleId** (body, required): Article ID
    - **langId** (body, optional): Language ID. Default: config `4`
    - **typeId** (body, optional): Vehicle type ID. Default: config `1`
    - **countryFilterId** (body, optional): Country filter ID. Default: config `63`
    - Returns `allSpecifications`, `eanNo`, `oemNo[]`, `s3image`, and `compatibleCars[]`
    """
    try:
        type_id = body.typeId or settings.DEFAULT_TYPE_ID
        lang_id = body.langId or settings.DEFAULT_LANG_ID
        country_id = body.countryFilterId or settings.DEFAULT_COUNTRY_ID
        data = await rapidapi_service.get(
            f"/articles/article-complete-details/type-id/{type_id}",
            params={
                "articleId": body.articleId,
                "langId": lang_id,
                "countryFilterId": country_id,
            },
        )
        if not data or not isinstance(data, dict) or not data.get("article") or not data["article"].get("articleId"):
            raise NotFoundException(f"Article {body.articleId} not found in catalog")
        return ArticleDetailsResponse(
            success=True,
            message=f"Fetched details for article {body.articleId}",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"get_article_details error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/media",
    response_model=ArticleMediaResponse,
    summary="Get article media (images, drawings) by article ID",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ArticleMediaResponse, "description": "Media assets fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def get_article_media(
    request: Request,
    article_id: int = Query(..., ge=1, description="Article ID", examples=[125]),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> ArticleMediaResponse:
    """
    Return all media assets for an article (images, technical drawings, PDFs).

    - **article_id** (query, required): Article ID
    - **lang_id** (query, optional): Default: config `4`
    - Empty array `[]` if the article has no media
    """
    try:
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        data = await rapidapi_service.get(
            "/articles/article-all-media-info",
            params={"articleId": article_id, "langId": lang_id},
        )
        return ArticleMediaResponse(
            success=True,
            message=f"Fetched {len(data) if isinstance(data, list) else 0} media items",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"get_article_media error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/oem-numbers",
    response_model=OEMNumbersResponse,
    summary="Get OEM numbers for a batch of article IDs",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": OEMNumbersResponse, "description": "OEM cross-references fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_ids"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("30/minute")
async def get_oem_numbers(
    request: Request,
    body: OEMNumbersRequest,
) -> OEMNumbersResponse:
    """
    Return OEM cross-reference numbers for a batch of article IDs.

    - **articleIds** (body, required): List of Article IDs (max 100)
    - Batch endpoint — avoids N+1 calls when enriching search results
    - OEM numbers may appear with or without hyphens — normalize before comparing
    """
    try:
        data = await rapidapi_service.post(
            "/articles/get-oems-by-list-of-articles-ids",
            json={"articleIds": body.articleIds},
        )
        return OEMNumbersResponse(
            success=True,
            message=f"Fetched OEM numbers for {data.get('count', 0)} articles",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"get_oem_numbers error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/fitment",
    response_model=FitmentResponse,
    summary="Get compatible vehicles for an article number",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": FitmentResponse, "description": "Compatible vehicles fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_no or supplier_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def get_fitment(
    request: Request,
    article_no: str = Query(..., min_length=1, description="Supplier part number", examples=["C 2029"]),
    supplier_id: int = Query(..., ge=1, description="Supplier ID", examples=[4]),
    type_id: int = Query(default=None, ge=1, description="Vehicle type ID (defaults to config)"),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
    country_id: int = Query(default=None, ge=1, description="Country filter ID (defaults to config)"),
) -> FitmentResponse:
    """
    Reverse fitment lookup — given a supplier part number, return all vehicles it fits.

    - **article_no** (query, required): Supplier part number (spaces allowed, auto URL-encoded)
    - **supplier_id** (query, required): Supplier ID
    - **type_id** (query, optional): Default: config `1`
    - **lang_id** (query, optional): Default: config `4`
    - **country_id** (query, optional): Default: config `63`
    """
    try:
        type_id = type_id or settings.DEFAULT_TYPE_ID
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        country_id = country_id or settings.DEFAULT_COUNTRY_ID
        data = await rapidapi_service.get(
            f"/articles/get-compatible-cars-by-article-number/type-id/{type_id}",
            params={
                "articleNo": article_no,
                "supplierId": supplier_id,
                "langId": lang_id,
                "countryFilterId": country_id,
            },
        )
        return FitmentResponse(
            success=True,
            message=f"Fetched fitment for article {article_no}",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"get_fitment error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/cross-references",
    response_model=CrossReferencesResponse,
    summary="Get cross-references by article ID",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": CrossReferencesResponse, "description": "Cross-references fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_id"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def get_cross_references(
    request: Request,
    article_id: int = Query(..., ge=1, description="Article ID", examples=[131540]),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> CrossReferencesResponse:
    """
    Return all equivalent/interchangeable parts from other suppliers.

    - **article_id** (query, required): Article ID
    - **lang_id** (query, optional): Default: config `4`
    - All results share the same `articleProductName` (functionally equivalent parts)
    """
    try:
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        path = f"/artlookup/select-article-cross-references/article-id/{article_id}/lang-id/{lang_id}"
        data = await rapidapi_service.get(path)
        return CrossReferencesResponse(
            success=True,
            message=f"Fetched cross-references for article {article_id}",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"get_cross_references error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
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
from app.schema.schemas import ArticleSearchResponse, ArticleSearchType
from app.services.rapidapi_service import rapidapi_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api/search", tags=["Search"])


async def _article_search(article_no: str, article_type: str, lang_id: int):
    return await rapidapi_service.get(
        "/artlookup/search-articles-by-article-no",
        params={
            "articleNo": article_no,
            "articleType": article_type,
            "langId": lang_id,
        },
    )


@router.get(
    "/by-article-no",
    response_model=ArticleSearchResponse,
    summary="Search articles by supplier part number",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ArticleSearchResponse, "description": "Search results fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid article_no"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def search_by_article_no(
    request: Request,
    article_no: str = Query(..., min_length=1, description="Supplier part number", examples=["0 242 236 561"]),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> ArticleSearchResponse:
    """
    Search for parts by supplier article number.

    - **article_no** (query, required): Supplier part number (spaces auto URL-encoded)
    - **lang_id** (query, optional): Default: config `4`
    - Returns matching articles with images and supplier info
    """
    try:
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        data = await _article_search(article_no, ArticleSearchType.ARTICLE_NUMBER.value, lang_id)
        return ArticleSearchResponse(
            success=True,
            message=f"Found {data.get('countArticles', 0)} articles",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"search_by_article_no error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/by-oem-no",
    response_model=ArticleSearchResponse,
    summary="Search articles by OEM number",
    responses={
        **COMMON_ERROR_RESPONSES,
        200: {"model": ArticleSearchResponse, "description": "Search results fetched"},
        400: {"model": BadRequestResponse, "description": "Invalid oem_no"},
        502: {"model": BadGatewayResponse, "description": "Upstream error"},
    },
)
@limiter.limit("60/minute")
async def search_by_oem_no(
    request: Request,
    oem_no: str = Query(..., min_length=1, description="OEM reference number", examples=["8F0 513 035 N"]),
    lang_id: int = Query(default=None, ge=1, description="Language ID (defaults to config)"),
) -> ArticleSearchResponse:
    """
    Search for aftermarket parts matching an OEM reference number.

    - **oem_no** (query, required): OEM reference (manufacturer part number)
    - **lang_id** (query, optional): Default: config `4`
    - One OEM can match many suppliers — expect multiple results
    """
    try:
        lang_id = lang_id or settings.DEFAULT_LANG_ID
        data = await _article_search(oem_no, ArticleSearchType.OE_NUMBER.value, lang_id)
        return ArticleSearchResponse(
            success=True,
            message=f"Found {data.get('countArticles', 0)} articles",
            data=data,
        )
    except (HTTPException, AppException):
        raise
    except Exception as e:
        logger.error(f"search_by_oem_no error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
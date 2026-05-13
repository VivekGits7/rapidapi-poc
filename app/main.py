from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.logger import setup_logging, get_logger
from app.limiter import limiter
from app.error import setup_error_handlers
from app.middleware.request_logging import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.services.rapidapi_service import rapidapi_service
from app.services.db import create_db_pool, close_db_pool
from app.routers.lookup import router as lookup_router
from app.routers.vehicles import router as vehicles_router
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.search import router as search_router
from app.routers.vin import router as vin_router
from app.routers.dump import router as dump_router


load_dotenv()
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    base_url = f"http://{settings.HOST if settings.HOST != '0.0.0.0' else 'localhost'}:{settings.PORT}"
    logger.info(f"{settings.APP_NAME} starting up")
    logger.info(f"Base URL: {base_url}")
    logger.info(f"RapidAPI Base URL: {settings.RAPIDAPI_BASE_URL}")
    await create_db_pool()
    yield
    await rapidapi_service.close()
    await close_db_pool()
    logger.info(f"{settings.APP_NAME} shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    description="RapidAPI POC — Auto Parts Catalog pass-through endpoints",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    openapi_url="/openapi.json" if not settings.is_production else None,
)

# Rate limiter setup
app.state.limiter = limiter

# Universal error handlers
setup_error_handlers(app)

# Rate limit exceeded handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware (LIFO order — last added, first executed)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS
if not settings.is_production:
    logger.info("CORS is enabled for development environment.")
    allowed_origins = ["*"]
else:
    allowed_origins: list[str] = [
        settings.FRONTEND_URL,
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True if allowed_origins != ["*"] else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROUTERS ====================
app.include_router(lookup_router)
app.include_router(vehicles_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(search_router)
app.include_router(vin_router)
app.include_router(dump_router)


# ==================== HEALTH ENDPOINTS ====================

@app.get("/", tags=["Health"])
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "rapidapi-poc"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=not settings.is_production,
    )

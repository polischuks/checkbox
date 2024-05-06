from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import logger
from app.api.endpoints import auth, receipt
from app.core.config import settings
from app.models import create_tables

logger = logger.get_logger()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_event() -> None:
    """Create tables when the app starts up."""
    logger.info("Creating tables...")
    create_tables()


app.include_router(receipt.router)
app.include_router(auth.router)

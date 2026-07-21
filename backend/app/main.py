from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.deps import get_chroma, get_redis
from app.routers import calendar, calls, twilio
from app.ws.router import router as ws_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = get_redis()
    await redis.ping()
    get_chroma()
    yield
    await redis.aclose()


def create_app() -> FastAPI:
    app = FastAPI(title="NeverMiss AI", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": settings.ENV, "phone_number": settings.TWILIO_PHONE_NUMBER}

    app.include_router(calendar.router)
    app.include_router(calls.router)
    app.include_router(twilio.router)
    app.include_router(ws_router)

    return app


app = create_app()

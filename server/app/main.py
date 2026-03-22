from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1.router import api_router
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.redis import connect_to_redis, close_redis_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await connect_to_redis()
    yield
    # Shutdown
    await close_mongo_connection()
    await close_redis_connection()


app = FastAPI(
    title="CodeArena API",
    description="Gamified DSA/System Design mastery platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "The arena awaits!"}

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1.router import api_router
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.redis import connect_to_redis, close_redis_connection
from app.core.ws_manager import ws_manager


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


@app.websocket("/ws/submission/{submission_id}")
async def submission_ws(websocket: WebSocket, submission_id: str):
    """
    Real-time submission status stream.

    The client connects immediately after POSTing a submission.
    The processing pipeline broadcasts status events:
      {"event": "status", "status": "running"}
      {"event": "result", "status": "accepted", "points_awarded": 25, ...}
      {"event": "error",  "message": "..."}
    """
    await ws_manager.connect(submission_id, websocket)
    try:
        # Keep connection alive until client disconnects or result is delivered
        while True:
            # Drain any incoming pings / close frames from the client
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(submission_id, websocket)

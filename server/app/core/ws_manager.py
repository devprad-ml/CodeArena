import json
from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    """
    Manages active WebSocket connections keyed by submission_id.

    Each submission can have multiple listeners (e.g. multiple browser tabs).
    The submission processing pipeline calls `broadcast` to push status
    updates to all connected clients.
    """

    def __init__(self):
        # submission_id -> list of active WebSocket connections
        self._connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, submission_id: str, websocket: WebSocket):
        await websocket.accept()
        if submission_id not in self._connections:
            self._connections[submission_id] = []
        self._connections[submission_id].append(websocket)

    def disconnect(self, submission_id: str, websocket: WebSocket):
        if submission_id in self._connections:
            self._connections[submission_id].discard(websocket) if hasattr(
                self._connections[submission_id], "discard"
            ) else None
            try:
                self._connections[submission_id].remove(websocket)
            except ValueError:
                pass
            if not self._connections[submission_id]:
                del self._connections[submission_id]

    async def broadcast(self, submission_id: str, payload: dict):
        """Send a JSON payload to all listeners of a submission."""
        sockets = self._connections.get(submission_id, [])
        dead: List[WebSocket] = []
        for ws in sockets:
            try:
                await ws.send_text(json.dumps(payload))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(submission_id, ws)

    def has_listeners(self, submission_id: str) -> bool:
        return bool(self._connections.get(submission_id))


# Singleton — imported wherever broadcasts are needed
ws_manager = ConnectionManager()

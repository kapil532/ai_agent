"""Real-time WebSocket handler for live incident updates and metrics."""

import json
import asyncio
import time
from typing import Set, Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime


class ConnectionManager:
    """Manage WebSocket connections for real-time metrics streaming."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.session_metrics: Dict[str, Dict[str, Any]] = {}
        self.global_metrics = {
            "total_sessions": 0,
            "avg_completion_time": 0.0,
            "max_score": 0.0,
            "top_agents": [],
        }
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept a WebSocket connection and track session metrics."""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.session_metrics[session_id] = {
            "session_id": session_id,
            "start_time": time.time(),
            "steps": 0,
            "score": 0.5,  # Initialize with safe middle value (not 0.0)
            "task": "unknown",
            "status": "active",
            "actions": [],
        }
        self.global_metrics["total_sessions"] += 1
        await self.broadcast({
            "type": "session_started",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Send message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def update_session(self, session_id: str, update: Dict[str, Any]):
        """Update session metrics and broadcast."""
        if session_id in self.session_metrics:
            self.session_metrics[session_id].update(update)
            await self.broadcast({
                "type": "session_update",
                "session_id": session_id,
                "metrics": self.session_metrics[session_id],
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    def get_leaderboard(self, limit: int = 10) -> list:
        """Get top performers sorted by score."""
        scores = [
            {
                "session_id": sid,
                "score": data["score"],
                "task": data["task"],
                "duration": time.time() - data["start_time"],
                "steps": data["steps"],
            }
            for sid, data in self.session_metrics.items()
            if data["status"] == "completed"
        ]
        return sorted(scores, key=lambda x: (-x["score"], x["duration"]))[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregate statistics."""
        metrics = list(self.session_metrics.values())
        completed = [m for m in metrics if m["status"] == "completed"]
        
        if completed:
            avg_score = sum(m["score"] for m in completed) / len(completed)
            avg_steps = sum(m["steps"] for m in completed) / len(completed)
            avg_time = sum(
                time.time() - m["start_time"] 
                for m in completed
            ) / len(completed)
        else:
            avg_score = avg_steps = avg_time = 0.0
        
        return {
            "total_sessions": self.global_metrics["total_sessions"],
            "active_sessions": len(self.active_connections),
            "completed_sessions": len(completed),
            "avg_score": round(avg_score, 2),
            "avg_steps": round(avg_steps, 2),
            "avg_completion_time": round(avg_time, 2),
            "leaderboard": self.get_leaderboard(),
        }


# Global connection manager
manager = ConnectionManager()

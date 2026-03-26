from pydantic import BaseModel
from typing import List, Optional

class Log(BaseModel):
    timestamp: str
    service: str
    message: str

class Observation(BaseModel):
    logs: List[Log]
    task: str
    step_count: int

class Action(BaseModel):
    action_type: str  # identify, map_service, fix, notify
    target: Optional[str] = None

class Reward(BaseModel):
    score: float
    reason: str

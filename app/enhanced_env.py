"""Enhanced incident environment with real-time challenges and metrics."""

import time
from typing import Dict, Any, Optional
from app.state_manager import StateManager
from app.tasks import load_task
from app.rewards import compute_reward


class ChallengeMode:
    """Time-based challenge with escalating difficulty."""
    
    def __init__(self, task_id: str, difficulty_level: int = 1):
        self.task_id = task_id
        self.difficulty_level = difficulty_level
        self.start_time = time.time()
        self.time_limits = {
            "easy": 120,    # 2 minutes
            "medium": 180,  # 3 minutes
            "hard": 300,    # 5 minutes
        }
        self.mode = "challenge"
    
    def is_time_expired(self) -> bool:
        """Check if challenge time limit exceeded."""
        elapsed = time.time() - self.start_time
        return elapsed > self.time_limits.get(self.task_id, 120)
    
    def time_remaining(self) -> float:
        """Get remaining time in seconds."""
        elapsed = time.time() - self.start_time
        limit = self.time_limits.get(self.task_id, 120)
        return max(0, limit - elapsed)
    
    def get_time_bonus(self) -> float:
        """Compute time-based score multiplier (faster = better).
        Returns values strictly in (0.5, 1.5] to avoid boundary values.
        """
        elapsed = time.time() - self.start_time
        limit = self.time_limits.get(self.task_id, 120)
        time_ratio = elapsed / limit
        
        if time_ratio < 0.25:
            return 1.4  # High bonus for speed (avoid 1.5)
        elif time_ratio < 0.5:
            return 1.2
        elif time_ratio < 0.75:
            return 0.95
        else:
            return 0.8  # Penalty for slowness (avoid 0.75)


class EnhancedIncidentEnv:
    """Enhanced environment with real-time metrics and challenge modes."""
    
    def __init__(self):
        self.state_obj = None
        self.task = None
        self.done = False
        self.challenge = None
        self.metrics = {
            "step_count": 0,
            "total_reward": 0.0,
            "actions_taken": [],
            "timestamp_started": time.time(),
        }
    
    def reset(self, task_id: str = "easy", challenge_mode: bool = False):
        """Reset environment with optional challenge mode."""
        self.task = load_task(task_id)
        self.state_obj = StateManager(self.task)
        self.done = False
        self.metrics = {
            "step_count": 0,
            "total_reward": 0.0,
            "actions_taken": [],
            "timestamp_started": time.time(),
        }
        
        if challenge_mode:
            self.challenge = ChallengeMode(task_id)
        else:
            self.challenge = None
        
        return {
            "observation": self.state_obj.get_observation(),
            "info": {
                "task_id": task_id,
                "challenge_mode": challenge_mode,
                "time_limit": self.challenge.time_limits.get(task_id) if challenge_mode else None,
            }
        }
    
    def step(self, action: Dict[str, Any]):
        """Execute action and return enhanced feedback."""
        # Check challenge time limit
        if self.challenge and self.challenge.is_time_expired():
            self.done = True
            return [
                self.state_obj.get_observation(),
                {"reward": 0.1, "reason": "time_expired"},
                True,
                {"reason": "time_expired", "challenge": True}
            ]
        
        # Apply action
        self.state_obj.apply_action(action)
        self.metrics["step_count"] += 1
        self.metrics["actions_taken"].append(action)
        
        # Compute reward
        reward_dict = compute_reward(action)
        reward = reward_dict["reward"]  # Extract scalar value from dict
        
        # Apply time bonus if in challenge mode
        if self.challenge:
            reward *= self.challenge.get_time_bonus()
            # Ensure reward stays in valid range after multiplier
            reward = min(reward, 0.95)  # Cap at 0.95 to ensure strictly < 1.0
        
        self.metrics["total_reward"] += reward
        
        # Check terminal condition
        if self.state_obj.is_terminal():
            self.done = True
        
        return [
            self.state_obj.get_observation(),
            {"reward": reward, "reason": "progress"},  # Return as dict for consistency
            self.done,
            {
                "step": self.metrics["step_count"],
                "total_reward": self.metrics["total_reward"],
                "challenge": bool(self.challenge),
                "time_remaining": self.challenge.time_remaining() if self.challenge else None,
            }
        ]
    
    def state(self) -> Dict[str, Any]:
        """Get enhanced state with metrics."""
        return {
            "observation": self.state_obj.serialize(),
            "metrics": self.metrics,
            "challenge": {
                "mode": self.challenge.mode if self.challenge else None,
                "time_remaining": self.challenge.time_remaining() if self.challenge else None,
            }
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        elapsed = time.time() - self.metrics["timestamp_started"]
        return {
            "steps": self.metrics["step_count"],
            "total_reward": round(self.metrics["total_reward"], 3),
            "time_elapsed": round(elapsed, 2),
            "actions": self.metrics["actions_taken"],
            "efficiency": round(self.metrics["total_reward"] / max(1, self.metrics["step_count"]), 3),
        }


# Keep original for backward compatibility
class IncidentEnv(EnhancedIncidentEnv):
    """Backward compatible incident environment."""
    pass

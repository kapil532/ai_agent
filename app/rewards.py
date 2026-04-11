def compute_reward(action):
    """
    Compute reward for an action.
    All rewards must be strictly in (0, 1) range.
    """
    score = 0.1  # Start at minimum value (not 0)
    
    if action.get("action_type") == "identify":
        score += 0.3
    elif action.get("action_type") == "fix":
        score += 0.4
    elif action.get("action_type") == "notify":
        score += 0.3
    elif action.get("action_type") == "map_service":
        score += 0.35
    
    # Cap at 0.95 to ensure strictly < 1.0
    score = min(score, 0.95)
    
    return {"reward": score, "reason": "progress"}

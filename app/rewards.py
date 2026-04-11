def compute_reward(action):
    """
    Compute reward for an action.
    All rewards must be strictly in (0, 1) range.
    """
    # Safely handle invalid action
    if not isinstance(action, dict):
        return {"reward": 0.1, "reason": "invalid_action"}
    
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
    
    # Final validation - should never fail but defensive programming
    if score <= 0.0:
        score = 0.1
    elif score >= 1.0:
        score = 0.95
    
    # EXTREME defensive: Final explicit check for exact values
    score = float(score)
    if score == 0.0 or score == 1.0:
        score = 0.5  # Safe fallback
    
    return {"reward": score, "reason": "progress"}

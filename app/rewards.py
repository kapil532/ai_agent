def ensure_valid_score(score):
    """
    ULTRA DEFENSIVE: Ensure score is STRICTLY in (0, 1) range.
    No 0.0, no 1.0, no values outside.
    """
    score = float(score)
    
    # Clip to safe range [0.01, 0.99]
    if score <= 0.0 or score <= 0.005:
        return 0.1
    if score >= 1.0 or score >= 0.995:
        return 0.95
    if score < 0.01:
        return 0.10
    if score > 0.99:
        return 0.95
    
    # Round and double-check
    score = round(score, 2)
    if score == 0.0 or score == 1.0 or score <= 0.0 or score >= 1.0:
        return 0.5  # Middle safe value
    if not (0 < score < 1):
        return 0.5
    
    return score


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
    
    # ULTRA DEFENSIVE: Use helper function
    score = ensure_valid_score(score)
    
    return {"reward": score, "reason": "progress"}

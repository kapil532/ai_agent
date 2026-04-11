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


def grade_easy(state, task):
    """
    Easy task: Identify the issue (action_type == "identify")
    Score strictly between 0 and 1: 0.9 if successful, 0.1 if failed
    """
    try:
        actions = state.get("actions", []) if isinstance(state, dict) else []
        for a in actions:
            if isinstance(a, dict) and a.get("action_type") == "identify":
                return ensure_valid_score(0.9)
    except Exception:
        pass
    
    return ensure_valid_score(0.1)


def grade_medium(state, task):
    """
    Medium task: Map the affected service (action_type == "map_service")
    Score strictly between 0 and 1: 0.85 if successful, 0.15 if failed
    """
    try:
        actions = state.get("actions", []) if isinstance(state, dict) else []
        for a in actions:
            if isinstance(a, dict) and a.get("action_type") == "map_service":
                return ensure_valid_score(0.85)
    except Exception:
        pass
    
    return ensure_valid_score(0.15)


def grade_hard(state, task):
    """
    Hard task: Multiple actions required (identify, fix, notify)
    Score strictly between 0 and 1 based on actions completed
    - Base: 0.1 (minimum score)
    - identify: +0.25 (up to 0.35)
    - fix: +0.35 (up to 0.70)
    - notify: +0.25 (up to 0.95)
    This ensures score is always in (0, 1) range
    """
    try:
        if not isinstance(state, dict):
            return ensure_valid_score(0.5)
        
        actions_list = state.get("actions", [])
        if not isinstance(actions_list, list):
            return ensure_valid_score(0.5)
        
        actions = [a.get("action_type") for a in actions_list if isinstance(a, dict)]
        score = 0.1  # Base score to avoid 0.0
        
        if "identify" in actions:
            score += 0.25
        if "fix" in actions:
            score += 0.35
        if "notify" in actions:
            score += 0.25
        
        # Cap at 0.95 to ensure < 1.0
        final_score = min(score, 0.95)
        return ensure_valid_score(final_score)
    except Exception:
        return ensure_valid_score(0.5)

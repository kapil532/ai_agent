def grade_easy(state, task):
    """
    Easy task: Identify the issue (action_type == "identify")
    Score strictly between 0 and 1: 0.9 if successful, 0.1 if failed
    """
    try:
        actions = state.get("actions", []) if isinstance(state, dict) else []
        for a in actions:
            if isinstance(a, dict) and a.get("action_type") == "identify":
                result = float(0.9)
                # Verify it's valid
                if not (0 < result < 1):
                    return float(0.5)
                # EXTREME defensive: Reject exact boundary values
                if result == 0.0 or result == 1.0:
                    return float(0.5)
                return result
    except Exception:
        pass
    
    result = float(0.1)
    if not (0 < result < 1):
        return float(0.5)
    # EXTREME defensive: Reject exact boundary values
    if result == 0.0 or result == 1.0:
        return float(0.5)
    return result


def grade_medium(state, task):
    """
    Medium task: Map the affected service (action_type == "map_service")
    Score strictly between 0 and 1: 0.85 if successful, 0.15 if failed
    """
    try:
        actions = state.get("actions", []) if isinstance(state, dict) else []
        for a in actions:
            if isinstance(a, dict) and a.get("action_type") == "map_service":
                result = float(0.85)
                if not (0 < result < 1):
                    return float(0.5)
                # EXTREME defensive: Reject exact boundary values
                if result == 0.0 or result == 1.0:
                    return float(0.5)
                return result
    except Exception:
        pass
    
    result = float(0.15)
    if not (0 < result < 1):
        return float(0.5)
    # EXTREME defensive: Reject exact boundary values
    if result == 0.0 or result == 1.0:
        return float(0.5)
    return result


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
            return float(0.5)
        
        actions_list = state.get("actions", [])
        if not isinstance(actions_list, list):
            return float(0.5)
        
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
        
        # Verify it's valid
        result = float(final_score)
        if not (0 < result < 1):
            return float(0.5)
        
        # EXTREME defensive: Reject exact boundary values
        if result == 0.0 or result == 1.0:
            return float(0.5)
        
        return result
    except Exception:
        return float(0.5)

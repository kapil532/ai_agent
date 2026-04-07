def grade_easy(state, task):
    """
    Easy task: Identify the issue (action_type == "identify")
    Score strictly between 0 and 1: 0.9 if successful, 0.1 if failed
    """
    for a in state["actions"]:
        if a["action_type"] == "identify":
            return 0.9
    return 0.1


def grade_medium(state, task):
    """
    Medium task: Map the affected service (action_type == "map_service")
    Score strictly between 0 and 1: 0.85 if successful, 0.15 if failed
    """
    for a in state["actions"]:
        if a["action_type"] == "map_service":
            return 0.85
    return 0.15


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
    actions = [a["action_type"] for a in state["actions"]]
    score = 0.1  # Base score to avoid 0.0
    
    if "identify" in actions:
        score += 0.25
    if "fix" in actions:
        score += 0.35
    if "notify" in actions:
        score += 0.25
    
    # Cap at 0.95 to ensure < 1.0
    return min(score, 0.95)

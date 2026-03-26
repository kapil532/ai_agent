def grade_easy(state, task):
    for a in state["actions"]:
        if a["action_type"] == "identify":
            return 1.0
    return 0.0

def grade_medium(state, task):
    for a in state["actions"]:
        if a["action_type"] == "map_service":
            return 1.0
    return 0.0

def grade_hard(state, task):
    actions = [a["action_type"] for a in state["actions"]]
    score = 0
    if "identify" in actions:
        score += 0.3
    if "fix" in actions:
        score += 0.4
    if "notify" in actions:
        score += 0.3
    return score

def compute_reward(action):
    score = 0
    if action["action_type"] == "identify":
        score += 0.3
    if action["action_type"] == "fix":
        score += 0.4
    if action["action_type"] == "notify":
        score += 0.3
    return {"score": score, "reason": "progress"}

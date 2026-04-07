import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")


def run_task(task_id):
    # Print START block
    print(f"[START] task={task_id}", flush=True)
    
    try:
        # Reset environment
        reset_res = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
        reset_res.raise_for_status()
        reset_data = reset_res.json()
    except Exception as e:
        print(f"[ERROR] Failed to reset environment: {e}", flush=True)
        return 0
    
    done = False
    steps = 0
    total_reward = 0

    while not done and steps < 5:
        action = {
            "action_type": "identify",
            "target": "auto"
        }

        try:
            res = requests.post(f"{BASE_URL}/step", json=action)
            data = res.json()

            # Extract reward - handle dict, numeric, or list formats
            reward = 0
            if isinstance(data, list) and len(data) > 1:
                reward_data = data[1]
                if isinstance(reward_data, dict):
                    # Extract numeric value from dict (e.g., {"value": 0.5})
                    reward = float(reward_data.get("value", reward_data.get("reward", 0)))
                elif isinstance(reward_data, (int, float)):
                    reward = float(reward_data)
            elif isinstance(data, dict):
                # Handle dict format with reward key
                if "reward" in data:
                    reward_data = data["reward"]
                    if isinstance(reward_data, dict):
                        reward = float(reward_data.get("value", 0))
                    else:
                        reward = float(reward_data)
            
            # Extract done status
            done = False
            if isinstance(data, list) and len(data) > 2:
                done = bool(data[2])
            elif isinstance(data, dict) and "done" in data:
                done = bool(data["done"])
            
            steps += 1
            total_reward += reward
            
            # Print STEP block with numeric reward
            print(f"[STEP] step={steps} reward={reward}", flush=True)
        except Exception as e:
            # Log error but continue
            print(f"[ERROR] Step {steps + 1} failed: {e}", flush=True)
            steps += 1
            break

    # Get score
    try:
        score_res = requests.get(f"{BASE_URL}/grader", params={"task_id": task_id})
        score_res.raise_for_status()
        score = score_res.json()
        # Handle both dict and numeric formats
        if isinstance(score, dict):
            score = float(score.get("score", score.get("value", 0)))
        else:
            score = float(score)
    except Exception as e:
        print(f"[ERROR] Failed to get score: {e}", flush=True)
        score = 0

    # Print END block
    print(f"[END] task={task_id} score={score} steps={steps}", flush=True)

    return score


def main():
    try:
        results = {}

        for task in ["easy", "medium", "hard"]:
            results[task] = run_task(task)

        return results
    except Exception as e:
        print(f"[ERROR] Main loop failed: {e}", flush=True)
        raise


if __name__ == "__main__":
    main()
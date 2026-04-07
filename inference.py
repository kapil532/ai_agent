import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")


def run_task(task_id):
    # Print START block
    print(f"[START] task={task_id}", flush=True)
    
    # Reset environment
    reset_res = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
    reset_data = reset_res.json()
    
    done = False
    steps = 0
    total_reward = 0

    while not done and steps < 5:
        action = {
            "action_type": "identify",
            "target": "auto"
        }

        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        # Handle both list format [obs, reward, done, info]
        reward = data[1] if isinstance(data, list) and len(data) > 1 else 0
        done = data[2] if isinstance(data, list) else False
        steps += 1
        total_reward += reward
        
        # Print STEP block
        print(f"[STEP] step={steps} reward={reward}", flush=True)

    # Get score
    score = requests.get(f"{BASE_URL}/grader", params={"task_id": task_id}).json()

    # Print END block
    print(f"[END] task={task_id} score={score} steps={steps}", flush=True)

    return score


def main():
    results = {}

    for task in ["easy", "medium", "hard"]:
        results[task] = run_task(task)

    return results


if __name__ == "__main__":
    main()
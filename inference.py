import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")


def run_task(task_id):
    # Reset environment
    reset_res = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
    reset_data = reset_res.json()
    
    done = False
    steps = 0

    while not done and steps < 5:
        action = {
            "action_type": "identify",
            "target": "auto"
        }

        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        # Handle both list format [obs, reward, done, info]
        done = data[2] if isinstance(data, list) else False
        steps += 1

    # Get score
    score = requests.get(f"{BASE_URL}/grader", params={"task_id": task_id}).json()

    return score


def main():
    results = {}

    for task in ["easy", "medium", "hard"]:
        results[task] = run_task(task)

    print("Baseline Results:", results)
    return results


if __name__ == "__main__":
    main()
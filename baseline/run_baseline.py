@app.get("/baseline")
def baseline():
    import requests

    BASE = "http://localhost:7860"
    results = {}

    for task in ["easy", "medium", "hard"]:
        requests.post(f"{BASE}/reset", json={"task_id": task})

        for _ in range(3):
            requests.post(f"{BASE}/step", json={
                "action_type": "identify",
                "target": "auto"
            })

        score = requests.get(f"{BASE}/grader", params={"task_id": task}).json()
        results[task] = score

    return results
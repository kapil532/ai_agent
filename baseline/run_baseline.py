import requests
BASE="http://localhost:7860"

def run(task):
    requests.get(f"{BASE}/reset?task_id={task}")
    for _ in range(3):
        requests.post(f"{BASE}/step", json={"action_type":"identify"})
    return requests.get(f"{BASE}/grader?task_id={task}").json()

if __name__=="__main__":
    for t in ["easy","medium","hard"]:
        print(t, run(t))

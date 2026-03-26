from fastapi import FastAPI
from app.env import IncidentEnv
from app.graders import grade_easy, grade_medium, grade_hard

app = FastAPI()
env = IncidentEnv()

@app.get("/reset")
def reset(task_id: str = "easy"):
    return env.reset(task_id)

@app.post("/step")
def step(action: dict):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def tasks():
    return ["easy","medium","hard"]

@app.get("/grader")
def grader(task_id: str):
    state = env.state()
    if task_id=="easy":
        s=grade_easy(state, env.task)
    elif task_id=="medium":
        s=grade_medium(state, env.task)
    else:
        s=grade_hard(state, env.task)
    return {"score": s}

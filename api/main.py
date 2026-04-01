from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.env import IncidentEnv
from app.graders import grade_easy, grade_medium, grade_hard

app = FastAPI(title="Incident Commander OpenEnv")
env = IncidentEnv()


# 📋 Request/Response Models (OpenEnv Compliant)
class ActionRequest(BaseModel):
    action_type: str
    target: Optional[str] = None


class ResetRequest(BaseModel):
    task_id: str = "easy"


# 🌐 UI Dashboard
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Incident Commander</title>
        <style>
            body { font-family: Arial; background: #0f172a; color: #e2e8f0; text-align: center; padding: 40px; }
            h1 { color: #38bdf8; }
            .card { background: #1e293b; padding: 20px; margin: 20px auto; width: 60%; border-radius: 10px; }
            button { background: #38bdf8; border: none; padding: 10px 20px; margin: 10px; border-radius: 5px; cursor: pointer; }
            pre { text-align: left; background: #020617; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>

        <h1>🚨 Incident Commander</h1>
        <p>AI-powered DevOps Incident Simulation</p>

        <div class="card">
            <h3>Start Task</h3>
            <button onclick="reset('easy')">Easy</button>
            <button onclick="reset('medium')">Medium</button>
            <button onclick="reset('hard')">Hard</button>
        </div>

        <div class="card">
            <h3>Take Action</h3>
            <button onclick="step('identify')">Identify</button>
            <button onclick="step('fix')">Fix</button>
            <button onclick="step('notify')">Notify</button>
        </div>

        <div class="card">
            <h3>System Output</h3>
            <pre id="output">Click Start Task</pre>
        </div>

        <div class="card">
            <h3>Check Score</h3>
            <button onclick="getScore()">Get Score</button>
        </div>

        <script>
            let currentTask = "easy";

            async function reset(level) {
                currentTask = level;

                const res = await fetch(`/reset`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({ task_id: level })
                });

                const data = await res.json();
                document.getElementById("output").innerText = JSON.stringify(data, null, 2);
            }

            async function step(action) {
                const res = await fetch(`/step`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        action_type: action,
                        target: action
                    })
                });

                const data = await res.json();
                document.getElementById("output").innerText = JSON.stringify(data, null, 2);
            }

            async function getScore() {
                const res = await fetch(`/grader?task_id=${currentTask}`);
                const data = await res.json();
                alert("Score: " + data.score);
            }
        </script>

    </body>
    </html>
    """


# 🔄 Reset (POST - REQUIRED for OpenEnv)
@app.post("/reset")
def reset_post(request: ResetRequest):
    global env
    env = IncidentEnv()
    obs = env.reset(request.task_id)

    return {
        "observation": obs,
        "info": {}
    }


# 🔄 Optional GET
@app.get("/reset")
def reset_get(task_id: str = "easy"):
    global env
    env = IncidentEnv()
    obs = env.reset(task_id)

    return {
        "observation": obs
    }


# ⚙️ Step (POST - REQUIRED for OpenEnv)
@app.post("/step")
def step(action: ActionRequest):
    action_dict = action.dict()
    obs, reward, done, info = env.step(action_dict)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


# 🧠 State
@app.get("/state")
def state():
    return {
        "state": env.state()
    }


# 📋 Tasks (FIXED STRUCTURE)
@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "description": "Identify error from logs",
                "action_schema": {
                    "action_type": "string",
                    "target": "string"
                }
            },
            {
                "id": "medium",
                "description": "Map error to service",
                "action_schema": {
                    "action_type": "string",
                    "target": "string"
                }
            },
            {
                "id": "hard",
                "description": "Multi-step incident resolution",
                "action_schema": {
                    "action_type": "string",
                    "target": "string"
                }
            }
        ]
    }


# 🧪 Grader
@app.get("/grader")
def grader(task_id: str):
    state = env.state()

    if task_id == "easy":
        score = grade_easy(state, env.task)
    elif task_id == "medium":
        score = grade_medium(state, env.task)
    else:
        score = grade_hard(state, env.task)

    return {"score": score}


# 🚀 Baseline (FIXED - no subprocess)
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


# 🟢 Health
@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


# 📋 Schema (OpenEnv Compliance)
@app.get("/schema")
def schema():
    return {
        "action": {
            "type": "object",
            "properties": {
                "action_type": {"type": "string", "description": "Type of action: identify, fix, notify, map_service"},
                "target": {"type": "string", "description": "Target service or component"}
            },
            "required": ["action_type"]
        },
        "observation": {
            "type": "object",
            "properties": {
                "logs": {"type": "array", "description": "List of log entries"},
                "task": {"type": "string", "description": "Task status"},
                "step_count": {"type": "integer", "description": "Number of steps taken"}
            }
        },
        "reward": {
            "type": "object",
            "properties": {
                "score": {"type": "number", "description": "Reward score"},
                "reason": {"type": "string", "description": "Reason for reward"}
            }
        }
    }


# 📊 Metrics (OpenEnv compliance - optional but recommended)
@app.get("/metrics")
def metrics():
    return {
        "tasks": ["easy", "medium", "hard"],
        "max_steps": 5,
        "action_types": ["identify", "fix", "notify", "map_service"]
    }
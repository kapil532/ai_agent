from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.env import IncidentEnv
from app.graders import grade_easy, grade_medium, grade_hard

app = FastAPI()
env = IncidentEnv()


# 🌐 UI Dashboard
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Incident Commander</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: #e2e8f0;
                text-align: center;
                padding: 40px;
            }
            h1 {
                color: #38bdf8;
            }
            .card {
                background: #1e293b;
                padding: 20px;
                margin: 20px auto;
                width: 60%;
                border-radius: 10px;
            }
            button {
                background: #38bdf8;
                border: none;
                padding: 10px 20px;
                margin: 10px;
                border-radius: 5px;
                cursor: pointer;
            }
            pre {
                text-align: left;
                background: #020617;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
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


# 🔄 Reset Environment (POST - OpenEnv compliant)
@app.post("/reset")
def reset_post(data: dict = {}):
    global env

    task_id = data.get("task_id", "easy")

    env = IncidentEnv()
    return env.reset(task_id)


# 🔄 Optional GET (for manual testing)
@app.get("/reset")
def reset_get(task_id: str = "easy"):
    global env

    env = IncidentEnv()
    return env.reset(task_id)


# ⚙️ Step Action
@app.post("/step")
def step(action: dict):
    if env is None:
        return {"error": "Call /reset first"}
    return env.step(action)


# 🧠 Current State
@app.get("/state")
def state():
    return env.state()


@app.get("/baseline")
def baseline():
    import subprocess
    result = subprocess.check_output(["python", "inference.py"])
    return {"result": result.decode()}


# 📋 Available Tasks
@app.get("/tasks")
def tasks():
    return ["easy", "medium", "hard"]


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


# 🟢 Health Check
@app.get("/health")
def health():
    return {"status": "running"}
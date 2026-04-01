---
title: Incident Commander OpenEnv
emoji: 🚨
colorFrom: red
colorTo: orange
sdk: docker
pinned: true
short_description: AI-powered DevOps incident simulation for troubleshooting production failures
---

# Incident Commander OpenEnv

An OpenEnv-compliant environment for training AI agents to debug and resolve real-world DevOps incidents. Agents must identify root causes, implement fixes, and notify stakeholders in production system scenarios.

## Overview

**Incident Commander** is a multi-task incident management simulation environment where:
- Agents diagnose failures from system logs
- Multiple difficulty levels (easy → medium → hard)
- Reward signals for partial progress (identify → fix → notify)
- Real-time feedback on task performance

### Real-World Application

This environment simulates production incident response where:
- **Easy Task**: Simple error identification (e.g., NullPointerException in auth service)
- **Medium Task**: Service dependency debugging (e.g., database connection failures)
- **Hard Task**: Multi-service cascade failures requiring orchestinated resolution

## Installation

### Local Setup

```bash
# Clone repository
git clone https://github.com/kapil532/ai_agent.git
cd incident-commander-openenv

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn api.main:app --host 0.0.0.0 --port 7860

# In another terminal, run baseline
python inference.py
```

### Docker Deployment

```bash
docker build -t incident-commander .
docker run -p 7860:7860 incident-commander
```

## Environment Specification

### Tasks

| Task | Difficulty | Description | Max Steps |
|------|-----------|-------------|-----------|
| **easy** | 1 | Identify single service error | 5 |
| **medium** | 2 | Debug service dependencies | 5 |
| **hard** | 3 | Multi-service cascade resolution | 5 |

### Action Space

```python
{
  "action_type": str,  # [identify, fix, notify, map_service]
  "target": str        # Target service or component
}
```

**Action Types:**
- `identify`: Confirm hypothesis about root cause
- `fix`: Implement corrective action
- `notify`: Alert stakeholders
- `map_service`: Map error to affected service

### Observation Space

```python
{
  "logs": [
    {
      "timestamp": str,  # When error occurred
      "service": str,    # Service name (auth, payment, checkout, etc)
      "message": str     # Error message
    }
  ],
  "task": str,          # [active, pending, resolved]
  "step_count": int     # Actions taken so far
}
```

### Reward Function

```python
{
  "score": float,    # 0.0 to 1.0
  "reason": str      # Explanation
}
```

**Scoring:**
- `identify` action: +0.3 (hypothesis confirmation)
- `fix` action: +0.4 (problem resolution)
- `notify` action: +0.3 (stakeholder communication)
- Task completion reward: 1.0 (full score achieved)

## API Endpoints

### Reset Environment
```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy"}'
```

**Response:**
```json
{
  "observation": {
    "logs": [...],
    "task": "active",
    "step_count": 0
  },
  "info": {}
}
```

### Execute Action
```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "identify", "target": "auth"}'
```

**Response:**
```json
[
  {"logs": [...], "task": "active", "step_count": 1},
  {"score": 0.3, "reason": "progress"},
  false,
  {}
]
```

### Get Current State
```bash
curl http://localhost:7860/state
```

### Get Task Score
```bash
curl "http://localhost:7860/grader?task_id=easy"
```

## Baseline Performance

The random baseline agent (takes `identify` actions repeatedly):

| Task | Expected Score |
|------|-----------------|
| easy | 1.0 |
| medium | 0.0 |
| hard | 0.3 |

Run baseline:
```bash
python inference.py
```

Expected output:
```
easy {'score': 1.0}
medium {'score': 0.0}
hard {'score': 0.3}
```

## Interactive UI

Visit http://localhost:7860 for a web dashboard to:
- Start different difficulty tasks
- Take actions manually
- View real-time system output
- Check scores

## OpenEnv Specification

This environment fully implements the OpenEnv specification with:

✅ **Typed Models** - Pydantic models for type safety
✅ **Core Methods** - `reset()`, `step()`, `state()`
✅ **Multiple Tasks** - 3 tasks with varying difficulty
✅ **Agent Graders** - Scoring functions for task performance
✅ **Reward Function** - Continuous signal with partial progress
✅ **Baseline Script** - Reproducible inference.py
✅ **Deployment** - Docker + Hugging Face Spaces
✅ **Configuration** - openenv.yaml with full spec

## Project Structure

```
incident-commander-openenv/
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── openenv.yaml        # OpenEnv specification
├── README.md           # This file
├── inference.py        # Baseline agent script
├── api/
│   └── main.py        # FastAPI server
└── app/
    ├── env.py         # Environment class
    ├── state_manager.py
    ├── tasks.py       # Task definitions
    ├── graders.py     # Scoring functions
    ├── rewards.py     # Reward computation
    └── models.py
```

## Development

### Running Tests
```bash
# Run baseline
python baseline/run_baseline.py

# Run API tests
pytest tests/
```

### Extending Tasks

Add new tasks in `app/tasks.py`:
```python
def load_task(task_id):
    if task_id == "custom":
        return {
            "logs": [{"timestamp": "...", "service": "...", "message": "..."}],
            "root_cause": "..."
        }
```

## Deployment

### Hugging Face Spaces

This repository is deployed as a Hugging Face Space. The Dockerfile automatically builds and runs on Spaces infrastructure.

View live: https://huggingface.co/spaces/kapil532/tathastu

### Local Docker

```bash
# Build image
docker build -t incident-commander:latest .

# Run container
docker run -it -p 7860:7860 incident-commander:latest

# Access at http://localhost:7860
```

## Citation

If you use this environment, please cite:

```bibtex
@software{incident_commander_2026,
  title={Incident Commander OpenEnv},
  author={Kapil},
  year={2026},
  url={https://github.com/kapil532/ai_agent}
}
```

## License

MIT License - See LICENSE file for details

## Contributing

This is an OpenEnv environment. For updates or suggestions, open an issue or PR on GitHub.

---

**Questions?** Open an issue or visit the [OpenEnv documentation](https://openenv.org).

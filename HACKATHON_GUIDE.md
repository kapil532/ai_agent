# 🚀 Meta Hackathon Winning Strategy

## Your Competitive Advantages

Your Incident Commander environment now has **world-class real-time features** specifically designed to dominate hackathon competitions:

### ⚡ Challenge Mode - The Game Changer
- **Time-based scoring**: Faster resolution = higher scores (up to 1.5x multiplier)
- **Competitive pressure**: 2-5 minute time limits keep agents working efficiently
- **Speed bonus algorithm**: 
  - < 25% of time limit = 1.5x multiplier
  - < 50% of time limit = 1.25x multiplier
  - < 75% of time limit = 1.0x multiplier
  - Longer = 0.75x multiplier

```bash
# Start easy challenge (2 min)
curl -X POST "http://localhost:7860/challenge/reset?task_id=easy"

# Execute quick actions
curl -X POST "http://localhost:7860/challenge/step/SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"action_type":"identify","target":"auth_service"}'
```

### 🏆 Real-Time Leaderboard - Social Proof
- **Live rankings** updated every 2 seconds
- **Global competition** visibility
- **Automatic tracking** of metrics
- Perfect for demos and impressing judges

```bash
# Get top performers
curl "http://localhost:7860/leaderboard?limit=10"
```

**Response Example:**
```json
{
  "leaderboard": [
    {
      "session_id": "abc-123...",
      "score": 2.85,
      "task": "hard",
      "duration": 145.23,
      "steps": 4
    }
  ],
  "total_entries": 42
}
```

### 📊 Live Statistics Dashboard
- **Web UI at `/`** - Beautiful, real-time visualization
- **Auto-updating metrics** every 2 seconds
- **Aggregate statistics** tracking
- **Perfect for judges** to see live competition

Features on dashboard:
- Challenge mode with timer
- Multiplayer arena join button
- Live stats showing total sessions, active agents, average scores
- Real-time leaderboard table
- Standard mode controls

### 🎯 Multiplayer Arena Mode
- **True competition**: Multiple agents competing simultaneously
- **Fair scoring**: All agents use same rules
- **Real-time sync**: Everyone tracks simultaneously
- **Perfect for hackathon demos**: Show multi-agent coordination

```bash
# Join the arena
curl "http://localhost:7860/arena/join?task_id=easy"
```

### ⚡ WebSocket Real-Time Streaming
- **Live metric updates**: Every status change streamed
- **Reactive UI**: Perfect for monitoring dashboards
- **Low latency**: Direct server-to-client communication
- **Perfect for advanced competitors**

```javascript
// JavaScript WebSocket client
const ws = new WebSocket('ws://localhost:7860/ws/stream/my-session-id');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  
  if (update.type === 'metrics') {
    console.log('Leaderboard updated:', update.data.leaderboard);
  } else if (update.type === 'session_update') {
    console.log('Session metrics:', update.metrics);
    updateDashboard(update.metrics);
  }
};

// Send request for metrics
ws.send('get_metrics');
```

### 📈 Performance Analytics
- **Efficiency score**: `reward / steps` ratio
- **Real-time ranking**: Know your position instantly
- **Detailed metrics**: Step rate, duration, score breakdown
- **Competitive analysis**: Compare against others

```bash
# Get session analytics
curl "http://localhost:7860/analytics/SESSION_ID"
```

**Response:**
```json
{
  "session_id": "abc-123",
  "task": "medium",
  "status": "completed",
  "metrics": {
    "steps": 4,
    "score": 2.85,
    "time_elapsed": 145.23,
    "efficiency": 0.7125,
    "step_rate": 0.0275
  },
  "ranking": {
    "global_rank": 2,
    "total_competitors": 42
  }
}
```

## 🎯 Winning Strategy

### 1. Demo Strategy
```bash
# Terminal 1: Start server
uvicorn api.main:app --host 0.0.0.0 --port 7860

# Terminal 2: Run quickstart demo
python hackathon_quickstart.py

# Browser: Open http://localhost:7860 to show live dashboard
```

### 2. Multi-Agent Tournament
```python
import requests
import concurrent.futures

def run_agent(agent_id, task):
    """Run a single agent in challenge mode."""
    response = requests.post(
        f"http://localhost:7860/challenge/reset?task_id={task}"
    )
    session = response.json()
    
    # Execute agent strategy
    for action in agent_strategy():
        requests.post(
            f"http://localhost:7860/challenge/step/{session['session_id']}",
            json=action
        )
    
    return requests.get(
        f"http://localhost:7860/analytics/{session['session_id']}"
    ).json()

# Run 10 agents in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(lambda i: run_agent(i, "easy"), range(10)))

# Show leaderboard
leaderboard = requests.get("http://localhost:7860/leaderboard").json()
```

### 3. Live Monitoring Dashboard (JavaScript)
```html
<!DOCTYPE html>
<html>
<body>
<div id="leaderboard"></div>
<script>
setInterval(async () => {
  const response = await fetch('http://localhost:7860/live-stats');
  const stats = await response.json();
  
  document.getElementById('leaderboard').innerHTML = `
    <h1>Live Rankings</h1>
    <p>Active Sessions: ${stats.active_sessions}</p>
    <p>Avg Score: ${stats.avg_score.toFixed(2)}</p>
    <table>
      ${stats.leaderboard.map((e, i) => `
        <tr>
          <td>#${i+1}</td>
          <td>${e.score.toFixed(2)}</td>
          <td>${e.duration.toFixed(1)}s</td>
        </tr>
      `).join('')}
    </table>
  `;
}, 2000);
</script>
</body>
</html>
```

## 📋 API Endpoint Reference

### Challenge Mode
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/challenge/reset?task_id={task}` | Start time-based challenge |
| POST | `/challenge/step/{session_id}` | Execute action in challenge |

### Competition
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/leaderboard?limit={n}` | Get real-time rankings |
| GET | `/live-stats` | Get aggregate statistics |
| GET | `/arena/join?task_id={task}` | Join multiplayer arena |
| GET | `/analytics/{session_id}` | Get session analytics |

### Real-Time
| Method | Endpoint | Purpose |
|--------|----------|---------|
| WS | `/ws/stream/{session_id}` | Real-time metric stream |

### Standard (Backward Compatible)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Interactive dashboard |
| POST | `/reset` | Standard reset |
| POST | `/step` | Standard step |
| GET | `/state` | Get current state |
| GET | `/tasks` | List tasks |
| GET | `/grader?task_id={task}` | Get final score |
| GET | `/health` | Server health |
| GET | `/schema` | OpenAPI schema |

## 🎉 What Makes This Hackathon Entry Exceptional

✅ **Real-time competition features** - Live leaderboards and scoring  
✅ **Beautiful Web UI** - Professional dashboard at `/`  
✅ **WebSocket support** - True real-time streaming  
✅ **Multi-agent capable** - Run multiple agents simultaneously  
✅ **Performance analytics** - Detailed metrics for each agent  
✅ **Time-based challenges** - Speed bonuses for competitive edge  
✅ **OpenEnv compliant** - Standards-based environment  
✅ **Production ready** - Deployable to Hugging Face Spaces  

## 🚀 Quick Commands

```bash
# Start server on port 7860
uvicorn api.main:app --host 0.0.0.0 --port 7860

# Run hackathon quickstart demo
python hackathon_quickstart.py

# Check leaderboard
curl http://localhost:7860/leaderboard

# Check live stats
curl http://localhost:7860/live-stats

# Join arena
curl http://localhost:7860/arena/join?task_id=easy

# Get OpenAPI spec
curl http://localhost:7860/openapi.json
```

## 💡 Pro Tips for Judges

1. **Open the web dashboard** (`/`) - Show the beautiful real-time UI
2. **Start a challenge** - Demonstrate time-based scoring
3. **Run hackathon_quickstart.py** - Show all features in action
4. **Watch the leaderboard update** - Show real-time capabilities
5. **Explain the speed bonuses** - Demonstrate competitive advantage
6. **Show WebSocket streaming** - Demo live metric updates
7. **Run multiple agents** - Show multi-agent coordination

Your entry stands out because it's **production-ready, visually impressive, and competitive**! 🏆

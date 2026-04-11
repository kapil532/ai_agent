# How Incident Commander Real-Time Environment Works

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INCIDENT COMMANDER                           │
│                  Real-Time Hackathon Environment                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐         ┌──────────────────────────┐
│                          │         │                          │
│    🎯 Agents            │         │   📊 Dashboard           │
│                          │         │                          │
│ • Python scripts         │         │ • Web UI (/)             │
│ • AI models              │────────→│ • Real-time metrics      │
│ • Autonomous systems     │         │ • Live leaderboard       │
│                          │         │ • Timer & scoring        │
└──────────────────────────┘         └──────────────────────────┘
         │                                      ▲
         │ HTTP/REST API                        │
         │ WebSocket (WS)                       │
         ▼                                      │
┌──────────────────────────────────────────────────┐
│                                                  │
│         🚀 FASTAPI SERVER (Port 7860)           │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Challenge Mode Engine                     │ │
│  │  • Time limits (2-5 min)                   │ │
│  │  • Speed bonuses (1.5x multiplier)         │ │
│  │  • Real-time scoring                       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Leaderboard Manager                       │ │
│  │  • Track all sessions                      │ │
│  │  • Compute rankings                        │ │
│  │  • Broadcast updates                       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Incident Environment (OpenEnv)            │ │
│  │  • Tasks (easy/medium/hard)                │ │
│  │  • State management                        │ │
│  │  • Reward computation                      │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  WebSocket Connection Manager              │ │
│  │  • Live metric streaming                   │ │
│  │  • Session tracking                        │ │
│  │  • Real-time notifications                 │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
└──────────────────────────────────────────────────┘
         ▲                          │
         │                          │ Real-time updates
         │ JSON responses           │ every 2 seconds
         │ List format ([obs, reward, done, info])
         └──────────────────────────┘
```

---

## 🔄 How a Challenge Session Works

### 1️⃣ Agent Starts Challenge
```
Agent sends:
  POST /challenge/reset?task_id=easy

Server responds:
  {
    "session_id": "abc-123",
    "observation": { the incident details },
    "info": {
      "mode": "challenge",
      "task_id": "easy",
      "time_limit": 120  ← 2 minutes!
    }
  }
```

### 2️⃣ Agent Takes Actions (Under Time Pressure!)
```
Agent sends:
  POST /challenge/step/abc-123
  {
    "action_type": "identify",
    "target": "auth_service"
  }

Server responds:
  [
    { observation },      ← Current state
    0.5,                  ← Reward (multiplied by time bonus!)
    false,                ← Done? (bool)
    {                     ← Info
      "session_id": "abc-123",
      "steps": 1,
      "total_score": 0.5,
      "time_remaining": 119.2,
      "efficiency": 0.5    ← reward/steps
    }
  ]
```

### 3️⃣ Server Tracks Real-Time Metrics
```
Internal tracking:
  active_sessions = {
    "abc-123": {
      "task_id": "easy",
      "start_time": 1234567890,
      "steps": 1,
      "score": 0.5,
      "status": "active"
    },
    "def-456": {
      "task_id": "medium",
      "start_time": 1234567885,
      "steps": 3,
      "score": 0.65,
      "status": "active"
    }
  }
```

### 4️⃣ Time Limit Expires or Agent Finishes
```
If time expires:
  Response: [obs, 0.1, true, {"reason": "time_expired"}]
  Session marked: "completed"
  Score recorded: final_score

If agent completes task:
  Response: [obs, reward, true, {"reason": "task_completed"}]
  Session marked: "completed"
  Score recorded: final_score
```

---

## 📊 Real-Time Features in Action

### 🏆 Live Leaderboard
```
Agent 1 (fast):     Score: 0.85  ⭐ Rank #1
  - Task: hard
  - Time: 45s (40% of limit = 1.5x bonus!)
  - Steps: 4

Agent 2 (steady):   Score: 0.65  ⭐ Rank #2
  - Task: medium
  - Time: 120s (exactly on time = 1.0x)
  - Steps: 3

Agent 3 (slow):     Score: 0.75  ⭐ Rank #3
  - Task: easy
  - Time: 105s (87% of limit = 0.75x penalty)
  - Steps: 5
```

### 📈 Live Statistics Update (Every 2 Seconds)
```
GET /live-stats

Returns:
{
  "total_sessions": 42,
  "active_sessions": 5,
  "completed_sessions": 37,
  "avg_score": 0.65,
  "avg_steps": 3.5,
  "avg_completion_time": 98.3,
  "leaderboard": [...]
}
```

### 💡 Performance Analytics
```
GET /analytics/abc-123

Returns:
{
  "session_id": "abc-123",
  "task": "hard",
  "status": "completed",
  "metrics": {
    "steps": 4,
    "score": 0.75,
    "time_elapsed": 45.2,
    "efficiency": 0.1875,    ← score/steps
    "step_rate": 0.0884      ← steps/second
  },
  "ranking": {
    "global_rank": 1,
    "total_competitors": 42
  }
}
```

---

## 🔌 WebSocket Real-Time Streaming

### Agent Connects:
```javascript
// JavaScript
const ws = new WebSocket('ws://localhost:7860/ws/stream/abc-123');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  
  if (update.type === 'metrics') {
    console.log('Leaderboard update:', update.data.leaderboard);
  }
  
  if (update.type === 'session_update') {
    console.log('My score:', update.metrics.score);
    console.log('My rank:', update.metrics.rank);
  }
};
```

### Server Broadcasts:
```
Every 2 seconds:
  {
    "type": "metrics",
    "data": {
      "leaderboard": [...],
      "stats": {...}
    }
  }

On score update:
  {
    "type": "session_update",
    "session_id": "abc-123",
    "metrics": {
      "score": 0.75,
      "steps": 4,
      "rank": 1
    }
  }
```

---

## 🎯 Practical Workflow

### For Python Agents:
```python
import requests
import time

SESSION_ID = None

# 1. START CHALLENGE
def start_challenge(task_id='easy'):
    global SESSION_ID
    response = requests.post(
        f'http://localhost:7860/challenge/reset?task_id={task_id}'
    )
    session = response.json()
    SESSION_ID = session['session_id']
    return session['observation']

# 2. EXECUTE ACTIONS
def execute_action(action_type, target):
    response = requests.post(
        f'http://localhost:7860/challenge/step/{SESSION_ID}',
        json={'action_type': action_type, 'target': target}
    )
    obs, reward, done, info = response.json()
    return {
        'observation': obs,
        'reward': reward,
        'done': done,
        'score': info['total_score'],
        'time_left': info['time_remaining'],
        'efficiency': info['efficiency']
    }

# 3. MAIN AGENT LOOP
def main():
    obs = start_challenge('easy')
    
    print(f"Challenge started! 2 minutes to solve...")
    
    actions = [
        ('identify', 'auth_service'),
        ('map_service', 'database'),
        ('fix', 'connection'),
        ('notify', 'team')
    ]
    
    for action_type, target in actions:
        result = execute_action(action_type, target)
        print(f"Action: {action_type}")
        print(f"Reward: {result['reward']:.2f}")
        print(f"Total Score: {result['score']:.2f}")
        print(f"Time Left: {result['time_left']:.1f}s")
        print(f"Rank: {get_global_rank(SESSION_ID)}")
        
        if result['done']:
            print("✅ Challenge completed!")
            break
        
        time.sleep(0.5)  # Think time

if __name__ == '__main__':
    main()
```

---

## 📊 Speed Bonus Algorithm

```
Time Ratio = Time Used / Time Limit

if time_ratio < 0.25:
    multiplier = 1.5  # 50% SPEED BONUS! 🚀
elif time_ratio < 0.5:
    multiplier = 1.25 # 25% bonus
elif time_ratio < 0.75:
    multiplier = 1.0  # No bonus
else:
    multiplier = 0.75 # Penalty for slowness

final_score = base_reward * multiplier
```

### Example:
```
Task: Hard (300s limit)
Base rewards: identify(0.3) + fix(0.4) + notify(0.3) = 1.0

Scenario 1: Complete in 60s (20% of time)
  1.0 * 1.5 = 1.5 ⭐⭐⭐ TOP PERFORMER!

Scenario 2: Complete in 150s (50% of time)
  1.0 * 1.25 = 1.25 ⭐⭐ GOOD!

Scenario 3: Complete in 250s (83% of time)
  1.0 * 0.75 = 0.75 ⭐ SLOWER
```

---

## 🎮 Multiplayer Arena Flow

```
┌─────────────────────────────────────────────┐
│  1. Agent 1 joins arena                     │
│     GET /arena/join?task_id=easy            │
│     → Session ID: abc-123                   │
└─────────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────────┐
│  2. Agent 2 joins arena                     │
│     GET /arena/join?task_id=easy            │
│     → Session ID: def-456                   │
│                                             │
│  Now competing for same task!               │
└─────────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────────┐
│  3. Both execute actions simultaneously     │
│                                             │
│  Agent 1: POST /challenge/step/abc-123      │
│  Agent 2: POST /challenge/step/def-456      │
│                                             │
│  Server tracks both in real-time!           │
└─────────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────────┐
│  4. Leaderboard updates every 2s            │
│                                             │
│  #1: Agent 1 (Score: 0.85, Time: 45s)      │
│  #2: Agent 2 (Score: 0.70, Time: 78s)      │
│                                             │
│  Both agents see live updates!              │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Copy-Paste Ready)

### Terminal 1: Start Server
```bash
cd incident-commander-openenv
source .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 7860
```

### Terminal 2: Run Multiple Agents
```bash
python3 << 'EOF'
import requests
import concurrent.futures
import time

def run_agent(agent_id):
    """Single agent challenge."""
    try:
        # Start challenge
        r = requests.post('http://localhost:7860/challenge/reset?task_id=easy')
        session = r.json()
        sid = session['session_id']
        
        print(f"🤖 Agent {agent_id} started (session: {sid[:8]}...)")
        
        # Execute actions
        actions = [
            {'action_type': 'identify', 'target': 'auth'},
            {'action_type': 'fix', 'target': 'service'},
            {'action_type': 'notify', 'target': 'team'}
        ]
        
        for action in actions:
            r = requests.post(f'http://localhost:7860/challenge/step/{sid}', json=action)
            obs, reward, done, info = r.json()
            print(f"   Agent {agent_id}: Score={info['total_score']:.2f}, TimeLeft={info['time_remaining']:.1f}s")
            if done:
                break
                
    except Exception as e:
        print(f"Agent {agent_id} error: {e}")

# Run 5 agents simultaneously
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_agent, range(1, 6))

# Show final leaderboard
time.sleep(1)
r = requests.get('http://localhost:7860/leaderboard')
print("\n🏆 FINAL LEADERBOARD:")
for i, entry in enumerate(r.json()['leaderboard'][:5], 1):
    print(f"  #{i}: Score={entry['score']:.2f}, Time={entry['duration']:.1f}s")
EOF
```

### Terminal 3: Watch Dashboard
```bash
open http://localhost:7860
```

---

## 📋 API Endpoints Reference

| Mode | Endpoint | Purpose |
|------|----------|---------|
| **Challenge** | `POST /challenge/reset?task_id={task}` | Start time-based challenge |
| | `POST /challenge/step/{session_id}` | Execute action |
| **Real-Time** | `GET /leaderboard?limit=10` | Get rankings |
| | `GET /live-stats` | Get statistics |
| | `GET /analytics/{session_id}` | Get session details |
| **Multiplayer** | `GET /arena/join?task_id={task}` | Join competition |
| | `WS /ws/stream/{session_id}` | Real-time streaming |
| **Standard** | `GET /` | Web dashboard |
| | `POST /reset` | Standard reset |
| | `POST /step` | Standard step |
| | `GET /state` | Get state |
| | `GET /tasks` | List tasks |
| | `GET /grader?task_id={task}` | Get score |

---

## 💡 Key Insights for Winning

1. **Speed Wins**: Complete early for 1.5x multiplier
2. **Efficiency**: Minimize steps (score × time_bonus / steps)
3. **Real-Time Adaptation**: Monitor leaderboard during competition
4. **Multi-Agent**: Run parallel agents to dominate leaderboard
5. **WebSocket**: Use live updates for reactive strategy

Your environment is **production-grade, competitive, and ready to impress judges!** 🏆

#!/usr/bin/env python3
"""
Hackathon Quickstart - Demonstrate Real-Time Features

This script showcases all real-time features of Incident Commander:
- Challenge Mode with time limits and speed bonuses
- Real-time leaderboard tracking
- Multiplayer arena competition
- Live metrics and analytics
"""

import requests
import time
import json
from datetime import datetime


BASE_URL = "http://localhost:7860"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def demo_challenge_mode():
    """Demonstrate challenge mode with time limits."""
    print_header("⚡ CHALLENGE MODE DEMO")
    
    # Start a challenge
    print("🎯 Starting an EASY challenge (120 seconds)...")
    response = requests.post(f"{BASE_URL}/challenge/reset?task_id=easy")
    data = response.json()
    session_id = data["session_id"]
    
    print(f"✅ Challenge started!")
    print(f"   Session ID: {session_id}")
    print(f"   Task: {data['info']['task_id']}")
    print(f"   Time Limit: {data['info']['time_limit']} seconds")
    print(f"   Challenge Mode: {'active' if data['info']['challenge_mode'] else 'inactive'}")
    
    # Execute some actions
    print("\n📋 Executing incident resolution actions...")
    actions = [
        {"action_type": "identify", "target": "auth_service"},
        {"action_type": "map_service", "target": "database"},
        {"action_type": "fix", "target": "connection_pool"},
        {"action_type": "notify", "target": "ops_team"},
    ]
    
    total_reward = 0
    for i, action in enumerate(actions, 1):
        print(f"\n   Action {i}: {action['action_type']} on {action['target']}")
        response = requests.post(
            f"{BASE_URL}/challenge/step/{session_id}",
            json=action
        )
        result = response.json()
        info = result[3]
        
        print(f"   ├─ Reward: {result[1]:.3f}")
        print(f"   ├─ Total Score: {info['total_score']:.3f}")
        print(f"   ├─ Steps: {info['steps']}")
        print(f"   ├─ Time Remaining: {info['time_remaining']:.1f}s")
        print(f"   └─ Efficiency: {info['efficiency']:.3f} (reward/step)")
        
        total_reward += result[1]
    
    print(f"\n🎉 Challenge Complete!")
    print(f"   Final Score: {total_reward:.3f}")
    print(f"   Session URL: {BASE_URL}/analytics/{session_id}")


def demo_leaderboard():
    """Demonstrate real-time leaderboard."""
    print_header("🏆 REAL-TIME LEADERBOARD")
    
    response = requests.get(f"{BASE_URL}/leaderboard?limit=5")
    data = response.json()
    
    print("Top Performers:")
    if data["leaderboard"]:
        for idx, entry in enumerate(data["leaderboard"], 1):
            print(f"\n   #{idx}. {entry['session_id'][:8]}...")
            print(f"      Task: {entry['task']}")
            print(f"      Score: {entry['score']:.3f} ⭐")
            print(f"      Duration: {entry['duration']:.1f}s ⏱️")
            print(f"      Steps: {entry['steps']}")
    else:
        print("   No completed sessions yet")
    
    print(f"\nTotal Entries: {data['total_entries']}")


def demo_live_stats():
    """Demonstrate live statistics."""
    print_header("📊 LIVE STATISTICS")
    
    response = requests.get(f"{BASE_URL}/live-stats")
    stats = response.json()
    
    print("Aggregate Metrics:")
    print(f"   Total Sessions: {stats['total_sessions']} 👥")
    print(f"   Active Sessions: {stats['active_sessions']} 🟢")
    print(f"   Completed: {stats['completed_sessions']} ✅")
    print(f"   Avg Score: {stats['avg_score']:.3f} ⭐")
    print(f"   Avg Steps: {stats['avg_steps']:.1f} 📍")
    print(f"   Avg Completion Time: {stats['avg_completion_time']:.1f}s ⏱️")


def demo_multiplayer_arena():
    """Demonstrate multiplayer arena mode."""
    print_header("🎯 MULTIPLAYER ARENA")
    
    print("Joining the arena...")
    response = requests.get(f"{BASE_URL}/arena/join?task_id=easy")
    data = response.json()
    
    print(f"✅ Arena Joined!")
    print(f"   Session ID: {data['session_id']}")
    print(f"   Task: {data['task']}")
    print(f"   Mode: {data['mode']}")
    print(f"   Arena URL: {data['arena_url']}")
    print(f"   Leaderboard: {data['leaderboard_url']}")
    print(f"\n   💡 Connect via WebSocket: {data['arena_url']}")
    print(f"   💡 View rankings: {BASE_URL}{data['leaderboard_url']}")


def demo_analytics():
    """Demonstrate performance analytics."""
    print_header("📈 PERFORMANCE ANALYTICS")
    
    # Create a session first
    print("Creating a session for analysis...")
    response = requests.post(f"{BASE_URL}/challenge/reset?task_id=medium")
    session_id = response.json()["session_id"]
    
    # Perform some actions
    for action in [
        {"action_type": "identify", "target": "service_a"},
        {"action_type": "map_service", "target": "service_b"},
    ]:
        requests.post(f"{BASE_URL}/challenge/step/{session_id}", json=action)
    
    # Get analytics
    response = requests.get(f"{BASE_URL}/analytics/{session_id}")
    analytics = response.json()
    
    print(f"Session: {analytics['session_id'][:8]}...")
    print(f"Task: {analytics['task']}")
    print(f"Status: {analytics['status']}")
    print(f"\nPerformance Metrics:")
    print(f"   Steps: {analytics['metrics']['steps']}")
    print(f"   Score: {analytics['metrics']['score']:.3f} ⭐")
    print(f"   Time Elapsed: {analytics['metrics']['time_elapsed']:.2f}s")
    print(f"   Efficiency: {analytics['metrics']['efficiency']:.3f} (score/step)")
    print(f"   Step Rate: {analytics['metrics']['step_rate']:.2f} steps/second")
    
    print(f"\nCompetitive Ranking:")
    print(f"   Global Rank: #{analytics['ranking']['global_rank']}")
    print(f"   Total Competitors: {analytics['ranking']['total_competitors']}")


def demo_websocket():
    """Demonstrate WebSocket streaming."""
    print_header("⚡ WEBSOCKET REAL-TIME STREAMING")
    
    print("To connect to WebSocket for real-time updates:")
    print("\nJavaScript Example:")
    print("""
    const sessionId = 'your-session-id';
    const ws = new WebSocket(`ws://localhost:7860/ws/stream/${sessionId}`);
    
    ws.onmessage = (event) => {
        const update = JSON.parse(event.data);
        console.log('Real-time update:', update);
        
        // Handle different update types
        if (update.type === 'metrics') {
            console.log('Leaderboard:', update.data.leaderboard);
        } else if (update.type === 'session_update') {
            console.log('Session update:', update.metrics);
        }
    };
    """)
    
    print("\nPython Example:")
    print("""
    import asyncio
    import websockets
    import json
    
    async def connect():
        uri = "ws://localhost:7860/ws/stream/session-id"
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print("Live update:", data)
    
    asyncio.run(connect())
    """)


def print_summary():
    """Print a summary of all features."""
    print_header("🚀 HACKATHON FEATURES SUMMARY")
    
    features = [
        ("⚡ Challenge Mode", "Time-based competitions with speed bonuses (1.5x multiplier)"),
        ("🏆 Leaderboard", "Real-time rankings updated every 2 seconds"),
        ("📊 Live Stats", "Aggregate metrics and performance analytics"),
        ("🎯 Multiplayer Arena", "Compete with other agents simultaneously"),
        ("⚡ WebSocket API", "Real-time metric streaming"),
        ("📈 Analytics", "Detailed per-session performance metrics"),
        ("💡 Beautiful UI", "Modern dashboard at `/`"),
    ]
    
    for feature, description in features:
        print(f"{feature}:")
        print(f"   → {description}\n")
    
    print("🔗 API Endpoints:")
    endpoints = [
        ("POST", "/challenge/reset", "Start a time-based challenge"),
        ("POST", "/challenge/step/{session_id}", "Execute action in challenge"),
        ("GET", "/leaderboard", "Get real-time rankings"),
        ("GET", "/live-stats", "Get aggregate statistics"),
        ("GET", "/arena/join", "Join multiplayer arena"),
        ("GET", "/analytics/{session_id}", "Get session analytics"),
        ("WS", "/ws/stream/{session_id}", "Real-time WebSocket stream"),
    ]
    
    for method, endpoint, desc in endpoints:
        print(f"   {method:4s} {endpoint:30s} - {desc}")
    
    print("\n💼 Web Dashboard:")
    print(f"   Open http://localhost:7860 in your browser!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🚨 Incident Commander - Hackathon Quickstart")
    print("="*60)
    print("\n⚠️  Make sure the server is running:")
    print("   uvicorn api.main:app --host 0.0.0.0 --port 7860")
    
    try:
        # Run all demos
        demo_challenge_mode()
        time.sleep(1)
        
        demo_leaderboard()
        time.sleep(1)
        
        demo_live_stats()
        time.sleep(1)
        
        demo_multiplayer_arena()
        time.sleep(1)
        
        demo_analytics()
        time.sleep(1)
        
        demo_websocket()
        
        print_summary()
        
        print("\n" + "="*60)
        print("✅ All demos completed successfully!")
        print("="*60)
        print("\n🎉 You're ready to win the hackathon!")
        print("   Visit: http://localhost:7860 for the interactive dashboard")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("   Make sure the server is running on http://localhost:7860")
        print("   Run: uvicorn api.main:app --host 0.0.0.0 --port 7860")
    except Exception as e:
        print(f"\n❌ Error: {e}")

#!/usr/bin/env python3
"""
Test harness to validate all score paths return strictly (0, 1) range.
Run this to find any boundary values being returned.
"""

import sys
import requests
import time
import json

BASE_URL = "http://localhost:7860"

def test_grader_endpoint():
    """Test /grader endpoint for all task types."""
    print("\n" + "="*60)
    print("Testing /grader endpoint")
    print("="*60)
    
    for task_id in ["easy", "medium", "hard"]:
        print(f"\nTask: {task_id}")
        
        # Reset first
        requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
        
        # Take a step
        requests.post(f"{BASE_URL}/step", json={
            "action_type": "identify",
            "target": "auto"
        })
        
        # Get score
        response = requests.get(f"{BASE_URL}/grader", params={"task_id": task_id})
        data = response.json()
        score = data.get("score")
        
        print(f"  Score: {score}")
        print(f"  Type: {type(score)}")
        print(f"  Is 0.0? {score == 0.0}")
        print(f"  Is 1.0? {score == 1.0}")
        print(f"  <= 0.0? {score <= 0.0}")
        print(f"  >= 1.0? {score >= 1.0}")
        print(f"  Valid? {0 < score < 1}")
        
        if score <= 0.0 or score >= 1.0 or not (0 < score < 1):
            print(f"  ❌ INVALID SCORE!")
            return False
    
    print("\n✅ Grader endpoint OK")
    return True


def test_step_endpoint():
    """Test /step endpoint reward extraction."""
    print("\n" + "="*60)
    print("Testing /step endpoint")
    print("="*60)
    
    for task_id in ["easy", "medium", "hard"]:
        print(f"\nTask: {task_id}")
        
        # Reset
        requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
        
        # Take multiple steps
        for i in range(3):
            response = requests.post(f"{BASE_URL}/step", json={
                "action_type": "identify" if i == 0 else "fix",
                "target": "auto"
            })
            data = response.json()
            
            # Step endpoint returns [obs, reward, done, info]
            if isinstance(data, list) and len(data) > 1:
                reward_data = data[1]
                if isinstance(reward_data, dict):
                    reward = reward_data.get("reward", 0.1)
                else:
                    reward = reward_data
                
                print(f"  Step {i+1} reward: {reward}")
                print(f"  Valid? {0 < reward < 1}")
                
                if reward <= 0.0 or reward >= 1.0 or not (0 < reward < 1):
                    print(f"  ❌ INVALID REWARD!")
                    return False
    
    print("\n✅ Step endpoint OK")
    return True


def test_challenge_endpoint():
    """Test /challenge/step endpoint."""
    print("\n" + "="*60)
    print("Testing /challenge/step endpoint")
    print("="*60)
    
    for task_id in ["easy", "medium", "hard"]:
        print(f"\nTask: {task_id}")
        
        # Reset challenge
        reset_resp = requests.post(f"{BASE_URL}/challenge/reset", json={"task_id": task_id})
        session_data = reset_resp.json()
        session_id = session_data.get("session_id")
        
        print(f"  Session ID: {session_id}")
        
        # Take steps in challenge mode
        for i in range(2):
            response = requests.post(f"{BASE_URL}/challenge/step/{session_id}", json={
                "action_type": "identify" if i == 0 else "fix",
                "target": "auto"
            })
            data = response.json()
            
            # Challenge endpoint returns [obs, reward_dict, done, info]
            if isinstance(data, list) and len(data) > 1:
                reward_data = data[1]
                if isinstance(reward_data, dict):
                    reward = reward_data.get("reward", 0.1)
                else:
                    reward = reward_data
                
                print(f"  Step {i+1} reward: {reward}")
                print(f"  Valid? {0 < reward < 1}")
                
                if reward <= 0.0 or reward >= 1.0 or not (0 < reward < 1):
                    print(f"  ❌ INVALID REWARD!")
                    return False
    
    print("\n✅ Challenge endpoint OK")
    return True


def test_metrics_endpoint():
    """Test /metrics endpoint."""
    print("\n" + "="*60)
    print("Testing /metrics endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/metrics")
    data = response.json()
    print(f"Data: {json.dumps(data, indent=2)}")
    print("\n✅ Metrics endpoint OK")
    return True


def test_leaderboard_endpoint():
    """Test /leaderboard endpoint."""
    print("\n" + "="*60)
    print("Testing /leaderboard endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/leaderboard")
    data = response.json()
    
    leaderboard = data.get("leaderboard", [])
    if leaderboard:
        for entry in leaderboard:
            score = entry.get("score")
            print(f"  Score: {score} - Valid? {0 < score < 1}")
            if score <= 0.0 or score >= 1.0 or not (0 < score < 1):
                print(f"  ❌ INVALID SCORE IN LEADERBOARD!")
                return False
    
    print("\n✅ Leaderboard endpoint OK")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SCORE VALIDATION TEST HARNESS")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    
    # Wait for server to be ready
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            print(f"\n✅ Server is running")
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"\n❌ Cannot connect to server at {BASE_URL}")
                print(f"   Make sure to run: python3 -m uvicorn api.main:app --port 7860 --host 0.0.0.0")
                return False
            print(f"   Waiting for server... (attempt {attempt+1}/{max_retries})")
            time.sleep(1)
    
    results = []
    
    try:
        results.append(("Grader", test_grader_endpoint()))
        results.append(("Step", test_step_endpoint()))
        results.append(("Challenge", test_challenge_endpoint()))
        results.append(("Metrics", test_metrics_endpoint()))
        results.append(("Leaderboard", test_leaderboard_endpoint()))
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED - Ready for validator")
    else:
        print("\n❌ SOME TESTS FAILED - Need to fix")
        sys.exit(1)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

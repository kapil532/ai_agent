#!/usr/bin/env python3
"""OpenEnv compliance test script"""
import httpx
import sys

base_url = 'http://localhost:8080'

def test_reset():
    print('1. Testing /reset endpoint...')
    response = httpx.post(f'{base_url}/reset', json={'task_id': 'easy'})
    assert response.status_code == 200, f"Reset failed: {response.status_code}"
    data = response.json()
    assert 'observation' in data, 'Missing observation in reset'
    assert 'info' in data, 'Missing info in reset'
    print('   ✓ Reset format correct\n')
    return True

def test_step():
    print('2. Testing /step endpoint...')
    response = httpx.post(f'{base_url}/step', json={'action_type': 'identify', 'target': 'auth'})
    assert response.status_code == 200, f"Step failed: {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f'Step should return list, got {type(data).__name__}'
    assert len(data) == 4, f'Step should return 4 elements, got {len(data)}'
    obs, reward, done, info = data
    print('   ✓ Step format correct: [obs, reward, done, info]\n')
    return True

def test_state():
    print('3. Testing /state endpoint...')
    response = httpx.get(f'{base_url}/state')
    assert response.status_code == 200, f"State failed: {response.status_code}"
    state = response.json()
    assert isinstance(state, dict), f'State should return dict'
    print('   ✓ State endpoint works\n')
    return True

def test_tasks():
    print('4. Testing /tasks endpoint...')
    response = httpx.get(f'{base_url}/tasks')
    assert response.status_code == 200, f"Tasks failed: {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), 'Tasks should return dict'
    assert 'tasks' in data, 'Missing "tasks" key'
    tasks = data['tasks']
    assert isinstance(tasks, list), 'tasks value should be list'
    assert len(tasks) >= 3, f'Should have at least 3 tasks, got {len(tasks)}'
    print(f'   ✓ Tasks endpoint works ({len(tasks)} tasks)\n')
    return True

def test_grader():
    print('5. Testing /grader endpoint...')
    response = httpx.get(f'{base_url}/grader?task_id=easy')
    assert response.status_code == 200, f"Grader failed: {response.status_code}"
    score = response.json()
    assert 'score' in score, 'Missing score in grader response'
    assert isinstance(score['score'], (int, float)), 'Score should be numeric'
    print('   ✓ Grader endpoint works\n')
    return True

def test_health():
    print('6. Testing /health endpoint...')
    response = httpx.get(f'{base_url}/health')
    assert response.status_code == 200, f"Health failed: {response.status_code}"
    health = response.json()
    assert 'status' in health, 'Missing status in health response'
    print('   ✓ Health endpoint works\n')
    return True

def test_schema():
    print('7. Testing /schema endpoint...')
    response = httpx.get(f'{base_url}/schema')
    assert response.status_code == 200, f"Schema failed: {response.status_code}"
    schema = response.json()
    assert isinstance(schema, dict), 'Schema should return dict'
    print('   ✓ Schema endpoint works\n')
    return True

if __name__ == '__main__':
    print('=== OpenEnv Compliance Test ===\n')
    
    try:
        test_reset()
        test_step()
        test_state()
        test_tasks()
        test_grader()
        test_health()
        test_schema()
        
        print('=== ✓ All Tests Passed ===')
        sys.exit(0)
    except Exception as e:
        print(f'\n✗ Test failed: {e}')
        sys.exit(1)

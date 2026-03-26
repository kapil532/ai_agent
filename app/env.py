from app.state_manager import StateManager
from app.tasks import load_task
from app.rewards import compute_reward

class IncidentEnv:
    def __init__(self):
        self.state_obj = None
        self.task = None
        self.done = False

    def reset(self, task_id="easy"):
        self.task = load_task(task_id)
        self.state_obj = StateManager(self.task)
        self.done = False
        return self.state_obj.get_observation()

    def step(self, action):
        self.state_obj.apply_action(action)
        reward = compute_reward(action)

        if self.state_obj.is_terminal():
            self.done = True

        return (self.state_obj.get_observation(), reward, self.done, {})

    def state(self):
        return self.state_obj.serialize()

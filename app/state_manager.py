class StateManager:
    def __init__(self, task):
        self.logs = task["logs"]
        self.step_count = 0
        self.actions = []

    def apply_action(self, action):
        self.step_count += 1
        self.actions.append(action)

    def get_observation(self):
        return {
            "logs": self.logs,
            "task": "active",
            "step_count": self.step_count
        }

    def is_terminal(self):
        return self.step_count >= 5

    def serialize(self):
        return {"actions": self.actions}

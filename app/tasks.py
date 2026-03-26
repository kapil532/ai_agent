def load_task(task_id):
    if task_id == "easy":
        return {
            "logs": [
                {"timestamp": "10:00", "service": "auth", "message": "NullPointerException"}
            ],
            "root_cause": "NullPointerException"
        }

    if task_id == "medium":
        return {
            "logs": [
                {"timestamp": "10:01", "service": "payment", "message": "DB connection failed"}
            ],
            "service": "payment"
        }

    if task_id == "hard":
        return {
            "logs": [
                {"timestamp": "10:02", "service": "checkout", "message": "Timeout error"},
                {"timestamp": "10:03", "service": "checkout", "message": "Retry failed"}
            ],
            "steps": ["identify", "fix", "notify"]
        }

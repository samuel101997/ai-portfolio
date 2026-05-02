# workflow/logger.py - Execution logging for the automation workflow
# Logs every classification and action to a JSON file for analysis

import json
import os
from datetime import datetime
from config import LOG_FILE_PATH


def load_logs():
    """Load existing logs from file."""
    if os.path.exists(LOG_FILE_PATH) and os.path.getsize(LOG_FILE_PATH) > 0:
        with open(LOG_FILE_PATH, "r") as f:
            return json.load(f)
    return []


def save_log(entry):
    """Append a log entry and save to file."""
    logs = load_logs()
    entry["timestamp"] = datetime.now().isoformat()
    entry["log_id"] = len(logs) + 1
    logs.append(entry)

    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    return entry


def clear_logs():
    """Clear all logs."""
    with open(LOG_FILE_PATH, "w") as f:
        json.dump([], f)
# config.py - Central configuration for the automation workflow

OLLAMA_MODEL = "mistral"
OLLAMA_BASE_URL = "http://localhost:11434"

# Intent categories the classifier can assign
INTENT_CATEGORIES = [
    "billing",
    "technical_support",
    "cancellation",
    "plan_change",
    "general_inquiry",
    "complaint",
]

# Priority levels
PRIORITY_LEVELS = ["low", "medium", "high", "urgent"]

# Paths
SAMPLE_MESSAGES_PATH = "sample_messages/test_messages.json"
LOG_FILE_PATH = "logs/workflow_log.json"
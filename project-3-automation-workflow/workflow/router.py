# workflow/router.py - Routes classified messages to appropriate actions
# Orchestrates the full workflow: classify → decide actions → execute → log

from workflow.classifier import classify_message
from workflow.actions import draft_reply, create_ticket, determine_actions
from workflow.logger import save_log


def process_message(customer_name, message):
    """Full workflow: classify, route, act, and log."""

    # Step 1: Classify the message
    classification = classify_message(message)

    # Step 2: Determine actions
    actions = determine_actions(classification)

    # Step 3: Execute actions
    ticket = create_ticket(customer_name, message, classification)
    reply = draft_reply(customer_name, message, classification)

    # Step 4: Build result
    result = {
        "customer": customer_name,
        "classification": classification,
        "actions_taken": actions,
        "ticket": ticket,
        "draft_reply": reply,
    }

    # Step 5: Log everything
    save_log(result)

    return result


# Quick test
if __name__ == "__main__":
    import json

    result = process_message(
        "Sarah Chen",
        "I was charged $45 for a data add-on I never purchased. Remove it from my bill."
    )

    print(json.dumps(result, indent=2))
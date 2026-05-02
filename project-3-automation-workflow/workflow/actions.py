# workflow/actions.py - Automated actions based on classification
# Drafts replies, creates tickets, flags escalations

import ollama
from config import OLLAMA_MODEL


def draft_reply(customer_name, message, classification):
    """Draft an auto-reply email based on the classification."""
    prompt = f"""You are a professional customer support agent for NovaTel Mobile.
Draft a brief, empathetic reply email to the customer based on their message and the classification.

Customer name: {customer_name}
Customer message: {message}
Intent: {classification['intent']}
Priority: {classification['priority']}
Summary: {classification['summary']}

Rules:
- Address the customer by name
- Acknowledge their specific issue
- Provide a clear next step or resolution
- Keep it under 150 words
- Be professional but warm
- Sign off as "NovaTel Support Team"
- Do NOT make up specific account details or promise exact refund amounts"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]


def create_ticket(customer_name, message, classification):
    """Create a structured support ticket."""
    priority_map = {"urgent": "P1", "high": "P2", "medium": "P3", "low": "P4"}

    ticket = {
        "customer": customer_name,
        "priority_code": priority_map.get(classification["priority"], "P3"),
        "intent": classification["intent"],
        "summary": classification["summary"],
        "key_entities": classification.get("key_entities", []),
        "original_message": message,
        "status": "open",
    }

    return ticket


def determine_actions(classification):
    """Decide what actions to take based on classification."""
    actions = []
    intent = classification["intent"]
    priority = classification["priority"]

    # Always create a ticket
    actions.append("create_ticket")

    # Always draft a reply
    actions.append("draft_reply")

    # Escalation rules
    if priority in ["urgent", "high"]:
        actions.append("escalate")

    if intent == "cancellation":
        actions.append("flag_retention")

    if intent == "complaint" and priority in ["urgent", "high"]:
        actions.append("escalate_manager")

    if intent == "billing":
        actions.append("flag_billing_review")

    return actions
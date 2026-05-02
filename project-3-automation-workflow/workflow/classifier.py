# workflow/classifier.py - LLM-based intent classification
# Uses Mistral to classify customer messages into intent categories

import json
import ollama
from config import OLLAMA_MODEL, INTENT_CATEGORIES, PRIORITY_LEVELS


CLASSIFICATION_PROMPT = """You are a customer support message classifier for NovaTel Mobile, a telecommunications company.

Analyze the customer message and respond with ONLY a valid JSON object (no other text):

{{
    "intent": "<one of: {intents}>",
    "priority": "<one of: {priorities}>",
    "confidence": <number between 0.0 and 1.0>,
    "summary": "<one sentence summary of the customer's issue>",
    "key_entities": ["<list of important details like account numbers, plan names, devices>"]
}}

Classification guidelines:
- billing: Charges, payments, refunds, bill disputes, fees
- technical_support: Network issues, device problems, service not working, setup help
- cancellation: Customer wants to cancel or leave NovaTel
- plan_change: Upgrade, downgrade, switch plans, add/remove features
- general_inquiry: Questions about plans, features, policies, no action needed
- complaint: Angry customer, repeated issues, threats to escalate, CCTS mention

Priority guidelines:
- urgent: Security concerns, CCTS threats, 911 issues, account compromise
- high: Service completely down, repeated unresolved issues, cancellation with anger
- medium: Billing disputes, partial service issues, standard cancellation
- low: General questions, plan inquiries, setup help

Customer message: {message}"""


def classify_message(message):
    """Classify a customer message using Mistral."""
    prompt = CLASSIFICATION_PROMPT.format(
        intents=", ".join(INTENT_CATEGORIES),
        priorities=", ".join(PRIORITY_LEVELS),
        message=message,
    )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_response = response["message"]["content"]

    try:
        # Try to extract JSON from the response
        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1
        if start != -1 and end > start:
            result = json.loads(raw_response[start:end])
        else:
            result = json.loads(raw_response)

        # Validate fields
        if result.get("intent") not in INTENT_CATEGORIES:
            result["intent"] = "general_inquiry"
        if result.get("priority") not in PRIORITY_LEVELS:
            result["priority"] = "medium"
        if not isinstance(result.get("confidence"), (int, float)):
            result["confidence"] = 0.5

        return result

    except json.JSONDecodeError:
        return {
            "intent": "general_inquiry",
            "priority": "medium",
            "confidence": 0.0,
            "summary": "Classification failed - could not parse LLM response",
            "key_entities": [],
            "raw_response": raw_response,
        }


# Quick test
if __name__ == "__main__":
    test_msg = "I was charged $45 for a data add-on I never purchased. Remove it from my bill."
    print(f"Message: {test_msg}\n")
    result = classify_message(test_msg)
    print(json.dumps(result, indent=2))
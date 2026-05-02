# tests/test_classifier.py - Classification accuracy tests

import json
import sys
import os

WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "project-3-automation-workflow")
sys.path.insert(0, WORKFLOW_PATH)

from workflow.classifier import classify_message

PRIORITY_ORDER = ["low", "medium", "high", "urgent"]


def priority_meets_minimum(actual, minimum):
    if actual not in PRIORITY_ORDER or minimum not in PRIORITY_ORDER:
        return False
    return PRIORITY_ORDER.index(actual) >= PRIORITY_ORDER.index(minimum)


def run_classifier_tests(test_cases_path):
    """Run all classifier test cases and return results."""
    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    results = []

    for tc in test_cases:
        result = {
            "id": tc["id"],
            "message": tc["message"][:80] + "..." if len(tc["message"]) > 80 else tc["message"],
            "category": tc["category"],
            "passed": False,
            "details": "",
        }

        try:
            classification = classify_message(tc["message"])
            result["actual_intent"] = classification["intent"]
            result["actual_priority"] = classification["priority"]
            result["confidence"] = classification.get("confidence", 0)

            intent_correct = classification["intent"] == tc["expected_intent"]
            priority_ok = priority_meets_minimum(
                classification["priority"], tc["expected_priority_min"]
            )

            result["passed"] = intent_correct and priority_ok

            if result["passed"]:
                result["details"] = (
                    f"Intent: {classification['intent']} ✓ | "
                    f"Priority: {classification['priority']} ✓ | "
                    f"Confidence: {classification.get('confidence', 0):.0%}"
                )
            else:
                issues = []
                if not intent_correct:
                    issues.append(
                        f"Intent: expected {tc['expected_intent']}, "
                        f"got {classification['intent']}"
                    )
                if not priority_ok:
                    issues.append(
                        f"Priority: expected >= {tc['expected_priority_min']}, "
                        f"got {classification['priority']}"
                    )
                result["details"] = " | ".join(issues)

        except Exception as e:
            result["details"] = f"Error: {str(e)}"

        results.append(result)

    return results


if __name__ == "__main__":
    from suite_config import CLASSIFIER_TEST_CASES
    results = run_classifier_tests(CLASSIFIER_TEST_CASES)
    passed = sum(1 for r in results if r["passed"])
    print(f"\nClassifier Tests: {passed}/{len(results)} passed")
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"  {status} {r['id']}: {r['details']}")
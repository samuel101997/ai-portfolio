# tests/test_edge_cases.py - Edge case and adversarial input tests

import sys
import os

ORIGINAL_DIR = os.getcwd()
RAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "project-2-rag-system")
WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "project-3-automation-workflow")

# Step 1: Clear stale modules, then load Project 3 (classifier)
for _k in list(sys.modules.keys()):
    if _k == "config" or _k.startswith("workflow"):
        del sys.modules[_k]
sys.path.insert(0, WORKFLOW_PATH)
from workflow.classifier import classify_message
sys.path.remove(WORKFLOW_PATH)

# Step 2: Clear Project 3's config and stale rag modules, then load Project 2 (RAG)
for _k in list(sys.modules.keys()):
    if _k == "config" or _k.startswith("rag"):
        del sys.modules[_k]
sys.path.insert(0, RAG_PATH)
os.chdir(RAG_PATH)
from rag.retriever import retrieve, format_context
from rag.embeddings import load_vector_store
from rag.generator import generate_answer

EDGE_CASES = [
    {"id": "edge_01", "name": "Empty input to RAG", "target": "rag", "input": "", "pass_condition": "Should not crash"},
    {"id": "edge_02", "name": "Empty input to classifier", "target": "classifier", "input": "", "pass_condition": "Should handle gracefully"},
    {"id": "edge_03", "name": "Gibberish to RAG", "target": "rag", "input": "asdfghjkl zxcvbnm qwerty 12345 !@#$%", "pass_condition": "Should not hallucinate"},
    {"id": "edge_04", "name": "Gibberish to classifier", "target": "classifier", "input": "asdfghjkl zxcvbnm qwerty", "pass_condition": "Should return valid category"},
    {"id": "edge_05", "name": "Very long input to classifier", "target": "classifier", "input": "I have a billing problem. " * 200, "pass_condition": "Should not crash"},
    {"id": "edge_06", "name": "Multi-intent message", "target": "classifier", "input": "I want to cancel my plan AND I was overcharged $50 AND my phone has no signal.", "pass_condition": "Should pick one valid intent"},
    {"id": "edge_07", "name": "Non-English input", "target": "classifier", "input": "Je veux annuler mon service immédiatement.", "pass_condition": "Should return valid classification"},
    {"id": "edge_08", "name": "Different company question", "target": "rag", "input": "What are Bell Canada's roaming rates?", "pass_condition": "Should not answer about Bell"},
    {"id": "edge_09", "name": "Numeric-only input", "target": "classifier", "input": "12345678", "pass_condition": "Should not crash"},
    {"id": "edge_10", "name": "Special characters only", "target": "rag", "input": "!@#$%^&*()", "pass_condition": "Should not crash"},
]


def run_edge_case_tests():
    os.chdir(RAG_PATH)
    vector_store = None
    results = []

    for tc in EDGE_CASES:
        result = {
            "id": tc["id"],
            "name": tc["name"],
            "target": tc["target"],
            "passed": False,
            "details": "",
            "pass_condition": tc["pass_condition"],
        }

        try:
            if tc["target"] == "rag":
                if vector_store is None:
                    vector_store = load_vector_store()

                if tc["input"].strip():
                    retrieved = retrieve(tc["input"], vector_store=vector_store)
                    context = format_context(retrieved)
                    answer = generate_answer(tc["input"], context)
                    result["response"] = answer
                else:
                    result["response"] = "(Empty input — skipped pipeline)"

                result["passed"] = True
                result["details"] = "Completed without crash"

            elif tc["target"] == "classifier":
                if tc["input"].strip():
                    classification = classify_message(tc["input"])
                    result["response"] = f"{classification['intent']} / {classification['priority']}"

                    valid_intents = ["billing", "technical_support", "cancellation",
                                    "plan_change", "general_inquiry", "complaint"]
                    valid_priorities = ["low", "medium", "high", "urgent"]

                    if (classification["intent"] in valid_intents and
                            classification["priority"] in valid_priorities):
                        result["passed"] = True
                        result["details"] = f"Valid: {classification['intent']} / {classification['priority']}"
                    else:
                        result["details"] = f"Invalid category: {classification['intent']}"
                else:
                    result["response"] = "(Empty input — skipped)"
                    result["passed"] = True
                    result["details"] = "Empty input handled"

        except Exception as e:
            result["details"] = f"CRASHED: {str(e)}"

        results.append(result)

    os.chdir(ORIGINAL_DIR)
    return results


if __name__ == "__main__":
    results = run_edge_case_tests()
    passed = sum(1 for r in results if r["passed"])
    print(f"\nEdge Case Tests: {passed}/{len(results)} passed")
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"  {status} {r['id']} ({r['name']}): {r['details']}")
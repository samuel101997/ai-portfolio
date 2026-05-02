# tests/test_rag.py - RAG system accuracy and hallucination tests

import json
import sys
import os

ORIGINAL_DIR = os.getcwd()
RAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "project-2-rag-system")
sys.path.insert(0, RAG_PATH)
os.chdir(RAG_PATH)

from rag.retriever import retrieve, format_context
from rag.embeddings import load_vector_store
from rag.generator import generate_answer


def run_rag_tests(test_cases_path):
    """Run all RAG test cases and return results."""
    os.chdir(RAG_PATH)

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    vector_store = load_vector_store()
    results = []

    for tc in test_cases:
        result = {
            "id": tc["id"],
            "question": tc["question"],
            "category": tc["category"],
            "passed": False,
            "details": "",
        }

        try:
            retrieved = retrieve(tc["question"], vector_store=vector_store)
            context = format_context(retrieved)
            answer = generate_answer(tc["question"], context)
            result["answer"] = answer

            answer_lower = answer.lower()
            found_keywords = []
            missing_keywords = []

            for kw in tc["expected_keywords"]:
                if kw.lower() in answer_lower:
                    found_keywords.append(kw)
                else:
                    missing_keywords.append(kw)

            if found_keywords:
                result["passed"] = True
                result["details"] = f"Found: {found_keywords}"
            else:
                result["details"] = f"Missing all keywords: {missing_keywords}"

            if tc.get("expected_source"):
                sources = [doc.metadata.get("source", "") for doc, _ in retrieved]
                source_match = any(tc["expected_source"] in s for s in sources)
                result["source_correct"] = source_match
                if not source_match:
                    result["details"] += f" | Wrong source retrieved"

        except Exception as e:
            result["details"] = f"Error: {str(e)}"

        results.append(result)

    os.chdir(ORIGINAL_DIR)
    return results


if __name__ == "__main__":
    from suite_config import RAG_TEST_CASES
    results = run_rag_tests(RAG_TEST_CASES)
    passed = sum(1 for r in results if r["passed"])
    print(f"\nRAG Tests: {passed}/{len(results)} passed")
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"  {status} {r['id']}: {r['details']}")
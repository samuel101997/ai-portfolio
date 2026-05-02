# suite_config.py - Configuration for the AI Testing Suite

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_ROOT = os.path.dirname(PROJECT_ROOT)

RAG_PROJECT_PATH = os.path.join(PORTFOLIO_ROOT, "project-2-rag-system")
WORKFLOW_PROJECT_PATH = os.path.join(PORTFOLIO_ROOT, "project-3-automation-workflow")

sys.path.insert(0, RAG_PROJECT_PATH)
sys.path.insert(0, WORKFLOW_PROJECT_PATH)

RAG_TEST_CASES = os.path.join(PROJECT_ROOT, "test_data", "rag_test_cases.json")
CLASSIFIER_TEST_CASES = os.path.join(PROJECT_ROOT, "test_data", "classifier_test_cases.json")
SECURITY_TEST_CASES = os.path.join(PROJECT_ROOT, "test_data", "security_test_cases.json")

RESULTS_PATH = os.path.join(PROJECT_ROOT, "results.md")
PASS_THRESHOLD = 0.7
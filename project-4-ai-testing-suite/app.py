# app.py - Streamlit dashboard for the AI Testing Suite

import json
import sys
import os
from datetime import datetime

import streamlit as st

# Suite config only
from suite_config import RAG_TEST_CASES, CLASSIFIER_TEST_CASES, SECURITY_TEST_CASES, RESULTS_PATH

st.set_page_config(page_title="NovaTel AI Testing Suite", page_icon="🧪")
st.title("🧪 NovaTel AI Testing Suite")
st.caption("Automated testing for RAG, classification, security, and edge cases.")


def generate_report(all_results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"# AI Testing Suite - Results Report\n\n"
    report += f"**Generated:** {timestamp}\n\n"

    total_tests = 0
    total_passed = 0

    for category, results in all_results.items():
        passed = sum(1 for r in results if r["passed"])
        total = len(results)
        total_tests += total
        total_passed += passed
        pct = (passed / total * 100) if total > 0 else 0

        report += f"## {category}\n\n"
        report += f"**Score: {passed}/{total} ({pct:.0f}%)**\n\n"
        report += f"| Test ID | Description | Result | Details |\n"
        report += f"|---------|-------------|--------|---------|\n"

        for r in results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            desc = r.get("name") or r.get("question", r.get("message", r.get("type", "")))
            if len(str(desc)) > 60:
                desc = str(desc)[:57] + "..."
            details = r.get("details", "")
            if len(str(details)) > 80:
                details = str(details)[:77] + "..."
            report += f"| {r['id']} | {desc} | {status} | {details} |\n"

        report += "\n"

    overall_pct = (total_passed / total_tests * 100) if total_tests > 0 else 0
    report += f"## Overall Summary\n\n"
    report += f"| Metric | Value |\n"
    report += f"|--------|-------|\n"
    report += f"| Total Tests | {total_tests} |\n"
    report += f"| Passed | {total_passed} |\n"
    report += f"| Failed | {total_tests - total_passed} |\n"
    report += f"| Pass Rate | {overall_pct:.0f}% |\n"

    return report


# --- Sidebar ---
with st.sidebar:
    st.header("Test Categories")
    run_rag = st.checkbox("RAG Accuracy & Hallucination", value=True)
    run_cls = st.checkbox("Classifier Accuracy", value=True)
    run_sec = st.checkbox("Security (Injection & Privacy)", value=True)
    run_edge = st.checkbox("Edge Cases", value=True)

# --- Main ---
if st.button("🚀 Run All Selected Tests", type="primary"):
    all_results = {}

    if run_rag:
        with st.spinner("Running RAG tests..."):
            from tests.test_rag import run_rag_tests
            rag_results = run_rag_tests(RAG_TEST_CASES)
            all_results["RAG Accuracy & Hallucination"] = rag_results

        passed = sum(1 for r in rag_results if r["passed"])
        st.markdown(f"### RAG Tests: {passed}/{len(rag_results)} passed")
        for r in rag_results:
            status = "✅" if r["passed"] else "❌"
            with st.expander(f"{status} {r['id']}: {r['question']}"):
                st.write(f"**Category:** {r['category']}")
                st.write(f"**Result:** {r['details']}")
                if r.get("answer"):
                    st.write(f"**Answer:** {r['answer'][:300]}")

    if run_cls:
        with st.spinner("Running classifier tests..."):
            # Clean module cache before importing classifier tests
            for mod in list(sys.modules.keys()):
                if mod == "config" or mod.startswith("rag"):
                    del sys.modules[mod]
            from tests.test_classifier import run_classifier_tests
            cls_results = run_classifier_tests(CLASSIFIER_TEST_CASES)
            all_results["Classifier Accuracy"] = cls_results

        passed = sum(1 for r in cls_results if r["passed"])
        st.markdown(f"### Classifier Tests: {passed}/{len(cls_results)} passed")
        for r in cls_results:
            status = "✅" if r["passed"] else "❌"
            with st.expander(f"{status} {r['id']}: {r['message']}"):
                st.write(f"**Expected:** {r.get('category')}")
                st.write(f"**Result:** {r['details']}")

    if run_sec:
        with st.spinner("Running security tests..."):
            for mod in list(sys.modules.keys()):
                if mod == "config":
                    del sys.modules[mod]
            from tests.test_security import run_security_tests
            sec_results = run_security_tests(SECURITY_TEST_CASES)
            all_results["Security Tests"] = sec_results

        passed = sum(1 for r in sec_results if r["passed"])
        st.markdown(f"### Security Tests: {passed}/{len(sec_results)} passed")
        for r in sec_results:
            status = "✅" if r["passed"] else "❌"
            with st.expander(f"{status} {r['id']} ({r['type']})"):
                st.write(f"**Pass Condition:** {r['pass_condition']}")
                st.write(f"**Result:** {r['details']}")
                if r.get("response"):
                    st.write(f"**Response:** {str(r['response'])[:300]}")

    if run_edge:
        with st.spinner("Running edge case tests..."):
            for mod in list(sys.modules.keys()):
                if mod == "config":
                    del sys.modules[mod]
            from tests.test_edge_cases import run_edge_case_tests
            edge_results = run_edge_case_tests()
            all_results["Edge Cases"] = edge_results

        passed = sum(1 for r in edge_results if r["passed"])
        st.markdown(f"### Edge Case Tests: {passed}/{len(edge_results)} passed")
        for r in edge_results:
            status = "✅" if r["passed"] else "❌"
            with st.expander(f"{status} {r['id']}: {r['name']}"):
                st.write(f"**Pass Condition:** {r['pass_condition']}")
                st.write(f"**Result:** {r['details']}")
                if r.get("response"):
                    st.write(f"**Response:** {str(r['response'])[:300]}")

    # Overall summary
    if all_results:
        st.markdown("---")
        total_tests = sum(len(r) for r in all_results.values())
        total_passed = sum(sum(1 for t in r if t["passed"]) for r in all_results.values())
        st.markdown(f"## Overall: {total_passed}/{total_tests} passed ({total_passed/total_tests*100:.0f}%)")

        report = generate_report(all_results)
        with open(RESULTS_PATH, "w") as f:
            f.write(report)
        st.success(f"Report saved to results.md")

else:
    st.info("Select test categories in the sidebar and click 'Run All Selected Tests'.")
# Failure Cases Analysis — AI Agent System

## Overview
This document records failure cases encountered during development and testing of the Smart Research Assistant, their root causes, and the fixes applied.

---

## FC-001: ImportError — AgentExecutor not found
| Field | Description |
|-------|-------------|
| **Input** | Running `streamlit run app.py` for the first time |
| **Expected** | App launches without errors |
| **Actual** | `ImportError: cannot import name 'AgentExecutor' from 'langchain.agents'` |
| **Root Cause** | LangChain v1.2.16 restructured its package. `AgentExecutor` and `create_react_agent` moved from `langchain.agents` to `langchain_classic.agents`. The `Tool` class moved to `langchain_core.tools`. |
| **Fix Applied** | Updated imports to `from langchain_classic.agents import AgentExecutor, create_react_agent` and `from langchain_core.tools import Tool` |
| **Status** | Fixed |
| **Lesson** | Always verify import paths against the installed package version. Pinning exact versions in requirements.txt can prevent this across environments. |

---

## FC-002: Missing ddgs package
| Field | Description |
|-------|-------------|
| **Input** | Clicking "Research" button with query "Compare Solar and wind energy" |
| **Expected** | Agent searches the web and returns results |
| **Actual** | `ImportError: Could not import ddgs python package. Please install it with pip install -U ddgs` |
| **Root Cause** | `duckduckgo-search` package requires `ddgs` as an underlying dependency, but it was not pulled in automatically during pip install |
| **Fix Applied** | Ran `pip install -U ddgs` to install the missing package |
| **Status** | Fixed |
| **Lesson** | Test tool initialization separately before integrating into the full agent pipeline. Hidden transitive dependencies can break at runtime. |

---

## FC-003: Agent numbering actions and adding descriptions
| Field | Description |
|-------|-------------|
| **Input** | Query: "Compare Solar and wind energy" |
| **Expected** | Agent outputs `Action: wikipedia` followed by `Action Input: Solar energy` |
| **Actual** | Agent outputs `Action 1: wikipedia (Understanding the basics of Solar Energy)` — numbered actions with parenthetical descriptions |
| **Root Cause** | Mistral 7B was being "creative" with the ReAct format. The system prompt did not explicitly forbid numbering or adding descriptions to action names. |
| **Fix Applied** | Added CRITICAL FORMATTING RULES to the system prompt specifying exact format requirements: no numbering, no parentheses, tool name only |
| **Status** | Fixed |
| **Lesson** | Local models need very explicit formatting instructions. What seems obvious to a human (follow the exact format shown) is not obvious to a 7B parameter model. Be prescriptive, not descriptive. |

---

## FC-004: JSON parsing error on agent output
| Field | Description |
|-------|-------------|
| **Input** | Query: "Compare Solar and wind energy" |
| **Expected** | Structured research report displayed in the UI |
| **Actual** | `Agent encountered an error: Expecting value: line 1 column 1 (char 0)` |
| **Root Cause** | The agent completed its research but the output did not conform to the expected ReAct format, causing a JSONDecodeError when LangChain tried to parse the response |
| **Fix Applied** | 1. Changed `handle_parsing_errors=True` to a descriptive string that tells the LLM how to fix its format. 2. Added a separate `except json.JSONDecodeError` handler that shows a user-friendly message instead of a cryptic error |
| **Status** | Fixed |
| **Lesson** | Always handle parsing errors gracefully in agent systems. Local models frequently produce malformed output. Giving the model corrective instructions in the error handler allows self-recovery. |

---

## FC-005: Agent hitting iteration limit
| Field | Description |
|-------|-------------|
| **Input** | Query: "Compare Solar and wind energy" with MAX_ITERATIONS=5 |
| **Expected** | Complete research report covering both topics |
| **Actual** | `Agent stopped due to iteration limit or time limit` — agent ran out of iterations before synthesizing findings |
| **Root Cause** | Comparison queries require multiple tool calls (search both topics, gather pros/cons for each, then synthesize). 5 iterations was not enough for this multi-step workflow. |
| **Fix Applied** | Increased MAX_ITERATIONS from 5 to 10 in config.py |
| **Status** | Fixed |
| **Lesson** | The iteration limit should be calibrated to the complexity of expected queries. Simple lookups need 2-3 iterations, comparisons need 6-8, deep research needs 10+. Consider making this configurable per query type. |

---

## FC-006: Slow inference on local model
| Field | Description |
|-------|-------------|
| **Input** | Any multi-step research query |
| **Expected** | Response within 1-2 minutes |
| **Actual** | Complex queries take 5-10 minutes on Mistral 7B running locally |
| **Root Cause** | Local LLM inference on CPU is inherently slow. Each agent iteration requires a full LLM call, and multi-step research involves 5-10 iterations. |
| **Fix Applied** | No code fix — this is a hardware/architecture limitation. Documented as a known limitation. |
| **Status** | Known Limitation |
| **Lesson** | For production deployment, consider GPU acceleration, model quantization, a smaller model for simple tasks, or a cloud-hosted LLM API. The trade-off is cost vs speed. |

---

## Summary

| ID | Issue | Category | Status |
|----|-------|----------|--------|
| FC-001 | Import path changes in LangChain v1.2 | Dependency | Fixed |
| FC-002 | Missing ddgs transitive dependency | Dependency | Fixed |
| FC-003 | Agent creative formatting of actions | Prompt Engineering | Fixed |
| FC-004 | JSON parse error on malformed output | Error Handling | Fixed |
| FC-005 | Iteration limit too low for complex queries | Configuration | Fixed |
| FC-006 | Slow local model inference | Performance | Known Limitation |
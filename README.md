# AI Portfolio — Samuel

## Overview

A four-project AI/ML portfolio demonstrating production-ready skills across the core patterns used in modern AI engineering: autonomous agents, retrieval-augmented generation, workflow automation, and systematic AI testing.

All projects are built around a unified use case — **NovaTel Mobile**, a fictional telecom company — showing how AI systems work together in a real business context.

## Projects

### [Project 1: Smart Research Assistant (AI Agent)](./project-1-ai-agent/)
An autonomous research agent that takes a question, searches the web, pulls Wikipedia articles, and synthesizes a summarized answer — all through a conversational Streamlit interface.

**Tech:** LangChain ReAct Agent, DuckDuckGo Search, Wikipedia API, Ollama + Mistral 7B, Streamlit

**AI Pattern:** Agent with tool use

---

### [Project 2: NovaTel Customer Support Assistant (RAG)](./project-2-rag-system/)
A document Q&A system for telecom support agents. Upload internal docs (plans, policies, troubleshooting guides), ask questions in natural language, get cited answers grounded in the documents.

**Tech:** FAISS, HuggingFace Embeddings (all-MiniLM-L6-v2), LangChain, Ollama + Mistral 7B, Streamlit

**AI Pattern:** Retrieval-Augmented Generation

**Highlights:** 159 chunks from 5 documents, 4.9/5 accuracy, 2/2 hallucination tests passed, parameter tuning across 4 configurations

---

### [Project 3: NovaTel Workflow Automation](./project-3-automation-workflow/)
An AI-powered message classifier and router that takes incoming customer messages, classifies them by intent and priority, auto-creates support tickets, drafts replies, and flags urgent issues for escalation.

**Tech:** Ollama + Mistral 7B (as classifier), JSON logging, Streamlit

**AI Pattern:** LLM-based classification and rule-based automation

**Highlights:** 22 messages batch-processed, 6 intent categories, 4 priority levels, deterministic routing with full audit trail

---

### [Project 4: NovaTel AI Testing Suite](./project-4-ai-testing-suite/)
An automated test framework that evaluates Projects 2 and 3 for accuracy, security vulnerabilities, and edge case handling. Runs 40 tests and generates a scored report.

**Tech:** Custom Python test framework, Streamlit dashboard

**AI Pattern:** AI system evaluation and red-teaming

**Highlights:** 37/40 tests passed (92%), found a real prompt injection vulnerability, tested hallucination resistance, edge case robustness, and privacy leak attacks

---

## The NovaTel Story

These aren't four disconnected demos. They tell a cohesive story about how AI supports a telecom company's customer support operations:

1. **Project 1** shows I can build an AI agent that uses tools autonomously
2. **Project 2** gives support agents instant access to company knowledge
3. **Project 3** automatically triages incoming customer messages
4. **Project 4** ensures all these systems are reliable, secure, and robust

This mirrors how AI teams work in production — you build systems, connect them, and then test everything.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Mistral 7B via Ollama (100% local, no API keys) |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace, local) |
| Vector Store | FAISS |
| Framework | LangChain |
| Frontend | Streamlit |
| Language | Python 3.11 |
| Version Control | Git + GitHub |

## Setup

All projects run locally with no API keys or cloud services required.

### Prerequisites
- Python 3.11
- Ollama with Mistral model
- 16 GB RAM
- NVIDIA GPU (optional, all models run on CPU)

### Quick Start

```bash
# Clone the repo
git clone https://github.com/samuel101997/ai-portfolio.git
cd ai-portfolio

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install all dependencies
pip install -r project-2-rag-system/requirements.txt

# Start Ollama
ollama serve
ollama pull mistral

# Run any project
cd project-2-rag-system && streamlit run app.py
```

## What I Learned

1. **LLMs are versatile beyond chatbots.** The same Mistral 7B model serves as a Q&A engine (Project 2), a text classifier (Project 3), and a target for security testing (Project 4).

2. **RAG is about chunking, not just models.** Retrieval quality depends more on how you split documents than which embedding model you use. A 500-character chunk with 50-character overlap outperformed both smaller and larger configurations.

3. **AI security is non-deterministic.** The same prompt injection attack succeeded on some runs and failed on others. This makes AI security fundamentally harder than traditional application security.

4. **Evaluation separates prototypes from production.** Anyone can build a RAG demo. Systematically testing it with 40 test cases across 4 categories shows engineering maturity.

5. **Cross-project integration reveals real engineering challenges.** Python module conflicts between projects taught practical lessons about dependency management that apply to any microservice architecture.

## Contact

- **GitHub:** [samuel101997](https://github.com/samuel101997)

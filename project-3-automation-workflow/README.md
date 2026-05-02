# Project 3: NovaTel Workflow Automation

## Overview

An AI-powered automation system that classifies incoming customer support messages, routes them to the appropriate action, and logs every decision for auditability. Built for NovaTel Mobile's customer support operations.

The system takes a raw customer message, uses Mistral 7B to classify it by intent and priority, then automatically creates a support ticket, drafts a reply, and flags messages for escalation or specialist review — all in seconds.

## Use Case

**Problem:** Customer support teams manually read, categorize, and route hundreds of messages daily. This is slow, inconsistent, and error-prone. Urgent messages can sit in queue alongside low-priority inquiries.

**Solution:** An LLM-powered workflow that instantly classifies and routes every message, ensuring urgent issues get escalated, cancellations reach the retention team, and billing disputes trigger automatic review — while logging every decision for compliance.

## How It Works

```
Customer Message
       │
       ▼
┌─────────────────┐
│  Classifier      │  Mistral 7B assigns:
│  (classifier.py) │  intent, priority, confidence, summary
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Router          │  Determines actions based on rules:
│  (router.py)     │  billing → flag billing review
│                  │  cancellation → flag retention
│                  │  urgent/high → escalate
│                  │  complaint+urgent → escalate to manager
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Actions         │  Executes:
│  (actions.py)    │  → Create support ticket
│                  │  → Draft auto-reply
│                  │  → Flag for escalation/review
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Logger          │  Saves full audit trail:
│  (logger.py)     │  timestamp, classification, actions, ticket
└─────────────────┘
```

## Intent Categories

| Intent | Description | Auto-Action |
|--------|-------------|-------------|
| billing | Charges, payments, refunds, disputes | Flag for billing review |
| technical_support | Network, device, service issues | Create ticket |
| cancellation | Customer wants to leave | Flag for retention team |
| plan_change | Upgrade, downgrade, switch plans | Create ticket |
| general_inquiry | Questions, no action needed | Draft reply |
| complaint | Angry customer, repeated issues, CCTS | Escalate to manager |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Mistral 7B via Ollama (local) |
| Frontend | Streamlit |
| Logging | JSON file-based execution logs |
| Language | Python 3.11 |

## Project Structure

```
project-3-automation-workflow/
├── app.py                     # Streamlit UI (3 modes)
├── config.py                  # Settings and categories
├── requirements.txt           # Dependencies
├── system_logs_analysis.md    # Analysis of batch run results
├── README.md                  # This file
├── workflow/
│   ├── __init__.py
│   ├── classifier.py          # LLM intent classification
│   ├── router.py              # Action routing logic
│   ├── actions.py             # Ticket creation, reply drafting
│   └── logger.py              # JSON execution logging
├── sample_messages/
│   └── test_messages.json     # 22 sample customer messages
└── logs/
    └── workflow_log.json      # Auto-generated execution logs
```

## Setup & Installation

```bash
# Navigate to project
cd ai-portfolio/project-3-automation-workflow

# Activate virtual environment
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running
ollama serve
ollama pull mistral

# Run the app
streamlit run app.py
```

## App Modes

### 1. Single Message
Type a customer name and message, click Process. See the classification, actions taken, generated ticket, and draft reply in real time.

### 2. Batch Process
Process all 22 sample messages at once. View a results summary table with intent, priority, confidence, and actions for every message. See classification stats by intent and priority.

### 3. View Logs
Browse the full execution log. Every processed message is logged with timestamp, classification, actions taken, ticket details, and draft reply. Logs persist across sessions.

## Batch Processing Results

Processed 22 sample messages with the following distribution:

| Intent | Count | Priority | Count |
|--------|-------|----------|-------|
| technical_support | 7 | high | 10 |
| plan_change | 4 | low | 6 |
| billing | 3 | medium | 4 |
| complaint | 3 | urgent | 2 |
| general_inquiry | 3 | | |
| cancellation | 2 | | |

- **Classification confidence:** 80-95% across all messages
- **Failure rate:** 0/22 — all messages classified successfully
- **Processing time:** ~5-8 seconds per message

See `system_logs_analysis.md` for detailed analysis.

## Key Learnings

1. **LLMs as classifiers are surprisingly reliable.** Mistral 7B correctly classified all 22 messages by intent with high confidence, demonstrating that local LLMs can replace traditional ML classifiers for text categorization.

2. **Structured JSON output needs guardrails.** LLMs don't always return clean JSON. The JSON extraction logic (finding `{` and `}` boundaries plus validation) was essential for 100% parse success.

3. **Deterministic routing rules create auditability.** Combining LLM classification (probabilistic) with rule-based routing (deterministic) gives you the best of both — flexible understanding with traceable decisions.

4. **Priority calibration is a real production challenge.** The model over-assigned "high" priority (45.5% of messages). In production, this would need calibration against historical data.

## Known Limitations

- **No feedback loop:** Agents can't correct misclassifications to improve future accuracy
- **Priority over-assignment:** Model tends to classify too many messages as high priority
- **No real integrations:** Tickets and replies are generated but not sent to actual systems
- **Sequential processing:** Batch mode processes messages one at a time
- **No multi-language support:** Only handles English messages

## Possible Improvements

- Integrate with real ticketing APIs (Zendesk, Freshdesk, Jira Service Management)
- Add agent feedback loop to correct and retrain classifications
- Implement priority calibration using historical ticket distributions
- Add sentiment analysis as secondary classification signal
- Support multi-language classification for diverse customer bases
- Add queue management and SLA tracking

## Related Projects

- **[Project 1: Smart Research Assistant](../project-1-ai-agent/)** — LangChain ReAct agent
- **[Project 2: NovaTel Customer Support Assistant](../project-2-rag-system/)** — RAG document Q&A for NovaTel support agents

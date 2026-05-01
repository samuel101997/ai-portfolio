# Project 2: NovaTel Customer Support Assistant (RAG System)

## Overview

An AI-powered document Q&A tool built for telecom customer support agents. Agents upload internal company documents — plans, billing policies, troubleshooting guides — and ask questions in natural language. The system retrieves relevant passages and generates accurate answers with source citations, grounded entirely in the provided documents.

This eliminates the need for agents to manually search through 50+ pages of policy manuals during live customer calls.

## Use Case

**Industry:** Telecommunications  
**User:** Customer support agents at NovaTel Mobile (fictional telecom company)  
**Problem:** Agents waste time searching through multiple documents to answer customer questions about plans, billing, device setup, and escalation procedures  
**Solution:** A RAG system that instantly retrieves the right information and generates cited answers from company documents

### Example Interaction

**Agent asks:** "Customer wants to cancel, what retention offers can I make?"  
**System answers:** "You can offer one retention offer (R1-R5) when a customer states intent to cancel [Source 1]. Options include: 20% discount for 6 months, free plan upgrade for 3 months, $100 bill credit, free device protection for 12 months, or extra 10 GB data permanently [Source 2]. If the customer declines, escalate to the Retention Team [Source 3]."

## Architecture

```
Documents (.txt/.pdf)
    │
    ▼
┌──────────────┐
│   Ingest     │  Load files, split into 500-char chunks
│  (ingest.py) │  with 50-char overlap
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Embed      │  Convert chunks to 384-dim vectors
│(embeddings.py│  using all-MiniLM-L6-v2
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  FAISS Index │  Store vectors for similarity search
│              │  (saved to disk for reuse)
└──────┬───────┘
       │
   User Query
       │
       ▼
┌──────────────┐
│  Retrieve    │  Embed query → find top-3 similar chunks
│(retriever.py)│  with similarity scores
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Generate    │  Send chunks + query to Mistral 7B
│(generator.py)│  with anti-hallucination prompt
└──────┬───────┘
       │
       ▼
   Answer with source citations
```

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| LLM | Mistral 7B via Ollama | Runs locally, no API keys, good instruction following |
| Embeddings | all-MiniLM-L6-v2 | Fast, lightweight (80MB), 384-dim vectors, runs on CPU |
| Vector Store | FAISS | Fast similarity search, saves to disk, no server needed |
| Framework | LangChain | Document loaders, text splitters, vector store integration |
| Frontend | Streamlit | Quick interactive UI with file upload and session state |
| Language | Python 3.11 | Compatible with all dependencies |

## Project Structure

```
project-2-rag-system/
├── app.py                  # Streamlit web interface
├── config.py               # All tunable parameters
├── requirements.txt        # Python dependencies
├── evaluation_rubric.md    # Testing results and parameter tuning
├── README.md               # This file
├── sample_docs/            # NovaTel support documents (5 files)
│   ├── novatel_mobile_plans_guide.txt
│   ├── novatel_troubleshooting_handbook.txt
│   ├── novatel_billing_account_policies.txt
│   ├── novatel_device_compatibility_setup.txt
│   └── novatel_escalation_procedures.txt
└── rag/                    # RAG pipeline modules
    ├── __init__.py
    ├── ingest.py           # Document loading and chunking
    ├── embeddings.py       # Vector embedding and FAISS index
    ├── retriever.py        # Similarity search and context formatting
    └── generator.py        # LLM answer generation with citations
```

## Setup & Installation

### Prerequisites
- Python 3.11
- Ollama installed with Mistral model
- 16 GB RAM recommended
- NVIDIA GPU optional (embedding model runs on CPU)

### Installation

```bash
# Clone the repo
git clone https://github.com/samuel101997/ai-portfolio.git
cd ai-portfolio/project-2-rag-system

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running with Mistral
ollama serve
ollama pull mistral
```

### Run the App

```bash
streamlit run app.py
```

### How to Use
1. Open the app in your browser (default: http://localhost:8501)
2. In the sidebar, check "Use sample documents" or upload your own PDFs/text files
3. Click **Ingest Documents** — wait for the success message
4. Type a question about the documents in the main area
5. View the answer with source citations
6. Expand "View source chunks" to see exactly which passages were retrieved

## Sample Documents

Five realistic NovaTel Mobile internal support documents (~14,000 words total):

| Document | Content | RAG Skill Tested |
|----------|---------|-----------------|
| Plans Guide | 4 postpaid + 3 prepaid plans, pricing, add-ons, discounts | Precise numerical retrieval |
| Troubleshooting Handbook | Step-by-step fixes for 9 issue categories | Sequential procedure retrieval |
| Billing & Account Policies | Payments, fees, refunds, suspensions, credit checks | Conditional policy lookup |
| Device Compatibility & Setup | Network bands, SIM/eSIM, APN settings, financing | Technical detail retrieval |
| Escalation Procedures | 4-tier escalation, SLAs, complaint handling | Multi-condition decision retrieval |

## Evaluation Results

Tested with 10 domain-specific questions + 2 hallucination tests:

| Metric | Score |
|--------|-------|
| Retrieval Relevance | 5.0/5 |
| Answer Accuracy | 4.9/5 |
| Source Citation Rate | 10/10 |
| Hallucination Prevention | 2/2 passed |
| Completeness | 4.9/5 |

See `evaluation_rubric.md` for detailed per-question results and parameter tuning experiments.

### Parameter Tuning

Tested 4 configurations (chunk size, overlap, top-k):

| Config | Avg Accuracy | Finding |
|--------|-------------|---------|
| 500/50/3 (default) | 4.9/5 | Best overall balance |
| 300/50/3 | 4.5/5 | Better for precise lookups, worse for procedures |
| 1000/100/3 | 4.6/5 | Better for procedures, pulled irrelevant detail |
| 500/50/5 | 4.8/5 | Slightly better completeness, added noise |

## Key Learnings

1. **Chunking strategy matters more than model choice.** The same LLM produced significantly different answer quality depending on chunk size. Multi-step procedures (like 7-step troubleshooting) are the hardest to retrieve because they span multiple chunks.

2. **Anti-hallucination prompting works.** Explicitly instructing the model to say "I don't have enough information" and to only use provided context successfully prevented fabricated answers on out-of-scope questions.

3. **Source citation improves trust and debuggability.** Labeling each chunk with `[Source X: filename]` before sending to the LLM made citations natural. This also made it easy to trace errors back to retrieval vs. generation.

4. **Semantic search has blind spots for exact values.** Questions about specific numbers (APN port 8080, price $75) rely on the embedding model capturing numerical meaning, which is weaker than keyword matching. Hybrid search would help.

## Known Limitations

- **Long procedures get truncated:** With top-k=3 and chunk size 500, a 7-step troubleshooting guide only partially appears in the context. Increasing top-k helps but adds noise.
- **Cross-document blending:** When retrieved chunks come from different documents, the LLM occasionally mixes policies (e.g., domestic data rules applied to international roaming).
- **No conversation memory:** Each question is independent — the system doesn't remember previous questions in the same session.
- **Text files only for sample docs:** The sample documents are `.txt` files. PDF extraction quality depends on the PDF structure.
- **Single-user local deployment:** Runs on localhost only. Not production-ready for concurrent users.

## Possible Improvements

- Add hybrid search (keyword + semantic) for better exact-match retrieval
- Implement cross-encoder re-ranking to filter marginally relevant chunks
- Add conversation memory for follow-up questions
- Use adaptive chunk sizes per document type (smaller for tables, larger for procedures)
- Add metadata filtering so agents can scope queries to specific document categories
- Deploy with FastAPI backend for multi-user support

## Related Projects

- **[Project 1: Smart Research Assistant (AI Agent)](../project-1-ai-agent/)** — LangChain ReAct agent with DuckDuckGo search, Wikipedia, and LLM summarization

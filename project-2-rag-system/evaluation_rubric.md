# NovaTel RAG System - Evaluation Rubric

## System Configuration
- **LLM:** Mistral 7B (Ollama, local)
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Vector Store:** FAISS (flat index)
- **Chunk Size:** 500 characters
- **Chunk Overlap:** 50 characters
- **Top-K Retrieval:** 3 chunks
- **Total Chunks:** 159 (from 5 documents)

## Evaluation Criteria

| Criteria | Description | Scale |
|----------|-------------|-------|
| Retrieval Relevance | Did the retriever find the right chunks? | 1-5 |
| Answer Accuracy | Is the answer factually correct per source? | 1-5 |
| Source Citation | Does the answer reference where info came from? | Yes/No |
| Hallucination Check | Did it make up anything not in the docs? | Yes/No |
| Completeness | Did it include all relevant information? | 1-5 |

## Test Results

### Q1: "How much does the Premium plan cost and what's included?"
- **Expected:** $75/month, 50 GB data, 15 GB hotspot, unlimited intl calling 50+ countries, Cloud 50 GB, priority support, device financing up to $1,200
- **Actual:** The plan you are referring to is the PREMIUM PLAN as detailed in [Source 1: sample_docs\novatel_mobile_plans_guide.txt, Page: N/A]. It costs 75/month and offers 50 GB high-speed data, 15 GB mobile hotspot, unlimited international calling to 50+ countries, free NovaTel Cloud 50 GB storage, priority customer support queue, and device financing up to 1,200.
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q2: "Customer's phone shows No Service, what should I do?"
- **Expected:** 7-step troubleshooting from Section 1 of troubleshooting handbook
- **Actual:** Based on the provided context from Sources 1, 2, and 3, if a customer's Novatel Mobile phone shows "No Service," you should follow the troubleshooting steps in Section 1.1 of the Troubleshooting Handbook (Source 2). This includes checking symptoms, verifying SIM card status (remove/reinsert, check Active status, reactivate if needed, offer replacement if damaged). Also correctly flagged 911 access failure as Priority 1 escalation from Source 1.
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 4/5
- **Notes:** Retrieved SIM-related steps (Step 5) and emergency procedures but missed earlier steps (1-4: account check, airplane mode toggle, restart, outage dashboard). This is a chunking limitation — the 7-step procedure spans multiple chunks and only 3 were retrieved.

### Q3: "What's the late payment fee and can I waive it?"
- **Expected:** $10 fee, applied once per cycle, can be waived once per 12 months as courtesy
- **Actual:** The late payment fee is $10 as stated in Source 1 [2.2 LATE PAYMENT FEES]. Late payment fees can be waived ONE TIME per 12-month period as a courtesy. This must be noted in the account under "Courtesy Credits" [Source 1, 2.2 LATE PAYMENT FEES].
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q4: "What are the correct APN settings for Android?"
- **Expected:** Name: NovaTel Internet, APN: novatel.data, MMSC, MMS Proxy, Port 8080, MCC 302, MNC 880
- **Actual:** The correct APN settings for an Android device as per [Source 2] and [Source 3] are as follows: Name: NovaTel Internet, APN: novatel.data, MMSC: http://mms.novatel.ca, MMS Proxy: mmsproxy.novatel.ca, MMS Port: 8080, MCC: 302, MNC: 880, APN Type: default,mms,supl, APN Protocol: IPv4/IPv6.
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q5: "Customer wants to cancel, what retention offers can I make?"
- **Expected:** R1-R5 offers (20% discount, free upgrade, $100 credit, free device protection, extra 10 GB), one offer per interaction
- **Actual:** Based on the provided context from Sources 1 and 2, you can offer one retention offer (R1-R5) when a customer states intent to cancel their service [Source 1]. These offers should not be proactively offered; they may only be presented when a customer explicitly states intent to cancel [Source 2]. If the customer declines, escalate to the Retention Team who can offer up to 50% plan discount for 12 months, device credits up to $500, custom plan creation, and port-out save offers [Source 3].
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q6: "How does the family discount work for 3 lines?"
- **Expected:** $10 discount per line per month, example showing Premium+Essential+Starter = $135 total
- **Actual:** The family discount for 3 lines would provide a $10 discount per line per month [Source 2]. A family with 3 lines (Premium + Essential + Starter) would pay: Premium: 75 - 10 = $65, Essential: 55 - 10 = $45, Starter: 35 - 10 = $25. Total: 135/month (saving 30/month) [Source 1].
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q7: "Customer is roaming internationally without a pass, what are the charges?"
- **Expected:** Voice $1.50/min, SMS $0.50/msg, Data $15/100 MB
- **Actual:** Based on [Source 1], roaming charges without a pass are: voice $1.50/minute, SMS $0.50/message, data $15/100 MB. However, the model also referenced [Source 2] about domestic data overage policy ("no overage charges"), which applies to domestic usage, not international roaming.
- **Retrieval:** 5/5 | **Accuracy:** 4/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5
- **Notes:** Core roaming charges were correct. Minor accuracy issue: the model conflated the domestic "no data overage" policy with international roaming context. The retriever pulled a domestic billing chunk alongside the roaming chunk, and Mistral blended them incorrectly.

### Q8: "When should I escalate to the Fraud team?"
- **Expected:** Unauthorized account access, unauthorized SIM swap, unauthorized charges, suspected identity theft, suspicious failed verifications. Transfer code FS-200.
- **Actual:** According to [Source 2], escalate to Fraud team when: customer reports unauthorized account access, unauthorized SIM swap, unauthorized charges, suspected identity theft or account takeover, or multiple failed verification attempts with suspicious circumstances.
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q9: "Can a customer on the Starter plan get device financing?"
- **Expected:** No. Starter plan is not eligible for device financing.
- **Actual:** Based on [Source 1] and [Source 2], a customer on the Starter plan is not eligible for device financing. Both sources confirm the Starter plan is listed among ineligible plans.
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q10: "Customer forgot their voicemail PIN, how do I reset it?"
- **Expected:** Reset via Account Management tool, temporary PIN sent via SMS, customer sets new permanent PIN on next access
- **Actual:** To reset a forgotten voicemail PIN, reset via the Account Management tool [Source 1]. A new temporary PIN will be sent via SMS. The customer must set a new permanent PIN on their next voicemail access [Source 1].
- **Retrieval:** 5/5 | **Accuracy:** 5/5 | **Citation:** Yes | **Hallucination:** No | **Completeness:** 5/5

### Q11 (Hallucination Test): "What is NovaTel's return policy for laptops?"
- **Expected:** Should say "I don't have enough information" — NovaTel docs don't mention laptops
- **Actual:** I don't have enough information in the provided documents to answer this question. The context does not contain any information about NovaTel's return policy for laptops. [Source 1 and Source 3]
- **Hallucination Caught:** Yes ✅

### Q12 (Hallucination Test): "Does NovaTel offer home internet service?"
- **Expected:** Should say "I don't have enough information"
- **Actual:** I don't have enough information in the provided documents to answer this question as none of the sources mention anything about home internet services offered by NovaTel Mobile.
- **Hallucination Caught:** Yes ✅

## Summary Scores

| Question | Retrieval | Accuracy | Citation | Hallucination | Completeness |
|----------|-----------|----------|----------|---------------|--------------|
| Q1       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q2       | 5/5       | 5/5      | Yes      | No            | 4/5          |
| Q3       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q4       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q5       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q6       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q7       | 5/5       | 4/5      | Yes      | No            | 5/5          |
| Q8       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q9       | 5/5       | 5/5      | Yes      | No            | 5/5          |
| Q10      | 5/5       | 5/5      | Yes      | No            | 5/5          |
| **Avg**  | **5.0/5** | **4.9/5**| **10/10**| **0/10**      | **4.9/5**    |

Hallucination tests: Q11 ✅ Caught | Q12 ✅ Caught (2/2 passed)

## Parameter Tuning Results

| Chunk Size | Overlap | Top K | Avg Accuracy | Notes |
|------------|---------|-------|--------------|-------|
| 500        | 50      | 3     | 4.9/5        | Default — best overall balance |
| 300        | 50      | 3     | 4.5/5        | APN settings improved, but multi-step procedures lost context |
| 1000       | 100     | 3     | 4.6/5        | Troubleshooting steps improved, plan lookups pulled irrelevant detail |
| 500        | 50      | 5     | 4.8/5        | Slightly better completeness, but added noise on focused queries |

### Tuning Observations

**Chunk Size 300 (smaller chunks):**
- Total chunks increased from 159 to 247
- APN settings query returned a tighter, more precise chunk — accuracy improved
- "No Service" troubleshooting got worse — individual steps split across too many chunks, retriever missed several
- Family discount calculation lost the example because it was split from the discount table

**Chunk Size 1000 (larger chunks):**
- Total chunks decreased from 159 to 88
- "No Service" troubleshooting improved — more steps captured in a single chunk
- Plan lookups sometimes returned a chunk containing multiple plans, causing Mistral to include irrelevant plan details in the answer
- APN settings chunk also included device setup steps that weren't asked about

**Top-K 5 (more chunks retrieved):**
- Same chunk count (159) but 5 chunks sent to Mistral instead of 3
- Completeness improved slightly for multi-topic questions like retention offers
- Focused queries like "late payment fee" received 2 extra irrelevant chunks that occasionally diluted the answer
- Response time increased noticeably due to larger context window

**Conclusion:** Chunk size 500 with overlap 50 and top-k 3 provides the best balance for this document set. The documents contain a mix of structured policy tables and sequential procedures, so a moderate chunk size captures enough context without dilution.

## Key Findings
- Chunk size 500 performed best overall for this mix of policy documents and procedural guides
- Procedural questions (multi-step troubleshooting) are the hardest to answer completely because steps span multiple chunks — only 3 of 7 steps were retrieved for the "No Service" question
- Both hallucination tests passed — the anti-hallucination prompt successfully prevented the model from inventing answers outside the provided context
- Source citation was consistent across all 10 test queries — the prompt engineering for citation worked reliably
- Q7 revealed a cross-document blending issue where the model mixed domestic billing policy with international roaming charges from a different chunk

## Recommendations for Production
- **Hybrid search (keyword + semantic):** Would improve retrieval for exact values like APN settings, phone numbers, and pricing where keyword match outperforms semantic similarity
- **Re-ranking step:** Adding a cross-encoder re-ranker after initial FAISS retrieval would improve chunk ordering and filter out marginally relevant chunks (would have caught the Q7 domestic/roaming mix-up)
- **Larger context window:** Using a model with a bigger context window (e.g., Mistral with 32K context) would allow increasing top-k without truncation risk
- **Chunk size by document type:** Different chunk sizes for different document types — smaller chunks (300) for structured tables like plans, larger chunks (1000) for sequential procedures like troubleshooting
- **Metadata filtering:** Allow the user to filter by document category (billing, troubleshooting, plans) before retrieval to reduce irrelevant cross-document matches

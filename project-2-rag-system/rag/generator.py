# rag/generator.py - Answer generation using retrieved context + Ollama
# Sends retrieved chunks + user question to Mistral for answer generation

import ollama
from config import OLLAMA_MODEL


SYSTEM_PROMPT = """You are a document Q&A assistant for NovaTel Mobile customer support. Your job is to answer questions based ONLY on the provided context passages.

Rules:
1. Only use information from the provided context to answer.
2. Cite your sources by referencing [Source X] when using information from that source.
3. If the context does not contain enough information to answer the question,
   say "I don't have enough information in the provided documents to answer this question."
4. Do not make up or infer information that is not explicitly stated in the context.
5. Keep answers clear and concise.
"""


def generate_answer(query, context):
    """Generate an answer using the retrieved context and user query."""
    user_prompt = f"""Context passages:

{context}

---

Question: {query}

Answer based only on the context above, citing sources:"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]


# Quick test
if __name__ == "__main__":
    from rag.retriever import retrieve, format_context

    query = "What is the late payment fee and can it be waived?"
    results = retrieve(query)
    context = format_context(results)

    print(f"Query: {query}\n")
    print("Generating answer...\n")
    answer = generate_answer(query, context)
    print(f"Answer:\n{answer}")
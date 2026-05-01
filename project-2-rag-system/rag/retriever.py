# rag/retriever.py - Document retrieval via similarity search
# Finds the most relevant chunks for a user's question

from config import TOP_K
from rag.embeddings import load_vector_store


def retrieve(query, vector_store=None, top_k=TOP_K):
    """Find the top-k most relevant chunks for a query."""
    if vector_store is None:
        vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(query, k=top_k)
    return results


def format_context(results):
    """Format retrieved chunks into a context string for the LLM."""
    context_parts = []

    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        context_parts.append(
            f"[Source {i+1}: {source}, Page: {page}]\n{doc.page_content}"
        )

    return "\n\n---\n\n".join(context_parts)


# Quick test
if __name__ == "__main__":
    query = "What is the late payment fee?"
    results = retrieve(query)

    print(f"Query: {query}")
    print(f"Retrieved {len(results)} chunks:\n")

    for doc, score in results:
        print(f"Score: {score:.4f}")
        print(f"Source: {doc.metadata}")
        print(f"Content: {doc.page_content[:150]}")
        print("---")
# rag/embeddings.py - Vector embedding and FAISS index management
# Converts text chunks to vectors and stores them for similarity search

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH


def get_embedding_model():
    """Initialize the embedding model (runs locally)."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_vector_store(chunks):
    """Embed chunks and create a FAISS index, then save to disk."""
    embeddings = get_embedding_model()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    return vector_store


def load_vector_store():
    """Load an existing FAISS index from disk."""
    embeddings = get_embedding_model()
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store


# Quick test
if __name__ == "__main__":
    from rag.ingest import ingest

    chunks = ingest()
    print(f"Embedding {len(chunks)} chunks...")

    vector_store = create_vector_store(chunks)
    print(f"Vector store created and saved to '{FAISS_INDEX_PATH}/'")

    loaded_store = load_vector_store()
    results = loaded_store.similarity_search("What is the Premium plan?", k=2)
    print(f"\nTest query returned {len(results)} results:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content[:150])
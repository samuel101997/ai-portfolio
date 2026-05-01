# app.py - Streamlit interface for the Document Q&A Assistant
# Upload documents, ask questions, get answers with source citations

import os
import streamlit as st
from rag.ingest import ingest
from rag.embeddings import create_vector_store, get_embedding_model
from rag.retriever import retrieve, format_context
from rag.generator import generate_answer
from config import SAMPLE_DOCS_PATH

st.set_page_config(page_title="NovaTel Support Assistant", page_icon="📱")
st.title("📱 NovaTel Customer Support Assistant")
st.caption("Ask questions about NovaTel plans, billing, troubleshooting, and policies.")

# --- Sidebar: Document Upload & Ingestion ---
with st.sidebar:
    st.header("📁 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or text files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    use_sample = st.checkbox("Use sample documents", value=True)

    if st.button("🔄 Ingest Documents", type="primary"):
        with st.spinner("Loading and chunking documents..."):
            if uploaded_files:
                upload_dir = "uploaded_docs"
                os.makedirs(upload_dir, exist_ok=True)
                for file in uploaded_files:
                    with open(os.path.join(upload_dir, file.name), "wb") as f:
                        f.write(file.getbuffer())
                chunks = ingest(upload_dir)
            elif use_sample:
                chunks = ingest(SAMPLE_DOCS_PATH)
            else:
                st.warning("Please upload files or check 'Use sample documents'.")
                st.stop()

            st.info(f"Split into {len(chunks)} chunks. Embedding...")

        with st.spinner("Creating vector embeddings..."):
            vector_store = create_vector_store(chunks)
            st.session_state["vector_store"] = vector_store
            st.session_state["ingested"] = True

        st.success(f"✅ Ingested {len(chunks)} chunks. Ready to answer questions!")

    if st.session_state.get("ingested"):
        st.info("✅ Documents loaded. Ask a question!")
    else:
        st.warning("⬆️ Ingest documents first.")

# --- Main Area: Question & Answer ---
if st.session_state.get("ingested"):
    query = st.text_input("Ask a question about NovaTel:")

    if query:
        with st.spinner("Searching and generating answer..."):
            vector_store = st.session_state["vector_store"]
            results = retrieve(query, vector_store=vector_store)
            context = format_context(results)
            answer = generate_answer(query, context)

        st.markdown("### Answer")
        st.write(answer)

        with st.expander("📚 View source chunks"):
            for i, (doc, score) in enumerate(results):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                st.markdown(f"**Source {i+1}:** {source} | Page: {page} | Score: {score:.4f}")
                st.text(doc.page_content)
                st.divider()
else:
    st.info("👈 Upload and ingest documents using the sidebar to get started.")
# rag/ingest.py - Document loading and chunking
# Reads PDFs and text files, splits them into chunks for embedding

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP, SAMPLE_DOCS_PATH


def load_documents(folder_path=SAMPLE_DOCS_PATH):
    """Load all PDF and text files from a folder."""
    documents = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())

        elif filename.lower().endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())

    return documents


def chunk_documents(documents):
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    return chunks


def ingest(folder_path=SAMPLE_DOCS_PATH):
    """Full ingestion pipeline: load files then chunk them."""
    documents = load_documents(folder_path)
    chunks = chunk_documents(documents)
    return chunks


# Quick test when running this file directly
if __name__ == "__main__":
    chunks = ingest()
    print(f"Loaded {len(chunks)} chunks")
    print(f"\n--- Sample chunk ---")
    print(f"Content: {chunks[0].page_content[:200]}")
    print(f"Metadata: {chunks[0].metadata}")
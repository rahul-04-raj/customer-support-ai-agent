"""
RAG (Retrieval-Augmented Generation) Pipeline
Uses FAISS (Facebook AI Similarity Search) as the vector database
and Sentence Transformers for local, free text embeddings.
"""

import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Configuration paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# In-memory FAISS index and related data
_index = None
_chunks: list[str] = []
_embedding_model = None


def _get_embedding_model():
    """Load the sentence-transformer embedding model (free, local, no API key)."""
    global _embedding_model
    if _embedding_model is None:
        print("[RAG] Loading embedding model (first run may take a minute)...")
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def _load_and_chunk_dir(directory: str) -> list[str]:
    """Load all .txt and .md files in a directory and split into chunks."""
    all_chunks = []
    
    if not os.path.exists(directory):
        return all_chunks

    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".md"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split by ## headings for clean, meaningful chunks
            sections = text.split("\n## ")
            for i, section in enumerate(sections):
                section = section.strip()
                if not section:
                    continue
                # Re-add the heading marker for all sections except the first
                if i > 0:
                    section = "## " + section
                # Tag the chunk with its source filename
                all_chunks.append(f"[Source: {filename}]\n{section}")
                
    return all_chunks


def init_knowledge_base():
    """Load documents, embed them, and build the FAISS vector index."""
    global _index, _chunks

    if _index is not None:
        return  # Already initialized

    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Knowledge base directory not found at {DATA_DIR}")

    print(f"[RAG] Loading knowledge base from {DATA_DIR}...")
    _chunks = _load_and_chunk_dir(DATA_DIR)
    print(f"[RAG] Split into {len(_chunks)} chunks.")

    # Generate embeddings for all chunks
    model = _get_embedding_model()
    embeddings = model.encode(_chunks, convert_to_numpy=True)
    embeddings = np.array(embeddings, dtype="float32")

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build the FAISS index (Inner Product = Cosine Similarity after normalization)
    dimension = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dimension)
    _index.add(embeddings)

    print(f"[RAG] FAISS index built with {_index.ntotal} vectors (dim={dimension}).")


def retrieve(query: str, top_k: int = 2) -> str:
    """Retrieve the top-k most relevant chunks for a given query using FAISS."""
    init_knowledge_base()

    # Embed the query
    model = _get_embedding_model()
    query_embedding = model.encode([query], convert_to_numpy=True)
    query_embedding = np.array(query_embedding, dtype="float32")
    faiss.normalize_L2(query_embedding)

    # Search the FAISS index
    scores, indices = _index.search(query_embedding, top_k)

    # Collect matched chunks
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(_chunks):
            results.append(f"[Relevance: {scores[0][i]:.3f}]\n{_chunks[idx]}")

    return "\n\n---\n\n".join(results)


if __name__ == "__main__":
    init_knowledge_base()
    # Quick test
    test_queries = [
        "What is the return policy?",
        "My device won't turn on",
        "How long does shipping take?",
    ]
    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print(f"{'='*60}")
        print(retrieve(q))

"""
Milestone 4: Embed chunks into ChromaDB and expose a retrieval function.

Usage:
  python embed.py           # load all chunks, then run 3 test queries
  python embed.py --load    # load only (skip test queries)
  python embed.py --query "your question here"
"""

import argparse
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path(__file__).parent / "chunks.json"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "uci-housing"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return client.get_or_create_collection(COLLECTION_NAME)


def load_chunks():
    with open(CHUNKS_FILE) as f:
        return json.load(f)


def embed_and_store(reset: bool = True):
    chunks = load_chunks()
    model = SentenceTransformer(MODEL_NAME)
    collection = get_collection(reset=reset)

    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    # ChromaDB metadata values must be scalar — flatten any non-scalar fields
    metadatas = [
        {k: v for k, v in c["metadata"].items() if isinstance(v, (str, int, float, bool))}
        for c in chunks
    ]

    print(f"Embedding {len(texts)} chunks with {MODEL_NAME}...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    print("Inserting into ChromaDB...")
    collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    count = collection.count()
    print(f"ChromaDB collection '{COLLECTION_NAME}' now contains {count} items.")
    return model, collection


def retrieve(query: str, k: int = 5, model=None, collection=None):
    if model is None:
        model = SentenceTransformer(MODEL_NAME)
    if collection is None:
        collection = get_collection()

    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    hits = []
    for i in range(len(results["documents"][0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return hits


def print_results(query: str, hits: list):
    print(f"\n{'='*70}")
    print(f"QUERY: {query}")
    print(f"{'='*70}")
    for rank, hit in enumerate(hits, 1):
        meta = hit["metadata"]
        print(f"\n--- Rank {rank} | distance={hit['distance']:.4f} ---")
        print(f"Source: {meta.get('description', 'N/A')}")
        print(f"URL:    {meta.get('source_url', 'N/A')}")
        print(f"Chunk:  #{meta.get('chunk_index', '?')} of doc {meta.get('doc_id', '?')}")
        print(f"\n{hit['text'][:400]}{'...' if len(hit['text']) > 400 else ''}")


TEST_QUERIES = [
    "What do students say about the flooring in Plaza Verde?",
    "Is Middle Earth better than Mesa Court for STEM students?",
    "Does Vista del Campo cover utilities in rent?",
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", action="store_true", help="Load chunks only, skip test queries")
    parser.add_argument("--query", type=str, help="Run a single retrieval query")
    args = parser.parse_args()

    model, collection = embed_and_store(reset=True)

    if args.load:
        pass
    elif args.query:
        hits = retrieve(args.query, model=model, collection=collection)
        print_results(args.query, hits)
    else:
        for q in TEST_QUERIES:
            hits = retrieve(q, model=model, collection=collection)
            print_results(q, hits)

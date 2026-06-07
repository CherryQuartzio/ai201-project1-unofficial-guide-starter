"""
summarize_chunks.py — Quick Milestone 3 verification (no langchain import).
Reads chunks.json (if it exists) or re-chunks documents/ on the fly using
the same settings as ingest.py, then prints the summary and 5 samples.
Run: python3 summarize_chunks.py   (uses system python3, no venv needed)
"""
import json
import os
import re
import sys

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")
CHUNKS_JSON = os.path.join(os.path.dirname(__file__), "chunks.json")

# Per-doc chunk sizes matching ingest.py
CHUNK_CONFIGS = {
    "01_first_year_housing_scoop":         (1000, 150),
    "02_honest_opinions_plaza_verde":      (800,  100),
    "03_acc_vdc_plaza_experiences":        (800,  100),
    "04_are_acc_apartments_bad":           (1000, 0),
    "05_middle_earth_or_mesa_court_recent":(1000, 150),
    "06_mesa_court_vs_middle_earth_psych": (1000, 150),
    "07_any_opinions_acc_housing":         (1200, 0),
    "08_middle_earth_or_mesa_court_classic":(600, 100),
    "09_transfer_looking_at_housing":      (800,  100),
    "10_how_do_i_choose_housing":          (1000, 150),
}


def simple_chunk(text, chunk_size, overlap):
    """Basic sliding-window chunker (no external deps)."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end >= len(text):
            break
        start = end - overlap
    return [c for c in chunks if c]


def main():
    # Try loading chunks.json first
    if os.path.exists(CHUNKS_JSON):
        print(f"Loading from {CHUNKS_JSON} ...")
        with open(CHUNKS_JSON, encoding="utf-8") as f:
            all_chunks = json.load(f)
        print(f"  Loaded {len(all_chunks)} chunks from JSON.")
    else:
        print(f"chunks.json not found — building from documents/ ...")
        all_chunks = []
        for fname in sorted(os.listdir(DOCUMENTS_DIR)):
            if not fname.endswith(".txt") or fname == ".gitkeep":
                continue
            slug = fname.replace(".txt", "")
            cfg_key = slug if slug in CHUNK_CONFIGS else None
            chunk_size, overlap = CHUNK_CONFIGS.get(cfg_key, (1000, 150))
            path = os.path.join(DOCUMENTS_DIR, fname)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            chunks = simple_chunk(text, chunk_size, overlap)
            for i, c in enumerate(chunks):
                all_chunks.append({"text": c, "metadata": {
                    "slug": slug, "chunk_index": i,
                    "chunk_size_used": chunk_size, "overlap_used": overlap,
                }})
            print(f"  {fname}: {len(chunks)} chunks")

    total = len(all_chunks)
    avg_len = int(sum(len(c["text"]) for c in all_chunks) / total) if total else 0
    min_len = min(len(c["text"]) for c in all_chunks) if total else 0
    max_len = max(len(c["text"]) for c in all_chunks) if total else 0

    print("\n" + "=" * 60)
    print("MILESTONE 3 — PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Total chunks     : {total}")
    print(f"  Avg chunk length : {avg_len} chars")
    print(f"  Min chunk length : {min_len} chars")
    print(f"  Max chunk length : {max_len} chars")

    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS (5 evenly spaced)")
    print("=" * 60)
    indices = [int(total * i / 5) for i in range(5)]
    for i, idx in enumerate(indices, 1):
        c = all_chunks[idx]
        m = c["metadata"]
        print(f"\n--- Sample {i} | {m['slug']} | chunk {m['chunk_index']} ---")
        print(c["text"][:600])
        if len(c["text"]) > 600:
            print(f"  ... ({len(c['text'])} chars total)")
        print()


if __name__ == "__main__":
    main()

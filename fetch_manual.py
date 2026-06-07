"""
fetch_manual.py — Helper to show which fallback .txt files are needed.
Run this to see which files are missing from documents/.
"""
import os
from ingest import DOCUMENTS, DOCUMENTS_DIR

missing = []
for doc in DOCUMENTS:
    fname = f"{doc['id']:02d}_{doc['slug']}_raw.txt"
    fpath = os.path.join(DOCUMENTS_DIR, fname)
    exists = os.path.exists(fpath)
    status = "✓ exists" if exists else "✗ MISSING"
    print(f"  [{doc['id']:02d}] {status}  →  documents/{fname}")
    if not exists:
        missing.append((doc, fpath))

print(f"\n{len(missing)} files missing.\n")
for doc, _ in missing:
    print(f"  URL:  {doc['url']}")
    print(f"  Save: documents/{doc['id']:02d}_{doc['slug']}_raw.txt\n")

"""
ingest.py — Milestone 3: Document Ingestion and Chunking Pipeline
==================================================================
Parses saved Reddit HTML files from the html/ directory, extracts
the post title, body text, and comment text, cleans them, and splits
each document into chunks using per-document RecursiveCharacterTextSplitter
settings specified in planning.md.

Usage:
    python ingest.py

Output:
    - documents/<slug>.txt          (cleaned raw text per document)
    - Prints 5 representative sample chunks to the console
    - Prints total chunk count across all documents
"""

import html as html_module
import json
import os
import random
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Document configuration
# Maps HTML filenames (without .html) to metadata + chunking params.
# Per-document chunk sizes and overlaps from planning.md (§Chunking Strategy).
# ---------------------------------------------------------------------------
DOCUMENTS = [
    {
        "id": 1,
        "slug": "first_year_housing_scoop",
        "html_name": "first year housing scoop _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/",
        "chunk_size": 1000,
        "overlap": 150,
        "description": "Mesa Court vs Middle Earth detailed breakdown",
    },
    {
        "id": 2,
        "slug": "honest_opinions_plaza_verde",
        "html_name": "Honest opinions about living in plaza verde_ (especially if you live on the first floor) _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/x4b6hb/honest_opinions_about_living_in_plaza_verde/",
        "chunk_size": 800,
        "overlap": 100,
        "description": "Honest opinions about living in Plaza Verde",
    },
    {
        "id": 3,
        "slug": "acc_vdc_plaza_experiences",
        "html_name": "ACC question - comment your experiences in VDC_Plaza! _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/10js4cg/acc_question_comment_your_experiences_in_vdcplaza/",
        "chunk_size": 800,
        "overlap": 100,
        "description": "ACC question — VDC vs Plaza Verde experiences",
    },
    {
        "id": 4,
        "slug": "are_acc_apartments_bad",
        "html_name": "Are the Acc apartments really that bad_ _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/",
        "chunk_size": 1000,
        "overlap": 0,
        "description": "Are the ACC apartments really that bad?",
    },
    {
        "id": 5,
        "slug": "middle_earth_or_mesa_court_recent",
        "html_name": "Middle Earth or Mesa Court _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/1ss7sgp/middle_earth_or_mesa_court/",
        "chunk_size": 1000,
        "overlap": 150,
        "description": "Middle Earth or Mesa Court (recent)",
    },
    {
        "id": 6,
        "slug": "mesa_court_vs_middle_earth_psych",
        "html_name": "Mesa Court vs Middle Earth _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/1sdqj6j/mesa_court_vs_middle_earth/",
        "chunk_size": 1000,
        "overlap": 150,
        "description": "Mesa Court vs Middle Earth (psychology major perspective)",
    },
    {
        "id": 7,
        "slug": "any_opinions_acc_housing",
        "html_name": "Any opinions on ACC housing_ _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/mo4ice/any_opinions_on_acc_housing/",
        "chunk_size": 1200,
        "overlap": 0,
        "description": "Any opinions on ACC housing?",
    },
    {
        "id": 8,
        "slug": "middle_earth_or_mesa_court_classic",
        "html_name": "Middle Earth or Mesa Court____ _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/31e68h/middle_earth_or_mesa_court/",
        "chunk_size": 600,
        "overlap": 100,
        "description": "Middle Earth or Mesa Court (classic debate)",
    },
    {
        "id": 9,
        "slug": "transfer_looking_at_housing",
        "html_name": "25+ Transfer looking at housing _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/1t04ih1/25_transfer_looking_at_housing/",
        "chunk_size": 800,
        "overlap": 100,
        "description": "25+ Transfer student housing perspectives",
    },
    {
        "id": 10,
        "slug": "how_do_i_choose_housing",
        "html_name": "how do i choose housing options _ r_UCI",
        "url": "https://www.reddit.com/r/UCI/comments/1rz6gkj/how_do_i_choose_housing_options/",
        "chunk_size": 1000,
        "overlap": 150,
        "description": "How do I choose housing options?",
    },
]

HTML_DIR = os.path.join(os.path.dirname(__file__), "html")
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")


# ---------------------------------------------------------------------------
# HTML Parsing helpers (regex-based for speed)
# ---------------------------------------------------------------------------

def preprocess_html(raw_html: str) -> str:
    """
    Strip all <style> and <script> blocks from raw HTML before extraction.
    This removes darkreader injections, SML.load() calls, and other
    browser-extension or inline JS/CSS that pollutes the output.
    """
    # Remove <style ...>...</style> (incl. darkreader blocks)
    html = re.sub(r'<style[^>]*>.*?</style>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Remove <script ...>...</script>
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    return html

def _strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "\n• ", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text)
    return text


def extract_post_title(raw_html: str) -> str:
    """Extract the post title from <h1 ... slot='title'>."""
    m = re.search(
        r'<h1[^>]*slot="title"[^>]*>(.*?)</h1>',
        raw_html,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        return _strip_tags(m.group(1)).strip()
    return ""


def extract_post_body(raw_html: str) -> str:
    """Extract the post body from the rtjson-content div."""
    m = re.search(
        r'<div[^>]*id="[^"]*-post-rtjson-content"[^>]*>(.*?)</div>\s*</div>\s*</div>',
        raw_html,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        return _strip_tags(m.group(1)).strip()
    return ""


def extract_comments(raw_html: str) -> list[str]:
    """
    Extract comment bodies. Comments live inside
    <shreddit-comment ...> tags, and the text is in
    <div class="md ..."> blocks inside them.
    We look for all md-class divs that follow shreddit-comment tags.
    """
    comments = []
    # Find all comment body blocks — they are <div ... class="md ..." ...>
    # nested inside shreddit-comment elements. We use a heuristic:
    # look for <div id="t1_...-comment-rtjson-content" ...> blocks.
    pattern = re.compile(
        r'<div[^>]*id="t1_[^"]*-comment-rtjson-content"[^>]*>(.*?)</div>\s*</div>\s*</div>',
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern.finditer(raw_html):
        body = _strip_tags(m.group(1)).strip()
        if body and body not in ("[deleted]", "[removed]"):
            comments.append(body)
    return comments


def extract_source_url(raw_html: str) -> str:
    """Try to extract the canonical URL from the HTML."""
    m = re.search(
        r'<div[^>]*id="canonical-url-updater"[^>]*value="([^"]+)"',
        raw_html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1)
    return ""


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing Reddit HTML/JS/CSS boilerplate
    that leaks through the regex parser, then normalizing whitespace.
    """
    # --- Remove JavaScript artifacts ---
    # SML.load(...) calls
    text = re.sub(r"SML\.load\(\[.*?\]\s*,\s*'[^']*'\s*,\s*'[^']*'\);", "", text, flags=re.DOTALL)
    # window.POST_ID and other inline JS
    text = re.sub(r"window\.POST_ID\s*=\s*'[^']*';", "", text)
    # Large JS blocks (minified code with function definitions)
    text = re.sub(r"new Set\(Object\.values\(\{.*?\}\)\).*?export\{.*?\};", "", text, flags=re.DOTALL)
    # Any remaining SML references
    text = re.sub(r"SML\.\w+\([^)]*\);?", "", text)

    # --- Remove CSS artifacts ---
    # darkreader and other CSS filter rules
    text = re.sub(
        r"\.jfk-bubble\.gtx-bubble.*?!important;\s*\}",
        "", text, flags=re.DOTALL,
    )
    text = re.sub(r"filter:\s*invert\([^)]*\)[^}]*}", "", text, flags=re.DOTALL)

    # --- Remove Reddit UI boilerplate ---
    # "Read more", "More replies", "N more replies"
    text = re.sub(r"^\s*Read more\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*More replies\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+ more repl(?:y|ies)\s*$", "", text, flags=re.MULTILINE)
    # "Share" button text
    text = re.sub(r"^\s*Share\s*$", "", text, flags=re.MULTILINE)
    # Promoted / ad sections
    text = re.sub(r"Promoted.*?(?=\[comment\]|\Z)", "", text, flags=re.DOTALL)
    # "New to Reddit?" signup prompts
    text = re.sub(r"New to Reddit\?.*?Privacy Policy\.", "", text, flags=re.DOTALL)
    # "People also ask" sections
    text = re.sub(r"People also ask about.*?(?=\[comment\]|\Z)", "", text, flags=re.DOTALL)
    # Sidebar subreddit recommendations
    text = re.sub(r"r/\w+\s*•\s*\d+d? ago", "", text)

    # --- Remove general artifacts ---
    # Convert markdown links to plain text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove bare URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove zero-width spaces and nbsp
    text = text.replace("\u200b", "").replace("\xa0", " ")

    # --- Remove lines that are just noise ---
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        # Skip lines that are just a bullet/dot with nothing else
        if stripped in ("•", "·", ""):
            continue
        # Skip lines with only Reddit UI text
        if stripped in (
            "Report", "About this ad", "Tired of ads?",
            "Learn More", "Shop Now", "Continue with Email",
            "Continue with Phone Number", "Join the conversation",
            "People also ask about section", "People also ask about",
        ):
            continue
        # Skip lines that are residual JS/CSS fragments
        if stripped.startswith("SML.") or stripped.startswith("filter:"):
            continue
        # Skip residual short code-like fragments
        if re.match(r'^[\[\]"\d,|]+$', stripped):
            continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Collapse excessive blank lines (keep at most 2 newlines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing spaces on each line
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_document(
    text: str,
    chunk_size: int,
    overlap: int,
    doc_meta: dict,
) -> list[dict]:
    """
    Split `text` into chunks using RecursiveCharacterTextSplitter.
    Returns a list of chunk dicts with `text` and `metadata`.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )
    raw_chunks = splitter.split_text(text)
    chunks = []
    for i, chunk_text in enumerate(raw_chunks):
        chunks.append(
            {
                "text": chunk_text,
                "metadata": {
                    "doc_id": doc_meta["id"],
                    "slug": doc_meta["slug"],
                    "source_url": doc_meta["url"],
                    "description": doc_meta["description"],
                    "chunk_index": i,
                    "chunk_size_used": chunk_size,
                    "overlap_used": overlap,
                },
            }
        )
    return chunks


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main() -> list[dict]:
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    all_chunks: list[dict] = []
    failed_docs: list[dict] = []

    print("=" * 60)
    print("Milestone 3 — Document Ingestion & Chunking Pipeline")
    print("=" * 60)

    for doc in DOCUMENTS:
        print(f"\n[{doc['id']:02d}/{len(DOCUMENTS)}] {doc['description']}")
        print(f"       chunk_size={doc['chunk_size']}  overlap={doc['overlap']}")

        # --- Step 1: Locate and read the HTML file --------------------------
        html_path = os.path.join(HTML_DIR, doc["html_name"] + ".html")
        if not os.path.exists(html_path):
            print(f"  ✗  HTML file not found: {html_path}")
            failed_docs.append(doc)
            continue

        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            raw_html = f.read()
        print(f"  ✓  Loaded HTML ({len(raw_html):,} chars)")

        # --- Step 2: Pre-process HTML (strip style/script blocks) ----------
        clean_html = preprocess_html(raw_html)

        # --- Step 3: Extract title, body, comments -------------------------
        title = extract_post_title(clean_html)
        body = extract_post_body(clean_html)
        comments = extract_comments(clean_html)
        source_url = extract_source_url(clean_html) or doc["url"]

        print(f"  ✓  Title: {title[:80]}")
        print(f"  ✓  Body: {len(body):,} chars")
        print(f"  ✓  Comments: {len(comments)} extracted")

        if not body and not comments:
            print(f"  ⚠  No content extracted! Skipping.")
            failed_docs.append(doc)
            continue

        # --- Step 3: Assemble the document text ----------------------------
        parts = [
            f"Source: r/UCI | {doc['description']}",
            f"URL: {source_url}",
            f"Title: {title}",
            "",
        ]
        if body:
            parts.append(body)
            parts.append("")
        if comments:
            parts.append("--- COMMENTS ---")
            for c in comments:
                parts.append(f"\n[comment]\n{c}")

        raw_text = "\n".join(parts)

        # --- Step 4: Clean -------------------------------------------------
        cleaned = clean_text(raw_text)

        # --- Step 5: Save cleaned text to documents/ -----------------------
        out_fname = f"{doc['id']:02d}_{doc['slug']}.txt"
        out_path = os.path.join(DOCUMENTS_DIR, out_fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"  ✓  Saved cleaned text → {out_fname}  ({len(cleaned):,} chars)")

        # --- Step 6: Chunk -------------------------------------------------
        doc_chunks = chunk_document(cleaned, doc["chunk_size"], doc["overlap"], doc)
        all_chunks.extend(doc_chunks)
        print(f"  ✓  {len(doc_chunks)} chunks produced")

    # -------------------------------------------------------------------------
    # Save chunks to JSON for Milestone 4 (embedding + ChromaDB)
    # -------------------------------------------------------------------------
    chunks_path = os.path.join(os.path.dirname(__file__), "chunks.json")
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"\n  ✓  Chunks saved → chunks.json")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    avg_len = (
        int(sum(len(c["text"]) for c in all_chunks) / len(all_chunks))
        if all_chunks else 0
    )
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Documents processed : {len(DOCUMENTS) - len(failed_docs)} / {len(DOCUMENTS)}")
    if failed_docs:
        print(f"  Failed docs         : {[d['slug'] for d in failed_docs]}")
    print(f"  Total chunks        : {len(all_chunks)}")
    print(f"  Avg chunk length    : {avg_len} chars")
    print(f"  Chunks file         : chunks.json")

    # -------------------------------------------------------------------------
    # Print 5 representative sample chunks (Milestone 3 requirement)
    # -------------------------------------------------------------------------
    if all_chunks:
        print("\n" + "=" * 60)
        print("SAMPLE CHUNKS (5 representative)")
        print("=" * 60)
        # Pick one chunk evenly spaced across the full list for variety
        n = len(all_chunks)
        indices = [int(n * i / 5) for i in range(5)]
        for i, idx in enumerate(indices, 1):
            chunk = all_chunks[idx]
            m = chunk["metadata"]
            print(f"\n--- Sample {i} | doc={m['doc_id']} slug={m['slug']} | chunk {m['chunk_index']} ---")
            print(chunk["text"][:600])
            if len(chunk["text"]) > 600:
                print(f"  ... ({len(chunk['text'])} chars total)")
            print()

    return all_chunks


if __name__ == "__main__":
    chunks = main()

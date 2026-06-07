"""
fetch_reddit_local.py
=====================
Run this script from your LOCAL MACHINE (outside WSL) where you have
normal internet access and a browser. It uses the Reddit JSON API to
fetch all 10 threads and saves them as _raw.txt files in a folder called
'reddit_raw/'.

After running it, copy the contents of 'reddit_raw/' into the
'documents/' folder inside your WSL project directory.

Usage (from local machine):
    pip install requests
    python fetch_reddit_local.py

Then copy:
    scp reddit_raw/*.txt  <your-wsl-path>/documents/
  OR just drag them in via File Explorer.
"""

import json
import os
import time

import requests

DOCUMENTS = [
    {"id": 1, "slug": "first_year_housing_scoop",          "url": "https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/"},
    {"id": 2, "slug": "honest_opinions_plaza_verde",        "url": "https://www.reddit.com/r/UCI/comments/x4b6hb/honest_opinions_about_living_in_plaza_verde/"},
    {"id": 3, "slug": "acc_vdc_plaza_experiences",          "url": "https://www.reddit.com/r/UCI/comments/10js4cg/acc_question_comment_your_experiences_in_vdcplaza/"},
    {"id": 4, "slug": "are_acc_apartments_bad",             "url": "https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/"},
    {"id": 5, "slug": "middle_earth_or_mesa_court_recent",  "url": "https://www.reddit.com/r/UCI/comments/1ss7sgp/middle_earth_or_mesa_court/"},
    {"id": 6, "slug": "mesa_court_vs_middle_earth_psych",   "url": "https://www.reddit.com/r/UCI/comments/1sdqj6j/mesa_court_vs_middle_earth/"},
    {"id": 7, "slug": "any_opinions_acc_housing",           "url": "https://www.reddit.com/r/UCI/comments/mo4ice/any_opinions_on_acc_housing/"},
    {"id": 8, "slug": "middle_earth_or_mesa_court_classic", "url": "https://www.reddit.com/r/UCI/comments/31e68h/middle_earth_or_mesa_court/"},
    {"id": 9, "slug": "transfer_looking_at_housing",        "url": "https://www.reddit.com/r/UCI/comments/1t04ih1/25_transfer_looking_at_housing/"},
    {"id": 10, "slug": "how_do_i_choose_housing",           "url": "https://www.reddit.com/r/UCI/comments/1rz6gkj/how_do_i_choose_housing_options/"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UCI-Unofficial-Guide/1.0; academic-project)"
}

OUT_DIR = "reddit_raw"
os.makedirs(OUT_DIR, exist_ok=True)


def extract_comments(comment_list, depth=0):
    texts = []
    for item in comment_list:
        if not isinstance(item, dict):
            continue
        data = item.get("data", {})
        body = data.get("body", "").strip()
        if body and body not in ("[deleted]", "[removed]"):
            texts.append(body)
        replies = data.get("replies", "")
        if isinstance(replies, dict):
            children = replies.get("data", {}).get("children", [])
            texts.extend(extract_comments(children, depth + 1))
    return texts


for doc in DOCUMENTS:
    print(f"Fetching [{doc['id']:02d}] {doc['slug']}…")
    json_url = doc["url"].rstrip("/") + ".json?limit=500"
    try:
        r = requests.get(json_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()

        post_data = data[0]["data"]["children"][0]["data"]
        title    = post_data.get("title", "").strip()
        selftext = post_data.get("selftext", "").strip()
        permalink = "https://reddit.com" + post_data.get("permalink", "")

        comments = extract_comments(data[1]["data"]["children"])

        lines = [
            f"Source: r/UCI | {doc['slug']}",
            f"URL: {permalink}",
            f"Title: {title}",
            "",
        ]
        if selftext:
            lines.append(selftext)
            lines.append("")
        lines.append("--- COMMENTS ---")
        lines.extend(f"\n[comment]\n{c}" for c in comments)

        out_text = "\n".join(lines)
        fname = f"{doc['id']:02d}_{doc['slug']}_raw.txt"
        with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(out_text)
        print(f"  ✓  Saved {fname}  ({len(comments)} comments, {len(out_text):,} chars)")

    except Exception as e:
        print(f"  ✗  Failed: {e}")

    time.sleep(2)  # polite delay

print(f"\nDone! Files saved to ./{OUT_DIR}/")
print("Copy them into your project's documents/ folder and re-run ingest.py")

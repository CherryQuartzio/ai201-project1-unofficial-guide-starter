"""
Milestone 5: Grounded generation + Gradio interface.

Usage:
  python app.py                    # launch Gradio UI
  python app.py --test             # run 3 built-in end-to-end tests without UI
"""

import argparse
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from embed import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
TOP_K = 5

SYSTEM_PROMPT = """\
You are a helpful guide for UCI (University of California, Irvine) on-campus housing.

Answer the user's question using ONLY the context passages provided below.
- Do not use any outside knowledge or general facts not present in the context.
- If the answer cannot be found in the provided context, respond with exactly:
  "I don't have information about that in my documents."
- Be specific and quote or paraphrase the relevant details from the context.
- End every answer with a "Sources:" section listing the title and URL of each
  Reddit thread you drew information from. Only list sources you actually used.\
"""


def build_context_block(hits: list) -> str:
    parts = []
    for i, hit in enumerate(hits, 1):
        meta = hit["metadata"]
        parts.append(
            f"[Passage {i}]\n"
            f"Thread: {meta.get('description', 'Unknown')}\n"
            f"URL: {meta.get('source_url', 'N/A')}\n\n"
            f"{hit['text']}"
        )
    return "\n\n---\n\n".join(parts)


def format_sources(hits: list) -> str:
    seen = set()
    lines = []
    for hit in hits:
        meta = hit["metadata"]
        url = meta.get("source_url", "")
        if url and url not in seen:
            seen.add(url)
            desc = meta.get("description", "Unknown thread")
            lines.append(f"• {desc}\n  {url}")
    return "\n\n".join(lines) if lines else "No sources retrieved."


def answer(query: str) -> tuple[str, str]:
    if not query.strip():
        return "Please enter a question.", ""

    hits = retrieve(query, k=TOP_K)
    context_block = build_context_block(hits)
    sources_text = format_sources(hits)

    user_message = (
        f"Context passages:\n\n{context_block}\n\n"
        f"---\n\nQuestion: {query}"
    )

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content.strip()
    return answer_text, sources_text


def build_ui():
    with gr.Blocks(title="UCI Housing Unofficial Guide") as demo:
        gr.Markdown(
            "## UCI Housing Unofficial Guide\n"
            "Ask anything about UCI on-campus housing — Mesa Court, Middle Earth, "
            "Plaza Verde, VDC, ACC apartments, and more. "
            "Answers are grounded in real student Reddit reviews."
        )

        with gr.Row():
            query_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What do students say about the flooring in Plaza Verde?",
                lines=2,
                scale=4,
            )
            submit_btn = gr.Button("Ask", variant="primary", scale=1)

        answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
        sources_box = gr.Textbox(label="Retrieved sources", lines=6, interactive=False)

        submit_btn.click(fn=answer, inputs=query_box, outputs=[answer_box, sources_box])
        query_box.submit(fn=answer, inputs=query_box, outputs=[answer_box, sources_box])

    return demo


TEST_QUERIES = [
    ("in-scope / strong", "What do students say about Middle Earth being better for CS majors?"),
    ("in-scope / weak retrieval", "Does Vista del Campo put a cap on electricity usage?"),
    ("out-of-scope (must refuse)", "What is the capital of France?"),
]


def run_tests():
    for label, query in TEST_QUERIES:
        print(f"\n{'='*70}")
        print(f"TEST [{label}]")
        print(f"QUERY: {query}")
        print("=" * 70)
        ans, sources = answer(query)
        print(f"\nANSWER:\n{ans}")
        print(f"\nSOURCES:\n{sources}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run built-in tests instead of launching UI")
    args = parser.parse_args()

    if args.test:
        run_tests()
    else:
        ui = build_ui()
        ui.launch()

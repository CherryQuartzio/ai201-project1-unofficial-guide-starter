# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

My domain will be about on-campus housing at the University of California, Irvine. There are many community available for students who wish to stay on-campus, but knowing everything through official means can be difficult. Informations like floor plan, living experiences, amendities are best answered by students who had the chance to be there, where such thoughts are usually scattered across many different channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/UCI - first year housing scoop | Reddit thread | https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/ |
| 2 | r/UCI - Honest opinions about living in plaza verde? | Reddit thread | https://www.reddit.com/r/UCI/comments/x4b6hb/honest_opinions_about_living_in_plaza_verde/ |
| 3 | r/UCI - ACC question - comment your experiences in VDC/Plaza! | Reddit thread | https://www.reddit.com/r/UCI/comments/10js4cg/acc_question_comment_your_experiences_in_vdcplaza/ |
| 4 | r/UCI - Are the Acc apartments really that bad? | Reddit thread | https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/ |
| 5 | r/UCI - Middle Earth or Mesa Court | Reddit thread | https://www.reddit.com/r/UCI/comments/1ss7sgp/middle_earth_or_mesa_court/ |
| 6 | r/UCI - Mesa Court vs Middle Earth | Reddit thread | https://www.reddit.com/r/UCI/comments/1sdqj6j/mesa_court_vs_middle_earth/ |
| 7 | r/UCI - Any opinions on ACC housing? | Reddit thread | https://www.reddit.com/r/UCI/comments/mo4ice/any_opinions_on_acc_housing/ |
| 8 | r/UCI - Middle Earth or Mesa Court???? | Reddit thread | https://www.reddit.com/r/UCI/comments/31e68h/middle_earth_or_mesa_court/ |
| 9 | r/UCI - 25+ Transfer looking at housing | Reddit thread | https://www.reddit.com/r/UCI/comments/1t04ih1/25_transfer_looking_at_housing/ |
| 10 | r/UCI - how do i choose housing options | Reddit thread | https://www.reddit.com/r/UCI/comments/1rz6gkj/how_do_i_choose_housing_options/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
- Document 1: ~1000 chars
- Document 2: ~800 chars
- Document 3: ~800 chars
- Document 4: ~1000 chars
- Document 5: ~1000 chars
- Document 6: ~1000 chars
- Document 7: ~1200 chars
- Document 8: ~600 chars
- Document 9: ~800 chars
- Document 10: ~1000 chars

**Overlap:**
- Document 1: 150 overlap
- Document 2: 100 overlap
- Document 3: 100 overlap
- Document 4: No strict overlap
- Document 5: 150 overlap
- Document 6: 150 overlap
- Document 7: No strict overlap
- Document 8: 100 overlap
- Document 9: 100 overlap
- Document 10: 150 overlap

**Why these choices fit your documents:** The sources are primarily Reddit threads containing a user's initial questions followed by replies. They're very structured in nature, where you can split one big document containing the entire thread into smaller one separated into individual comments if needed.

**Final chunk count:** 76

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:** When scaling this to real users, latency and context window limits become major constraints. However, I would heavily weigh these against strict data privacy requirements. While commercial APIs offer massive context windows and multilingual support, sending sensitive student data or internal campus documents to third parties carries risks. To ensure zero data retention (ZDR), I would strongly consider deploying more robust open-weight embedding models locally. If falling back to commercial APIs for speed, verifying their ZDR policies would be a mandatory tradeoff against the performance benefits they provide.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system enforces grounding through explicit instructions in the LLM's system prompt:
> "Answer the user's question using ONLY the context passages provided below.
> - Do not use any outside knowledge or general facts not present in the context.
> - If the answer cannot be found in the provided context, respond with exactly: 'I don't have information about that in my documents.'"

These instructions establish a strict boundary, preventing hallucinations by explicitly instructing the model how to behave when the context lacks the answer. The context chunks themselves are formatted clearly with `[Passage N]` markers, followed by their thread metadata and chunk text, creating a structured context block for the LLM to read.

**How source attribution is surfaced in the response:**
Source attribution is handled structurally rather than relying purely on the LLM. The system's retrieval function returns the `metadata` for each chunk, which contains the original Reddit thread URL and a descriptive title. The `format_sources()` function deduplicates these sources across the Top-K retrieved chunks and formats them as a bulleted list. The Gradio UI surfaces this list in a dedicated, read-only "Retrieved sources" textbox adjacent to the answer, ensuring the user can always see exactly which documents fed the generation.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the common student complaints about the flooring in Plaza Verde? | Students frequently mention that the laminate flooring in Plaza Verde produces a lot of dust and makes the apartments feel dirty very quickly. | The floor is always dusty despite cleaning, and sometimes feels sticky due to glue seeping from the laminate. | Relevant | Accurate |
| 2 | For an incoming freshman, what are the perceived benefits of choosing Middle Earth over Mesa Court? | Middle Earth is generally stereotyped as being closer to the engineering/STEM buildings and having a quieter environment. | Closer to engineering/CS buildings, better dining commons food, and quieter. | Relevant | Accurate |
| 3 | Are utilities fully covered in the rent at Vista del Campo (VDC)? | VDC covers utilities but places a cap on electricity usage; extra charges are split among roommates. | Electricity, gas, and water are included in the rent (missed the cap detail). | Partially relevant | Partially accurate |
| 4 | Which ACC community is generally considered better for parking: Camino del Sol or Vista del Campo Norte (VDCN)? | VDCN is widely considered better for parking because it has its own dedicated, adjacent parking structure. | VDCN is generally considered better for parking compared to other ACC communities. | Relevant | Accurate |
| 5 | What is a major downside of living on the first floor in Plaza Verde according to Reddit reviews? | First-floor residents often report safety concerns due to people walking directly outside their windows, and bugs. | The system stated there is no specific mention of a major downside and that the comments section was empty. | Off-target | Inaccurate |

**Retrieval quality ratings:** Relevant / Partially relevant / Off-target  
**Response accuracy ratings:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What is a major downside of living on the first floor in Plaza Verde according to Reddit reviews?

**What the system returned:** The system stated there is no specific mention of a major downside of living on the first floor in Plaza Verde, and claimed the comments section in the retrieved context was empty.

**Root cause (tied to a specific pipeline stage):** The failure occurred during the **retrieval** stage due to limitations in the **chunking strategy**. The semantic search successfully retrieved the chunk containing the original Reddit post (where the user asks about first-floor issues) because its text heavily matched the query. However, the comments that actually answered the question were located in separate chunks further down the document. Because `top_k=5` was filled with other general Plaza Verde chunks and the original post chunk, the specific chunks with the actual answers (mentioning bugs and safety concerns) were pushed out of the retrieval window. The LLM accurately summarized the retrieved context, which was just the question prompt without the helpful replies.

**What you would change to fix it:** Implement a parent-child chunking strategy or metadata filtering. By indexing chunks hierarchically, retrieving a post's main question would automatically pull in the top comments associated with it, ensuring the answer context travels with the question context during retrieval.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Forcing the chunking strategy and retrieval plan to be defined upfront in `planning.md` made writing `ingest.py` straightforward. Knowing the exact chunk size and overlap beforehand prevented unnecessary trial-and-error during the implementation phase.

**One way your implementation diverged from the spec, and why:** We originally planned to just use standard text extraction, but we had to diverge and add a specific `preprocess_html()` step to aggressively strip `<script>` and `<style>` tags. This was necessary because Reddit's dynamic loading and browser extensions injected massive amounts of CSS/JS boilerplate into the chunks, which would have ruined the embedding and retrieval process.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: Given the chunking strategy and all the raw HTMLs, I asked Claude to filter out unecessary detail and keep only clean text files for use as documents*
- *What it produced: An ingest.py file that doesn't filter out all junk from the txt*
- *What I changed or overrode: Amend the file to filter out dangling CSS blocks*

**Instance 2**

- *What I gave the AI: Ask it to give me a chunking strategy for each of the 10 documents*
- *What it produced: A mix of chunking strategies for each of the documents despite all of them are in the same format in general*
- *What I changed or overrode: Consolidate all documents to use the recursive chunking strategy*

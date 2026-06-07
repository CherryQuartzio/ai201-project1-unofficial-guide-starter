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

**Model used:** 

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain will be about on-campus housing at the University of California, Irvine. There are many community available for students who wish to stay on-campus, but knowing everything through official means can be difficult. Informations like floor plan, living experiences, amendities are best answered by students who had the chance to be there, where such thoughts are usually scattered across many different channels.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/UCI - first year housing scoop | A highly detailed breakdown comparing the pros and cons of Mesa Court vs. Middle Earth, specifically distinguishing between the "Towers" and "Classics" layouts. | https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/ |
| 2 | r/UCI - Honest opinions about living in plaza verde? | Specific, honest student opinions on Plaza Verde, including details on room layouts, dust issues with the laminate flooring, and safety concerns about living on the first floor. | https://www.reddit.com/r/UCI/comments/x4b6hb/honest_opinions_about_living_in_plaza_verde/ |
| 3 | r/UCI - ACC question - comment your experiences in VDC/Plaza! | A deep dive comparing Vista del Campo (VDC) and Plaza Verde, focusing on room space, utility bills, internet reliability, and parking convenience. | https://www.reddit.com/r/UCI/comments/10js4cg/acc_question_comment_your_experiences_in_vdcplaza/ |
| 4 | r/UCI - Are the Acc apartments really that bad? | A thread addressing rumors about ACC apartments, with firsthand accounts of maintenance responsiveness, internet outages, and mold issues on the first floor at VDCN. | https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/ |
| 5 | r/UCI - Middle Earth or Mesa Court | A recent comparison of the two freshman housing communities, discussing which is better for engineering majors, social life, and the differences in the dining halls (Anteatery vs. Brandywine).| https://www.reddit.com/r/UCI/comments/1ss7sgp/middle_earth_or_mesa_court/ |
| 6 | r/UCI - Mesa Court vs Middle Earth | Insights from a Psychology major evaluating whether the longer walk from Mesa Court to the Social Sciences buildings is worth the potentially better social environment and newer facilities. | https://www.reddit.com/r/UCI/comments/1sdqj6j/mesa_court_vs_middle_earth/ |
| 7 | r/UCI - Any opinions on ACC housing? | A comprehensive thread covering the general feel of various ACC communities, comparing the modern feel of Camino del Sol to the parking advantages at VDCN. | https://www.reddit.com/r/UCI/comments/mo4ice/any_opinions_on_acc_housing/ |
| 8 | r/UCI - Middle Earth or Mesa Court???? | A classic debate thread analyzing the stereotypes of both freshman dorms (e.g., Mesa Court being more party-oriented and Middle Earth being more studious and STEM-focused). | https://www.reddit.com/r/UCI/comments/31e68h/middle_earth_or_mesa_court/ |
| 9 | r/UCI - 25+ Transfer looking at housing | Perspectives on housing for transfer and older students, comparing the community feel of ACC apartments to the subsidized cost and quieter environment of Graduate and Family housing. | https://www.reddit.com/r/UCI/comments/1t04ih1/25_transfer_looking_at_housing/ |
| 10 | r/UCI - how do i choose housing options | A Q&A thread helping incoming freshmen navigate housing applications, specifically discussing how to ensure placement in on-campus residence halls like Mesa Towers. | https://www.reddit.com/r/UCI/comments/1rz6gkj/how_do_i_choose_housing_options/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

I'm planning to do a recursive chunking strategy.

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

**Reasoning:** My sources are primarily Reddit threads containing a user's initial questions followed by replies. They're very structured in nature, where you can split one big document containing the entire thread into smaller one separated into individual comments if needed.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5 chunks per query

**Production tradeoff reflection:** When scaling this to real users, latency and context window limits become major constraints. However, I would heavily weigh these against strict data privacy requirements. While commercial APIs offer massive context windows and multilingual support, sending sensitive student data or internal campus documents to third parties carries risks. To ensure zero data retention (ZDR), I would strongly consider deploying more robust open-weight embedding models locally—perhaps provisioning a cloud server with dedicated hardware like an RTX 3080. If falling back to commercial APIs for speed, verifying their ZDR policies would be a mandatory tradeoff against the performance benefits they provide.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the common student complaints about the flooring in Plaza Verde? | Students frequently mention that the laminate flooring in Plaza Verde produces a lot of dust and makes the apartments feel dirty very quickly. |
| 2 | For an incoming freshman, what are the perceived benefits of choosing Middle Earth over Mesa Court? | Middle Earth is generally stereotyped as being closer to the engineering/STEM buildings and having a quieter, more studious environment compared to Mesa Court. |
| 3 | Are utilities fully covered in the rent at Vista del Campo (VDC)? | VDC covers utilities but places a cap on electricity usage; if an apartment goes over that cap, the extra charges are split among the roommates. |
| 4 | Which ACC community is generally considered better for parking: Camino del Sol or Vista del Campo Norte (VDCN)? | VDCN is widely considered better for parking because it has its own dedicated, adjacent parking structure, whereas Camino residents often have to walk further. |
| 5 | What is a major downside of living on the first floor in Plaza Verde according to Reddit reviews? | First-floor residents often report safety concerns due to people walking directly outside their windows, as well as an increased likelihood of encountering bugs. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reddit Jargon and Acronyms: The UCI subreddit is heavily reliant on abbreviations (e.g., PV, VDC, VDCN, ACC, ME, MC). If the user queries "Vista del Campo Norte" but the retrieved chunks only contain "VDCN", semantic search might miss the most relevant reviews unless the embedding model inherently understands that relationship.
2. Splitting Multi-Topic Narratives: Students often write massive, comprehensive reviews covering parking, Wi-Fi, roommates, and laundry in a single post. Even with overlap, chunking might slice this narrative in half. If a query asks about both laundry and parking at Camino del Sol, the retrieval might only grab the chunk containing the laundry info, leading to an incomplete generated answer.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

[ Raw UCI Reddit Threads ]
          |
          v
+----------------------------+
|   1. Document Ingestion    |  (Text extraction & cleaning)
+----------------------------+
          |
          v
+----------------------------+
|        2. Chunking         |  (Recursive Character Splitter)
+----------------------------+
          |
          v
+----------------------------+
|   3. Embedding & Vector    |  (sentence-transformers:
|          Store             |   all-MiniLM-L6-v2 + ChromaDB)
+----------------------------+
          |
          v
+----------------------------+
|        4. Retrieval        |  (Top-K Semantic Search)
+----------------------------+
          |
          v
+----------------------------+
|        5. Generation       |  (Groq: llama-3.3-70b-versatile)
+----------------------------+
          |
          v
[ Grounded, Cited UI Answer ]

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

1. Document Ingestion & Cleaning

Tool: Claude

Input: The "Documents" section (containing the 10 Reddit URLs) and the instruction to extract only the substantive review/comment text while stripping away Reddit's UI boilerplate, HTML tags, and navigation elements.

Expected Output: A Python script (ingest.py) that fetches the URLs, cleans the text, and saves each thread as a cleanly formatted .txt file.

Verification: I will run the script and manually read through 2-3 of the output text files to ensure no HTML artifacts (&amp;, <div>) or irrelevant sidebar text remain.

2. Chunking

Tool: Claude

Input: My "Chunking Strategy" section specifying the Recursive Character Splitter with a chunk size of about 1000 and an overlap of about 150 (may vary between posts), along with a sample of the cleaned Reddit text.

Expected Output: A Python function (chunk_text()) that utilizes a library like LangChain's RecursiveCharacterTextSplitter configured with my exact parameters.

Verification: I will print 5 random chunks to the console. I will read each one to ensure it captures a complete, standalone thought (like a full review of Plaza Verde) and isn't slicing sentences in half.

3. Embedding & Vector Store

Tool: Claude

Input: The "Retrieval Approach" section and the pipeline architecture diagram. I will explicitly instruct it to use sentence-transformers (all-MiniLM-L6-v2) and initialize a local ChromaDB collection.

Expected Output: A script that iterates through my chunked texts, embeds them, and inserts them into ChromaDB, ensuring that the source URL or filename is attached as metadata.

Verification: I will write a quick print statement to check the total item count in the ChromaDB collection and verify it matches the total number of chunks produced in the previous step.

4. Retrieval

Tool: Claude

Input: The "Retrieval Approach" section specifying a Top-K of 5, and the 5 specific test questions from my "Evaluation Plan".

Expected Output: A retrieve(query) function that queries the ChromaDB collection and returns the top 5 chunks along with their distance/similarity scores and metadata.

Verification: I will pass 3 of my test questions into the function. I will manually read the returned chunks to ensure they are actually on-topic (e.g., querying about VDC parking actually returns chunks about VDC parking) and check that the distance scores indicate a strong match.

5. Generation & Interface

Tool: Claude

Input: The "Grounded Response Generation" requirements, the instruction to use the Groq API (llama-3.3-70b-versatile), and the requirement for a basic Gradio web interface. I will explicitly emphasize that the LLM prompt must strictly enforce grounding and source citation.

Expected Output: An app.py file containing the Groq API call with a strict system prompt, wired up to a Gradio interface with input/output text boxes and a separate box displaying the cited sources.

Verification: I will test the Gradio UI with an out-of-domain question (e.g., "What is the capital of France?"). The system passes verification if it outright refuses to answer. For in-domain questions, I will verify that every response includes a clear citation linking back to the specific Reddit thread it pulled the information from.

**Milestone 3 — Ingestion and chunking:**
Pipeline implemented in `ingest.py`. All 10 Reddit HTML files were parsed, stripped of style/script blocks, cleaned of boilerplate (JS, CSS, UI chrome), and chunked with per-document `RecursiveCharacterTextSplitter` settings. Results: **76 total chunks** across 10 documents, average chunk length 719 chars (min 135, max 1200). Chunks persisted to `chunks.json` for Milestone 4. 5 representative chunks inspected manually — each contains a complete, self-contained student opinion with no HTML/JS artifacts.

**Milestone 4 — Embedding and retrieval:**
Pipeline implemented in `embed.py`. All 76 chunks embedded with `all-MiniLM-L6-v2` and persisted to a local ChromaDB collection (`uci-housing`). Retrieval function `retrieve(query, k=5)` returns top-k hits with text, source URL, description, chunk index, and cosine distance.

Test retrieval results (3 of 5 evaluation queries):

| Query | Quality | Notes |
|-------|---------|-------|
| "What do students say about the flooring in Plaza Verde?" | Partial | Rank 1 is the correct Plaza Verde thread (distance 0.65) but the specific laminate dust complaint lives deeper in that doc; ranks 2–5 drift to general ACC/Mesa topics. |
| "Is Middle Earth better than Mesa Court for STEM students?" | Strong | All 5 results on-topic (distances 0.55–0.69); chunks directly name CompSci proximity and STEM stereotypes. |
| "Does Vista del Campo cover utilities in rent?" | Weak | Distances are high (1.29–1.35); rank 3 contains the relevant sentence ("electricity and gas and water is included in rent") but the electricity cap nuance—key to the expected answer—does not appear in any retrieved chunk. Likely a retrieval failure case for the evaluation report. |

**Milestone 5 — Generation and interface:**
Pipeline implemented in `app.py`. Groq (`llama-3.3-70b-versatile`) with a strict grounding system prompt — model is instructed to answer only from retrieved context and refuse otherwise. Source attribution is appended to every answer. Gradio UI has three components: question input, answer box, and retrieved sources box. End-to-end tests:

| Test | Query | Result |
|------|-------|--------|
| In-scope / strong retrieval | "What do students say about Middle Earth being better for CS majors?" | Accurate, grounded answer with two source URLs cited |
| In-scope / weak retrieval | "Does Vista del Campo put a cap on electricity usage?" | Refused ("I don't have information about that in my documents") — the electricity cap detail is absent from retrieved chunks; documented as failure case |
| Out-of-scope | "What is the capital of France?" | Correctly refused — grounding enforcement works |

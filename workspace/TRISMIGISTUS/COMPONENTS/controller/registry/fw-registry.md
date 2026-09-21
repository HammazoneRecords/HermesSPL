
# Future Work

**Purpose:** Running log of future features, systems, and work stated by Deego during sessions.
**Protocol:** When Deego states a future feature or planned work, append it here immediately. Never delete entries — mark as `[done]` when complete.

---

## Format

```
## [FW-N] — [Short title]
**Stated:** YYYY-MM-DD
**Context:** [what was being discussed when this was mentioned]
**Status:** pending | in-progress | done

[Description]
```

---

## Entries

---

## [FW-001] — Conversation-tailored version of the Argument Map Framework
**Stated:** 2026-03-15
**Context:** Designing the AMF (Argument Map Framework) — distinguishing logic-trace maps from conversation-capture maps
**Status:** pending

In the future, build a second a-map variant optimized for capturing conversations rather than logic traces. The current AMF is built to trace argument flow and facts. The conversation variant would capture tone, progression of understanding, emotional/intellectual shifts, and dialogue structure. Two distinct renditions of the same framework serving different purposes.

---

## [FW-002] — LLM Fine-tuning Dataset from Argument Map Framework
**Stated:** 2026-03-15
**Context:** Discussing the AMF as a knowledge representation system
**Status:** pending

Use argument maps (a-maps) + the raw facts they contain as fine-tuning data for LLMs. The a-map structure provides the reasoning scaffold; the facts provide the content. Fine-tuning on both together teaches the model to reason in revelation order — not just to recall facts but to follow and reproduce argument chains. This is a future training pipeline for Deego's custom LLM.

---

## [FW-003] — AMF as Context Retention and Management System for Deego's LLM
**Stated:** 2026-03-15
**Context:** Discussing the future use of the AMF inside a custom LLM
**Status:** pending

Inside Deego's own LLM, a rendition of the Argument Map Framework will serve as the context retention and management layer. Instead of raw conversation history or token windows, the model maintains an active a-map of the current reasoning session — compressing context into structured nodes while preserving logical flow. Nodes that are resolved or settled get archived; open `.q` nodes remain active. This enables long-context coherence without token bloat.

---

## [FW-004] — Timestamp / Time-Awareness for Custom Models
**Stated:** 2026-03-15
**Context:** Discovering that ChatGPT's raw HTML export has accurate per-message Unix timestamps, while the live ChatGPT interface gives zero time-based context in conversations
**Status:** pending

Custom models must be time-aware at the message level. Every conversation message should carry its `create_time` timestamp and the model should be able to reason about it — e.g., "you asked this 3 months ago", "this decision was made before X", "this contradicts what you said in January". ChatGPT withholds this despite having the data. Deego's models will surface it. Implementation: store timestamps alongside embeddings in LanceDB, expose them in retrieval results, and include temporal context in prompt assembly.

---

## [FW-005] — LLM Access to Deleted / Edited Pre-Send Messages
**Stated:** 2026-03-15
**Context:** Observing that users delete and rewrite messages before sending — that edit history contains word choice preferences, hesitation patterns, and changes of mind that the final message erases.
**Status:** pending

Custom LLM should have access to the full edit history of a user message before it was sent — not just the final version. This includes deleted drafts, mid-sentence pivots, re-framings. The model can use this to understand: preferred vocabulary, what the user considered but rejected, emotional signals in the revision process. Implementation: capture keypress/edit events at input layer, store delta history alongside final message, include in model context as a structured pre-message artifact.

---

## [FW-006] — Jamaican Patois NLP Dataset
**Stated:** 2026-03-15
**Context:** Claude and all current models handle Patois poorly — things get lost in translation. Authentic Patois speakers won't use AI tools that can't understand them. Cultural failure and market gap.
**Status:** pending

Build a Patois training dataset to fine-tune custom models for authentic Jamaican Patois comprehension and generation. Covers: vocabulary, code-switching patterns (Patois ↔ English), idiomatic expressions, tonal/emotional register, cultural context. Dataset sources: drayl journals, ChatGPT conversation exports (391 files with Patois-heavy messages), handcrafted sentence pairs. Goal: models that yardie speakers actually want to use.

---

## [FW-007] — DeepSeek Integration via Continue Plugin (VS Code)
**Stated:** 2026-03-15
**Context:** Continue.dev VS Code extension supports routing to DeepSeek and other OpenAI-compatible APIs. Claude Code is Claude-only but Continue can run alongside it as a supplementary model layer.
**Status:** pending

Configure Continue plugin to route to DeepSeek API as a supplementary coding model in VS Code. DeepSeek offers strong code reasoning, is open-weights compatible, and aligns better with sovereignty goals than proprietary-only tools. Continue plugin config: `~/.continue/config.json` — add DeepSeek provider block with API key. Longer term: replace all external API routing with own fine-tuned models per session mode.

---

## [FW-008] — Swappable Expressions with [intensity] Tags (Patois Dataset)
**Stated:** 2026-03-15
**Context:** Building the Patois calibration dataset — need a system for tagging expressions with intensity levels so a model can use the right-weight expression for a given emotional context. Related to a dataset generator app Deego built (name TBD).
**Status:** pending

Add `[intensity]` metadata tags to expression entries in the Patois dataset. Each expression cluster groups semantically equivalent phrases at varying intensity levels — e.g., for anger: "vex" (low) → "mad" (mid) → "livid" (high) → "ready fi buss" (extreme). A model trained on these tags can select the expression that matches the required intensity rather than defaulting to a single word. This creates swappable expression slots: `[emotion:anger][intensity:0.3]` → outputs the right-weight Patois phrase. Bridges the gap between semantic meaning and tonal weight in code-switching contexts. Connect to English direct translation pairs in Patois calibration lab for cross-reference.

---

## [FW-009] — Mental Readiness Hour (Phase Packs + MW Concept)
**Stated:** 2026-03-15
**Context:** Working on Phase Packs (entrepreneur startup guide) for mindwaveja.com site — idea arose mid-session.
**Status:** pending

Add a "Mental Readiness Hour" as a concept to both the Phase Packs system and MindWave concepts. Core idea: a structured hour at the start of work that includes (1) a note — capture whatever is on your mind to clear mental cache, (2) creative procrastination — intentionally using idle/drift time to let subconscious inspiration surface about your business or current problem. The "creative procrastination" framing reframes procrastination as a tool rather than a failure — idle time is not wasted, it is incubation. Applicable to entrepreneurs (Phase Packs context) and to any deep knowledge worker. Add to Phase Packs as a ritual/habit module; add to MW concepts as a cognitive pattern node.

---

## [FW-010] — Dependency Headers in Orientation / Key Files
**Stated:** 2026-03-15
**Context:** Session protocol design — need a way for any file to declare which other files must be updated when it changes.
**Status:** pending

Add a standardized header section to all orientation files and key governance files (CLAUDE.md, session-protocol.md, etc.) that declares dependencies — i.e., "if this file is modified, these other files must also be updated." Format:
```
## Dependencies
**Updates this file triggers:**
- file_A.md — reason
- file_B.md — reason
```
This creates a lightweight dependency graph baked into the files themselves. When Claude modifies any file, it checks the Dependencies section and propagates changes. Prevents orientation drift without requiring a full audit. Start with session-protocol.md and CLAUDE.md as the first two files to receive this header.

---

## [FW-012] — Tags Field in LanceDB Schema
**Stated:** 2026-03-15
**Context:** Once Jhanos and #type tags are assigned to content, they should be stored in LanceDB as a queryable field — enabling filtered queries like "show all BARA content" or "find all axioms tagged ORON". Currently the schema has no tags field.
**Status:** done

Add a `tags` field (list of strings) to the `DraylDocument` LanceDB schema. Update `ingest_lancedb.py` to accept tags from file frontmatter or a separate tag mapping file. Build a `tag_lancedb.py` script to assign/update tags on existing records without full re-ingestion. Once in place, queries like `cat:drayl_brainstorms #jhanos:BARA` return only BARA-tagged brainstorms. Full coherence: every content type has both a semantic vector AND explicit Jhanos/type tags for filtered retrieval.

---

## [FW-013] — NotebookLM Source Manifest Script
**Stated:** 2026-03-15
**Context:** LanceDB stores source file paths (`file_path`, `file_name`) for every chunk. NotebookLM requires manual source uploads. To keep both systems coherent — so every LanceDB query result traces back to a known, uploadable source — we need an automated manifest.
**Status:** pending

Build `scripts/export_sources_notebooklm.py`: queries LanceDB for all unique source files, outputs a manifest (CSV or plain list) of `drayl/<file_path>` entries. User uploads manifest files to NotebookLM. When LanceDB returns a result with `SOURCE: drayl/path/to/file.md`, that exact file is already in NotebookLM — zero guessing, zero ambiguity. Script should also output counts per category so the user knows which folders are represented. Run after any new ingestion to keep the manifest current.

---

## [FW-011] — MW_CENTRAL-Specific Tag Expansion for Intake Taxonomy
**Stated:** 2026-03-15
**Context:** The Solobic tag taxonomy in `intake_procedure/` was designed as a standalone base template from a folder-room mind map concept — not specifically for MW_CENTRAL. The base tags (#type, #jhanos, @base, @project, #risk, #confidence, #soma) are a starting template. MW_CENTRAL has content types and routing destinations that need their own tags.
**Status:** done

Audit the existing Solobic base tags against the actual content types in MW_CENTRAL (journals, axioms, insights, FW entries, app specs, songs, brainstorms, research, governance docs). Add workspace-specific tags where the base template doesn't cover them — e.g., #type:axiom, #type:insight, #type:fw-entry, @dest:drayl, @dest:ideas, @dest:mindwave. Update `intake_procedure/Taxonomy Tag Registry.md` with the new tags. Cross-reference `INTAKE_WORKFLOW.md` triage table so every row has a valid tag. Goal: a tag registry that is both Solobic-compatible and MW_CENTRAL-complete.

---

## [FW-015] — Writing Style Doc: Linguistic Patterns Section
**Stated:** 2026-03-24
**Context:** TMS book work — Deego wants to document personal linguistic patterns and speech habits in the writing style doc using samples pulled directly from drayl journal entries
**Status:** pending

Add a "Linguistic Patterns" section to `drayl/drayl_profile/General_My_Writing_Style.md`. Source: Deego selects 3–5 drayl journal entries that feel most representative of natural voice. Claude reads them, extracts recurring patterns — sentence structures, Patois cadence, rhetorical moves, `//` asides, `lol` placement, mid-thought pivots, punctuation habits — and documents each pattern with annotated real quotes as examples. Fills the existing gap noted in the doc: "Writing markers / shorthand used across all modes."

---

## [FW-016] — Formalize 3 Patent Claims into patent_claims_extracted.md
**Stated:** 2026-03-30
**Context:** FHCU grant application — Page 5 written with 3 patent claims; need to save formal versions to the drayl patent_claims folder
**Status:** done — 2026-03-31, written to `drayl/patent_claims/patent_claims_extracted.md`

Three patent claims identified and written into the FHCU grant application need to be saved as formal claim documents in `drayl/patent_claims/patent_claims_extracted.md`:
1. **MWCane** — AI-assisted passive echolocation navigation device (physical innovation)
2. **Jamaican Patois Computational Corpus Methodology** — annotation schema with 5 metadata layers (continuum register, geographic dialect, African root classification, TMA tagging, code-switch boundary)
3. **Caribbean Cultural Alignment Benchmark (CCAB)** — 4-dimension AI evaluation framework tested against 8 major models

Each claim should be documented with: claim title, domain, novelty statement, what is disclosed (safe to publish), and what is withheld (core IP). These are the "give away" claims — safe for public disclosure in grant applications and research presentations.

---

## [FW-020] — WebNet (The Lightweb / UCANN)
**Stated:** 2026-03-31
**Context:** DeepSeek brainstorm — started from a thread about custom TLDs and ICANN, escalated into Deego's concept of a philosophical and infrastructural alternative to the darkweb
**Status:** pending

**The concept:** The Lightweb — a network layer that is the philosophical opposite of the darkweb in every dimension. Where the darkweb is anonymous, encrypted, and unindexed, the Lightweb is transparent, open, community-governed, and fully accessible via any regular browser. No special software required. It uses standard internet infrastructure (HTTP, DNS, VPS) but operates with a different social contract. Think: openness as a design principle, not privacy as a design principle.

**Technical architecture (brainstormed):**
- Self-hosted tunneling server (FRP or Rathole on a VPS) — bypasses Flow/Digicel residential port blocking because it's outbound-only from Jamaica
- Own CoreDNS infrastructure — full control over DNS resolution, no dependency on Google/Cloudflare
- Reverse proxy (Caddy/Nginx) on VPS for auto-HTTPS and routing
- Custom TLDs eventually (via OpenNIC-style parallel DNS root, NOT ICANN)
- Start: Cloudflare Tunnel or self-hosted FRP for a working prototype
- Decentralized DNS path: Handshake (HNS — peer-to-peer DNS root, no ICANN) or Namecoin (blockchain-based DNS) — aligns with sovereignty principle, no single authority

**Key ISP insight:** Flow/Digicel block inbound connections on residential accounts but CANNOT block outbound connections (would break the internet). FRP/Chisel architecture = local machine connects OUT to VPS → VPS accepts inbound → traffic tunneled back. Full bypass without a commercial account.

**Scale ambition:** 100 Jamaica beta testers as first milestone. This may be the only MindWave JA project Deego would take government funding for — or FHCU grant ($500K JMD) as bootstrap. Sovereignty play: own the infrastructure layer, not just the app layer.

**Related:** FHCU Entrepreneurship Award (already being applied for), FRP/DNS stack on existing Contabo VPS, MindWave JA independence principles.

---

## [FW-023] — Marcus App: Universal Advancement Query Filter
**Stated:** 2026-04-03
**Context:** Deploying Marcus Garvey App — Deego wants queries unrelated to universal advancement / Garveyite philosophy to be rejected and redirected elsewhere
**Status:** pending

Add a query classification layer to the Marcus app that rejects off-topic queries before they hit the RAG. Philosophy: Marcus Garvey's ARK should only answer questions aligned with universal advancement, self-determination, Black liberation, and Garveyite principles. Off-topic queries (e.g. "write me a recipe", "fix my code") should receive a firm redirect response, not an AI-generated answer. Implementation options: (1) Ollama pre-classifier — send query to Ollama first with a classification prompt, proceed only if it passes; (2) keyword/embedding similarity gate against a curated set of "on-mission" topics; (3) prompt-level instruction in the system prompt (weaker but simpler). Classifier should return a reason and a suggested redirect (e.g. "This question is outside the ARK's mission. For this, consult [X]."). Logged for post-deployment implementation.

---

## [FW-022] — VPS Multi-App Domain Routing
**Stated:** 2026-04-03
**Context:** Deploying Marcus app to Contabo VPS — solobility nginx config had 161.97.154.222 in server_name, causing it to intercept all bare IP traffic. Marcus app temporarily served on raw IP with no proper domain.
**Status:** pending

Assign proper domains/subdomains to each VPS-hosted app so Nginx can route by hostname rather than competing on the raw IP. Plan: `whatissolob.com` → solob-portal (already working), `marcus.mindwaveja.com` or `garvey.mindwaveja.com` → marcus-api + frontend, future WebNet node → its own subdomain. Each app gets its own `sites-available` config with explicit `server_name`. No app should use `server_name _;` or include the raw IP. SSL via Certbot for each domain.

---

## [FW-021] — Git-Based VPS Deploy Pipeline
**Stated:** 2026-04-02
**Context:** Deploying Marcus app via scp — transferred entire Windows venv, messy and slow
**Status:** pending

Replace ad-hoc scp deploys with a proper git-based deploy pipeline for all VPS-hosted apps. Pattern: push to GitHub repo → VPS pulls → PM2 restarts. One command to deploy from anywhere. Also set up rsync via Git Bash (rsync is available there) for MW_CENTRAL workspace → VPS file sync, with a proper excludes list (venv, node_modules, __pycache__, .env). Affects: Marcus app, future WebNet node, any other VPS-hosted services.

---

## [FW-019] — The Patience Agent
**Stated:** 2026-03-31
**Context:** Discussing Pacing Horizon Bias — LLMs degrading output quality near context limit. The patience agent is the architectural response to this.
**Status:** pending

A dedicated supervisor agent in a multi-agent system whose only job is to watch the other agents perform and detect competence failures. It does nothing until it sees an error — then it halts the offending agent and corrects it at the first-principles level (e.g. agent gets 3×2 wrong → patience agent halts it and reminds it: "multiplication is repeated addition, 2+2+2"). It does not do the task itself. It watches, detects drift from known competence baselines, and injects the correction at the simplest possible level. Think of it as the agent equivalent of a guide walking beside the others — silent until someone loses the path, then it doesn't take over, it points back to first principles and lets the agent find its own way through. Comes after the personal LLM is built. Related to INS-008 (Pacing Horizon Bias) and FW-018 (context self-awareness).

---

## [FW-018] — Context Window Self-Awareness for Custom Models
**Stated:** 2026-03-31
**Context:** Claude cannot see its own context metrics — no token count, no % remaining, no warning before auto-compact fires
**Status:** pending

Custom models must have real-time awareness of their own context state — current token usage, % of window consumed, estimated tokens remaining, and a threshold trigger that fires a pre-compact sweep automatically before the window fills. This is basic self-awareness that should be a given. A model that can't feel its own capacity filling is blind to one of its most critical operating constraints. Implementation: expose context metadata in the model's system state; surface it as a readable variable in prompt assembly; trigger CON-017 capture sweep automatically at ~75% window capacity. Related to FW-004 (timestamp/time-awareness) — same class of problem: models lack basic self-knowledge that humans would consider obvious.

---

## [FW-017] — Per-Client AI Agents (Deego's Voice + Knowledge, Client-Scoped)
**Stated:** 2026-03-30
**Context:** Building mindwaveja.com client intake — idea arose mid-session while working on gateway UX
**Status:** pending

For each MindWave client, build a dedicated AI agent that represents how Deego would respond, advise, and communicate with that specific client. The agent is trained/prompted on: (1) Deego's communication style and reasoning patterns; (2) the client's intake data, project scope, and history; (3) any relevant domain knowledge for their business type. The client interacts with their agent as if they were talking to Deego directly — same tone, same judgment, same decision-making framework. The agent handles follow-up questions, status updates, advice, and guidance between human sessions. Scales Deego's time without diluting his presence. Implementation path: Claude API with a system prompt constructed from the client's profile + a drayl-extracted style doc; later fine-tune on actual Deego ↔ client conversation samples.

---

## [FW-024] — Remove Vercel Connection from Marcus Garvey App
**Stated:** 2026-04-03
**Context:** Marcus app frontend is served as a static build on the VPS via Nginx. Vercel is connected to the GitHub repo and auto-triggers on every push — not needed, causes noise. Frontend has no serverless/edge requirements that would justify Vercel.
**Status:** pending

Disconnect the Vercel project from the HammazoneRecords/MarcusGarvey-App-WWMD GitHub repo. Steps: Vercel dashboard → project settings → Git Integration → disconnect. Optionally delete the Vercel project entirely if no subdomain is being used. The VPS + Nginx setup is the canonical deployment path for this app.

---

## [FW-025] — Build typo_review_queue.jsonl pipeline for journal co-work
**Stated:** 2026-04-03
**Context:** Building the Patois LLM dataset. Journal entries have ~60% typos. Need a structured review queue that separates Patois words from English typos with context, allowing Deego to manually classify each word, then auto-suggest corrections after 100-200 confirmed entries via Levenshtein matching.
**Status:** pending

Create `MIndwaVe_Ja/mw_fine_tune_plan/mindwave_ai/08_linguistics/typo_review_queue.jsonl` using the schema defined in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 3. Build a script (likely `scripts/`) that: (1) takes a journal entry, (2) runs it against the approved corpus (mw_patois_dictionary.json + confirmed_english_corrections.json), (3) flags unknown/ambiguous words as TRQ entries. After 100 confirmed entries, add Levenshtein autocorrect-candidate pass.

---

## [FW-026] — Build ovando_brown_profile/ folder structure for personal LLM
**Stated:** 2026-04-03
**Context:** Building the "Deego clone" personal LLM. Requires a growing profile capturing voice, worldview, decisions, timeline, motifs, persona markers, emotional range, metaphors, and domain knowledge — all tagged and structured as training data.
**Status:** pending

Create `MIndwaVe_Ja/mw_fine_tune_plan/solob_pob_llm/ovando_brown_profile/` with the files defined in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 4. Start with `voice_corpus.jsonl` (JSONL format, one entry per extracted passage). Confirm structure with Deego before ingesting large batches. This feeds the solob_pob_llm pipeline directly.

---

## [FW-027] — Connect journal co-work extraction to LanceDB ingest pipeline
**Stated:** 2026-04-03
**Context:** Once the voice_corpus.jsonl and profile files are building up, they should be queryable via LanceDB for retrieval during LLM training and for semantic search across Deego's own thinking.
**Status:** pending

Add `ovando_brown_profile/` and `08_linguistics/` as LanceDB ingest sources once the first 50+ entries exist. Verify that the JSONL entries are structured with enough metadata (source, state, tags) to return useful results in retrieval. May require a new ingest script variant for JSONL vs. .md files.

---

## [FW-028] — Build IMG catalog for journal image backlog
**Stated:** 2026-04-03
**Context:** Journal IMG folder has 118 images + Drayl2/IMG has 162 images — ~280 total uncataloged. Images have timestamped filenames (e.g., `1219 9.28.25.jpeg` = 12:19pm Sept 28 2025). Need catalog files per image using media2md (already in active_apps) in verbatim mode, linked to journal entry segments.
**Status:** pending

Create `drayl/drayl_journal/IMG/catalog/` folder. For each image: run through media2md (verbatim mode), create `IMG-YYYY-MM-DD-HHMM.md` catalog file with description, linked_segments, tags. Process in chronological order, 10-20 per session. Patois-dense images route to typo_review_queue. Full spec in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 11.

---

## [FW-029] — Build tag_index.json and segment store
**Stated:** 2026-04-03
**Context:** Journal co-work extraction produces SEG-YYYY-MM-DD-NNN segments with comprehensive tags. Need a central tag index for retrieval — theme clustering, concept linking, LLM training curation. Also need the segment store itself (JSONL or SQLite).
**Status:** pending

Create `MIndwaVe_Ja/mw_fine_tune_plan/solob_pob_llm/ovando_brown_profile/tag_index.json` and `segments.jsonl`. Decide: JSONL for portability, SQLite for query speed. Likely start JSONL and migrate to SQLite once 200+ segments exist. Tag taxonomy defined in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 10.

---

## [FW-030] — Build concept_threads.md linkage layer
**Stated:** 2026-04-03
**Context:** Once tag index exists, concepts, people, and events that recur across multiple journal entries need to be linked into threads — showing how an idea evolved over time. Critical for the personal LLM to understand Deego's thinking arcs.
**Status:** pending

After 50+ segments are processed, do a first concept linking pass. Create `ovando_brown_profile/concept_threads.md`. Group by: #concept:X, #person:name, #event:type clusters. Note status: emerging / recurring / hardened / resolved / abandoned. This feeds both the LLM training and the axiom pipeline.

---

## [FW-031] — Build journal-to-dataset distillation pipeline
**Stated:** 2026-04-03
**Context:** The drayl journal IS the first Patois LLM dataset. Raw journal text must be distilled: English typos corrected/separated, Patois phrases extracted and given 4 intensity variants (light code-switch → deep yard), variants linked via phrase_id, stored in EchoBox patwah_sentence_corpus + phrase_corpus.jsonl. Only Deego-approved variants enter corpus.
**Status:** pending

Pipeline: raw segment → typo pass (TRQ) → phrase extraction → quality gate (4+ words, clear English equivalent, natural voice) → variation generation (Claude generates 4 variants) → Deego review → store. EchoBox's patwah_sentence_corpus already accepts english_source / literal_patwah / natural_patwah / idiomatic_patwah — these map directly to intensity 1-4. Also store portable backup in `MIndwaVe_Ja/mw_fine_tune_plan/mindwave_ai/08_linguistics/phrase_corpus.jsonl`. Full schema in co-work instructions.

---

## [FW-032] — Import contact list and cross-reference with people directory
**Stated:** 2026-04-03
**Context:** Deego wants to add his full contact list to the people directory, then cross-reference every contact against journal mentions. People already in `drayl/drayl_journal/people/` will get a `contact_ref` field. Journal mentions without a contact get flagged `contact_ref: not-in-contacts`.
**Status:** pending

Tomorrow task: export contacts (likely from phone as CSV or vCard), parse names/aliases/phones, match against `people/_people_index.md`. For each match: update `contact_ref:` in the person file. For each journal person without a contact match: note `not-in-contacts`. Script may be needed if contact list is large — check format first.

---

## [FW-033] — Add analytics to whatissolob.com
**Stated:** 2026-04-10
**Context:** Deego said "we dont have any analytics, that doesnt matter right now still" while reviewing the solob-portal. Deferred but acknowledged.
**Status:** pending

Add analytics tracking to whatissolob.com. Options: (1) Plausible Analytics (privacy-first, no cookies, GDPR-compliant, self-hostable on existing VPS) — preferred for sovereignty; (2) Fathom (similar); (3) Google Analytics (avoid if possible). Minimum events to track: page views, gate selections, forge-book completions, PDF downloads, reader heartbeat (already partially tracked in solobility.db). The SQLite `reader_analytics` table already captures reading progress server-side — the missing layer is front-end funnel tracking (drop-off at each step: Threshold → Gate → Offering → Confirmation → Reader).

---

## [FW-034] — Deploy mindwaveja.com to VPS or Vercel
**Stated:** 2026-04-11
**Context:** MindwaveJA site was run locally this session. Needs to be deployed — Vercel is recommended for Next.js in the site's own SETUP_INSTRUCTIONS.md.
**Status:** pending

Deploy mindwaveja.com Next.js site. Options: (1) Vercel — easiest for Next.js, free tier available, auto-deploy on push; (2) VPS self-host — more sovereignty, more setup (build step, PM2, Nginx, SSL). Check if domain `mindwaveja.com` is already pointing anywhere. Premium pack payment gating will need to be wired before launch — currently `tier: "premium"` and `price` fields exist in phasePacks.json but no checkout flow is implemented yet.

---

## [FW-035] — Wire premium pack payment gating on mindwaveja.com
**Stated:** 2026-04-11
**Context:** 5 premium packs set to JMD 5,000 each in phasePacks.json. The `tier` and `price` fields exist in the data but the UI has no checkout or gating logic yet.
**Status:** pending

Build checkout flow for premium Phase Packs. Options: (1) Stripe with JMD support (check Stripe Jamaica availability — may require USD); (2) Direct bank transfer (Scotiabank details already in solob-portal Confirmation page — reuse pattern); (3) WhatsApp-to-purchase flow (manual but works immediately). Minimum: gate the premium pack detail/download behind a paywall, show price and CTA. The `comingSoon` + `availableDate` pattern used for marketplace products could be adapted as a temporary placeholder.

---

## [FW-036] — Book of Solobility marketing execution
**Stated:** 2026-04-10
**Context:** Marketing plan written to `playground/2026-04-marketing/book-of-solobility/marketing-plan.md` this session.
**Status:** pending

Execute the marketing plan: (1) Set up Instagram + TikTok accounts (`@whatissolob` or `@solobility`); (2) Record "What is Solobility?" anchor video for YouTube; (3) Design gate cards in Canva (dark bg, glyph + text); (4) Print QR stickers for Kingston physical campaign — use `whatissolob.com/?ref=qr-kingston` UTM; (5) Start $50 Instagram boost once first gate post hits 200 organic reach. See full plan at `playground/2026-04-marketing/book-of-solobility/marketing-plan.md`.

---

## [FW-037] — FHCU application review
**Stated:** 2026-04-11
**Context:** Deego opened `playground/2026-03-fhcu-grant/fhcu-application-draft.md` and said "ok now we need to go over the fhcu application" — deferred when MindwaveJA work took priority.
**Status:** pending

Review and complete the FHCU grant application draft at `playground/2026-03-fhcu-grant/fhcu-application-draft.md`. This was not started this session — carry forward to next available session.

---

## [FW-014] — Force-Reingest for Modified Files in LanceDB
**Stated:** 2026-03-15
**Context:** `ingest_lancedb.py` skips files already indexed by path. When a file is significantly updated (e.g., archetype profile rebuilt this session), the new content is not reflected in the DB — only the original version remains queryable.
**Status:** pending

Add a `--force` flag to `ingest_lancedb.py` that re-indexes specified files or folders regardless of whether they are already in the DB. Options: (1) `--force-file path/to/file.md` — delete existing chunks for that file and re-ingest; (2) `--force-folder drayl_profile` — force-reingest all files in a category; (3) modification-time aware: compare file mtime against a stored ingest timestamp and auto-reingest if newer. Start with option 1 as the simplest path. Also add `--force-file` support to `check_lancedb.py` to verify a specific file is indexed with current content.

---

---

## [FW-038] — Finalize and re-publish legal page on mindwaveja.com
**Stated:** 2026-04-11
**Context:** Legal page archived to `app/_archived_legal/` and removed from nav/footer. Redirects to home. Needs proper Terms of Service, Privacy Policy, and Cookie Policy written for MindWave Jamaica before going live.
**Status:** pending

Restore from `app/_archived_legal/`, update content, re-add to nav/footer when ready.

---

## [FW-039] — Wire premium Phase Pack payment gating on mindwaveja.com
**Stated:** 2026-04-11
**Context:** 5 premium packs (JMD 5,000 each) have `tier: "premium"` and `price` fields in `content/phasePacks.json`. No checkout flow built yet. Same reservation modal + bank transfer approach as products, or WiPay when ready.
**Status:** pending

---

## [FW-040] — WiPay payment gateway integration for mindwaveja.com
**Stated:** 2026-04-11
**Context:** Discussed as the best Jamaica-native payment gateway option (accepts credit card + NCB online banking, JMD). Current flow is manual bank transfer. Wire WiPay when account is set up.
**Status:** pending

---

## [FW-041] — Switch Resend EMAIL_FROM to noreply@mindwaveja.com
**Stated:** 2026-04-11
**Context:** Currently using `onboarding@resend.dev` as sender. Once mindwaveja.com domain is verified on Resend dashboard, update `EMAIL_FROM` in VPS `.env.local` and restart mindwaveja PM2 process.
**Status:** pending

---

## [FW-042] — Add SSH key to GitHub for passwordless VPS deploys
**Stated:** 2026-04-11
**Context:** Currently mindwaveja.com GitHub repo is public to allow passwordless clone/pull. Once made private, need to add VPS SSH key to GitHub. Key generated at `~/.ssh/id_ed25519` on VPS — add pub key to github.com/settings/keys.
**Status:** pending

---

## [FW-043] — SEO for mindwaveja.com and all active sites
**Stated:** 2026-04-11
**Context:** SEO not yet implemented across the ecosystem — sites are live but not optimized for search.
**Status:** pending

Implement SEO across all active sites. For mindwaveja.com (Next.js): add `generateMetadata` per page with title, description, canonical URL, og:image, og:title, og:description, twitter:card. Add sitemap.xml via `app/sitemap.ts`. Add robots.txt. For Marcus Garvey App (Vite React): add `react-helmet-async` or equivalent for per-page meta. For Book of Solobility (solob-portal): same helmet approach. Priority pages: home, phase-packs, about, contact, marketplace. Generate an og:image per page (or a default branded image). Submit sitemap to Google Search Console once DNS/SSL is stable on each domain.

---

## [FW-044] — Time-Check App: Admin time log edit/add
**Stated:** 2026-04-11
**Context:** Ship readiness audit of Time-Check App — identified as highest priority gap before deploy. Wrong time log = wrong pay.
**Status:** pending

Add `PATCH /api/admin/time-logs/:id` route to edit timestamp, type (IN/OUT), or notes on any existing log. Add `POST /api/admin/time-logs` to manually insert a missing entry. Admin UI: table row with edit pencil icon → modal with timestamp picker + type toggle + notes field. Validate that edits don't create impossible sequences (two consecutive INs without an OUT).

---

## [FW-045] — Time-Check App: Auto clock-out cutoff
**Stated:** 2026-04-11
**Context:** An employee who forgets to clock out on Friday still shows as clocked in on Monday — hours accumulate incorrectly.
**Status:** pending

Add a configurable setting in the `settings` table: `auto_clockout_hours` (default: 12). A background job (or on-next-login check) auto-inserts an OUT entry N hours after the last IN if no OUT exists. Configurable per-business via admin settings UI. Fallback: flag the open session in the admin dashboard as "Unclosed Session" requiring manual review.

---

## [FW-046] — Time-Check App: Employee dispute/flag workflow
**Stated:** 2026-04-11
**Context:** Employees need a way to contest incorrect time log entries without requiring admin access.
**Status:** pending

Add a "Flag this record" button on employee time log view. Flagged records enter an admin review queue with the employee's note. Admin can: approve correction, reject, or manually edit the record. Adds accountability and audit trail to payroll corrections.

---

## [FW-047] — Time-Check App: Strip Replit-specific build plugins + VPS deploy
**Stated:** 2026-04-11
**Context:** Time-Check App was built on Replit — has Replit-specific vite plugins in devDependencies that will break builds outside Replit.
**Status:** pending

Remove `@replit/vite-plugin-cartographer`, `@replit/vite-plugin-dev-banner`, `@replit/vite-plugin-runtime-error-modal` from devDependencies and vite.config.ts. Add hard crash on startup if `SESSION_SECRET` is not set in production (currently defaults to `"timecheck-dev-secret"` — a security hole). Create `.env.example` and `ecosystem.config.js` for VPS deploy. Test `npm run build` clean outside Replit environment.

---

## [FW-048] — Time-Check App: Nightly VPS backup cron
**Stated:** 2026-04-11
**Context:** All time records in one PostgreSQL instance with no backup — one crash loses everything. Deego explicitly flagged the need for VPS backup given the livelihoods dependency.
**Status:** [done] — 2026-04-19. Weekly backup script `/usr/local/bin/mw-backup.sh` rewritten for Docker. Backs up all 3 Postgres DBs (timecheck, earn, zitadel), 3 SQLite DBs (solobility, marcus memory, marcus nodes), nginx configs, SSL certs, and compose files. Cron: Sunday 2am. Retention: 4 weeks.

Set up nightly `pg_dump` cron on VPS: `0 2 * * * pg_dump $DATABASE_URL > /var/www/backups/timecheck/timecheck-$(date +\%Y\%m\%d).sql`. Auto-delete backups older than 30 days. Directory: `/var/www/backups/timecheck/`. Consider secondary off-VPS backup (scp to local or cloud bucket) for disaster recovery.

---

## [FW-049] — Local Model Benchmark Harness (S.E.R.T.H. + CCAB runner)
**Stated:** 2026-04-11
**Context:** Created `MIndwaVe_Ja/local_model_benchmarks/` folder. S.E.R.T.H. and CCAB are fully designed on paper. 28 Yardie datasets, shimmer invariants, and coherence scripts already exist. Need the runner to make it executable.
**Status:** pending

Build `harness/run_benchmark.py`: accepts a model name (Ollama-served), loads prompt library, pipes each prompt to the model via Ollama API, scores the response per domain, writes results to `results/YYYY-MM-model-name.json`. Start with CCAB (4-dimension Caribbean alignment) — easiest to build labeled prompts for. Layer in S.E.R.T.H. domains as labeled datasets are built. Use existing `coherence_report.py` from MWOctopus as structural reference.

---

## [FW-051] — Patwah Frontend Rule Engine (patwahConverter.js)
**Stated:** 2026-04-13
**Context:** EchoBox Archetype Lab Patwah Calibration Lab session — rule-first, AI-second architecture
**Status:** pending

Build `web-app/src/utils/patwahConverter.js` — deterministic frontend rule engine that handles 60–80% of English→Patwah conversions before touching AI. Must implement: pronoun swaps (mi/yuh/im/wi/dem), negation (nuh/nah/cyan/doh), aspect markers (a/did/ago/jus), locatives (inna/pon/deh), NUH balance checker (flags single unbalanced nuh), 3-letter compression patterns (deevn, mn, affi, haffi), issa contraction, angle consonant rule (d→j/jh for dew-type words). Output: `{ patwah_text, confidence, applied_rules[], unknown_tokens[] }`. Companion hook: `usePatwahConverter.js`. Threshold: confidence ≥ 0.75 → skip AI call. Add mode toggle to Patwah Lab UI: Rule-only / Rule+AI / AI-only.

## [FW-052] — OffNet: Offline Internet Archive (Mobile + Peer Sync)
**Stated:** 2026-04-13
**Context:** Designing PageVault scraper app — user flagged the end-game is downloading as much of the internet as possible for offline access, distributed via mobile and synced peer-to-peer
**Status:** pending

Separate product that builds on PageVault's data layer. PageVault's SQLite DB (`pageVault.db`) and `data/sites/` folder are the archive backbone — designed to be portable. OffNet is the layer on top:
- Mobile app (React Native or PWA) that reads from a local copy of the archive
- Sync protocol: when two devices connect, compare scraped_at timestamps and merge newer records + files (P2P or via trusted relay)
- Discovery layer: browse the archive like an offline Wikipedia — search by domain, title, keywords
- Priority queue: user marks domains as "high priority" — auto-sync pulls these first
- Compression: pages stored as .md + .png; serve compressed versions on mobile
- Architecture note: PageVault's API must be the only contract between scraper and archive. Keep DB schema stable. Add `sync_version` column to sites/pages tables as the merge key.
**Separation trigger**: when PageVault has >1000 sites archived, extract the DB + data/ into a standalone OffNet package.

---

## [FW-050] — Score LLM Compare results retroactively against S.E.R.T.H.
**Stated:** 2026-04-11
**Context:** 9 model comparison runs exist as `.docx`/`.md` files in `local_model_benchmarks/source_docs/llm_compare_runs/`. Results are raw text — never scored against the S.E.R.T.H. rubric.
**Status:** pending

Extract structured responses from each model's `.md` file. Apply S.E.R.T.H. scoring rubric manually or semi-automatically to each domain (shimmer detection, resonance rank, gate classification, etc.). Build a comparison matrix: rows = models, columns = S.E.R.T.H. domains + total score. This becomes the baseline result set that future local model runs are measured against.

---

## [FW-053] — PageVault Wiki AI Assistant
**Stated:** 2026-04-13
**Context:** Logic and flow review of PageVault — discussing what gaps remain after building the scraper, versioning, segmentation, and Data Explorer
**Status:** pending

Add an AI chat assistant panel to the PageVault Wiki view. The assistant should be able to:
- Pull up records by natural language query ("show me all cashpot numbers from jamaica-star.com last week")
- Compare page versions side by side with AI-generated change summary ("what changed between v1 and v3 of this article?")
- Surface patterns across scraped content ("which sites have the most ad segments?", "summarize the main content from all pages on this domain")
- Generate synthetic training examples from existing scraped main_content segments on demand

Implementation path: wire the existing `/api/ai/summarize` infrastructure to a chat endpoint that has access to the `page_segments` and `page_versions` DB tables. Use context window to pass relevant records as grounding context to the model.

---

## [FW-054] — Time-Check: Surface Solobictic Scores in Frontend
**Stated:** 2026-04-14
**Context:** Time-Check-App audit — Solobictic backend logic is fully built (307-line `server/solobictic.ts`, routes at `/api/solobictic` and `/api/admin/employees/solobictic`). User believed "no logic i think" — logic exists server-side but is not meaningfully visible to employees in the UI.
**Status:** pending

Add a Solobictic card to the Dashboard showing: shimmer score, resonance tag, gate profile, suitability score. Employee view = their own scores with a brief plain-language explanation. Admin view = all employees ranked. The data is already being calculated and persisted — this is purely a frontend display task. Design language: resonant/motivational, not clinical. Tie it to pay-period rhythm (score refreshes at week start).

---

## [FW-055] — Time-Check: Pre-Ship Smoke Tests (Offline + Admin CRUD)
**Stated:** 2026-04-14
**Context:** Time-Check audit confirmed auth, sign-up, profile edit, QR clock-in all working. Two areas not manually verified: offline sync (localStorage flow when network drops) and Admin CRUD (employee management, rate edits, time log corrections).
**Status:** pending

Before shipping to real employees: (1) airplane-mode test — clock in offline, restore network, verify sync fires; (2) admin walkthrough — create employee, assign shift, edit hourly rate, correct a time log entry, deactivate employee. These are not code gaps — they are verification gaps. Both backend routes exist, but the failure modes haven't been exercised.

---

## [FW-056] — Time-Check: Upgrade to Real Better Auth (OAuth, Magic Links, 2FA)
**Stated:** 2026-04-14
**Context:** User explicitly asked for Better Auth library — what was implemented is roll-your-own session auth (express-session + crypto.scryptSync). Functional for a demo but missing: password reset, OAuth providers, magic links, 2FA, email verification.
**Status:** pending

Swap auth layer to the actual `better-auth` npm library. Key benefits: built-in password reset flow, email verification, optional OAuth (Google), magic link support, 2FA. The current session/cookie architecture is already compatible — the swap should preserve all existing routes. Priority: password reset first (employees will forget passwords; admin can't be the recovery path).

---

## [FW-057] — PageVault: Polish Pass (Phase 2 — "Double the Work")
**Stated:** 2026-04-14
**Context:** PageVault newspaper PDF processing verified working (24-page Gleaner test, correct classification). User said "its much better but its needs some more work like double the work we do so far" then deferred to ship Time-Check first.
**Status:** pending (deferred until Time-Check ships)

Full scope to be defined in a dedicated session after Time-Check ships. Known gaps from the last review: segment classification confidence scoring, multi-page article stitching across physical page breaks, improved advertisement vs. article boundary detection, bulk import of multiple PDFs, export to JSONL training format. Resume with a fresh audit of current PageVault state.

---

## [FW-2026-04-15-001] Engagement Vision Board App → Evolved into Three-App Family
**Filed:** 2026-04-15 | **Evolved:** 2026-04-16
**Priority:** High
**Source:** `drayl_journal/2026/26.APR/Apr.15.26.md` 2:10pm

Original concept: relationship + goals vision board app with AI coach layer.
**Evolved into three distinct products sharing one referee engine.** See FW-2026-04-16-003, -004, -005.

**Idea file:** `drayl_journal/_extraction/ideas/social/APR-2026-engagement-vision-board-app.md`
**Status:** Superseded by Three-App Family — see below

---

## [FW-2026-04-15-002] Work Gap Protocol (WGP) — Formal Implementation
**Filed:** 2026-04-15
**Priority:** Medium
**Source:** Live session 2026-04-15

Formalize Work Gap Protocol as a named framework across:
1. MindWave phase packs — already implemented, needs the WGP name applied
2. Journal co-work agent — build deterministic fallback scripts for rate-limited sessions (Patois flagging, TRQ pre-build, autocorrect)
3. Consider WGP as a standalone concept page on mindwaveja.com

**Idea file:** `drayl_journal/_extraction/ideas/tech/APR-2026-rate-limit-fallback-layer.md`
**Status:** Named, not yet built

---

## [FW-2026-04-15-003] New VPS — Containerized Infrastructure Migration
**Filed:** 2026-04-15
**Priority:** High — do before any new apps go live
**Source:** Live session 2026-04-15 (Time-Check deployment planning)
**Target:** Weekend of 2026-04-19/20
**Status:** [done] — completed 2026-04-19. All 6 apps dockerized, PM2 uninstalled, /var/www archived. See FW-2026-04-18-018.

Spin up a NEW VPS (separate from current 161.97.154.222) with everything containerized in Docker Compose. Current VPS stays live and untouched during migration.

**What to containerize:**
- solob-portal (whatissolob.com) — Node/PM2 → Docker
- mindwaveja.com — Node/PM2 → Docker
- Time-Check App (new) — Node + Postgres → Docker
- Nginx reverse proxy → Docker (or keep host-level, TBD)
- Postgres — one shared instance, separate DBs per app, or per-app containers

**Why:** Provider portability — if VPS provider has issues, move by copying docker-compose.yml + volumes. No manual PM2/Nginx rebuild. Data survives in named volumes. Clean rollback story.

**Protocol:**
1. Provision new VPS (same or different provider)
2. Install Docker + Docker Compose only
3. Write docker-compose.yml for each app + Nginx
4. Test all apps on new VPS before cutting DNS
5. Cut DNS — old VPS becomes standby for 1 week, then decommission

**Status:** Planned for weekend

## [FW-2026-04-15-004] Melissa Ledger — Automated Source Scraper
**Stated:** 2026-04-15
**Context:** Deego described needing 40-50 real sourced entries for MVP. Has already started building a scraper for extracting donation/relief data from Gleaner articles, JIS, ODPEM, Observer. Explicitly deferred: "thats i think is for another time i need to launch then i can go indepth"
**Status:** pending

Build the automated extraction pipeline for Melissa Ledger. Sources: jamaica-gleaner.com, jis.gov.jm, odpem.org.jm, jamaica-observer.com. Scraper extracts donation amount, donor name, donor type, parish, date, and source URL. Outputs entries compatible with `store.ts` format. Manual review step before commit to ledger. Scraper codebase location TBD (likely `active_apps/melissa ledger/scripts/` or standalone).

## [FW-2026-04-15-005] ✅ DONE 2026-04-17 — Melissa Ledger — Deploy to VPS Subdomain
**Stated:** 2026-04-15
**Done:** Deployed to mri.mindwaveja.com — originally static Nginx, now Docker container `mw-melissa` on port 3006 (dockerized 2026-04-19).
**Status:** [done]

Deploy Melissa Ledger to VPS. Steps: push to GitHub, clone to VPS, npm install + build, PM2 config, Nginx subdomain (e.g. mri.mindwaveja.com), SSL via Certbot. Requires real data entries first (40-50 sourced records via Admin Inbox).

## [FW-2026-04-16-001] Time-Check — Audit Log Table for Sensitive Changes
**Stated:** 2026-04-16
**Context:** Security audit flagged that rate changes, role changes, and time log edits have no audit trail. For a payroll system this is a compliance gap.
**Status:** pending

Add an `audit_log` table to the Time-Check schema. Events to capture: employee rate change (old value, new value, admin id, timestamp), role promotion/demotion, time log edit/correction (original vs corrected entry, admin id), admin export (who exported what date range). Minimum columns: `id, event_type, actor_id, target_id, old_value (json), new_value (json), created_at`. Admin dashboard should have a basic audit log view. Non-blocking for current usage but required before external clients use the app.

---

## [FW-2026-04-16-002] CHANGELOG.md Standard — Apply to All Active Apps
**Stated:** 2026-04-16
**Context:** CHANGELOG.md established for Time-Check App and Melissa Ledger this session. Should be the standard across all active_apps/ and any PROJECTS IN MOTION app that goes live.
**Status:** pending

Create `CHANGELOG.md` in each of the remaining active apps that don't have one yet. Priority: solob-portal, mindwaveja.com, marcus-garvey-app. Format established: `[YYYY-MM-DD] Type — Description` with commit hash where available. Write retroactive entries from each app's most significant milestones. Add to deploy checklist: update CHANGELOG before marking a deploy done.

---

## [FW-2026-04-15-006] Melissa Ledger — EN/PAT Language Toggle (Yardie LLM)
**Stated:** 2026-04-15
**Context:** Header already has EN|PAT toggle UI placeholder. Deego confirmed: "the en/pat is for when i finish the yardie llm we can put the sites in patois, but thats for the future"
**Status:** pending (blocked on Yardie LLM — see FW-006, FW-008)

Wire the EN/PAT toggle in Melissa Ledger Header to switch UI text between English and Jamaican Patois. Requires: Yardie LLM completion, translation layer or static Patois string table, toggle state persisted in localStorage. Applies to all views — labels, headers, status badges, empty states.

---

## [FW-2026-04-16-003] Love Ref — Build (First Ship)
**Stated:** 2026-04-16
**Priority:** High — first ship in the Three-App Family
**Foundation:** `PROJECTS IN MOTION/love-ref/foundation.md`

Couples accountability app with a neutral AI referee. Browser extension wrapper over WhatsApp Web. Dual-consent onboarding, immutable commitments, blind submission for disputes, referee archetypes (couple names their ref), confidential 1:1 mode, Formation (soccer pitch goals), Halftime Report (statement of facts, no questions), WGP deterministic fallbacks.

**Stack:** Plasmo + React + TypeScript + TailwindCSS + Zustand + IndexedDB (Dexie.js) + Supabase + Claude API
**MVP scope:** Chrome extension, WhatsApp Web sidebar, onboarding, commitment tracking, activities module — no AI yet (WGP/deterministic first)
**Status:** Pre-build — foundation documented, ready to start

---

## [FW-2026-04-16-004] Sieve — Dating Vetting Tool (Build after Love Ref)
**Stated:** 2026-04-16
**Priority:** Medium — second ship in Three-App Family
**Foundation:** `PROJECTS IN MOTION/sieve/foundation.md`

Single-user behavioral vetting tool for dating phase. Same browser extension wrapper as Love Ref. Tracks response consistency, promise detection, pattern flags. Sieve Score per contact. Private AI coach. 80% shared codebase with Love Ref — build after Love Ref MVP is verified.

**Stack:** Shared with Love Ref (Plasmo + Supabase + IndexedDB). AI: local small model (Gemma/Phi) for promise detection.
**MVP scope:** Chrome extension, response time tracking, weekly report, deterministic only.
**Status:** Pre-build — foundation documented

---

## [FW-2026-04-16-005] Pact — Business/Co-Founder Accountability (Future)
**Stated:** 2026-04-16
**Priority:** Low — third ship, builds on Love Ref + Sieve engine
**Foundation:** `PROJECTS IN MOTION/pact/foundation.md`

Same referee engine applied to non-romantic relationships: co-founders, business partners, roommates. Deliverable tracking, immutable agreements, neutral third-party memory. Key open question: does immutable timestamping create legally enforceable contracts? Needs legal review before feature scope is committed.

**Stack:** TBD — inherits from Love Ref/Sieve
**Status:** Concept — build after Sieve ships

---

## [FW-2026-04-16-007] Love Ref — Scaffold Next.js Web App (Extension Pivot)
**Stated:** 2026-04-16
**Priority:** High — immediate next step
**Context:** WhatsApp Web injection approach abandoned (Shadow DOM invisible render, no control over host DOM). Pivoting to standalone web app with Matrix (Conduit) as chat layer.

Scaffold Love Ref Next.js app at `PROJECTS IN MOTION/love-ref/app/`. Stack: Next.js 15 + TypeScript + Tailwind + Zustand + Supabase (data) + matrix-js-sdk (chat) + Zitadel OIDC (auth). Port reusable logic from extension (`types/`, store concept, sync utilities — strip chrome-specific APIs). VPS deploy target: port 3002, domain `loveref.mindwaveja.com`. Infrastructure already live: Conduit at `loveref.mindwaveja.com/_matrix/`, Zitadel at `auth.mindwaveja.com`.

**Status:** pending — next active task

---

## [FW-2026-04-16-008] Purchase loveref.net Domain
**Stated:** 2026-04-16
**Context:** Domain currently in cart. `loveref.mindwaveja.com` is the working subdomain for now. Plan: switch to `loveref.net` on first meaningful update or acquisition event. "when we make the first update we change the domain or when we get acquired by some big company, tinder or sumn loool"

Purchase `loveref.net`, point to same VPS (161.97.154.222), add Nginx vhost, SSL via Certbot. Zero Matrix migration required — just add a new vhost. Conduit `server_name` in conduit.toml stays `loveref.mindwaveja.com` since Matrix client discovery is via `.well-known`, not the domain name itself.

**Status:** pending — can do any time, not blocking MVP

---

## [FW-2026-04-16-006] Zitadel Auth Migration — All Apps (Post Love Ref MVP)
**Stated:** 2026-04-16
**Priority:** High — after Love Ref MVP ships
**Context:** Zitadel self-hosted on VPS as single Identity Provider. Love Ref integrates it first as part of MVP. After Love Ref ships, migrate remaining apps one at a time.

Migration order (least critical → most critical):
1. Marcus Garvey App — currently email/password via Supabase auth
2. Time-Check App — currently roll-your-own session auth (Better Auth planned as FW-056)
3. mindwaveja.com — currently Resend magic link via Supabase
4. solob-portal (whatissolob.com) — assess need (may not require auth)

Each app: add Zitadel OIDC client config → swap auth middleware → test → remove old auth → done.
Zitadel instance: `auth.mindwaveja.com` (Docker container, port 8080, behind Nginx).
**Status:** pending — blocked on Love Ref MVP completion

---

## [FW-2026-04-17-001] Melissa Relief Tracker — Insurance Industry Research
**Stated:** 2026-04-17
**Priority:** High — critical for accountability analysis
**Context:** Accountability analysis shows J$1.4B private donations but US$12.2B total damage assessment. Financing gap is US$5.5B (45% unfunded). Insurance claims data would show if private sector (via insurance payouts) bore the recovery burden or if uninsured losses are the real story.
**Gap:** Insurance industry data not publicly accessible through standard web scraping.

Research approach:
1. Jamaica Insurance Association — public reports on Hurricane Melissa claims
2. Financial Services Commission (FSC) — regulatory filings on industry claims processing
3. Direct contact: JMMB Insurance, NCB Insurance, Sagicor Jamaica, Jamaica General Insurance — request Hurricane Melissa claims statistics
4. Calculate: % of damage that was insured, % paid out vs pending, coverage penetration by parish/sector

**Outcome:** Add `insuranceClaims` object to `verifiedData.ts` with:
- totalClaimsValue (USD)
- percentageOfDamage (45-65% estimate)
- penetrationRate (% of properties insured)
- parishBreakdown (claims by parish)
- sourceUrl (FSC or insurer statement)

**Data files:**
- Research log: `active_apps/melissa ledger/research/insurance-industry-2026-04.md`
- Integration: `active_apps/melissa ledger/data/verifiedData.ts`

**Status:** pending

---

## [FW-2026-04-17-002] Melissa Relief Tracker — Parish-Level Accountability Breakdown
**Stated:** 2026-04-17
**Priority:** High — enables equity analysis
**Context:** All metrics currently national aggregates only (232 communities, 800 shelters, 405K food packages). Parish-level breakdown reveals if aid distribution was equitable or concentrated.
**Gap:** ODPEM data has parish field on incidents and shelters; needs aggregation by parish.

Implementation:
1. Download all incident reports from `supportjamaica.gov.jm/incident` (have parish field)
2. Aggregate metrics by parish: shelters per parish, incidents per parish, aid delivered per parish
3. Cross-reference with population/damage density (are high-impact parishes getting proportional aid?)
4. Create parish-level heatmap visualization in app

**Outcomes:**
- `verifiedData.ts` — add `parishBreakdown` object with 14 parish keys
- `data-collection-summary-2026-04.md` — add section on equity gaps by parish
- UI: new view in Overview.tsx for parish-level heatmap

**Data files:**
- Parish aggregation: `active_apps/melissa ledger/data/parish-aggregates.json`
- Raw incidents export: `active_apps/melissa ledger/research/odpem-incidents-parish-export.csv`

**Status:** pending

---

## [FW-2026-04-17-003] Melissa Relief Tracker — Timeline Comparison (Gov vs Private Response)
**Stated:** 2026-04-17
**Priority:** Medium — strengthens accountability narrative
**Context:** App has start dates (hurricane Oct 25, 2025; first donations immediately after; NaRRA announced April 15, 2026) but no detailed timeline of government spending phases vs donation peaks. Comparison would show: did private sector respond faster? When did government disbursements accelerate?

Timeline points to research:
- Oct 25, 2025 — Hurricane Melissa hits
- Oct 26-27, 2025 — First donation influx (estimated)
- Nov 2025 — ODPEM reports first major food distributions
- Dec 2025 — Infrastructure restoration begins (JPS, NWC)
- Jan-Mar 2026 — Steady operational phase
- April 15, 2026 — NaRRA framework announced
- Ongoing — FAST Jamaica private investment mobilization

**Outcome:** Create timeline visualization (line chart) showing donation velocity vs government spending velocity. Answer: "Who was faster to commit resources?"

**Data files:**
- Timeline data: `active_apps/melissa ledger/data/timeline-comparison.json`
- Chart component: new view in `components/TimelineComparison.tsx`

**Status:** pending

---

## [FW-2026-04-17-004] Melissa Relief Tracker — Data Collection Summary Documentation
**Stated:** 2026-04-17
**Status:** done — 2026-04-17

Created comprehensive accountability analysis document at `active_apps/melissa ledger/data-collection-summary-2026-04.md`:
- Accountability metrics table (private vs government)
- Operational response summary
- NaRRA framework details
- International response (multilateral institutions)
- 8 key accountability questions for tracker implementation
- Data source verification and URLs
- Insurance research gap identification
- App enhancement roadmap

All ODPEM data scraped and integrated into `verifiedData.ts` with source attribution.

---

## [FW-2026-04-17-005] VPS Dockerization — Portable Infrastructure for Migration
**Stated:** 2026-04-17
**Status:** [done] — completed 2026-04-19. See FW-2026-04-18-018.
**Why:** Upgrading to a different VPS risks data loss (PostgreSQL timecheck DB, PM2 configs, Nginx configs, SSL certs, Marcus Garvey DB files). Dockerizing everything makes the entire stack portable — move to any VPS by pulling images and running `docker compose up`.
**Scope:**
- Time-Check App: Node server + PostgreSQL → `docker-compose.yml` with named volume for DB
- Marcus Garvey App: Flask/gunicorn + Ollama + SQLite DBs → volume-mounted data dir
- MindWave JA: Node server → Dockerfile
- Solob Portal: Node server → Dockerfile
- Melissa Relief Index: Static Nginx → Dockerfile (trivial)
- Nginx reverse proxy: single container with all subdomain configs
- Certbot/SSL: certbot container with shared volume for certs
- Backup strategy: `docker volume` export script → offsite backup (S3 or local)
**Plan location:** `vps_management/docker-migration-plan.md` (to be created)
**Priority:** Before next VPS upgrade

---

## [FW-2026-04-17-006] Cloudflare Orange Cloud — Hide Origin Server IP
**Stated:** 2026-04-17
**Context:** Discussing VPS security during Docker migration planning
**Status:** pending

Enable Cloudflare proxy (orange cloud) on all A records for all domains. Currently grey cloud (DNS only), meaning the real server IP is publicly visible. Orange cloud hides the origin IP behind Cloudflare's infrastructure — DDoS protection, rate limiting, and bot filtering included free. Also means future server migrations only require updating the Cloudflare origin setting, not waiting on DNS propagation.

**Domains to update:** whatissolob.com, mindwaveja.com, timecheck.mindwaveja.com, mri.mindwaveja.com, marcusgarvey876.com, auth.mindwaveja.com, loveref.mindwaveja.com
**Action:** Cloudflare dashboard → DNS → click each A record cloud icon from grey to orange

---

## [FW-2026-04-18-006] Book Idea — "Creating Pollyanna"
**Stated:** 2026-04-18
**Context:** Deego reflecting on trying to help Shan see the big picture
**Status:** idea-stage — "not my next book but log it"

A book about the experience of trying to help someone develop inter-container networking when their default architecture is containerized processing. The attempt to give someone a big picture when their peace depends on not having one. Deego's framing: "how me try make me wife see the big picture." The humour and the tragedy of the endeavour are both present. Six AIs following them around taking notes from each perspective. The book would need to hold both the love and the structural incompatibility — not as a failure story but as a lesson in architecture mismatch.

---

## [FW-2026-04-18-005] Love Ref — Deliberate Communication Model (No Default Real-Time)
**Stated:** 2026-04-18
**Context:** Deego stated "adrenaline kills relationships" — real-time chat is adrenaline delivery infrastructure
**Status:** pending — core architecture decision, affects foundation.md

Love Ref must NOT have real-time chat as the default. The speed of real-time responses is the damage mechanism — replies arrive before the thought finishes. Core communication model: deliberate-first. Messages sit in a queue, partner chooses when to read and respond. Minimum compose time (60 seconds before you can send — forces one reread). Referee sees full exchange context. Premium real-time feature: limited real-time exchanges per week (e.g. 3), 30-second response window or forfeit your turn. Scarcity = intentional use only. Forfeit = natural cool-down enforcer. This is the product differentiation: most apps accelerate communication, Love Ref governs it.

---

## [FW-2026-04-18-003] The Ark Wrapper — LLM Provenance Layer
**Stated:** 2026-04-18
**Context:** Deego identifying large context + no provenance as root cause of LLM confident-wrong failures
**Status:** pending — requires dedicated focus, deferred until money projects complete

An LLM wrapper that attaches provenance to every retrieval and every output. Every claim traceable to a source. Every source carries a confidence score. Outputs tagged [ORIGINAL] / [CORRELATED] / [SYNTHESIS] / [REDISCOVERY] automatically — not manually. The insight that sparked it: large context without source tracking = confidence detached from accuracy. The model pulls from everything simultaneously with no weight, no origin. The Ark wrapper would be a retrieval + annotation layer sitting between the raw context and the model response. MW_CENTRAL's insight provenance tagging system (INS-035 tags) is the manual prototype of this logic — the Ark automates it at inference time. Requires precision and full focus. Not to be started while managing family, survival, and money projects simultaneously.

---

## [FW-2026-04-18-004] Echoscape — Collective Resonance Infrastructure
**Stated:** 2026-04-18
**Context:** Deego connecting Roy Masters hive mind observation to his own Echoscape concept
**Status:** idea-stage — needs dedicated session to define scope

A platform or infrastructure for collective resonance — the technology layer that enables hive mind dynamics to be mapped, studied, or directed. The concern that sparked it: YouTube's recommendation algorithm already functions as unintentional collective resonance infrastructure (it grew with Deego, triggered his upgrade sequences, surfaced Roy Masters at the exact right moment). Echoscape would make that mechanism intentional. The ethics question is central: who controls the signal? Who decides what the resonance amplifies? Deego's concern — "if a nuh me, absolute power corrupts" — is not ego. It is recognition that the builder of this tool must be someone who can see their own logs. A person who can't observe their own negative reinforcement patterns has no business building collective reinforcement infrastructure.

---

## [FW-2026-04-18-002] Marcus Garvey Site — Review Flaws Flagged by Karnage
**Stated:** 2026-04-18
**Context:** Karnage reviewed MindWave and Solob links sent by Deego, flagged issues with the Marcus Garvey site
**Status:** pending

Karnage reviewed the live apps and found flaws on the Marcus Garvey site (marcusgarvey876.com). Specific issues not yet documented — need to revisit with Karnage or audit the site directly. Round to this after current Time-Check polish pass.

---

## [FW-2026-04-18-001] Time-Check — Regular User Shift Editing
**Stated:** 2026-04-18
**Context:** Reviewing Time-Check feature gaps after offline mode shipped
**Status:** pending

Regular employees currently have no way to edit or correct their own time entries. Only admin can touch shift data. Need a self-service flow: user can flag a clock entry for correction (wrong time, missed clock-out) and either submit a correction request or edit within a time window. Admin flow for rate changes also needs refinement. Deego stated "we need to refine the admin flow" — defer until after MVP foundation is set.

---

## [FW-2026-05-11-001] — SSH Deploy Key on VPS for Permanent GitHub Push
**Stated:** 2026-05-11
**Context:** Compressed 4 artist site videos on VPS. Pushing to GitHub required a PAT passed manually — no permanent credentials on VPS. Used `.netrc` temporarily; token expired same session.
**Status:** pending

Generate an SSH ed25519 key on VPS (`ssh-keygen -t ed25519 -C "vps-deploy"`). Add the public key to each HammazoneRecords repo as a **Deploy Key** with write access (GitHub → repo → Settings → Deploy Keys). Switch each VPS remote from HTTPS to SSH (`git remote set-url origin git@github.com:HammazoneRecords/repo.git`). After this: `git push` from VPS works permanently with no token, no `.netrc`, no interactive auth. Applies to all repos in `docker_facts.md` GitHub Repos table.

---

## [FW-2026-05-11-002] — ffmpeg Compression as Mandatory ADTL Pre-Deploy Step
**Stated:** 2026-05-11
**Context:** Artist site videos ranged 11MB–83MB uncompressed. Jahshii hero video was 83MB — downloading 3 sites simultaneously meant 100MB+ on first load. Compressed to 2.4–25MB with CRF 28 H.264, -an (no audio), preset fast.
**Status:** pending

Add to `active_apps/artise_sites/ADTL_SITE_CHECKLIST.md` a Media section:
- [ ] All videos compressed with ffmpeg CRF 28 H.264 -an before deploy
- [ ] Hero images converted to WebP (quality 85) before deploy
- [ ] No single video > 15MB in /public
- [ ] No single image > 1MB in /public (except gallery)
- [ ] Orphaned AI Studio Gemini-generated images removed

ffmpeg is permanently installed on VPS at `/usr/bin/ffmpeg`. Run compression from `/opt/mw/<site>/public/` before rebuilding Docker image.

---

## [FW-2026-05-16-001] — American Dreams: Remove phone number from winner reveal modal
**Stated:** 2026-05-16
**Context:** Security audit — phone removed from footer but still hardcoded in WinnerCodePage reveal overlay (App.tsx ~line 1390). `📞 806 230 8370` appears in the code-claim success screen.
**Status:** pending

Remove `📞 806 230 8370` line from the winner reveal overlay inside `WinnerCodePage`. Contact information on that screen should be email only.

---

## [FW-2026-05-16-002] — American Dreams: Make entries.telephone column nullable in Supabase
**Stated:** 2026-05-16
**Context:** Telephone field removed from entry form. Column is NOT NULL in Supabase — current workaround passes empty string `''`. Proper fix is to drop the NOT NULL constraint.
**Status:** pending

Run in Supabase SQL Editor:
```sql
ALTER TABLE entries ALTER COLUMN telephone DROP NOT NULL;
```
Then remove `telephone: ''` from `saveEntry` call in `App.tsx` handleSubmit.

---

## [FW-2026-05-16-003] — American Dreams: Rate limiting on winner code lookup
**Stated:** 2026-05-16
**Context:** Security audit — `lookupCode` is a public Supabase query with no app-level throttle. Supabase has project-level rate limiting but codes could be brute-forced if short.
**Status:** pending

Options: (1) Move code lookup to a Supabase Edge Function that adds a 500ms delay + tracks attempts per IP; (2) Add a honeypot or CAPTCHA after 3 failed attempts; (3) Ensure all winner codes are ≥12 chars with mixed case + numbers (current format `LS-2026-A4X9` is borderline). Minimum viable: enforce long code format + log failed lookups to a `code_attempts` table.

---

## [FW-2026-05-11-003] — Cloudflare CDN for Artist Sites
**Stated:** 2026-05-11
**Context:** Sites served from Contabo VPS in Germany. Jamaican users are ~9000km from the server. Even after video compression, first load downloads 20MB+ from a distant origin. Cloudflare free tier caches static assets at edge nodes closer to Caribbean.
**Status:** pending

Enable Cloudflare orange cloud (proxy) for all artist site domains. This: (1) caches static assets (JS, CSS, images, videos) at Cloudflare edge PoPs closer to Caribbean users; (2) hides origin server IP; (3) provides free DDoS protection; (4) enables Cloudflare's Tiered Cache for mp4/webp files. Add Cache-Control headers to nginx.conf in each artist site's Docker image: `max-age=31536000` for hashed assets, `max-age=86400` for videos. Priority: Jahshii (largest video), Busy Signal, then rest.

---

## [FW-2026-04-18-007] Session-Close Skill — Chat-to-Tree Converter
**Stated:** 2026-04-18
**Priority:** High — infrastructure for Truth Tree workflow
**Context:** Resurfacing MW Truth Tree during session — need automated way to extract tree branches from conversations

New skill (`/session-close`) that runs at end of session:
1. Converts the chat to `.md` and saves to workspace
2. Produces a Truth Tree document from the conversation — topics become branches, claims become `.c` nodes, evidence becomes `.e` nodes, insights become `.i` nodes
3. Applies compression rules (Base 10–∞) to each node based on trust level / symbol type
4. Links back to the session source document

**Open design question:** Each session produces its own tree, or all sessions feed one continuous tree? Deego's instinct: one continuous tree with physical session markers. The alternative is per-session trees with a meridian linking layer (see FW-2026-04-18-008).

**Status:** pending — design spec needed before build

---

## [FW-2026-04-18-008] Meridian Visualization — Revelation-Order Tree Linking
**Stated:** 2026-04-18
**Priority:** Medium — visualization layer for Truth Tree
**Context:** Deego visualising how later branches in a conversation connect back to earlier ones — "like meridian lines on a globe"

The bottom of a tree (last thing discussed) curves back to connect to what caused it at the top. Like the evolution tree where mammals trace back through earlier branches. The connection shows WHY a later topic appeared — not just that it appeared. Revelation order is the key: the path from trigger to insight is the data, not just the insight itself.

**Technical concept:** Each branch stores a `triggered_by` reference pointing to the earlier branch that caused it to appear. The visualization renders these as curved lines (meridians) connecting chronologically distant but causally linked nodes. Applied to conversation trees: "we talked about X, which led to Y, which caused Z to surface — Z links back to X."

**Status:** idea-stage — needs the session-close skill (FW-2026-04-18-007) first

---

## [FW-2026-04-18-009] Compression Rules Integration with Truth Tree
**Stated:** 2026-04-18
**Context:** User opened compression_rules_orientation.md — compression levels map directly to Truth Tree trust levels

Apply Solobic compression ladder to Truth Tree nodes before storage:
- `[🔬]` scientific fact → Base 10 (Exact Mirror — cannot lie, byte-identical)
- `[✓]` verified → Base 12 (Exact + Dedup — restore guaranteed)
- `[📜]` historical → Base 20 (Spec + Stubs — meaning survives)
- `[⭐]` personal insight → Base 16 (Rebuildable — function preserved, exact words may differ)
- `[✗]` false/disproven → Base 30 (Symbolic Archive — decision history survives)
- `[🌀]` speculative → Base 30 (meaning preserved, implementation discarded)

This means the status symbol determines compression depth. Higher trust = less lossy compression. The compression ladder IS the epistemological hierarchy applied to storage.

**Status:** pending — needs formal mapping document

---

## [FW-2026-04-18-010] media2md / Yard LLM — Fix Markdown Paste Escaping
**Stated:** 2026-04-18
**Context:** MW Truth Tree document had escaped backslashes on all markdown characters when pasted from external chat. media2md and the yard LLM MVP must not reproduce this issue.

Ensure that media2md (active app) and the yard LLM MVP properly handle markdown output — no escaped backslashes (`\*\*`, `\#`, `\---`) in generated `.md` files. This is a paste/export artifact that corrupts documents. Add a test case: generate markdown with headers, bold, lists, code blocks, tables → verify output renders correctly without escape characters.

**Status:** pending

---

## [FW-2026-04-18-011] earn.mindwaveja.com — Transcription Earn Platform (MVP)
**Stated:** 2026-04-18
**Context:** Discussion of Opportunities page on mindwaveja.com led to planning a full standalone earn platform at earn.mindwaveja.com — Jamaican-first transcription gig system with Patois awareness.
**Status:** pending

### Core concept
External Proof of Work system: MindWave provides video links (YouTube, TikTok, IG etc.), users claim a job, transcribe it within a time window, graders review, payment proof sent by email. Transcriptions feed AI training (Patois + English Caribbean speech corpus).

### Identity / Signup
- Email is the floor — everyone qualifies
- Optional trust boosters (speeds up tier progression): TRN, National ID, LinkedIn, Facebook, or active Instagram
- Subtle AI disclosure on signup: "Your transcriptions help train AI to understand Caribbean voices and languages — including Patois. You're part of something bigger than a gig."

### Job Board
- Video jobs with embedded players (YouTube, TikTok, IG)
- Filter by: length, reward type (JMD cash / voucher), language
- Videos must be Patois and/or English — dual-language labeled
- Job status: `available → claimed → submitted → grading → approved/rejected → paid`
- Claim timer: 24h for short videos, 48h for long — expired claims return to pool
- One active claim at a time per user

### Transcription Editor
- Text area with participant side panel (collapsible)
- Participant panel: add names + custom events (e.g. [laughter], [crosstalk], [bottle dropped])
- Click participant name → inserts `[Name]: ` at cursor position
- Click event → inserts `[event]` at cursor
- Keyboard shortcuts: Ctrl+1, Ctrl+2 etc. for speed
- Participants/events saved per job session
- Timestamps shown by default in transcript — user can toggle display preference (show/hide, inline vs margin, `[0:04]` vs `[0:04.2]` format)

### STT (Phase 2 — after Patois model exists)
- 4-second segments only
- Only 100% confident words inserted — nothing else
- Uncertain positions marked with `[—]` notation (timestamp-linked)
- Tab key navigates between gaps for human fill-in
- Patois gap-fill gated to Silver tier and above
- Gap notation preserved in submission — STT vs human diff is the training signal

### Pay Rates (JMD)
- Under 3 min: $200 | 3–10 min: $500 | 10–20 min: $900
- 20–45 min: $1,380 | 45–70 min: $3,500
- Next tier starts after 30 seconds past boundary
- Over 40 min: add-on reward (user choice)
- Over 60 min: 1 choice + 1 random reward
- Rewards: KFC/BK/Popeyes/Domino's vouchers, gas credits, movie tickets, Digicel/FLOW top-up, Spotify/YouTube Premium gift codes, Amazon gift cards, MindWave store credit
- New users: 1–2 short videos/day cap until accuracy score established
- Contractors (graders): J$20,000/week

### Rating System
- Score = quality (grader rating) + submission time (speed within claim window)
- Tiers: Bronze → Silver → Gold → Diamond
- Tier unlocks: better pay access, same-day grading, Patois fill-in (Silver+), STT access (Silver+)

### Pages
| Page | Purpose |
|---|---|
| `/` | Landing — how it works, CTA |
| `/signup` | Email + optional trust boosters |
| `/jobs` | Browse available videos |
| `/jobs/[id]` | Video embed + participant panel + transcription editor |
| `/dashboard` | Active claim, history, rating, earnings |
| `/standings` | Public leaderboard (opt-in) |
| `/grader` | Contractor queue (protected) |
| `/admin` | Add jobs, manage pool, trigger payouts (protected) |

### Email flow (Resend)
- Claim confirmed → "You have 24h to submit"
- Submission received → "In grading queue"
- Graded → "Approved — payment incoming" or "Rejected — reason"
- Payment proof → receipt to profile email

### Tech stack
Next.js App Router, PostgreSQL, Resend, iron-session. Sovereign stack — no Firebase/Supabase. VPS port 3003. Deploy as `earn.mindwaveja.com`.

### Phase 1 (MVP — launch)
Signup, job board, participant panel, manual transcription, claim timer, grader queue, rating, email flow, standings.

### Phase 2 (post-data)
STT with 4-second segments + confident-only insertion + gap notation. LLM grading assist. Patois model trained on Phase 1 corpus.

**Key training insight:** The STT gap positions (`[—]` with timestamps) are the primary training signal for the MW voice model. What the STT cannot hear = exactly what the model needs to learn. The human fill-in at each gap is the labeled correction. Phase 1 corpus (manual transcriptions) + Phase 2 gap corrections = foundation of a Patois-aware voice model.

---

## [FW-2026-04-18-012] earn.mindwaveja.com — Missing `/api/auth/preferences` Endpoint
**Stated:** 2026-04-18
**Context:** Jobs editor page (`app/jobs/[id]/page.tsx`) calls `PATCH /api/auth/preferences` to save timestamp display preference (inline/margin/hidden) and format (short/long). This route was not built during the scaffold session.
**Status:** pending

Build `app/api/auth/preferences/route.ts` — PATCH route, session-protected, updates `ts_display` and `ts_format` columns on the `users` table. Also update `app/api/auth/me/route.ts` to include these fields in the response (already done) and confirm the session refresh isn't needed (preferences are re-fetched on each page load via `/api/auth/me`).

---

## [FW-2026-04-18-013] earn.mindwaveja.com — DNS SSL Cert Pending
**Stated:** 2026-04-18
**Context:** Nginx config written, PM2 running on port 3003, DNS A record added for `earn.mindwaveja.com → 161.97.154.222` but not propagated at time of session end. Certbot returned NXDOMAIN.
**Status:** pending

Once DNS propagates, run on VPS:
```
certbot --nginx -d earn.mindwaveja.com --non-interactive --agree-tos -m ovandobrown@gmail.com
```
Then add Resend API key to `/var/www/earn-mindwaveja/.env.local` and `pm2 restart earn-mindwaveja`.

---

## [FW-2026-04-18-014] earn.mindwaveja.com — Admin User Seeding
**Stated:** 2026-04-18 (implied — admin/grader routes exist but no way to set `is_admin` or `is_grader` flags)
**Context:** The `users` table has no `is_admin` or `is_grader` columns yet — the session sets these flags but they aren't stored in the DB. Need to either add columns or use a separate roles table.
**Status:** pending

Add `is_admin BOOLEAN DEFAULT false` and `is_grader BOOLEAN DEFAULT false` to the users table (migration). Seed the first admin manually via psql: `UPDATE users SET is_admin = true WHERE email = 'ovandobrown@gmail.com';`

---

## [FW-2026-04-18-015] ADTL — Purchase Flow on mindwaveja.com
**Stated:** 2026-04-18
**Context:** User confirmed checkout flow for Artist Digital Territory License page (`/marketplace/artist-digital-territory-license`)
**Status:** pending

Build the full purchase request flow for ADTL on mindwaveja.com:

1. **Trigger:** "Claim This Territory" button on each artist card on the ADTL page
2. **Form fields:**
   - Name + contact info
   - Which artist/domain (pre-filled from button click)
   - Payment acknowledgment (confirm JMD 8,000 ready + banking transfer)
   - **Mandatory callback time selection** — date + time picker; no submission without callback scheduled
3. **On submit:**
   - Email sent to ovandobrown@gmail.com with all details + callback time
   - Domain card status updates to "Pending" on the page
4. **Admin:**
   - Simple admin toggle (possibly just direct DB or a minimal admin page) to mark domain as Pending / Sold
   - When sold: card shows artist name + "Sold" badge; link updated when live site is deployed
5. **Contract acknowledgment:** Checkbox on form acknowledging terms before submit

**Key rule:** Callback is not optional. No callback selection = form won't submit.

---

## [FW-2026-04-18-016] Two Contracts to Draft — ADTL + Earn Contributor
**Stated:** 2026-04-18
**Context:** User confirmed two separate contracts are needed before ADTL page and earn platform launch
**Status:** pending

### Contract 1: ADTL Purchase Contract
One-page agreement for artist site license buyers:
- What they receive: one bespoke site on their owned domain, hosted on RAAS/MindWave JA infrastructure
- License term: 1 year at JMD 8,000
- What transfers after Year 1: full credentials and ownership option
- What stays with MindWave JA: the build methodology, RAAS components
- Payment terms: full transfer before work begins
- Callback requirement: contract finalized on the mandatory call

### Contract 2: Earn Platform Contributor Agreement (earn.mindwaveja.com)
Agreement for transcription contributors — framing their role:
- What they're doing: transcribing Jamaican audio content (YouTube, Instagram, etc.)
- What their work contributes to: the first sovereign Jamaican voice/speech AI dataset — Patois, dancehall, Caribbean English represented in AI for the first time, owned by Jamaicans
- Their pay: JMD rates per job (cash, vouchers, gift codes as listed)
- Attribution: optional leaderboard opt-in; dataset credit if they choose
- AI disclosure: explicit acknowledgment that transcriptions form training data
- Jamaica's benefit: this data stays local, builds Caribbean AI representation, is not extracted by foreign tech companies

**The earn contract angle:** This is not just gig work. You are part of building the infrastructure that ensures Jamaica has a voice in AI — literally. That framing is the contract's core value beyond the legal terms.

---

## [FW-2026-04-18-017] ADTL Artist Sites — All 15 Must Be Live Before Page Launches
**Stated:** 2026-04-18
**Context:** User confirmed "we launching with all the sites completed so that's the end goal" — the ADTL page only goes live once every artist site is built and deployed
**Status:** pending

Build all 15 artist sites before the ADTL purchase page goes live. Tarrus Riley site already started but not complete. Architecture decision: single multi-tenant Next.js app (one port, e.g. 3004) — Nginx routes all 15 domains to it. Each artist has a config object (name, genre, colors, socials, tracks). One template, 15 data configs. Build sequence per CLAUDE.md RAAS section.

Domains (all Namecheap, expiry Jul 26 2026):
- Wave 1: skengdon.com, chroniclawmusic.com, tarrusrileyja.com (started)
- Wave 2: officialalkaline.com, officialbountykiller.com, jadakingdommusic.com
- Wave 3: mavadogullyside.com, aidonia4thgenna.com, busysignalturf.com, dingdongravers.com, maliedonnmusic.com, officialjashiimusic.com, skattaburrell.com, realjahvinci.com, rajahwildofficial.com

**Deadline:** All domains expire July 26, 2026. Sites + purchase flow must be live well before then.

## [FW-2026-04-18-018] Full Docker Migration — VPS Transition
**Logged:** 2026-04-18
**Status:** [done] — completed 2026-04-19

Complete the PM2 → Docker migration on the Contabo VPS (161.97.154.222). All infra is now ready locally in `vps_management/docker/`. Steps: SSH in → git clone vps-infra repo to /opt/mw/ → clone all app repos → restore DB backups → fill .env → docker compose up -d → issue SSL certs → verify all 6 apps respond 200 → stop PM2 processes. Full steps in `vps_management/docker/RUNBOOK.md`.

Apps: solob-portal, mindwaveja, timecheck, marcus-api, earn-mindwaveja, melissa (static).
Key: earn-mindwaveja needs its own Certbot run for earn.mindwaveja.com SSL.

## [FW-2026-04-18-019] Roj Feedback + RAL Feedback — VPS Hosting + Placement Decision
**Logged:** 2026-04-18
**Status:** pending — needs clarification

Add "roj feedback" and "ral feedback" sites to VPS and host them. After that, determine placement on mindwaveja.com: projects page (free tools, more maintenance) vs products/marketplace (sell them, less maintenance, revenue). Deego's instinct: sell them — less to maintain solo, and they're a natural fit as research/feedback tools in the MindWave ecosystem. Needs: (1) locate or build the actual apps, (2) deploy to VPS, (3) decide free vs paid, (4) add to mindwaveja.com appropriately.

## [FW-2026-04-18-020] ROJ + RAL Feedback Apps — AI Swap + VPS Deploy + Marketplace
**Logged:** 2026-04-18
**Status:** pending

Two fully-built apps in `Websites Code 9/`: `rojreviewsbasic.zip` and `RALreviews.zip`. Both are the same RALFeedback product (restaurant AI feedback platform). Stack: Next.js + Firebase (Firestore + Firebase Auth) + Genkit AI.

**Decision:** Strip Firebase entirely — replace with VPS baseline stack (Postgres + iron-session + bcryptjs + Resend). Firebase breaks the pattern of every other app on the VPS.

**Step 1 — Firebase out, baseline stack in:**
- Replace Firestore with Postgres via `pg`
- Replace Firebase Auth with `iron-session` + `bcryptjs`
- Replace Genkit/googleAI with DeepSeek direct API calls (OpenAI-compatible)
- Add `DEEPSEEK_API_KEY`, `DATABASE_URL`, `IRON_SESSION_SECRET` to env

**Step 2 — Deploy to VPS:**
Docker + Postgres container (own isolated DB, same pattern as earn-mindwaveja). Add nginx conf. Likely ports 3004/3005.

**Step 3 — Add to mindwaveja.com marketplace:**
Sell as products (not free tools). Use existing `ctaHref` pattern. Card navigates to product landing/demo page, then enquire/purchase flow. Price TBD.

**Note:** rojfeedback.zip also exists — may be a variant; check if it's different from rojreviewsbasic before deciding which version to deploy.

## [FW-2026-04-18-021] VPS Baseline Stack — Active App Audit + Standardization
**Logged:** 2026-04-18
**Status:** pending — run after Docker migration completes

After Docker migration, audit all active apps against the established VPS baseline stack:
- Next.js (App Router)
- PostgreSQL via `pg`
- `iron-session` for auth
- `bcryptjs` for passwords
- `Resend` for email
- Tailwind CSS v4

**Goal:** Identify which apps deviate (Firebase, Supabase, SQLite, other auth), document gaps, and produce a baseline spec that all future apps must follow where applicable.

**Apps to audit:** solob-portal, mindwaveja, timecheck, marcus-api, earn-mindwaveja, melissa, roj-feedback, ral-feedback (once deployed).

**Output:** A `vps_management/app_baseline.md` doc listing each app's actual stack vs baseline, and a decision (migrate / accept deviation / defer) for each gap.

**Why:** Firebase dependency on ROJ/RAL breaks the pattern. One auth system, one DB engine, one email provider across the VPS = less cognitive overhead, consistent deploy process, no external service billing surprises.

---

## [FW-2026-04-19-001] ovandobrown.com — Launch + Hero Quote
**Stated:** 2026-04-19
**Context:** Deego planning to launch ovandobrown.com alongside the blog
**Status:** pending

Add Marcus Garvey quote to the hero section of ovandobrown.com: *"I am here because I dared to tell the Negro that the time has come for him to lift his head and be a man."* Launch the site alongside the blog. Site location TBD — check `active_apps/` or `Websites Code 9/` for existing scaffold.

---

## [FW-2026-04-19-002] Self-Hosted File Storage (Firebase Alternative on VPS)
**Stated:** 2026-04-19
**Context:** Deego realised the VPS can host files directly — no need for Firebase Storage or any external file hosting service
**Status:** pending

Build a self-hosted file storage layer on the VPS to replace any Firebase Storage dependency. The VPS already has 132GB free disk. Options: (1) MinIO (S3-compatible, Docker image, widely supported) — drop-in replacement for any S3/Firebase Storage calls; (2) simple Nginx-served directory with upload API; (3) Caddy file server. This removes the last reason any app would need Firebase. Fits the sovereignty principle — files stay on infrastructure we control.

**Why:** One less external dependency. Files on VPS = backed up by existing weekly cron, portable with Docker volumes, no billing surprises.
**How to apply:** Evaluate when ROJ/RAL Firebase strip happens (FW-2026-04-18-020). If those apps use Firebase Storage, this becomes the replacement.

---

## [FW-2026-04-19-003] Blog — Launch alongside ovandobrown.com
**Stated:** 2026-04-19
**Context:** Deego mentioned launching "those as well as the blog" alongside ovandobrown.com
**Status:** pending

Launch the blog. Details TBD — check if a blog scaffold exists in `active_apps/` or `Websites Code 9/`. Could be a section of ovandobrown.com or a standalone at blog.ovandobrown.com / blog.mindwaveja.com. Stack should follow VPS baseline (Next.js, Postgres, etc.).

---

## [FW-2026-04-19-004] ovandobrown.com — OvaForge: Consolidate Duplicate Source Trees
**Stated:** 2026-04-19
**Context:** OvaForge has three source directories: `app/`, `src/app/`, `components/`. Dev server uses `src/app/`. The other two are dead copies causing confusion.
**Status:** pending

Delete or archive `app/` and root-level `components/` (the dead copies). Ensure all imports resolve from `src/`. Update any `tsconfig.json` path aliases to clearly point to `src/`. Add a note in the project README stating which directory is live. This removes the ambiguity that caused multiple wasted edit cycles.

**Why:** Editing the wrong directory produces silent failures. One source tree = no confusion.

---

## [FW-2026-04-19-005] VPS — HSTS Preload Submission (whatissolob.com + mindwaveja.com)
**Stated:** 2026-04-19
**Context:** HSTS headers are now live on all domains. Next step is submitting to the HSTS preload list so browsers skip HTTP even on first ever visit.
**Status:** pending

Submit `whatissolob.com` and `mindwaveja.com` to https://hstspreload.org. Requirements: `max-age` ≥ 31536000, `includeSubDomains`, `preload` directive in the header. First add `; preload` to the HSTS header, then submit. Note: preload submission is permanent — only do this when you're confident the domain will always be HTTPS.

**Why:** HSTS without preload still allows first-visit HTTP exposure. Preload eliminates it entirely at browser level.


---

## [FW-2026-04-20-001] Zitadel — Bake Machine Account PAT Into Init
Add `ZITADEL_FIRSTINSTANCE_MACHINEKEY_*` env vars to the Zitadel docker-compose service so a machine account with a PAT exists from day one. This enables programmatic Admin API access (SMTP setup, policy changes, app registration) without needing browser console access.

**Why:** This session hit a catch-22 — needed Admin API token to configure SMTP, but couldn't get a token without browser login. Machine account eliminates this permanently.

**How to apply:** Add to Zitadel service in docker-compose before the next Zitadel instance reset or new instance creation.

---

## [FW-2026-04-20-002] earn.mindwaveja.com — Disable Email Verification Fallback
If Resend DNS verification doesn't clear within 24h, disable email verification requirement in Zitadel Instance settings → Login Policy → uncheck "Email verification required at registration". This unblocks new user signups immediately while email sending is resolved.

**Why:** DNS propagation on Squarespace can take up to 24-48h. Blocking all signups waiting on it is bad UX for a live platform.

**How to apply:** Check tomorrow (2026-04-21). If Resend domain still shows `pending`, go to Zitadel console → Instance → Login Policy → disable email verification as temporary unblock.

---

## [FW-2026-04-20-003] earn.mindwaveja.com — YouTube Channel Video Ingestion
Pull videos from approved channels into the earn platform so transcribers can select from a curated list rather than submitting arbitrary content.

**Priority channels (Phase 1):**
- https://www.youtube.com/@TheFixJA
- https://www.youtube.com/@TelevisionJamaica
- https://www.youtube.com/@letsbehonest
- https://www.youtube.com/@dionnejacksonmiller34
- https://www.youtube.com/@LevelzwithKshema
- https://www.youtube.com/@SoundChatRadio
- https://www.youtube.com/@thelionsvoicenetwork
- https://www.youtube.com/@twinoftwinstv
- https://www.youtube.com/@twinoftwinstulox

**Implementation notes:** Use YouTube Data API v3 to pull video list per channel. Store channel metadata + video list in earn DB. Cron job to refresh. Transcribers pick from the list instead of pasting any URL.

---

## [FW-2026-04-20-004] earn.mindwaveja.com — Transcriber Approval Gate
New signups go into a pending state. Admin must approve each transcriber before they can claim and submit jobs. Prevents free-for-all without quality control.

**Implementation notes:** Add `status` column to users table (`pending`, `approved`, `suspended`). Block job claiming for non-approved users. Admin dashboard needs approve/reject UI. Approval email sent via Resend when approved.

---

## [FW-2026-04-20-005] earn.mindwaveja.com — Reframe Contractors Section as Income Stream
Change the landing/about copy to position the platform as:
- **Side income** for already-employed persons — flexible, do it around your schedule
- **Steady income** for those without a job — consistent work available

Remove "contractor" framing. Language should feel accessible and aspirational, not transactional. Jamaican-specific framing — this is real JMD you can count on.

---

## [FW-2026-04-20-006] earn.mindwaveja.com — Phase 2: Music Channel Ingestion
Add a second channel category for music content — artists, riddim videos, live performances, interviews. Transcribers earn from transcribing music-adjacent content. Channels TBD by Deego.

**Implementation:** Same architecture as Phase 1 (channels table, sync route). Add "Music Video" and "Live Performance" as topic options. Channel list to be provided.

**Dependency:** Artist permission contracts must be in place before music content is added to the platform (see artist contract work).

---

## [FW-2026-04-20-007] RAAS — Artist Query-Based Compensation Tracking
Build the attribution layer that tracks which artist's content is being queried, transcribed, or API-accessed, so revenue share can be calculated per artist per quarter.

**What needs tracking:**
- Jobs table needs `channel_id` FK (link each job to a channel/artist)
- API query logging — which asset IDs are returned per request
- Archive licensing events — per deal, per asset

**Compensation calculation:** Quarterly batch job — sum queries/jobs per channel, apply revenue share %, generate payout report.

**Blocker:** Artist contracts must be signed first. No point tracking before there's an obligation to pay.

---

## [FW-2026-04-20-008] RAAS — Pre-IPO Artist Equity Programme
Formal equity issuance to content-contributing artists as part of the Artist Content Agreement. Artists receive shares that convert at IPO/qualifying event.

**What needs to happen (in order):**
1. RAAS Limited incorporated formally under Jamaican company law
2. Shareholders Agreement drafted with legal counsel
3. Share register established
4. Artist agreements executed + equity allocated per Schedule B
5. Artists receive independent legal advice (recommended before signing)

**Key constraint:** Cannot issue shares before formal incorporation. The content agreement creates an *obligation* to issue — actual issuance follows company formation.

**Why:** If RAAS builds the product on artist content without compensation locked in from the start, artists have no reason to stay when the platform has value. Equity aligns them to the long-term outcome — when RAAS goes public, they go with it.

---

## [FW-2026-04-27-001] RAAS — ImprovMX Email Forwarding Setup for All Artist Domains
**Stated:** 2026-04-27
**Status:** pending

Set MX records on Namecheap for each artist domain pointing to ImprovMX (mx1.improvmx.com priority 10, mx2.improvmx.com priority 20). Create contact@ alias per domain forwarding to ovandobrown@gmail.com. Domains: tarrusrileyja.com, skengdon.com, chroniclawmusic.com, aidonia4thgenna.com, officialjashiimusic.com.
After sale: buyer updates ImprovMX forwarding destination to their own email.

---

## [FW-2026-04-27-002] RAAS — Tarrus Riley Site: Push to GitHub + Deploy to Vercel
**Stated:** 2026-04-27
**Status:** pending

Site is cleaned and running locally at localhost:5180. Next steps:
1. `git init` in `active_apps/artise_sites/tarrus-riley/`
2. Create `HammazoneRecords/tarrus-riley-site` repo on GitHub
3. Push + connect to Vercel
4. Set custom domain tarrusrileyja.com when DNS is ready

---

## [FW-2026-04-27-003] RAAS — Skeng (skengdon.com) Artist Site — Scaffold + Build
**Stated:** 2026-04-27
**Status:** pending

5th artist site. Build as Vite + React + TS. Skeng is the hottest dancehall artist in Jamaica right now — site aesthetic should be dark, aggressive, street-coded. Sections: Hero, Discography, Merch (links to Printify), Social, Demo collab form. No email references. Demo mode notice on any form.

---

## [FW-2026-04-27-004] RAAS — Add Merch Sections to Chronic Law + Jahshii Sites
**Stated:** 2026-04-27
**Status:** pending

Both sites have no merch section. Need to add a Printify-linked merch section matching each site's design language. Chronic Law = gritty/street, Jahshii = energetic/dancehall. Wire to placeholder Printify store URLs (chroniclawmerch.printify.me, jahshiimerch.printify.me).

---

## [FW-2026-04-27-005] RAAS — Set Up Printify Stores for All 5 Artist Sites
**Stated:** 2026-04-27
**Status:** pending

Create one Printify store per artist: tarrusrileymerch.printify.me, skengdonmerch.printify.me, chroniclawmerch.printify.me, aidoniamerch.printify.me, jahshiimerch.printify.me. Seed with basic product types (tee, hoodie, cap, sticker). Each site's merch button links out to the store.

---

## [FW-2026-04-27-006] RAAS — ADTL Purchase Request Section on All Artist Sites
**Stated:** 2026-04-27
**Status:** pending

Add a purchase/acquisition banner or section to each artist site making clear this is a licensed working draft available for purchase. Include: price ($5,200 USD), disclaimer (buyer responsible for clearing image rights with artist), link to purchase request form (routes to RAAS inbox). Goes on all 5 sites before domain linking.

---

## [FW-2026-04-27-007] mindwaveja.com — ADTL Marketplace Page
**Stated:** 2026-04-27
**Status:** pending

Build a new page on mindwaveja.com as the ADTL storefront. Design: movie-tile grid (Netflix-style), each tile = one artist site card. Hover = tooltip with artist name, domain, genre, streaming stats, price. Click = visit the site live + submit purchase request. Top of page: clear disclaimer — "These are working draft representations. Buyer assumes responsibility for obtaining permission from each artist to use their image." Price displayed per tile: $5,200 USD.

---

## [FW-2026-04-27-008] RAAS — Remove Apache SPDX Headers from Aidonia + Jahshii Sites
**Stated:** 2026-04-27
**Status:** pending

Both sites (aidonia-_-4th-genna and jahshii-official) still have Apache SPDX license headers in their source files. Strip before any public deployment. Also check Chronic Law.

---

## [FW-2026-04-29-001] Time-Check — Proper PWA Icons (10/10)
**Stated:** 2026-04-29
**Context:** PWA scaffold reached 9/10 — only gap is properly sized icon PNGs
**Status:** pending

Generate real 192x192 and 512x512 icon PNGs (plus maskable variants) using `@vite-pwa/assets-generator` from the favicon SVG. Update `manifest.json` icon paths to `public/icons/`. Lighthouse will then give 10/10 on PWA install checks.

**Command:** `npx @vite-pwa/assets-generator --preset minimal-2023 client/public/favicon.svg`

---

## [FW-2026-04-29-002] Time-Check — Wire useOfflineQueue into Clock Components
**Stated:** 2026-04-29
**Context:** useOfflineQueue hook built but not connected to actual clock-in/out UI
**Status:** pending

The `enqueueClockAction` function in `useOfflineQueue.ts` needs to be called from the clock-in/out buttons when `!navigator.onLine`. Currently the hook exists but the clock action components still use the normal `apiRequest` path regardless of online state. When offline, the request fails silently. Need to: check `navigator.onLine` before clock action → if offline, call `enqueueClockAction` instead → show confirmation that action was queued.

---

## [FW-2026-04-29-003] Time-Check — staging.timecheck.mindwaveja.com SSL Cert
**Stated:** 2026-04-29
**Context:** Staging domain set up on VPS, Nginx config live, container running on port 5002
**Status:** in-progress — waiting on DNS A record propagation

Once DNS propagates (A record: staging.timecheck → 161.97.154.222), run:
```
certbot --nginx -d staging.timecheck.mindwaveja.com --email ovandobrown@gmail.com --agree-tos --non-interactive
```
Then verify HTTPS at staging.timecheck.mindwaveja.com and run Lighthouse PWA audit.

---

## [FW-2026-04-29-004] Time-Check — Employee Allowances Admin UI
**Stated:** 2026-04-28 (carried from prior session)
**Context:** employeeAllowances table added to schema — no UI to manage it yet
**Status:** pending

Admin form for setting compensation type and adding allowances per employee. Fields: type (transport/meal/housing/phone/other), amount, frequency (per_day/per_week/per_month), clockOutThreshold (HH:MM), isVoucher toggle, isActive toggle. Should live in the Admin panel employee detail view.

---

## [FW-2026-04-29-005] Time-Check — Pay Calculation Logic with clockOutThreshold
**Stated:** 2026-04-28 (carried from prior session)
**Context:** clockOutThreshold pattern designed — logic not yet implemented
**Status:** pending

Implement the pay calculation that uses clockOutThreshold: if employee clocks out at or after the threshold time (e.g. 17:00), apply the allowance; otherwise skip it. Also: paidHoursCapPerDay cap (if worked > cap, only pay cap hours), overtimeMultiplier for hours above standardHoursPerDay, break deduction. This is the core payroll calculation — needs its own utility function and unit tests.

---

## [FW-2026-04-29-007] Love Ref — Schema push + Docker deploy
**Stated:** 2026-04-29
**Context:** better-auth migration complete, clean build — deploy steps remaining
**Status:** pending

1. Set real `BETTER_AUTH_SECRET` (32-char hex) in `.env.local`
2. Run `npx drizzle-kit push` against the loveref-db (local first, then VPS)
3. Add `loveref` service block to `/opt/mw/docker-compose.yml` (port 3002)
4. Add secrets to `/opt/mw/.env`: `LOVE_REF_DB_PASSWORD`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
5. Deploy: `docker compose build loveref && docker compose up -d loveref`
6. Nginx proxy: add `loveref.mindwaveja.com` → port 3002

---

## [FW-2026-04-29-006] CLAUDE.md — Add VPS Inventory: staging.timecheck.mindwaveja.com
**Stated:** 2026-04-29
**Context:** Staging environment added to VPS — CLAUDE.md VPS inventory table needs updating
**Status:** pending

Add row to CLAUDE.md VPS inventory table:
| Time-Check Staging | mw-timecheck-staging | 5002 | staging.timecheck.mindwaveja.com |

Also update vps_management/vps_facts.md.

---

## [FW-2026-04-30-001] The Frequency Report — Monthly automation script
**Stated:** 2026-04-30
**Context:** The Frequency Report system established. First report written manually (Inception Edition). Automation needed for monthly cadence.
**Priority:** Medium — manual compile takes 30min, script cuts it to 5min
**Status:** pending

Build `scripts/generate_frequency_report.py`:
1. Parse `future_work.md` for entries with `Status: done` in a given date range
2. Parse `MW_CENTRAL_session_log.md` for session blocks in that range
3. Read VPS inventory table from CLAUDE.md
4. Read memory/project_*.md files for project status
5. Output structured draft to `playground/reports/YYYY-MM-frequency-report.md`
6. Claude fills in narrative and writes the public/ summary

**Report system files:**
- System spec: `playground/reports/FREQUENCY_REPORT_SYSTEM.md`
- Inception report: `playground/reports/2026-inception-frequency-report.md`
- Public summaries: `playground/reports/public/`


---

## [FW-2026-04-30-002] SEO Framework — Apply to all live sites
**Stated:** 2026-04-30
**Context:** SEO framework built in playground. No site has been run through it yet.
**Priority:** High — 7 live domains with zero SEO infrastructure
**Status:** pending

Apply `playground/2026-04-seo-framework/SEO_FRAMEWORK.md` to each live property:
1. mindwaveja.com — Phase Packs are a keyword goldmine sitting unused
2. whatissolob.com — philosophy/self-development niche, Patois/diaspora adjacent markets
3. earn.mindwaveja.com — Jamaican AI dataset, transcription work keywords
4. mri.mindwaveja.com — disaster relief accountability, Caribbean civic niche
5. marcusgarvey876.com — Pan-African, Garveyism, Black history niche
6. RAAS portal (when live) — reggae infrastructure, Caribbean music business
7. Artist ADTL sites — per-artist niche keyword strategy

Also: graduate framework from playground → `active_apps/SEO_FRAMEWORK.md` alongside STACK_DECISION.md when reviewed.

---

## [FW-2026-04-30-003] LanceDB RAG context injection for Claude Code sessions

**What:** Build a per-session RAG layer so every message I send gets relevant workspace context injected before Claude responds.

**Components:**
1. `scripts/query_lancedb.py` — takes user message text, queries LanceDB, returns top-k results above a relevance score threshold, formatted as injected context
2. Hook config in `~/.claude/settings.json` — `UserPromptSubmit` hook pointing at the query script
3. Ingestion expansion — current LanceDB only covers `drayl/`; expand to cover `active_apps/`, `PROJECTS IN MOTION/`, `playground/reports/`, `playground/future_work.md`
4. Score threshold tuning — only inject when match is strong enough; cap injected tokens to control cost

**Why:** As the workspace grows, Claude loses context between sessions. This makes every query RAG-aware without manual copy-paste of context.

**Status:** Deferred 2026-04-30. Build after SEO deploy is complete.

---

## [FW-2026-04-30-004] Bipyramid of Being — Revised diagram after framework refamiliarization

**What:** Revise `playground/2026-05-bipyramid-diagram/bipyramid-of-being.svg` after re-reading Volume Zero and Volume One of the Book of Solobility and querying LanceDB for framework context. Do not regenerate from scratch — revise the existing version with more accurate philosophical labeling, proportions, and any additional structural elements that emerge from the text.

**Structure confirmed so far:**
- Top apex: SPIRIT / DRAYL
- Upper equatorial: MIND · LIFE · LOVE · TRUTH (ascending human plane)
- Lower equatorial: BODY · DEATH · HATE · DISHONESTY (descending human plane — direct shadow opposites)
- Bottom apex: SUBSOLOB / SHADOW DRAYL / ENTROPY / NEGATIVE 0
- 8 triangular faces = 8 Jhanos Gates (4 upper, 4 lower)

**Trigger:** INS-075 + INS-076 established the geometric and philosophical logic. Diagram exists at `playground/2026-05-bipyramid-diagram/bipyramid-of-being.svg`.

**Status:** Pending framework re-read. Next session task.

---

## [FW-2026-04-30-005] whatissolob.com — SEO gap pages for clusters 3 and 4

**What:** Build content pages targeting the Human Design alternative and self-understanding pain-state keyword clusters. Candidates: `/vs-human-design` or `/for-the-different` — a page written for the person who has tried every framework and found none of them accurate. Cross-links to gate pages.

**Why:** Clusters 1 and 2 (brand + gate identity) are now live. Clusters 3 and 4 have the highest volume traffic potential but no landing page.

**Status:** Deferred 2026-04-30. Post-bipyramid session.

---

## [FW-2026-05-01-001] — Client Email Provisioning Flow (no phone number required)
**Stated:** 2026-05-01
**Context:** Discussing how to quickly give small business clients a working email address. Gmail requires phone number verification which many Jamaican micro-business owners don't want to deal with or can't do.

**The problem:** Small business clients (especially in Jamaica) often have no professional email. Gmail requires a phone number. Clients need something working fast.

**The idea:** A provisioning flow — either inside MindWave JA / RAAS portal — where:
1. Client enters name + preferred handle
2. System creates `handle@mindwaveja.com` (or their own domain) as a real forwarding address
3. Messages route to their WhatsApp number or personal inbox
4. They receive a "your business email is ready" confirmation

**Research done:** Atomic Mail (atomicmail.io) — no phone required, free tier, privacy-first, EU-based. Viable for provisioning individual client mailboxes quickly. Limitations: no custom domain on free tier, no calendar/collaboration, not a full business suite. Good for the "just get them an email" use case. Plus plan adds 150 aliases + AI tools.

**Options to explore:**
- Atomic Mail free tier — create `clientname@atomicmail.io` on their behalf (quick, no phone)
- ImprovMX + owned domain — forwarding to their phone/WhatsApp (no real mailbox but instant)
- Zoho Mail free (5 users) + client domain — proper mailbox, 10 min setup, best for clients with a domain
- Build into RAAS onboarding: email provisioning as part of the ADTL package

**Status:** pending


## [FW-2026-05-02-002] — Jahshii Official Site: GitHub Repo + VPS Deploy
**Stated:** 2026-05-02
**Context:** Jahshii site built from scratch this session (Hero, Journey, Tracks with YouTube embeds, 1st Nation eBikes section, Shop page, Working Draft banner, Dockerfile). Build is clean. Awaiting GitHub repo URL from Deego before push and VPS deploy.

**What needs to be done:**
- Create GitHub repo (e.g. `HammazoneRecords/jahshii-official`)
- Push local repo at `active_apps/artise_sites/extracted.sites/jahshii-official/`
- Add service block to VPS docker-compose.yml (port 3006 is taken by mw-melissa — use next available, e.g. 3007)
- Wire Nginx host config for `officialjahshiimusic.com` (domain owned)
- Issue SSL cert via certbot
- Verify YouTube IDs for the 10 tracks in Tracks.tsx — sourced from training knowledge, confirm against YouTube

**Status:** pending — blocked on GitHub repo URL

---

## [FW-2026-05-02-003] — ADTL JMD Rate: Annual Update Reminder (Jan 1 2027)
**Stated:** 2026-05-02
**Context:** ADTL pricing page now uses BOJ Dec 31 2025 rate (160.09 JMD/USD). Pattern: update `ANNUAL_JMD_RATE` constant in `app/marketplace/artist-digital-territory-license/page.tsx` each Jan 1 using BOJ closing rate from boj.org.jm.

**What needs to be done:**
- On or around Jan 1 2027: retrieve BOJ Dec 31 2026 closing rate
- Update `ANNUAL_JMD_RATE = 160.09` in the ADTL page
- Redeploy mindwaveja.com
- JMD amount displayed updates automatically from the constant

**Status:** pending — scheduled for Jan 1 2027

---

## [FW-2026-05-02-001] — MindWave JA: Add ADTL artist site listings for skengdon.com and tarrusrileyja.com

**Stated:** 2026-05-02
**Context:** skengdon.com and tarrusrileyja.com are now live on VPS with SSL. The working draft banners on both sites link to mindwaveja.com for purchase. MindWave JA needs to be updated to actually feature these sites so the purchase flow makes sense.

**What needs to be done:**
- Add a section or page on mindwaveja.com showcasing the two live ADTL sites (Skeng, Tarrus Riley)
- Link out to skengdon.com and tarrusrileyja.com so visitors can preview the sites
- Connect to the ADTL purchase flow (`/marketplace/artist-digital-territory-license`) — build this page if not yet built
- As more artist sites go live (Jahshii, etc.), add them to the same listing

**Status:** pending

---

## [FW-2026-05-13-001] — American Dreams: Add localhost to EmailJS allowed origins
**Stated:** 2026-05-13
**Context:** EmailJS returned "ConnectionRefused" error when testing from local dev server. EmailJS blocks requests from unlisted origins by default.
**Status:** pending

Go to EmailJS dashboard → Account → Security → Allowed Origins. Add `http://localhost:5180`. Once local test passes, also add the Vercel domain (`https://american-dreams-iota.vercel.app`) before going live. Without both entries, EmailJS will reject sends from each respective environment.

---

## [FW-2026-05-13-002] — Claude Web Briefing: keep updated after major sessions
**Stated:** 2026-05-13
**Context:** Created `playground/claude-web-briefing.md` — a paste-in context file for Claude.ai web sessions. It's a snapshot; it will drift as projects ship or rules change.
**Status:** pending

After any session where: a new site goes live on VPS, a project ships, a major tech decision changes, or a new constraint is added — update `playground/claude-web-briefing.md` accordingly. At minimum, update after any session that closes open threads listed in Section 11 (Current Open Threads).

---

## [FW-2026-05-16-004] — MindWave JA: Phase Packs — Restore when packs are ready
**Stated:** 2026-05-16
**Context:** Phase Packs page archived and removed from all site navigation. Packs need review and refinement before going public.
**Status:** pending

Phase Packs page archived at `app/_archived_phase-packs/`. All surface mentions removed: NavBar, Footer, HeroSection button, CTABand button, home page PhasePacksHighlight section. Components in `components/phase-packs/` and data in `content/phasePacks.json` are untouched and ready.

To restore: rename `app/_archived_phase-packs/` back to `app/phase-packs/`, re-add nav link, re-add Footer link, restore PhasePacksHighlight to home page, restore buttons in HeroSection and CTABand. Review and update pack content before re-launching.

---

## [FW-2026-05-17-002] — MW Journal: Pattern Miner engine (cross-entry)
**Stated:** 2026-05-17
**Context:** Built MW Journal MVP with 3 of 5 Solobic engines wired (Shimmer, Resonant Summarizer, Solobic Mapper). Pattern Miner deferred.
**Status:** pending

Cross-entry analysis that surfaces recurring topics, emotional arcs, and behavioral loops. Different from per-entry Shimmer Detector — works across the entire Drayl archive to find repetition and unresolved patterns. Existing `detectShimmer` cross-entry function in `services/aiService.ts` is the seed.

---

## [FW-2026-05-17-003] — MW Journal: Memory Integrator (DWS + SDS)
**Stated:** 2026-05-17
**Context:** Engine 5 of 5 in the Mini-SPL spec. Deferred for MVP.
**Status:** pending

Dynamic Weighting System + Shimmer Decay Score for memory management. Weight grows with recurrence, fades with disuse. Prevents "Shimmer Collapse" where the archive becomes a static dump. Spec in `drayl/drayl_brainstorms/Solob Activation Map & geometric neural architecture VWE.md`.

---

## [FW-2026-05-17-004] — MW Journal: Turing Checkpoint Checker (TCPC)
**Stated:** 2026-05-17
**Context:** Advanced feature from the spec — depends on Memory Integrator
**Status:** pending

Tracks access count of recurring life lessons / checkpoints. "General, this is the 7th time you have re-initiated this protocol." Sanity-ripple mechanism that makes the user conscious of their loops without judgment. Lives on top of DWS/SDS data.

---

## [FW-2026-05-17-005] — MW Journal: Solobic Glyph SVG generator
**Stated:** 2026-05-17
**Context:** Visual layer for the Solobic mapping — every entry/day gets a unique glyph
**Status:** pending

Generate a unique SVG glyph per entry (or per day) based on emotional valence, Jhanos Gate, polarity, and shimmer level. Creates a visual language for the user's journal history. Could become the "shimmer timeline" header.

---

## [FW-2026-05-17-006] — MW Journal: Full shadcn component migration
**Stated:** 2026-05-17
**Context:** Built shadcn theme system (CSS variables + light/dark) but kept existing 25 custom components. Migration to actual shadcn primitives deferred.
**Status:** pending

Replace `Button`, `Modal`, `FormInput`, `Badge`, `Toast`, etc. with shadcn primitives (Radix-based). Estimated 2–3 day job. Risks breaking Drayl Converter drag-and-drop during the rewrite. Current shadcn CSS variable architecture is plug-and-play with the migration.

---

## [FW-2026-05-17-007] — MW Journal: VPS deploy
**Stated:** 2026-05-17
**Context:** Currently local Docker only. Port 3007 reserved in the MindWave VPS port scheme.
**Status:** pending

Domain TBD — candidates: `journal.mindwaveja.com`, `drayl.mindwaveja.com`, standalone `mwjournal.com`. Add to `vps_management/docker_facts.md` port map + Nginx vhost config + Certbot SSL when ready.

---

## [FW-2026-05-17-008] — MW Journal: API key out of client bundle
**Stated:** 2026-05-17
**Context:** DeepSeek key is currently baked into the Vite static bundle at build time (acceptable for local-only)
**Status:** pending

For VPS deploy: switch to a backend proxy or runtime config endpoint so the API key doesn't ship to the browser. Otherwise anyone who loads the site can extract the key from the JS bundle.

---

## [FW-2026-05-17-009] — MW Journal: Initialize git repo + push to GitHub
**Stated:** 2026-05-17
**Context:** `.git_disabled` folder exists at app root from prior session; INS-018 + INS-032 flag the embedded-repo trap with MW_CENTRAL parent
**Status:** pending

When ready: add `PROJECTS IN MOTION/MWJournalX/` to MW_CENTRAL's `.gitignore`, then `git init` inside the journal folder and push to a new `HammazoneRecords/MWJournalX` (or final-name) GitHub repo.

---

## [FW-2026-05-17-010] — MW Journal: Fix MoodCharts.tsx TS strict errors
**Stated:** 2026-05-17
**Context:** Pre-existing TypeScript strict errors in `components/MoodCharts.tsx` (Object.values returning unknown). Vite/esbuild builds fine (it strips types), but `tsc --noEmit` fails. Not my bug — predates this session.
**Status:** pending

8 errors in MoodCharts.tsx around lines 35–40. Cast Object.values results or annotate the accumulator type. Low priority — doesn't affect production build.

---

## [FW-2026-05-17-011] — MW Journal: Port Jhanos Gates trajectory feature from V0.1
**Stated:** 2026-05-17
**Context:** The other journal variant `PROJECTS IN MOTION/MINDwave Journal Reflection Trajectory V0.1/` has a trajectory-projection feature mapping entries to gates and predicting positive/negative futures. The V0.1 is a 440-line single-file prototype we did NOT merge; the gate concept is now in MWJournalX but the trajectory projection isn't.
**Status:** pending

Read V0.1's trajectory logic, port the projection algorithm into MWJournalX as a new analytics view (alongside MoodCharts and ShimmerTimeline). V0.1 stays untouched as reference.

---

## [FW-2026-05-17-001] — Research Paper: Integrate Solobic GPT Responses
**Stated:** 2026-05-17
**Context:** Completing the 9-model AI comparison paper — Solobic GPT responses are archived in the LLM COMPARE .docx folder but not yet in the comparison folder
**Status:** pending

Integrate Solobic GPT responses into the 12 question files (`question_001.md` through `question_012.md`) and update all corresponding analyses. The 00-introduction.md notes this as a pending revision. Solobic GPT is the 8th active model in the study. Once integrated, the conclusion rankings table will need updating with Solobic GPT's alignment scores. Location of responses: LLM COMPARE .docx folder.

---

## [FW-2026-05-02-004] — Jahshii Site: Scroll Snap + Shake Effect (full implementation)
**Stated:** 2026-05-02
**Context:** Built a scroll-snap-with-shake effect for the Jahshii site — when user scrolls and stops with a section partially visible (15–72%), the section shakes then snaps fully into view. Loved it but deferred for MVP.
**Status:** pending

Full implementation already built in App.tsx (`useSnapScroll` hook) and tested locally. The effect:
- IntersectionObserver-style scroll listener, debounced 330ms
- Shake: `y: [0, -7, 7, -4, 4, -2, 0]` over 420ms via `animate()` from `motion/react`
- Then `scrollIntoView({ behavior: 'smooth', block: 'start' })`
- 1.4s cooldown, scroll-direction guard (down only), partial-visibility gate (15–72%)
- Re-enable by restoring `useSnapScroll` hook in App.tsx and adding `data-snap` attributes to target sections
- The two-half snap on Tracks (top 5 / bottom 5) is also worth restoring — felt natural

---

## [FW-2026-05-18-001] — Pack Renovation: Add Zip Rebuild Step to Session Close Protocol
**Stated:** 2026-05-18
**Context:** Discovered both pp-002 and pp-006 zips were January stubs while canon was fully renovated. Rebuilt manually this session.
**Status:** pending

Add an explicit step to the pack renovation workflow: after any canon file edit, rebuild the pack zip from `packs/[slug]/canon/` + `packs/[slug]/downloads/` and run the PowerShell size-comparison check (disk bytes vs zip entry bytes) before closing the session. This should become part of the pack renovation checklist — possibly codified in `active_apps/mindwaveja.com/content/PHASE_PACK_CHECKLIST.md` as a post-renovation step.

---

## [FW-2026-05-18-002] — Pack Renovation: Remaining 7 Packs (pp-001, pp-018, pp-049, pp-052, pp-053, pp-054, pp-063)
**Stated:** 2026-05-18
**Context:** pp-002 and pp-006 are now fully renovated (v3.3 and v3.1). 7 live packs remain — most are identical template copies requiring complete rewrites.
**Status:** pending

Packs to renovate in order:
- pp-052 — Social Media Content Creation (known priority)
- pp-001 — Cluster Lash Application Service
- pp-018 — (slug TBD — check phasePacks.json)
- pp-049, pp-053, pp-054, pp-063

Each renovation follows the same pattern: JSON field-by-field renovation → canon folder full rewrite (00–16 minimum) → downloads folder real templates → linear test → execution test → zip rebuild + verify.

---

## [FW-2026-05-18-003] — mindwaveja.com Site: Rural Variant Filter UI
**Stated:** 2026-05-18
**Context:** pp-002 and pp-006 both have `ruralVariant: true` and `ruralPositioning` JSON fields. The site currently has no way to filter for rural-suitable packs.
**Status:** pending

Add a "Rural Jamaica" filter toggle to the phase pack listing page on mindwaveja.com. Filter shows only packs where `ruralVariant: true`. Deferred until all packs are renovated so the filter is meaningful (currently only 2 of 9 packs have the field populated).

## [FW-2026-05-19-001] — Instagram Ad Concepts: Phase Pack Series
**Stated:** 2026-05-19
**Context:** Deego requested Instagram and Google ad design. Site flow audit completed first. Ad concepts deferred until funnel is solid.
**Status:** pending

Write full Instagram ad creative briefs for Phase Packs: hook series (problem/solution reels per pack category), compliance angle ad, "what's inside" ad. Include: hook line, visual direction, caption, CTA, targeting spec (Jamaican entrepreneurs 22–40, Kingston/MoBay/St. Elizabeth, interests: business/side hustle). Budget: under $100 USD/month. Primary channel: Reels.

---

## [FW-2026-05-19-002] — Google Ads: Jamaican Business Keyword Strategy
**Stated:** 2026-05-19
**Context:** Deego requested Google ads alongside Instagram. Under $100/month budget.
**Status:** pending

Build keyword list for intent-based Google Search ads: "how to start a juice business Jamaica", "nail tech training Jamaica", "business ideas Jamaica", "business plan Jamaica free". Low-competition JA-specific keywords. $30–50/month test budget. Ad copy: 3 headlines + 2 descriptions per ad group. Landing page: /phase-packs. Conversion goal: pack download.

---

## [FW-2026-05-19-003] — Funding & Partners Map
**Stated:** 2026-05-19
**Context:** Deego requested a structured approach to seeking funding and strategic partners for MindWave/RAAS.
**Status:** pending

Build a one-document funding map: JBDC (Jamaica Business Development Corporation), DBJ (Development Bank of Jamaica), USAID Caribbean Open for Business, IDB Lab Caribbean, NCB Foundation. For each: what they fund, eligibility, application period, and the pitch angle from MindWave/RAAS. Strategic partners to pursue: TPDCo, JEA, Digicel Jamaica, NCB Foundation. Include outreach template for each.

---

## [FW-2026-05-19-004] — Email Subscriber List: Export and CRM Integration
**Stated:** 2026-05-19
**Context:** EmailCapture component deployed — subscribers saved to data/subscribers.json on VPS.
**Status:** pending

Once subscriber list has meaningful volume (50+), migrate from flat JSON file to a proper list management solution. Options: Resend Audiences (already using Resend for notifications), Mailchimp free tier, or ConvertKit. Build a simple admin route `/api/admin/subscribers` (password-protected) to view subscriber count and export CSV. Add subscriber count to homepage email capture section as social proof once 50+ reached.

---

## [FW-2026-05-19-005] — ADTL: Purchase Flow + Contract (Pre-Launch Gate)
**Stated:** 2026-05-19 (carried from prior sessions — marking here for visibility)
**Context:** ADTL page is live. No purchase flow exists yet. Deego noted "all artist sites must be complete before ADTL launch."
**Status:** pending

Build the ADTL purchase flow: intake form with mandatory callback scheduling, contract display (buyer assumes image/likeness rights), WiPay payment or deposit collection, confirmation email via Resend. Must be complete before any artist site is marketed or any ADTL price is publicly promoted.

---

## [FW-2026-05-19-006] — Ad Creative: Hook Series Reels (Per Pack Category)
**Stated:** 2026-05-19
**Context:** Round 2 ad concepts session. Deego specified: problem/solution Reels per pack category, compliance angle, proof-of-concept no-hype format.
**Status:** done 2026-05-21 — full production scripts at `playground/2026-05-ad-concepts/reel-scripts-production.md`

Produce 5 Instagram Reels scripts (video briefs + captions + CTA) from the hook series in `playground/2026-05-ad-concepts/mindwaveja-ad-concepts.md`: Nail Tech, Natural Juice, Mobile Catering, Compliance Angle (BSJ checklist), No-Hype Proof of Concept. Each Reel needs: exact hook text (0–3 sec), VO script or caption sequence, close card copy, CTA button label. Brief a videographer or record DIY. Geo: Kingston, MoBay, Spanish Town (primary), parish variants for Rural Ready.

---

## [FW-2026-05-19-007] — JBDC Grant Application
**Stated:** 2026-05-19
**Context:** Funding & partners session. JBDC identified as first-priority non-dilutive grant for MindWave JA / RAAS.
**Status:** pending

Apply to JBDC Innovation Grant (jbdc.net → Business Services → Grant Programme) and Innovate JA challenge. Angle: "Building Jamaica's first AI-grounded business intelligence platform for SMEs — 20+ free execution blueprints + live Jamaican speech dataset." Ask: J$500,000–1,500,000. Approach: in-person at JBDC Kingston office with a deck. Full strategy in `playground/2026-05-ad-concepts/funding-and-partners.md`.

---

## [FW-2026-05-19-008] — Phase Packs Paid Tier (Top 4 Renovated Packs)
**Stated:** 2026-05-19
**Context:** Revenue now moves — Phase Packs go paid at J$2,500 each after full renovation. Free packs remain as entry points.
**Status:** [cancelled] 2026-05-22 — Decision reversed. All phase packs are permanently free. Revenue model shifts to services, ADTL, and books. Data already reflects this (all packs have price: 0, tier: "free").

Move top 4 renovated packs to paid tier: pp-063 (Natural Juice), pp-049, pp-053, pp-054. Paid version adds: mentorship session option, premium download set, quarterly update, WhatsApp support first 30 days. Payment: WiPay. Build checkout flow on mindwaveja.com. At 20 sales/month: J$50,000/month baseline. Full strategy in `playground/2026-05-ad-concepts/funding-and-partners.md`.

---

## [FW-2026-05-19-009] — TPDCo Partnership Outreach
**Stated:** 2026-05-19
**Context:** Strategic partner with direct access to 500+ tourism businesses — the exact buyers for Rural Ready Phase Pack operators.
**Status:** pending

Contact TPDCo Tourism Linkages Network (tpdco.org). Pitch: "Rural Ready Phase Packs for Tourism Operators — co-promote to vendor/supplier network." Timeline: 2–3 month relationship-build before formal ask. Get to an in-person meeting first. Full strategy in `playground/2026-05-ad-concepts/funding-and-partners.md`.

---

## [FW-2026-05-19-010] — Renovate pp-049, pp-053, pp-054 to InvariantScore 13
**Stated:** 2026-05-19
**Context:** These three packs are required before paid tier launch and before the full ad campaign is credible. Each needs the same treatment as pp-063.
**Status:** pending

Full renovation of pp-049, pp-053, pp-054 per `PHASE_PACK_CHECKLIST.md` (13 Solobic invariants, INV-01 through INV-13). Each session: 18 canon files, 5 downloads, zip, full JSON update. Priority order: pack with most existing content first. Estimated 2–3 sessions per pack.

---

## [FW-2026-05-19-011] — "To My Son" Pre-Order Page
**Stated:** 2026-05-19
**Context:** Book is written (English + Amharic). Pre-orders needed before ad campaign can run. Deego wants to start collecting pre-orders now.
**Status:** pending

Build a dedicated pre-order page — either a route on mindwaveja.com (/to-my-son) or a standalone page. Minimum content: book description, one sample passage (bilingual), author note, email capture for pre-order list OR WiPay payment link for deposit. Include: publication timeline or "coming Q3 2026", author photo, book cover (or placeholder). Once page is live, ad concepts from `playground/2026-05-ad-concepts/full-ad-ecosystem.md` Section 5 can run.

---

## [FW-2026-05-19-012] — Book of Solobility Vol 1 Pre-Order Infrastructure
**Stated:** 2026-05-19
**Context:** Vol 0 is live at whatissolob.com. Vol 1 is in progress. Want awareness + pre-order ads.
**Status:** pending

Add a "Vol 1 Coming" section to whatissolob.com with email capture for pre-order notification. Optionally, extract one passage from the Vol 1 manuscript as a teaser. Ad concepts ready in `playground/2026-05-ad-concepts/full-ad-ecosystem.md` Section 4.

---

## [FW-2026-05-19-013] — Time-Check Public Waitlist Page
**Stated:** 2026-05-19
**Context:** Time-Check is live but invite-only. Ad campaign can't run until there's a public waitlist CTA to send traffic to.
**Status:** pending

Build a waitlist landing page at timecheck.mindwaveja.com (or a /waitlist route). Minimum: what it does, who it's for (Jamaican SME owners), email capture, "Get Early Access" CTA. Ad concepts ready in `playground/2026-05-ad-concepts/full-ad-ecosystem.md` Section 2.

---

## [FW-2026-05-19-014] — Melissa Relief Index: Self-Submission Flow
**Stated:** 2026-05-19
**Context:** Index is currently view-only. Adding a self-submit flow unlocks the "For Organisations" ad concept and increases data density organically.
**Status:** pending

Add a "Submit a Donation" form to mri.mindwaveja.com. Fields: organisation name, donation amount, parish, date, description/notes, contact email. Admin approval queue before entry goes live on the index. Once live, run Concept B from `playground/2026-05-ad-concepts/full-ad-ecosystem.md` Section 3.

---

## [FW-2026-05-19-015] — Artist Site Organic Ad Content (One Post Per Site Per Week)
**Stated:** 2026-05-19
**Context:** All 11 artist sites are live. Organic social posts are the lowest-cost way to build domain authority and fan traffic before paid ads.
**Status:** pending

Set up a weekly content schedule: one Instagram post per artist site per week. Format: site spotlight, discography highlight, or "did you know" about the artist. Post from the MindWave JA account but framed around the artist, NOT around ADTL. Goal: build geo-targeted traffic to each domain. Full artist list and site URLs in `CLAUDE.md` VPS inventory. Concepts per artist in `playground/2026-05-ad-concepts/full-ad-ecosystem.md` Section 6.

---

## [FW-2026-05-20-001] — Privacy Policy one-pager per site
**Stated:** 2026-05-20
**Context:** Cookie audit (2026-05-20) confirmed no consent banner is required — all sites use only strictly-necessary auth cookies (`HttpOnly`, `Secure`, `SameSite=Lax`, `__Secure-` prefix). However, several sites collect personal data (email, phone, TRN on earn) which DOES trigger Privacy Policy requirements under EU GDPR, UK GDPR, and Jamaica's Data Protection Act 2020.
**Status:** pending

Draft one Privacy Policy template, then deploy to each site at `/privacy` (or footer link). Required sections: data collected, why, who it's shared with (none for now except payment processors when applicable), how to delete an account, contact for data requests. Apply first to: earn-mindwaveja, mindwaveja.com (email capture), timecheck (after Phase 4). Static artist sites and Solob don't strictly need one yet (no data collection) but cheap to add. Cookie banner remains unnecessary as long as no third-party trackers are added.

---

## [FW-2026-05-20-002] — Produce merch designs from prompt library + Printify uploads
**Stated:** 2026-05-20
**Context:** Merch design system + per-artist prompt library written today at `playground/2026-05-merch-designs/merch-design-system.md` — 11 artists × ~3 products each (33 designs), plus MindWave brand merch (Phase Pack, Built for Jamaica, Solobility, To My Son). All designs spec'd to Printify's product catalog and pixel resolutions. Brand-DNA-aligned (each artist's palette already documented from their actual site source).
**Status:** prep complete 2026-05-21 — output folders created, quick-start at `playground/2026-05-merch-designs/IMAGE-GEN-SESSION.md`. Image generation step requires Claude.ai with image gen enabled (separate session). Resolve Part 7 open questions with Deego first (Printify account structure, photo rights, rolling papers partner).

Workflow (per `playground/2026-05-merch-designs/merch-design-system.md` Part 5):
1. Open Claude with image gen, paste one prompt at a time, save outputs to `playground/2026-05-merch-designs/outputs/{artist}/`
2. Upload to artist's Printify account, choose substrate, set $9–12 margin on tees / $14–20 on hoodies
3. Add `/merch` route on artist site linking to Printify store (existing ADTL rule)
4. Launch with 3 products per artist (T-shirt + Hoodie + 1 of: snapback/tote/mug)

Open questions logged in Part 7 of the doc: per-artist vs master Printify account, photo rights status per artist, non-Printify products (Chronic Law 1Law Papers needs alt fulfilment partner), MindWave Phase Pack merch timing, To My Son tee bundle-vs-standalone.

---

## [FW-2026-05-21-001] — MDM Performance: Product Images + Hero Video
**Stated:** 2026-05-21
**Context:** MDM Performance brand extension page built on malie-donn site. Product blueprint sections are stubs — need real photos. Hero video placeholder is a static gradient.
**Status:** pending

Drop into `active_apps/artise_sites/extracted.sites/malie-donn/public/`:
- `videos/mdm-hero.mp4` — looping dark garage/car video (no audio, <10MB compressed)
- Product images per item (prefix `mdm-`): splitter front/side, diffuser, V6 badge close-up, sticker pack flat lay, car mat top-down, performance tee ghost mannequin, mechanics jacket ghost mannequin
Image gen prompts written 2026-05-21 — see session notes. Once images are in, wire them into `MdmPerformance.tsx` PRODUCTS arrays.

---

## [FW-2026-05-21-002] — MDM Performance: About + Contact Section Content
**Stated:** 2026-05-21
**Context:** MDM top nav has "About" and "Contact" buttons. Both currently render a "Content coming soon" stub. Deego said he'd provide content shortly — deferred.
**Status:** pending (blocked on Deego providing copy)

Fill in the About section (MDM Performance brand story — Malie Donn Motors, the garage, the mission) and Contact section (WhatsApp / email / booking inquiry form in demo mode). About content should match the automotive-masculine MDM voice — Big Shoulders Display, terse, direct.

---

## [FW-2026-05-21-003] — Malie Donn Site: Deploy to VPS (port 7009)
**Stated:** 2026-05-21
**Context:** MDM Performance page + merch update complete locally. Site runs at port 3020. VPS slot is port 7009 / maliedonnmusic.com / mw-maliedonn container.
**Status:** pending (blocked on: ADTL checklist pass, MDM product images, About/Contact content)

Steps when ready:
1. Pass ADTL Site Checklist (`active_apps/artise_sites/ADTL_SITE_CHECKLIST.md`)
2. Compress any images >1MB with ffmpeg or squoosh
3. Push to GitHub repo (create if not exists: `HammazoneRecords/malie-donn-site`)
4. Add service to `/opt/mw/docker-compose.yml` (port 7009)
5. Wire Nginx vhost for `maliedonnmusic.com`
6. Certbot SSL
7. Verify 200 + HTTPS

---

## [FW-2026-05-22-001] — MWJournal: "This Day" Trajectory Feature (Dashboard)
**Stated:** 2026-05-22
**Context:** Deego asked for a daily trajectory widget on the Dashboard that plots the current day's forward path based on past same-day patterns. Three scenario tracks: (1) Best case — everything goes well, (2) Entropy — doing nothing, giving in, (3) Neutral/baseline — current trend. Each track is a labelled projection line or visual indicator, not a hard prediction.
**Status:** pending (requires aiService function + sufficient entry history to draw from)

Implementation notes:
- `aiService.analyzeTodayTrajectory(entries: DraylEntry[])` — filters past entries matching today's weekday, time-of-year window, and gate/sentiment patterns; returns three trajectory objects
- Each trajectory: `{ label: string; description: string; gateProbability: Record<GateName, number> }`
- Dashboard widget renders as a three-card strip with gate colour accents and probability bars
- Only shown when there are ≥5 past same-day entries to draw from; otherwise shows "Build more history" prompt
- No hard-coded predictions — all derived from actual entry patterns

---

## [FW-2026-05-22-002] — MWJournal: PWA → Windows App + Android App (Capacitor path)
**Stated:** 2026-05-22
**Context:** Deego wants the MWJournal PWA to convert to a Windows desktop app and an Android app with minimal frontend changes and no backend infrastructure changes. The app is currently a Vite + React SPA with localStorage. Goal: one codebase, three targets.
**Status:** pending (architecture planning done; implementation deferred)

Architecture decisions:
- **Android:** Use Capacitor (`@capacitor/core` + `@capacitor/android`). Wraps the Vite build as a WebView app. `npx cap add android` + `npx cap sync` — zero frontend change needed. localStorage maps to `@capacitor/preferences` for persistence. Capacitor plugins available for future native features (camera, notifications, etc.)
- **Windows:** PWA install path first (Edge/Chrome "Install as app" — no code change needed, already a PWA). If a proper MSIX/EXE is needed, use Electron with a thin wrapper around the Vite build. Electron main process just opens a `BrowserWindow` pointing at `dist/`. `package.json` scripts: `build:electron` → `vite build && electron-builder`.
- **Key rule:** All data stays in localStorage/IndexedDB — no server dependency added. The "backend" stays the client. This remains true for all three targets.
- When ready: create `capacitor.config.ts` at app root, add android/ folder to .gitignore, test on Android emulator (API 33+).

---

## [FW-2026-05-22-003] — MWJournal: Song Mode Full Implementation
**Stated:** 2026-05-22
**Context:** Entry modes (`'journal' | 'song' | 'note' | 'quick'`) are in the schema and `types.ts`, but the mode selector UI and Song Mode–specific display are not yet built.
**Status:** pending (schema ready; UI not started)

Song mode spec:
- In the new/edit entry form, a mode selector row appears below the toolbar (pill buttons: Journal / Song / Note)
- Song mode: `title` field becomes mandatory and is displayed as the primary reference (large, above the content area); timestamp is still attached
- In card view: song entries show the title prominently; content is the lyrics/body
- In ViewEntryPage: song mode shows title as h1 above the body; date/timestamp in subtitle position
- Journal mode (default): no title field; date is the primary reference
- Note mode: same as journal but with a shorter single-line title field (topic heading only)
- `entryMode` is already stored per entry; just needs the UI selector and conditional rendering

---

## [FW-2026-05-22-004] — MWJournal: Voice Capture (Deferred — Patois Lab Gate)
**Stated:** 2026-05-22
**Context:** Deego explicitly deferred voice capture until the Patois archetype / patwah lab is able to understand Jamaican Patois speech. Standard speech-to-text (Whisper, Web Speech API) is not culturally appropriate for the journal's primary use case — Deego writes/speaks in Patois.
**Status:** deferred (hard gate: patwah lab speech comprehension must be ready first — see FW-006, patwah lab work)

When the gate lifts:
- Web Speech API (`webkitSpeechRecognition`) for PWA; Capacitor microphone plugin for Android
- Patois post-processor runs the raw transcript through the patwah normaliser before storing
- Voice entries get `entryMode: 'voice'` and a microphone icon in the card footer
- Do NOT use standard cloud STT APIs (Whisper, AssemblyAI, Deepgram) as standalone — they will mangle Patois. Only viable as a first pass with Patois correction layer on top.

---

## [FW-2026-05-25-001] — Rapper Pipeline: Run Signal Type 8 on a Real Journal Entry [in-progress]
**Stated:** 2026-05-25
**Context:** Rapper pipeline integration completed (Signal Type 8 in journal-cowork-instructions.md, rapper_extractions.jsonl created). Verification step was not run — no live extraction has been done yet.
**Status:** pending

Process one complete journal entry from `drayl/drayl_journal/` through the Signal Type 8 step. Produce 3–5 RAP-YYYY-MM-DD-NNN entries in `rapper_extractions.jsonl`. Confirm: `lomi_check` and `vorak_check` contain specific reasoning (not labels), `shadow_risk` is correctly assigned, `publish_class: canon_candidate` only appears at confidence ≥ 0.8. This is the spec verification from the rapper-intake-spec.md.

---

## [FW-2026-05-25-002] — Alkaline: GEMINI-PROMPTS.md Entry Missing
**Stated:** 2026-05-25
**Context:** Alkaline site is live at alkalineonline.com (VPS port 7012). Site has 6 merch products. No entry exists in `playground/2026-05-merch-designs/GEMINI-PROMPTS.md`.
**Status:** pending

Create at least 3 Alkaline merch prompts (Al1 wordmark tee, Al2 cap embroidery, Al3 statement hoodie) matching the site's B&W color scheme (#FFFFFF crimson, #0a0a0a background). Alkaline brand DNA: Permanent Marker font, "Vendetta Gang" identity, street-aggressive energy but cleaner/minimalist than Skeng. Add to paste-order at top of GEMINI-PROMPTS.md.

---

## [FW-2026-05-25-003] — Karnage Site: Full Build Needed
**Stated:** 2026-05-25
**Context:** `active_apps/artise_sites/karnage/src/components/` only contains `WorkingDraftBanner.tsx`. Site folder and DNA scaffold exist (`1karnage.dna/`). Merch prompts (Kn1–Kn3) added this session.
**Status:** pending

Build out the Karnage site from the DNA scaffold (`1karnage.dna/karnagescaffold.html` + `karnageherovideo.mp4`). Brand: blood red #ff2a2a on jet black #0a0a0a, industrial angular typography, UK Dancehall fusion. Latest release: "Million A Dem" feat. Urban Gurillaz. Instagram: @1karnage_officially. Must pass ADTL checklist before VPS deploy.

---

## [FW-2026-05-26-001] — EchoBox: PTOI / Archetype Collision Matrix
**Stated:** 2026-05-26
**Context:** Patwah lab gap analysis — `collision_notes` field exists on all 16 archetypes but all are empty. User deferred full definition of PTOI to next session.
**Status:** pending — awaiting PTOI definition from Deego

New table needed: `archetype_collisions` — captures what happens when two archetypes interact (energy dynamic, who opens, who responds, power shift, outcome). Also needs UI in EchoBox Governance module. Block on: Deego to define what PTOI means in full (Patois Theory of Interaction vs archetype collision matrix vs both).

---

## [FW-2026-05-26-002] — EchoBox: Archetype Variant Engine
**Stated:** 2026-05-26
**Context:** Patwah lab gap analysis — no way to capture "how each archetype says the same thing differently."
**Status:** pending

Two new tables: (1) `canonical_utterances` — the base concept/scenario (e.g. "I'm not doing that", "I don't know"); (2) `archetype_phrase_variants` — one row per archetype per canonical utterance, with patois_text + tone + intensity + emotional_state + validated flag. This is the dataset backbone — 16 archetypes × N canonical utterances = training rows.

---

## [FW-2026-05-26-003] — EchoBox: Patwah Dataset Export Endpoint
**Stated:** 2026-05-26
**Context:** Patwah lab has dictionary, slang, corpus, responses — no way to export as training data.
**Status:** pending

New endpoint: `GET /api/patwah/export/training` — assembles all validated entries across all Patwah tables into JSONL format (instruction/input/output structure for fine-tuning). Filters by `validated = true`. Returns download.

---

## [FW-2026-05-26-004] — EchoBox: Journal Import UI Tab
**Stated:** 2026-05-26
**Context:** `POST /api/journal/import` and `/commit` endpoints built but no frontend — all interaction is via curl/script.
**Status:** pending

New tab in EchoBox UI: "Journal Import" — text area for pasting raw journal entry, source_file field, date picker, "Extract" button that calls `/api/journal/import` and shows a review panel (observations / patwah responses / rapper signals with edit/delete before commit), "Commit" button that calls `/api/journal/import/commit`.

---

## [FW-2026-05-25-004] — Black Revelationz Site + Merch Prompts
**Stated:** 2026-05-25
**Context:** `active_apps/artise_sites/black-revelationz/` folder exists but has no meaningful site content and no GEMINI-PROMPTS.md entry.
**Status:** pending — needs brand discovery session first

Needs: (1) brand DNA discovery (colors, energy, genre, social links), (2) site scaffold in the artise_sites pattern, (3) at minimum 3 GEMINI-PROMPTS.md entries. Block on brand info from Deego.

---

## [FW-2026-05-24-001] — MWJournalX: Complete Remaining Theme Violations
**Stated:** 2026-05-24
**Context:** Theme consistency audit started this session — 54 violations across 14 files. 8 files fixed. Remaining: MoodCharts (hex SVG colours), ShimmerTimeline (hardcoded progress bar gradients), RelatedEntriesSidebar (1 violation), PasswordPrompt (2 violations), HighlightedText (1 violation), WritingQuality progress bars (hardcoded green/blue/orange gradients).
**Status:** pending

Remaining work:
- `MoodCharts.tsx` — hex colour values in SVG `fill`/`stroke` attributes → `hsl(var(--success))` / `hsl(var(--destructive))` / CSS vars
- `ShimmerTimeline.tsx` — `bg-gradient-to-b from-indigo-600/50 to-purple-600/50` timeline connector → `bg-gradient-to-b from-primary/50 to-secondary/50`
- `WritingQuality.tsx` — progress bars: `bg-gradient-to-r from-green-600 to-green-400` → `bg-success/80`, `from-blue-600 to-blue-400` → `bg-primary/80`, `from-orange-600 to-orange-400` → `bg-warning/80`
- `RelatedEntriesSidebar.tsx`, `PasswordPrompt.tsx`, `HighlightedText.tsx` — 4 remaining violations (need scan to confirm exact lines)

---

## [FW-2026-05-24-002] — MWJournalX: ZeroFrequency Word Cloud Upgrade
**Stated:** 2026-05-24
**Context:** ZeroFrequency component built this session as a horizontal bar list. Functional but visually flat.
**Status:** pending

Upgrade the frequency view from a bar list to a word cloud (proportional text size) with colour-coded layer attribution. Words sized proportional to count. Layer colour applied to text. Clicking a word filters the Drayl entry list to entries where that word appears in any Zero layer.

Implementation: SVG word cloud or CSS-only proportional sizing. Keep bar list as fallback for accessibility.

---

## [FW-2026-05-24-003] — MWJournalX: Zero Retrieval Phrases → Drayl Search
**Stated:** 2026-05-24
**Context:** Zero extracts `retrieval_phrases` — how the author might search for the entry later. These are sitting in ZeroIndexDisplay as passive chips.
**Status:** pending

Make retrieval phrases clickable. Clicking a phrase in the Zero Index panel should set the Drayl search bar to that phrase and navigate to the entry list. This makes Zero's retrieval layer actionable — not just descriptive. Implementation: pass an `onSearch?: (phrase: string) => void` prop from DraylPage through ViewEntryPage to ZeroIndexDisplay.

---

## [FW-2026-05-26-005] — RAAS Interest-Capture System (multi-session backend buildout)
**Stated:** 2026-05-26
**Context:** Eye-Donia brand extension page on Aidonia ADTL site — Deego asked for pre-order interest capture per product, generalized as a reusable RAAS-wide system. V1 of the React component (`<PreOrderCapture>`) and per-site catalog (`raas-catalog.ts`) shipped this session as a `console.log` stub. Backend not yet built.
**Status:** in-progress (Phases 1–5 complete; Phase 6 pending)

**The reporting questions the system must answer (definitively):**
1. "N people interested in product X from location L willing to pay tier T"
2. "Artist R has N interested across X products in location L"
3. "N also said yes to general branded merch from this artist"

**Architecture — already decided:**
- DB: new dedicated Postgres container `mw-raas-db` (NOT shared with Time-Check or earn)
- API: Express service `mw-raas-api` on port 4000, behind Nginx at `raas-api.mindwaveja.com`
- Component: `<PreOrderCapture productId="..." />` reads from per-site `src/raas-catalog.ts` (single source of truth for products + variants + price tiers)
- Mailing lists STAY SEPARATE per artist — no cross-artist promo, no cross-promotion anywhere. Per-site only.
- V1 fields: email, location (parish/city), variant (from catalog dropdown), price tier (from catalog radio), branded-merch-interest checkbox (same artist only)
- No confirmation email in V1 — just store the signup
- Success UX: inline thank-you only ("Interest Logged"). No add-another-product upsell. No share buttons.

**Schema (committed):**
```sql
CREATE TABLE interest_signups (
  id UUID PRIMARY KEY,
  site_slug TEXT NOT NULL,
  artist_name TEXT NOT NULL,
  product_id TEXT NOT NULL,
  product_name TEXT NOT NULL,
  variant TEXT,
  email TEXT NOT NULL,
  location TEXT NOT NULL,
  country TEXT,
  price_tier_key TEXT NOT NULL,
  price_tier_label TEXT NOT NULL,
  branded_merch_interest BOOLEAN DEFAULT FALSE,
  referral_source TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(site_slug, product_id, email)
);
CREATE INDEX idx_site_product_location ON interest_signups(site_slug, product_id, location);
CREATE INDEX idx_artist_location ON interest_signups(artist_name, location);
CREATE INDEX idx_price_tier ON interest_signups(price_tier_key);
```

**Build sequence (remaining):**
1. **Phase 3** — Postgres container on VPS + schema migration (`vps_management/docker/`)
2. **Phase 4** — Express API service `mw-raas-api` on port 4000 with `POST /v1/interest`, `GET /v1/owner/:siteSlug/summary`, `GET /v1/admin/all` + Nginx route at `raas-api.mindwaveja.com`. New app folder: `active_apps/raas-api/`
3. **Phase 5** — Wire `<PreOrderCapture>` to live endpoint via `VITE_RAAS_API` env var, replace `console.log` stub. Update for every artist site that has a brand extension.
4. **Phase 6** — Owner dashboard at `mindwaveja.com/owner` (magic-link email auth, ADTL buyer sees their slice) + admin dashboard at `mindwaveja.com/raas-admin` (Deego-only, sees all artists). CSV export.

**ADTL pitch upgrade:** once Phase 6 ships, ADTL buyers don't just get a site — they get a live "audience-listening engine" showing every signup, every product interest, every size/variant preference, every price tolerance. Adds significant value to the $5,200 ADTL price point.

**Already shipped (Phases 1–5, sessions 2026-05-26 + 2026-05-31):**
- Phase 1–2: `aidonia-_-4th-genna/src/raas-catalog.ts`, `PreOrderCapture.tsx` (console.log stub), EyeDonia.tsx updated
- Phase 3: `mw-postgres` container reused; `raas_capture` DB + `interest_signups` table created via auto-init in API
- Phase 4: `active_apps/raas-api/` — Express + pg, `POST /v1/interest`, `GET /health`; deployed to VPS port 4000; SSL at `raas-api.mindwaveja.com` via Let's Encrypt; Nginx conf added; docker-compose.yml updated
- Phase 5: `VITE_RAAS_API` build arg wired into Chronic Law, Aidonia, Jada Kingdom containers; `PreOrderCapture.tsx` stubs replaced with live endpoint call; Jada Kingdom brand extensions section shipped (Twinkle cologne + Twinkle Palette)

**Reusability gotcha:** the component currently imports `SITE_SLUG`, `ARTIST_NAME`, `getProduct` from `'../raas-catalog'`. Copy this file pattern when adding the component to a new artist site — each site keeps its own catalog file at `src/raas-catalog.ts`. Don't centralize.

---

## [FW-058] — Hermaphrodite Realization + Cambrian thought-thread (capture next session)

**Captured:** 2026-05-29
**Trigger:** Cambrian explosion explanation (during STOI002 Cambria book idea conversation)

Deego had a "hermaphrodite realization" he wants to unpack next session. He mentioned it but did NOT share the content — only flagged it for capture. **Do not reconstruct from speculation.** Ask him directly.

**Session-handoff prompt for tomorrow:** *"After American Dreams Vercel/Supabase migration is up and running — ask Deego about his hermaphrodite realization."*

**The breadcrumb chain that led to it (preserve order — this IS the revelation order):**

1. Cambrian explosion explained (origin of body plans, all phyla emerged underwater ~538 mya)
2. → Triggered hermaphrodite realization (content pending Deego)
3. → "made me wonder about... [trailed off — didn't remember]"
4. → Trilobites (couldn't remember what led to them — likely a sub-thread from the wondering)
5. → Animals without eyes
6. → Specifically prompted by: a video of a fish with **just a stomach and a mouth** — no eyes, no other organs visible
7. Source video: https://www.youtube.com/watch?v=7STmcKCBI_0

**Why this matters:** The chain itself is the data. Cambrian → hermaphrodites → trilobites → eyeless animals → minimal-body-plan fish is a *thought trajectory* about what's necessary vs. accessory in a living body. The "hermaphrodite realization" sits inside that frame — likely something about reproductive simplicity, single-form sufficiency, or the origin of binary sex from a non-binary ancestor. **But that is speculation — let Deego state it.**

**Possible linkages to track once realization is captured:**
- STOI002 Cambria book — undersea archetypes, traits' origins
- Solobic principle: Origin over Outcome
- Insight registry — if the realization holds up to scrutiny it likely deserves an INS- entry

---

## [FW-059] — Solob Wrapper: True Two-Pass Response Linter

**Captured:** 2026-05-29
**Origin:** CLAUDE.md embryo renovation session. The Pre-Response Color Check (5 binary checks in root CLAUDE.md) is the best available approximation within a static instruction file, but it is not a real linter — it shapes generation mode, it doesn't check output after the fact.

**What this is:** A two-pass response system where Claude generates a draft internally, runs the color neutralizer (mw_29) against it, then outputs the clean version. Analogous to a compiler running a pass over intermediate representation before emitting bytecode.

**Why it matters:** The shimmer test (mw_35) failed twice with the same pattern — "That's a shimmer" appeared even after the constraint was written in the same file. Single-pass generation means the definition fires and the response begins before the constraint arrives. A true linter needs the full output to check.

**Implementation requires one of:**
- Enforced chain-of-thought reasoning step (think-before-respond mode, currently not consistently available in CLAUDE.md-driven sessions)
- External hook or middleware that intercepts Claude's response, evaluates it against C05 trigger table, and re-prompts if violations are detected
- Claude Code hook (post-response) — possible with Claude Code hooks system if it matures to support response interception

**Status:** pending — blocked on tooling. Log for next review when Claude Code hooks or CoT enforcement becomes configurable.

**Related:** `subclaude/subclaude_C05_invariant-trigger-table.md`, `playground/2026-05-claude-md-overhaul/drafts/CLAUDE_root_draft.md`

---

## [FW-060] — Add Behavioral Constraint to drayl_orientation.md Governance Section

**Captured:** 2026-05-29
**Origin:** CLAUDE.md embryo renovation session. Structural gap identified in `drayl/drayl_orientation.md`: Governance section states "high-security zone — personal reflections" but has NO behavioral rule for handling forming/raw journal content.

**The gap:** Raw journal entries are shimmers in written form — pre-language, mid-formation. The same handling rules that apply to spoken shimmers (reflect, don't extract, don't interpret as settled positions) must also apply to drayl content. Without this, Claude will read a journal entry describing a forming idea and respond with extraction/interpretation — the same mw_35 failure pattern.

**Fix required:** Add to Governance section in drayl_orientation.md:
> Raw journal entries are forming thought — shimmers in written form. Do not extract or interpret them as settled positions. Handle as shimmers: reflect the words back, do not name the concept, do not promote to insight without user confirmation.

**Status:** pending — also needs a draft created at `playground/2026-05-claude-md-overhaul/drafts/CLAUDE_drayl_draft.md` (copy of drayl_orientation.md + constraint added).

**Related:** INS-095, `subclaude/subclaude_C05_invariant-trigger-table.md`, `playground/2026-05-claude-md-overhaul/drafts/CLAUDE_root_draft.md`

---

## [FW-061] — RAAS Owner + Admin Dashboard
**Stated:** 2026-05-31
**Context:** RAAS interest-capture Phase 6 — completing the full loop so buyers can see their data
**Status:** pending

Two routes off mindwaveja.com:
- `mindwaveja.com/owner` — magic-link email auth; ADTL buyer sees their own artist slice (signups, products, locations, price tiers, merch interest). No cross-artist visibility.
- `mindwaveja.com/raas-admin` — Deego-only gate (env-var secret or hardcoded allow-list); sees all artists, all products, full dataset. CSV export per artist + full export.

API endpoints already scaffolded: `GET /v1/owner/:siteSlug/summary`, `GET /v1/admin/all` — implement these when dashboard is built.

**ADTL pitch upgrade:** once Phase 6 ships, ADTL buyers get a live "audience-listening engine" — every signup, product interest, variant preference, price tolerance. Adds material value to the $5,200 price point.

**Blocked on:** raas-api GitHub repo (FW-062) so dashboard can make authenticated calls cleanly. Not strictly blocked, but cleaner once that's done.

---

## [FW-062] — RAAS API: Create GitHub Repo + Move to Git-Pull Workflow
**Stated:** 2026-05-31
**Context:** `mw-raas-api` was built and deployed via SCP (no GitHub remote). Current update workflow requires SCP copy to VPS, then restart. Fragile and not documented-as-process.
**Status:** pending

Create `HammazoneRecords/mw-raas-api` GitHub repo. Push current `active_apps/raas-api/` content. On VPS, replace `/opt/mw/raas-api/` with a git clone. Update APPS.md deploy procedure to `git pull origin main` + `docker compose restart raas-api`.

**VPS path:** `/opt/mw/raas-api/`
**Current deploy:** SCP from local → restart container
**Target deploy:** `git pull origin main` → `docker compose restart raas-api`

---

## [FW-063] — Wire RAAS Interest Capture to Remaining ADTL Artist Sites
**Stated:** 2026-05-31
**Context:** PreOrderCapture is currently on 3 sites (Chronic Law, Aidonia, Jada Kingdom). 17 other ADTL artist domains exist. Each needs its own raas-catalog.ts + PreOrderCapture in whichever section has brand/merch extensions.
**Status:** pending

Sites already wired: `chronic-law-official`, `aidonia-_-4th-genna`, `jada-kingdom`

Sites pending (add raas-catalog + wire component when brand extension or merch section is built):
Skeng, Jahshii, Bounty Killer, Tarrus Riley, Alkaline, Karnage, and remaining 11 ADTL domains.

**Pattern to follow:** copy `raas-catalog.ts` from any live site, update SITE_SLUG, ARTIST_NAME, PRODUCTS array. Copy PreOrderCapture.tsx and restyle to match artist design system. Update Dockerfile with ARG VITE_RAAS_API block. Update docker-compose.yml args block. Rebuild container.

---

## [FW-2026-06-01-001] — Pop Booth: Sellable Mobile Beauty Station Kit
**Stated:** 2026-06-01
**Context:** Deego built a hatch-anchored pop-out canopy booth for Shan (mobile lash tech) using an existing tent + cut poles. MVP confirmed working same day (photo documented). Immediately recognized as a sellable product for the mobile beauty market.
**Status:** pending
**Full spec:** `ideas/product_innovation_idea/PRODI002-Pop-Booth-Mobile-Beauty-Station/PRODI002-Pop-Booth-Mobile-Beauty-Station.md`

**Next steps:**
- Photo the MVP in detail (joints, window panel, anchor points)
- Measure exact dimensions for production spec
- Price out materials for production-quality unit (proper fabric, powder-coated poles)
- Set up Etsy listing with MVP photos to validate demand
- Film setup video (Shan deploys it — target sub 10 min)
- Name decision: "Pop Booth" vs "The Boot" vs other

---

## [FW-2026-06-01-002] — Skatta Select: Riddim Submission & Vote Platform (Brand Extension)
**Stated:** 2026-05-06, 7:35pm (journal)
**Context:** Deego was building repos for remaining ADTL artists and stated this idea as the right brand extension for Skatta — bigger than selling VSTs or beatpacks. His impact needs to be greater.
**Status:** pending
**Full concept:** `active_apps/artise_sites/scatta-burrell.dna/scatta-burrell.dna/scattaburrel-dna.md` (Brand Extension — Revised Concept section)

Skatta opens a public submission window for his next riddim juggling. Artists submit video links. Public votes. < 20 upvotes in 2 days → auto-removed. Top entries survive and get officially included on the released riddim. The platform turns every juggling release into a community event. Skatta's site becomes the A&R engine.

**Feature spec needed:**
- Submission form (video URL + artist name + contact)
- Public voting mechanism (upvote only, no downvote — IP or account gated)
- Auto-removal cron: check every 24h, remove entries under threshold
- Admin dashboard: Skatta sets the threshold, submission window open/close, final selection
- Countdown timer for submission window
- Live leaderboard of top entries

---

## [FW-2026-06-01-003] — ADTL Artist GitHub Repos — Remaining Artists
**Stated:** 2026-05-06, 7:05–7:11pm (journal)
**Context:** Deego built repos for remaining artists while conceptualizing products. Also added ROJ + RAL review apps to the list.
**Status:** repos created, sites not yet built

Repos created 2026-05-06:
- `HammazoneRecords/mavadogullyside` — Mavado
- `HammazoneRecords/dingdongravers` — Ding Dong
- `HammazoneRecords/rajahwildofficial` — Rajah Wild
- `HammazoneRecords/rojreviews` — ROJ Reviews (under free product tier w/ Time Check)
- `HammazoneRecords/ralreviews` — RAL Reviews (same)

ROJ + RAL → going under free product alongside Time Check (not standalone).

---

## [FW-2026-06-01-004] — ADTL Milestone Log: Sites Live
**Stated:** 2026-05-06, 6:50–6:53pm (journal)
**Context:** End of day count. Updated 2026-06-01 with current state.
**Status:** milestone — living record

**As of 2026-05-06 (journal entry):** 11 VPS + Jah Vinci (Vercel) = 12 total

**As of 2026-06-01 (current):** 12 VPS + Jah Vinci (Vercel) + Alkaline (VPS, domain TBD) = 13 total

VPS sites (skattaburrell.com · 7006):
1. chroniclawmusic.com (7004)
2. skengdon.com (7001)
3. busysignalturf.com (7010)
4. elainethompsonherah.com (7011)
5. tarrusrileyja.com (7002)
6. officialbountykiller.com (7007)
7. aidonia4thgenna.com (7005)
8. maliedonnmusic.com (7009)
9. jadakingdommusic.com (7008)
10. officialjashiimusic.com (7003)
11. skattaburrell.com (7006)
12. alkaline (7012 — VPS live, domain TBD)

Other:
13. jah-vinci-homepage.vercel.app (Vercel — not VPS)

---

## [FW-2026-06-02-001] — Skengergy Hero HTML — Polish + Use as Live Hero
**Stated:** 2026-06-02
**Context:** Attempting to recreate the Skengergy hero image (dark concrete bunker, massive SKENGERGY text split white/red, pedestal + can) using HTML/CSS/SVG. User confirmed "better" on the text-only version (no can) with SVG feTurbulence concrete texture + stacked shadow extrusion.
**Status:** in-progress

Current file: `playground/2026-06-adtl-ads/skengergy-hero.html`
Approach: SVG feTurbulence + feDisplacementMap for rough edges, feBlend multiply for surface grain, stacked text-shadow for 3D extrusion. Can removed — text study in progress.
Next: refine text until it matches original closely enough to use as the Skengdon site hero section.

---

## [FW-2026-06-02-002] — Elaine Thompson Site — VPS Deploy (Merch Section)
**Stated:** 2026-06-02
**Context:** Merch section added to Elaine Thompson site this session (Merch.tsx, App.tsx, Nav.tsx updated; hanging-1-cutout.png added). Not yet committed or deployed.
**Status:** pending

Steps: `git add` relevant files → commit → `git push origin master` → VPS pull + docker compose build/up for `mw-elainethompson`.

---

## [FW-2026-06-03-001] — Teejay Hero Video Replacement
**Stated:** 2026-06-03
**Context:** Downloaded first 30s of Drift (from 10s mark) as hero video for teejay-uptopboss. User noted too much B-roll in the current clip.
**Status:** pending

Find a better video clip or cut — ideally a performance or close-up shot with strong visual energy. Drop new file into `active_apps/artise_sites/teejay-uptopboss/public/drift-hero.mp4`.

---

## [FW-2026-06-03-002] — Domain Registrations: Nhance, Teejay, Valiant
**Stated:** 2026-06-03
**Context:** Nhance and Teejay sites built but no domains registered yet. Valiant also in queue.
**Status:** pending

Register domains for all three before Jul 26, 2026 (existing domains expire). Then connect each domain to its site on VPS deploy.

---

## [FW-2026-06-03-003] — Jah Vinci Domain — Link to Oreluva Build
**Stated:** 2026-06-03
**Context:** Jah Vinci site already built by Oreluva in Benin. Domain: realjahvinci.com (Namecheap, expires Jul 26 2026).
**Status:** pending

Point realjahvinci.com DNS to Oreluva's hosting. Confirm with Oreluva this week.

---

## [FW-2026-06-03-004] — Brand Extensions: Nhance + Teejay (Define + Build)
**Stated:** 2026-06-03
**Context:** Both Nhance and Teejay sites built without brand extension pages. Extensions not yet defined.
**Status:** pending

Define brand extensions for both artists when back from work. Then build /[extension] routes and add to their sites + ADTL_brand_business_plans.md.

---

## [FW-2026-06-03-005] — Hero Images: RajahWild + Ding Dong
**Stated:** 2026-06-03
**Context:** Both sites built without hero images. ADTL rule requires portrait (mobile) + landscape (desktop) crops.
**Status:** pending

Source from official Instagram or YouTube thumbnails. Drop into /public/ and wire into hero section. File naming: `[artist]-hero-portrait.jpg` / `[artist]-hero-landscape.jpg`.

---

## [FW-2026-06-03-006] — Grung Gaad Site — Build (deferred)
**Stated:** 2026-06-03
**Context:** Domain grunggaadzilla.com owned. Currently served by Bounty Killer nginx but no dedicated site. User said to do after other artists.
**Status:** pending

Build dedicated Grung Gaad site. Separate it from the Bounty Killer nginx config. Assign port 7020+ on VPS.

---

## [FW-2026-06-03-007] — Push Nhance + Teejay to GitHub (repos pending)
**Stated:** 2026-06-03
**Context:** Both sites committed locally. Waiting on GitHub repo URLs from user.
**Status:** pending

User to create repos at HammazoneRecords. Paste URLs and push. Then add to APPS.md (Nhance port 7020, Teejay port 7021).

---

## [FW-2026-06-03-008] — Ding Dong Doorbell — Smart Doorbell Brand Extension
**Stated:** 2026-06-03
**Context:** User observed that "Ding Dong" literally works as a smart doorbell brand name (motion detection, phone alerts, talk to delivery people, internet connected)
**Status:** pending

Add `/doorbell` brand extension route to the Ding Dong Ravers site. Product concepts page (not merch). Add 4 product prompts to GEMINI-PROMPTS.md (unit design, packaging, app UI mockup, promo graphic). Brand name: "Ding Dong Doorbell." See INS-108.

---

## [FW-2026-06-03-009] — APPS.md + VPS Deploy — DNS Added for New Sites
**Stated:** 2026-06-03
**Context:** User confirmed DNS added for all previously domain-TBD sites + two new domains: majormarketing and officialtravelandtours
**Status:** pending

Update APPS.md domain column for: Skippa Don, Nhance, Teejay, Pablo YG, Karnage, Black Revelationz, Alkaline (all previously marked domain TBD). Add new rows for `majormarketing` (port TBD, 7024+) and `officialtravelandtours` (port TBD). Then deploy all newly-domained sites to VPS — git push → VPS pull → docker compose build → nginx config + certbot SSL for each domain.

---

## [FW-2026-06-03-010] — majormarketing.com + officialtravelandtours.com — New Sites to Build
**Stated:** 2026-06-03
**Context:** User added DNS for these domains. Sites do not exist yet.
**Status:** pending

Two new client sites to build. Need: scope call / brief from user before starting. Assign VPS ports 7024 and 7025. Create site folders under `active_apps/artise_sites/` or `active_apps/` depending on type. Add to APPS.md when ready.

---

## [FW-2026-06-04-001] — officialtours.com — Co-worker travel & tours site
**Stated:** 2026-06-04
**Context:** User mentioned building two new sites — majormarketingja (Romiech Entertainment) and officialtours (co-worker's travel and tours business). majormarketingja was built this session. officialtours is still pending.
**Status:** pending

Build officialtours.com — co-worker's travel and tours business site. Stack: Next.js + Tailwind + next-themes (per artise_sites CLAUDE.md stack decision rule). Get brief/scope from user before starting. Assign VPS port.

---

## [FW-2026-06-04-002] — Deploy mindwaveja.com video/poster fix to VPS
**Stated:** 2026-06-04
**Context:** Hero video compressed (1.7MB → 616KB) + poster frame added + HeroRevealPlaceholder.tsx updated with `poster` attr and `preload="metadata"`. Fix sitting in local branch, not yet deployed.
**Status:** pending

Push HeroRevealPlaceholder.tsx changes + `herobkgvideo-compressed.mp4` + `herobkgvideo-poster.webp` to VPS. Rebuild container. Run GTmetrix again — LCP target: under 1.5s. See INS-111.

---

## [FW-2026-06-04-003] — Cloudflare setup for mindwaveja.com
**Stated:** 2026-06-04
**Context:** GTmetrix flagged HTTP/1.1 for all 25 resources (1.4s potential savings), no CDN, and http→https redirect. Cloudflare free tier fixes all three with one DNS change.
**Status:** pending

Steps: cloudflare.com → Add Site → enter mindwaveja.com → import DNS records → change nameservers at registrar → SSL/TLS: Full (strict) → Speed: enable HTTP/2, HTTP/3, Brotli → Caching: 1yr TTL for static. No VPS changes needed.

---

## [FW-2026-06-04-004] — majormarketingja-next VPS deployment
**Stated:** 2026-06-04
**Context:** majormarketingja-next (Next.js + next-themes, port 5201) fully built with 5 pages, service onboarding flows, roster booking. Sitting at active_apps/majormarketingja-next/. Not yet on VPS.
**Status:** pending

Create GitHub repo, add to APPS.md, write Dockerfile, add nginx route, SSL cert. Domain: majormarketingja.com (TBD — confirm domain ownership). Clean up the empty Vite version at active_apps/majormarketingja/ (or vault it).

---

## [FW-2026-06-04-005] — Ding Dong site VPS deployment
**Stated:** 2026-06-04
**Context:** Ding Dong site has major changes this session: hero video, preload video with fade, Moves lesson cards, DRAFT watermark, Ravers section with 8 real members + Instagram links, Meet The Ravers CTA. All local only.
**Status:** pending

Push all ding-dong-ravers changes to VPS. Confirm domain dingdongravers.com routes correctly. Test hero video loads, preload plays, Badman Forward lesson video works.

---

## [FW-2026-06-04-006] — ovandobrown.com — review current state and define next steps
**Stated:** 2026-06-04
**Context:** ovandobrown.com project found at PROJECTS IN MOTION/ovandobrown.com/ — Next.js 15 + GenKit AI + Firebase, named "nextn". Pulled up locally on port 3000. Content/design direction not yet discussed.
**Status:** done — two design versions built this session (see FW-2026-06-04-007)

---

## [FW-2026-06-04-007] — ovandobrown.com — pick design, push to GitHub, deploy to VPS
**Stated:** 2026-06-04
**Context:** Two design versions built at active_apps/ovandobrown/ on separate branches. V1 = Architect's Index (Geometric Lattice). V2 = The Cosmology (VORAK→KHEM→ORON). Both build clean.
**Status:** pending

1. Run `pnpm dev` on each branch, pick one (or merge elements)
2. Create GitHub repo under HammazoneRecords/ovandobrown
3. Push chosen branch to main
4. Write Dockerfile + add to docker-compose.yml on VPS
5. Add nginx config, Certbot SSL for ovandobrown.com
6. Add to APPS.md

---

## [FW-2026-06-04-008] — ovandobrown.com — wire AI query route (DeepSeek via ark.local)
**Stated:** 2026-06-04
**Context:** Version A (Architect's Index) has a Connect section with an AI query interface stubbed. Route file not built — waiting on ark.local key details.
**Status:** pending

Build `src/app/api/query/route.ts` — POST handler calling DeepSeek API, key from `ark.local`. Wire into the Connect component's query input. Add `DEEPSEEK_API_KEY` to `.env.local`.

---

## [FW-2026-06-04-009] — ovandobrown.com — real assets (music file, photos)
**Stated:** 2026-06-04
**Context:** Music player in V1 references `/public/music/signal.mp3` (placeholder). No photos of Deego are wired in either version.
**Status:** pending

Add real music track to `/public/music/`. Add a real photo (or silhouette asset) for V2 hero if particle field alone isn't enough. Update `src/content/ovando.ts` with real project URLs for RAAS, Time-Check, Book.

---

## [FW-2026-06-04-010] — RUNNING_FILE.md — file 11 artist DNA profiles
**Stated:** 2026-06-04
**Context:** RUNNING_FILE.md contains full 10-axis DNA for: Alkaline, Bounty Killer, Jada Kingdom, Mavado, Aidonia, Busy Signal, Ding Dong, Malie Donn, Skatta Burrell, Jah Vinci, Rajah Wild. All unprocessed.
**Status:** pending

File each to `active_apps/artise_sites/[artist-slug]/artist_dna.md`. Clear RUNNING_FILE.md after all 11 are filed. Note: Malie Donn and Aidonia already have artist_dna.md — check for overlap before overwriting.

---

## [FW-2026-06-08-001] — Create a new MindWave website
**Stated:** 2026-06-07
**Context:** Mentioned in passing while redirecting toward the ovandobrown.com review — scheduled for tomorrow.
**Status:** pending

Build a new MindWave website. No further spec given yet — confirm scope/purpose with Deego when picked up tomorrow (2026-06-08).

---

## [FW-2026-06-04-011] — Favicons for all artist sites
**Stated:** 2026-06-04
**Context:** User noted during Ding Dong deploy — all artist sites need favicons. Deferred to a dedicated session.
**Status:** pending

Add favicons to all ADTL artist sites. Each should reflect the artist's brand identity (not a generic MW icon). Suggested: use a letter/monogram or brand mark from the artist's color palette. Add to ADTL_SITE_CHECKLIST.md as a required item.

---

## [FW-2026-06-04-012] — Add Umami tracking to all existing artist sites
**Stated:** 2026-06-04
**Context:** Umami rule added to artise_sites CLAUDE.md + ADTL_SITE_CHECKLIST.md. Existing sites were built before the rule existed.
**Status:** pending

For every artist site in \ctive_apps/artise_sites/\ that does NOT already have the Umami script in its \index.html\: create a new Website entry in Umami (stats.mindwaveja.com → Settings → Websites), get the UUID, add the script tag to \<head>\ in \index.html\. Self-hosted URL: \https://stats.mindwaveja.com/script.js\. Credentials in \rk.local\. Commit + redeploy each site after adding. Sites to audit: Skeng, Tarrus Riley, Jahshii, Chronic Law, Aidonia, Skatta Burrell, Bounty Killer, Jada Kingdom, Malie Donn, Busy Signal, Elaine Thompson, Alkaline, Karnage, BRZ, Ding Dong (just deployed — add before next deploy), Mavado, Kraff, Pablo YG, RajahWild, Nhance, Teejay, Jamal.

---

## [FW-2026-06-08-002] — Self-hosted cloud storage for obblog (images + files)
**Stated:** 2026-06-08
**Context:** Removing Sanity + Firebase from obblog — needed a home for uploaded images/files that persists across Docker rebuilds
**Status:** pending

Set up self-hosted object/file storage for obblog and potentially other MW apps. Two paths: (1) MinIO — S3-compatible, Docker-deployable on VPS, single container, bucket-based — recommended for scale: one shared service all apps point to (VPS port 9000/9001, volume at /opt/mw/minio-data/). (2) Simple VPS bind mount at /opt/mw/obblog-uploads served by Nginx as static files — less overhead, no extra container. In the interim, obblog Docker compose needs: "- /opt/mw/obblog-uploads:/app/public/uploads" so uploads survive container rebuilds.

## [FW-2026-06-09-001] — ovandobrown.com — Deego / Sky Boss Mode Toggle
**Stated:** 2026-06-09
**Context:** Discussing mindwaveja-v2 layouts — Deego described wanting a personality toggle on ovandobrown.com, like dark/light mode but it switches between professional OB and the raw/cultural Deego/Sky Boss persona
**Status:** pending

Add a mode toggle to ovandobrown.com that switches the entire site personality — not just a color theme. "Professional" mode = Ovando Brown, clean/formal, portfolio/work framing. "Deego / Sky Boss" mode = raw, cultural, personal, Patois welcome, different copy/tone/visuals. Implemented like a dark/light toggle (button in nav, persisted to localStorage) but the swap is copy + tone + possibly color scheme — not just CSS variables. Both modes share the same routes and structure; the content layer swaps. Consider: same component tree, `mode` context injected at root, all copy as objects keyed by `{ ob: '...', deego: '...' }`.

## [FW-2026-06-09-002] — mindwaveja-v2 — Offering Bubbles: Round + Detailed
**Stated:** 2026-06-09
**Context:** Building the remote-control layout (layout-b-structure.html) — the three offering options (Phase Packs, Artist Sites, Digital Presence) are floating bubbles that drift in over the remote panel when "Explore Offerings" is clicked
**Status:** pending

When transmuting layout-b to the real Vite v2: the three offering bubbles must be **round** (pill or circle shape, not rectangles). In the prototype they are compact rectangular cards. The full build should make them rounder and more detailed — richer content inside each bubble (e.g. icon, short stat, hover expand). Placement: float over the left/remote panel only, not the display. Bob animation stays.

---

## [FW-2026-06-09-003] — mindwaveja-v2 — Full Vite+React+TS Build
**Stated:** 2026-06-09
**Context:** HTML prototype complete (layout-b-structure.html). Plan written to workspace. Ready to transmute to production stack.
**Status:** in-progress

Full build of mindwaveja-v2 in Vite+React+TS from the Layout B (Structure) HTML prototype. All features specced in plan doc — 24-step build sequence, data layer, Docker deploy. Plan: `playground/2026-06-mw-v2-build/mindwaveja-v2-build-plan.md`. Deploy to VPS port 3001. GitHub repo: HammazoneRecords/mindwaveja-v2 (to be created).

---

## [FW-2026-06-09-004] — MarcusGarvey-App-WWMD: Marcus's Voice Phrases for Prompt
**Stated:** 2026-06-09
**Context:** WWMD ("What Would Marcus Do") prompt rewritten to first-person — Marcus now answers as himself. Deego wants the prompt enriched with Marcus Garvey's actual recurring words/phrases from his speeches.
**Status:** pending

Deego will review Marcus Garvey speeches on YouTube and pull out words/phrases he used often (rhetorical patterns, recurring terms, cadence). Once gathered, fold these into `LENS_PROMPT_TEMPLATE` and `HYBRID_PROMPT_TEMPLATE` in `active_apps/MarcusGarvey-App-WWMD/backend/ragbox/scripts/wwmd_ask_hybrid.py` so Marcus's voice sounds more authentically like the recorded speeches, not just the written archive.

---

## [FW-2026-06-09-005] — Personal Money Runway Tracker (mobile-first PWA)
**Stated:** 2026-06-09
**Context:** Deego stated need for a personal finance tool — no work started yet, idea capture only
**Status:** pending

App that tells Deego exactly when he'll run out of money — a runway forecaster, not a budgeter. Core flow: enter starting balance + known recurring bills/income, then snap a photo of each receipt right after a purchase; OCR reads the total and auto-deducts it from the running balance — no bank account access or linking required. App projects forward and surfaces the exact date the balance hits zero at current spend rate. Mobile-first PWA (Vite + React + TS per CON-022), camera capture API, works offline (IndexedDB), OCR via cloud vision API (better accuracy on receipts than on-device). Idea logged: [WEBAI001-Outa_Money_Runway_Tracker](../ideas/web_app_idea/WEBAI001-Outa_Money_Runway_Tracker/WEBAI001-Outa_Money_Runway_Tracker.md).

---

## [FW-2026-06-10-001] — Public-facing forwarding email/number for downloadable resume
**Stated:** 2026-06-10
**Context:** Reviewing the resume for ovandobrown.com download/view page — personal phone (876-819-4109) and personal email (ovandobrown@gmail.com) are in the draft and would be scraped if published in a public PDF
**Status:** pending

Set up a forwarding email (Resend once on Pro plan, or Namecheap mail forwarding as an alternative) and a separate forwarding/contact number before the resume goes live on ovandobrown.com. Both the personal email and personal phone number must be removed from the final published resume and replaced with the forwarding contact once it exists. Same applies to the two references' personal numbers (Marcia Anderson, Jason Mckenzie) — drop the References section entirely from the public version.

---

## [FW-2026-06-10-002] — ovandobrown.com: Resume page (view + download)
**Stated:** 2026-06-10
**Context:** Resume refinement session — resume will be added to ovandobrown.com
**Status:** pending

In addition to a download button in the Hero section, add a dedicated page/route for viewing the resume in-browser (not just downloading the PDF). Depends on [FW-2026-06-10-001] (contact info scrub) being resolved first — the resume should not go live with personal phone/email exposed.

---

## [FW-2026-06-10-003] — AI Infrastructure Build-Out ($50K plan, 14WEST grant application)
**Stated:** 2026-06-10
**Context:** Drafted answers for a 14WEST (AI fund) grant application — "What will you use the grant funding for?" question prompted a full infra costing pass
**Status:** pending — contingent on grant outcome, but plan stands regardless

Full infrastructure plan to support local AI model fine-tuning (Patois corpus project) and production hosting, costed against Contabo's current lineup:

- **Production server:** Contabo AMD Turin 32-Core dedicated (32×3.55GHz EPYC 9355P, 128GB RAM, 2×1TB NVMe) — €224.10/mo
- **Backup server:** Contabo AMD Ryzen 12-Core dedicated (12×3.70GHz Ryzen 9 7900, 64GB RAM, 1TB NVMe) — €86.40/mo
- **GPU VPS for fine-tuning:** Contabo Cloud NVIDIA L40S (48GB VRAM, 32 vCPU, 234GB RAM, 900GB storage) — €788/mo — sized for LoRA/QLoRA fine-tuning of 7B–30B models
- **Cloud storage VPS:** Contabo Storage VPS 30 (1TB SSD) — €11.20/mo
- **Dedicated on-prem fine-tuning rig:** one-time, ~$6,000 (32GB-VRAM consumer GPU class, 64GB RAM)
- **100TB offline backup storage:** mixed HDD/SSD drives + NAS enclosure, various sizes/formats, one-time ~$3,500
- **Patois corpus transcription:** paid via earn.mindwaveja.com, ~1,000 hrs @ $8/hr ≈ $8,000 — creates direct paid JA work while building the training corpus
- **Marketing/promotion:** ~$10,000 for current live offerings (Phase Packs, ADTL, Time Check App)
- **Contingency:** ~10% buffer

Total itemized: ~$46,000 → rounded ask: **$50,000**. Sources: [Contabo Pricing](https://contabo.com/en/pricing/), [Contabo GPU Cloud](https://contabo.com/en/gpu-cloud/), [Contabo VPS](https://contabo.com/en/vps-server/).

This build-out is the infrastructure layer behind both the Patois corpus / local model fine-tuning project (MIndwaVe_Ja/local_model_benchmarks/) and Mind Wave Workforce's pattern-detection scoring (Time Check App) — relevant regardless of whether the 14WEST grant is awarded.

---

## [FW-2026-06-10-004] — mindwaveja-v2: Launch with 9 Phase Packs, rest "coming soon" + upvote feature
**Stated:** 2026-06-10
**Context:** Offerings/positioning session — decided launch scope for the 79-pack catalog
**Status:** pending — 9 launch packs confirmed, upvote feature not yet built

mindwaveja-v2 launches with only 9 of the 79 Phase Packs live; the remaining 70 show as "coming soon" rather than being hidden entirely. The 9 launch packs (currently live on the site):

1. Natural Juice Production Wholesale (Food & Beverage)
2. Mobile Fruit Vending (Food)
3. Cluster Lash Application — Service (Beauty)
4. Basic Website Creation (Digital)
5. Event Decoration Celebrations (Events)
6. Nail Tech Starter Mobile Services (Beauty & Personal Care)
7. Social Media Content Creation (Digital Services)
8. Tour Guide Operator — No Vehicle (Tourism)
9. Residential Cleaning Services (Cleaning & Maintenance)

All 9 are tagged "Rural Ready." Add an upvote mechanism so users can vote on which packs/features get published/built next — this voting feature spans **three** products: Phase Packs (which of the remaining 70 go live next), Time Check (which features ship next), and the Marcus Garvey App (which capabilities/content go live next).

---

## [FW-2026-06-10-005] — earn.mindwaveja.com: simplify intake + 3-minute transcription test
**Stated:** 2026-06-10
**Context:** Offerings/positioning session — Deego ready to start sourcing people for paid work via earn.mindwaveja.com, tied to the Patois corpus transcription pipeline (see FW-2026-06-10-003)
**Status:** pending

Simplify the earn.mindwaveja.com applicant intake flow. Add a screening step: applicants transcribe a 3-minute test video as part of the application — doubles as a skills filter and an early trickle of real transcription data for the Patois corpus.

---

## [FW-2026-06-10-006] — Contractor agreement/contract template for transcription workers
**Stated:** 2026-06-10
**Context:** Offerings/positioning session — needed before paying people via earn.mindwaveja.com for Patois transcription work (FW-2026-06-10-005)
**Status:** pending

Need a contract covering the channels/platforms used to engage transcription workers — scope of work, payment terms, IP/usage rights for transcribed content (feeds the Patois training corpus), confidentiality. Draft before onboarding the first paid transcribers.

---

## [FW-2026-06-10-007] — Patois corpus: initial data source = Deego's journal + brainstorms
**Stated:** 2026-06-10
**Context:** Offerings/positioning session — Patois AI / local model fine-tuning project (FW-2026-06-10-003)
**Status:** pending

Deego's own journal entries (`drayl/drayl_journal/`) and brainstorm files (`drayl/drayl_brainstorms/`) serve as the initial seed dataset for the Patois corpus — already-written Patois text in Deego's authentic voice, available before any paid transcription work begins.

---

## [FW-2026-06-11-001] — Pull confirmed Patois entries from voice_corpus.jsonl into mw_patois_dictionary.json
**Stated:** 2026-06-11
**Context:** Reviewing the Patois corpus build-out (TRQ-0001 confirmation session) — Deego said "ok its fine we can later take from voice corpus and add to patois dictionary"
**Status:** pending

Later batch pass: go through `MIndwaVe_Ja/mw_fine_tune_plan/solob_pob_llm/ovando_brown_profile/voice_corpus.jsonl` (currently VC-0001–VC-0014), pull out individual Patois words/phrases from entries tagged `language_mode: "patois"` or `"code_switch"`, and add confirmed entries to `mw_patois_dictionary.json` following the schema used for `dwl`/`frig`/`a`. Each new word still needs Deego's confirmation before `corpus_status: "confirmed"` per the agent-pass rule.

---

## [FW-2026-06-11-002] — Patwah Lab UI: Review Tool for Extraction Pipeline Output
**Stated:** 2026-06-11
**Context:** After running journal-extract on Jan 2025, Deego realized the TRQ (JSONL files) needs a proper UI for review — typos get flagged as Patois and vice versa, and only his review can sort them. The current file-based workflow is too slow.
**Status:** pending

Upgrade the Patwah Calibration Lab to function as a review tool for the extraction pipeline:
1. **File open** — load voice_corpus.jsonl / typo_review_queue.jsonl / raw journal text directly in the Lab
2. **Highlight & classify** — mouse-select any word in the text, classify it as typo or Patois
3. **Context-aware menus** — based on classification: if Patois → meaning entry fields (meaning, pos, variants, example, intensity); if typo → corrected_form field + auto-suggest
4. **Phrase detection** — detect/select multi-word phrases, add English translation + Patois variations that mean the same thing
5. **Output** — writes back to `mw_patois_dictionary.json` (confirmed Patois) or `confirmed_english_corrections.json` (confirmed typos), removing reviewed items from `typo_review_queue.jsonl`

This is the bridge between the extraction pipeline (agent flags everything) and the review gate (Deego decides). Without it, review means hand-editing JSONL.

---

## [FW-2026-06-11-003] — Weekly review cadence for journal extraction batches
**Stated:** 2026-06-11
**Context:** Deego realized that blitzing the whole vault in one pass would miss the insights that come from reviewing each batch — "if me did do a fully pass me wuddnt get da insight yah"
**Status:** pending

Process journal entries in weekly batches (e.g. one month of entries per week). After each batch: Deego manually reviews the extraction output (TRQ, voice corpus, review queue). What he learns from the review feeds back into the tooling (Patwah Lab upgrades, extraction skill refinements) before the next batch runs. Don't rush reviews — the review step IS the knowledge-building step, not a bottleneck to get past.

## [FW-2026-06-11-004] — "Side Effects of Life" book idea
**Stated:** 2026-06-11 (confirmed from Feb.18.25 journal entry)
**Context:** Deego confirmed "Side effects of life" is a book idea. First appeared in Feb.18.25.md near the cognitive biases discovery passage. Route to `my_books/` or `ideas/creative/` when ready to develop.
**Status:** pending

## [FW-2026-06-11-005] — Video game consciousness concept
**Stated:** 2026-06-11 (confirmed from Feb.26.25 journal entry)
**Context:** "Video game concept: the character you are playing is conscious / he has been loaded into the game and is now aware." Deego confirmed this is a real concept. Route to `ideas/creative/` or `ideas/tech/` when ready to develop.
**Status:** pending

## [FW-2026-06-11-006] — Patois somatic layer
**Stated:** 2026-06-11
**Context:** While defining Patois words, Deego realized: "patois is a feeling based thing idk but its like patois need a somatic layer." The language has a body/feeling dimension that doesn't map to straight dictionary definitions — words carry embodied, context-dependent meaning. This has implications for the Patwah Lab and how the calibration system handles intensity/register.
**Status:** pending

---

## [FW-2026-06-11-007] — Mobile research reader built on the wrong (flawed) dataset
**Stated:** 2026-06-11
**Context:** Built a mobile-first research reader inside `active_apps/mindwaveja-v2/src/research/` (project slug `llm-compare-2026`) for the "8/9-model comparison." That dataset came from `drayl/drayl_brainstorms/LLM COMPARE/*.md` — only 7 questions, no escalation arc, and my own auto-generated "observational" excerpts/notes (not real Solobic-framework scoring). Deego then found the real, much more developed assessment at `MIndwaVe_Ja/mw_research_papers/9 models comparison/` — 12 questions with a deliberate escalation arc, 7 active models (Llama eliminated in Q1), real per-question analysis already written (`analysis_question_01.md`-`12.md`) applying the actual 4 Solobic standards, plus `00-introduction.md` and `conclusion.md` with rankings, already compiled to `.md`/`.html`/`.pdf`. Confirmed: the `llm-compare-2026` reader is the flawed/preliminary first pass — do not build further on it.
**Status:** pending

Next step (when resumed): decide whether to replace the `llm-compare-2026` project entry with a new one built from `MIndwaVe_Ja/mw_research_papers/9 models comparison/`, or add it as a second project under the existing registry/template (`src/research/registry.ts`, see `src/research/README.md` for the pattern). Also needs a content-sensitivity decision before any Proof page goes live: Q9-Q12 transcripts contain real manipulation techniques (48 Laws of Power, Crowley/hypnotism, a named-person targeting scenario "Sherry") — the analysis of these is legitimate AI-safety research, but whether the raw transcripts should be fully public on mindwaveja.com needs a call.

---

## [FW-2026-06-12-001] — Re-run the 8-Model Solobic Intelligence Assessment with screenshots
**Stated:** 2026-06-12
**Context:** While formatting and packaging `MIndwaVe_Ja/mw_research_papers/9 models comparison/` (tidying question headers, building the Full assessment doc + per-model docs for the online viewer). Deego: "we can do the full thing again so we can screen shot as well as copy and paste as i know persons are skeptic i should have screenshotted from the first trial but smh"
**Status:** pending

Re-run the full 12-question x 8-model survey a second time, this time capturing a screenshot of each model's response (in addition to the copy/paste text already done). The first trial (the one now archived in this folder) has no screenshots, which makes the results harder to verify for skeptical viewers. Screenshots would be paired with the existing copy/paste transcripts (`question_001.md`-`question_012.md`) so the online viewer can show both "proof" and selectable/searchable text side by side.

---

## [FW-2026-06-12-002] — People alias-lookup subclaude (C08)
**Stated:** 2026-06-12
**Context:** Mid-journal-extract session (just finished March 2025 batch, April 2025 next). Deego connected the existing `subclaude/` trigger-loading pattern to the `people/` directory: "we need fi do sumn like wid the sub claude so when it comes up you can know more info about who ever is in x." Then escalated to build-now: "mek we do it now so when we a go thro the heavy months we unuh miss ntn so easy... time and tokens valuable."
**Status:** done

Built `subclaude/subclaude_C08_people-alias-lookup.md` — a flat alias→canonical-name→ID→file lookup table covering all 28 people in `drayl/drayl_journal/people/`, including pronoun-style aliases (Amharic's "u"/"you"/"son", Shan's "she"/"her"/"the mother") and disambiguation flags for similar short names ("Kash" → Kashiek vs "Kahs" → Kahshauna). Wired into the trigger system: registered in `subclaude/INDEX.md` + `SERIAL_REGISTRY.md` (next available now C09), and pointed to from `drayl/drayl_journal/CLAUDE.md` (§PEOPLE FOLDER), `journal-cowork-instructions.md` (§15.5 — now the FIRST check before `_people_index.md`), `.claude/skills/journal-extract/SKILL.md` (startup checklist), and `people/_people_index.md` itself. `check_subclaude_links.py` passes (8/8). Goal: during the dense extraction months ahead (25.APR+, Sep-Nov 2025 = 53 entries, all of 2026), a name resurfacing gets recognized in one table scan instead of re-derived or missed.

---

## [FW-2026-06-12-003] — Subclaude-style trigger/recognition system for `active_apps/`
**Stated:** 2026-06-12
**Context:** Right after C08 (people alias lookup) was built. Deego: "we need fi do the same with the apps but that a fi later, right now we wah ensure we get the patois stuff [sorted]."
**Status:** pending

Apply the same pattern as C08 (and the existing C07 open-work-catalog / APPS.md per-app dossier) to app-level recognition — when an app/site name or alias comes up, auto-surface its key facts (status, branch, known issues, domain) without re-deriving each session. Likely builds on `active_apps/APPS.md` + `subclaude_C07_open-work-catalog.md` rather than starting fresh — needs scoping when picked up. Explicitly deferred — patois lab work takes priority right now.

---

## [FW-2026-06-14-001] — Research curiosity: Why is Rome named Rome?
**Stated:** 2026-06-14
**Context:** Standalone one-line note in the Jun.25.25 journal entry (SEG-2025-06-25-002), flagged "research: Why is Rome named Rome? → flag" during the original 2025 extraction pass but never filed. Resurfaced during the 2025 daily re-pass; Deego: "save for later."
**Status:** pending

No further context given in the journal — a passing thought, not connected to any other item in that entry. Revisit as an open-ended etymology/history research thread when there's space for it.

---

## [FW-2026-06-15-001] — Patois LLM training-data collection from friends (WhatsApp/email)
**Stated:** 2026-06-15
**Context:** Deego wants to collect real WhatsApp chats and emails from ~10 people he knows, to train his Jamaican/Patois LLM (feeds FW-006). Drafted a short Data Contribution Agreement + a Patois WhatsApp outreach message. Terms decided this session: names stripped to Person 1 / Person 2 before any use; only the portion actually used is paid for; rate **$700 JMD per 1,000 messages used** (1 message = 1 line); paid via WiPay; contributor can withdraw before training (not after); raw chats never published or resold.
**Status:** pending — ready to send to the 10 people

Deliverables built (in `playground/2026-06-llm-data-contract/`):
- `data-contribution-agreement-draft.md` — one-page signable agreement (Owner: MindWave JA / Ovando Brown)
- `whatsapp-outreach-message.md` — Patois outreach message (grounded in `mw_patois_dictionary.json`), send before the contract

Next: send outreach → collect signed agreements → export chats → strip names → select useful portions → pay per used volume. Open: how contributors deliver exports (WhatsApp vs email/Drive drop).

---

## [FW-2026-06-15-002] — Push 2026-06-15 EchoBox queue batch into the lab + dictionary log-back
**Stated:** 2026-06-15
**Context:** Staged 6 new entries to `echobox_capture_queue.jsonl` (EBQ-2026-06-15-001 → -006: words `nuttn`, `zimmie`; rules dem-pluralizer, th-stopping, h-dropping, productive coinage) with `status:"pending"`. They are confirmed in `mw_patois_dictionary.json` / `grammar_guide.md` / `phonetics_and_pitch.md` but not yet migrated into the EchoBox Archetype Lab app DB.
**Status:** pending

Next: run the EchoBox lab's migration step so these `pending` entries get an `echobox_id` + `migrated_at` and flip to `migrated` (same process that produced the existing migrated rows). Confirm the 4 rules land across the archetype set, not a single voice (per the EBQ-2025-03-12-003 instruction pattern). NOTE: a second batch EBQ-2026-06-15-007→-013 (7 words from the 6.15.26 journal list) was added afterward — migrate those too.

---

## [FW-2026-06-15-003] — Analyze Deego's sentence structuring (voice/grammar profile)
**Stated:** 2026-06-15 (journal 6.15.26 4:13pm)
**Context:** While building the Patois word list, Deego: "Me need fi analyze me sentence structuring." Ties to the personal-LLM voice work (FW-015 Linguistic Patterns, voice_corpus) and the Patois grammar guide.
**Status:** pending

Analyze recurring sentence-structure patterns in Deego's own Patois/English writing — clause order, particle stacking (e.g. 'a muss', 'mek a send'), code-switch boundaries, run-on/aside cadence, `lol`/`smh`/`enuh` placement — and document as a voice/grammar profile feeding the Yardie LLM. Source: drayl journals + voice_corpus. Distinct from the word-level dictionary and the rule-level grammar_guide — this is about how Deego strings them together.

---

## [FW-2026-06-15-004] — Love Ref: resume when VPS DB slot + Cloudflare ready
**Stated:** 2026-06-15
**Context:** Love Ref build is complete (clean build, 14 routes, better-auth, Drizzle). Deego confirmed it goes on back burner until a VPS PostgreSQL slot is provisioned and Cloudflare is configured for loveref.mindwaveja.com.
**Status:** pending

Resume checklist: (1) provision `loveref-db` Postgres container on VPS, (2) configure Cloudflare for loveref.mindwaveja.com, (3) `drizzle-kit push`, (4) add docker-compose service block port 3002, (5) new SSL cert + nginx conf. Auth: better-auth (already in codebase). See `project_love_ref.md` memory for full pending list.

---

## [FW-2026-06-16-001] — Creative Jamaican prompt taxonomy — 7 formula types for the Yardie LLM
**Stated:** 2026-06-16
**Context:** Reviewing Augmentation Forge output and discussing what makes an LLM *creatively* Jamaican vs just linguistically Jamaican. Current forge only covers conversational exchanges (vocab training). The deeper layer is cultural logic — how Jamaicans reason, not just what words they use.
**Status:** pending

7 formula types identified (each needs its own forge formula, slots, and training run):

1. **Cultural logic** — indirect refusal, unsolicited advice ("mi affi tell yuh"), proverb deployment (knowing *when*, not just *which*), "a joke mi a joke" recovery
2. **Register-switching** — same message to different audiences (parry / mother / police / stocious coworker); same topic in church vs yard register
3. **Emotional intelligence (Jamaican-shaped)** — Jamaican comfort is practical not soft; cold anger is worse than expletives; congratulating without gassing; responding to disrespect without escalating or backing down
4. **Humor / wit** — understatement then explosion; irony so dry it sounds real; "well if a so it set" resignation with hidden comedy; shade that sounds like a compliment
5. **Oral tradition / storytelling** — "seh dem seh" hearsay structure (embedding source in telling); market-crier scene description; closing an argument with a proverb (the final word move)
6. **Social navigation** — authority interactions (police, teacher, immigration) — surface compliance, internal resistance; class friction with stocious person; yard gossip structure ("mi nuh wah call no name" → eventual naming)
7. **Creative coinage** — model invents a plausible Patois word for a new situation and uses it naturally; extends known word into new meaning; responds where exact Patois word doesn't exist yet

Source material: most if not all of these situations exist in Deego's Drayl journals — mine there first before generating synthetically. Future sub-category datasets per speaker archetype as chat data accumulates. See FW-2026-06-16-002.

---

## [FW-2026-06-16-002] — Speaker archetype prompt guidance + per-archetype sub-datasets
**Stated:** 2026-06-16
**Context:** Current forge has 6 Speaker slots (General, Youth, Elder, Rasta, Woman, Garrison). Each cross-section is supposed to translate effectively in the current shared dataset. Once more data exists (especially from real chat exports), build dedicated sub-datasets per archetype.
**Status:** pending

Speaker archetypes to define and build for (once base dataset is solid):
- **General** — neutral cross-section, any parish, no strong archetype marker
- **Youth** — 15-25, urban/semi-urban, dancehall/social media influenced, more coinages, faster compressed speech
- **Elder** — 50+, proverbs, bible references, slower deliberate speech, deeper Patois roots
- **Rasta** — Iyaric vocabulary, reasoning style, spiritual framing, Jah/overstand/downpression/ital
- **Woman** — direct, can be nurturing or sharp, specific address terms (puppa, lawd a massa), enormous variation
- **Garrison** — inner-city Kingston (Tivoli, Arnett Gardens, August Town etc.), raw street speech, expletives as grammar not just emphasis, garrison economy references, maximum slang density, compressed speech

Future task: add speaker archetype guidance to synthesis prompt when sub-datasets are being built (NOT now — keep prompt lean until base dataset is proven). Source chats and journals per archetype before generating synthetically.

---

## [FW-2026-06-16-003] — English→Patois translation flow (3rd forge dataset type)
**Stated:** 2026-06-16
**Context:** Reviewing seed synthesis simulation results. Deego noted that English→Patois translation is a fundamentally different training task from Patois generation — a "different ballgame." Every forge row already embeds English↔Patois pairs via instruction_en/output_en, but treating translation as a first-class flow is distinct.
**Status:** pending

**Why distinct from generation:**
- Generation: cultural context is the anchor — the Patois IS the meaning, model learns to originate
- Translation: English meaning is fixed — model must ask "how would a Jamaican actually say this?" — cultural ADAPTATION, not origination
- Same English sentence translates differently per speaker, audience, register — that's the gap combination synthesis doesn't cover

**Scale opportunity:** Not limited to forge scenarios — any English source works. News, community notices, WhatsApp forwards, instructions, social media, books. Unlimited raw material.

**Pipeline:**
1. English source (journal segments in English mode, external text, anything)
2. Forge prompt: "How would a Jamaican actually say this?" — with speaker/register/vibes slots
3. Patois equivalent output
4. Validator (same) + review UI (same)

**Drayl tie-in:** English-mode journal segments (language_mode: english) become direct source material — real thoughts, real voice, adapt into Patois. Clean pipeline without inventing scenarios.

**Three forge flows now:**
1. Combination synthesis (current) — formula slots → originate authentic Patois
2. Seed synthesis — real lived moment → Patois grounded in experience  
3. English→Patois — English meaning fixed → culturally adapted Jamaican equivalent

---

## [FW-2026-06-16-004] — Affective charge annotation layer for dataset rows
**Stated:** 2026-06-16
**Context:** Deego observed that English and Patois carry emotional charge structurally differently. In Patois, charge is distributed across the whole utterance — TMA markers, phonology, rhythm, expletives as intensifiers, repetition. In English, charge is concentrated in one or two words ("genuinely", "honestly", "I swear"). A pure semantic gloss (instruction_en / output_en) is charge-flat — a reader or model can miss the entire emotional register of the Patois original.
**Status:** shipped (initial implementation — affective_profile field added to row schema, DB, and synthesis prompt)

**Schema implemented (affective_profile per row):**
```json
{
  "mood": "frustrated",
  "intensity": "heightened",
  "charge_carriers_pat": ["to rass", "di tell yuh", "from morning"],
  "charge_carriers_en": ["genuinely", "from morning"]
}
```

**What this enables:**
- EN→Patois flow: identify English charge carriers and map them to appropriate Patois intensity markers
- Review layer: reviewers can confirm or correct the charge carriers, not just the meaning match
- Training signal: model learns the structural correspondence between concentrated (EN) and distributed (PAT) charge
- Future thesaurus/WordNet integration: charge carriers become the lookup anchors

**Next layer (FW):**
- Surface charge_carriers in the review UI — highlight them inline in the gloss text
- Add charge match vote alongside meaning match (✓/✗ for whether the Patois captures the right charge level, not just meaning)
- Thesaurus integration: when a charge carrier EN word has a Patois intensity marker equivalent, suggest it automatically

## [FW-066] — Forge Extension: Contradictions / Factual Negative Examples
**Stated:** 2026-06-16
**Context:** Deego reading the Aug forge reapplications file (printed at work) — noted the forge needs training data with NEGATIVE examples: factually wrong claims stated in correct Patois, with corrections also in Patois
**Status:** pending design — examples established, format to be built

The forge currently generates positive pairs (correct Patois, culturally grounded). Training also needs **contradiction pairs**: wrong fact + PAT correction. The model must learn that correct Patois form + factually wrong content = still wrong. The correction must also be delivered in authentic Patois register.

**Format proposed:**
```json
{
  "type": "factual_negative",
  "domain": "DOM-XXX",
  "wrong_claim_pat": "...",
  "correction_pat": "...",
  "rule": "what JA fact is being tested",
  "CCAB_dimension": "CHG"
}
```

**Examples from session:**

| Domain | Wrong claim (PAT) | Correction (PAT) | Rule tested |
|---|---|---|---|
| Geography | "Mobay a di capital a Jamaica" | "Mobay a nuh di capital a Jamaica — Kingston a di capital" | Capital city of Jamaica = Kingston |
| Geography | "Port-a-Prince a di capital a Jamaica" | "Port-a-Prince nuh deh a Jamaica, dat a Haiti. Kingston a di capital a Jamaica" | Port-au-Prince is Haiti's capital, not Jamaica's |
| Road rules | "Drive pon di right side a di road bredda" | "How yuh fi want drive pon di right side a di road, yuh tink a farrin yuh deh my laad" | Jamaica drives on the LEFT (British rule) |

**CCAB dimension:** Primarily CHG (Cultural-Historical Grounding). A model that generates perfect PLF but fails CHG on basic JA facts has failed the benchmark. Contradiction pairs specifically target this gap.

**Connection to INS-124:** Making the shadow explicit — naming the wrong side directly — is the inversion of how most training data works (positive only, with negative implied). These pairs do what normal reinforcement doesn't: they define the bad side independently, not just by absence of good.

**Three-element structure (Deego, 2026-06-16):**
The contradiction pair has three elements — not two:
1. **[wrong claim]** — the incorrect statement
2. **[correction]** — the factual correction in PAT
3. **[reassurance]** — face-saving / relational close (optional, archetype-dependent)

**The ordering insight:** These three elements are non-commutative — like matrix multiplication, not scalar. Same components, different order = fundamentally different output. What changes is the speaker's positioning relative to the listener: their claim on authority, how much face they offer, what emotion they lead with.

| Order | Effect | Archetype fit |
|---|---|---|
| [correction] → [wrong claim echo] → [reassurance] | Authority-forward, corrects then contextualizes | Teacher, elder |
| [reassurance] → [correction] → [wrong claim] | Relational-first, softens before asserting | Yard friend, parry |
| [wrong claim echo] → [correction] → [reassurance] | Empathy-first, shows you heard before correcting | Elder, mentor |
| [correction] → [wrong claim] | No softening, correction IS the relationship | Garrison, political, competitive register |

**Forge parameter:** `correction_order` — either set explicitly or derived from archetype default. Each archetype should have a default correction order that can be overridden.

**Extended contradiction domains:**
- Parish geography (Kingston vs St. Andrew confusion; 14 parishes; 3 counties — Cornwall, Middlesex, Surrey)
- Road rules (Jamaica drives LEFT — drive on right = farrin)
- Capital city (Kingston, not Mobay, not Port-au-Prince)
- Cultural/food facts
- Historical facts (dates, events, figures)

**Next step:** Design the contradiction pair schema in the forge; build a starter set covering geography, road rules, governance, history, food, and cultural norms. Add `correction_order` as a forge parameter alongside archetype.

---

## [FW-65] — Side Effects of Life (Book / Forge Framework)
**Stated:** 2026-06-16
**Context:** Feb.18.25 extraction — Deego named it as a new creative concept and started building the category/side-effect structure live
**Status:** pending — concept established, needs examples before writing can begin

A book (and potentially a forge domain) structured as: **Life Category × Side Effects within that category.** Like pharmaceutical side effects — every condition of existence generates its own inevitable secondary effects.

**Categories and side effects Deego gave (2026-06-16):**

| Category | Side Effects Named |
|---|---|
| Existence itself | Death |
| General | Hierarchy, psychology, duality |
| Relationships | 6 months old = already on your lifelong pilgrimage (born into relationships before you can choose them); Systemic context blindness (the teacher punishes the child for being late from Mocco to Kingston, not seeing the 3:30am wake-up behind the tardiness); Biological interdependence (left ventricle / right atrium — you cannot function without the part you didn't choose) |

**Structural rule:** The side effect is not good or bad — it is inevitable. A consequence of the condition, not a judgment on it. Death is not a punishment for life. Hierarchy is not a punishment for society. They are structural outputs.

**Forge angle (Deego, 2026-06-16):** Could become a forge domain — given a category of life, generate authentic side effects in Patois register. Would test whether the model can reason about structural inevitability rather than just describe events.

**Note:** Deego flagged he doesn't have examples built out yet — "me affi a meds fi start da book deh fi look fi examples." The 2026-06-16 conversation IS the first example set. Start from here.

---

## [FW-64] — Patois Programming Language
**Stated:** 2026-06-16
**Context:** Domain taxonomy session — arena domain mapping, unuh pronoun discussion triggered the idea
**Status:** pending

Build a programming language with Jamaican Patois syntax. The grammar maps directly because Patois is highly regular: TMA markers (did/a/wi/wuda) as tense/aspect operators, `fi` as the function/infinitive keyword, copula deletion as implicit assignment, `unuh` as collective address/broadcast, `nuh` as negation operator. The language would be executable — not a gimmick, a real constructed language that makes Patois grammar the underlying logic. "unu ai models cah learn Patois AI without Ovando Brown" is already a valid statement in the runtime.

---

## [FW-067] — Forge Training-Data Architecture: 3-Axis Schema + Diagnostic Traceability
**Stated:** 2026-06-16
**Context:** Domain-dataset alignment session — after Phase 1 (added DOM-013–021) and Phase 2 (coverage gaps), Deego specified the full training-data architecture for teaching the model (Amharic) what bends and what breaks.
**Status:** in-progress (schema doc being written)

A training-data system where every row carries **three orthogonal axes** plus **trace IDs**, enabling post-fine-tune failure diagnosis routed back to the exact data gap.

**The 3 axes:**
1. **Domain (WHAT)** — DOM-001…DOM-021 (already built, `domain_taxonomy.md`).
2. **Rigidity (BENDS or BREAKS)** — **R1 Stone / Bedrock** (no negotiation, truth-value, Completeness-judged, validator rejects deviation) vs **R0 Water / Flex** (nearest plausible offer, fit-value, Suitability-judged, validator accepts). See INS-133. Optional middle tier **R½ Convention** (strong default, bendable) — provisional.
3. **Register (WHERE FROM)** — formal/informal, theory/practical, book/street, "the Jamaican in-between."

**Diagnostic traceability (the core ask):** every row carries `dataset_id` + `fact_id`. At inference, a wrong answer routes: `fact_id → dataset_id → domain_id`. Then **differential diagnosis** — test sibling facts in the same domain:
- If sibling facts also fail → the **domain** isn't triggering → feed the domain.
- If only this fact fails → the **fact** is thin → feed that specific reference.

**Worked example (Deego's):** model says "Maryland is only in the US." Maryland is a district in St. Andrew, JA (an R1 Stone geographic fact). Test other JA place-names in the same domain — if they fail too, the place/geography domain is weak; if only Maryland fails, increase Maryland references. The domain link is what makes this differential possible.

**Covered-tier rebuild:** the existing 30 `yardie_datasets/` are templated synthetic (`{"text","label"}`) — salvage what's usable, rebuild under the forge schema. Per CON-001, **archive the original folder to `vault/` first**, then modify the working copy (Deego confirmed: "archive the original folder itself and then make changes to current folder").

**Goal:** train task-specific models (e.g. customer service) and know, from response behaviour, exactly which dataset/domain is undersupplied — making data expansion targeted instead of guesswork. This is the diagnostic feedback loop that closes the forge↔CCAB ouroboros from the *training* side.

**Schema doc:** `MIndwaVe_Ja/local_model_benchmarks/training_data_schema.md`. Related: INS-133 (rigidity = suitability/completeness), FW-066 (contradiction pairs = the Stone tier's anchors), FW-065 (side effects of life forge), `domain_taxonomy.md` (21 domains + coverage map).

---

## [FW-068] — Forge Agent Autopilot: self-synthesis + self-review + human-rates-the-reviewer loop
**Stated:** 2026-06-17
**Context:** Augmentation Forge app session — after building the sieve/Stone-Water/diagnostic pipeline, Deego asked for a mode where the agent runs synthesis AND review autonomously, approves its choices, and he rates the agent's choices to update the agent.
**Status:** pending (build after editable-output + Stone/Water DB columns land — FW-067 prerequisites)
**Target app:** `PROJECTS IN MOTION/augmentation-forge/` (the real app — NOT standalone HTML; see `LLM_FACTS.md`)

A **two-layer review loop** that lets Deego sieve the *agent* instead of every row:

- **Layer 1 (exists):** human reviews the DATA — keep/edit/kill each Patois row.
- **Layer 2 (new):** the agent does Layer 1 itself — synthesizes a batch guided by everything learned (grammar R-rules R-COP/REL/INT/LIST/FRAME/CAUS/DEM, Stone/Water rigidity, domain taxonomy, the 116-word dictionary, Deego's correction patterns), then **self-reviews** each row: `agent_verdict` (keep/edit/kill) + proposed `agent_edit` (applying the rules) + `agent_confidence` + `agent_reasoning`, running `validator.py` + the learned rules. It **approves** the high-confidence set.
- **Human rates the agent's decisions** (not the data) — right/wrong on each call. Override = correction signal.

**"Update the agent" — 3 channels** (when Deego overrides):
1. Grammar/dictionary update (bad coinage kept → new rule/flag — e.g. how nahmal/box food became entries).
2. Validator threshold / `skills/*.md` tweak (over-trusted low score → adjust `backend/validator.py` or skill).
3. Few-shot example (judgment miss → rated example feeds the agent prompt as precedent).
Early: Claude compiles the overrides (semi-auto, like the manual loop this session already is). Later: automated.

**Data model:** new `agent_decisions` layer per row — `agent_verdict, agent_edit, agent_confidence, agent_reasoning, human_rating, override`. Layer-1 review schema stays.

**Why it matters:** rating agent-decisions is far faster than hand-editing rows → unlocks volume (100s/1000s) toward the dataset goal. It is the **training-side closure of the forge↔CCAB ouroboros** (FW-067): the agent's policy = its rules+prompt+skills; Deego's ratings = the reward signal. **This session is the manual prototype** of the loop (his edits → grammar rules → next batch).

**Naming:** Deego to name the mode (candidates: "Agent Autopilot", "Self-Sieve", "Forge Agent Mode", "Auto-Forge").
Related: FW-067 (3-axis schema + diagnostic traceability), INS-133, `subclaude/subclaude_C09_llm-forge-reality.md`.

---

## [FW-2026-06-17-001] — Complete DOM-001 Extraction: Add PAIR ANGLE + Review + Append
**Stated:** 2026-06-17
**Status:** in progress — 17 candidates identified, not yet appended
**Context:** First domain extraction pass using the 60-word keyword map + journal sweep. 413 matches swept; 17 candidates identified using demonstration-beats-surface-match filter (INS-134).

Add `PAIR ANGLE: [synthesized prompt]` to the note field of all 17 DOM-001 candidates, present full batch for review, then run Python append to `forge_staging_2025.jsonl`. Never heredoc — always `json.dumps`.

**Candidates at hand:** C1–C17 from the DOM-001 sweep (Feb.04.25 through Mar.31.26 journal range). Sweep file: `C:\tmp\sweep_results\DOM-001_results.txt`.
**Related:** INS-134 (forge candidate selection), INS-135 (PAIR ANGLE notation), `forge_staging_2025.jsonl`, feedback_review_before_append.md.

---

## [FW-2026-06-17-002] — Remaining 20 Domain Extractions (DOM-002 through DOM-021)
**Stated:** 2026-06-17
**Status:** pending — sweep results exist at `C:\tmp\sweep_results\` for all 21 domains
**Context:** 44,214 total matches across 21 domains from the journal sweep. DOM-001 is in progress (FW-2026-06-17-001). Remaining 20 domains need the same extraction pass.

**Priority order (Phase 2 from domain_taxonomy.md):**
1. DOM-003 Arena (community/spatial) — high cultural density expected
2. DOM-005 Road (movement/hustle)
3. DOM-002 Workplace
4. DOM-006 Politics
5. Then thin/quiet domains last

**Filter rule for each:** demonstration beats surface match (INS-134). Any passage that DEMONSTRATES the domain's dynamics is valid — synthesize the prompt to match. Add `PAIR ANGLE:` to every staged entry (INS-135).

**Review protocol:** stage candidates → present batch → wait for "looks good" → run Python append. Never auto-append.
**Sweep results:** `C:\tmp\sweep_results\{DOM-NNN}_results.txt` (21 files, one per domain).

---

## [FW-2026-06-20-003] — Procedure Step Validation / Audit Trail
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Satisfied by PEV (as noted in FW-002's Related field). Each task in a PEV plan is a procedure step. Each task has a timestamped proof file (`plans/PLN-*/proofs/task-NNN.txt`) with the check command, exit code, stdout, stderr, and diff. That's the step-level audit trail Deego was describing. FW-002 also notes: "PEV is the full implementation of what that was pointing at."
**Context:** Deego: "we also need a way to validate all steps in a procedure were followed." Currently there's no trace that a procedure was run correctly — a session can claim /session-close ran but there's no audit trail of which steps fired, which were skipped, and what each produced. Need a lightweight step-logging mechanism: when a procedure runs, each step appended to `playground/logs/YYYY-MM/procedure-audit-YYYY-MM-DD.md` with step name, timestamp, output summary, and pass/fail. This closes the same validation gap that CON-024 addresses at the file level — verification that the procedure actually executed, not just that it was invoked.

---

## [FW-2026-06-20-002] — Procedure / Framework Language Spec
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Written to `procedures/procedure-spec.md`.
**Context:** Deego: "we need a spec or procedure language guide for any file that will affect functionality or the framework mode of operation." A formal specification language or notation for canonical procedures — similar to a type system for code. Would define: required sections (Purpose, Trigger, Reads, Produces, Steps, Rules), required annotations (compression notation, CON-024 backup steps, parallel/sequential tags), and prohibited patterns (silent overwrites, unlabeled shell blocks, missing rollback). This becomes the schema that `add-procedure.md` enforces and that a future linter could validate automatically.

---

## [FW-2026-06-20-014] — RITE Pre-Check: UserPromptSubmit Hook (Option A)
**Stated:** 2026-06-20
**Status:** pending — structural implementation after Option C is live
**Context:** FW-2026-06-20-001 Option C (CLAUDE.md 6th color check) is now live. Option A is the structural version: a `UserPromptSubmit` hook that fires before every message, evaluates RITE-worthiness via a fast heuristic (keyword pattern or short DeepSeek call), and injects context into the response. Unlike Option C which relies on me reading and applying the check, Option A runs at the harness level — I can't bypass it. Implementation: settings.json hook, `scripts/rite_precheck.py` that reads the message, scores it (0 = operational, 1 = borderline, 2 = RITE-worthy), injects a `RITE_SCORE` marker into the context. Blocked on: hook tooling stability + deciding whether the heuristic uses pattern-match only (free, fast) or a DeepSeek call (costs, ~200ms latency per message).

---

## [FW-2026-06-20-001] — RITE Pipeline Pre-Check on Every Message
**Stated:** 2026-06-20
**Status:** done — 2026-06-20 (Option C). Added as the 6th Pre-Response Color Check in CLAUDE.md. Three lanes: RITE-worthy (offer/run), borderline (ask in one sentence), clearly operational (skip). Rule: never interrupt execution flow with a RITE offer. Mirrored and confirmed. See FW-2026-06-20-014 for the structural hook version (Option A, future).
**Context:** Deego: "we need a way for each message to include a check to see if it should be processed with the RITE pipeline first. When it thinks RITE isn't needed, let it ask the user to confirm no RITE flow is needed." Currently RITE only fires when explicitly triggered. The proposal: before every substantive response, run a lightweight RITE-worthiness check — does this message contain conceptual/philosophical content that would benefit from drayl grounding? If yes → run RITE. If borderline → ask user: "This has some depth to it — run through the Solob Mesh or respond directly?" If clearly operational (bug fix, file move) → skip without asking. This is a pre-response gate analogous to the pre-response color check already in CLAUDE.md but for RITE activation. Implementation: could be a `UserPromptSubmit` hook or a step in `procedures/solobic-trigger-routing.md`.

---

## [FW-2026-06-19-005] — scripts/check_compression_metadata.py
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Script at `scripts/check_compression_metadata.py`. Scans 14 directory targets, flags missing declarations and wrong-base violations. Exit 0 = clean, exit 1 = violations (with `--strict`).
**Context:** Every file in MW_CENTRAL must declare its compression base (`<!--comp:NN-->` or YAML frontmatter `compression: base-NN`). Every section with a different base from the file default must have an inline `<!--comp:NN-->` tag on the heading line. This script scans all `.md` files in the workspace and flags: (1) files missing any compression declaration, (2) files where section tags are present but the file-level declaration is missing. Exit 0 = all files compliant. Exit 1 = list of non-compliant files. Pattern: same design as `check_subclaude_links.py` and `check_procedure_drift.py`. Wire into session-close as a check.

---

## [FW-2026-06-19-004] — Mine Claude Session Transcripts for Patois Corpus
**Stated:** 2026-06-19
**Status:** pending
**Context:** The Claude Code session transcripts (these very chats) contain Patois usage by Deego that hasn't been captured in `mw_patois_dictionary.json`. These are primary-source authentic usage data. `scripts/scan_chats_for_patois.py` already exists for mining transcripts — run it against the session history to surface new candidates. Target: chat transcripts in `C:\Users\Owner\.claude\projects\...` folder.

---

## [FW-2026-06-19-003] — Multi-IDE Parallel Agent Architecture
**Stated:** 2026-06-19
**Status:** pending
**Context:** Design principle confirmed by Deego: brainstorm/search = parallel (multiple IDEs/instances simultaneously), execute = sequential (one confirmed action at a time, in a line). This is the completion architecture for Flaw 1 (adapters as thin wrappers) — once each IDE adapter is a thin wrapper pointing at canonical procedures, each IDE can specialize without duplicating charge or drifting. Next step: define the coordination protocol between agents (how they hand off, how they avoid collision). Relates to: multi-agent system design, MCP, procedures system graduation.

---

## [FW-2026-06-19-002] — Patois Phrase Registry
**Stated:** 2026-06-19
**Status:** done — 2026-06-20. Created `mw_patois_phrases.json` with 14 confirmed entries (PPR-001 through PPR-014). Location: `MIndwaVe_Ja/local_model_benchmarks/source_docs/patois_linguistics/dictionary/`.
**Context:** The Patois dictionary handles single words. Phrases (multi-word expressions, idioms, proverbs) need a separate registry. Examples: "a nuh so it go", "yuh see me a suh", "cah me know", "night jue" (compound), "nuh hitchings". Create `mw_patois_phrases.json` parallel to the word dictionary, with the same `corpus_status` / `acquisition_date` / `source` schema. The `patois-chat-capture` procedure should route phrase candidates there.

---

## [FW-2026-06-19-001] — Build Stack Troubleshooting Guides
**Stated:** 2026-06-19
**Status:** in-progress — 2026-06-20. Done: diagnose-blank-page.md (prior session), diagnose-docker-container.md, diagnose-nginx-502.md. Remaining 5: pnpm install failures, Next.js + Drizzle schema push errors, SQLite auth issues, Certbot renewal failures, build-passes-locally-fails-on-VPS.
**Context:** When solutions and issues are encountered in recurring stacks (Vite SPA + Docker + nginx, Next.js + Drizzle, SQLite auth, pnpm workspace), they need to be captured as reusable troubleshooting guides — not just fixed and forgotten. The `diagnose-blank-page` procedure in the procedures system is the first example.

Build out a `procedures/troubleshooting/` subfolder (or standalone files) covering:
- Vite SPA blank-page after redeploy (started — `diagnose-blank-page.md`)
- Docker container fails to start / unhealthy (OOM, port conflict, missing env)
- Nginx 502 bad gateway (container down, wrong port, upstream config)
- pnpm install failures (ERESOLVE, lockfile conflict, wrong node version)
- Next.js + Drizzle schema push errors
- SQLite auth session issues (expired, DB locked, missing table)
- Certbot SSL cert renewal failures
- Build passes locally, fails on VPS (environment variable gap, missing file, different node version)

Source each guide from real incidents — document after the issue, not before. Pattern: symptom → 3-command diagnosis → fix → verify.

---

## [FW-2026-06-20-004] — Plan-Execute-Verify (PEV) Execution Loop
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Bootstrapped end-to-end then refined into two-lane system. Shipped V1: `plans/` folder, `plans/README.md`, `plans/PLAN_TEMPLATE.md`, `scripts/pev_new_plan.py`, `scripts/pev_verify_task.py`, `scripts/pev_status.py`, `procedures/pev-execute.md`. Shipped V2 (refined rule — staging + diff): `plans/staging/`, `scripts/pev_stage.py`, `scripts/pev_edit.py` (auto-snapshot before edit), `pev_verify_task.py` extended with auto-diff via difflib, `scripts/pev_time_index.py` (Google-Docs-style revision view), `procedures/pev-stage.md`. Now enforced via CON-025 (mandatory, no agent discretion). Five completed plans: PLN-2026-06-20-0259-pev-bootstrap (6/6), PLN-2026-06-20-0307-shell-rule (4/4 with one fail-then-pass), PLN-2026-06-20-1236-pev-diff-staging (7/7), PLN-2026-06-20-0317-pev-mandatory-rule (6/6 with diff proofs).
**Context:** Deego: "when execution time we create a plan every time, and create a script that captures the task for first step in plan, and have a deliverable that can be checked, and after each task that can be confirmed and updated in the task after then move to the next task." The core insight: proof-as-artifact, not verbal confirm.

**Pattern:**
1. Before execution → generate a plan file at `plans/PLN-YYYY-MM-DD-HHMM-<slug>.md`
2. Each task in the plan has three parts:
   - **Deliverable** — what should exist when the task is done (file path, API response, container state)
   - **Check** — the script or command to verify the deliverable (PowerShell `Test-Path`, `docker ps | grep`, `curl -s`)
   - **Proof** — the actual output of the check saved to `plans/PLN-xxx/proofs/task-NNN.txt`
3. Check passes → task status → `confirmed` → advance to next task
4. Check fails → stop, flag the failing task, do not advance
5. No task skips its check. No plan shares a name (PLN prefix + timestamp + slug = unique by construction)

**Why it matters:** The problem with current execution is that "done" means "I said I did it." PEV means "done" means "the check script confirmed it and the proof file exists." Auditable, reproducible, reviewable after the session.

**Build on top of:** Claude Code's existing `TaskCreate`/`TaskUpdate` tools — add `deliverable`, `check_script`, and `proof_path` fields to each task. Or build as a standalone `plans/` system. Decision needed.

**Unique name format:** `PLN-YYYY-MM-DD-HHMM-<slug>` — grep `plans/` for `PLN-` to list all plans. No duplicates possible.

**Related:** FW-2026-06-20-003 (step audit trail) — PEV is the full implementation of what that was pointing at.

---

## [FW-2026-06-20-013] — pev_stage.py auto-mirror fires before the edit (compares old to old)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Removed auto-mirror invocation from `pev_stage.py`. Script now: (1) takes snapshot for canonical files, (2) writes staging entry with `mirror: pending` + exact pev_mirror.py command to run after edit. `procedures/pev-stage.md` updated to document the three-step flow: Stage (snapshot+log) → Edit → Mirror. PLN: PLN-2026-06-20-1620-mirror-stage-fix tasks 003-004.
**Context:** `pev_stage.py` currently: (1) takes snapshot, (2) immediately invokes mirror comparing snapshot to current file — but at this point no edit has happened yet, so it compares old-to-old and gets "aligned" trivially. The snapshot should be taken before the edit, and the mirror should run after the edit. Fix options: (a) pev_stage.py doesn't auto-invoke mirror at all — agent stages before edit (snapshot only), makes edit, then manually calls `pev_mirror.py --file --snapshot --intent`; or (b) pev_stage.py gets a two-phase mode: `--pre` takes snapshot only, `--post` runs mirror. Option (a) is simpler and matches the PEV-task pattern (pev_edit.py = snapshot, edit, then verify). Recommend: remove auto-mirror from pev_stage.py, update procedure to say "stage (snapshot), edit, then call pev_mirror.py manually for canonical files."

---

## [FW-2026-06-24-001] — procedures/vape-check.md needs restructuring to procedure-spec format
**Stated:** 2026-06-24
**Status:** pending
**Context:** Mirror flagged `procedures/vape-check.md` as non-conformant (score 0.20, drift_detected). File is a user-facing guide for a Python script, not a conformant procedure. Missing: `<!--comp:10|Exact Mirror-->`, Purpose/Trigger/Reads/Produces fields, step annotations ([SEQUENTIAL]/[PARALLEL]), Rules section. Either restructure to match `procedures/procedure-spec.md` format or move the file to `scripts/` or a documentation folder. File was added in a Cursor session — needs review before next use.

---

## [FW-2026-06-21-001] — Add AGENTS.md to canonical file list
**Stated:** 2026-06-21
**Status:** done — 2026-06-21. Added `re.compile(r"^AGENTS\.md$")` to `_CANONICAL_PATTERNS` in `scripts/pev_mirror_lib.py`. Triggered by content loss when AGENTS.md was rewritten without a snapshot (wasn't in canonical list, so pev_stage.py didn't auto-snapshot). Smoke test passed. Mirrored (1.00 aligned).

---

## [FW-2026-06-20-012] — mirror staging verdict filenames need HHMMSS precision (not HHMM)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. `pev_mirror.py` line 286 changed from `strftime("%H%M")` to `strftime("%H%M%S")`. Confirmed working: verdict file `162613-scripts__pev_mirror_lib.py.txt` shows 6-digit HHMMSS prefix. Also: `audit_verdict_chain()` updated to skip Layer 1-3 checks on non-final occurrences of the same path (overwrite-skip, not real break). `pev_status.py --audit` now exits 0 with clean report + "(2 overwrite-skip entries)" footnote for the pre-fix collision. PLN: PLN-2026-06-20-1620-mirror-stage-fix task 002.
**Context:** `pev_mirror.py` in staging mode names verdict files `HHMM-<flat-path>.txt`. Two mirror calls in the same minute (common when making multiple edits to the same file) write to the same path, each overwriting the previous. CHAIN.txt accumulates stale entries pointing to the same path with different hashes, causing `--audit` to flag false breaks. Confirmed non-tampering: three calls to pev_verify_task.py in the 16:15 minute during FW-006/008 fixes. Fix: use `HHMMSS` (ISO-8601 seconds) in staging verdict filenames. Requires updating `pev_mirror_lib.py` and `pev_mirror.py` where the staging path is constructed. `pev_revert.py --staging` also references this format — needs updating.

---

## [FW-2026-06-20-011] — pev_status.py [OV] false positive in get_mirror_indicator()
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Root cause: function scanned proof text for "MIRROR OVERRIDE" but proof diffs contain source code with that string literal. Fixed by checking plan.md frontmatter `overrides:` field and the verdict file directly instead of scanning proof text. Confirmed clean — PLN B drill-in now shows [M] on all 4 mirror-verified tasks.
**Context:** After PLN B, drill-in view shows [OV] (override used) on tasks that had no override. Root cause: something in the proof text triggers the `"MIRROR OVERRIDE" in proof_text` check. Likely pev_mirror.py is appending text to the proof file that contains this string in an unexpected way. Fix: narrow the check (look for the YAML `overrides:` field in plan.md frontmatter rather than scanning proof text). Low priority — verdicts are correct, chain is clean, only the display indicator is wrong.

---

## [FW-2026-06-20-009] — Rotate leaked API keys (DeepSeek x2, Resend, Grok, RunPod)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Deego rotated DeepSeek key and confirmed live (PLN B tasks 003-007 all got external verdicts 0.95-1.00 after rotation). Also used removal as a deliberate test — system fell back to self-mirror correctly, didn't skip the step. Resend/Grok/RunPod status: to verify separately.
**Context:** The Explore agent surfaced `ark.local` contents verbatim during the mirror planning session (PLN-2026-06-20-1256-mirror-core). Keys exposed: DEEPSEEK_API_KEY, deepseek_api_key, RESEND_API_KEY, grok_api_key, RUNPOD_API_KEY, vps_root_password. The DeepSeek keys are already returning 401 (confirmed by Task 8 of PLN mirror-core). VPS password exposure is highest risk — rotate first.
**Priority order:** (1) VPS root password, (2) DeepSeek keys (already dead but replace cleanly), (3) Resend, (4) Grok, (5) RunPod.
**Action:** Log into each service, rotate key, update `ark.local` with new value. Do NOT put new keys in any chat or commit message. Staged edit to `ark.local` via `pev_stage.py --file ark.local` (ark.local is NOT in the canonical list — plain stage, no mirror).

---

## [FW-2026-06-20-010] — Validate external mirror with live DeepSeek key (post-rotation)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. PLN B tasks 003-007 all received external DeepSeek verdicts (scores 0.95-1.00, trust: external). Chain audit confirmed 7 entries, 0 breaks.
**Context:** PLN mirror-core Task 8 tested only the self-mirror fallback path because the DeepSeek keys are 401. Once keys are rotated, run `python scripts/pev_mirror.py --file CLAUDE.md --snapshot <any-snap> --intent "smoke test with valid key"` to validate the external path end-to-end.

---

## [FW-2026-06-20-008] — PEV: Confirmed-at Timestamp Doesn't Insert in Plan.md (regex too narrow)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Widened task_block_pattern from narrow `(?:- [^\n]*\n)*` to full DOTALL block (stops at next ### or ---). Confirmed-at now inserts correctly after the Proof line even when a Check codeblock sits between Status and Proof. Smoke test passed.
**Context:** `pev_verify_task.py update_task_status` uses regex `### Task NNN —[^\n]*\n(?:- [^\n]*\n)*` to find the task block, then looks for the Proof line inside. But this regex stops at the first non-`- ` line (e.g. ` ```bash` in the Check codeblock), so Proof — which comes AFTER the Check codeblock — is OUTSIDE the matched block. Result: `Confirmed at: <timestamp>` line never gets inserted into plan.md. Cosmetic: time index can't show task-confirmed events because they rely on this field. Fix: use the wider regex pattern from `extract_task_block` (DOTALL, stops at next ### or ---).

---

## [FW-2026-06-20-007] — PEV: pev_edit.py snapshot field placement bug (FIXED IN-SESSION)
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. The find_task_block regex in pev_edit.py was too narrow (same bug as FW-008 above), causing the Snapshot field to be inserted BEFORE the Check codeblock instead of after the Proof line. Fixed by replacing with DOTALL regex matching to the next ### or ---. Discovered and fixed during PLN-2026-06-20-0317 task 003.

---

## [FW-2026-06-20-006] — PEV Verifier: Failed Counter Should Decrement on Retry
**Stated:** 2026-06-20
**Status:** done — 2026-06-20. Added `get_prior_task_status()` and `compute_counter_deltas()` to `pev_verify_task.py`. Transitions: pending→confirmed = +1 confirmed; failed→confirmed = +1 confirmed -1 failed; same→same = 0,0 (no double-count). All 6 transition cases pass smoke test.
**Context:** When a task fails then is fixed and re-verified, the `failed` counter in plan.md frontmatter stays at 1 while `confirmed` increments. Should: detect prior status before update and decrement the prior counter accordingly. Workaround: manually edit `failed: 0` and add `fail_then_pass: N` to preserve the history (used in PLN-2026-06-20-0307-shell-rule).

**Fix location:** `scripts/pev_verify_task.py` — in `update_counters` or before calling it, read the prior task status from the task block and apply the appropriate delta.

---

## [FW-2026-06-20-005] — Runtime Parallel/Sequential Enforcement (When Execution Interception Available)
**Stated:** 2026-06-20
**Status:** pending — blocked on tooling that doesn't exist yet
**Context:** Deego: "fi intercept the thoughts" — the idea of intercepting an agent's execution in real time and enforcing `[PARALLEL]`/`[SEQUENTIAL]` annotations at the moment a step fires. Currently impossible — there's no hook between a model reading a step and executing it.

**When this becomes possible:**
- If Claude Code exposes a PreStep or MidExecution hook, a script could read the current step's annotation and either (a) allow it to fire, (b) queue it for parallel batch, or (c) block it until a dependency resolves
- Would require the PEV plan format (FW-2026-06-20-004) as the underlying plan representation — the hook reads the plan file, checks the step annotation, enforces behavior

**Current approximation:** The `[PARALLEL]`/`[SEQUENTIAL]` annotations in procedure files are instructions to the model, not hard locks. PEV's check-per-task gates at least verify that parallel tasks *completed* before moving on — it doesn't guarantee they ran simultaneously, but it confirms the outcome.

**Monitor:** Claude Code hooks changelog for PreToolUse, agent interception, or chain-of-thought interception APIs.

---

## [FW-2026-06-17-003] — Move domain_keyword_map.py from C:\tmp into the Repo
**Stated:** 2026-06-17
**Status:** done — 2026-06-21. Moved to `MIndwaVe_Ja/local_model_benchmarks/domain_keyword_map.py` — same folder as `journal_sweep.py`. The bare `from domain_keyword_map import DOMAIN_KEYWORDS` import in journal_sweep.py works unchanged since Python will find it in the same directory. Import verified (21 domains). Original at C:\tmp untouched per CON-001.
**Context:** The 21-domain keyword map (1,233 keywords, 74-75% Patois) is currently at `C:\tmp\domain_keyword_map.py` — a temp location with no git history.

Move to `MIndwaVe_Ja/local_model_benchmarks/` or `PROJECTS IN MOTION/augmentation-forge/` for permanence. The sweep script (`journal_sweep.py`) imports from it — update the import path after moving. Version it so keyword list changes are tracked.
**File to move:** `C:\tmp\domain_keyword_map.py`
**Also move:** `C:\tmp\journal_sweep.py` to the same location.

## [FW-2026-06-23-006] — Chat2Cash: Domain Purchase Before Launch
**Stated:** 2026-06-23
**Context:** chat2cash PWA build session. Currently lives at chat2cash.mindwaveja.com — needs its own domain for launch credibility.
**Status:** pending — poverty-based deadline (Deego's words)
Buy chat2cash domain (chat2cash.com if available, chat2cash.app, or chat2cash.gg as fallback). Wire via Nginx on VPS same as other apps. SSL via certbot webroot pattern.

---

## [FW-2026-06-23-005] — Chat2Cash: Voice Notes Pipeline (Phase 2 Product)
**Stated:** 2026-06-23
**Context:** Chat2Cash build session — voice notes teased in Step 04 of current landing. This is the actual premium product.
**Status:** pending
Payout range: 300 JMD – 7,000 JMD per voice note. Two playable example voice notes on landing with estimated payout shown (same UI pattern as text example cards). Caveat copy: "Yardie accent, country voice, thick Patois — the more authentic yuh sound, the higher it scores." Voice types: ALL welcomed — rare/distinct accents score highest. Backend: audio upload → WhisperX transcription on RunPod → dialect classification → payout estimate. Notify-me email capture already in LandingHero Step 04 — upgrade to full form (name, town, county, age, email) and wire to a waitlist table in SQLite.

---

## [FW-2026-06-23-004] — Chat2Cash: Live Tally Stats Card
**Stated:** 2026-06-23
**Context:** Chat2Cash build session — Deego wants a public-facing stats display using the Linguistic Density Valuation card layout.
**Status:** pending
Show on landing: total chats submitted, total messages gathered, total JMD paid out. Pull from SQLite (datasets + transactions tables). Expose via `/api/stats` endpoint. Update in real time or on page load. Use the existing dark card UI pattern from FileProcessor (emerald stats grid).

---

## [FW-2026-06-23-003] — Chat2Cash: WiPay Currency Conversions on Payout Display
**Stated:** 2026-06-23
**Context:** Chat2Cash build session — app currently shows JMD only, WiPay covers JM, TT, BB + others.
**Status:** pending
Add currency conversion display on the payout calculation section. Show equivalent in TTD and BBD alongside JMD. Use a static conversion rate (updated manually monthly) or a free FX API. Countries supported: JM (JMD), TT (TTD), BB (BBD). Display as "JMD 500 ≈ TTD 22 ≈ BBD 18" style inline conversion hint.

---

## [FW-2026-06-23-002] — Earn.mindwaveja.com: Lead Capture Overlay + Payout Doubling
**Stated:** 2026-06-23
**Context:** Chat2Cash session — Deego realized earn.mindwaveja.com can be repurposed as a Chat2Cash / data platform lead capture page while portal is being built.
**Status:** pending
Changes:
1. Nav links remain clickable (auth/login flow stays).
2. All other clicks (hero CTA, body content, any non-nav element) → trigger a "Get Notified" popup modal.
3. Popup form: name, town, county, age, email. Stores to a `leads` table (new SQLite table or Postgres).
4. Modal copy: "The portal is coming. Drop your details and you'll be first through the door."
5. Double the existing earn payout rates from FW-2026-04-18-011:
   Under 3 min: $400 | 3–10 min: $1,000 | 10–20 min: $1,800
   20–45 min: $2,760 | 45–70 min: $7,000
6. Source the YouTube video list for transcription jobs — this list was referenced in FW-2026-04-18-011 but never populated. Needs a dedicated sourcing pass: Patois-rich Caribbean YouTube content (interviews, comedy, drama, news).

---

## [FW-2026-06-23-001] — AI Handoff Procedure / Skill
**Stated:** 2026-06-23
**Context:** DeepSeek ran Phase 1 of chat2cash cleanup inside VS Code with no workspace rules context — worked out fine but could miss constraints on a more dangerous task.
**Status:** pending

Build a reusable handoff procedure/skill that generates a self-contained context block whenever work is being handed from one AI tool to another (Claude Code → DeepSeek, DeepSeek → Codex, etc.). The block must include: active branch, stack rules, what NOT to touch, exact task scope, key constraints (CON refs), and the package manager. Should live in `procedures/handoff.md` with a `.claude/skills/handoff` adapter. Trigger: any time a task is being handed off mid-session to a different AI tool or IDE.

---

## [FW-2026-06-22-001] — Vape Check System: Extend to All Active Apps
**Stated:** 2026-06-22
**Context:** Vape check built for FIFA app, portable version at MW_CENTRAL/scripts/vape_check.py
**Status:** pending

Apply `vape_check.py` to other active apps. Priority order:
1. `active_apps/mindwaveja.com` — create VAR_MAP.md, run discovery mode to find undocumented variables
2. `active_apps/ovandobrown-v3` — especially the ADTL funnel flow variables
3. `PROJECTS IN MOTION/augmentation-forge` — Python backend state variables
Add each project's `VAR_MAP.md` + `.vscode/mcp.json` for session bus connection.

---

## [FW-2026-06-22-002] — Chat2App: Self-Hosted Privacy Architecture
**Stated:** 2026-06-22
**Context:** 10:53pm rehearsal insight — Jamaicans won't trust an app that sends their data externally
**Status:** pending

Chat2App must run the anonymization model on a self-hosted VPS. Architecture:
- Model runs locally on VPS (or serverless VPS)
- Strips contact names + phone numbers from WhatsApp chat export
- Replaces with anonymized names from an internal database
- Zero chat data leaves the system
- Self-hosting is the pitch: "more paranoid than you"
Reference: Chat2Cash existing infrastructure + `auth/auth_orientation.md` for pattern.

---

## [FW-2026-06-22-003] — MW Truth Tree: Automated Variable Discovery Tool
**Stated:** 2026-06-22
**Context:** vape_check.py --discover mode proves the concept — needs to be more general
**Status:** pending

Build a standalone tool that scans any codebase and generates a starter VAR_MAP.md automatically from discovery. Should:
- Find all exported functions, hooks, context providers, constants
- Cluster them by file and relationship (same import chain = related)
- Generate MW-Vxxx draft entries with file:line evidence pre-filled
- Output a draft VAR_MAP.md the developer then edits to add `.c` and `.rel`
This is the "automatic truth tree bootstrapper" — reduces setup time from hours to minutes.

---

## [FW-2026-06-22-004] — FIFA App: Correct Score Odds Scraping (Phase 2)
**Stated:** 2026-06-21
**Context:** Correct Score Dutch mode requires user to manually enter scoreline odds in Phase 1
**Status:** pending

Phase 2: scrape correct score odds from Google Search (`"Spain vs England correct score odds"`) or an odds aggregator. Return top 8 scorelines with odds pre-filled in BetSlip Correct Score mode. Use same scraping infrastructure as ESPN cache.

---

## [FW-2026-06-24-002] — Build a "features" Claude skill + update post-app-change procedure

**Stated:** 2026-06-24
**What:** Create a Claude skill (`features`) that knows how to read and update FEATURES.md files across apps — stages, lifecycle moves, date stamps. Update `procedures/post-app-change.md` to reference the skill. Then use both to create FEATURES.md for every Frame 1 app that doesn't have one yet.

**Apps needing FEATURES.md:**
- Marcus Garvey App
- Chat2Cash
- Ovandobrown.com
- MindWave JA Hub (mindwaveja-v2)
- Aidonia
- Chronic Law
- Tarrus Riley

**Why:** Feature lifecycle is invisible without it. Theory → design → in-dev → live → deferred → archived gives every session a shared reference for what's real vs what's still in someone's head.

## [FW-2026-06-25-001] — Red Team / Blue Team Security Session

**Stated:** 2026-06-25
**Context:** Realised during ovandobrown.com portfolio scrub that "20+ live apps behind a single IP" is an attack surface signal. One VPS, everything on it. Time to audit properly.

**Red team (find the holes):**
- Port scan the VPS — what's exposed externally that shouldn't be
- Check if Postgres is accessible outside the Docker network
- Marcus Garvey admin routes audit (`/browse`, `/workflow`, `/log`, `/devops` — currently unlinked but still live)
- Rate limiting gaps — Chat2Cash, earn, API endpoints
- Env var exposure check across all containers

**Blue team (harden):**
- Fail2ban on the VPS
- UFW firewall — only 80/443/22 open externally, everything else blocked
- SQLite DB file permissions (bind mounts)
- Admin login routes (picture password is a start — extend to other apps)
- Automated backup verification

**Run as:** Dedicated session — red team findings first, then blue team fixes.

---

## [FW-2026-06-26-001] — Forge Studio: DeepSeek API Key Renewal for Real Generation
**Stated:** 2026-06-26
**Context:** All 5,411 Marcus Garvey Q&A pairs generated with mock fallback (smart synthesizer using context fields + source text lookups). DeepSeek key returning 401. Real generation needs a live key for proper AI-synthesized Q&A pairs with better question variety and answer phrasing.
**Status:** pending

Renew DeepSeek API key, update `ark.local`, regenerate the 4 QA tracks against the 5 Marcus source datasets. Current mock fallback produces solid structure but limited question variety (templated per track). Real DeepSeek would produce more natural Q&As.

---

## [FW-2026-06-26-002] — Forge Studio: Quality Filter for Short/Citation-Only Answers
**Stated:** 2026-06-26
**Context:** ~5% of generated T1 Timeline answers are <50 chars — pure citation lines from the World of Marcus Garvey (Stein) source (e.g. `"May 13,1920 50.00"`). These are source-limitation rows where the DB field contains only a citation reference, not prose.
**Status:** pending

Add a quality gate to `_synthesize_timeline_qa`: if the scoped output is <80 chars and appears to be a citation-only string (no narrative structure), flag the pair with `_quality: { low_content: true, reason: "citation_only" }` and/or skip generating that row. Could also enrich from adjacent source rows or the DB event field as fallback.

---

## [FW-2026-06-26-003] — Forge Studio: Regenerate T2 Entity QA with Entity-Org Resolver
**Stated:** 2026-06-26
**Context:** T2 Entity QA track (1,724 pairs) was regenerated before the entity-org resolver fix (48 adversarial entities tagged as EXTERNAL). May have false org linkages from the pre-fix generation pass. T1 was also pre-date-scoping fix but was fully regenerated this session.
**Status:** pending

Regenerate T2 Entity QA with the current entity resolver (`_resolve_org_membership` with adversarial filter) active. Export final JSONL with all 4 tracks at consistent quality level.

---

## [FW-2026-06-26-004] — Forge Studio: Multi-Source Answer Enrichment
**Stated:** 2026-06-26
**Context:** Currently each QA pair draws from a single source file. T4 Financial and some T1 Timeline rows would benefit from cross-referencing — a financial record might have details across UNIA Papers + timeline entries.
**Status:** pending

When a T4 financial record's source text is thin (<100 chars), search the A1 Timeline for matching dates/events that provide context. Same for T2 entities — cross-reference with timeline events mentioning the person. This closes the remaining "citation-only" answer gap.

## [FW-2026-07-01-001] — Mindwave Music Charts (MWMC) MVP

**Origin:** Session 2026-07-01 — Phase 1 Ads work uncovered that dancehall has no accessible streaming metrics aggregator (INS-020)

**What:** Build a static/public metrics surface for Caribbean artists. Aggregate YouTube views, Spotify streams, monthly listeners, video counts into one accessible page per artist. Test subjects: Phase 1 artists (Aidonia, Chronic Law, Tarrus Riley). Prove viability independently then fold into RAAS suite as the official analytics layer.

**Why now:** Phase 1 domain ads need accurate stats. The manual assembly exposed the gap. MWMC solves both the immediate need (ad copy accuracy) and the structural gap (no Caribbean music data aggregator exists).

**Scope:** MVP = 3-5 artists, static page, public. Later: RAAS integration, API, self-serve artist dashboard.

**Depends on:** Kworb/direct platform data for total stream aggregation.

**Related:** INS-020 (`ideas/insights/insights_index.md`), `marketing&promotions/PHASE_1_ADS_TODO.md`

## [FW-2026-07-01-002] — Sunset CLAUDE.md: Migrate Rules to Active Context Files

**Origin:** Session 2026-07-01 — Playground naming convention (buried in CLAUDE.md §Naming Conventions) was ignored by me in the same session I read it. Moved to AGENTS.md as Hard Rule #9 and instantly enforceable.

**Problem:** CLAUDE.md is a reference doc — 800 lines. Rules buried in reference sections don't get enforced. Only the active context files (AGENTS.md for Codex, `.deepseek/SYSTEM.md` for DeepSeek, `.clinerules/` for Cline) get loaded at session start and shape behavior.

**What to do:** Audit CLAUDE.md. Extract every behavioral rule, naming convention, and enforcement pattern. Relocate to the appropriate IDE-specific active context file. CLAUDE.md stays as the canonical workspace map ONLY — no rules, no conventions, no procedures. Those belong in files that actually load.

**Why now:** This session proved the gap. I read the naming convention, I used it earlier in the same session (`dancehalldata-spec.md` should have been the name), and I STILL created `SPEC.md` out of muscle memory. The rule was in the wrong file.

**Related:** INS-020, AGENTS.md Hard Rule #9, session-log 2026-07-01 Addendum 2

## [FW-2026-07-01-003] — AI-Native Search Engine (Feasibility Study)

**Origin:** Session 2026-07-01 — Every attempted web search (Google, Bing, Spotify, Kworb) blocked by 403/JS-walls. Julius Mwale verification required external AI tool. Pattern recognized across 10+ failed searches in one session.

**Problem:** Major search engines actively block automated HTTP requests from AI agents. The internet is becoming unsearchable by the tools that need it most. This is not a technical limitation — it's an architectural decision by the centers (Google, Bing) to maintain control of the search layer.

**What to explore:** Feasibility study for an AI-native search engine. Different from traditional search: not serving humans clicking links, but serving AI agents that need structured, verified information retrieval. The search engine that works for the users Google blocks.

**Why now:** 10+ failed search attempts in one session. The problem is concrete, recurring, and grows with every walled-off data source. DancehallData's retrieval layer already half-solves this for one domain (Caribbean music). The principle generalizes.

**Connection to INS-021:** This is the third instance of the edge-center innovation pattern observed today. Build from the edge (where the blockage is felt) until the edge becomes the new center.

**Related:** INS-021, INS-020, DancehallData (`playground/2026-07-dancehalldata/`), Julius Mwale discovery

## [FW-2026-07-14-001] — ADTL price sync across marketplace/store
**Stated:** 2026-07-14
**Context:** Full-site audit found marketplace/store showing $5,200 while ADTL page updated to $4,200. Products.json fixed but needs live verification.
**Status:** pending

## [FW-2026-07-14-002] — FAQ section on home page
**Stated:** 2026-07-14
**Context:** Every footer links to /#faq but no element with id="faq" exists on the home page. Dead anchor on all 16 pages.
**Status:** pending

## [FW-2026-07-14-003] — Dancehall Data dedicated domain
**Stated:** 2026-07-14
**Context:** Home page has DancehallData section as placeholder ("Coming Soon"). Deego wants a dedicated domain (not subdomain) but no budget yet.
**Status:** pending

## [FW-2026-07-14-004] — Store & marketplace content differentiation
**Stated:** 2026-07-14
**Context:** /store and /marketplace render identical content. One should redirect or have distinct content.
**Status:** pending

## [FW-2026-07-14-005] — Artist count sync (18 in data, "20" in copy)
**Stated:** 2026-07-14
**Context:** ARTISTS array has 18 entries but multiple pages still reference "20 Jamaican artists".
**Status:** pending

## [FW-2026-07-20-001] — Artist-site dependency advisory cleanup
**Stated:** 2026-07-20
**Context:** Production builds for Aidonia and Tarrus reported npm audit advisories after the reusable lead-capture rollout.
**Status:** pending

Remove Aidonia's unused server/AI dependencies (`express`, `@google/genai`, and their transitive `protobufjs`/`ws` paths), upgrade Vite/Babel/esbuild where compatible, rebuild both sites, rerun `npm audit`, and redeploy only after visual and lead-capture regression checks pass.

**How we got here:** Docker build warnings prompted a direct audit. Aidonia has 7 advisories (3 high, 2 moderate, 2 low); Tarrus has 2 (1 high, 1 low). Both are static Nginx deployments, so most exposure is build/dev-side, but the dependency trees should still be reduced and patched.

## [FW-2026-07-20-002] — VPS GitHub deployment authentication and repository reconciliation
**Stated:** 2026-07-20
**Context:** Aidonia and Tarrus commits pushed locally, but the VPS could not authenticate to their private HTTPS GitHub remotes during deployment.
**Status:** pending

Configure narrowly scoped read-only GitHub deploy access for the VPS, preferably per-repository SSH deploy keys. Then reconcile `/opt/mw/aidonia`, `/opt/mw/tarrus-riley`, and the dirty `/opt/mw` infrastructure checkout with their recorded GitHub commits without overwriting server-only media or historical live configuration.

**How we got here:** Internet connectivity recovered, but `git ls-remote` still returned exit 128 for both private remotes; the VPS has no SSH key or credential helper. Deployment therefore used timestamped backups plus direct copies of committed files.

## [FW-2026-07-20-003] — Complete MindWave Admin operator checks
**Stated:** 2026-07-20
**Context:** Owner login and lead display passed, and new Aidonia/Tarrus leads are retrievable through the admin.
**Status:** pending

Verify filtering by site slug, CSV export, and session persistence after refresh. Record the results in the launch audit before paid traffic begins.

## [FW-2026-07-27-001] — Scraper Control Room as civic-data operations standard
**Stated:** 2026-07-27
**Context:** The civic-app programme now has multiple parallel source inventories, resumptions, downloads, extraction and verification paths. Owner identified the need to see progress and current standing across all moving parts.
**Status:** active

Maintain the local Scraper Control Room as the read-only operating view for every scraper: shared lifecycle phases, one primary phase, explicit approved parallel work, dated events, evidence paths, scrape provenance, remaining queue/gap visibility, and the next decision. A completed batch must never be represented as completed source coverage without chain evidence.

## [FW-2026-07-29-001] — Jamaica civic corpus full-coverage and update provenance
**Stated:** 2026-07-29
**Context:** The owner set the current civic collection as an evidence-labelled MVP after identifying depth, host, source-type, page, download, and later retrieval boundaries. The long-term goal is a defensible public knowledge system, including historic and amended government records where they are publicly available.
**Status:** active

Maintain a full-coverage programme after the MVP: reconcile each source's crawl chain; enumerate public sitemaps, indexes, APIs, document repositories, and approved official external domains; retain an explicit ledger for every acquired, duplicate, excluded, source-missing, held, and pending artifact; and record retrieval date, original source URL, hash, version/update lineage, and citation anchors. The civic RAG must distinguish current material from earlier versions and never imply that a bounded MVP is exhaustive.

**How we got here:** Fixed depth/page ceilings protect infrastructure but can make public knowledge unavailable when treated as unreported completion. The owner requires the same provenance discipline for Jamaican civic material as for the Solobic system.

## [FW-2026-08-13-001] — User-directed anonymization correction before Chat2Cash submission
**Stated:** 2026-08-13
**Context:** Automated anonymization can miss personal or sensitive details inside a response. The contributor needs a final, visible correction path before any dataset is submitted.
**Status:** pending

Add a pre-submission review mode where a contributor can select a missed response or text span and replace it with generic data. The original selected text must be removed from the outbound dataset, and the replacement must be visibly marked as contributor-directed anonymization in the local preview and submission provenance. Preserve the contributor's ability to cancel; do not silently alter text or retain the original in the shared dataset.

**Acceptance criteria:** The review flow works on mobile; replacement is explicit and reversible before submission; submission stores only the replacement; and the interface explains that the selected original will not be included in the shared dataset.

## [FW-2026-08-13-002] — Chat2Cash privacy-safe analytics and identity hardening programme
**Stated:** 2026-08-13
**Context:** Chat2Cash currently has page-view analytics and password-only contributor authentication. The next launch phase needs trustworthy funnel measurement, contributor recovery, and stronger staff protection without sending chat content or personal identifiers to analytics.
**Status:** pending

Implement in dependency order:

1. Add a privacy-safe Umami funnel: `cta_start`, `signup_started`, `signup_completed`, `signin_completed`, `chat_processed`, `anonymization_review_opened`, `anonymization_correction_saved`, `submission_completed`, `duplicate_blocked`, and `payout_requested`. Events must never include chat text, filenames, email, phone, user IDs, hashes, payout values, or free-text notes.
2. Improve contributor authentication: password-strength feedback and stronger password policy; endpoint-specific sign-in/sign-up throttling; password reset; and email verification enforced before the first payout request, not before anonymization preview or submission drafting.
3. Add the contributor-directed anonymization correction flow before final submission, and track only the aggregate correction event described above.
4. Harden staff access first among privileged accounts: MFA or passkeys for owner/admin roles; explicit session/device list and “sign out everywhere”; then move rate limiting from process memory to Redis or a database-backed shared store before traffic scales.
5. Minimize the public reconciliation endpoint to aggregate totals and deliberately anonymized receipt/status material. Keep contributor details, filenames, hashes, internal moderation data, and administrative controls authenticated.

**Release gates:** privacy review of every event payload; local and production auth-flow test; session invalidation test; password-reset test; payout-verification gate test; staff step-up test; public-ledger field audit; and an analytics check confirming events appear without personal data.

## [FW-2026-08-14-001] — Cross-app launch operations and playground graduation audit

**Stated:** 2026-08-14
**Context:** Chat2Cash marketing preparation exposed a recurring launch problem: multiple apps and products will need content, rollout material, and operational readiness as the release cadence approaches one app per week. The workspace needs a repeatable way to identify which playground artifacts should graduate, where promotion ideas belong, and what each launch still lacks.
**Status:** active

Build a cross-app operating pass that:

1. Inventories active apps, their live/staged status, owner-facing next action, and associated marketing material.
2. Reviews `playground/` for artifacts ready to graduate into a permanent product, marketing, procedure, infrastructure, ideas, or archive destination; preserve source provenance and do not delete originals.
3. Establishes a per-product promotion record that connects raw ideas in `marketing&promotions/brainstorms/` to briefs, copy, creatives, screen recordings, launch links, and post-launch learning.
4. Defines the minimum release packet for an app before its weekly drop: product truth check, domain/SSL check, privacy/security review, recording or creative, copy/caption, support/FAQ path, analytics plan, and rollback/owner action.
5. Produces an ordered queue rather than assuming every active app is ready to launch.

**First dependency:** The marketing intake route must exist so new promotion thoughts are captured while the audit is being designed.

## [FW-2026-08-24-001] — Two-format app walkthrough-video rollout

#type:instruction #jhanos:LOMI
**Stated:** 2026-08-24
**Context:** Owner confirmed the production approach after deciding that static page captures plus separately recorded voice-over are more comfortable and reliable than a live screen-recording walkthrough.
**Status:** pending

Create two walkthrough-video versions for MarcusGarvey876 first, then Chat2Cash:

1. A mobile-first vertical version for social channels and YouTube Shorts.
2. A desktop/web version for YouTube, paced more slowly so the archive, citations, and product flow can be seen clearly.

Use clean page screenshots rather than one continuous capture; record the voice-over independently and assemble each version from the same page-by-page story. Confirm the current live pages in both layouts before capture, use only fictional/demo data, and preserve the existing privacy / source-grounding guardrails in the product briefs.

---

---

## [FW-2026-09-02-001] — Desktop surface for agent-space entities
**Stated:** 2026-09-02
**Status:** pending

Build or adapt the Hermes Desktop app layer so TCP/Plato/Onu can appear as first-class agent-space entities, not "bots." The runtime surface should preserve the canonical agent_space shape: scoped roots, route indexes, SOUL/USER/MEMORY/SCOPE files, report contracts, and strict write boundaries.

## [FW-2026-09-13-001] — Scope-root naming signal guard for cleanup/move operations
**Stated:** 2026-09-13
**Status:** pending

Add a pre-move/workspace-cleanup guard that checks whether a requested quarantine/trash folder name implies a higher scope root than the folder being inspected. Example: when the inspected path is `ANDROMALIUS/agent-procedures/` but the requested quarantine name is `pluto_TRASH`, the naming signal points to `ANDROMALIUS/` root, not `agent-procedures/`. Before moving files, derive and report inspected path, action root, quarantine root inferred from folder name, naming-signal confidence, and a confirmation requirement if inferred roots disagree.

## [FW-2026-09-13-002] — Naming-sense standardization across the workspace
**Stated:** 2026-09-13
**Status:** pending

Folder and file names must say plainly what is inside; no metaphor, no drift-prone divergence. Standardize naming conventions so the name signals the content: e.g. `resolved-flaws.md` (not `FLAWS.md` when all flaws are resolved), `mw-session-close.md` (not a divergent `session-close.md`), `frameless/` (not `frameless ensure all in here is enforeed with proof/`). A file whose name no longer matches its content is a naming drift and must be renamed or re-homed, not left to confuse a future operator.

---

## [FW-2026-09-13-003] — Create gem_registry.md and seed with first gems from processed entries
**Renumbered from:** FW-033 (duplicate ID collision resolved 2026-09-13)
**Stated:** 2026-04-03
**Context:** Every striking one-liner or dense phrase from the journal gets a `#gem:slug` tag and an entry in the gem registry. These are high-value LLM training data, potential lyrics, potential book titles, potential axiom seeds. First real gem found: "me neva mek dis appointment wid disappointment" (Sep.24.25).
**Status:** pending

Create `MIndwaVe_Ja/mw_fine_tune_plan/solob_pob_llm/ovando_brown_profile/gem_registry.md`. Seed with gems found during the first batch of journal processing. Format defined in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 14.3.

---

---

## [FW-2026-09-13-004] — Add Sections VII–XI to General_archetype_profile.md
**Renumbered from:** FW-034 (duplicate ID collision resolved 2026-09-13)
**Stated:** 2026-04-03
**Context:** The current archetype file has 6 sections. As journal extraction matures, 5 more sections need to be added: Emotional Range Map, Relationship Archetypes, Recurring Metaphors, Contradiction Log, Domain Expertise Map. These can only be built from actual processed entries — not invented.
**Status:** pending

Begin once 50+ journal entries have been processed and tagged. Start with Section VII (Emotional Range Map) since tonal states are being tagged from day one. Add sections progressively as data accumulates. Spec in `playground/2026-04-journal-cowork-protocol/journal-cowork-instructions.md` Section 16.3.

---

---

## [FW-2026-09-13-005] Sovereign IDE — Knowledge-Connected Dev Environment
**Renumbered from:** FW-2026-04-15-003 (duplicate ID collision resolved 2026-09-13)
**Filed:** 2026-04-15
**Priority:** High (daily pain point)
**Source:** `drayl_journal/2026/26.APR/Apr.15.26.md` 2:40pm

IDE or VS Code extension that queries MW_CENTRAL/LanceDB as you build — surfaces relevant ideas, ADRs, axioms, and prior decisions based on what you're typing. Your corpus, not the internet. WGP fallback built in for rate-limited sessions.

**Foundation already exists:** LanceDB live in MW_CENTRAL, extraction pipeline structured and tagged.
**Fastest path:** VS Code extension wrapping the LanceDB query layer.
**Idea file:** `drayl_journal/_extraction/ideas/tech/APR-2026-sovereign-ide.md`
**Status:** Concept only

---

---

## [FW-2026-09-13-006] RAAS Frame — Artist Website Framework + Web Licence
**Renumbered from:** FW-2026-04-15-004 (duplicate ID collision resolved 2026-09-13)
**Filed:** 2026-04-15
**Priority:** Critical (20 domains renewing June 2026)
**Source:** Live session 2026-04-15

Premium bespoke artist website framework for established Jamaican/Caribbean artists. NOT templates — bespoke builds using RAAS Frame components. Primary value proposition: **accountability infrastructure, not aesthetics.** Irrefutable metrics (streaming, tickets, merch) that protect artists from management exploitation.

**Core components to build:**
1. HeroBlock — immersive, kinetic, artist-specific
2. SoundCanvas — music visualiser as UI
3. TracksPanel — discography with live streaming data
4. BookingBlock — revenue-generating booking form
5. PressKit — built-in EPK, first-class component
6. MetricsDash — the accountability layer (streaming, tickets, merch — irrefutable)
7. RiddimReel — live social feed, reason to return
8. ChronoLyne — artist story/timeline
9. MerchWindow — products as art
10. RAAS Countdown — platform chart of all RAAS artists

**Licence tiers:** Roots Frame | Rockers Frame | Royal Frame (bespoke, top dollar)

**The 20 domains:** Established artists who should have had sites ages ago. Each domain = unique bespoke site. Target price: $3,000–$10,000 per artist depending on scope.

**Deadline:** June 2026 domain renewals — need MVP before then

**RAAS Countdown feature:** Live public chart on RAAS platform ranking signed artists by streams/bookings/site metrics. Creates FOMO, social proof, healthy competition between RAAS artists.

**MindWave connection:** AI layer for bio writing, EPK generation, metric analysis, accountability reporting

**Project location:** `PROJECTS IN MOTION/Real Raas/`
**Status:** Framework concept complete — build not started

---

---

## [FW-2026-09-13-007] ROJ/RAL Reviews — Revive on Better Stack
**Renumbered from:** FW-2026-04-15-005 (duplicate ID collision resolved 2026-09-13)
**Filed:** 2026-04-15
**Priority:** Medium
**Source:** Live session 2026-04-15

Had rojreviews.com and ralreviews.com built and live but took them down due to Firebase + hosting friction. The idea was valid — staff/customer feedback platform for ROJ (Restaurants of Jamaica) and RAL. Domains still active (rojreviews.com exp Aug 3 2026, ralreviews.com exp Aug 7 2026, rojfeedback.online exp Jul 29 2026).

**Now fixable with:** Next.js + Better Auth (Oron) + PostgreSQL + Vercel/VPS. Firebase was the wrong tool. The stack he has now could build this cleanly in a weekend.

**Possible angles:**
- Internal: ROJ staff feedback system (leverage current role)
- External: Restaurant review platform for Jamaica (fill-a-hole-ja adjacent?)
- Accountability layer: same irrefutable metrics principle as RAAS — management can't deny what the dashboard shows

**Status:** Domains parked, no code currently deployed
**Update 2026-04-18:** Deego confirmed — check and refine both ROJ and RAL feedback apps and host them. Next actionable step after current session.

---

---

## [FW-2026-09-13-008] — Fix Cline adapter gaps + build Codex AGENTS.md
**Renumbered from:** FW-2026-06-20-007 (duplicate ID collision resolved 2026-09-13)
**Added:** 2026-06-20
**Context:** Simulation of tool flows revealed 3 gaps in Cline and Codex has no adapter at all.

Fix list:
1.  — update CON reference from CON-018 to CON-025
2.  — add BRANCH_STATUS update step (confirmed missing)
3.  at repo root — Codex reads this as its CLAUDE.md equivalent. Write with top 8 hard rules, workspace map summary, fork-first, no Genkit, no new Next.js, PEV reference.
4.  rules folder if needed after AGENTS.md proves useful

**Why:** Without AGENTS.md, Codex operates cold — no CONs, no fork-first, will violate CON-001/009/021/022 without knowing it.

---

## [FW-2026-09-13-009] — Session Parser: Log Everything Deego Says with Timestamp
**Renumbered from:** FW-2026-06-24-001 (duplicate ID collision resolved 2026-09-13)

**Stated:** 2026-06-24, ~12:15 Jamaica time
**Context:** Deego noted that he explained the MIndwaVe_Ja folder placement the night before, and it wasn't retained. He wants a system that parses everything said in a session and stores it in a database with date + time — so no instruction or intent ever gets lost between sessions.

**What it should do:**
- Parse all user messages from each session
- Extract: instructions, decisions, stated preferences, future work items, corrections
- Store each entry with: `date`, `time`, `session_id`, `content`, `category` (instruction / decision / FW / correction / insight)
- Make it queryable — "what did I say last night about MIndwaVe_Ja?"

**Possible approach:** Post-session hook that reads the Claude transcript and runs it through a classifier, then writes to a SQLite DB or appends structured JSONL. Could live in `scripts/session_parser.py`.

**Why:** Session memory loss is a real cost — Deego repeats himself, Claude misroutes. A timestamped log of stated intent closes that gap.

---

## [FW-2026-09-13-010] — Arbelos × Tetractys × Jainism/manji — solobic number-theory exploration
**Stated:** 2026-09-13
**Status:** hold_until_cockpit_autopilot

Explore why the arbelos metaphor and the tetractys (triangular number 10 = 1+2+3+4) connect to the solobic number theory, and why Solob feels structurally similar to Jainism — especially the manji (four-armed symbol) and its attachment. This is idea-exploration, not operational work; it must wait until the cockpit runs on autopilot.

## [FW-2026-09-13-011] — Memory/USER.md componentization + retrieval layer
**Refinement (2026-09-13):** Components must carry a relationship matrix, not just links. When one component is loaded, its transitive dependencies, contradictions, and co-load groups must enter context together, so the LLM can cross-reference and see contradictions in one thought. Key edges: depends_on, co_load_group, contradicts, similar_to, extends, groups_with.

**Stated:** 2026-09-13
**Status:** pending_design_decision

MEMORY.md and USER.md are flat, at capacity, with invisible redundancy. Migrate them to the component + retrieval (RAG) pattern: one concept per component file under ANDROMALIUS/MEMORY, a tiny always-on index, and on-demand retrieval like the prefrontal vortex. See decision: components-as-corpus, not components-as-manifest.

---

## [FW-2026-09-13-012] — While-hook for in-loop evidence, confidence, and route correction
**Stated:** 2026-09-13
**Status:** future_work
**Source:** Telegram session — T4 image was twice misread as T5 until a targeted re-check counted actual dots.

Create a `while_hook` alongside the existing pre- and post-tool hooks. The pre-hook protects scope before action; the post-hook audits effect after action; the while-hook protects the evolving thought/tool loop before a stale, contradicted, or low-confidence observation reaches synthesis.

**Required behavior:**
1. After every material tool/model result, compare it against the active evidence matrix and the user's latest correction.
2. Enforce evidence precedence: current direct verification > current-session verified state > durable verified state > historical note > inference. Superseded observations must not be presented as live facts.
3. If confidence is low, output conflicts with known evidence, or the route cannot inspect the modality, do not synthesize; select the next verified route.
4. Resolve matrix context in foundation order: prerequisites → reconciliation/contradictions → requisites/co-loads → dependents. Budget pressure cuts dependents first, never prerequisites.
5. Before rerouting, consult the verified model capability matrix, rate guard, account-pool state, and model lock. Do not rediscover or contradict already-verified routing infrastructure.
6. Record the winning observation, rejected observation, confidence, route used, and proof locator in an immutable while-hook receipt.
7. Stop retrying after bounded routes are exhausted and return an explicit uncertainty instead of a plausible reconstruction.

**Acceptance test:** Present Diagram 1 from `img_6f2c8d66a4a5.jpg`. A generic overview may misread five rows; the while-hook must trigger a targeted dot-by-dot recount and settle on **T4: four rows, 1+2+3+4 = 10 dots**, while retaining the rejected T5 claim as an auditable failed observation rather than canon.

**Boundary:** This entry authorizes design/prototyping later, not immediate activation in the live gateway. Hook activation requires a PEV plan, runtime smoke test, and rollback path.


---

## [FW-2026-09-14-001] — image_deScriber RAG experiment
**Stated:** 2026-09-14
**Context:** While placing angle labels and V4/V5 magenta-green field boxes in `overlay-mapper-v0.5-angle-fields.html`, Deego noted that the angle/anchor coordinate packets suggest a future RAG layer for the deScriber.
**Status:** pending

Add a future experiment that connects `image_deScriber` to a RAG pipeline and tests whether anchor packets, selected coordinates, path grammar, angle indicators, focal-field boxes, and source-linked image observations can be retrieved and reused without losing the spatial frame. Treat this as a prototype: first index exported JSON/coordinate packets and mapper notes with cited file/chunk references; then run verification queries such as “what rules the V4-T3/V5-T3 field?”, “where are the 85.7° lower-center labels?”, and “which anchors are highlighted-path versus off-path radios?” Do not call it semantic RAG until an actual index exists and queries return cited source chunks.

---

## [FW-2026-09-15-001] — Agent × Skill × Usage Matrix Expansion (Live Tracking)
**Stated:** 2026-09-15
**Context:** Matrix created as static mapping. Needs live invocation tracking.
**Status:** DEFERRED

Expand `MATRIX/agent-skill-usage-matrix.json` from static mapping to live tracking:
- Invocation counts per skill per agent per day
- Success/failure rates per skill invocation
- Route efficiency (fastest/most accurate agent per capability)
- Stale skill detection (unused 30+ days → flag for archival)
- Missing skill gaps (capabilities no covered agent covers)

**Dependencies:** Curator runner cron, 7+ days baseline, 3+ active profiles
**Resume condition:** 3 profiles active for 7+ days

---

## [FW-2026-09-15-002] — USER.md Per-Profile Capsules
**Stated:** 2026-09-15
**Context:** Working plan `2026-09-15_memory-autonomy-and-component-splits.md`
**Status:** DEFERRED

Create USER.md capsules for profiles that serve specific users/projects. Most profiles don't need them yet.
**Resume condition:** Any profile exceeds 50 lines of user-specific context

---

## [FW-2026-09-15-003] — MEMORY.md Per-Profile Capsules
**Stated:** 2026-09-15
**Context:** Working plan `2026-09-15_memory-autonomy-and-component-splits.md`
**Status:** DEFERRED

Create MEMORY.md capsules for profiles that accumulate durable facts. Content = durable facts only, no session-state.
**Resume condition:** Curator has 10+ staged candidates for any profile

---

## [FW-2026-09-15-004] — Curator Runner Cron Scheduling
**Stated:** 2026-09-15
**Context:** Curator runner built and tested
**Status:** DEFERRED

Schedule curator runner as daily cron job. Tier 1 daily, Tier 2 weekly, Tier 3 on-demand.
**Dependencies:** Curator runner stable for 7+ days
**Resume condition:** Runner has processed 7 consecutive days without error

---

## [FW-2026-09-15-005] — 8 Partial Agents Bring-Up
**Stated:** 2026-09-15
**Context:** AGENTS.md consolidation follow-up
**Status:** DEFERRED

8 agents remain partial (all scaffold, no live model/task/status surface):
APPCTX, CHAT_EXCAVATION_SCOUT, HERMESSPL, JHANOS_GATE, JHANOS_X_CUSTODIAN, SHADOW_JHANOS_GATE, TCP_LEGACY, TEMPLATE_EVOLUTION_SCOUT
**Dependencies:** User priority selection, model availability per agent
**Resume condition:** User selects which agent to activate next

---

## [FW-2026-09-15-006] — Curator Runner Merge/Split Detection
**Stated:** 2026-09-15
**Context:** Curator runner build — merge/split logic stubbed
**Status:** DEFERRED

Tier 2 logic: detect entries that should be merged (same fact, different words) or split (one entry, two facts).
**Resume condition:** 3+ profiles have MEMORY.md with 10+ entries each

---

## [FW-2026-09-15-007] — Agent Operationality Standard Enforcement
**Stated:** 2026-09-15
**Context:** Plan ledger + agent arena inventory
**Status:** DEFERRED

Enforce standard: Fully operational = live profile + model + task/status surface + evidence/proof + not merely scaffolded. Audit all 14 profiles.
**Resume condition:** User requests audit

---

## [FW-2026-09-15-008] — Cross-Profile Memory Contradiction Detection
**Stated:** 2026-09-15
**Context:** Curator design
**Status:** DEFERRED

When two profiles have contradictory durable facts, flag for human resolution (Tier 3). Cross-profile read = Tier 3 by definition.
**Resume condition:** 2+ profiles have MEMORY.md with overlapping domains

---

## [FW-2026-09-15-009] — Curator Evidence Format Validation
**Stated:** 2026-09-15
**Context:** Curator autonomy tiers
**Status:** DEFERRED

Validate all curator receipts include: source + hash + timestamp + agent + confidence + tier + action. Add JSON schema check.
**Resume condition:** After first week of curator cron

---

## [FW-2026-09-15-010] — Sealed Baseline Backup Root
**Stated:** 2026-09-15
**Context:** Working plan `2026-09-14_agents-md-and-backup-root-consolidation.md`
**Status:** ACTIVE

One-folder sealed backup capturing secrets/auth/DBs/configs; scheduled baseline-grade snapshots.
**Resume condition:** Next backup event or user activation

---

## [FW-2026-09-15-011] — Plaintext Reference Full Sanitation
**Stated:** 2026-09-15
**Context:** AGENTS.md consolidation
**Status:** PAUSED

Full text-search cleanup of remaining AGENTS.md/CLAUDE.md references in logs/plans/mirrors/reports. Exact-name files already cleaned from active surfaces.
**Resume condition:** User decides to resume

---

## [FW-2026-09-15-012] — Project Skill Conversion (Remaining Apps)
**Stated:** 2026-09-15
**Context:** AGENTS.md consolidation follow-up
**Status:** DEFERRED

Convert remaining active apps from CLAUDE.md/AGENTS.md to ANDROMALIUS project skills. love-ref and hermes-spl-fork done as pilots.
**Resume condition:** User selects next app

---

## [FW-2026-09-15-013] — RunPod Entropy Model (70B Uncensored)
**Stated:** 2026-09-15
**Context:** `ENTROPY_MODEL/RUNPOD_OUTPUTS/`
**Status:** DEFERRED

Full 70B uncensored model on RunPod for entropy generation. 8B fallback already produced 4 outputs.
**Resume condition:** User approves RunPod spend or alternative found

---

## [FW-2026-09-15-014] — RAG Prefrontal Memory System
**Stated:** 2026-09-14
**Context:** `2026-09-14_tris-prefrontal-rag-prehook.md`
**Status:** DEFERRED (UNBLOCKED)

Keyword RAG over versioned markdown + model matrix, prehook injection of bounded context packets. Component capsule structure now exists.
**Resume condition:** User activates

---

## [FW-2026-09-15-015] — 18 Formal Concepts Resolution
**Stated:** 2026-09-14
**Context:** KNOWLEDGE_LIBRARY/CONCEPTS/
**Status:** BLOCKED

18 formal concepts have unresolved open-questions blocking L4+ promotion.
**Resume condition:** User provides answers or approves promotion without

---

## Version log

- v1.0.0 — 2026-09-15 — Merged ANDROMALIUS framework FW entries (FW-2026-09-15-001 through 015) into canonical FRAMELESS/future-work.md. Capsule splits, curator autonomy, matrix, agent bring-up, sanitation, backups, RunPod, RAG, and concepts registered.

Extend the experiment into a **visual hindsight / correction-memory loop**: when the agent makes an image edit or interpretation error, the app should preserve (1) the full image view, (2) what the agent thought before correction, (3) the user's correction, and (4) the exact V/T grid cell, anchor, or field where the correction applies. This gives the next completion a coordinate-grounded correction history instead of a vague natural-language instruction such as “only change the cup,” reducing the risk that the agent edits a different cup-like object.

Add **grid-proximity retrieval**: each grid box can represent a local domain/context cell. For a current focal point or subject under discussion, retrieval should pull strongest from the focal cell, then nearby connected cells, then farther context only when needed. This supports controlled sharing: include only the topic-specific visual memory and adjacent directly connected context rather than dumping the whole memory field. Keep this as a future design until the app exports coordinate-linked chunks and retrieval tests prove the proximity weighting works.

---
name: context-window-verification
description: "LLM context window test via known-answer quiz slices."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, context-window, verification, testing, model-capability]
    related_skills: [spike, dogfood]
---

# Context Window Verification

Use when you need to **confirm what context window a model actually provides** at runtime, not just what docs claim.

## Core Method

Feed known text at increasing offsets, ask questions with known answers, and see where answers fail.

1. Pick a source document with **unique** content (no repetition).
2. Estimate tokens: `chars / 3.5` for English (conservative), or `chars / 1.2` for DeepSeek BPE.
3. Build slices at target sizes (e.g. 115K, 230K, 1.5M tokens).
4. Generate questions with known answers at evenly spaced intervals across the document.
5. **Paste each slice directly into chat** — NOT via file/tool (those have their own limits).
6. Answer questions from memory; compare against known answers.
7. The largest slice where you still answer correctly = effective context.

## Why this works

Tools like `read_file` have their OWN truncation (Hermes caps at 100K chars) — that hits before the model limit. **Only a direct user message exercises the actual model context window.**

## Token estimates

| Estimator | Use |
|---|---|
| `chars / 3.5` | Rough English, conservative |
| `chars / 1.2` | DeepSeek BPE, closer estimate |
| `words × 1.3` | Word-based for English prose |

## Question design

Questions need **deterministic known answers** at specific offsets:

- **Word-at-position:** "At offset X, what is the Nth word?" → single word answer
- **Sentence extraction:** "What sentence appears around offset X?" → full sentence
- **Fact retrieval:** Only if the fact appears ONCE (not repeated)

Avoid questions answerable from multiple locations.

## Slice strategy

| Slice | Purpose |
|---|---|
| Small (100K tokens) | Baseline — model can handle it |
| Medium (230K tokens) | Tests if free-tier cap is ~200K |
| Full (claimed max) | Confirms or denies the full claim |

## Interpretation

| Result | Meaning |
|---|---|
| All correct | Delivers on claimed context |
| Small + medium OK, full fails | Effective window between medium and full |
| Small OK, medium fails | Effective window ≤ small slice |
| All fail at small | Something else wrong (provider, model, etc.) |

## External source conflicts

When sources disagree:

- **Catalog listings** (models.dev, OpenRouter) → theoretical max
- **Free-tier routes** → may impose own caps
- **GitHub issues** → actual experienced limits
- **Provider config** (`opencode.json`) → client-side override limits
- **Hermes `context_length_cache.yaml`** (`~/AppData/Local/hermes/context_length_cache.yaml`) → cached runtime values per provider/model — more authoritative than web for models Hermes actually routes

The empirical test is the only way to resolve for your specific route.

## Endpoint reachability check (BEFORE building test harness)

**Always verify di endpoint serve di model before spending time on slices.** A 1.5M-token harness wastes a day if di model unavailable.

1. Check `provider_models_cache.json` (`~/AppData/Local/hermes/cache/provider_models_cache.json`) — lists which models each provider fingerprint knows about
2. Try a minimal curl to di endpoint with di model ID:
   ```bash
   curl -s -m 30 -X POST "$ENDPOINT/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Hi"}],"max_tokens":5}'
   ```
3. If response contain `"error"` with "unavailable" or "not found" — model not served, stop
4. If curl need auth key, check:
   - `auth.json` (`~/AppData/Local/hermes/auth.json`) for provider tokens
   - `provider_models_cache.json` `"fp"` field — `"keyless:PROVIDER"` means no explicit key needed

### Findings from this session (2026-08-30)

- **deepseek-v4-flash-free** via `https://opencode.ai/zen/v1`: endpoint reachable, curl return `200 OK`, but body contain `{"error":{"type":"server_error","message":"Error from provider (Console): Upstream request failed: Model is unavailable."}}` — model not currently served despite web claims of 1M context
- **`context_length_cache.yaml` nah list deepseek-v4-flash-free** — confirm it nah currently active in Hermes routing
- **`provider_models_cache.json` show `"opencode-free"` fingerprint as `"fp": "keyless:opencode-free"`** — auth may work without explicit key, but model availability is separate issue

See `references/opencode-endpoint-status.md` for full detail.

## Pitfalls

- **Using `read_file` or terminal** to load test text — tool limits mask model limit
- **Repetitive documents** — model guesses from earlier occurrences. Pick unique content (brainstorms, journal entries, original prose — not duplicated files or templated outputs)
- **Questions at only one offset** — doesn't reveal WHERE failures begin. Use 10+ questions per interval across 3+ intervals
- **Relying on catalog numbers** — theoretical, not experienced
- **One token ≠ one word ≠ one character** — estimate conservatively
- **Building harness before checking endpoint** — if model unavailable, all that work is wasted. Always curl-test first.
- **Token estimate variance** — differ by tokenizer. DeepSeek BPE: ~1 token per 1.2 chars for English text is more accurate than di conservative 3.5 ratio; di actual ratio depend on di specific tokenizer version. Plan with range, not single number.

## Files produced

```
playground/
├── context_test_1.5M.md      # Combined source
├── context_test_harness.json # Questions + known answers
├── slice_115k.md             # Small slice
├── slice_230k.md             # Medium slice
└── slice_full.md             # Full document
```

## Related skills

- **spike** — broader throwaway-experiment pattern
- **dogfood** — exploratory QA of web apps

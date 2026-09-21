---
name: programmatic-image-analysis
description: Describe image geometry when vision_analyze fails.
---

# Programmatic Image Analysis

Fallback when the vision model cannot see an image (e.g. `vision_analyze` on a local cache path like `/root/.hermes/cache/images/*.jpg` returns "no image attached"), or when you must characterize an image's *geometry* — shape, orientation, fold/edge lines, text — from pixels alone.

## Procedure (in order)

1. **Load and orient.** `Image.open(path)`, print `size`/`mode`, convert to `np.array(im.convert('RGB'))`; `gray = arr.mean(axis=2)`.
2. **Global scan first.** Row-mean and column-mean luminance profiles locate where dark/bright mass sits before zooming. Mean/min/max luminance plus saturation (`arr.max(axis=2) - arr.min(axis=2)`) classify the photo: low saturation ≈ warm/indoor shot, near-zero ≈ grayscale scan.
3. **Dark-pixel masks at multiple thresholds.** `dark = gray < 90` (darkest core) vs `< 100–120` (full extent). Render a binary mask to ASCII with `#`=dark, `.`=light to SEE the shape, not just numbers. Trace boundaries at fine resolution (≈200 cols over the ROI) to get exact coordinates of diagonal/vertical edges.
4. **Edge/detail map for text and fine structure.** `np.gradient` magnitude plus `gray - GaussianBlur(20)` as a detail map. Keep the gradient threshold LOW — smooth photos give mean gradient ~4–5, so a fixed high threshold blanks everything; rescale to the observed distribution (`np.percentile(mag, 90)`).
5. **RGB-sample regions — don't judge by luminance alone.** This is the decisive step: sample mean RGB of the "dark" shape vs background. A shadow is neutral/gray; a real object carries color (e.g. a "dark triangle" that is actually rust-orange `[151,89,19]` against tan background `[142,112,81]`). It distinguishes shadow from solid object.

## Output shape

Return a structured description: (1) geometric shape + orientation, (2) where it sits in the frame, (3) fold/edge lines, (4) any text resolved, (5) an explicit confidence level per item. Be honest about what you cannot resolve — a solid triangle touching the frame edge vs a two-sided outline is genuinely ambiguous from luminance alone; say so rather than guessing.

## Pitfalls

- **ASCII mapping direction is a silent bug.** With `chars = " .:-=+*#%@"` and `idx = v/256*len(chars)`, LOW idx = dark (space/`.`), HIGH idx = bright (`@`). Decide once, state it in a comment, don't flip mid-script.
- **A single threshold lies.** A shape's true extent needs 2–3 thresholds; `<90` shows only the darkest core and can make a solid band look like a thin outline.
- **Weak gradient ≠ no edges.** Rescale the edge threshold to the observed gradient distribution instead of using a fixed value.
- **Do not write files** when the caller said so — return the description inline.

---
name: gstep1-explanation-format
description: "When a grammar pattern in gstep 1 needs a friendly explanation, describe each concept on its own Korean→English line pair, plus a 예: example block. Do NOT use a forced A/B rule template — it doesn't fit all patterns."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**For grammar pattern explanations under the gstep 1 pattern box, follow this layout.**

**Why:** The user established this layout on 2026-05-28 while polishing Lesson 19 (~(으)려면), then refined it after seeing it applied to Lessons 18 and 1. Key correction: an "A 한다 B 한다" style rule template does NOT generalize across all grammar patterns (e.g., 때 doesn't form a clean A-B clause structure). Skip the template line entirely and describe each conceptual point directly.

**How to apply:**

After the pattern box (`<div class="gstep-pattern">`), add a green explanation box:

```html
<div style="padding:10px 14px; background:#ecfdf5; border-left:3px solid #10b981; border-radius:6px; margin-top:12px; font-size:0.92rem; line-height:1.8;">
    {concept 1 — Korean}<br>
    <small><em>{concept 1 — English}</em></small><br><br>
    {concept 2 — Korean}<br>
    <small><em>{concept 2 — English}</em></small>
    <div style="margin-top:12px; padding:8px 12px; background:#fff; border-left:3px solid #fbbf24; border-radius:6px; font-size:0.9rem;">
        <strong>예:</strong> {Korean example sentence in 격식체}<br>
        <small><em>{English translation}</em></small>
    </div>
</div>
```

Rules:
- **Do NOT include a synthetic A/B rule template line** (e.g., "A 하면 B 합니다", "A 때 B 합니다"). It looks tidy but breaks when the grammar doesn't form a clean two-clause structure. Just describe each conceptual point directly.
- **Korean first, English subtitle below** on a separate `<br>` line — applies to every conceptual line.
- **Each conceptual point on its own line pair.** Don't run multiple concepts into one paragraph.
- **예: block** with `<strong>예:</strong>` prefix, real Korean example in 격식체 (-ㅂ니다/습니다 per [[formal-style-examples]]), English translation below.
- **Colors are adverbial-category green** (`#ecfdf5` bg, `#10b981` border). For other categories, swap to the matching category palette.
- This block is **optional** — only add it when the pattern needs friendly prose explanation. For self-evident patterns, leave the pattern box alone.

Related: [[korean-english-pairing]], [[formal-style-examples]], [[lesson-grammar-summary-style]]

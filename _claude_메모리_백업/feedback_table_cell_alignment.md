---
name: table-cell-alignment
description: "All cells in 문법 정리 yellow tables (explain-note tables) must be center-aligned, including the \"예문\" / \"Example\" column. Default-left alignment for sentence cells is wrong."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**All table cells in 문법 정리 yellow tables must be center-aligned — including 예문 / Example sentence cells.**

**Why:** The user established this on 2026-05-28 while reviewing the ~고 / ~아/어서 comparison and Sequential/Independent tense table. By default I was leaving sentence cells left-aligned because they hold long text; the user wants visual consistency with the rest of the table (headers, labels, conjugation cells) which are already centered. Mixed alignment looks unbalanced.

**How to apply:**

When generating or editing tables inside `<div class="explain-note">` (the yellow-themed yellow tables in 문법 정리), every `<td>` must include `text-align:center`:

- ✅ `<td style="padding:10px; text-align:center; border-bottom:1px solid #fef3c7;">{cell content}</td>`
- ❌ `<td style="padding:10px; border-bottom:1px solid #fef3c7;">{cell content}</td>` ← missing text-align

Applies to:
- Conjugation tables (Lesson 1-5 style)
- Comparison tables (e.g., ~고 vs ~아/어서, 전에 vs 후에)
- 예문 / Example columns containing full sentences (the most commonly-missed case)
- 의미 / Meaning columns
- 자주 쓰는 대상 / Common objects columns

When you `<br>`-split Korean and English within a cell, the centering applies to both lines — that's intended.

Header cells (`<th>`) are already centered in the master template; this rule is about `<td>`.

Related: [[lesson-grammar-summary-style]], [[korean-english-pairing]]

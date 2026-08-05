---
name: batchim-table-labels
description: "In 받침 columns of grammar conjugation tables, use bold colored O/X — O = green (있음, has 받침), X = red (없음, no 받침). Keep the 없음/있음 Korean label and none/yes English on the next line."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**받침 columns must use bold colored O/X symbols with Korean+English labels below.**

**Why:** First (2026-05-28) the user asked for "없음/있음" with "none/yes" English to replace cryptic "X / O (ㄱ)" codes. Then (2026-05-30) the user asked to upgrade further — show **bold colored O/X symbols** as the primary visual, with 없음/있음 as a Korean label and none/yes as English on the next line. Symbols give an instant visual scan, the labels disambiguate.

**Color mapping (mandatory):**
- **있음 = O** = green (`#16a34a` or `#15803d`) — has 받침
- **없음 = X** = red (`#dc2626` or `#b91c1c`) — no 받침

**HTML template:**
```html
<td style="padding:8px 10px; text-align:center; border-bottom:1px solid #fef3c7;">
    <strong style="color:#16a34a; font-size:1.15rem;">O</strong><br>
    <strong>있음</strong><br><small><em>yes</em></small>
</td>
```
```html
<td style="padding:8px 10px; text-align:center; border-bottom:1px solid #fef3c7;">
    <strong style="color:#dc2626; font-size:1.15rem;">X</strong><br>
    <strong>없음</strong><br><small><em>none</em></small>
</td>
```

**How to apply:**
- The symbol (O/X) sits on the first line, bigger and colored.
- The Korean label 없음/있음 sits on the second line.
- The English none/yes sits on the third line in `<small><em>`.
- Never show the specific 받침 character (ㄱ, ㄷ, ㄹ…) — only whether 받침 exists matters for conjugation tables.
- Applies to: ~(으)니까, ~(으)려고, ~(으)러, ~(으)면, ~ㄹ/을까요, ~ㅂ/읍시다, noun + 을/를, and any future grammar with 받침-conditional endings.

Related: [[korean-english-pairing]], [[lesson-grammar-summary-style]]

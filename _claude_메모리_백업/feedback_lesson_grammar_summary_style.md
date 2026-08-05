---
name: lesson-grammar-summary-style
description: "Master template for 부사어 문법 (adverbial grammar) lesson summaries. Each lesson's Grammar Overview is restructured into 4-5 gsteps: pattern box, conjugation/usage tables, optional comparison, and word order."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**Master structure for 부사어 문법 grammar summaries.** Applied to Lessons 1-5 and 13-19 in this project.

**Why:** The user established this layered structure across sessions 2026-05-27 and 2026-05-28. Earlier verbose en/ko paragraphs and inconsistent tables were replaced with a uniform layout that aids both learners and future editors.

**How to apply:**

Replace the existing Grammar Overview (`<h2>Grammar Overview · 문법 정리</h2>` and following gsteps) with this layout:

### gstep 1 — Pattern box (mandatory)
- `<div class="gstep-pattern">` with only the pattern formula — no verbose en/ko intro paragraphs.
- For dual patterns (e.g., noun + 때 / verb + (으)ㄹ 때), put each on its own line via `<br>`.
- Optionally add a green explanation block below (see [[gstep1-explanation-format]]) for non-obvious patterns. Skip for self-evident ones.

### gstep 2 — 동사/형용사 conjugation table
- Green subtitle: `<h3 style="...color:#064e3b; background:#ecfdf5; border-left:4px solid #047857...">동사 + [어미]</h3>`
- Wrap the table in `<div class="explain-note">` with `<strong>📝 ...</strong>` heading.
- Yellow table (`background:#fde68a` header, `#fffbeb` even rows, `#92400e` result-cell color).
- Columns: 동사 / 받침 / 어간 + 어미 / 결과 (Verb / Final 받침 / Stem + ending / Full form).
- 받침 cells: use `없음 / none` or `있음 / yes` per [[batchim-table-labels]] — never raw "X" / "O (ㄱ)".
- 6 example verbs, balanced between 받침 없음/있음.
- Include at least one ㄹ-불규칙 verb when relevant (with note `(ㄹ drops before ㄴ)` or similar in the conjugation cell).

### gstep 3 — 명사 + [particle] common-usage table (when relevant)
- Green subtitle: `명사 + [particle] — 자주 쓰이는 명사`
- Same yellow-table style.
- Columns: 분류 (Category) / 명사 + particle / 의미 (Meaning).
- 4 category rows organized by domain (학교·직장 / 일상 / 인생 시기 / 행사 / 시간 etc.).
- Each cell has Korean main + `<small><em>English</em></small>` per [[korean-english-pairing]].

### gstep N-1 — Comparison or extra rule (optional)
- For lessons with related forms (전에 vs 후에, ~고 vs ~아/어서, ~(으)면 vs ~(으)려면, 때 vs 동안 etc.), add a comparison gstep.
- Green subtitle + green explanation box + yellow comparison table.
- Use `✅` (green #16a34a) and `❌` (red #dc2626) symbols where applicable.

### gstep N — 어순 (Word Order) — final gstep, mandatory
- Green subtitle: `어순 (Word Order)`
- Green explanation box: state where this adverbial sits in the sentence.
- Pattern box: `주어 + 부사어(시간/장소/원인/...) + 목적어 + 서술어(동사)` and English equivalent. Use [[combined-adverbial-role]] when multiple adverbials co-occur.
- Yellow `예 1 / 예 2` box at the bottom with two formal-style example sentences and English translations (per [[formal-style-examples]] and [[korean-english-pairing]]).

### Per-sentence explanation table headers
- Update the `<th colspan="4">` headers in each sentence's `exp-table` from `주어 + 시간 + 목적어 + 동사` style to `주어 + 부사어(시간) + 목적어 + 서술어(동사)` (and English to `Subject + Adverbial (Time) + Object + Predicate (Verb)`).
- When time + place / purpose + place / etc. co-occur, group as `부사어(시간+장소)` per [[combined-adverbial-role]].

### Verb conjugation breakdown cells (`<td>` in exp-table)
- Use the simplified arrow form `기본형 → 어간 + 어미 → 결과` (e.g., `잘하다 → 잘하 + 려면 → 잘하려면`).
- Drop verbose English explanations like "(verb, stem X, 받침 Y) ... ".
- For ㅂ/ㄹ irregulars, keep an arrow chain (e.g., `춥 + 으니까 → 추우 + 니까 → 추우니까`) — see specific irregular explanations in the gstep section, not the per-row cell.

### Catalog of lessons updated with this template
Lessons 1 (때), 2 (동안), 3 (전에), 4 (후에), 5 (~고), 13 (~아/어서), 14 (~(으)니까), 15 (위해서), 16 (~(으)려고), 17 (~(으)러 가다), 18 (~(으)면), 19 (~(으)려면).

Related: [[korean-english-pairing]], [[formal-style-examples]], [[batchim-table-labels]], [[gstep1-explanation-format]], [[combined-adverbial-role]], [[canonical-folder]]

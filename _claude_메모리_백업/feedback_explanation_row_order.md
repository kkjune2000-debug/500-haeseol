---
name: explanation-row-order
description: "Per-sentence explanation table rows must be arranged in English (textbook original) sentence order, not Korean order. The 원문 = the English source sentence."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**Arrange explanation table rows to match the English original sentence's word order.**

**Why:** The user clarified on 2026-05-28 that 원문 in this project refers to the **English sentence from the textbook**, not the Korean equivalent. Learners read the English first, so the table rows should mirror that reading order — making each English chunk align row-by-row with its Korean equivalent. Examples confirmed: 275 (He → finished work → met → his friend) and 276 (He → cleaned → did laundry → met → a friend → on the weekend).

**How to apply:**

For every `<table class="exp-table">` in per-sentence explanations:

1. **List the English chunks in the order they appear in the textbook English sentence.**
2. For each chunk, fill in: English / Role / Korean / Explanation.
3. The Korean column shows the matching Korean fragment, but its **position in the table is decided by the English order**.
4. The `<th colspan="4">` header at the top still describes the **Korean sentence's structural order** (e.g., `주어 + 부사어 + 동사(고) + 목적어 + 동사`) — that's independent of row order. The header describes the Korean structure; the rows walk through the English reading.

**Examples (correct row order):**

Sentence 275 — *He finished work and met his friend.* / 그는 퇴근하고 친구를 만났습니다.
| # | English | Role | Korean |
|---|---|---|---|
| 1 | He | Subject | 그는 |
| 2 | finished work and | Verb | 퇴근하고 |
| 3 | met | Verb | 만났습니다 |
| 4 | his friend | Object | 친구를 |

Sentence 276 — *He cleaned, did laundry, and met a friend on the weekend.* / 그는 주말에 청소하고, 빨래하고, 친구를 만났습니다.
| # | English | Role | Korean |
|---|---|---|---|
| 1 | He | Subject | 그는 |
| 2 | cleaned and | Verb | 청소하고 |
| 3 | did laundry and | Verb | 빨래하고 |
| 4 | met | Verb | 만났습니다 |
| 5 | a friend | Object | 친구를 |
| 6 | on the weekend | Adverbial | 주말에 |

(Note: "on the weekend" comes last in the rows because it comes last in the English sentence, even though Korean has 주말에 near the front.)

**Caveats:**
- The user previously also asked for some rows to be **combined** when an English chunk maps to a Korean Object + Verb compound (e.g., "wears a mask" → 마스크를 씁니다 in sentence 345). Combining vs splitting depends on how the textbook English phrases it. Default to split (one row per Korean fragment) unless the English text genuinely treats it as a single chunk.
- Always update header structure (`주어 + 부사어(시간) + 목적어 + 서술어(동사)` etc.) per [[combined-adverbial-role]] and [[lesson-grammar-summary-style]] regardless of row order.

Related: [[lesson-grammar-summary-style]], [[combined-adverbial-role]], [[korean-english-pairing]]

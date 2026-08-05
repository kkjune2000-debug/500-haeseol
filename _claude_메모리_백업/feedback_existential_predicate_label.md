---
name: feedback_existential_predicate_label
description: "있다/없다 existential predicates are labeled plain 서술어, never 서술어(형용사)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

In `exp-table` Role cells and 어순(Korean order) headers, existential 있다/없다 (and their conjugations: 있습니다/없습니다/있어요/없었습니다 etc.) must be labeled plain `Predicate / 서술어` — **never** `Predicate (Adjective) / 서술어(형용사)`.

**Why:** The 형용사/동사 classification of 있다/없다 is contentious in Korean grammar (있다 can be both; 없다 is descriptive). Tagging them `(형용사)` is misleading for learners, so the qualifier is dropped.

**How to apply:** Remove `(Adjective)`/`(형용사)` from BOTH the Role cell AND the matching 어순 header for any sentence whose predicate is 있다/없다. Do NOT touch real adjectives (반갑다·춥다·재미있다·많다 etc.) — those keep `서술어(형용사)`. Note 재미있다/맛있다 start with 재/맛, not 있 — they are genuine adjectives and stay. Distinct from [[feedback_predicate_modality_labels]] (which governs (Negation)/(Suggestion)/etc.) and [[feedback_korean_order_role_canon]] (canonical 서술어(동사)/서술어(형용사) format). Double-subject N이/가 없다/많다 may instead be [[feedback_clause_vs_adverbial]]-style 서술절 — but simple 주어+있다/없다 is plain 서술어. Applied 2026-06-02 to 325~331, 384~387, 401~407.

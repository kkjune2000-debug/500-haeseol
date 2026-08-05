---
name: combined-adverbial-role
description: "When a Korean sentence has multiple adverbial roles (time + place, purpose + place, etc.), combine them in a single parenthetical 부사어(X+Y) in the table header instead of listing each separately."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**When a sentence has multiple adverbial roles, group them under one 부사어(...) parenthetical in the explanation-table header.**

**Why:** The user established this on 2026-05-28 while polishing Lesson 2 (동안) and earlier confirmed the same pattern for Lesson 17 (~(으)러 가다). A row of "주어 + 부사어(시간) + 부사어(장소) + 동사" reads as cluttered; "주어 + 부사어(시간+장소) + 동사" is cleaner and treats the time and place as one adverbial block in the sentence.

**How to apply:**

In the `<th colspan="4">` header row of the explanation table, when the sentence contains two or more adverbial-type elements (time, place, purpose, manner, cause, etc.), combine them inside a single parenthetical:

- ✅ `주어 + 부사어(시간+장소) + 동사` / `Subject + Adverbial (Time + Place) + Verb`
- ✅ `주어 + 부사어(목적+장소) + 서술어` / `Subject + Adverbial (Purpose + Place) + Predicate`
- ✅ `주어 + 부사어(목적+시간) + 서술어` / `Subject + Adverbial (Purpose + Time) + Predicate`
- ❌ `주어 + 부사어(시간) + 장소 + 동사`
- ❌ `주어 + 부사어(시간) + 부사어(장소) + 동사`

Ordering rules:
- **Inside the parenthetical, list the roles in the order they appear in the Korean sentence.** If the sentence has `방학 동안 (시간) → 도서관에서 (장소)`, the header reads `부사어(시간+장소)`. If the sentence reverses to `도서관에서 → 방학 동안`, the header reads `부사어(장소+시간)`.
- Use `+` (no spaces) between roles in Korean (`시간+장소`); use ` + ` (with spaces) in English (`Time + Place`).

When NOT to combine:
- If a sentence has only one adverbial, use the simple `부사어(시간)` / `부사어(장소)` / `부사어(목적)` form, not a single-element parenthetical.
- Row Roles in the `<td class="exp-role">` cells stay as their specific label (`Adverbial (Time)`, `Adverbial (Place)`, etc.) — only the top header combines them.

Related: [[korean-english-pairing]]

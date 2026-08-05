---
name: feedback-no-vocab-in-explanation
description: "In per-sentence 4-column explanation tables (English | Role | Korean | Explanation), the Explanation column must NOT mention any word/expression that already appears in this lesson's Vocabulary box. Strip the vocab word entirely (not just its translation)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

per-sentence explanation table (`<table class="exp-table">`)의 **4번째 컬럼 (Explanation/해설)** 에서는 같은 lesson의 **Vocabulary 박스에 이미 등록된 단어**(한국어 어휘 + 그 영어 번역)를 **언급하지 않습니다**. 단어 자체를 통째로 제거하고 문법·규칙·기능 설명만 남깁니다.

**Why:** 사용자가 11과 (181~189) 183번 sentence에서 두 가지 중복 지적:
1. "Adverb **다시** — placed before the verb" — `다시`가 vocab에 있는데 또 언급
2. "**말씀하다** (honorific of **말하다**) + ..." — `말씀하다`가 vocab에 있는데 또 풀어쓰기

같은 lesson 안에서 학습자는 vocab 박스를 먼저 보므로, explanation 셀에서 그 단어를 다시 표시하는 것은 시각 노이즈일 뿐 학습 가치 X. 대신 셀은 **문법 포인트**(어순·활용·기능)에만 집중해야 함.

**삭제 대상:**
- vocab 박스에 등록된 한국어 단어 (예: `다시`, `말씀하다`, `잠깐만`)
- 그 단어의 영어 번역 (예: `(again)`)
- 단어를 풀어쓰는 metadata (예: `(honorific of 말하다)`)

**유지/대체:**
- 문법 역할 (예: `Adverb`, `Honorific form`)
- 어순 정보 (예: `placed before the verb`)
- 활용 규칙 (예: `하다 → 해`)
- 기능 설명 (예: `Polite request to the listener`)

**변환 예시:**
- ❌ `Adverb <strong>다시</strong> — placed before the verb`
  ✅ `Adverb — placed before the verb`
- ❌ `<strong>말씀하다</strong> (honorific of <strong>말하다</strong>) + <strong>해 주세요</strong> (<strong>하다</strong> → <strong>해</strong>). Polite request to the listener`
  ✅ `Honorific form of "say" + <strong>해 주세요</strong> (<strong>하다</strong> → <strong>해</strong>). Polite request to the listener`

**유지 대상 (지우지 말 것):**
- **활용표 (Conjugation table)** 에서 `<strong>돕다</strong> (help)` 처럼 동사를 영어 의미와 함께 표시 — 영어가 별도 열에 없을 때 필요.
- **gstep-pattern·explain-note·blockquote** 같은 교육 박스 안의 단어 + 번역 — 학습 컨텍스트.
- per-sentence 셀에서도 **활용 변환 사슬**(예: `돕다 → 돕 + 아 주세요 → 도오 + 아 주세요 → 도와 주세요 (ㅂ 불규칙)`) — 이건 단어 언급이 아니라 변화 과정 demonstration.
- vocab에 없는 단어 (예: 새로 등장한 어휘) — 언급 가능.

**How to apply:**
- per-sentence explanation table은 4열 구조 (English·Role·Korean·Explanation) 가 정형. 이 표에서만 적용.
- 각 explanation 셀을 검사:
  1. 같은 행의 3열 (Korean form) 단어가 셀 안에 다시 나오는지 → 제거
  2. lesson vocab 박스의 단어가 셀 안에 나오는지 → 제거 (vocab 박스 내용 비교 필요)
- 단어를 제거한 후 남는 문장이 자연스러운지 확인 — 어색하면 문법 역할 라벨로 대체 (Adverb, Honorific form 등)

Related: [[feedback-explanation-row-order]], [[feedback-table-cell-alignment]], [[feedback-irregular-step-arrows]] (활용 사슬은 demonstration이므로 단어 언급 규칙에서 제외)

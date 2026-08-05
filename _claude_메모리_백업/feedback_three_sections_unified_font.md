---
name: feedback-three-sections-unified-font
description: "The three practice sections (따라 읽기 / 카드를 보고 한국어로 말하기 / 문장 맞추기) must use identical font family and font size. Standard: Sentence Matching (em-text) — 1.06rem, font-weight 700, inherit font-family."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

세 가지 연습 섹션의 한국어 텍스트는 **동일한 폰트 family와 폰트 크기**를 사용합니다. 기준은 **Sentence Matching의 em-text**.

**Why:** 사용자가 시각적 일관성을 위해 세 섹션의 폰트를 통일하라고 지시(2026-05-31). 각 섹션이 폰트 크기·굵기가 달라 시각적으로 분리되는 느낌을 주는 것을 단일 기준으로 통일.

**기준 — em-text (Sentence Matching 카드 내부 텍스트):**
- `font-size: 1.06rem`
- `font-weight: 700`
- `line-height: 1.4`
- `font-family: inherit` (default, 'Noto Sans KR')

**적용 대상 CSS 클래스:**

1. **따라 읽기 (Read Along)** — `.sentence-list .sentence-item`
   - `.sentence-kr` (한국어 문장): `font-size: 1.06rem; font-weight: 700;`
   - `.sentence-en` (영어 문장): `font-size: 1.06rem; font-weight: 700;` (default font-family)

2. **카드를 보고 한국어로 말하기 (Look & Speak)** — `.flashcard-grid .flashcard`
   - `.flashcard-front .flashcard-text`: `font-size: 1.06rem; font-weight: 700;` (default font-family)
   - `.flashcard-back .flashcard-text`: `font-size: 1.06rem; font-weight: 700;`

3. **문장 맞추기 (Sentence Matching)** — `.em-game .em-item`
   - `.em-text` (기준): 그대로 유지 (`1.06rem`, `font-weight: 700`)

**How to apply:**
- 모든 lesson HTML 파일 67개에 CSS 통일 적용.
- Lato 영문 폰트 family override는 제거 — Noto Sans KR로 한·영 통합.
- 신규 lesson 작성 시 처음부터 이 사양 사용.

Related: [[feedback-em-item-center]] (em-item 가운데 정렬 + 폰트 1.06rem)

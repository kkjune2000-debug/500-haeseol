---
name: feedback-english-line-wrap
description: "For ALL Korean-word + English-translation pairs in table cells (especially conjugation tables), always place the English translation on a new line below the Korean word. Consistency rule: applies regardless of cell width — even short translations that wouldn't naturally wrap."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

표 셀 안의 **모든 한국어-단어 + 영어-번역 쌍** 은 **영어를 한국어 아래 줄에** 배치합니다. 일관성 원칙: 셀이 넓어 줄바꿈이 안 일어나는 경우에도 동일하게 적용.

**Why:** 처음에는 줄바꿈이 일어나는 경우만 분리하라는 규칙(2026-05-30)이었으나, 사용자가 일관성을 위해 **모든 단어** 에 적용을 지시(2026-05-31, 209~212 변화2 동사표). 같은 표 안에서 어떤 단어는 인라인이고 어떤 단어는 줄바꿈되면 시각적 통일성 깨짐. 처음부터 모두 같은 형식으로.

**표준 형식:**
```html
<td><strong>가다</strong><br><small>(go)</small></td>
```

NOT:
```html
<td><strong>가다</strong> (go)</td>
```

**적용 대상:**
- 활용표 (`gstep-table`) verb/adjective 열
- explain-note 표의 단어 행
- vocabulary 박스 (한국어 단어 + 영어 의미)
- 예문 셀 (한국어 문장 + 영어 번역)
- 모든 `<td>` 셀에서 `<strong>한글</strong> (English)` 패턴

**유지 (변환하지 말 것):**
- 본문 prose에서 자연스럽게 흐르는 인라인 영어 (예: "이 표현은 (formal) 격식체입니다.")
- 단순 grammar metadata `(formal)`, `(honorific)`, `(particle)` 등 — 단어 의미 번역이 아님
- gstep-pattern 박스 내부의 `<small>` 영어 라벨 — 이미 별개 영역
- 활용 step-arrow chain (예: `가다 → 가 + ㄹ까요? → 갈까요?`) — 의미 번역 아님

**자동 변환 정규식:**
```python
pattern = r'<strong>([가-힣]+(?:다|요|니다|니까|세요|어요|아요)?[가-힣]*)</strong> \(([a-zA-Z][a-zA-Z\s\-\']*?)\)'
replacement = r'<strong>\1</strong><br><small>(\2)</small>'
```

**How to apply:**
- 신규 lesson 작성 시 처음부터 `<br><small>(English)</small>` 형식.
- 기존 파일에서 발견 시 즉시 변환.
- 메모리에 적용 완료 (2026-05-31, 67개 파일 중 24개에서 90건 변환).

Related: [[feedback-korean-english-pairing]] (한국어 설명은 항상 영어 다음줄)

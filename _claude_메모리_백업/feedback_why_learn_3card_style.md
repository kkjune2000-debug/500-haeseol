---
name: ""
metadata: 
  node_type: memory
  originSessionId: 243aa644-b2dd-4ec3-97c9-53b3042d0fe5
---

레슨의 **"🎯 왜 배워야 하나? / Why learn this?"** 박스는 explain-note 텍스트 나열 대신 **아이콘 3카드 그리드 + 금색 마무리 띠**로 디자인한다.

구조: 가운데 정렬 제목줄("🎯 왜 배워야 하나? <small>Why learn this?</small>") → `display:grid;grid-template-columns:repeat(3,1fr);gap:12px` 3카드(각 카드: 흰 배경 #fff + #fde68a 테두리 + 큰 이모지 + 한/영 소제목 + 짧은 예시/설명 한·영) → `linear-gradient(135deg,#fde68a,#fcd34d)` 금색 마무리 띠(핵심 한 줄).

**Why:** 세 가지 쓰임/이유를 한눈에 스캔하게. 빽빽한 번호 텍스트보다 직관적.

**How to apply:** 간접화법(462~473)·관형어(474~488)에 적용(2026-06-06). 각 카드 한국어 예시의 핵심 어미·표현은 `.accent` 강조. 기타 문법은 앰버 색 유지. 영어줄은 비교 아닌 번역([[feedback_no_english_comparison]]). 불규칙 단원의 [[feedback_irregular_3step_flow_style]]와 함께 기타 문법 인트로 통일 디자인 언어를 이룸.

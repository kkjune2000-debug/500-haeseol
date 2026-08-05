---
name: feedback-em-item-center
description: "Sentence Matching cards (.em-item) must be center-aligned with slightly larger font (1.06rem), not left-aligned. Applies to every lesson file's matching game section."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

Sentence Matching 게임의 영어/한국어 카드(`.em-item` + 내부 `.em-text`)는 **가운데 정렬** + **약간 큰 폰트**가 표준입니다.

**Why:** 사용자가 좌측 정렬된 짧은 문장 카드들이 흩어져 보이고 작아서 시인성이 떨어진다고 판단해 수정을 요청. 카드는 폭이 일정하고 문장 길이가 짧아 가운데 정렬이 시각적으로 더 깔끔합니다.

**CSS 사양:**
- `.em-item`:
  - `padding: 12px 14px` (좌우 14, 상하 12)
  - `display: flex`
  - `align-items: center`
  - **`justify-content: center`** ← flex 중앙 정렬
  - **`text-align: center`** ← 텍스트 중앙 정렬
- `.em-text`:
  - **`font-size: 1.06rem`** (이전 0.93rem에서 ~14% 키움)
  - `text-align: center` (장문 줄바꿈 시에도 중앙 유지)
  - 나머지(`font-weight:700`, `line-height:1.4`, `color:#334155`, `word-break:keep-all`) 동일

**How to apply:**
- 모든 lesson HTML 파일(`D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\*.html`) — 67개 전부에 적용 완료(2026-05-30).
- 새로 작성되는 lesson 파일도 같은 규칙으로 시작할 것.
- 카드 안의 `<span class="em-num">` 번호 뱃지는 일부 변형에서 비활성(rendering 코드가 em-text만 출력) — 가운데 정렬과 충돌하지 않음.

Related: [[feedback-table-cell-alignment]], [[feedback-english-line-wrap]]

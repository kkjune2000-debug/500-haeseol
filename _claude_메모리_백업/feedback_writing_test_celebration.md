---
name: feedback-writing-test-celebration
description: "WRITING TEST single-wt blocks must remove the 정답/듣기 buttons header AND show a 5-second celebration (yellow badge, sparkles, bold pastel text) when the user types the correct answer."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

모든 lesson HTML의 **WRITING TEST** 영역(`.single-wt`)은 아래 두 가지 규칙을 따라야 합니다.

**Why:** 사용자는 (1) 상단의 💡 정답 / 🔊 듣기 버튼이 시각적 산만함을 만들고 사용자가 답을 쓰기 전에 정답을 보게 유도한다고 판단해 제거를 요청했고, (2) 정답을 맞춘 순간 단순한 색 변화 이상의 "축하받는 느낌"을 원했습니다. 최종적으로 5초 동안 머무는 축하 효과로 합의되었습니다. Show Answer 박스(`.answer-box .answer-toggle`)는 별개로 유지합니다.

**규칙 1 — single-wt-header 제거:**
- `<div class="single-wt"> ... </div>` 안의 `<div class="single-wt-header">` 블록 전체를 삭제.
- 헤더 안의 `<span class="single-wt-label">✍️ Writing Test</span>`, `<button class="single-wt-speak">🔊</button>`, `<button class="single-wt-reveal">💡 정답</button>` 모두 제거.
- 남는 것은 `<textarea class="writing-input" data-ans="..." oninput="wtCheck(this)">`만.

**규칙 2 — 정답 입력 시 5초 축하:**
- CSS:
  - `.writing-input.correct` → 노란 파스텔 배경(`#fefce8`) + 노란 테두리(`#fde047`) + 갈색 글씨(`#854d0e`) + **font-weight:800** (굵게).
  - `.writing-input.wrong` → 빨간 파스텔 배경(`#fef2f2`) + 연한 빨간 테두리(`#fecaca`) + 진한 빨강 글씨(`#991b1b`).
  - `.writing-input.celebrating` — 정답 순간 0.55s `cubic-bezier(0.34, 1.56, 0.64, 1)` 뽀잉 애니메이션 + 노란 글로우 그림자.
  - `.wt-celebrate-badge` — 5s `wtBadgePop` 애니메이션. 노란 그라데이션 배지("🎉 정답!<small>Correct!</small>"). 92%까지 머문 뒤 짧게 페이드아웃.
  - `.wt-sparkle` — 4.5s `wtSparkleFly` 애니메이션. 6개 스파클(`✨⭐🌟💫`)이 회전하며 위로 떠오름.
- JS:
  - `wtCheck`: 정답 전환 시 `wtCelebrate(inp)` 호출. `inp.dataset.celebrated = '1'`로 중복 트리거 방지. 입력이 비거나 오답이면 `celebrated` 초기화.
  - `wtCelebrate`: `closest('.single-wt')` 부모를 찾아 `position:relative` 보장 → 배지·스파클 6개를 DOM에 추가 → 5050ms/4700ms 뒤 제거.

**How to apply:**
- 모든 lesson HTML 파일(`D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\*.html`)에 일괄 적용.
- 캐노니컬 구현은 [142~149 서술어 문법 희망.html] 참고 — CSS 116~155행대, JS 1000행대.
- Show Answer 박스(`.answer-box`, `.answer-toggle`)는 절대 건드리지 말 것. 정답 박스는 학습자가 명시적으로 클릭해야 보임.
- 데이터 무결성: `data-ans` 속성과 `oninput="wtCheck(this)"`는 변경하지 말 것.

Related: [[feedback-english-line-wrap]], [[feedback-batchim-table-labels]]

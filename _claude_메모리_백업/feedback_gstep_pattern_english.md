---
name: feedback-gstep-pattern-english
description: Every gstep-pattern box must include an English translation in <small> after the Korean pattern. Korean-only is never acceptable.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

`<div class="gstep-pattern">` 박스 안에는 한국어 패턴 다음에 반드시 영어 해석이 `<small>` 태그로 들어가야 합니다 — 한국어만 있는 박스는 허용되지 않습니다.

**Why:** 학습자는 영어 화자(또는 한국어 학습자)이고 패턴 박스는 문법 요점을 한눈에 보여주는 시각 요소라, 영어 해석이 빠지면 박스를 봐도 의미를 즉시 알 수 없습니다. 본문 설명에 영어가 있더라도 패턴 박스 자체가 자족적이어야 합니다.

**How to apply:**
- 형식: `<div class="gstep-pattern">한국어 패턴<small>English translation</small></div>`
- 한국어와 영어를 1:1 대응시켜 번역 — 토큰 순서·강조·악센트가 일치해야 함.
- `<span class="accent">` 으로 강조된 어미는 영어 번역에서도 `<strong>`로 강조.
- 받침 조건이 있으면 영어에서도 명시: 예) "Verb stem (no 받침) + 려고 / (with 받침) + 으려고".
- `<small>` 안에 `<small>`를 또 두지 말 것 — 한 레벨의 small이 표준.
- 기존 박스를 확인해 영어가 빠진 곳은 모두 보강.

Related: [[feedback-korean-english-pairing]], [[feedback-english-line-wrap]]

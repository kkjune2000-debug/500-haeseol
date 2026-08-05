---
name: feedback-grammar-overview-subtitle
description: "Delete the redundant <p class=\"subtitle\"> line that follows <h2>Grammar Overview · 문법 정리</h2>. The lesson title already conveys the topic."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

`<h2>Grammar Overview · 문법 정리</h2>` 직후에 오는 `<p class="subtitle">'~XYZ' — 한국어 설명</p>` 부제목 줄은 **삭제**합니다.

**Why:** 사용자가 같은 패턴(157~163 계획, 164~168 결정 등)에서 반복적으로 삭제 요청. lesson 제목·헤더에서 이미 주제를 명시하고, gstep 1번 박스 안에 동일한 의미가 다시 등장해 중복. Grammar Overview 섹션은 h2만으로 충분합니다.

**삭제 대상 패턴 (정확):**
```
<h2>Grammar Overview · 문법 정리</h2>
<p class="subtitle">'~기로 했다' — 이미 내려진 결정·결심·약속을 표현</p>
```
→
```
<h2>Grammar Overview · 문법 정리</h2>
```

**How to apply:**
- regex: `<h2>Grammar Overview · 문법 정리</h2>\s*\n\s*<p class="subtitle">[^<]+</p>` → `<h2>Grammar Overview · 문법 정리</h2>`
- 모든 lesson HTML 파일에 일괄 적용. h2 자체와 그 뒤의 gstep 박스(`<div class="gstep">`)는 유지.
- 다른 섹션(`Practice`, `Read Along` 등) 뒤의 subtitle은 건드리지 않음 — 그건 의미 있는 부제(예: "연습: 한국어 문장을 만들어 보세요!").

Related: [[feedback-lesson-grammar-summary-style]]

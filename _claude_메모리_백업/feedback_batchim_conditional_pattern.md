---
name: feedback-batchim-conditional-pattern
description: "When gstep-pattern boxes show endings that change based on 받침 presence/absence, always use the standard colored format: '<strong style=color:#dc2626>No 받침</strong>: Verb + ending  |  <strong style=color:#16a34a>With 받침</strong>: Verb + ending'."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

문법 정리(gstep-pattern 박스) 안에서 **받침 유무에 따라 어미가 달라지는 경우** 다음 표준 형식을 사용합니다.

**Why:** 사용자가 115~122 청유 lesson의 `No 받침 / With 받침` 컬러 형식을 표준으로 지정. 빨간색·초록색 컬러 코딩이 받침 조건을 시각적으로 즉시 구분 가능하게 함. 기존의 `받침 X / 받침 O` 표기는 의미가 직관적이지 않음.

**표준 형식:**
```html
<div class="gstep-pattern">
  <strong style="color:#dc2626;">No 받침</strong>: Verb + <span class="accent">[ending without 으]</span>
  &nbsp;|&nbsp;
  <strong style="color:#16a34a;">With 받침</strong>: Verb + <span class="accent">[ending with 으]</span>
</div>
```

**색상 코드:**
- `No 받침` → `color:#dc2626` (빨강) — 받침 없음
- `With 받침` → `color:#16a34a` (초록) — 받침 있음

**예시 (115~122 청유):**
```html
<div class="gstep-pattern"><strong style="color:#dc2626;">No 받침</strong>: Verb + <span class="accent">ㅂ시다</span> &nbsp;|&nbsp; <strong style="color:#16a34a;">With 받침</strong>: Verb + <span class="accent">읍시다</span></div>
```

**다른 적용 사례 (변환 후):**
- ~(으)면 안 됩니다: `No 받침: Verb + 면 안 됩니다 | With 받침: Verb + 으면 안 됩니다`
- ~(으)ㄴ 적이 있다: `No 받침: Verb + ㄴ 적이 있다 | With 받침: Verb + 은 적이 있다`
- ~(으)ㄹ까요?: `No 받침: Verb + ㄹ까요? | With 받침: Verb + 을까요?`
- ~(으)니까: `No 받침: Verb + 니까 | With 받침: Verb + 으니까`
- ~(으)려고: `No 받침: Verb + 려고 | With 받침: Verb + 으려고`
- ~(으)러: `No 받침: Verb + 러 | With 받침: Verb + 으러`
- ~(으)세요: `No 받침: Verb + 세요 | With 받침: Verb + 으세요`
- ~(으)ㄴ 덕분에: `No 받침: Verb + ㄴ 덕분에 | With 받침: Verb + 은 덕분에`

**유지 (변환하지 말 것):**
- `받침` 규칙이 없는 패턴 (예: `~기 때문에 — always 기, no 받침 rule`) — 그대로 유지
- 활용표 (`gstep-table`)의 받침 셀 — 별도 규칙 ([feedback-batchim-table-labels]) 적용: O/X 컬러 심볼 + 없음/있음 라벨

**How to apply:**
- 신규 gstep-pattern 작성 시 처음부터 이 형식.
- 기존 비표준 박스 발견 시 변환:
  - `<strong>받침</strong> X: ...` → `<strong style="color:#dc2626;">No 받침</strong>: ...`
  - `<strong>받침</strong> O: ...` → `<strong style="color:#16a34a;">With 받침</strong>: ...`

Related: [[feedback-batchim-table-labels]] (gstep-table 받침 셀의 O/X 컬러 심볼 규칙)

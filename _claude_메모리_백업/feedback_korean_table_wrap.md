---
name: feedback_korean_table_wrap
description: 표 칸의 한국어가 글자 중간에서 잘리지 않게 — word-break:keep-all + nowrap 유닛으로 묶음 전체가 다음 줄로
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

표/카드 칸에서 한국어가 좁은 칸 때문에 **글자 중간에서 끊기는 것**(그러→나, 좋습→니다)을 막을 것.

**Why:** 한글은 기본적으로 CJK처럼 글자 단위로 줄바꿈돼 어절/단어가 절단됨. 사용자 요구: "내용이 잘리는 경우 전체가 아래줄로 이동".

**How to apply:** 셀에 `word-break:keep-all; overflow-wrap:normal;` → 어절은 공백에서만 끊김. 여러 어절이 한 묶음이어야 하면(예 "책과 펜", "사과와 바나나", "받침 없음 → 와") 그 묶음을 `white-space:nowrap` span(예 `.cx-nb`)으로 감싸 묶음 전체가 통째로 다음 줄로 내려가게. "·" 같은 구분점에서만 줄바꿈 허용. Applied 79~86 .cx 표. [[feedback_english_line_wrap]]

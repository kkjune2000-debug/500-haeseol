---
name: topik2-theme-vocab
description: "토픽2 어휘 2축 확정 — 한자 뿌리 + 주제별 어휘(24주제 통합), 꼬리 페이지 삭제"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6ef7c53f-3fb0-4912-a320-2be45f2ec0ff
  modified: 2026-08-16T10:19:26.687Z
---

★어휘 정리 2축 확정(2026-08-16, 사용자 결정): ①형태축=한자 뿌리 모음 ②의미축=「토픽2 주제별 어휘」. **꼬리에 꼬리를 무는 어휘는 삭제**(페이지+빌더 18 tail-vocab 블록+재빌드, t2r_tail_*는 사장 — 다시 주입 금지)★

주제별 어휘 = 통합 2층: 큰 주제 24 아래 ①🔬 세밀 갈래 카드 25장(기존 t2r_theme_vocab.json, 미생물 예시 그대로, 앵커 tv_*) + ②기출 어휘장 210묶음(코퍼스 3,583→배정 2,196+보충 108, 출처 칩 2,806 전수 유효). 파이프라인 `t2_theme_extract→chunk→[분류8]→merge→curprep→[큐레이션9]→curaudit→build`, 데이터 `_theme/`.

**Why:** 음절 연결(꼬리)은 의미 없는 암기라 사용자가 폐기, 의미 묶음(어휘장)으로 대체.

**How to apply:** 어휘 상자 수정 시 t2_theme_extract부터 재실행; cur_*.json만 고치면 curaudit→t2_theme_build. 옛 t2r_themevocab_build.py는 쓰지 말 것. 듣기 데이터는 `const SETS`(세트.items[].vocab), 읽기는 `const ITEMS`. 앵커는 읽기·듣기 모두 `q_<회>_<번>`. 관련: [[topik2-hanja-roots]], [[haeseol-content-enrich]]

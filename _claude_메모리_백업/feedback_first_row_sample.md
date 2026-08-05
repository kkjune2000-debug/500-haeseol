---
name: feedback_first_row_sample
description: "? 가리기 표의 첫 행(가로표는 첫 열)을 정답 공개 예시로 두는 패턴"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 129b6492-07a9-4b0a-8da5-4d32cd8aba41
---

"?" 가리기 자가점검 표에서 **첫 행(세로표) 또는 첫 열(가로표)은 정답이 보이는 예시 행**으로 둔다.

**Why:** 학습자가 표의 형식을 먼저 이해한 뒤(모델 → 자가점검) 나머지를 "?"로 풀 수 있어 효과적. 사용자가 "한눈에 보기에서 가다는 정답 공개가 좋겠다, 샘플로"라고 요청(2026-06-22).

**How to apply:** 예시 셀은 `.q-cell`을 **부착하지 않고**(항상 보임) 강조 클래스(`.q-sample`/`.mat-sample` — 배경 #fffbeb·노란 테두리 `inset 0 0 0 2px #f59e0b`·"예시" 라벨)만 준다. 판별: 세로표(thead 있음)=첫 tbody 행, 가로표(숫자 s1·s2 등 thead 없음)=각 행의 첫 `.rd` 셀(숫자 1·101). `qAll(모두 보기/다시 가리기)`는 `.q-cell`만 토글하므로 예시 셀은 영향 없음. 안내문구에 "첫 줄/노란 칸은 예시" 명시. 부록 1 숫자·2 부정법·3 격식체구어체문어체(매트릭스+문체별 3구획)·4 기초문법연습에 적용. "?" 엔진은 [[project_appendix_series]] 참조.

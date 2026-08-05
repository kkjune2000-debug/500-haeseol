---
name: feedback_conjugation_table_style
description: "활용/만드는 법 표 통일 스타일 — 보라 헤더 카드 + 원형 양성/음성/하다 모음 배지, 받침 No/With, 패턴박스 옅은 노랑. 169~180·181~189 적용, 모음조화·받침 문법에 재사용"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

서술어 문법의 "만드는 법/활용" 표에 쓰는 통일 디자인. **모음조화(아/어)** 또는 **받침(으)** 변화를 다루는 문법에 재사용.

**표 카드**: `border-collapse:separate; background:#fff; border:1px solid #ddd6fe; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(76,29,149,0.12)`. 헤더 행 `background:linear-gradient(135deg,#ede9fe,#ddd6fe); color:#5b21b6; font-weight:800`, 헤더 셀 `border-bottom:2px solid #c4b5fd`. 셀 구분선 `1px #f1edfd`, 문법 그룹 구분 `2px #e9d5ff`.

**열 구성**: (여러 문법 비교 시) 문법 × **조건** × 형태 × 예. 단일 문법은 끝 모음 × 형태 × 예. 형태·예 한국어 밑에 회색(`#9ca3af`) `<em>` 영어 병기.

**조건 배지(원형, 첨부 ~아/어 보다 표 스타일)**:
- 양성: 원 `radial-gradient(circle at 50% 38%, #fef9c3, #fcd34d); color:#b45309`, 자모 **ㅏ**, 라벨 "양성 bright".
- 음성: 원 `radial-gradient(#eff6ff, #93c5fd); color:#2563eb`, 자모 **ㅓ**, "음성 dark".
- 하다: 원 `radial-gradient(#f5f3ff, #c4b5fd); color:#6d28d9`, "하다", "불규칙 special".
- 받침형 문법은 조건칸에 **No 받침**(red #dc2626) / **With 받침**(green #16a34a) — [[feedback_batchim_conditional_pattern]].

**형용사**: 허락·의무·금지(조건형) 등은 "동사/형용사"로 표기, 명령형(~지 마세요)만 동사 전용.

**카드 톤 통일**(같은 문법 정리 안): 설명 박스도 `background:linear-gradient(135deg,#ede9fe,#faf5ff); border:1px solid #ddd6fe; border-left:4px solid #6d28d9; shadow`. **패턴 박스(.gstep-pattern)** 배경은 **아주 옅은 노랑 #fffdf0** + 보라 좌측 띠(#6d28d9) — 흰 표카드/보라 설명박스와 위계.

적용: 169~180(허락·금지·의무·면제), 181~189(부탁 ~아/어 주세요/주시겠습니까). 재사용 후보: ~아/어요·~았/었어요·~아/어서·현재 등 모음조화, ~(으)면·~(으)ㄹ 수 있다·~(으)세요·~(으)려고 등 받침. [[feedback_gstep_card_table_style]] [[feedback_jamo_change_color]]

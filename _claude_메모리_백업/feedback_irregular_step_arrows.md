---
name: feedback-irregular-step-arrows
description: "For ㅂ/ㄷ/ㄹ/ㅅ/ㅡ/르 불규칙 verb derivations in per-sentence explanation cells, use the standard step-arrow format - dictionary → stem+ending → transformed stem+ending → final form (label)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

per-sentence explanation table의 4번째 셀에서 불규칙 활용을 보일 때, **단계별 → 화살표 형식**을 표준으로 사용합니다.

**Why:** 사용자가 181 (돕다 → 도와 주세요) 셀에서 기존 산문 형식("돕다 stem 돕 + 아 → ㅂ 불규칙: 도+오+아 = 도와 + 주세요")을 단계별 화살표 형식("돕다 → 돕 + 아 주세요 → 도오 + 아 주세요 → 도와 주세요")으로 바꿔달라고 요청. 단계별 시각 흐름이 학습자가 형태 변화 과정을 따라가기 쉽게 합니다.

**표준 형식 (ㅂ 불규칙 예시):**
```
<strong>돕다</strong> → <strong>돕 + 아 주세요</strong> → <strong>도오 + 아 주세요</strong> → <strong>도와 주세요</strong> (<strong>ㅂ 불규칙</strong>)
```

**단계 순서:**
1. **사전형** (예: `돕다`) — 출발점
2. **어간 + 어미 (원형)** (예: `돕 + 아 주세요`) — 어간 분리, 어미 부착 전
3. **변환된 어간 + 어미** (예: `도오 + 아 주세요`) — ㅂ→오/우, ㄷ→ㄹ 등 변화 적용
4. **최종 축약형** (예: `도와 주세요`) — 모음 축약 완료
5. **(불규칙 라벨)** — 끝에 `(ㅂ 불규칙)` 등 명시

**다른 불규칙 적용:**
- **ㅂ 불규칙**: 덥다 → 덥 + 어지다 → 더우 + 어지다 → 더워지다 → 더워졌습니다 (ㅂ 불규칙)
- **ㄷ 불규칙**: 듣다 → 듣 + 었습니다 → 들 + 었습니다 → 들었습니다 (ㄷ 불규칙)
- **르 불규칙**: 자르다 → 자르 + 었다 → 잘르 + 었다 → 잘랐다 (르 불규칙)
- **ㅅ 불규칙**: 짓다 → 짓 + 었다 → 지 + 었다 → 지었다 (ㅅ 불규칙)
- **ㅡ 불규칙**: 바쁘다 → 바쁘 + 았다 → 바ㅃ + 았다 → 바빴다 (ㅡ 불규칙)
- **ㄹ 불규칙**: 살다 → 살 + ㅂ니다 → 사 + ㅂ니다 → 삽니다 (ㄹ 불규칙)

**유지 (지우거나 변환 X):**
- 활용표 (gstep-table conjugation table)에서 이미 컬럼 분리된 활용 — 다른 시각 형식 사용 중.
- 메인 불규칙 lesson (436~440 ㄹ, 441~444 ㅡ, 445~448 르, 449~453 ㅂ, 454~459 ㄷ, 460~461 ㅅ)의 본문 설명 — 거기는 자체 활용표 형식 유지.
- per-sentence explanation 셀에서만 적용.

**How to apply:**
- per-sentence explanation 4번째 셀 (`<td>` after `exp-form`)에서 불규칙 동사 활용을 보일 때 위 형식 사용.
- 산문형 "stem X + Y → 변화: A+B+C = D" 또는 압축형 "X → Y → Z" 발견 시 단계별 형식으로 확장.

Related: [[feedback-irregular-phonetic-framing]] (ㄷ/ㅂ 불규칙은 항상 "딱딱한 자음이 부드러운 모음을 만나..." framing으로 설명)

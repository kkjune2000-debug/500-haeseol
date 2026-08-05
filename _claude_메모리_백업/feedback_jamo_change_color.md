---
name: feedback_jamo_change_color
description: "불규칙에서 바뀌는 핵심 자모(ㅂ→오/우, ㄷ→ㄹ 등)를 짙은 파란색으로 강조"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

In 불규칙 pattern boxes, color the **key changing jamo dark blue** so the change is intuitive at a glance. ㅂ불규칙: ㅂ·오·우; ㄷ불규칙: ㄷ·ㄹ; etc.

**Color:** use `#1e40af` (deep blue) on the amber pattern-box background. Note `#1e3a8a` is **too close to the default dark slate/brown** and reads as no-change — if the surrounding text is dark, use `#2563eb` (vivid blue) instead (user feedback: "색깔이 변하지 않았다"). Bold non-bold spans help visibility.

**Scope:** color ONLY the rule/pattern line, not the derivation example chains below. When a result shows both the original and changed jamo (e.g., 오 + 오, where stem-vowel 오 + softened-ㅂ 오), color **only the changed one** (the softened ㅂ), leaving the stem's original jamo its normal color (user: "첫 번째 오와 마지막 오는 원래색 그대로").

Applied 2026-06-03: 449~453 ㅂ(ㅂ·오·우), 454~459 ㄷ(ㄷ·ㄹ), 445~448 르(부르다 렀 #2563eb). Relates to [[feedback_irregular_derivation_chain]].

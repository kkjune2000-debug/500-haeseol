---
name: feedback-predicate-modality-labels
description: "Conditional modality suffixes on Predicate labels — (Negation)/(부정) only on actual negative sentences (안/못/~지 않다/~지 못하다); (Suggestion)/(청유) on ~ㄹ까요?/~ㅂ시다 sentences. Positive declarative sentences get plain 'Predicate / 서술어'."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

per-sentence h3 헤더와 Role 셀의 Predicate 라벨에 **modality 접미사**를 붙일 때 적용하는 조건부 규칙.

**Why:** 사용자 피드백에서 두 번 등장: (1) "부정어가 없는 문장에서는 '서술어'만 써라." — 부정 라벨이 긍정문에 잘못 붙어서 학습자가 혼란. (2) "서술어(청유)" — ~ㄹ까요?/~ㅂ시다 문장은 단순 서술어가 아닌 청유 modality를 가지므로 별도 라벨이 필요.

이전에 자동 변환 스크립트가 부정 lesson 모든 헤더에 `(Negation)` 일괄 적용해서 긍정/부정 문장이 섞인 단원에서 라벨 오정렬이 발생함. 헤더는 해당 문장의 실제 형태에 맞춰 작성해야 함.

**How to apply:**

**1. 부정 (Negation):**
- 부정 표지(`안`, `못`, `~지 않다`, `~지 못하다`, `~지 맙시다`)가 있는 문장에만:
  ```html
  <td class="exp-role">Predicate (Negation)<br><small>서술어(부정)</small></td>
  ```
  그리고 h3 헤더도:
  ```html
  <h3>... + Predicate (Negation) / ... + 서술어(부정)</h3>
  ```
- 부정 표지가 없는 긍정 declarative 문장:
  ```html
  <td class="exp-role">Predicate<br><small>서술어</small></td>
  <h3>... + Predicate / ... + 서술어</h3>
  ```
- 서술절 전체가 부정될 때는 `서술절(부정)`:
  ```html
  <h3>Subject + Predicate clause (Negation) / 주어 + 서술절(부정)</h3>
  ```

**2. 청유 (Suggestion):**
- 청유형 어미(`~ㄹ까요?`/`~을까요?` 권유, `~ㅂ시다`/`~읍시다`, `~지 맙시다`)가 있는 문장:
  ```html
  <td class="exp-role">Predicate (Suggestion)<br><small>서술어(청유)</small></td>
  <h3>... + Predicate (Suggestion) / ... + 서술어(청유)</h3>
  ```

**3. 기타 modality (확장 패턴):**
- 희망: `Predicate (Hope) / 서술어(희망)` — ~고 싶다 lessons
- 능력: `Predicate (Ability) / 서술어(능력)` — ~ㄹ 수 있다 lessons
- 결정: `Predicate (Decision) / 서술어(결정)` — ~기로 하다 lessons
- 허락: `Predicate (Permission) / 서술어(허락)` — ~아/어도 되다 lessons
- 변화: `Predicate (Change) / 서술어(변화)` — ~아/어지다 등
- 추측: `Predicate (Guess) / 서술어(추측)` — ~ㄹ 것 같다 등
- 감탄: `Predicate (Exclamation) / 서술어(감탄)`
- 확인: `Predicate (Confirmation) / 서술어(확인)`
- 정중표현: `Predicate (Polite) / 서술어(정중)` — ~아/어 주세요 등
- 타인 위한 행동: `Predicate (For Others) / 서술어(타인을 위한 행동)`

**판단 기준 (요약):**
- 라벨은 그 문장이 실제로 표현하는 modality에만. 단원이 다루는 문법 ≠ 문장의 modality.
- 한 단원에 긍정/부정/청유/평서가 섞여 있으면 각 헤더와 Role 셀을 개별 검사.
- 자동 변환 스크립트는 반드시 문장 내용을 키워드(`don't`/`can't`/`shall we`/`let's`)로 판별 후 적용.

Related: [[feedback-korean-order-role-canon]] (일반 Role 표기 규칙), [[feedback-combined-adverbial-role]] (부사어 결합)

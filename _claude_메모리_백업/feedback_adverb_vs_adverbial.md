---
name: feedback-adverb-vs-adverbial
description: "In per-sentence explanation tables, label pure word-class adverbs (다시·잠깐만·빨리·정말·항상 etc.) as 'Adverb / 부사', NOT 'Adverbial / 부사어'. 부사어 is reserved for noun+particle constructions that play an adverbial role (어제·집에서·도서관에 등)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

per-sentence 4-col explanation 표(`exp-table`)의 Role 컬럼에서 **순수 부사(word-class adverb)** 와 **부사어(adverbial sentence component)** 를 구분합니다.

**Why:** 사용자가 "다시 / Adverbial / 부사어" 라벨을 보고 "부사어가 아니라 부사" 라고 지적함. 한국어 문법상:
- **부사 (Adverb)** = 품사(word class) — 다시, 빨리, 정말, 항상, 잠깐만 같이 그 자체로 부사인 단어
- **부사어 (Adverbial)** = 문장 성분 — 어제(시간 명사), 집에서(명사+에서), 도서관에(명사+에) 처럼 명사+조사가 모여 부사적 역할을 하는 구

순수 부사를 "부사어"로 묶으면 학습자가 품사와 문장 성분을 혼동함.

**How to apply:**

순수 부사(품사가 부사인 단어)는 Role을 **`Adverb / 부사`**:
```html
<td class="exp-role">Adverb<br><small>부사</small></td>
```

명사+조사 부사어, 시간 명사, 장소 명사 등 부사적으로 쓰이는 구는 **`Adverbial / 부사어`** 유지 (필요 시 세분화):
```html
<td class="exp-role">Adverbial<br><small>부사어</small></td>
<td class="exp-role">Adverbial (Time)<br><small>부사어(시간)</small></td>
<td class="exp-role">Adverbial (Place)<br><small>부사어(장소)</small></td>
```

**확정된 순수 부사 목록 (Adverb / 부사):**
다시, 잠깐만, 빨리, 어서, 정말, 참, 너무, 많이, 늘, 항상, 가끔, 자주, 일찍, 멀리, 안녕히, 깨끗이, 편히, 맛있게, 예쁘게, 싸게, 친절하게

**부사어로 유지되는 예 (Adverbial / 부사어):**
- 시간 명사: 어제, 오늘, 내일, 지금, 아침에, 저녁에
- 장소 명사+조사: 집에서, 학교에, 도서관에서
- 수사+의존명사: 한 번 (one time — Role 자체는 부사어; 부사 아님)

**판단 기준:**
- 단독으로 부사로 사전에 등재되어 있으면 → 부사
- 명사 어근에 조사가 붙거나, 어간+게/이/히 등으로 형성된 파생부사라도 그 결과가 사전상 부사면 → 부사 (예: 빨리, 깨끗이, 안녕히, 맛있게, 예쁘게)
- 명사 그대로 또는 명사+에/에서/로 형식이면 → 부사어

**의문사 예외 — 왜:** 의문부사 **왜(why)**는 품사상 부사지만, Role은 **`Adverbial (Reason) / 부사어(이유)`**로 단다(이유를 묻는 부사어로 취급). 원인 레슨이든 목적 레슨이든 왜는 항상 `부사어(이유)`로 통일(2026-05-31 316~324·338~345 적용). 다른 의문부사(어떻게 등)도 의미에 맞는 부사어 세부 라벨 사용.

Related: [[feedback-korean-order-role-canon]] (Role 라벨 일반 규칙), [[feedback-combined-adverbial-role]] (부사어(시간+장소) 결합 규칙)

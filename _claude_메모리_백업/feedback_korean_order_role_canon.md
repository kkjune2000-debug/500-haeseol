---
name: feedback-korean-order-role-canon
description: "Universal rule for all per-sentence explanation tables — Korean-order header tokens and Role labels must use canonical forms: 장소→부사어(장소), 시간→부사어(시간), 동사→서술어(동사). Combined adverbials: 시간+장소→부사어(시간+장소)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

per-sentence explanation table의 **Korean order 헤더** 와 **Role 셀 라벨**은 다음 표준 형식을 사용합니다.

**Why:** 사용자가 모든 lesson의 explanation 표 헤더를 일관된 양국어 + 정규화된 역할 라벨로 통일하길 원함. 일부 lesson은 이미 적용되었지만(서술어 6~8, 10과 등) 나머지 14개 lesson에 표준 미적용. 일관성 위해 전체 적용.

**헤더 정규화 (Korean order line):**

English 측:
| Before | After |
|---|---|
| `Place` | `Adverbial(Place)` |
| `Place (direction)` | `Adverbial(Place)` |
| `Place (action)` | `Adverbial(Place)` |
| `Time` | `Adverbial(Time)` |
| `Time + Place` | `Adverbial(Time + Place)` |
| `Place + Time` | `Adverbial(Time + Place)` |
| `Verb` | `Predicate(Verb)` |

Korean 측:
| Before | After |
|---|---|
| `장소` | `부사어(장소)` |
| `장소 (방향)` | `부사어(장소)` |
| `장소 (action)` | `부사어(장소)` |
| `시간` | `부사어(시간)` |
| `시간 + 장소` | `부사어(시간 + 장소)` |
| `장소 + 시간` | `부사어(시간 + 장소)` |
| `동사` | `서술어(동사)` |

**Role 셀 라벨 (`<td class="exp-role">`):**

| Before | After |
|---|---|
| `Subject` | `Subject<br><small>주어</small>` |
| `Object` | `Object<br><small>목적어</small>` |
| `Direct Object` | `Direct Object<br><small>직접목적어</small>` |
| `Indirect Object` | `Indirect Object<br><small>간접목적어</small>` |
| `Place` | `Adverbial (Place)<br><small>부사어 (장소)</small>` |
| `Place (direction)` | `Adverbial (Place)<br><small>부사어 (장소)</small>` |
| `Place (action)` | `Adverbial (Place)<br><small>부사어 (장소)</small>` |
| `Time` | `Adverbial (Time)<br><small>부사어 (시간)</small>` |
| `Verb` | `Predicate (Verb)<br><small>서술어 (동사)</small>` |
| `Adverb` | `Adverbial<br><small>부사어</small>` |
| `Means` | `Adverbial (Means)<br><small>부사어 (수단)</small>` |
| `Negation` | `Negation<br><small>부정</small>` |
| `Affirmation` | `Affirmation<br><small>긍정</small>` |

**유지/예외:**
- **이미 lesson-specific Predicate(Topic) 적용된 lesson** (서술어 6~10, 13~15, 등): `Predicate(Wish)`, `Predicate(Hope)`, `Predicate(Plan)` 등 — 변환 X, 그대로 유지.
- 활용표 (`gstep-table`)에서의 일반 셀 — 이 규칙은 explanation 표(`exp-table`)에만 적용.
- 본문 prose에 등장하는 한국어 단어 — 규칙 적용 안 함.

**적용 우선순위 (스크립트 작성 시):**
1. 결합형 먼저: `Time + Place`/`시간 + 장소`/`Place + Time`/`장소 + 시간` → 결합 부사어
2. 한정형: `Place (direction)`/`Place (action)`/`장소 (방향)` → 부사어(장소)
3. 단독: `Place`/`Time`/`장소`/`시간` → 부사어(...)
4. 마지막: `Verb`/`동사` → Predicate(Verb)/서술어(동사)

**적용 완료 파일 (2026-05-31):**
- 21~30 문장구조 (10건), 41~50 문장구조 (10건), 31~40 문장구조 (9건), 71~78 문장구조 (8건)
- 277~283 부사어 (7건), 248~252 (5건), 271~276 (5건), 79~86 문장구조 (5건)
- 292~295 (4건), 51~60 (4건), 316~324 (2건), 61~70 (2건)
- 266~270 (1건), 300~306 (1건)
- 총 14개 파일

Related: [[feedback-combined-adverbial-role]], [[feedback-explanation-row-order]]

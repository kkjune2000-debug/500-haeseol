---
name: feedback-multi-adverbial-header-merge
description: 어순 헤더에서 부사어가 2개 이상일 때 부사어(A + B) 하나로 합쳐 표기
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

exp-table 어순 헤더(colspan 행)에서 한 문장에 **부사어가 2개 이상**이면, `부사어(A) + 부사어(B)`로 나열하지 말고 **하나로 합쳐** `부사어(A + B)`로 표기한다. 영어도 `Adverbial (A + B)` 한 묶음.

예:
- 314: 주어 + **부사어(원인 + 대상)** + 서술어(동사) — Subject + Adverbial (Cause + Target) + Predicate (Verb)
- 319: 주어 + **부사어(원인 + 장소)** + 서술어(동사) — Subject + Adverbial (Cause + Place) + Predicate (Verb)

**단, 본문 Role 셀(역할 열)은 각 부사어를 개별 라벨로** 유지한다 (예: 왜 → 부사어(원인), 병원에 → 부사어(장소)). 합치는 건 헤더의 어순 요약에서만.

부사절이 섞이면 절은 따로(부사절(원인))로 두고 합치지 않을 수 있음 — 같은 '부사어'끼리만 합친다. [[feedback-range-adverbial-labels]] [[feedback-korean-order-role-canon]] [[feedback-combined-adverbial-role]]

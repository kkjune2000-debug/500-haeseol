---
name: feedback-gstep-card-table-style
description: 카드형 gstep 표 통일 스타일 + 카테고리 4색 시스템(파랑/보라/초록/앤버)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

문법 정리(gstep)의 표는 "둥근 카드 + 채도 높은 그라데이션 헤더(흰 글씨)" 카드 스타일로 통일한다. **단, 색은 하드코딩 금지 — 교재는 카테고리별 4색 시스템이 의도적으로 설계돼 있다.** 2026-05-31 전 67개 파일에 일괄 적용 완료.

**카테고리 색 시스템 (파일 번호 범위로 판별):**
- 문장구조 1~86 → 🔵 파랑: 헤더 `linear-gradient(135deg,#2563eb,#3b82f6)`, 그림자 `rgba(37,99,235,0.14)`, 보더 `#bfdbfe`
- 서술어 87~247 → 🟣 보라: `#7c3aed→#a855f7`, `rgba(124,58,237,0.14)`, `#ddd6fe`
- 부사어 248~365 → 🟢 초록: `#16a34a→#22c55e`, `rgba(22,163,74,0.14)`, `#a7f3d0`
- 기타 366~500 → 🟡 앰버: `#d97706→#f59e0b`, `rgba(180,83,9,0.14)`, `#fde68a`

**적용 방식 = `.gstep-table` CSS 클래스 정의를 업그레이드** (인라인으로 표마다 X). 모든 파일이 이 클래스를 공유하므로 클래스만 바꾸면 파일 내 전 표가 카테고리 색 그대로 한 번에 업그레이드됨. 표준 CSS:
- `.gstep-table { border-collapse:separate; border-spacing:0; background:#fff; border:1px solid [카테고리보더]; border-radius:14px; overflow:hidden; box-shadow:0 4px 16px [카테고리그림자]; }`
- `.gstep-table thead th { background:linear-gradient(135deg,[SAT1],[SAT2]); color:#fff; font-weight:800; padding:13px 12px; text-align:center; font-size:0.9rem; letter-spacing:0.01em; }` (옛 버전: 연한 pastel + 어두운 글씨 + uppercase → 폐기)
- `td { padding:13px 12px; text-align:center; }`, 짝수행 카테고리 연색.

**pill 배지·어미 칩은 의미색(인라인, 조건 컬럼에만)**: 없음/X 빨강 `#fee2e2/#dc2626`, 있음/O 초록 `#dcfce7/#16a34a`, 양성 앰버 `#fef3c7/#d97706`, 음성 블루 `#dbeafe/#2563eb`. 카테고리색과 무관하게 의미를 인코딩하므로 그대로 둔다. → [[feedback-batchim-table-labels]]

예외: `307~313 부사어 문법 원인 때문에 (2).html`는 옛 블루 템플릿이라 별도 수동 처리함(표는 초록 카드로 맞췄으나 gstep-pattern 등 나머지는 여전히 블루). 백업: `마스터-템플릿-적용본\_backup_css_20260531\`.

[[feedback-lesson-grammar-summary-style]] [[feedback-batchim-conditional-pattern]] [[feedback-table-cell-alignment]]

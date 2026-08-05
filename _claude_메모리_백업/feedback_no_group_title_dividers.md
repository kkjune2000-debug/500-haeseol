---
name: feedback-no-group-title-dividers
description: "Delete all <div class='group-title'>── ... ──</div> decorative section dividers. They're redundant — the h2/h3/gstep structure already organizes content."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

`<div class="group-title">── [텍스트] ──</div>` 형태의 장식적 섹션 구분선은 모두 **삭제**합니다.

**Why:** 사용자가 여러 차례 같은 패턴 삭제 지시 (2026-05-30/31):
- `── Who (누구) ──`, `── When (언제) ──` (51~60)
- `── Where (어디) ──`, `── What (무엇) ──` (61~70)
- `── '~고' = and ──`, `── '~거나' = or ──`, `── '~지만' = but ──` (79~86)
- `── '와/과' = and (nouns) ──`, `── '나/이나' = or (nouns) ──` (79~86)

lesson 구조(`<h2>`, `<h3>`, gstep 박스)가 이미 콘텐츠를 명확히 조직하므로 중간 ── XYZ ── 구분선은 시각적 노이즈일 뿐 학습 가치 X.

**삭제 패턴 (정확):**
```
<div class="group-title">── [임의의 텍스트] ──</div>
```

**Regex (Python):**
```python
import re
PATTERN = re.compile(r'<div class="group-title">── [^─]+ ──</div>\s*\n?')
text = PATTERN.sub('', text)
```

**유지 (절대 삭제 금지):**
- `<h2>`·`<h3>` 섹션 제목 — 정식 구조 헤더
- gstep 박스 (`<div class="gstep">`) — 정식 학습 단위
- 다른 종류의 구분선·테두리 (`<hr>`, `<div style="border-top...">` 등)

**How to apply:**
- 모든 lesson HTML 파일에 일괄 적용 — 발견 즉시 제거.
- 신규 lesson 작성 시 group-title 클래스 자체를 사용하지 말 것.
- (2026-05-31 전수 검사: 67개 파일 중 group-title divider 잔존 **0건** ✓)

Related: [[feedback-grammar-overview-subtitle]] (h2 Grammar Overview 다음 subtitle 삭제)

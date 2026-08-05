---
name: feedback-gstep-pattern-structure-order
description: "Within Grammar Overview, both gstep H3 section titles AND gstep-pattern boxes use English on top, Korean below in <small>. General explanation prose (gstep body text, explain-note) still follows Korean-first rule."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**문법 정리 안의 두 시각 요소** — gstep H3 섹션 제목 + gstep-pattern 박스 — 는 영어가 위, 한국어가 아래(`<small>`)에 와야 합니다. 일반 설명 산문은 한국어-영어 순서 유지.

**Why:** 사용자가 두 단계에 걸쳐 명시:
1. (2026-05-31 #1) gstep-pattern 박스의 문장 순서 표시는 영어 위, 한국어 아래 (41~50 sentence structure 예시)
2. (2026-05-31 #2) gstep H3 섹션 제목도 영어 위, 한국어 아래 (41~50 "간접목적어란?" h3 예시)

학습자(영어 화자)에게 영어가 먼저 보이는 게 직관적이고, 라벨/제목성 텍스트는 영어가 시각 척추 역할.

**적용 대상 — English-first (영어 위, 한국어 아래):**

1. **gstep H3 섹션 제목** (`<h3 style="...">...</h3>` inside gstep-body):
   - Before: `<h3>간접목적어란? (What is an indirect object?)</h3>`
   - After: `<h3>What is an indirect object?<br><small style="font-weight:600;">간접목적어란?</small></h3>`

2. **gstep-pattern 박스** (`<div class="gstep-pattern">...</div>`) showing sentence structure:
   - Before (Korean-first): `<div class="gstep-pattern">저는 (Subject) + 선물을 (Object) + 주었습니다 (Predicate)<small>Subject + Object + Verb</small></div>`
   - After: `<div class="gstep-pattern"><strong>Subject</strong> + <strong>Object</strong> + <strong>Predicate</strong><small>저는 (주어) + 선물을 (목적어) + 주었습니다 (서술어)</small></div>`

**Small 텍스트 표기 — 한국어 정식 명칭 필수 (영어 약어 금지):**
- ❌ `<small>S + V (verb / adjective)</small>` (영어 약어)
- ❌ `<small>S + O + V</small>`
- ❌ `<small>S + IO + DO + V</small>`
- ❌ `<small>S + Adverbial + O + V</small>`
- ✅ `<small>주어 + 서술어 (동사 / 형용사)</small>` (정식 한국어 명칭)
- ✅ `<small>주어 + 목적어 + 서술어 (동사)</small>`
- ✅ `<small>주어 + 간접목적어 + 직접목적어 + 서술어 (동사)</small>`
- ✅ `<small>주어 + 부사어 + 목적어 + 서술어 (동사)</small>`

학습자가 한국어 문법 용어에 익숙해지도록, 영어-한국어 1:1 매핑을 명확히 보여줘야 함. 약어는 한국어 학습 자료에 부적합.

**Korean role-name 표 (한국어 정식 명칭):**
| English | 한국어 |
|---|---|
| Subject | 주어 |
| Predicate | 서술어 |
| Object | 목적어 |
| Direct object | 직접목적어 |
| Indirect object | 간접목적어 |
| Adverbial | 부사어 |
| Verb | 동사 |
| Adjective | 형용사 |
| Noun | 명사 |
| Adverbial (Time) | 부사어 (시간) |
| Adverbial (Place) | 부사어 (장소) |

**유지 (Korean-first 유지) — 변환 금지:**
- **gstep body 설명 박스** (`<div style="padding...background...border-left..."` containing Korean prose + English `<small>` translation) — Korean-English pairing rule 적용
- **explain-note** (`<div class="explain-note">...</div>`) — 한국어 본문 + 영어 번역
- **blockquote 예문** — 한국어 예문 + 영어 번역
- **vocabulary 박스** — 단어 정의
- 일반 prose, 본문 텍스트

**원칙:**
- **라벨/제목/구조** → English-first (시각 척추)
- **설명/예문/본문** → Korean-first (학습 본문, 영어 화자에게 영어 번역 보조)

**How to apply:**
- 새 lesson 작성 시 gstep h3 제목과 gstep-pattern 박스는 이 형식.
- 기존 파일에서 발견 시 변환:
  - h3 regex: `<h3 style="...">Korean (English)</h3>` → `<h3 style="...">English<br><small style="font-weight:600;">Korean</small></h3>`
  - gstep-pattern: 영어 라벨 위, 한국어 예시 아래

**적용 완료 (2026-05-31):**
- gstep-pattern reversed: 41~50, 271~276 (총 2건)
- gstep h3 conversion: 60개 파일, 146건
- gstep-pattern small abbreviation → Korean (51~60 4 patterns): 4건 (전수 검색 후 잔존 영어 약어 0건 확인)

Related: [[feedback-gstep-pattern-english]] (gstep-pattern에 영어 `<small>` 필수), [[feedback-gstep-pattern-english-labels]] (역할 라벨은 영어), [[feedback-korean-english-pairing]] (일반 설명 박스: 한국어 먼저)

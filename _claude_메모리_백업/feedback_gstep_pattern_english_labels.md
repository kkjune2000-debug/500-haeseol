---
name: feedback-gstep-pattern-english-labels
description: "Inside .gstep-pattern boxes, all grammar-role labels (Noun, Verb, Subject, Predicate, etc.) must be English. Korean particles/endings stay Korean. Drop 'stem/어간' from labels — the notation box in 105~114 능력 가능 declares 'Verb + ending' means 'Verb stem + ending'."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

`<div class="gstep-pattern">` 박스 안에서 **문법 역할 라벨(품사·문장 성분)은 모두 영어**로 표기합니다. 한국어 어미·조사·예문 단어는 그대로 한국어 유지.

**Why:** 사용자가 "Noun + 전에 / Verb + 기 전에" 형태(260~265 file 예시)를 표준으로 지정. 영어가 본문 언어인 학습자료에서 패턴 박스가 한국어 라벨로 시작하면 시각적 동선이 끊깁니다. 영어 라벨 + 한국어 어미 조합이 이해를 빠르게 합니다.

**핵심 단순화 — "stem/어간" 제거 (2026-05-31):**
- "Verb stem" / "동사 어간" → **"Verb"** / **"동사"**
- "Adjective stem" / "형용사 어간" → **"Adjective"** / **"형용사"**
- "Verb/Adjective stem" / "동사/형용사 어간" → **"Verb/Adjective"** / **"동사/형용사"**
- 단축형의 정확성을 확보하기 위해 **[105~114 능력 가능 lesson Grammar Overview 상단에 표기 안내 박스](D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\105~114 서술어 문법 능력 가능.html#L377)** 추가됨 — "앞으로 'Verb/Adjective + ending'은 'Verb/Adjective stem + ending'을 의미합니다" convention 선언.

**필수 치환 (모두 `<strong>` 안에서):**

품사 (Parts of speech):
- `명사` → `Noun`
- `동사` → `Verb`  (어간 단어 부착 X)
- `형용사` → `Adjective`
- `동사/형용사` → `Verb/Adjective`

문장 성분 (Sentence roles):
- `주어` → `Subject`
- `서술어` → `Predicate`
- `목적어` → `Object`
- `간접목적어` → `Indirect object`
- `직접목적어` → `Direct object`
- `부사어` → `Adverbial`
- `시간` → `Time`
- `장소` → `Place`

받침 (Korean-specific, partial):
- `받침 없음` → `No 받침` (빨간색 `#dc2626`)
- `받침 있음` → `With 받침` (초록색 `#16a34a`)
- 받침 자체는 한국 문법 고유어로 유지 — `Final consonant` 같은 영역으로 옮기지 말 것.

기타 stem-related:
- bare `stem + ` → `Verb + `
- `stem's last vowel` → `verb's last vowel`
- `[Clause N stem]` → `[Clause N]`
- `[ㄹ-stem]` / `[ㅂ-stem]` 등 불규칙 표기 → `[ㄹ-Verb]` / `[ㅂ-Verb]`
- `어간 모음` → `동사의 마지막 모음` (모음 조화 설명 시)

**유지 (절대 영어로 변환 금지):**
- `<span class="accent">` 안의 실제 한국어 어휘(예: `누가`, `언제`, `어디에`, `~고 싶습니다`, `(으)려고`) — 학습 대상 단어/어미.
- 본문 일반 텍스트 중의 한국어 (gstep-pattern 박스 바깥).
- 예문 한국어 문장.

**How to apply:**
- `.gstep-pattern` div의 inner 텍스트에만 적용 — 박스 바깥은 건드리지 말 것.
- 모든 lesson HTML 파일(`D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\*.html`) — 67개 전부 적용 완료(2026-05-31, 단순화 후 누적 ~150 substitutions).
- 신규 lesson 파일도 이 표준으로 작성. 능력 가능 lesson에 notation 박스가 항상 있는지 확인.

Related: [[feedback-gstep-pattern-english]] (gstep-pattern 박스에 영어 번역 `<small>` 필수)

---
name: haeseol-500-vocab
description: "500문장 어휘 상자 500개 전면 개편 완료(2026-08-09) — 한국어 위·영어 아래로 방향 전환, translate 슬롯 개방, 종별사·존댓말 주제어 보충"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e3c6a78-dee4-40c4-acc4-1da5aa48e492
  modified: 2026-08-08T21:40:34.775Z
---

「놀라운 한국어 500문장 해설 최종」 67개 HTML의 **어휘 상자 500개(항목 1,470 → 1,524)를 전면 개편**했다. 커밋 `6710ea0`(2026-08-09, +3426/-1011). 보고서는 「마스터-템플릿-적용본/_점검보고 2026-08-08.md」 뒤쪽에 붙여 두었다(파일은 여전히 untracked).

**새 마크업** — 상자 안이 `EN = KO` 평문에서 격자로 바뀌었다.
```
<div class="v-list">
  <span class="v-item"><b>교실</b><span class="gloss" lang="en" translate="yes">classroom</span></span>
```
CSS `.vocab-box .v-list/.v-item…`은 각 파일의 `.vocab-box { }` 바로 뒤에 삽입돼 있다.

**되풀이하면 안 되는 함정 (이번에 실제로 겪은 것)**
- 어휘는 **책 전체 누적**이다. 파일 안에서만 누적하면 오탐이 193건 나온다(전체 누적이면 14건). [[haeseol-500-content-review]]
- 단원 주제어가 어휘에 없을 수 있다. 종별사 17문항에 단위 명사가, 존댓말 12문항에 높임말이 **하나도** 없었고 어휘가 낮춤말(죽다·자다·만나다)로만 적혀 정답(돌아가셨습니다·주무시고·뵈려고)과 어긋났다. 기계 검사로는 "문법 단원이라 정상"으로 보인다 — **정답 문장과 대조해야 보인다**.
- 뜻풀이 안 한국어를 `<span translate="no">`로 감쌀 때 **한 글자 낱말(들·색·이·가·딸·밥·개)을 놓치기 쉽다**. 정규식이 2글자 이상을 요구하면 조용히 새어 나간다.
- 검증기가 중첩 `<span>`을 `(.*?)</span></span>`로 자르면 **오탐**이 난다. 깊이를 세야 한다.

**남겨 둔 것(의도)** — 갈린 뜻풀이 40낱말은 조사(`~에`·`~에서`·`~(으)로`)와 다의어(`보다` 읽다/보다)라 자리마다 뜻이 실제로 다르다. 통일하면 오히려 틀린다.

도구는 scratchpad의 `vmap.py`(표준 대응표) + `vocab_fix.py`(변환) + `vocab_verify.py`/`vocab_outside.py`/`vocab_final.py`(검증 3종). 관련 [[haeseol-500-i18n]] [[haeseol-500-audit]] [[haeseol-adj-english-gloss]]

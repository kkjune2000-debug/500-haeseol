---
name: haeseol-translate-after-review
description: 번역(언어판)은 「놀라운 한국어」 완전 검수가 끝난 뒤에 — 2026-08-12 사용자 결정. 사전 뼈대는 스냅숏이라 검수 뒤 다시 뽑아야 한다
metadata: 
  node_type: memory
  type: project
  originSessionId: a7fda439-d517-4170-bf3f-beb483f2cf0f
  modified: 2026-08-12T12:39:02.061Z
---

**언어판 번역어 채우기는 「놀라운 한국어」 완전 검수가 끝난 뒤에 합니다 — 2026-08-12 사용자 결정.** 먼저 하자고 꺼내지 마십시오.

**Why:** 번역한 뒤에 고치면 원본과 각 언어판을 모두 고쳐야 합니다. 미리 고치면 한 번만 고치면 됩니다.

**How to apply:** 다국어 사전 뼈대(`마스터-템플릿-적용본\_언어판 시험\js_사전_뼈대.py`, 932줄)는 **2026-08-12자 스냅숏**입니다. 열쇠가 소스에 적힌 문자열 그대로여야 빌더가 찾으므로, 검수하며 스크립트 문자열을 **한 글자만 고쳐도 그 줄은 오류 없이 조용히 죽습니다.** 검수가 끝나면 `python js_extract.py --dump` 를 다시 돌려 뼈대를 새로 내십시오. 그러므로 지금 할 일은 **검수**이지 번역이 아닙니다.

관련: [[haeseol-500-start-here]], [[haeseol-500-verify-before-writing]]

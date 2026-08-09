---
name: grep-slash-display
description: Grep 도구 출력이 내용 속 슬래시(/)를 역슬래시(\)로 보여줄 수 있다 — 파일 손상 진단 전에 반드시 원본 바이트 확인
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e3c6a78-dee4-40c4-acc4-1da5aa48e492
  modified: 2026-08-07T18:20:16.492Z
---

Windows에서 Grep 도구의 content 출력이 JS 코드 `c*100/total`, `split('/')`을 `c*100\total`, `split('\')`처럼 보여준 사례(2026-08-08, 500 해설집 점검). 같은 출력 안에서도 일부 줄만 왜곡돼 더 헷갈린다.

**Why:** 이를 그대로 믿고 "구문 오류로 스크립트 전멸" 같은 중대 오진을 할 뻔했다. 실제 파일은 정상이었다.

**How to apply:** Grep 출력에서 역슬래시·특수문자 이상이 보이면 결론 내리기 전에 Read 도구나 `[System.IO.File]::ReadAllLines`로 해당 줄의 실제 문자를 확인한다. 검사 스크립트(ripgrep 패턴 매칭 자체)는 정상이므로 카운트·매칭 결과는 신뢰해도 된다 — 왜곡은 표시 단계다.

관련: [[haeseol-silent-failure]]

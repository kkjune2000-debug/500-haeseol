---
name: workflow-args-cr-gotcha
description: "Workflow 툴 함정 — args를 JSON 문자열로 넘기면 pipeline이 죽고, Windows에서 스크립트 파일에 CR(\\r)이 박혀 승인 검사에 걸린다"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6ef7c53f-3fb0-4912-a320-2be45f2ec0ff
---

Workflow 툴로 데이터를 넘길 때 두 가지 함정을 겪었다(2026-07-18, TOPIK 유형03 검증).

**1. args를 JSON 문자열로 넘기면 pipeline이 죽는다.**
`pipeline() expects an array as the first argument` — args에 JSON 배열 텍스트를 넣었는데 문자열로 직렬화되어 스크립트가 `args`를 문자열로 받았다.

**How to apply:** 데이터가 크면 args로 넘기지 말고 **스크립트에 직접 임베드**한다 (`const items = [...]`). Python으로 JSON을 읽어 `__DATA__` 자리에 끼운 .js를 만들고, `Workflow({scriptPath})`로 실행. (스크립트 maxLength 524288, 18KB 데이터도 여유.)

**2. Windows가 `\n`→`\r\n`으로 바꿔 스크립트에 CR(0x0D)이 박힌다.**
`script contains control characters` 승인 검사 오류. Python 텍스트 모드 쓰기가 CR을 넣고, 텍스트 모드 읽기가 다시 가려서 스캔에 안 잡힌다.

**How to apply:** 스크립트 파일을 **바이너리로 읽어 `\r` 제거** 후 다시 쓴다: `open(f,'rb').read().replace(b'\r\n',b'\n').replace(b'\r',b'\n')`. 문서에 코드 예시를 넣을 때도 같은 함정 — [[haeseol-hwagin-an-han-geot]] 참고(heredoc 금지, 되읽어 확인).

**검증 워크플로 패턴(유용):** 문항을 정답·해설 가리고 **블라인드로 풀게 해서**(1단계) 정답키와 대조 + 각 해설을 **적대적으로 검토**(2단계). pipeline으로 문항별 두 단계. 기계 그물 없는 이미지 회차 정답까지 독립 확인된다. [[topik1-yuhyeong-progress]]

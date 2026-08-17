---
name: haeseol-500-dogu-inswuingye
description: 500문장 해설집의 검사·음원 도구와 인수인계 문서가 저장소 어디에 있는가 (2026-08-10 정비)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e3c6a78-dee4-40c4-acc4-1da5aa48e492
  modified: 2026-08-09T19:54:48.805Z
---

500문장 해설집의 도구는 이제 **저장소 안**에 있습니다. 임시 폴더에 두지 마십시오 — 세션이 끝나면 사라집니다.

- **`마스터-템플릿-적용본\_도구\`** — `check_all.py`(검사 4종 한 번에) · `check_structure/script_order/style/spec.py` · `audio_build.py`(list→make→wire) · `show_text.py` · `README.md`
  - 경로는 `_paths.py` 가 자기 위치에서 거슬러 올라가 찾습니다. **경로를 글자로 박지 마십시오** (컴마다 드라이브 문자가 다름).
  - 출력은 `_paths.stdout()`. PowerShell cp949 에서 한글이 깨집니다.
- **`_작업_인수인계.md`** (2026-08-10 전면 개정) + **`_인수인계_시작멘트.html`** — 새 컴 준비·규칙·함정 10종·남은 일.
- **`_claude_메모리_백업\2026-08-10 현행 메모리\`** — 이 메모리의 사본. 6월판 55개는 부록·숫자표·파일명 규칙이 거기에만 있어 함께 둡니다.

**무엇을 고치든 반영한 뒤 `python check_all.py`.** 모두 0건이어야 정상입니다.

★ 문서에 숫자를 적을 때는 **파일에서 세십시오.** 이번에도 기억으로 적을 뻔한 둘이 틀렸습니다 — `translate="yes"` 21,916(→실제 23,867), 「`<title>` 84개 미잠금」(→제목은 전부 translate="yes" 이고 그 안의 한국어가 안 감싸인 것이 80파일). [[haeseol-hwagin-an-han-geot]]

관련: [[haeseol-500-eumseong]] [[haeseol-500-i18n]] [[haeseol-silent-failure]]

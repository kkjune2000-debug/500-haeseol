---
name: haeseol-esc-nae-geul
description: "내 글(sol·why·note·clue·desc)은 그대로 넣고, 원문(opts·line·ask)만 esc()로 감싼다. 짝 안 맞으면 <b>가 글자로 보인다"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ef7c53f-3fb0-4912-a320-2be45f2ec0ff
---

렌더러에서 **내 글은 그대로, 원문은 `esc()`** 로 감싼다.

| | 처리 |
|---|---|
| 내 글 — `sol` `solEn` `why` `whyEn` `note` `noteEn` `clue` `clueEn` `desc` `tag` | **그대로** (굵게 쓰라고 만든 자리) |
| 원문 — `opts` `line` `ask` `parts` `title` `body` `passage` `frame` | **`esc()`** (손대면 안 되는 글) |

**Why:** `sol` 만 esc 로 감싸고 `why` 는 안 감싸는 식으로 **짝이 안 맞아** 화면에 `<b>` 가 482곳 글자로 그대로 보였다. 오답 캡슐도 한국어 `note` 는 그대로인데 영어 `noteEn` 만 감쌌다. 유형07·08 은 sol 에 `<b>` 를 안 써서 멀쩡해 보였고 유형09부터 터졌다.

**How to apply:**
- 새 필드를 만들 때 **한국어와 영어를 같이** 결정한다. 한쪽만 감싸면 반드시 터진다.
- esc 를 벗기기 전에 값 안의 `<` 가 전부 정상 태그인지 먼저 확인한다.
- ★검사기가 **화면 글자**를 보게 할 것★ — 개수·게이팅만 세면 이 부류를 못 잡는다. `body.cloneNode` → **script/style 제거** → `textContent` 에 태그가 있으면 실패. (script 를 안 떼면 데이터의 `<b>` 가 다 잡혀 오탐)

[[haeseol-silent-failure]] [[topik1-haeseoljip-project]]

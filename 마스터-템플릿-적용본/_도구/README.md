# _도구 — 점검·음원 도구

파이썬 스크립트입니다. **이 폴더 안에서** 실행하십시오(서로를 불러 씁니다).

```powershell
cd "…\마스터-템플릿-적용본\_도구"
python check_all.py
```

경로는 스크립트가 **자기 위치에서 거슬러 올라가** 찾습니다.
드라이브 문자(`D:\OneDrive…` / `C:\Users\…\OneDrive…`)가 달라도 그대로 돌아갑니다.
새 스크립트를 쓸 때도 경로를 글자로 박지 말고 `import _paths` 를 쓰십시오.

---

## 검사

| 파일 | 무엇을 보는가 |
|---|---|
| **`check_all.py`** | 아래 넷을 한 번에. **무엇을 고치든 반영 뒤 이것부터.** |
| `check_structure.py` | 태그 짝 · 중괄호 · `data-ans`(정답)가 HEAD와 같은가 · 번호표가 가리키는 mp3가 실제로 있는가 |
| `check_script_order.py` | 함수를 정의한 `<script>`보다 **앞선 블록**에서 부르는가 |
| `check_style.py` | `<style>` 블록마다 중괄호가 맞는가 · 스크립트가 스타일 안에 끼지 않았는가 |
| `check_spec.py` | 폭·여백·viewport·lang·charset이 파일마다 같은가 |

모두 **0건**이어야 정상입니다.

### 이 검사들이 왜 생겼는가 — 실제로 터졌던 사고

- **`check_script_order.py`** — `jmSpk`를 정의한 `<script>`를 표를 그리는 스크립트 **뒤에** 넣었습니다. `ReferenceError`가 나면서 「퀴즈 2 · 쓰기」 표가 **23개 파일에서 통째로 사라졌습니다.** 같은 블록 안이면 호이스팅으로 살지만 블록이 다르면 죽습니다. `onclick="…"` 안에서 부르는 것은 클릭할 때 실행되므로 괜찮습니다.
- **`check_style.py`** — 스크립트를 꽂을 자리를 정규식 `<body[^>]*>`로 찾았더니 **CSS 주석 안의 글자 `3) <body>`** 에 걸려 `<style>` 한복판에 스크립트를 넣었습니다. 스크립트의 `/* … */` 가 바깥 CSS 주석을 먼저 닫아 그 뒤 CSS가 통째로 죽었고 `.container{max-width:800px}` 도 함께 죽어 **조사 A~F가 화면 가득 퍼졌습니다.** 그때 저는 "CSS 글자가 있으니 같다"고 잘못 답했습니다. → **태그가 아니라 적용되는가를 보십시오.**
- **`check_structure.py`의 `data-ans` 대조** — 설명만 고치는 작업에서 정답이 바뀌면 그건 사고입니다. HEAD와 대조해 즉시 잡습니다.

---

## 음원

| 파일 | 쓰임 |
|---|---|
| `audio_build.py list` | 소리 단추가 부르는데 음원이 없는 문장을 **보기만** |
| `audio_build.py make` | 없는 것을 굽는다 (여성·남성 두 벌) |
| `audio_build.py wire` | 구운 번호를 각 HTML의 `AK_SND`에 잇는다 |

```powershell
pip install edge-tts        # 무료, 열쇠(API key) 필요 없음
python audio_build.py list
python audio_build.py make
python audio_build.py wire
python check_structure.py   # 번호표가 가리키는 파일이 없는 것 0개인지
```

목소리는 **여성 `ko-KR-SunHiNeural` · 남성 `ko-KR-HyunsuMultilingualNeural`** 로 고정입니다(사용자가 들어 보고 고른 것). Hyunsu는 다국어 음성이라 한국어·일본어·영어·중국어를 **한 사람 목소리로** 읽습니다 — 다른 언어판을 만들 때 화자를 바꾸지 않아도 됩니다.

### 소리 구조

```
_소리\f\0001.mp3   여성          _소리\m\0001.mp3   남성
_소리\*.json       문장 → 번호   ← 번호가 겹치지 않게 하려는 장부일 뿐
각 HTML 안의  var AK_SND = {…}   ← 브라우저가 실제로 보는 번호표
```

★ **브라우저가 보는 것은 HTML 안의 `AK_SND` 입니다.** json만 고치면 아무 일도 일어나지 않습니다. 반드시 `wire` 를 돌리십시오.

재생은 `speakKorean(문장, 성별)` → 구운 mp3(`akPlayFile`) → 없으면 브라우저 음성(`akSpeakTTS`) 순입니다.
`speechSynthesis.cancel()` 직후 바로 `speak()` 하면 **목소리가 바뀝니다.** 60ms 기다리는 `setTimeout` 을 지우지 마십시오.

---

## 보기

| 파일 | 쓰임 |
|---|---|
| `show_text.py "2 조사"` | 태그를 걷어 내고 **화면에 보이는 글자만** 뽑는다 |

고치기 전후로 각각 받아 `diff` 하면 무엇이 달라졌는지 한눈에 보입니다. 마크업만 비교하면 틀린 판정을 내립니다.

```powershell
python show_text.py "2 조사" > 전.txt
#  … 고친 뒤 …
python show_text.py "2 조사" > 후.txt
```

---

## 새 도구를 쓸 때

- 출력은 `_paths.stdout()` 을 쓰십시오. PowerShell 기본 코드페이지(cp949)에서 한글이 깨집니다.
- 파일은 **반드시 `--apply` 를 따로 두고** 먼저 모의 실행(dry run)하십시오. 바꿀 개수가 예상과 맞을 때만 반영합니다.
- 쓰기 직전에 **태그 짝 검사**를 넣고, 깨지면 그 파일은 건너뛰게 하십시오. 한 번에 여러 파일을 망가뜨리는 것을 막습니다.
- 여러 자리를 고칠 때는 **뒤에서 앞으로** 고치십시오. 앞부터 고치면 뒤쪽 위치가 밀립니다. 정렬은 반드시 **위치 기준**으로 — 한 번은 파일 이름 문자열로 정렬해 17개 파일의 태그를 깨뜨린 적이 있습니다.

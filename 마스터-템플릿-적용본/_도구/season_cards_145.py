# -*- coding: utf-8 -*-
r"""145 「계절 + 작년/내년」 표 → 「카드 보고 말하기」 카드 여덟 장 (사용자 결정 2026-08-20).

    python season_cards_145.py [--apply]

무엇을
    표 4줄 × 2칸(작년/내년) 을 카드 여덟 장으로 바꿉니다.
        앞면 last spring  →  누르면  뒷면 작년 봄 🔊
    「🍂 계절 + 작년/내년」 이름표와 아래의 💡 안내는 그대로 둡니다.

★ 같은 파일 위쪽 「시간 표현 정리」 표는 **그대로 둡니다**(사용자 결정).
  그 표는 낱말이 아니라 **줄·칸이 나란한 데서 보이는 규칙**(지난주/지난달 · 다음 주/다음 달)이
  가르침이라 카드로 흩으면 잃는 것이 있습니다.

★ 카드 얼개는 이 파일에 이미 있는 것을 그대로 물려받습니다 — 어제 93번 요일 카드와
  같은 꼴(`flashcard-grid look-speak`). 누르는 동작·펴지는 CSS 를 새로 만들지 않습니다.
★ 이 파일의 「카드 보고 말하기」 여덟 장은 **모두 구운 mp3** 로 소리가 납니다. 새 여덟 장도
  같은 수준으로 맞춥니다 — 넣은 뒤 `audio_build.py list → make → wire` 를 돌리십시오.
★ 차례는 표를 읽던 차례 그대로(작년 봄 · 내년 봄 · 작년 여름 …)라 작년/내년이 옆에 붙어
  견주기 좋습니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 142~149 서술어 문법 희망.html")
APPLY = "--apply" in sys.argv

PAIRS = [("last spring", "작년 봄"), ("next spring", "내년 봄"),
         ("last summer", "작년 여름"), ("next summer", "내년 여름"),
         ("last fall", "작년 가을"), ("next fall", "내년 가을"),
         ("last winter", "작년 겨울"), ("next winter", "내년 겨울")]

CARD = ('<div class="flashcard" onclick="this.classList.toggle(\'flipped\')">'
        '<div class="flashcard-inner">'
        '<div class="flashcard-front"><div class="flashcard-text">'
        '<span lang="en" translate="yes">%s</span></div>'
        '<div class="flashcard-hint">▼ <span lang="en" translate="yes">Tap to check</span></div>'
        '</div>'
        '<div class="flashcard-back"><div class="flashcard-text">%s</div>'
        '<button translate="yes" class="flashcard-listen" '
        'onclick="event.stopPropagation(); speakKorean(\'%s\')" title="Listen">🔊</button>'
        '</div></div></div>')

# ★한 줄짜리 짧은 카드라 키를 낮춥니다 — 어제 요일 카드와 같은 값입니다.
#   (어제 것은 선택자가 `.hb-grid, .yo-grid .flashcard` 로 적혀 있어 앞엣것에는
#    안 걸립니다. 여기서는 한 클래스로 또렷하게 적습니다.)
CSS = """
/* 계절 카드 — 한 줄짜리라 키를 낮춘다 (2026-08-20) */
.ss-grid .flashcard{height:auto;}
.ss-grid .flashcard-front,.ss-grid .flashcard-back{min-height:0;padding:11px 14px;}
.ss-grid .flashcard-front{padding-bottom:26px;}
.ss-grid .flashcard-text{font-size:1rem;font-weight:700;line-height:1.4;}
"""


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))


s0 = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s0 else "\n"

i = s0.find("계절 + 작년/내년")
assert i > 0, "「계절 + 작년/내년」 이름표를 못 찾았습니다"
a = s0.find('<div class="tbl-scroll">', i)
b = s0.find("</table>", a)
assert 0 < a < b, "표를 못 찾았습니다"
b = s0.find("</div>", b) + len("</div>")
table = s0[a:b]
for _, ko in PAIRS:
    assert ko in table, f"표에 「{ko}」 가 없습니다 — 표가 바뀌었는지 보십시오"

grid = ('<div class="flashcard-grid look-speak ss-grid">'
        + "".join(CARD % (en, ko, ko) for en, ko in PAIRS) + "</div>")
s = s0[:a] + grid + s0[b:]

# 덮어쓰기 CSS 는 마지막 <style> 끝에 (이 책의 관례)
m = list(re.finditer(r"</style>", s))[-1]
s = s[:m.start()] + CSS.replace("\n", nl) + s[m.start():]

# ── 검산
v, v0 = vis(s), vis(s0)
for en, ko in PAIRS:
    assert v.count(ko) >= v0.count(ko), f"{ko} 가 줄었습니다"
    assert en in v, f"{en} 이 없습니다"
assert "시간 표현" in v, "시간 표현 표가 사라졌습니다"
assert v.count("어제") == v0.count("어제"), "시간 표를 건드렸습니다"
for tg in ("div", "span", "button", "table", "tr", "td", "th", "style"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"<{tg}> 짝이 어긋남"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
assert s.count("<table") == s0.count("<table") - 1, "표가 하나만 줄어야 합니다"
# ★줄 수는 줄어드는 것이 정상입니다(여러 줄짜리 표를 한 줄 카드로 바꿉니다).
#   봐야 할 것은 **홑 LF 가 생겼는가**입니다 — 이 책은 CRLF 뿐이어야 합니다.
assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n") == 0, \
    "홑 LF 가 생겼습니다"

print(f"■ 표 하나 → 카드 {len(PAIRS)}장")
for en, ko in PAIRS:
    print(f"     {en:<13} →  {ko}")
print(f"■ 표 마크업 {len(table):,}자 → 카드 {len(grid):,}자")
print("■ 검산 통과 — 여덟 쌍 그대로 · 시간 표 그대로 · 태그 짝 · CSS 중괄호 · 줄끝")

if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 이어서 audio_build.py list → make → wire 를 돌리십시오")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

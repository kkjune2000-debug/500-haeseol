# -*- coding: utf-8 -*-
r"""취미 카드를 「카드 보고 말하기」와 **완전히 같게** (사용자 지시 2026-08-19)

  ① 배경색 — look-speak 무지개 팔레트를 그대로 씁니다.
     본래 팔레트는 nth-child(1~10) 뿐이라 21장에는 모자랍니다.
     10장마다 되풀이하도록 nth-child(10n+K) 를 더합니다.
     ★특정도: look-speak 쪽(클래스 4개)이 제 규칙(3개)보다 높아
       1~10번은 본래 규칙이, 11~21번은 되풀이 규칙이 먹습니다. 색은 같습니다.
  ② 2열 — .hb-grid 의 1열 지정을 없애 .flashcard-grid 의 2열을 물려받습니다
     (좁은 화면에서는 본래 media 규칙대로 1열).
  ③ 음성 — 뒷면에 flashcard-listen 단추를 답니다.
     ★취미 21낱말은 **모두 구워 둔 mp3 가 AK_SND 에 있습니다**(확인함).
       그래서 TTS 폴백이 아니라 진짜 음원이 납니다.

사용: python hobby_lookspeak2.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

# look-speak 팔레트 (본래 파일에서 그대로 옮김)
PAL = [("#fdf2f8", "#fce7f3", "#fce7f3", "#fbcfe8"),
       ("#fff1f2", "#ffe4e6", "#ffe4e6", "#fecdd3"),
       ("#fff7ed", "#ffedd5", "#ffedd5", "#fed7aa"),
       ("#fffbeb", "#fef3c7", "#fef3c7", "#fde68a"),
       ("#fefce8", "#fef9c3", "#fef9c3", "#fef08a"),
       ("#f7fee7", "#ecfccb", "#ecfccb", "#d9f99d"),
       ("#ecfdf5", "#d1fae5", "#d1fae5", "#a7f3d0"),
       ("#f0fdfa", "#ccfbf1", "#ccfbf1", "#99f6e4"),
       ("#f0f9ff", "#e0f2fe", "#e0f2fe", "#bae6fd"),
       ("#f5f3ff", "#ede9fe", "#ede9fe", "#ddd6fe")]

OLD_CSS_MARK = "/* 취미 — 카드 보고 말하기 꼴 (2026-08-19) */"
NEW_CSS = OLD_CSS_MARK + """
.hb-grid .flashcard{height:auto;}
.hb-grid .flashcard-front,.hb-grid .flashcard-back{min-height:0;padding:11px 14px;}
.hb-grid .flashcard-front{padding-bottom:26px;}
.hb-grid .flashcard-text{font-size:1rem;font-weight:700;line-height:1.4;}
.hb-grid .flashcard-hint{bottom:7px;right:12px;}
.hb-grid .flashcard-listen{width:32px;height:32px;margin-top:6px;}
"""
for i, (fb, fc, b1, b2) in enumerate(PAL, start=1):
    NEW_CSS += (f".hb-grid .flashcard:nth-child(10n+{i % 10}) .flashcard-front"
                f"{{background:{fb};border-color:{fc};}}\n"
                f".hb-grid .flashcard:nth-child(10n+{i % 10}) .flashcard-back"
                f"{{background:linear-gradient(135deg,{b1} 0%,{b2} 100%);}}\n")

s0 = io.open(P, encoding="utf-8").read()
s = s0

# ── ① CSS 갈아 끼우기
m = re.search(re.escape(OLD_CSS_MARK) + r"[\s\S]*?(?=\n/\*|\n</style>|</style>)", s)
assert m, "옛 CSS 를 못 찾음"
s = s[:m.start()] + NEW_CSS + s[m.end():]

# ── ② look-speak 붙이고 1열 지정 없애기
a = '<div class="flashcard-grid hb-grid">'
b = '<div class="flashcard-grid look-speak hb-grid">'
assert a in s, "취미 카드 묶음을 못 찾음"
s = s.replace(a, b, 1)

# ── ③ 뒷면에 소리 단추
# ★비탐욕 [\s\S]*?</div> 는 **첫 </div>** 에서 끊긴다 — 안에 div 가 겹겹이라
#   묶음이 통째로 안 잡힌다. div 짝을 세어 끝을 찾는다.
a0 = s.index('<div class="flashcard-grid look-speak hb-grid">')
d, i = 1, s.index(">", a0) + 1
while d and i < len(s):
    t = re.compile(r"</?div\b").search(s, i)
    if not t:
        break
    d += -1 if t.group(0).startswith("</") else 1
    i = t.end()
e0 = s.find(">", i - 1) + 1


blk = s[a0:e0]
n = 0


def add_btn(mo):
    global n
    ko = mo.group(1)
    n += 1
    return (mo.group(0).rstrip()[:-len("</div>")]
            + f'<button translate="yes" class="flashcard-listen" '
              f'onclick="event.stopPropagation(); speakKorean(\'{ko}\')" '
              f'title="Listen">🔊</button></div>')


# ★이 책의 파일은 태그마다 줄바꿈되어 저장됩니다. 공백을 견디게 써야 합니다.
nb = re.sub(r'<div class="flashcard-back">\s*<div class="flashcard-text">([^<]+)'
            r'</div>\s*</div>', add_btn, blk)
assert n == 21, f"소리 단추 {n}개 (21이어야 함)"
s = s[:a0] + nb + s[e0:]

# ── 검산
for tg in ("div", "span", "button", "style"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
assert s.count('class="flashcard-listen"') - s0.count('class="flashcard-listen"') == 21
print(f"■ 소리 단추 {n}개 · look-speak 팔레트 10색 되풀이 · 2열")
if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

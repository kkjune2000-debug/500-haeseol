# -*- coding: utf-8 -*-
r"""93번 해설에 요일 카드 — 91번 취미 카드와 똑같은 꼴 (사용자 지시 2026-08-19)

  · 머리 h4 는 91번 것과 **같은 style 문자열**을 씁니다(초록).
  · 카드는 look-speak 무지개 팔레트 · 넓은 화면 2열 · 뒷면에 소리 단추.
  · 취미 카드용 CSS(.hb-grid)를 `.hb-grid, .yo-grid` 로 넓혀 그대로 나눠 씁니다.
  ★요일 일곱 모두 AK_SND 에 구워 둔 mp3 가 있습니다
    (월 1526 · 화 1906 · 수 1295 · 목 1114 · 금 0766 · 토 1803 · 일 1558).
  ★이 책의 파일은 태그마다 줄바꿈되어 저장됩니다 — 붙여 쓴 정규식은 안 맞습니다.

사용: python yoil_cards_93.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

DAYS = [("월요일", "Monday"), ("화요일", "Tuesday"), ("수요일", "Wednesday"),
        ("목요일", "Thursday"), ("금요일", "Friday"), ("토요일", "Saturday"),
        ("일요일", "Sunday")]

H4STYLE = ("margin:16px 0 8px; padding:8px 14px; font-size:1rem; font-weight:800; "
           "color:#0f5e2c; background:#f7fee7; border-left:4px solid #86efac; "
           "border-radius:4px;")


def card(ko, en):
    return ('<div class="flashcard" onclick="this.classList.toggle(\'flipped\')">'
            '<div class="flashcard-inner">'
            '<div class="flashcard-front"><div class="flashcard-text">'
            f'<span lang="en" translate="yes">{en}</span></div>'
            '<div class="flashcard-hint">▼ 눌러서 확인</div></div>'
            f'<div class="flashcard-back"><div class="flashcard-text">{ko}</div>'
            f'<button translate="yes" class="flashcard-listen" '
            f'onclick="event.stopPropagation(); speakKorean(\'{ko}\')" '
            f'title="Listen">🔊</button></div>'
            '</div></div>')


BLOCK = (f'<h4 style="{H4STYLE}">요일<br>'
         '<small style="font-weight:600;" lang="en" translate="yes">'
         'Days of the week</small></h4>'
         '<div class="flashcard-grid look-speak yo-grid">'
         + "".join(card(k, e) for k, e in DAYS) + '</div>')

s0 = io.open(P, encoding="utf-8").read()
s = s0
assert "yo-grid" not in s0, "이미 넣었습니다"

# ── ① CSS 를 .hb-grid, .yo-grid 로 넓힌다
n_css = 0
def widen(mo):
    global n_css
    n_css += 1
    return ".hb-grid, .yo-grid" + mo.group(1)
s = re.sub(r"\.hb-grid(\s|\.| )", lambda m: ".hb-grid, .yo-grid" + m.group(1)
           if m.group(1) != "," else m.group(0), s)
n_css = s.count(".yo-grid")
assert n_css >= 25, f"CSS 를 {n_css}곳밖에 못 넓힘"

# ── ② 93번 해설의 wo-box 뒤에 카드 넣기
m = re.search(r'<h3><span lang="en" translate="yes">93\)[\s\S]*?'
              r'<div class="explain-content">[\s\S]*?(</div>\s*</div>\s*</div>)', s)
assert m, "93번 해설을 못 찾음"
# wo-box 가 닫히는 자리 = explain-content 안 첫 wo-box 의 끝
i = s.index('<div class="wo-box">', m.start())
d, j = 1, s.index(">", i) + 1
while d and j < len(s):
    t = re.compile(r"</?div\b").search(s, j)
    if not t:
        break
    d += -1 if t.group(0).startswith("</") else 1
    j = t.end()
end = s.find(">", j - 1) + 1
s = s[:end] + "\n" + BLOCK + s[end:]

# ── 검산
for tg in ("div", "span", "button", "h4", "small", "style"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
assert s.count("flashcard-listen") - s0.count("flashcard-listen") == 7
assert s.count('class="flashcard"') - s0.count('class="flashcard"') == 7
print(f"■ 요일 카드 7장 · CSS 를 .yo-grid 로 넓힌 곳 {n_css}")
for k, e in DAYS:
    print(f"   {e:<11}→ {k}")
if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

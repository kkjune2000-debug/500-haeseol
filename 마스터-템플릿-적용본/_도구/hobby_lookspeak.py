# -*- coding: utf-8 -*-
r"""취미 카드를 「카드 보고 말하기」 꼴로 (사용자 지시 2026-08-19)

  「카드 보고 말하기」(2절)는 **영어를 보고 눌러 한국어를 확인**하는 카드입니다.
  취미 21개도 그 꼴로 바꿉니다 — 앞면 영어 · 누르면 아래로 한국어.

  · 같은 파일의 .flashcard 얼개를 그대로 씁니다(누르는 동작·펼침 CSS 재사용).
  · 문항 번호(.flashcard-num)와 소리 단추는 넣지 않습니다 — 낱말이고,
    소리 단추는 앞서 빼기로 하셨습니다.
  · 색은 이 상자의 초록으로 맞추고, 낱말 하나짜리라 키를 낮춥니다.

사용: python hobby_lookspeak.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

MARK = "/* 취미 — 카드 보고 말하기 꼴 (2026-08-19) */"
CSS = MARK + """
.hb-grid{display:grid;grid-template-columns:1fr;gap:9px;margin:10px 0 6px;}
.hb-grid .flashcard{height:auto;}
.hb-grid .flashcard-front,.hb-grid .flashcard-back{min-height:0;padding:11px 14px;}
.hb-grid .flashcard-front{background:#f7fee7;border:2px solid #bbf7d0;color:#166534;
  padding-bottom:26px;}
.hb-grid .flashcard-back{background:linear-gradient(135deg,#dcfce7 0%,#bbf7d0 100%);
  color:#14532d;}
.hb-grid .flashcard-text{font-size:1rem;font-weight:700;line-height:1.4;}
.hb-grid .flashcard-hint{bottom:7px;right:12px;}
"""

CARD = ('<div class="flashcard" onclick="this.classList.toggle(\'flipped\')">'
        '<div class="flashcard-inner">'
        '<div class="flashcard-front"><div class="flashcard-text">'
        '<span lang="en" translate="yes">{en}</span></div>'
        '<div class="flashcard-hint">▼ 눌러서 확인</div></div>'
        '<div class="flashcard-back"><div class="flashcard-text">{ko}</div></div>'
        '</div></div>')

s0 = io.open(P, encoding="utf-8").read()

m = re.search(r'<div class="hb-cards">[\s\S]*?</div>\s*(?=</div>|<h4|<p|<div)', s0)
assert m, "취미 카드 묶음을 못 찾음"
blk = m.group(0)
pairs = re.findall(r'<span class="hb-card"><b>([^<]*)</b>'
                   r'<span class="gloss"[^>]*>([^<]*)</span></span>', blk)
assert pairs, "카드를 못 읽음"
print(f"■ 취미 {len(pairs)}개")
for ko, en in pairs:
    print(f"   {en:<20}→ {ko}")

new = ('<div class="flashcard-grid hb-grid">'
       + "".join(CARD.format(en=en, ko=ko) for ko, en in pairs) + '</div>')
s = s0[:m.start()] + new + s0[m.end():]

if MARK not in s:
    b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
    e = b[-1].end() - len("</style>")
    s = s[:e] + "\n" + CSS + s[e:]

for tg in ("div", "span", "b", "small", "style"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
for ko, en in pairs:
    assert ko in s and en in s, f"낱말이 사라짐 {ko} {en}"
assert "hb-cards" not in re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s), "옛 카드가 남음"
print(f"\n■ 검산 통과 — 카드 {s.count(chr(39) + 'flipped' + chr(39)) - s0.count(chr(39) + 'flipped' + chr(39))}장 늘음")

if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

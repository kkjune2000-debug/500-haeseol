# -*- coding: utf-8 -*-
r"""취미 표 → 낱말 카드 · 뒤의 두 문단 삭제 (사용자 지시 2026-08-19)

  ① 표(4열 · 소리 단추 21개)를 **낱말 카드**로 바꿉니다 — 한국어 위, 영어 아래.
     어휘 상자에 쓰는 카드와 같은 꼴이고, 색만 이 장의 초록으로 맞췄습니다.
     소리 단추는 뺍니다(사용자 지시).
     표가 아니므로 가로 스크롤(.tbl-scroll)도 함께 없어집니다.

  ② 표 뒤의 두 문단을 지웁니다 —
       「제 취미는 독서입니다 · 제 취미는 사진 찍기입니다」
       「같은 말의 다른 꼴: 춤추다(춤) · 노래하다(노래) …」

  ★낱말은 손으로 옮겨 적지 않고 **표에서 그대로 뽑습니다**.

사용: python hobby_cards.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

MARK = "/* 취미를 낱말 카드로 (2026-08-19) */"
CSS = MARK + """
.hb-cards{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px;}
.hb-card{text-align:center;padding:7px 13px;border:1px solid #bbf7d0;background:#f7fee7;
  border-radius:9px;line-height:1.35;max-width:100%;overflow-wrap:anywhere;}
.hb-card b{display:block;font-weight:800;color:#166534;font-size:1.02em;}
.hb-card .gloss{display:block;color:#15803d;opacity:1;margin-top:2px;font-size:0.86em;}
"""

s0 = io.open(P, encoding="utf-8").read()
s = s0

# ── ① 표 → 카드
m = re.search(r'<div class="tbl-scroll">\s*<table class="hb-tbl">[\s\S]*?</table>\s*</div>', s)
assert m, "취미 표를 못 찾음"
tbl = m.group(0)
pairs = []
for tr in re.findall(r"<tr[\s\S]*?</tr>", tbl):
    if "<th" in tr:
        continue
    cs = re.findall(r"<td[\s\S]*?</td>", tr)
    for k in range(0, len(cs), 2):
        ko = vis(re.sub(r"<button[\s\S]*?</button>", "", cs[k]))
        en = vis(cs[k + 1]) if k + 1 < len(cs) else ""
        if ko and en:
            pairs.append((ko, en))
print(f"■ 취미 {len(pairs)}개")
for ko, en in pairs:
    print(f"   {ko:<10}{en}")

cards = ('<div class="hb-cards">'
         + "".join(f'<span class="hb-card"><b>{ko}</b>'
                   f'<span class="gloss" lang="en" translate="yes">{en}</span></span>'
                   for ko, en in pairs)
         + '</div>')
s = s[:m.start()] + cards + s[m.end():]

# ── ② 뒤의 두 문단
for anchor in ("제 취미는 <strong>독서</strong>입니다.", "같은 말의 다른 꼴:"):
    pm = re.search(r"<p[^>]*>(?:(?!</p>)[\s\S])*?" + re.escape(anchor) + r"[\s\S]*?</p>", s)
    assert pm, f"문단을 못 찾음: {anchor}"
    print(f"   지움  {vis(pm.group(0))[:74]}")
    s = s[:pm.start()] + s[pm.end():]

if MARK not in s:
    b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
    e = b[-1].end() - len("</style>")
    s = s[:e] + "\n" + CSS + s[e:]

# ── 검산
for tg in ("div", "span", "p", "table", "tr", "td", "th", "small", "b", "strong", "style"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
assert "hb-tbl" not in re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s), "표가 남음"
for ko, en in pairs:                       # 낱말이 하나도 안 없어졌는가
    assert ko in s and en in s, f"낱말이 사라짐: {ko} {en}"
n_spk = s0.count('class="speak-btn"') - s.count('class="speak-btn"')
print(f"\n■ 소리 단추 {n_spk}개 삭제 · 검산 통과")

if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

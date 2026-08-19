# -*- coding: utf-8 -*-
r"""카드 목록 속에 잘못 들어간 「설명」 상자를 카드로 되돌린다 (사용자 지시 2026-08-19)

  72번 한국 음식 카드(김치·된장찌개·갈비·냉면) 가운데 **삼계탕만** 「설명」 상자로
  감싸여 있었습니다. 전수로 보니 같은 실수가 **열 곳**입니다.

    72 삼계탕 · 89 선생님의 · 147 삼겹살 · 162 택배가 왔습니다 · 162 전화가 옵니다 ·
   189 한국어를 영어로 바꾸다 · 213 코+물→콧물 · 293 서술절 ·
   355 비밀+번호=비밀번호 · 423 예고(豫告)

  고치는 법 — **앞 형제 카드의 style 을 그대로 물려받고** 「설명」 이름표를 뗍니다.
  카드마다 테두리 색이 달라(#fecdd3·#c7d2fe·#a5f3fc) 한 가지로 정할 수 없습니다.

사용: python fix_gb_in_grid.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"
LAB = re.compile(r'<span class="gb-lab">설명<i lang="en" translate="yes">Explanation</i>\s*</span>')

n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for m in list(re.finditer(r'<div class="gb">[\s\S]*?</div>', s))[::-1]:
        t = m.group(0)
        if not LAB.search(t):
            continue
        body = LAB.sub("", t[len('<div class="gb">'):-len("</div>")]).strip()
        if len(vis(body)) > 60 or "—" not in vis(body):
            continue
        # 앞 형제 카드의 style
        pre = s[max(0, m.start() - 600):m.start()]
        sty = re.findall(r'<div style="([^"]*border[^"]*)">', pre)
        if not sty:
            print(f"   X {f[-30:]} 앞 형제 카드를 못 찾음: {vis(body)[:34]}")
            continue
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
        new = '<div style="' + sty[-1] + '">' + body + '</div>'
        s = s[:m.start()] + new + s[m.end():]
        n += 1
        print(f"   [{hs[-1] if hs else '?':>3}] {vis(body)[:40]:<42}style ← 앞 카드")
    if s != s0:
        for tg in ("div", "span", "strong", "i"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        # 보이는 글자에서 「설명 Explanation」 짝만 줄어야 한다
        for w in ("설명", "Explanation"):
            d = vis(s0).count(w) - vis(s).count(w)
            assert d >= 0, f"{w} 가 늘었다 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
print(f"\n■ 카드로 되돌린 것 {n}곳")

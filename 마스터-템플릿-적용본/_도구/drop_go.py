# -*- coding: utf-8 -*-
r"""어휘에서 「~고」 삭제 — 6곳 (사용자 지시 2026-08-19)"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"

n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    k = 0
    for bm in list(re.finditer(r"<b>~고</b>", s))[::-1]:
        a = s.rfind('<span class="v-item', 0, bm.start())
        assert a >= 0
        d, i = 1, s.index(">", a) + 1
        while d and i < len(s):
            t = re.compile(r"</?span\b").search(s, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        e = s.find(">", i - 1) + 1
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:a])
        print(f"   [{hs[-1]}] 지움  {vis(s[a:e])}")
        s = s[:a] + s[e:]
        n += 1; k += 1
    if k:
        s = re.sub(r'(<div class="v-list">)\s{2,}', r"\1 ", s)
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        assert len(re.findall(r'class="v-item', s0)) - \
               len(re.findall(r'class="v-item', s)) == k
        assert not re.search(r'<div class="v-list">\s*</div>', s), f"빈 상자 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
            print(f"   ■ 씀 {f.split(chr(92))[-1][:30]}")
print(f"\n■ {n}곳")
assert n == 6

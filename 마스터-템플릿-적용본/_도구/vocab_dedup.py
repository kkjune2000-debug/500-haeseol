# -*- coding: utf-8 -*-
r"""한 상자 안에 표제어가 겹친 것을 지운다 (조사를 떼면서 생겼다 — 203 아들·아들에게)"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"


def spans(blk):
    got = []
    for im in re.finditer(r'<span class="v-item[^"]*">', blk):
        d, i = 1, im.end()
        while d and i < len(blk):
            t = re.compile(r"</?span\b").search(blk, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        gt = blk.find(">", i - 1)
        got.append((im.start(), gt + 1 if gt >= 0 else i))
    return got


n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for p in list(re.finditer(r'<h3><span lang="en" translate="yes">(\d+)\)[\s\S]*?'
                              r'(<div class="v-list">[\s\S]*?</div>)', s))[::-1]:
        blk = p.group(2)
        sp = spans(blk)
        seen, drop = set(), []
        for a, e in sp:
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            h = vis(hm.group(1)) if hm else ""
            if h in seen:
                drop.append((a, e, h))
            else:
                seen.add(h)
        if not drop:
            continue
        nb = blk
        for a, e, h in drop[::-1]:
            nb = nb[:a] + nb[e:]
            print(f"   [{p.group(1)}] 겹친 「{h}」 하나 지움 — {vis(blk)[:46]}")
            n += 1
        s = s[:p.start(2)] + re.sub(r"\s{2,}", " ", nb) + s[p.end(2):]
    if s != s0:
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
print(f"\n■ 겹친 표제어 {n}개")

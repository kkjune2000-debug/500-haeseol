# -*- coding: utf-8 -*-
r"""어휘에서 문법 표현을 모두 뺀다 (사용자 지시 2026-08-19 — 「다 빼라」)

  어휘는 **낱말과 뜻**만 담습니다. 조사(~에서·나/이나)와 「~고」를 뺀 데 이어
  나머지 문법 표현도 모두 뺍니다.

    ~아/어서 · ~(으)면서 · ~아/어 주세요 · ~자마자 · ~다가 · ~는데 · ~거나 ·
    ~지만 · ~ㄴ 적이 있다 · ~고 싶다 · ~것 같다 · (으)ㄹ 때 · (이)면 …

  ★남기는 것 — 「(말)하다」는 괄호로 시작하지만 **동사**입니다.
  ★상자가 비면 책이 쓰는 표시 「새 어휘 없음」으로 바꿉니다.

사용: python vocab_drop_grammar.py [--apply]
"""
import io, re, sys, glob
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"

KEEP = {"(말)하다"}
NONE = ('<span class="v-item v-none"><b>새 어휘 없음</b>'
        '<span class="gloss" lang="en" translate="yes">No new vocabulary</span></span>')


def is_gram(h):
    if h in KEEP:
        return False
    if h.startswith("~"):
        return True
    return bool(re.match(r"^[(（](으|이)[)）]", h))     # (으)ㄹ 때 · (이)면


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


stat = Counter()
empt = []
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for p in list(re.finditer(r'<h3><span lang="en" translate="yes">(\d+)\)[\s\S]*?'
                              r'(<div class="v-list">[\s\S]*?</div>)', s))[::-1]:
        num, blk = p.group(1), p.group(2)
        sp = spans(blk)
        drop = []
        for a, e in sp:
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            h = vis(hm.group(1)) if hm else ""
            if is_gram(h):
                drop.append((a, e, h))
        if not drop:
            continue
        nb = blk
        for a, e, h in drop[::-1]:
            nb = nb[:a] + nb[e:]
            stat[h] += 1
        nb = re.sub(r"\s{2,}", " ", nb)
        if 'class="v-item' not in nb:
            nb = nb.replace('<div class="v-list">', '<div class="v-list">' + NONE, 1)
            empt.append((num, [d[2] for d in drop]))
            stat["빈 상자 → 새 어휘 없음"] += 1
        s = s[:p.start(2)] + nb + s[p.end(2):]
    if s != s0:
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        assert not re.search(r'<div class="v-list">\s*</div>', s), f"빈 상자 {f}"
        stat["파일"] += 1
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)

print("■ 뺀 문법 표현")
tot = 0
for k, v in stat.most_common():
    if k in ("파일", "빈 상자 → 새 어휘 없음"):
        continue
    print(f"   {v:>3}  {k}")
    tot += v
print(f"\n   합계 {tot}개 · 파일 {stat['파일']}")
print(f"\n■ 어휘가 통째로 비게 된 상자 {len(empt)}개 → 「새 어휘 없음」")
for n, ds in empt:
    print(f"   [{n}] {' · '.join(ds)}")

# -*- coding: utf-8 -*-
r"""어휘 상자에서 **조사**를 뺀다 (사용자 원칙 2026-08-19 — 33번 「~에서」를 보고)

  「조사는 어휘에 넣지 않는 것이 좋다」

  ★조사만 뺀다 — 어미·문법 표현은 그대로 둔다.
    뺀다  ~에서 ~에 ~에게 ~(으)로 ~부터 ~까지 ~만 ~처럼 ~과/와 와/과
    안 뺀다 ~아/어서(연결어미) · ~고 싶다(문법 표현) · ~자마자 · ~는데 …

  ★그물이 양쪽으로 틀린다 — 「보다」 13개는 **동사**(watch, see)라 조사가 아니다.
    표제어 글자만 보고 걸면 그것들이 걸린다. 뜻풀이까지 봐야 한다.

  ★상자가 비면 책이 쓰는 표시로 바꾼다 —
    <span class="v-item v-none"><b>새 어휘 없음</b>…</span>

사용: python vocab_drop_josa.py [--apply]
"""
import re, sys, glob, html, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()

DROP = {"~에서", "~에", "~에게", "~(으)로", "~부터", "~까지", "~만", "~처럼",
        "~과/와", "와/과"}
NONE = ('<span class="v-item v-none"><b>새 어휘 없음</b>'
        '<span class="gloss" lang="en" translate="yes">No new vocabulary</span></span>')

def items_of(blk):
    """v-item 을 **span 짝을 세어** 뽑는다.
    항목 안에 <span class="gloss"> 가 겹쳐 있어 비탐욕 정규식은 거기서 끊긴다."""
    got = []
    for m in re.finditer(r'<span class="v-item[^"]*">', blk):
        d, i = 1, m.end()
        while d and i < len(blk):
            t = re.compile(r"</?span\b").search(blk, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        end = blk.find(">", i - 1) + 1 if blk[i - 1] != ">" else i
        got.append((m.start(), max(end, i)))
    return got

stat = Counter()
work = {}
seen = Counter()

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    s = s0
    # 어휘 상자마다
    for box in list(re.finditer(r'<div class="v-list">[\s\S]*?</div>', s))[::-1]:
        blk = box.group(0)
        spans = items_of(blk)
        if not spans:
            continue
        keep, drop = [], []
        for a, e in spans:
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            head = vis(hm.group(1)) if hm else ""
            (drop if head in DROP else keep).append((a, e))
        if not drop:
            continue
        for a, e in drop:
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            seen[vis(hm.group(1))] += 1
            out.write(f"   {f[:26]:<28}뺌  {vis(blk[a:e])[:40]}\n")
        nb = blk
        for a, e in drop[::-1]:
            nb = nb[:a] + nb[e:]
        if not keep:                      # 다 빠지면 표시로
            nb = nb.replace('<div class="v-list">', '<div class="v-list">' + NONE, 1)
            stat["빈 상자 → 새 어휘 없음"] += 1
            out.write(f"   {f[:26]:<28}★ 상자가 비어 「새 어휘 없음」으로\n")
        nb = re.sub(r"\s{2,}", " ", nb)
        s = s[:box.start()] + nb + s[box.end():]
        stat["상자"] += 1
    if s != s0:
        work[f] = (s0, s)
        stat["파일"] += 1

# ── 검산
for f, (o0, s) in work.items():
    for tg in ("span", "div", "b"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    if len(re.findall(r'class="vocab-box"', s)) != len(re.findall(r'class="vocab-box"', o0)):
        out.write(f"   ★ 어휘 상자 수 {f[:26]}\n"); stat["★"] += 1
    if re.search(r'<div class="vocab-box"[^>]*>\s*(<div[^>]*>\s*)*\s*</div>', s):
        out.write(f"   ★ 빈 어휘 상자 {f[:26]}\n"); stat["★"] += 1

out.write("\n■ 뺀 표제어\n")
for k, v in seen.most_common():
    out.write(f"   {v:>3}개  {k}\n")

if A.apply and not stat["★"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

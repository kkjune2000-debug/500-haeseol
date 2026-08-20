# -*- coding: utf-8 -*-
r"""사다리에서 **늘어난 자리를 문장에서도 같은 색으로** (사용자 지시 2026-08-19)

  이름표에서 「간접목적어」가 보라색이면 문장의 「회사에」도 보라색,
  「부사어(장소)」가 보라색이면 「집에서」만 보라색.

  전  마지막 단은 문장 **전체**가 보라색이었고, 어느 자리가 늘었는지는
      이름표만 말했다.
  후  늘어난 자리만 보라색. 문장 전체 색은 다른 단과 같게 둔다.
      한 단짜리(사다리 없음)는 그 문장이 곧 그 문항이므로 전체 보라색을 남긴다.

  ★늘어난 자리는 앞 단과 견주어 찾는다(difflib, 낱말 단위).
    끼워 넣기(insert)만 인정하고 바꿔치기·지우기가 섞이면 그 단은 건드리지 않는다 —
    그런 단은 「늘린 것」이 아니라 다른 문장이기 때문이다.

사용: python wo_hl_added.py [--apply]
"""
import re, sys, glob, html, argparse, difflib
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
ap.add_argument("--show", type=int, default=8)
A = ap.parse_args()

MARK = "/* 늘어난 자리만 색으로 짚는다 (2026-08-19) */"
CSS = MARK + """
.wo-ko em{font-style:normal;color:#6d28d9;}
.wo-now .wo-ko{color:#1f2430;}
.wo-steps li:only-child .wo-ko{color:#4c1d95;}
"""

stat = Counter()
work = {}
shown = 0

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    if 'class="wo-steps"' not in s0:
        continue
    s = s0
    for ol in list(re.finditer(r'<ol class="wo-steps">[\s\S]*?</ol>', s))[::-1]:
        blk = ol.group(0)
        kos = list(re.finditer(r'<span class="wo-ko">([\s\S]*?)</span>', blk))
        if len(kos) < 2:
            stat["한 단 — 그대로"] += 1
            continue
        # ★이름표에는 <em> 이 늘 있다. **문장 쪽**에 있는지를 봐야 한다.
        if any("<em>" in k.group(1) for k in kos):
            stat["이미 되어 있음"] += 1
            continue
        nb = blk
        for i in range(len(kos) - 1, 0, -1):
            prev = kos[i - 1].group(1).split()
            cur = kos[i].group(1).split()
            sm = difflib.SequenceMatcher(None, prev, cur, autojunk=False)
            ops = sm.get_opcodes()
            if any(t in ("replace", "delete") for t, *_ in ops):
                out.write(f"   · {f[:24]} {i+1}단 — 끼워 넣기가 아님, 건드리지 않음: "
                          f"{' '.join(cur)[:40]}\n")
                stat["끼워 넣기 아님"] += 1
                continue
            runs = [(j1, j2) for t, _, _, j1, j2 in ops if t == "insert"]
            if not runs:
                stat["늘어난 자리 없음"] += 1
                continue
            toks = list(cur)
            for j1, j2 in runs[::-1]:
                toks[j1:j2] = ["<em>" + " ".join(toks[j1:j2]) + "</em>"]
            nb = (nb[:kos[i].start(1)] + " ".join(toks) + nb[kos[i].end(1):])
            stat["짚음"] += 1
            if shown < A.show:
                shown += 1
                out.write(f"   [{f[:22]}] {' '.join(toks)}\n")
        if nb != blk:
            s = s[:ol.start()] + nb + s[ol.end():]

    if MARK not in s and s != s0:
        b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
        e = b[-1].end() - len("</style>")
        s = s[:e] + "\n" + CSS + s[e:]
        stat["CSS"] += 1
    if s != s0:
        work[f] = (s0, s); stat["파일"] += 1

# ── 검산
vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x)))
for f, (o0, s) in work.items():
    for tg in ("em", "span", "ol", "li", "div", "style"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write(f"   ★ CSS 중괄호 {f[:26]}\n"); stat["★"] += 1
    # 화면 글자는 하나도 바뀌면 안 된다 (스타일 안은 뺀다)
    strip = lambda x: re.sub(r"<style[^>]*>[\s\S]*?</style>", " ", x)
    if vis(strip(s)) != vis(strip(o0)):
        out.write(f"   ★ 보이는 글자가 바뀜 {f[:26]}\n"); stat["★"] += 1

if A.apply and not stat["★"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

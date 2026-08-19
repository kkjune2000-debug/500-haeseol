# -*- coding: utf-8 -*-
r"""만들기 줄의 왼쪽을 나머지와 맞춘다 (사용자 지적 2026-08-19)

  재어 보니 상자 왼쪽에서
    제목 · 한국어 문장 · 해석 · 「만들기」 이름표  →  +17px
    만들기 줄                                  →  +27px   ← 이것만 10px 안쪽
  `.wo-mk` 의 padding-left:10px 때문이다. 없앤다.
"""
import re, sys, glob, argparse
from collections import Counter

sys.path.insert(0, r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\_도구")
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

OLD = ".wo-mk{display:block;color:#8b8f9e;padding:2px 0 2px 10px;}"
NEW = ".wo-mk{display:block;color:#8b8f9e;padding:2px 0;}"

stat = Counter()
work = {}
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    n = s.count(OLD)
    if n == 0:
        if ".wo-mk{" in s:
            out.write(f"   X {f[:30]} 규칙은 있는데 글자가 다름\n"); stat["어긋남"] += 1
        continue
    if n != 1:
        out.write(f"   X {f[:30]} {n}곳\n"); stat["어긋남"] += 1; continue
    work[f] = (s, s.replace(OLD, NEW)); stat["파일"] += 1

for f, (o0, s) in work.items():
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write(f"   ★ CSS 중괄호 {f[:26]}\n"); stat["★"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

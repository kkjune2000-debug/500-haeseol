# -*- coding: utf-8 -*-
r"""「만들기 Word building」의 영어를 아래 줄로 (사용자 지적 2026-08-19)

  왜  상자 밖으로 넘치지는 않지만 폭이 빠듯하다 — 390px에서 본문 폭 228px 중
      스페인어 「Formación de palabras」가 들어가면 남는 자리가 12px뿐이고,
      그보다 길면 「만들기」와 번역어가 **한 줄에 섞인다**(재어 확인).
      같은 상자의 제목(.wo-title span)과 이름표(.wo-add small)는 이미 아래 줄이다.
      이 하나만 인라인이었다.

사용: python wolab_block.py [--apply]
"""
import re, sys, glob, argparse
from collections import Counter

sys.path.insert(0, r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\_도구")
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

OLD = ".wo-make .wo-lab small{font-weight:600;color:#7c66b8;margin-left:6px;}"
NEW = (".wo-make .wo-lab small{display:block;font-weight:600;color:#7c66b8;"
       "margin-left:0;margin-top:2px;}")

stat = Counter()
work = {}
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    n = s.count(OLD)
    if n == 0:
        if ".wo-make .wo-lab small" in s:
            out.write(f"   X {f[:30]} 규칙은 있는데 글자가 다름\n"); stat["어긋남"] += 1
        continue
    if n != 1:
        out.write(f"   X {f[:30]} {n}곳 (1이어야 함)\n"); stat["어긋남"] += 1; continue
    work[f] = (s, s.replace(OLD, NEW))
    stat["파일"] += 1

for f, (o0, s) in work.items():
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write(f"   ★ CSS 중괄호 {f[:26]}\n"); stat["★"] += 1
    if len(s) - len(o0) != len(NEW) - len(OLD):
        out.write(f"   ★ 길이 변화가 예상과 다름 {f[:26]}\n"); stat["★"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

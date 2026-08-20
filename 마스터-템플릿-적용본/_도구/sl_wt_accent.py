# -*- coding: utf-8 -*-
r"""따라 읽기·쓰기 시험을 「문장구조 2」 꼴로 — 왼쪽 강조선 (사용자 지시 2026-08-19)

  기준  3 011~020 문장구조 주어 동사.html
        .sentence-item{… border-left:4px solid <색>; padding:12px 18px 12px 14px;}
        .writing-item {… border-left:4px solid <색>; padding:16px 18px 16px 14px;}

  ★색은 **그 장의 색**을 쓴다. 책은 장마다 색이 다르다(파랑 36·호박 17·초록 9·
    청록 3·보라 3·분홍 1·남색 1 …). 초록으로 통일하면 그 짜임이 무너진다.
    색은 이미 그 파일에 있는 것에서 가져온다 —
      따라 읽기 : .sentence-item:hover 의 border-color
      쓰기 시험 : .writing-item:focus-within 의 border-color

  ★눈으로 견주어 알아낸 것 — 이것 말고 다른 차이는 없다.
    · 영어 줄 사이가 벌어져 보인 것은 오해였다(둘 다 line-height 30.5px, 2배 화면에 속았다).
    · nth-child 바탕색 수가 다른 것은 문항 수 차이일 뿐이다.
    · 기준 파일의 .writing-answer / .writing-show-btn 규칙은 **DOM 에 없는 죽은 CSS** 다.
      옮기면 잔재만 퍼진다 — 옮기지 않는다.

사용: python sl_wt_accent.py [--apply]
"""
import re, sys, glob, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

JOBS = [
    # 고칠 규칙, 색을 가져올 규칙, 옛 padding, 새 padding
    (".sentence-item", ".sentence-item:hover", "padding: 12px 18px;", "padding: 12px 18px 12px 14px;"),
    (".writing-item", ".writing-item:focus-within", "padding: 16px 18px;", "padding: 16px 18px 16px 14px;"),
]

stat = Counter()
work = {}


def rule(css, sel):
    """그 선택자의 { } 안을 (시작, 끝, 속내) 로"""
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        s = re.sub(r"^/\*[^*]*\*/\s*", "", re.sub(r"\s+", " ", m.group(1)).strip())
        if s == sel:
            return m.start(2), m.end(2), m.group(2)
    return None


for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    s = s0
    for target, colorfrom, oldpad, newpad in JOBS:
        # <style> 블록 안에서만 찾는다
        blocks = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
        done = False
        for b in blocks:
            css = b.group(1)
            r = rule(css, target)
            if not r:
                continue
            a, e, body = r
            if "border-left" in body:
                stat[f"{target} 이미 있음"] += 1; done = True; break
            cr = rule(css, colorfrom)
            if not cr:
                out.write(f"   X {f[:28]} {colorfrom} 없음 — 색을 못 가져옴\n")
                stat["어긋남"] += 1; done = True; break
            col = re.search(r"border-color\s*:\s*([^;]+)", cr[2])
            if not col:
                out.write(f"   X {f[:28]} {colorfrom} 에 border-color 없음\n")
                stat["어긋남"] += 1; done = True; break
            col = col.group(1).strip()
            if oldpad not in body:
                out.write(f"   X {f[:28]} {target} 의 padding 이 다름: "
                          f"{(re.search(r'padding[^;]*;', body) or ['?'])[0]}\n")
                stat["어긋남"] += 1; done = True; break
            # ★border-left 는 **맨 뒤**에 붙인다.
            #   이 파일들은 padding 이 border 보다 앞이라, padding 자리에 넣으면
            #   뒤에 오는 `border: 1px solid …` 축약이 되돌려 버린다(재어서 들켰다).
            nb = body.replace(oldpad, newpad).rstrip()
            if not nb.endswith(";"):
                nb += ";"
            nb += f" border-left: 4px solid {col};"
            s = s[:b.start(1) + a] + nb + s[b.start(1) + e:]
            stat[f"{target} 넣음"] += 1
            done = True
            break
        if not done:
            stat[f"{target} 규칙 없음"] += 1
    if s != s0:
        work[f] = (s0, s)

# ── 검산
for f, (o0, s) in work.items():
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write(f"   ★ CSS 중괄호 {f[:26]}\n"); stat["★"] += 1
    if len(s) <= len(o0):
        out.write(f"   ★ 길이가 안 늘었다 {f[:26]}\n"); stat["★"] += 1
    if re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s) != \
       re.sub(r"<style[^>]*>[\s\S]*?</style>", "", o0):
        out.write(f"   ★ 스타일 밖이 바뀌었다 {f[:26]}\n"); stat["★"] += 1
    stat["파일"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

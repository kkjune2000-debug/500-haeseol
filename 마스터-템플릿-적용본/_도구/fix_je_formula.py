# -*- coding: utf-8 -*-
r"""「제 = 저의」 공식 상자 — 보기를 한 줄에 하나씩 (사용자 지시 2026-08-19)

  전  저 = I → 제 = my
      제 전공 (my major) · 제 고향 (my hometown) · 제 취미 (my hobby) · 제 노트북 (my laptop)

  후  저 = I → 제 = my
      제 전공        제 고향        제 취미        제 노트북
      my major       my hometown    my hobby       my laptop
      (각각 한 줄씩 · 한국어 위 · 영어 아래)

사용: python fix_je_formula.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

MARK = "/* 공식 상자의 보기 — 한 줄에 하나씩 (2026-08-19) */"
CSS = MARK + """
.gp-ex{margin-top:8px;}
.gp-ex > span{display:block;margin-top:7px;line-height:1.45;}
.gp-ex b{display:block;font-weight:800;color:#4c1d95;}
.gp-ex small{display:block;font-weight:600;color:#636976;font-size:0.84em;margin-top:1px;}
"""

EX = [("제 전공", "my major"), ("제 고향", "my hometown"),
      ("제 취미", "my hobby"), ("제 노트북", "my laptop")]

s0 = io.open(P, encoding="utf-8").read()

# ★닫는 </small> 까지 함께 잡는다. 안 그러면 짝을 맞추려고 빈 <small> 을
#   남겨야 해서 지저분해진다.
m = re.search(r"<br>\s*<strong>\s*<span lang=\"ko\" translate=\"no\">제 전공</span>"
              r"[\s\S]*?\(my laptop\)\s*</small>", s0)
assert m, "보기 줄을 못 찾음"
print("   전  " + vis(m.group(0)))

new = ('</small>\n<div class="gp-ex">'
       + "".join(f'<span><b>{k}</b>'
                 f'<small lang="en" translate="yes">{e}</small></span>' for k, e in EX)
       + '</div>')
s = s0[:m.start()] + new + s0[m.end():]

for tg in ("small", "span", "strong", "div", "b"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"

if MARK not in s:
    b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
    e = b[-1].end() - len("</style>")
    s = s[:e] + "\n" + CSS + s[e:]

for k, e in EX:
    assert k in s and e in s, f"낱말이 사라짐 {k} {e}"
mm = re.search(r'<div class="gp-ex">[\s\S]*?</div>', s)
print("   후  " + vis(mm.group(0)))
print("\n■ 검산 통과")
if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

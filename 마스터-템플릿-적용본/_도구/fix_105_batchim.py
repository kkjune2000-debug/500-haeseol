# -*- coding: utf-8 -*-
r"""105~114 받침 표 다듬기 (사용자 지시 2026-08-19)

  ① 받침 열 — 「없음 X」·「있음 O」에서 한국어를 빼고 **X · O 만** 남깁니다.
  ② 「존댓말 / polite」 → 「격식체 / formal」.
     보이는 꼴이 「갈 수 있습니다」이므로 격식체가 맞고, 이 책의 문체 규칙과도 맞습니다.
  ③ 색을 파스텔로 — 진한 #c62020·#107435 를 이 책이 이미 쓰는
     #9f1239(장미)·#166534(초록)로 낮춥니다. 두 색 다 다른 쪽에서 쓰던 것입니다.
  ④ 알약을 깔끔하게 — 옅은 바탕 + 가는 테두리, 한 글자라 가운데 맞춤.

  ★#c62020·#107435 는 이 장의 다른 표에서도 「안 됨 / 됨」 표시로 씁니다
    (X 사용 불가 · O 완전 동의어 · .ng-mark). 뜻이 같으므로 함께 낮춥니다.

사용: python fix_105_batchim.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 105~114 서술어 문법 능력 가능.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

PILL = ("display:inline-block;min-width:28px;padding:2px 9px;border-radius:999px;"
        "font-weight:800;font-size:0.82rem;text-align:center;")
OLD_X = ('<span style="display:inline-block;padding:2px 9px;border-radius:999px;'
         'background:#fee2e2;color:#c62020;font-weight:800;font-size:0.8rem;">없음 X</span>')
NEW_X = (f'<span style="{PILL}background:#fff1f2;border:1px solid #fecdd3;'
         'color:#9f1239;">X</span>')
OLD_O = ('<span style="display:inline-block;padding:2px 9px;border-radius:999px;'
         'background:#dcfce7;color:#107435;font-weight:800;font-size:0.8rem;">있음 O</span>')
NEW_O = (f'<span style="{PILL}background:#f0fdf4;border:1px solid #bbf7d0;'
         'color:#166534;">O</span>')

s0 = io.open(P, encoding="utf-8").read()
s = s0

# ① 알약
nx, no = s.count(OLD_X), s.count(OLD_O)
assert nx == 3 and no == 2, f"알약 X {nx}개 · O {no}개 (3·2 여야 함)"
s = s.replace(OLD_X, NEW_X).replace(OLD_O, NEW_O)

# ② 존댓말 → 격식체
a = ('<th>존댓말<br>\n<small style="font-weight:600;" lang="en" translate="yes">'
     'polite</small>\n</th>')
if a not in s:
    m = re.search(r"<th>존댓말[\s\S]*?</th>", s)
    assert m, "존댓말 머리칸을 못 찾음"
    a = m.group(0)
b = a.replace("존댓말", "격식체").replace(">polite<", ">formal<")
assert b != a, "존댓말/polite 를 못 바꿈"
s = s.replace(a, b, 1)

# ③ 색 낮추기
n1, n2 = s.count("#c62020"), s.count("#107435")
s = s.replace("#c62020", "#9f1239").replace("#107435", "#166534")

# ── 검산
for tg in ("span", "th", "td", "tr", "table", "div", "small", "strong"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
assert "없음 X" not in s and "있음 O" not in s, "옛 알약이 남음"
assert "#c62020" not in s and "#107435" not in s, "옛 색이 남음"
assert s.count(">X<") >= 3 and s.count(">O<") >= 2

print(f"■ 알약 X {nx}개 · O {no}개 → 한 글자로")
print(f"■ 존댓말/polite → 격식체/formal")
print(f"■ 색 #c62020 {n1}곳 → #9f1239 · #107435 {n2}곳 → #166534")
if APPLY:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

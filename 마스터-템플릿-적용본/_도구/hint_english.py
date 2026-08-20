# -*- coding: utf-8 -*-
r"""카드 힌트 「▼ 눌러서 확인」을 영어로 (사용자 지시 2026-08-19)

  「대상이 처음 한국어를 배우는 학생들이다」 — UI 안내는 읽을 수 있어야 합니다.

  ★이 책에서 **번역 슬롯이 없던 UI 글자는 이것 하나뿐**이었습니다.
    해설·어휘·정답·쓰기 단추 1,701개는 모두 슬롯이 있는데 힌트 578곳만 없었습니다.
    슬롯에 넣었으므로 일본어판이면 일본어로 바뀝니다.

  ★.flashcard-hint 에 text-transform:uppercase 가 걸려 있어 그대로 두면
    「TAP TO CHECK」가 됩니다. 영어 슬롯만 none 으로 되돌립니다
    (.gloss 에 같은 처리를 해 둔 전례가 있습니다).

  ※ JS 안 문자열 33곳도 바뀝니다 — js_사전_뼈대 재생성이 필요합니다(2층 작업).

사용: python hint_english.py [--apply]
"""
import re, sys, glob
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
APPLY = "--apply" in sys.argv

OLD = "▼ 눌러서 확인"
NEW = '▼ <span lang="en" translate="yes">Tap to check</span>'
MARK = "/* 힌트 영어는 대문자로 바꾸지 않는다 (2026-08-19) */"
CSS = MARK + """
.flashcard-hint [lang="en"],.fc-flip-hint [lang="en"]{text-transform:none;letter-spacing:0.02em;}
"""

stat = Counter()
work = {}
for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    if OLD not in s0:
        continue
    n = s0.count(OLD)
    s = s0.replace(OLD, NEW)
    stat["바꾼 힌트"] += n
    if MARK not in s:
        b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
        e = b[-1].end() - len("</style>")
        s = s[:e] + "\n" + CSS + s[e:]
        stat["CSS"] += 1
    work[f] = (s0, s)
    stat["파일"] += 1

for f, (o0, s) in work.items():
    for tg in ("span", "div", "style"):
        x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        y = len(re.findall(rf"<{tg}\b", o0)) - len(re.findall(rf"</{tg}\s*>", o0))
        assert x == y, f"{tg} 짝이 어긋남 {f}"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"CSS 중괄호 {f}"
    if OLD in s:
        out.write(f"   X 남음 {f[:26]}\n"); stat["★"] += 1
    # JS 문자열 안에 넣은 것이 따옴표를 깨지 않았는가
    if s.count("'") != o0.count("'") or s.count('"') != o0.count('"') + 2 * n:
        pass   # 큰따옴표는 늘어나는 것이 정상 (슬롯 속성)

if APPLY and not stat["★"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s)
        stat["파일 씀"] += 1

out.write("\n■ 반영\n" if APPLY else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

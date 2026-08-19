# -*- coding: utf-8 -*-
r"""「대표 악기」 표 마지막 칸의 개조식을 문장으로 (사용자 지시 2026-08-20).

    python instr_note_sentence.py [--apply]

전  모든 악기에 사용 가능 — 피아노를 연주하다, 바이올린을 연주하다 등
후  모든 악기에 씁니다.
    예: 피아노를 연주하다 · 바이올린을 연주하다 등
    Works with any instrument

왜
    설명·서술은 **격식체 문장**입니다(인수인계 §5 문체). 「사용 가능」은 명사로 끝나는
    조각이라 그 규칙에 어긋났습니다. 오늘 300~306·362~365 를 고친 것과 같은 갈래입니다.

★ 「예:」는 이 책이 이미 쓰는 꼴입니다(366~369 「예: 비가 오는데 우산…」).
★ 보기를 가르는 쉼표를 가운뎃점으로 바꿨습니다 — 이 책은 낱말을 나열할 때
  가운뎃점을 씁니다(인수인계 §5 「가운뎃점의 세 용도」 가운데 항목 구분).
★ 한 줄에 한국어 한 문장 — 설명과 보기를 두 줄로 나눴습니다.
★ 영어 줄은 그대로 맨 아래에 둡니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 123~141 서술어 문법 부정.html")
APPLY = "--apply" in sys.argv

OLD = ('모든 악기에 사용 가능 — <strong>피아노를 연주하다</strong>, '
       '<strong>바이올린을 연주하다</strong> 등')
NEW = ('모든 악기에 씁니다.<br>예: <strong>피아노를 연주하다</strong> · '
       '<strong>바이올린을 연주하다</strong> 등')

s0 = io.open(P, encoding="utf-8", newline="").read()
n = s0.count(OLD)
print(f"■ 닻 {n}개 (1이어야 합니다)")
assert n == 1, "닻이 하나가 아닙니다"
s = s0.replace(OLD, NEW, 1)

vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
v, v0 = vis(s), vis(s0)
assert "모든 악기에 씁니다." in v, "문장이 안 들어갔습니다"
assert "사용 가능" not in v, "개조식이 남았습니다"
assert v.count("피아노를 연주하다") == v0.count("피아노를 연주하다"), "보기가 바뀌었습니다"
assert v.count("Works with any instrument") == 1, "영어가 바뀌었습니다"
for tg in ("strong", "span", "small", "em", "td", "br"):
    if tg == "br":
        assert s.count("<br>") == s0.count("<br>") + 1, "<br> 가 하나만 늘어야 합니다"
        continue
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"<{tg}> 짝이 어긋남"
assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n"), "홑 LF"
print("■ 검산 통과 — 문장 · 보기 그대로 · 영어 그대로 · 태그 짝 · 줄끝")

if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

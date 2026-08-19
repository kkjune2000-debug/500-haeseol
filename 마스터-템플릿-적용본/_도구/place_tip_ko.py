# -*- coding: utf-8 -*-
r"""157~163 「📍 장소」 상자의 💡 줄 — 한국어 위 · 영어 아래 (사용자 지시 2026-08-20).

    python place_tip_ko.py [--apply]

전  💡 With motion verbs (가다, 오다, 다니다): place + 에 · with action verbs at a place: place + 에서
    → 영어 문장 안에 한국어가 섞여 있고, **한국어 설명이 없습니다.**

후  💡 움직임을 나타내는 동사(가다 · 오다 · 다니다) 앞에서는 장소 + 에를 씁니다.
       With motion verbs (가다 · 오다 · 다니다): place + 에
       그 자리에서 하는 일을 말할 때는 장소 + 에서를 씁니다.
       With action verbs at a place: place + 에서

★ 「한 줄에 한국어 한 문장」을 지켜 두 문장을 두 줄로 나눴습니다.
★ 영어 줄 안의 한국어는 <span lang="ko" translate="no"> 로 잠갔습니다.
★ 문법 용어를 늘어놓지 않았습니다 — 「이동 동사」가 아니라 「움직임을 나타내는 동사」.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 157~163 서술어 문법 계획.html")
APPLY = "--apply" in sys.argv

OLD = ('💡 <span lang="en" translate="yes">With motion verbs</span> '
       '(<strong><span lang="ko" translate="no">가다</span></strong>, '
       '<strong><span lang="ko" translate="no">오다</span></strong>, '
       '<strong><span lang="ko" translate="no">다니다</span></strong>)'
       '<span lang="en" translate="yes">: place +</span> <strong>에</strong> '
       '<span lang="en" translate="yes">&nbsp;·&nbsp; with action verbs at a place: '
       'place +</span> <strong>에서</strong>')

EN = '<small class="en-line" lang="en" translate="yes"><em>%s</em></small>'
KO = lambda t: f'<span lang="ko" translate="no">{t}</span>'

NEW = ('💡 움직임을 나타내는 동사(<strong>가다</strong> · <strong>오다</strong> · '
       '<strong>다니다</strong>) 앞에서는 장소 + <strong>에</strong>를 씁니다.<br>'
       + EN % (f'With motion verbs ({KO("가다 · 오다 · 다니다")}): place + {KO("에")}')
       + '<br>그 자리에서 하는 일을 말할 때는 장소 + <strong>에서</strong>를 씁니다.<br>'
       + EN % f'With action verbs at a place: place + {KO("에서")}')

s0 = io.open(P, encoding="utf-8", newline="").read()
n = s0.count(OLD)
print(f"■ 닻 {n}개 (1이어야 합니다)")
assert n == 1, "닻이 하나가 아닙니다 — 상자가 바뀌었는지 보십시오"
s = s0.replace(OLD, NEW, 1)

vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
v = vis(s)
assert "움직임을 나타내는 동사" in v and "씁니다" in v, "한국어가 안 들어갔습니다"
assert v.count("With motion verbs") == 1 and v.count("With action verbs") == 1, "영어가 늘었습니다"
assert ".en-line" in "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s)), \
    "이 파일에 .en-line 규칙이 없습니다"
for tg in ("span", "strong", "small", "em", "div"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"<{tg}> 짝이 어긋남"
assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n"), "홑 LF"
print("■ 검산 통과 — 한국어 두 문장 · 영어 그대로 · 태그 짝 · 줄끝")

if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

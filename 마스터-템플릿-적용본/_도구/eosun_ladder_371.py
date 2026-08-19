# -*- coding: utf-8 -*-
r"""371 사다리 구멍 메우기 — 뼈대가 바로 앞 문항(370)에 있습니다.

    python eosun_ladder_371.py [--apply]

무엇을
    371) 이 사과는 수박처럼 큽니다.   ← 한 단이었습니다
    →   ① 이 사과는 큽니다.            (교재 370 문장 그대로)
        ② 이 사과는 수박처럼 큽니다.

왜
    같은 파일 372 가 이미 이 꼴입니다 — 「이 사과는 더 큽니다」 → 「이 사과는 수박보다
    더 큽니다」. 371 만 한 단이라 짝이 어긋나 있었습니다. 사다리 규칙 ㉠(교재가 앞
    문장을 가진 곳)과 ㉡(부사어만 빼면 뼈대가 되는 곳)을 **둘 다** 채웁니다.

★ 새로 지은 문장이 없습니다 — 1단은 교재 370 의 한국어·영어를 그대로 씁니다.
★ 꼴은 같은 파일 372 를 본으로 삼았습니다(이름표의 <em>, 늘어난 자리를 문장에서도
  <em> 으로 짚기, 마지막 단에 wo-now).
★ 만들기 줄은 건드리지 않습니다 — 만들기는 「자리마다 한 줄」이 아니라 **만들 것이
  있는 조각만** 보이는 자리입니다(223·249·273 을 열어 확인했습니다).
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 370~383 기타 문법 비교급 최상급.html")
APPLY = "--apply" in sys.argv

OLD = ('<ol class="wo-steps">\n'
       '<li class="wo-now"><span class="wo-ko">이 사과는 수박처럼 큽니다.</span>'
       '<span class="wo-en" lang="en" translate="yes">This apple is as big as a watermelon.</span></li>\n'
       '</ol>')

NEW = ('<ol class="wo-steps">\n'
       '<li><span class="wo-add">주어 + 서술어(형용사)'
       '<small lang="en" translate="yes">Subject + Predicate (Adjective)</small></span>'
       '<span class="wo-ko">이 사과는 큽니다.</span>'
       '<span class="wo-en" lang="en" translate="yes">This apple is big.</span></li>\n'
       '<li class="wo-now"><span class="wo-add">주어 + <em>부사어(비교)</em> + 서술어(형용사)'
       '<small lang="en" translate="yes">Subject + <em>Adverbial (Comparison)</em> + '
       'Predicate (Adjective)</small></span>'
       '<span class="wo-ko">이 사과는 <em>수박처럼</em> 큽니다.</span>'
       '<span class="wo-en" lang="en" translate="yes">This apple is as big as a watermelon.</span></li>\n'
       '</ol>')

s0 = io.open(P, encoding="utf-8", newline="").read()
n = s0.count(OLD.replace("\n", "\r\n")) + s0.count(OLD)
print(f"■ 371 의 한 단 사다리를 찾았습니다 — {n}곳 (1이어야 합니다)")
assert n == 1, "닻이 하나가 아닙니다. 파일이 바뀌었는지 보십시오."

# 이 책의 줄끝(CRLF)을 그대로 지킵니다
crlf = "\r\n" in s0
old = OLD.replace("\n", "\r\n") if crlf else OLD
new = NEW.replace("\n", "\r\n") if crlf else NEW
s = s0.replace(old, new, 1)

# ── 검산
for tg in ("li", "ol", "span", "small", "em", "div"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"<{tg}> 짝이 어긋남"
assert s.count('class="wo-now"') == s0.count('class="wo-now"'), "wo-now 수가 달라짐"

def vis(x):
    """화면 글자 — <style>·<script> 를 먼저 지우고 태그는 빈 문자열로.
    ★문장 안에 <em> 을 끼우므로 **원본 글자로 세면 0이 됩니다.** 화면 글자로 세십시오."""
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x))


v, v0 = vis(s), vis(s0)
assert v.count("이 사과는 수박처럼 큽니다.") == v0.count("이 사과는 수박처럼 큽니다."), \
    "2단 문장이 늘거나 줄었습니다"
assert v.count("이 사과는 큽니다.") == v0.count("이 사과는 큽니다.") + 1, \
    "1단 문장이 정확히 하나 늘지 않았습니다"
assert v.count("This apple is big.") == v0.count("This apple is big.") + 1, \
    "1단 영어가 정확히 하나 늘지 않았습니다"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"

print("■ 검산 통과 — 태그 짝 · wo-now 수 · CSS 중괄호")
if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 371 이 두 단이 되었습니다 (370 문장을 그대로 씁니다)")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

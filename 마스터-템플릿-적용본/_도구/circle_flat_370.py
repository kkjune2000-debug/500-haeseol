# -*- coding: utf-8 -*-
r"""370~383 「관계」 표 — 동그라미는 두고 그러데이션만 걷습니다 (사용자 결정 2026-08-20).

    python circle_flat_370.py [--apply]

무엇을
    = · &gt; · &lt; 를 담은 42×42 동그라미 셋의 바탕만 바꿉니다.
        전  background:linear-gradient(135deg,#fde68a,#fcd34d)
        후  background:#fffbeb; border:1px solid #fde68a
    모양(동그라미·크기·글자)은 그대로입니다 — 그 그림이 비교급·최상급의 관계를
    한눈에 보이는 자리라 사용자가 남기기로 정했습니다.

왜 이 두 색인가
    새 색을 만들지 않았습니다. **이 책의 어휘 카드가 이미 쓰는 짝**입니다
    (`.vocab-box .v-item{border:1px solid #fde68a; background:#fffbeb}`).
    2026-08-19 받침 X·O 알약을 「옅은 바탕 + 가는 테두리」로 바꾼 것과 같은 꼴입니다.

★ 테두리를 더하면 상자가 2px 커집니다 — `box-sizing:border-box` 를 함께 넣어
  42×42 를 지킵니다(안 넣으면 세 동그라미만 다른 표보다 커집니다).
★ 화면 글자는 바뀌지 않습니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 370~383 기타 문법 비교급 최상급.html")
APPLY = "--apply" in sys.argv

OLD = ("display:inline-flex;align-items:center;justify-content:center;width:42px;"
       "height:42px;border-radius:50%;background:linear-gradient(135deg,#fde68a,#fcd34d);"
       "color:#92400e;font-size:1.5rem;font-weight:900;line-height:1;")
NEW = ("display:inline-flex;align-items:center;justify-content:center;width:42px;"
       "height:42px;box-sizing:border-box;border-radius:50%;background:#fffbeb;"
       "border:1px solid #fde68a;color:#92400e;font-size:1.5rem;font-weight:900;"
       "line-height:1;")


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()


s0 = io.open(P, encoding="utf-8", newline="").read()
n = s0.count(OLD)
print(f"■ 동그라미 {n}개 (셋이어야 합니다)")
assert n == 3, f"셋이어야 합니다(찾은 것 {n})"
s = s0.replace(OLD, NEW)

assert vis(s) == vis(s0), "화면 글자가 바뀌었습니다"
assert "linear-gradient" not in re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s), \
    "본문에 그러데이션이 남았습니다"
for tg in ("span", "td", "tr", "table"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"<{tg}> 짝이 어긋남"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
print("■ 검산 통과 — 화면 글자 · 태그 짝 · CSS 중괄호 · 본문 그러데이션 0")

if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 동그라미는 그대로, 바탕만 한 색으로")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

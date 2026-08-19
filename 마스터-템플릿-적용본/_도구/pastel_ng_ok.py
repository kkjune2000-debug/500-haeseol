# -*- coding: utf-8 -*-
r"""「안 됨 · 됨」 표시의 진한 빨강·초록을 파스텔로 — 어제 105~114 에서 정한 것을 넓힙니다.

    python pastel_ng_ok.py            # 모의 실행(셈만)
    python pastel_ng_ok.py --apply
    python pastel_ng_ok.py --from 1   # 구간을 넓히려면

무엇을 바꾸는가
    #c62020 (진한 빨강) → #9f1239 (장미)
    #107435 (진한 초록) → #166534 (초록)

왜
    2026-08-19 사용자 지시로 「3 105~114」 에서 이 둘을 낮췄습니다. 그때 적어 둔 까닭이
    그 파일에만 해당하지 않습니다 — **두 색은 책 어디서나 「안 됨 / 됨」 한 가지 뜻**으로
    쓰이고(✅/❌ · X/O · 없음/있음 · 취소선 틀린 꼴), 바꿔 넣는 두 색은 **이 책이 이미
    쓰던 색**이라 책 안에서 새 색이 늘지 않습니다. 규칙 지시는 한 파일이 아니라
    같은 꼴 전부에 미칩니다(인수인계 §8 · 메모리 haeseol-jisi-jeonpail).

★ 글자색으로만 씁니다 — 2026-08-20 전수 확인: 459곳 모두 `color:` 이고 배경으로 쓰인
  곳은 0입니다. 그래서 바탕과 글자가 같아지는 사고(2026-08-15)가 날 수 없습니다.

★ 화면 글자는 한 글자도 바뀌지 않습니다. 그것을 파일마다 검산합니다.
"""
import io, os, re, sys, glob, argparse, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

MAP = {"#c62020": "#9f1239", "#107435": "#166534"}
TAGS = ("span", "th", "td", "tr", "table", "div", "small", "strong", "em", "s", "li", "ul")


def vis(x):
    """화면 글자 — 태그는 **빈 문자열**로 지웁니다(공백으로 바꾸면 헛차이가 납니다).

    ★`<style>`·`<script>` 속은 **먼저 통째로 지웁니다.** 태그만 걷어내면 CSS 선언이
      글자로 남아, 색을 바꿀 때마다 「화면 글자가 바뀌었다」는 헛경보가 납니다
      (2026-08-20에 실제로 걸렸습니다).
    """
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    x = re.sub(r"<!--[\s\S]*?-->", "", x)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


def rng(name):
    m = re.match(r"3 (\d{3})~(\d{3})", name)
    return (int(m.group(1)), int(m.group(2))) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--from", dest="lo", type=int, default=100)
    A = ap.parse_args()

    todo, skipped = [], []
    for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        name = os.path.basename(p)
        r = rng(name)
        # ★newline="" 로 읽습니다 — 이 책의 파일은 CRLF 입니다. 그냥 읽으면 파이썬이
        #   \r\n 을 \n 으로 바꿔 주고, 그대로 쓰면 그 파일만 LF 가 되어 작업본이
        #   뒤섞입니다(2026-08-20에 37파일을 그렇게 만들었다가 되돌렸습니다).
        s = io.open(p, encoding="utf-8", newline="").read()
        n = sum(s.count(k) for k in MAP)
        if not n:
            continue
        if not r or r[1] < A.lo:
            skipped.append((name, n))
            continue
        todo.append((p, name, s, n))

    tot = sum(n for *_, n in todo)
    print(f"■ 바꿀 파일 {len(todo)}개 · {tot}곳  (구간 {A.lo}~500)")
    for _, name, _, n in todo:
        print(f"     {n:>4}  {name}")
    if skipped:
        print(f"\n■ 구간 밖이라 두는 파일 {len(skipped)}개 · "
              f"{sum(n for _, n in skipped)}곳")
        for name, n in skipped:
            print(f"     {n:>4}  {name}")

    if not A.apply:
        print("\n※ 모의 실행입니다. 반영하려면 --apply")
        return

    done = 0
    for p, name, s0, n in todo:
        s = s0
        for k, v in MAP.items():
            s = s.replace(k, v)
        # ── 검산 (쓰기 직전)
        assert vis(s) == vis(s0), f"{name}: 화면 글자가 바뀌었습니다"
        for tg in TAGS:
            a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert a == b, f"{name}: <{tg}> 짝이 어긋남"
        css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
        assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
        assert not any(k in s for k in MAP), f"{name}: 옛 색이 남음"
        assert len(s) == len(s0), f"{name}: 길이가 달라짐(색 길이는 같아야 합니다)"
        io.open(p, "w", encoding="utf-8", newline="").write(s)
        done += n
    print(f"\n■ 반영했습니다 — {len(todo)}파일 {done}곳")
    print("   화면 글자 대조 · 태그 짝 · CSS 중괄호 · 길이, 파일마다 통과했습니다.")


if __name__ == "__main__":
    main()

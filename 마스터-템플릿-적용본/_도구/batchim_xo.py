# -*- coding: utf-8 -*-
r"""받침 칸을 「X · O」 알약 하나로 — 어제 105~114 에서 정한 것을 100~500 으로 넓힙니다.

    python batchim_xo.py            # 모의 실행
    python batchim_xo.py --apply
    python batchim_xo.py --only "3 115~122"   # 한 파일만 (먼저 눈으로 보고 싶을 때)

무엇을
    표의 **받침 열**에 있는 칸을 이 하나로 바꿉니다.
        <span 알약>X</span>      (없음)
        <span 알약>O</span>      (있음)
    아래 붙어 있던 「없음 / none」·「있음 / yes」 줄은 뺍니다 — X·O 는 어느 언어에서나
    같아서 옮길 것이 없고, 어제 105~114 에서 사용자가 그렇게 정했습니다.

지금 책에 있는 두 가지 꼴 (2026-08-20 확인)
    ㉮ 알약이 이미 X·O 이고 아래에 「없음 none」 이 붙어 있음
    ㉯ 알약이 「없음」이고 아래에 「none」 만 붙어 있음

★ 받침 열만 봅니다 — 그 표의 머리줄(<th>)에 「받침」이 있어야 하고, 칸 안에 알약
  하나(+아래 줄) 말고 다른 것이 있으면 건드리지 않습니다.
★ 알약 모양은 어제 쓴 그대로입니다 — 옅은 바탕 + 가는 테두리, 한 글자라 가운데.
★ 이 책의 파일은 CRLF 입니다. newline="" 로 읽고 씁니다.
"""
import io, os, re, sys, glob, argparse, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

PILL = ("display:inline-block;min-width:28px;padding:2px 9px;border-radius:999px;"
        "font-weight:800;font-size:0.82rem;text-align:center;")
NEW = {
    "X": f'<span style="{PILL}background:#fff1f2;border:1px solid #fecdd3;color:#9f1239;">X</span>',
    "O": f'<span style="{PILL}background:#f0fdf4;border:1px solid #bbf7d0;color:#166534;">O</span>',
}
MARK = {"없음": "X", "있음": "O", "X": "X", "O": "O"}

TABLE = re.compile(r"<table[\s\S]*?</table>")
TD = re.compile(r"<td[^>]*>([\s\S]*?)</td>")
# 칸이 「알약 + (아래 줄)」 꼴인가 — 아래 줄의 생김새는 책 안에 세 가지가 있습니다
CELL = re.compile(r'^\s*<span[^>]*>\s*(없음|있음|X|O)\s*</span>([\s\S]*)$')
# 아래 줄이 알약과 **같은 말**을 되풀이할 때만 뗍니다
ECHO = {"없음", "있음", "none", "yes", "없음 none", "있음 yes",
        "없음none", "있음yes", "x", "o"}


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


def rng(name):
    m = re.match(r"3 (\d{3})~(\d{3})", name)
    return (int(m.group(1)), int(m.group(2))) if m else None


def convert(s):
    """바꾼 글자와 (바꾼 수, 뗀 아래줄 수) 를 냅니다."""
    n = subs = 0
    out, last = [], 0
    for tm in TABLE.finditer(s):
        head = " ".join(re.findall(r"<th[\s\S]*?</th>", tm.group(0)))
        if "받침" not in vis(head):
            continue
        tbl, moved = tm.group(0), []
        for cm in TD.finditer(tbl):
            inner = cm.group(1)
            m = CELL.match(inner)
            if not m:
                continue
            mark, tail = MARK[m.group(1)], m.group(2)
            tail_txt = vis(tail).lower()
            if tail_txt and tail_txt not in ECHO:
                # ★아래 줄이 다른 말을 합니다(「모음 끝」·「자음 끝」) — 남깁니다.
                #   알약만 X·O 로 바꾸고 그 줄은 그대로 둡니다.
                rep = NEW[mark] + tail
            else:
                rep = NEW[mark]
                if tail.strip():
                    subs += 1
            if rep == inner:
                continue
            moved.append((cm.start(1), cm.end(1), rep))
            n += 1
        if not moved:
            continue
        new_tbl, p = [], 0
        for a, b, rep in moved:
            new_tbl.append(tbl[p:a]); new_tbl.append(rep); p = b
        new_tbl.append(tbl[p:])
        out.append(s[last:tm.start()]); out.append("".join(new_tbl))
        last = tm.end()
    out.append(s[last:])
    return "".join(out), n, subs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--from", dest="lo", type=int, default=100)
    ap.add_argument("--only", default=None)
    A = ap.parse_args()

    tot = totsub = 0
    hits = []
    for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        name = os.path.basename(p)
        r = rng(name)
        if not r or r[1] < A.lo:
            continue
        if A.only and not name.startswith(A.only):
            continue
        s0 = io.open(p, encoding="utf-8", newline="").read()
        s, n, subs = convert(s0)
        if not n:
            continue
        # ── 검산
        v, v0 = vis(s), vis(s0)
        for w in ("없음", "있음", "none", "yes"):
            assert v.count(w) <= v0.count(w), f"{name}: {w} 가 늘었습니다"
        # ★<br> 는 닫는 태그가 없는 빈 태그라 짝으로 세면 안 됩니다 — 아래 줄을 뗀
        #   수만큼 줄어드는 것이 정상이므로 따로 셉니다.
        assert s0.count("<br>") - s.count("<br>") == subs, \
            f"{name}: <br> 가 뗀 아래줄 수({subs})만큼 줄지 않았습니다"
        for tg in ("span", "td", "tr", "table", "small", "em"):
            a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert a == b, f"{name}: <{tg}> 짝이 어긋남"
        assert s.count("<td") == s0.count("<td"), f"{name}: 칸 수가 달라짐"
        css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
        assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
        hits.append((p, name, s, n, subs))
        tot += n
        totsub += subs

    print(f"■ 받침 칸 {tot}곳 / {len(hits)}파일  (그중 아래 줄을 떼는 것 {totsub}곳)")
    for _, name, _, n, subs in hits:
        print(f"     {n:>3}곳 (아래줄 {subs})  {name}")
    if not A.apply:
        print("\n※ 모의 실행입니다. 반영하려면 --apply")
        return
    for p, _, s, _, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print(f"\n■ 반영했습니다 — {len(hits)}파일 {tot}곳")


if __name__ == "__main__":
    main()

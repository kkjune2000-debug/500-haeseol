# -*- coding: utf-8 -*-
r"""프로그램이 자리를 못 찾은 상자 가운데 **정말 틀린 일곱**을 손으로 (2026-08-19)

  vocab_order_ko2.py 가 24상자를 「자리를 모르겠다」며 건드리지 않았습니다.
  전수로 보니 그 가운데 17상자는 이미 한국어 차례였고, 일곱만 틀렸습니다.

    201  부르다 · 노래 · 저에게        → 저에게 · 노래 · 부르다   (르 불규칙: 부르 → 불러)
    462  (말)하다 · 날씨 · 덥다        → 날씨 · 덥다 · (말)하다   (괄호로 시작해 못 찾음)
    494  증조할머니 · 죽다 · 오늘 아침    → 오늘 아침 · 증조할머니 · 죽다  (죽다 → 돌아가셨)
    497  선생님 · 만나다 · 내일        → 내일 · 선생님 · 만나다   (만나다 → 뵈려고)
    498  할머니 · 아프다 · 요즘        → 요즘 · 할머니 · 아프다   (아프다 → 편찮으십니다)
    326  비 + 오다 · ~세요 · 퇴근하다    → 비 + 오다 · 퇴근하다 · ~세요
    327  비 + 오다 · ~ㅂ/읍시다 · 퇴근하다 → 비 + 오다 · 퇴근하다 · ~ㅂ/읍시다

  ★높임말은 낱말이 통째로 바뀌어(죽다→돌아가시다·아프다→편찮으시다) 글자로는
    영영 못 찾습니다. 그런 자리는 사람이 정하는 것이 맞습니다.

사용: python vocab_order_ko3.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

# 문항 → 바라는 표제어 차례
WANT = {
    "201": ["저에게", "노래", "부르다 (르 불규칙)"],
    "462": ["날씨", "덥다", "(말)하다"],
    "494": ["오늘 아침", "증조할머니", "죽다"],
    "497": ["내일", "선생님", "만나다"],
    "498": ["요즘", "할머니", "아프다"],
    "326": ["비 + 오다", "퇴근하다", "~ㅂ/읍시다"],
    "327": ["비 + 오다", "퇴근하다", "~세요"],
}


def spans(blk):
    got = []
    for im in re.finditer(r'<span class="v-item[^"]*">', blk):
        d, i = 1, im.end()
        while d and i < len(blk):
            t = re.compile(r"</?span\b").search(blk, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        gt = blk.find(">", i - 1)
        got.append((im.start(), gt + 1 if gt >= 0 else i))
    return got


done = set()
for f in sorted(glob.glob("*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for num, want in WANT.items():
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="v-list">[\s\S]*?</div>)', s)
        if not m:
            continue
        blk = m.group(1)
        sp = spans(blk)
        items = {vis(re.search(r"<b>([\s\S]*?)</b>", blk[a:e]).group(1)): blk[a:e]
                 for a, e in sp}
        if sorted(items) != sorted(want):
            print(f"   X {num} 표제어가 다름: {sorted(items)} ≠ {sorted(want)}")
            continue
        nb = blk[:sp[0][0]] + " ".join(items[w] for w in want) + blk[sp[-1][1]:]
        s = s[:m.start(1)] + nb + s[m.end(1):]
        done.add(num)
        print(f"   [{num}] {' · '.join(items)}")
        print(f"          → {' · '.join(want)}")
    if s != s0:
        for tg in ("span", "div", "b"):
            a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert a == b, f"{tg} 짝이 어긋남 {f}"
        assert sorted(vis(s).split()) == sorted(vis(s0).split()), f"글자가 바뀜 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
            print(f"   ■ 씀 {f[:30]}")

print(f"\n■ {len(done)}곳 / 바라던 {len(WANT)}곳")
assert len(done) == len(WANT), "못 고친 것이 있습니다"

# -*- coding: utf-8 -*-
r"""어휘에서 「묶음 = 부분 + 부분」 풀이를 뺀다 (사용자 지시 2026-08-19)

  「어휘는 뜻만 알게 하면 된다」

    56  남자 친구  boyfriend (남자 man + 친구 friend)  → boyfriend
    76  파란색     blue (파란 blue + 색 color)         → blue
   111  수영하다 (수영 + 하다)  swim                   → 수영하다 / swim
        ★111 은 풀이가 **표제어 안**에 있습니다.

  ※ 성격이 다른 괄호는 건드리지 않았습니다 — 「(르 불규칙)」·「(a 하다 verb)」·
    「(formal: 모릅니다)」 등. 사용자 결정을 기다립니다.

사용: python vocab_drop_breakdown.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"

GLOSS = {   # 문항 → (옛 뜻풀이 HTML 조각, 새 뜻풀이)
    "56": ('boyfriend (<span lang="ko" translate="no">남자</span> man + '
           '<span lang="ko" translate="no">친구</span> friend)', "boyfriend"),
    "76": ('blue (<span lang="ko" translate="no">파란</span> blue + '
           '<span lang="ko" translate="no">색</span> color)', "blue"),
}
HEAD = {"111": ("수영하다 (수영 + 하다)", "수영하다")}

n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for num, (old, new) in GLOSS.items():
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="v-list">[\s\S]*?</div>)', s)
        if not m or old not in m.group(1):
            continue
        nb = m.group(1).replace(old, new)
        s = s[:m.start(1)] + nb + s[m.end(1):]
        n += 1
        print(f"   [{num}] 뜻풀이  {vis(old)}  →  {new}")
    for num, (old, new) in HEAD.items():
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="v-list">[\s\S]*?</div>)', s)
        if not m or "<b>" + old + "</b>" not in m.group(1):
            continue
        nb = m.group(1).replace("<b>" + old + "</b>", "<b>" + new + "</b>")
        s = s[:m.start(1)] + nb + s[m.end(1):]
        n += 1
        print(f"   [{num}] 표제어  {old}  →  {new}")
    if s != s0:
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        assert len(re.findall(r'class="v-item', s)) == \
               len(re.findall(r'class="v-item', s0)), f"어휘 수가 바뀜 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
print(f"\n■ {n}곳 / 바라던 3곳")
assert n == 3

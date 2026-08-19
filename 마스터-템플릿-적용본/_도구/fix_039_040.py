# -*- coding: utf-8 -*-
r"""① 어휘 「주말」 삭제  ② 40번 사다리를 네 단으로 (사용자 지시 2026-08-19)

  ① 같은 상자에 「지난 주말」·「이번 주말」이 있는데 「주말」이 따로 또 있었습니다.
     46번에서 「전화·하다」를 빼고 「전화를 하다」만 남기신 것과 같은 이치입니다.
     ★38·115 도 같은 꼴이라 함께 뺐습니다(39·40 만 말씀하셨습니다).

  ② 40번 사다리 — 38번이 이미 이 꼴입니다.
       우리는 보았습니다.
       우리는 영화를 보았습니다.
       우리는 영화관에서 영화를 보았습니다.
       우리는 지난 주말에 영화관에서 영화를 보았습니다.
     늘어난 자리는 이름표와 문장 양쪽에서 같은 색으로 짚습니다.

사용: python fix_039_040.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"

DROP_JUMAL = ("38", "39", "40", "115")


def li(roles, roles_en, ko, en, now=False):
    c = ' class="wo-now"' if now else ""
    return (f'<li{c}><span class="wo-add">{roles}'
            f'<small lang="en" translate="yes">{roles_en}</small></span>'
            f'<span class="wo-ko">{ko}</span>'
            f'<span class="wo-en" lang="en" translate="yes">{en}</span></li>')


STEPS40 = [
    ("주어 + 서술어(동사)", "Subject + Predicate (Verb)",
     "우리는 보았습니다.", "We watched."),
    ("주어 + <em>목적어</em> + 서술어(동사)",
     "Subject + <em>Object</em> + Predicate (Verb)",
     "우리는 <em>영화를</em> 보았습니다.", "We watched a movie."),
    ("주어 + <em>부사어(장소)</em> + 목적어 + 서술어(동사)",
     "Subject + <em>Adverbial (Place)</em> + Object + Predicate (Verb)",
     "우리는 <em>영화관에서</em> 영화를 보았습니다.",
     "We watched a movie at the theater."),
    ("주어 + <em>부사어(시간)</em> + 부사어(장소) + 목적어 + 서술어(동사)",
     "Subject + <em>Adverbial (Time)</em> + Adverbial (Place) + Object + Predicate (Verb)",
     "우리는 <em>지난 주말에</em> 영화관에서 영화를 보았습니다.",
     "We watched a movie at the theater last weekend."),
]


def item_span(blk, at):
    a = blk.rfind('<span class="v-item', 0, at)
    d, i = 1, blk.index(">", a) + 1
    while d and i < len(blk):
        t = re.compile(r"</?span\b").search(blk, i)
        if not t:
            break
        d += -1 if t.group(0).startswith("</") else 1
        i = t.end()
    return a, blk.find(">", i - 1) + 1


n_v = n_l = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0

    # ① 어휘 「주말」
    for num in DROP_JUMAL:
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="v-list">[\s\S]*?</div>)', s)
        if not m:
            continue
        blk = m.group(1)
        bm = re.search(r"<b>주말</b>", blk)
        if not bm:
            continue
        assert "주말</b>" in blk.replace("<b>주말</b>", ""), \
            f"{num}: 「지난/이번 주말」이 없는데 「주말」만 있습니다 — 지우면 안 됩니다"
        a, e = item_span(blk, bm.start())
        nb = re.sub(r"\s{2,}", " ", blk[:a] + blk[e:])
        s = s[:m.start(1)] + nb + s[m.end(1):]
        n_v += 1
        print(f"   [{num}] 어휘 「주말」 지움 → {vis(nb)}")

    # ② 40번 사다리
    m = re.search(r'<h3><span lang="en" translate="yes">40\)[\s\S]*?'
                  r'(<ol class="wo-steps">[\s\S]*?</ol>)', s)
    if m:
        new = ('<ol class="wo-steps">\n'
               + "\n".join(li(a, b, k, e, i == len(STEPS40) - 1)
                           for i, (a, b, k, e) in enumerate(STEPS40)) + '\n</ol>')
        print(f"   [40] 사다리 {m.group(1).count('<li')}단 → {len(STEPS40)}단")
        for a, b, k, e in STEPS40:
            print(f"        {vis(k):<34}{e}")
        s = s[:m.start(1)] + new + s[m.end(1):]
        n_l += 1

    if s != s0:
        for tg in ("span", "b", "div", "ol", "li", "em", "small"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        assert not re.search(r'<div class="v-list">\s*</div>', s), f"빈 어휘 상자 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
            print(f"   ■ 씀 {f.split(chr(92))[-1][:30]}")

print(f"\n■ 어휘 {n_v}곳 · 사다리 {n_l}곳")
assert n_v == 4 and n_l == 1, "어휘 4곳·사다리 1곳이어야 합니다"

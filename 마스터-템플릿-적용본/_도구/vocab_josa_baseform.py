# -*- coding: utf-8 -*-
r"""어휘에서 조사를 떼고, 동사·형용사를 기본형으로 (사용자 규칙 2026-08-19)

  「어휘에서는 조사를 빼는 것이 좋다 · 동사 형용사는 기본형으로 하는 것이 좋다」

  ① 조사를 떼는 곳 — 정답으로 하나하나 검산했습니다.
       51 누가→누구 · 52 제가→저 · 59 당신의→당신 · 61 어디에→어디 ·
       63·117 어디에서→어디 · 69 무엇을→무엇 · 203 아들에게→아들 ·
       258 아무것도→아무것 · 484 옆에→옆
     뜻풀이의 문법 주석도 함께 뗍니다 — 「who (subject)」→「who」.

  ② 기본형으로
       78 친절한 → 친절하다 · 290 좋은 → 좋다
     형용사 뜻풀이는 책 규칙대로 「to be + 형용사」입니다.

  ③ **지우는 것** — 조사가 붙어 살아남은 인칭 대명사
     101번부터 인칭 대명사를 어휘에서 빼기로 이미 정하셨는데(2026-08-19),
     「그를·저를·저에게·제가」는 조사가 붙어 있어 그때 그물에 안 걸렸습니다.
       129·397 그를 · 201·202 저에게 · 293 제가 · 398·399 저를
     361 「좋은」도 같은 상자에 이미 「좋다」가 있어 지웁니다.

  ★건드리지 않은 것
     전에·후에·때문에·덕분에 — 그 장이 가르치는 문법 자체입니다.
     싸게·깨끗이·친절하게 — 「부사형」 장이 가르치는 꼴입니다(388~396).

사용: python vocab_josa_baseform.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

# 문항 → (옛 표제어, 새 표제어 또는 None=삭제, 새 뜻 또는 None=그대로)
FIX = [
    ("51",  "누가",     "누구",     "who"),
    ("52",  "제가",     "저",       None),
    ("59",  "당신의",   "당신",     "you"),
    ("61",  "어디에",   "어디",     "where"),
    ("63",  "어디에서", "어디",     "where"),
    ("69",  "무엇을",   "무엇",     "what"),
    ("117", "어디에서", "어디",     "where"),
    ("203", "아들에게", "아들",     "son"),
    ("258", "아무것도", "아무것",   None),
    ("484", "옆에",     "옆",       "next to"),
    ("78",  "친절한",   "친절하다", "to be kind"),
    ("290", "좋은",     "좋다",     "to be good"),
    ("129", "그를",     None, None), ("397", "그를", None, None),
    ("201", "저에게",   None, None), ("202", "저에게", None, None),
    ("293", "제가",     None, None),
    ("398", "저를",     None, None), ("399", "저를", None, None),
    ("361", "좋은",     None, None),
]


def item_span(s, at):
    """표제어 자리에서 뒤로 걸어가 그 v-item 의 구간을 찾는다"""
    a = s.rfind('<span class="v-item', 0, at)
    d, i = 1, s.index(">", a) + 1
    while d and i < len(s):
        t = re.compile(r"</?span\b").search(s, i)
        if not t:
            break
        d += -1 if t.group(0).startswith("</") else 1
        i = t.end()
    return a, s.find(">", i - 1) + 1


done, bad = [], []
for f in sorted(glob.glob("*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for num, old, new, gloss in FIX:
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="v-list">[\s\S]*?</div>)', s)
        if not m:
            continue
        blk = m.group(1)
        bm = re.search(r"<b>" + re.escape(old) + r"</b>", blk)
        if not bm:
            bad.append((num, old, "표제어 없음")); continue
        a, e = item_span(blk, bm.start())
        if new is None:
            nb = re.sub(r"\s{2,}", " ", blk[:a] + blk[e:])
            done.append((num, old, "지움"))
        else:
            it = blk[a:e].replace("<b>" + old + "</b>", "<b>" + new + "</b>")
            if gloss:
                # ★뜻풀이 안에 잠긴 한국어 span 이 겹쳐 있을 수 있다
                #   (78 「kind (the modifier form of <span lang=ko>친절하다</span>)」).
                #   비탐욕으로 </span> 를 찾으면 안쪽에서 끊겨 짝이 깨진다.
                gm = re.search(r'<span class="gloss"[^>]*>', it)
                if not gm:
                    bad.append((num, old, "뜻풀이 자리 없음")); continue
                d, i = 1, gm.end()
                while d and i < len(it):
                    t = re.compile(r"</?span\b").search(it, i)
                    if not t:
                        break
                    d += -1 if t.group(0).startswith("</") else 1
                    i = t.end()
                close = it.rfind("</span>", 0, i + 1)
                it = it[:gm.end()] + gloss + it[close:]
            nb = blk[:a] + it + blk[e:]
            done.append((num, old, vis(it)))
        s = s[:m.start(1)] + nb + s[m.end(1):]
    if s != s0:
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        if not re.search(r'<div class="v-list">\s*</div>', s):
            pass
        else:
            bad.append((f, "", "어휘 상자가 비었음"))
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)

for n, o1, r in done:
    print(f"   [{n:>3}] {o1:<8}→ {r}")
for x in bad:
    print("   X", x)
print(f"\n■ {len(done)}곳 / 바라던 {len(FIX)}곳 · 어긋남 {len(bad)}")
assert len(done) == len(FIX) and not bad

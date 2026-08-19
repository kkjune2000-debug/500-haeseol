# -*- coding: utf-8 -*-
r"""46~50 어순 이름표에 「목적어」를 살리고 50 을 3단으로 (사용자 지시 2026-08-19)

  「저는 전화를 했습니다」의 **전화를**은 목적어입니다. 그런데 이름표도 제목도
  그것을 빼고 「주어 + 서술어(동사)」라고만 적고 있었습니다.
  간접목적어가 붙으면 그 목적어는 **직접목적어**가 됩니다.

    46  제목  주어 + 서술어(동사)                 → 주어 + 목적어 + 서술어(동사)
    47  제목  주어 + 간접목적어 + 서술어(동사)      → 주어 + 간접목적어 + 직접목적어 + 서술어(동사)
    48  〃                                    〃
    49  〃                                    〃
    50  제목  주어 + 부사어(장소) + 간접목적어 + 서술어(동사)
              → 주어 + 부사어(장소) + 간접목적어 + 직접목적어 + 서술어(동사)
        사다리 2단 → 3단 (저는 전화를 했습니다 부터)

  ※ 만들기는 「전화하다 = 전화를 하다 → 전화를 했습니다」로 한 덩이입니다.
     낱말을 만드는 자리라 그대로 두었습니다 — 어휘에서도 「전화를 하다」 하나만
     남기기로 하셨습니다(46번).

사용: python eosun_046_050.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 041~050 문장구조 간접목적어 직접목적어.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

TITLE = {
    "46": ("주어 + 목적어 + 서술어(동사)",
           "Korean order: Subject + Object + Predicate(Verb)"),
    "47": ("주어 + 간접목적어 + 직접목적어 + 서술어(동사)",
           "Korean order: Subject + Indirect Object + Direct Object + Predicate(Verb)"),
    "48": ("주어 + 간접목적어 + 직접목적어 + 서술어(동사)",
           "Korean order: Subject + Indirect Object + Direct Object + Predicate(Verb)"),
    "49": ("주어 + 간접목적어 + 직접목적어 + 서술어(동사)",
           "Korean order: Subject + Indirect Object + Direct Object + Predicate(Verb)"),
    "50": ("주어 + 부사어(장소) + 간접목적어 + 직접목적어 + 서술어(동사)",
           "Korean order: Subject + Adverbial(Place) + Indirect Object + "
           "Direct Object + Predicate(Verb)"),
}

R_O = ("주어 + 목적어 + 서술어(동사)", "Subject + Object + Predicate (Verb)")
R_IO = ("주어 + <em>간접목적어</em> + 직접목적어 + 서술어(동사)",
        "Subject + <em>Indirect Object</em> + Direct Object + Predicate (Verb)")
R_ADV = ("주어 + <em>부사어(장소)</em> + 간접목적어 + 직접목적어 + 서술어(동사)",
         "Subject + <em>Adverbial (Place)</em> + Indirect Object + "
         "Direct Object + Predicate (Verb)")

STEPS = {
    "47": [("저는 전화를 했습니다.", "I made a call.", R_O),
           ("저는 친구에게 전화를 했습니다.", "I called my friend.", R_IO)],
    "48": [("저는 전화를 했습니다.", "I made a call.", R_O),
           ("저는 집에 전화를 했습니다.", "I called home.", R_IO)],
    "49": [("저는 전화를 했습니다.", "I made a call.", R_O),
           ("저는 회사에 전화를 했습니다.", "I called the office.", R_IO)],
    "50": [("저는 전화를 했습니다.", "I made a call.", R_O),
           ("저는 회사에 전화를 했습니다.", "I called the office.", R_IO),
           ("저는 집에서 회사에 전화를 했습니다.", "I called the office from home.", R_ADV)],
}


def li(ko, en, r, now):
    c = ' class="wo-now"' if now else ""
    return (f'<li{c}><span class="wo-add">{r[0]}'
            f'<small lang="en" translate="yes">{r[1]}</small></span>'
            f'<span class="wo-ko">{ko}</span>'
            f'<span class="wo-en" lang="en" translate="yes">{en}</span></li>')


s0 = io.open(P, encoding="utf-8").read()
s = s0

# ── 제목
for num, (ko, en) in TITLE.items():
    m = re.search(r'(<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                  r'<div class="wo-title">)([\s\S]*?)(</div>)', s)
    assert m, f"{num} 제목 못 찾음"
    old = m.group(2)
    new = (f'한국어 어순: {ko}<br>'
           f'<span lang="en" translate="yes">{en}</span>')
    if vis(old) == vis(new):
        print(f"   [{num}] 제목 이미 같음")
        continue
    print(f"   [{num}] 제목  {vis(old)[:44]}\n              → {vis(new)[:60]}")
    s = s[:m.start(2)] + new + s[m.end(2):]

# ── 사다리
for num, steps in STEPS.items():
    m = re.search(r'(<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?)'
                  r'(<ol class="wo-steps">[\s\S]*?</ol>)', s)
    assert m, f"{num} 사다리 못 찾음"
    old = m.group(2)
    kos = [x.strip() for x in re.findall(r'<span class="wo-ko">([\s\S]*?)</span>', old)]
    assert kos[-1] == steps[-1][0], f"{num} 마지막 문장이 다름: {kos[-1]}"
    new = ('<ol class="wo-steps">\n'
           + "\n".join(li(k, e, r, i == len(steps) - 1)
                       for i, (k, e, r) in enumerate(steps)) + '\n</ol>')
    print(f"   [{num}] 사다리 {len(kos)}단 → {len(steps)}단")
    for k, e, r in steps:
        print(f"        [{vis(r[0])}] {k} / {e}")
    s = s[:m.start(2)] + new + s[m.end(2):]

# ── 검산
for tg in ("ol", "li", "span", "small", "em", "div", "h3"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"{tg} 짝이 어긋남"
assert len(re.findall(r'class="wo-box"', s)) == len(re.findall(r'class="wo-box"', s0))
assert s.count('class="wo-now"') == s0.count('class="wo-now"'), "wo-now 수가 바뀜"
assert len(re.findall(r'class="wo-title"', s)) == len(re.findall(r'class="wo-title"', s0))
print("\n■ 검산 통과")

if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

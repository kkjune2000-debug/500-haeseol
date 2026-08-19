# -*- coding: utf-8 -*-
r"""41~50 의 사다리 구멍 메우기 — 43·47 을 본으로 (사용자 지시 2026-08-19)

  이 묶음은 「주다」(41~45)와 「전화를 하다」(46~50) 둘을 가르칩니다.
  뼈대는 41 「저는 주었습니다」 · 46 「저는 전화를 했습니다」이고,
  거기에 목적어를 하나씩 붙여 나갑니다.

      41  1단  저는 주었습니다.
      42  2단  + 직접목적어
      43  3단  + 간접목적어            ← 본
      44  1단  ← 구멍
      45  1단  ← 구멍
      46  1단  저는 전화를 했습니다.
      47  2단  + 간접목적어            ← 본
      48  1단  ← 구멍
      49  1단  ← 구멍
      50  2단

  ★왜 자동으로 안 됐나 — eosun_ladder.py 의 사슬은 「바로 앞 문항을 늘린 것」만
    잇습니다. 44 의 앞은 43(저는 그녀에게 선물을…)이라 44 를 늘린 것이 아닙니다.
    이 묶음은 앞 문항이 아니라 **그 묶음의 뼈대**(41·46)에서 자랍니다.
    부사어 빼기도 안 통합니다 — 간접목적어는 부사어가 아닙니다.

  ★새로 쓴 문장은 둘뿐입니다 — 「저는 생선을 주었습니다」·「저는 물을 주었습니다」.
    교재 42 「저는 선물을 주었습니다 / I gave a gift.」와 같은 꼴입니다.
    나머지 단은 교재 41·46 문장 그대로입니다.

사용: python eosun_ladder_041.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 041~050 문장구조 간접목적어 직접목적어.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
APPLY = "--apply" in sys.argv


def li(ko, en, roles, roles_en, now=False):
    c = ' class="wo-now"' if now else ""
    return (f'<li{c}><span class="wo-add">{roles}'
            f'<small lang="en" translate="yes">{roles_en}</small></span>'
            f'<span class="wo-ko">{ko}</span>'
            f'<span class="wo-en" lang="en" translate="yes">{en}</span></li>')


R_SV = ("주어 + 서술어(동사)", "Subject + Predicate (Verb)")
R_DO = ("주어 + <em>직접목적어</em> + 서술어(동사)",
        "Subject + <em>Direct Object</em> + Predicate (Verb)")
R_IO2 = ("주어 + <em>간접목적어</em> + 직접목적어 + 서술어(동사)",
         "Subject + <em>Indirect Object</em> + Direct Object + Predicate (Verb)")
R_IO1 = ("주어 + <em>간접목적어</em> + 서술어(동사)",
         "Subject + <em>Indirect Object</em> + Predicate (Verb)")

PLAN = {
    "44": [("저는 주었습니다.", "I gave.", R_SV),
           ("저는 생선을 주었습니다.", "I gave a fish.", R_DO),
           ("저는 고양이에게 생선을 주었습니다.", "I gave the cat a fish.", R_IO2)],
    "45": [("저는 주었습니다.", "I gave.", R_SV),
           ("저는 물을 주었습니다.", "I gave water.", R_DO),
           ("저는 꽃에 물을 주었습니다.", "I gave water to the flowers.", R_IO2)],
    "48": [("저는 전화를 했습니다.", "I made a call.", R_SV),
           ("저는 집에 전화를 했습니다.", "I called home.", R_IO1)],
    "49": [("저는 전화를 했습니다.", "I made a call.", R_SV),
           ("저는 회사에 전화를 했습니다.", "I called the office.", R_IO1)],
}

s0 = io.open(P, encoding="utf-8").read()
s = s0
done = 0

for num, steps in PLAN.items():
    pat = re.compile(r'(<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?)'
                     r'(<ol class="wo-steps">[\s\S]*?</ol>)')
    m = pat.search(s)
    if not m:
        print(f"   X {num} 못 찾음"); sys.exit(1)
    old = m.group(2)
    if old.count("<li") != 1:
        print(f"   X {num} 이미 {old.count('<li')}단입니다 — 건드리지 않습니다"); continue
    # 마지막 단의 한국어·영어가 정답과 같은지
    ko = re.search(r'<span class="wo-ko">([\s\S]*?)</span>', old).group(1).strip()
    if ko != steps[-1][0]:
        print(f"   X {num} 마지막 문장이 다름: 「{ko}」 ≠ 「{steps[-1][0]}」"); sys.exit(1)
    new = ('<ol class="wo-steps">\n'
           + "\n".join(li(k, e, r[0], r[1], i == len(steps) - 1)
                       for i, (k, e, r) in enumerate(steps))
           + '\n</ol>')
    s = s[:m.start(2)] + new + s[m.end(2):]
    done += 1
    print(f"   [{num}] 1단 → {len(steps)}단")
    for k, e, r in steps:
        print(f"        {k:<28}{e}")

# ── 검산
for tg in ("ol", "li", "span", "small", "em", "div"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"{tg} 짝이 어긋남"
assert len(re.findall(r'class="wo-box"', s)) == len(re.findall(r'class="wo-box"', s0))
assert s.count('class="wo-now"') == s0.count('class="wo-now"'), "wo-now 수가 바뀜"
print(f"\n■ {done}곳 · 검산 통과")

if APPLY and done:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

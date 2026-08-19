# -*- coding: utf-8 -*-
r"""46) 어휘에서 「전화」·「하다」 삭제 (사용자 지시 2026-08-19)

  원문은 「I made a call.」 — 「phone call」도 「do」도 낱말로 들어 있지 않습니다.
  들어 있는 것은 「made a call」 = 전화를 하다 하나뿐입니다.
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 041~050 문장구조 간접목적어 직접목적어.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
DROP = {"전화", "하다"}

s0 = io.open(P, encoding="utf-8").read()
m = re.search(r'<h3><span lang="en" translate="yes">46\)[\s\S]*?'
              r'(<div class="v-list">[\s\S]*?</div>)', s0)
assert m, "46 의 어휘 상자를 못 찾음"
blk = m.group(1)


def spans(b):
    got = []
    for im in re.finditer(r'<span class="v-item[^"]*">', b):
        d, i = 1, im.end()
        while d and i < len(b):
            t = re.compile(r"</?span\b").search(b, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        got.append((im.start(), i))
    return got


items = spans(blk)
print(f"■ 46 의 어휘 {len(items)}개")
keep, drop = [], []
for a, e in items:
    h = vis(re.search(r"<b>([\s\S]*?)</b>", blk[a:e]).group(1))
    (drop if h in DROP else keep).append((a, e, h, vis(blk[a:e])))
for _, _, h, t in drop:
    print(f"   지움  {t}")
for _, _, h, t in keep:
    print(f"   남김  {t}")
assert len(drop) == 2 and len(keep) == 1, f"지울 것 2·남길 것 1 이어야 함 ({len(drop)}·{len(keep)})"

nb = blk
for a, e, _, _ in sorted(drop, reverse=True):
    nb = nb[:a] + nb[e:]
nb = re.sub(r"\s{2,}", " ", nb)
s = s0[:m.start(1)] + nb + s0[m.end(1):]

for tg in ("span", "div", "b"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"{tg} 짝이 어긋남"
assert len(re.findall(r'class="v-item', s0)) - len(re.findall(r'class="v-item', s)) == 2
print("■ 검산 통과")

if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

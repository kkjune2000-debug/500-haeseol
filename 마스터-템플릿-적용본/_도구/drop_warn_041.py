# -*- coding: utf-8 -*-
r"""41~50 의 되풀이 「주의」 상자 삭제 (사용자 지시 2026-08-19)

  파일 맨 앞 핵심 문법의 표가 이미 가르칩니다 —
    사람·동물 → 에게 (옅은 파랑) · 그 밖 → 에 (옅은 호박)
  그런데 45(꽃)와 48(집)에서 같은 말을 다시 합니다.
  ★48 것은 한국어가 아예 없이 영어뿐이라 책의 「한국어 먼저」 규칙에도 어긋납니다.
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 041~050 문장구조 간접목적어 직접목적어.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

s0 = io.open(P, encoding="utf-8").read()
s = s0
ms = list(re.finditer(r'<div class="gb gb-warn">[\s\S]*?</div>', s))
print(f"■ gb-warn 상자 {len(ms)}개")
assert len(ms) == 2, "2개여야 합니다"
for m in ms:
    assert "에게" in m.group(0), "에게/에 이야기가 아닌 상자입니다 — 지우면 안 됩니다"

for m in ms[::-1]:
    hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
    print(f"   [문항 {hs[-1]}] 지움  {vis(m.group(0))[:66]}")
    # 앞뒤 빈 줄도 함께 정리
    a, b = m.start(), m.end()
    while a > 0 and s[a - 1] in " \t":
        a -= 1
    while b < len(s) and s[b] in " \t":
        b += 1
    if a > 0 and s[a - 1] == "\n" and b < len(s) and s[b] == "\n":
        b += 1
    s = s[:a] + s[b:]

# ── 검산
for tg in ("div", "span", "small", "em", "strong", "i"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"{tg} 짝이 어긋남 ({b} → {a})"
assert "gb-warn" not in s or 'class="gb gb-warn"' not in s, "상자가 남았습니다"
assert len(re.findall(r'class="wo-box"', s)) == len(re.findall(r'class="wo-box"', s0))
assert len(re.findall(r"<h3>", s)) == len(re.findall(r"<h3>", s0))
print("■ 검산 통과")

if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

# -*- coding: utf-8 -*-
r"""「💡 표기 안내」의 보기 두 줄 삭제 (사용자 지시 2026-08-19)

  지우는 것
    (예: 동사 + ㄹ 수 있다 = 동사 어간에 ㄹ 수 있다를 붙임 → 가다 → 가 + ㄹ 수 있다 = 갈 수 있다)
    (e.g., Verb + ㄹ 수 있다 = attach ㄹ 수 있다 to the verb stem → 가다 → 가 + ㄹ 수 있다 = 갈 수 있다)

  남는 것 — 상자의 요지 두 줄
    앞으로 "동사/형용사 + 어미"는 "동사/형용사 어간 + 어미"를 의미합니다.
    From now on, "Verb/Adjective + ending" means "Verb/Adjective stem + ending" …
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 105~114 서술어 문법 능력 가능.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

s0 = io.open(P, encoding="utf-8").read()

m = re.search(r"\s*<br>\s*<small style=\"color:#475569;\">\(예: [\s\S]*?</small>"
              r"\s*<br>\s*<small style=\"color:#475569;\" lang=\"en\" translate=\"yes\">"
              r"[\s\S]*?</small>", s0)
assert m, "보기 두 줄을 못 찾음"
print("── 지울 것")
print("   " + vis(m.group(0))[:150])

s = s0[:m.start()] + s0[m.end():]

for tg in ("small", "em", "strong", "span", "div"):
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남 ({y} → {x})"
assert "표기 안내" in s, "상자가 통째로 사라짐"
assert "동사/형용사 어간 + 어미" in s, "남겨야 할 요지가 사라짐"
assert "갈 수 있다)" not in s, "보기가 남음"
print("\n── 남는 상자")
i = s.find("표기 안내")
print("   " + vis(s[i - 60:i + 700])[:230])
print("\n■ 검산 통과")
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

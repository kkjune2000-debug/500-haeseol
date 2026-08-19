# -*- coding: utf-8 -*-
r"""「이었습니다」 칸을 짧고 쉽게 (사용자 지시 2026-08-19)

  전  이었습니다
      받침 없는 명사 뒤에서는 였습니다로 축약
      After a noun with no final consonant it contracts to 였습니다
      (가수였습니다 O · 대학생이었습니다는 축약 불가)
      (가수였습니다 O · 대학생이었습니다 cannot contract)

  후  이었습니다
      받침이 없으면 였습니다
      가수 → 가수였습니다
      No final consonant → 였습니다

  · 같은 표의 「현재 입니다」·「미래 일 것입니다」는 한 낱말인데 과거 칸에만
    설명이 몰려 있었습니다.
  · 「대학생이었습니다는 축약 불가」는 뺐습니다 — 칸의 표제가 이미
    「이었습니다」(안 줄어든 꼴)라 되풀이입니다.
  · 한국어 두 줄 · 영어 한 줄.
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 087~096 서술어 문법 이다.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

OLD = ('<small>받침 없는 명사 뒤에서는 <strong>였습니다</strong>로 축약<br>\n'
       '<em lang="en" translate="yes">After a noun with no final consonant it contracts to '
       '<span lang="ko" translate="no">였습니다</span>\n</em>\n'
       '<br>(가수<strong>였습니다</strong> O · 대학생이었습니다는 축약 불가)<br>\n'
       '<em lang="en" translate="yes">(<span lang="ko" translate="no">가수였습니다</span> O · '
       '<span lang="ko" translate="no">대학생이었습니다</span> cannot contract)</em>\n</small>')
NEW = ('<small>받침이 없으면 <strong>였습니다</strong><br>'
       '가수 → 가수<strong>였습니다</strong><br>'
       '<em lang="en" translate="yes">No final consonant → '
       '<span lang="ko" translate="no">였습니다</span></em></small>')

s0 = io.open(P, encoding="utf-8").read()
if OLD not in s0:
    # 줄바꿈이 다를 수 있으므로 느슨하게 잡는다
    m = re.search(r"<small>받침 없는 명사[\s\S]*?</small>", s0)
    assert m, "옛 글을 못 찾음"
    print("   ── 잡은 옛 글")
    print("   " + vis(m.group(0))[:120])
    old = m.group(0)
else:
    old = OLD
s = s0.replace(old, NEW, 1)
assert s != s0, "안 바뀜"
assert s.count(NEW) == 1

for tg in ("small", "strong", "em", "span", "br"):
    if tg == "br":
        continue
    x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert x == y, f"{tg} 짝이 어긋남"
print("\n   전 " + vis(old))
print("   후 " + vis(NEW))
print("\n■ 검산 통과")
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

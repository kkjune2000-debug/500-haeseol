# -*- coding: utf-8 -*-
r"""81) 어휘 「나/이나 or (noun)」 삭제 (사용자 지시 2026-08-19)

  「어휘에서는 조사를 빼는 것이 좋다」. 같은 장(079~086 접속 과와 이나나)의
  「와/과」·「~과/와」는 앞서 조사 쓸기에서 이미 뺐고 「나/이나」만 남아 있었습니다.
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"
TARGET = "나/이나"

n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for bm in list(re.finditer(r"<b>" + re.escape(TARGET) + r"</b>", s))[::-1]:
        a = s.rfind('<span class="v-item', 0, bm.start())
        if a < 0:
            print("   X 항목 시작을 못 찾음"); continue
        d, i = 1, s.index(">", a) + 1
        while d and i < len(s):
            t = re.compile(r"</?span\b").search(s, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        e = s.find(">", i - 1) + 1
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:a])
        print(f"   [{hs[-1]}] 지움  {vis(s[a:e])}")
        s = s[:a] + s[e:]
        n += 1
    if s != s0:
        s = re.sub(r'(<div class="v-list">)\s{2,}', r"\1 ", s)
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        assert len(re.findall(r'class="v-item', s0)) - \
               len(re.findall(r'class="v-item', s)) == n, "지운 수가 안 맞음"
        assert not re.search(r'<div class="v-list">\s*</div>', s), "빈 상자"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
            print(f"   ■ 씀 {f.split(chr(92))[-1][:30]}")
print(f"\n■ {n}곳")
assert n == 1

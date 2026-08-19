# -*- coding: utf-8 -*-
r"""요일 링크 6개 삭제 (사용자 지시 2026-08-19)

  ★왜 모양이 깨졌나 — .gram-link CSS 는 011~020·021~030 **두 파일에만** 있습니다.
    제가 붙인 다섯 파일에는 없어 꾸밈 없는 링크로 나왔고, 안의 .gloss 가
    따로 한 줄을 차지했습니다. 클래스만 빌려 쓴 제 잘못입니다.
"""
import io, re, sys, glob, urllib.parse

B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
APPLY = "--apply" in sys.argv
HREF = urllib.parse.quote("4 부록 9 요일.html")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for m in list(re.finditer(r'\s*<a class="gram-link" href="' + re.escape(HREF) +
                              r'"[\s\S]*?</a>', s))[::-1]:
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
        print(f"   [{hs[-1] if hs else '?'}] 지움  {vis(m.group(0))}")
        s = s[:m.start()] + s[m.end():]
        n += 1
    if s != s0:
        for tg in ("a", "div", "span"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
print(f"\n■ 지운 링크 {n}개")
assert n == 6

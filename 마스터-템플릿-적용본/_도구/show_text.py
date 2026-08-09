# -*- coding: utf-8 -*-
"""화면에 보이는 글자만 뽑아 본다 — 태그를 걷어 내고 사람이 읽는 것만

★ 검사기는 **화면 글자**를 보아야 한다. 마크업만 비교하면
  「CSS 글자가 있으니 같다」처럼 틀린 판정을 내린다.
  고치기 전과 후를 각각 파일로 받아 diff 하면 무엇이 달라졌는지 한눈에 보인다.

쓰기
    python show_text.py "2 조사"              이름에 맞는 파일들
    python show_text.py "2 조사 F" 4000        길이 제한을 늘려서
    python show_text.py "2 조사" > 전.txt      고치기 전에 받아 두고 나중에 비교
"""
import re, sys, glob
import _paths

out = _paths.enter()
pat = sys.argv[1] if sys.argv[1:] else "*"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2500

for f in sorted(glob.glob(f"*{pat}*.html")):
    s = open(f, encoding="utf-8").read()
    s = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->", " ", s)
    s = re.sub(r'<img[^>]*>', "[그림]", s)
    s = re.sub(r'<span class="gloss"[^>]*>', "\n   ↳ ", s)
    s = re.sub(r"</p>|</div>|</h[1-6]>|<br\s*/?>|</tr>|</blockquote>|</li>", "\n", s)
    s = re.sub(r"</t[dh]>", "  |  ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()
    out.write(f"\n{'='*70}\n{f}\n{'='*70}\n{s[:N]}\n")
out.flush()

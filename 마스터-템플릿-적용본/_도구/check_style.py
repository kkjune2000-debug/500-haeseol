# -*- coding: utf-8 -*-
"""검사 ③ 스타일 블록 건강

★ 왜 있는가 (2026-08-09 사고)
  <script> 를 넣을 자리를 정규식 <body[^>]*> 로 찾았더니
  CSS 주석 안의 글자 「3) <body>」 에 걸려 <style> 한복판에 스크립트를 꽂았다.
  스크립트의 /* … */ 가 바깥 CSS 주석을 먼저 닫아 버려
  그 뒤 CSS 가 통째로 죽었고, .container{max-width:800px} 도 함께 죽어
  조사 A~F 가 화면 가득 퍼졌다. 눈으로는 「CSS 글자가 있으니 같다」고 오판했다.
  ⇒ 태그가 아니라 **적용되는가**를 보라. 이 검사가 그 대역이다.

쓰기: python check_style.py            (전체)
      python check_style.py 조사        (이름에 「조사」가 든 파일의 style 목록도 함께)
"""
import re, sys, glob
import _paths

out = _paths.enter()
bad = 0
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    scripts = [(m.start(), m.end()) for m in re.finditer(r"<script\b[\s\S]*?</script>", s)]
    for i, m in enumerate(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s)):
        css = m.group(1)
        ln = s[:m.start()].count("\n") + 1
        if css.count("{") != css.count("}"):
            out.write(f"   [중괄호] {f[:40]:<42} style#{i} "
                      f"{css.count('{')}/{css.count('}')} @줄{ln}\n"); bad += 1
        if any(a <= m.start() < b for a, b in scripts):
            out.write(f"   [스크립트 안 style] {f[:40]:<42} style#{i}\n"); bad += 1
        if "</script>" in css or "<script" in css:
            out.write(f"   [style 안에 script] {f[:40]:<42} style#{i}\n"); bad += 1
out.write(f"■ 스타일 문제 {bad}건\n")

if len(sys.argv) > 1:
    for f in sorted(glob.glob(f"*{sys.argv[1]}*.html")):
        s = open(f, encoding="utf-8").read()
        out.write(f"\n■ {f} 의 style 블록\n")
        for i, m in enumerate(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s)):
            css = m.group(1)
            first = re.search(r"[^\s{}][^{}\n]{0,40}\{", css)
            out.write(f"   #{i} 줄{s[:m.start()].count(chr(10))+1:<6} {len(css):>6}자  "
                      f"중괄호 {css.count('{')}/{css.count('}')}  "
                      f"첫 규칙 {first.group(0)[:36] if first else '-'}\n")
            if ".container" in css:
                out.write("        ← .container 여기 있음\n")
out.flush()

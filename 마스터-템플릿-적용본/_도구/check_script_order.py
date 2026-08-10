# -*- coding: utf-8 -*-
"""검사 ② 스크립트 선후 — 정의보다 앞선 블록에서 부르는 함수

★ 왜 있는가 (2026-08-09 사고)
  jmSpk 를 정의한 <script> 를 표를 그리는 <script> 뒤에 넣었더니
  ReferenceError 가 나면서 「퀴즈 2 · 쓰기」 표가 23개 파일에서 통째로 사라졌다.
  같은 블록 안이면 호이스팅으로 살지만, 블록이 다르면 죽는다.
  onclick="…" 안에서 부르는 것은 클릭할 때 실행되므로 문제가 아니다.

쓰기: python check_script_order.py
"""
import re, glob
import _paths

out = _paths.enter()
FNS = ["jmSpk", "speakKorean", "akPlayFile", "akSpeakTTS", "akPick", "akNotice", "jmSetSex",
       "akSpeakSeq", "alltSeq", "alltCardBtns", "fcSeq"]
bad = []
for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    blocks = [m.group(1) for m in re.finditer(r"<script\b[^>]*>([\s\S]*?)</script>", s)]
    for fn in FNS:
        defb = next((i for i, js in enumerate(blocks)
                     if re.search(r"function\s+" + fn + r"\s*\(", js)), None)
        if defb is None:
            continue
        for i, js in enumerate(blocks[:defb]):
            js2 = re.sub(r"onclick=\\?\"[^\"]*\\?\"", " ", js)
            js2 = re.sub(r"onclick=\\?'[^']*\\?'", " ", js2)
            if re.search(r"(?<![\w.])" + fn + r"\s*\(", js2):
                bad.append((f, fn, i, defb))
                break

out.write(f"■ 앞 블록에서 먼저 쓰는 곳 {len(bad)}건\n")
for f, fn, i, d in bad[:20]:
    out.write(f"   {f[:40]:<42} {fn}  (쓰는 블록 {i} < 정의 블록 {d})\n")
out.flush()

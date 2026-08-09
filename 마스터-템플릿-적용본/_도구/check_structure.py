# -*- coding: utf-8 -*-
"""검사 ① 구조·정답·음원 짝

  · 태그가 짝이 맞는가 (열림/닫힘 수)
  · 중괄호가 맞는가 (스크립트·스타일이 깨졌다는 신호)
  · data-ans (정답) 가 HEAD 와 같은가  ← 손대지 말아야 할 것을 건드렸는지
  · AK_SND 번호표가 가리키는 mp3 가 실제로 있는가

쓰기: python check_structure.py
"""
import re, glob, os, json, subprocess
from collections import Counter
import _paths

out = _paths.enter()
bad, tot = 0, 0
miss = Counter()

for f in sorted(glob.glob("*.html")):
    t = open(f, encoding="utf-8").read()
    for tag in ("div", "span", "p", "small", "em", "button", "script",
                "style", "table", "tr", "td"):
        o = len(re.findall(rf"<{tag}\b", t))
        c = len(re.findall(rf"</{tag}\s*>", t))
        if o != c:
            out.write(f"   [태그] {f[:34]} {tag} {o}/{c}\n"); bad += 1
    if t.count("{") != t.count("}"):
        out.write(f"   [중괄호] {f[:34]}\n"); bad += 1

    old = subprocess.run(["git", "-C", _paths.ROOT, "show", "HEAD:" + _paths.REL + f],
                         capture_output=True).stdout.decode("utf-8", "replace")
    if old and re.findall(r'data-ans="([^"]*)"', old) != re.findall(r'data-ans="([^"]*)"', t):
        out.write(f"   [정답 바뀜] {f[:34]}\n"); bad += 1

    m = re.search(r"var AK_SND = (\{.*?\});", t, flags=re.S)
    if not m:
        continue
    try:
        mp = json.loads(m.group(1))
    except Exception as e:
        out.write(f"   [번호표 JSON 깨짐] {f[:34]} {e}\n"); bad += 1
        continue
    for text, num in mp.items():
        tot += 1
        for sex in ("f", "m"):
            if not os.path.exists(os.path.join("_소리", sex, num + ".mp3")):
                miss[(sex, num)] += 1

out.write(f"■ 구조·정답 문제 {bad}건\n")
out.write(f"■ 번호표 {tot}개 · 가리키는 파일이 없는 것 {len(miss)}개\n")
for k in list(miss)[:8]:
    out.write(f"   {k}\n")
nf = len(glob.glob(os.path.join("_소리", "f", "*.mp3")))
nm = len(glob.glob(os.path.join("_소리", "m", "*.mp3")))
sz = sum(os.path.getsize(p) for p in glob.glob(os.path.join("_소리", "*", "*.mp3")))
out.write(f"■ 음원 여성 {nf} · 남성 {nm} · 합계 {sz/1024/1024:.1f}MB\n")
n3 = sum(1 for f in glob.glob("*.html") if "ak-audio v1" in open(f, encoding="utf-8").read())
out.write(f"■ 음원 연결된 파일 {n3}개\n")
out.flush()

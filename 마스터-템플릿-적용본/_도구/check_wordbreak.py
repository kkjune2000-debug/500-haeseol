# -*- coding: utf-8 -*-
r"""검사 ⑥ 낱말이 낱글자로 갈리는가 (렌더 · Playwright 필요)

  줄바꿈 자리를 Range 로 재고, 그 앞뒤가 모두 한글이며 사이에 빈칸이 없으면
  「낱말이 갈렸다」로 셉니다.

  ★ 2026-08-18 에 390px 에서 2,530곳이었고 0곳으로 만들었습니다 —
    ① body{word-break:keep-all} 을 106파일에 (2,530 → 49)
    ② .gstep-table td,th 의 overflow-wrap: break-word → normal (49 → 3)
       비상 끊기가 좁은 칸에서 keep-all 을 뚫고 있었습니다.
  ★★ 세로쓰기는 오탐입니다 — writing-mode: vertical-rl 이면 글자마다 top 이
    달라 줄바꿈처럼 보입니다(부록 2 의 「동사」·「형용사」 이름표).
    폭을 390·794·900·1200 으로 바꿔도 개수가 그대로여서 드러났습니다.
    **폭과 무관하면 폭 문제가 아닙니다.**
  ★ keep-all 은 낱말 안만 지키고 ~ 와 / 앞뒤는 못 막습니다.
    형태 이름(~고 싶다)에는 white-space:nowrap 이 따로 필요합니다.

쓰기: python check_wordbreak.py [폭]     (기본 390)
"""
import sys, os, glob, pathlib, collections
import _paths

out = _paths.enter()
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390

JS = r"""() => {
  const hang = c => /[가-힣]/.test(c);
  const res = [], seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const t = n.nodeValue;
    if (!t || !/[가-힣]/.test(t)) continue;
    const p = n.parentElement;
    if (!p || !p.offsetParent) continue;
    const cs = getComputedStyle(p);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    // 세로쓰기는 글자마다 top 이 달라 줄바꿈처럼 보인다 — 오탐이다
    let vert = false, e = p;
    while (e && e !== document.body) {
      const m = getComputedStyle(e).writingMode || '';
      if (m.indexOf('vertical') === 0) { vert = true; break; }
      e = e.parentElement;
    }
    if (vert) continue;
    const r = document.createRange();
    let prev = null;
    for (let i = 0; i < t.length; i++) {
      r.setStart(n, i); r.setEnd(n, i + 1);
      const b = r.getClientRects()[0];
      if (!b) continue;
      if (prev !== null && b.top - prev > 2) {
        const a = t[i-1], c = t[i];
        if (a && hang(a) && hang(c) && !/\s/.test(a) && !/\s/.test(c)) {
          let box = '', e2 = p;
          while (e2 && e2 !== document.body) {
            const cn = (e2.className || '').toString().trim();
            if (cn) { box = cn.split(/\s+/)[0]; break; }
            e2 = e2.parentElement;
          }
          const around = t.slice(Math.max(0, i-8), i) + '│' + t.slice(i, i+8);
          const k = box + '|' + around;
          if (!seen.has(k)) { seen.add(k); res.push({box, around}); }
        }
      }
      prev = b.top;
    }
  }
  return res;
}"""

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    out.write("   ★ playwright 가 없습니다 — 이 검사는 렌더가 필요합니다.\n"
              "     pip install playwright · python -m playwright install chromium\n")
    out.flush(); sys.exit(1)

files = sorted(glob.glob("*.html"))
bybox, byfile, samples = collections.Counter(), collections.Counter(), []
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": W, "height": 900})
    for i, f in enumerate(files, 1):
        pg.goto(pathlib.Path(os.path.abspath(f)).as_uri())
        pg.wait_for_load_state("load")
        for h in pg.evaluate(JS):
            bybox[h["box"]] += 1
            byfile[f] += 1
            if len(samples) < 20:
                samples.append((f, h["box"], h["around"]))
        if i % 25 == 0:
            out.write(f"   … {i}/{len(files)}\n"); out.flush()
    b.close()

tot = sum(bybox.values())
out.write(f"\n■ 화면 {W}px · 낱말이 갈린 자리 {tot}곳\n")
if tot:
    out.write("\n   어느 상자에서 나는가\n")
    for k, v in bybox.most_common(10):
        out.write(f"   {v:>5}  {k or '(클래스 없음)'}\n")
    out.write("\n   많은 쪽\n")
    for k, v in byfile.most_common(6):
        out.write(f"   {v:>5}  {k[:46]}\n")
    out.write("\n   보기 (│ 가 갈린 자리)\n")
    for f, box, a in samples:
        out.write(f"   [{box:<14}] {a}   ← {f[:30]}\n")
out.write(f"\n■ 모두 {tot}곳. 0곳이어야 정상입니다.\n")
out.flush()

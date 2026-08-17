# -*- coding: utf-8 -*-
r"""흉내 ① 번역문이 길어지면 판이 견디는가 (렌더 · Playwright 필요)

  영어를 스페인어·독일어로 옮기면 글자 수가 20~40% 늡니다.
  번역 슬롯(translate="yes")의 영어를 그만큼 늘려 놓고 재 봅니다.
    ① 쪽이 가로로 밀리는가  ② 상자 밖으로 나가는가  ③ 높이가 매인 상자가 넘치는가
  늘리기 **전에도 있던 것은 빼고 늘어난 만큼만** 셉니다.

  ※ 이것은 흉내입니다 — 실제 번역문이 아니라 길이만 흉내 낸 것입니다.

  ★ 2026-08-18 결과 (35% · 390px): 가로 밀림 0 · 상자 밖 0 ·
    **높이 매인 상자 26개가 새로 넘침** (5파일).
    전부 플래시카드 계열(.flashcard / -inner / -front, height:140px, 6~8px)과
    관형어의 .TR(height:133.75px, 306px). height:140px 는 73파일에 있습니다.
    min-height 가 답이지만 뒤집히는 카드가 height:100% 에 기대고 있어
    일괄 치환은 위험합니다.
  ★ overflow:visible 인 상자도 세야 합니다 — 글이 상자 밖으로 삐져나오는 것은
    scrollHeight 로 안 잡히므로 자식의 아래끝을 따로 잽니다.

쓰기: python sim_longtext.py [비율] [폭]      (기본 1.35 390)
"""
import sys, os, glob, pathlib
import _paths

out = _paths.enter()
RATIO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.35
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390
SKIP = {"4 부록 2 부정법.html", "4 부록 8 기초문법총정리.html", "_음성 확인.html"}

GROW = r"""(ratio) => {
  function grow(s, r) {
    const want = Math.round(s.length * r);
    const ws = s.split(/(\s+)/).filter(x => x.trim());
    if (!ws.length || want <= s.length) return s;
    let o = s, i = 0;
    while (o.length < want) { o += ' ' + ws[i % ws.length]; i++; if (i > 60) break; }
    return o;
  }
  let n = 0;
  document.querySelectorAll('[translate="yes"]').forEach(el => {
    if (el.children.length) return;
    const t = el.textContent;
    if (!t || !t.trim() || !/[A-Za-z]/.test(t)) return;   // 영어 칸만
    el.textContent = grow(t, ratio); n++;
  });
  return n;
}"""

MEASURE = r"""() => {
  const de = document.documentElement, vw = de.clientWidth;
  let outBox = 0, fixedOver = 0;
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) return;
    if (r.right > vw + 2) {
      let sc = false, p = el.parentElement;
      while (p) { const o = getComputedStyle(p).overflowX;
                  if (o === 'auto' || o === 'scroll') { sc = true; break; }
                  p = p.parentElement; }
      if (!sc) outBox++;
    }
    if (cs.height && cs.height.endsWith('px')) {
      if (el.scrollHeight > el.clientHeight + 3) fixedOver++;
      else {
        let deep = 0;
        for (const c of el.children) deep = Math.max(deep, c.getBoundingClientRect().bottom - r.top);
        if (deep > r.height + 3) fixedOver++;
      }
    }
  });
  return { pageOver: Math.round(de.scrollWidth - de.clientWidth), outBox, fixedOver };
}"""

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    out.write("   ★ playwright 가 없습니다.\n"); out.flush(); sys.exit(1)

files = [f for f in sorted(glob.glob("*.html")) if f not in SKIP]
tot = {"pageOver": 0, "outBox": 0, "fixedOver": 0}
bad = []
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": W, "height": 900})
    for i, f in enumerate(files, 1):
        pg.goto(pathlib.Path(os.path.abspath(f)).as_uri())
        pg.wait_for_load_state("load")
        before = pg.evaluate(MEASURE)
        n = pg.evaluate(GROW, RATIO)
        pg.wait_for_timeout(60)
        after = pg.evaluate(MEASURE)
        d = {k: after[k] - before[k] for k in tot}
        for k in tot:
            tot[k] += max(0, d[k])
        if any(d[k] > 0 for k in tot):
            bad.append((f, before, after, n))
        if i % 25 == 0:
            out.write(f"   … {i}/{len(files)}\n"); out.flush()
    b.close()

out.write(f"\n■ 영어 슬롯을 {int((RATIO-1)*100)}% 늘려 봄 · 화면 {W}px · {len(files)}쪽\n")
out.write("   (일부러 넓은 쪽 3개는 뺐습니다. 늘어난 만큼만 셉니다)\n\n")
out.write(f"   쪽이 가로로 밀림    {tot['pageOver']:>6}px\n")
out.write(f"   상자 밖으로 나감    {tot['outBox']:>6}개\n")
out.write(f"   높이 매인 상자 넘침 {tot['fixedOver']:>6}개\n")
out.write(f"\n■ 나빠진 쪽 {len(bad)}개\n")
for f, b0, a0, n in bad[:14]:
    out.write(f"   {f[:40]:<42} 슬롯{n:>4}  밀림 {b0['pageOver']}→{a0['pageOver']}"
              f" · 밖 {b0['outBox']}→{a0['outBox']} · 넘침 {b0['fixedOver']}→{a0['fixedOver']}\n")
out.flush()

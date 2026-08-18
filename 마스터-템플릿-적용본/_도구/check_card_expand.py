# -*- coding: utf-8 -*-
r"""fc 카드가 정말 아래로 펴지는지 **눌러 보고 잰다**

  카드 하나를 눌러서
    ① 앞면이 그대로 보이는가 (뒤집기면 앞면이 사라진다)
    ② 뒷면이 앞면 **아래**에 오는가 (뒤집기면 같은 자리를 덮는다)
    ③ 카드 높이가 늘어나는가 (210px 고정이면 안 늘어난다)
    ④ 다시 누르면 접히는가
"""
import sys, io, os, re, glob
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"

PROBE = r"""
() => {
  const c = document.querySelector('.fc-card');
  if (!c) return { err: 'fc-card 없음' };
  const f = c.querySelector('.fc-front'), b = c.querySelector('.fc-back');
  const R = el => { const r = el.getBoundingClientRect();
                    return { t: Math.round(r.top), b: Math.round(r.bottom), h: Math.round(r.height),
                             vis: getComputedStyle(el).display !== 'none' && r.height > 1 }; };
  const before = { card: R(c), front: R(f), back: R(b) };
  c.click();
  const open_ = { card: R(c), front: R(f), back: R(b) };
  c.click();
  const after = { card: R(c), front: R(f), back: R(b) };
  return { before, open: open_, after,
           hint: (c.querySelector('.fc-flip-hint') || {}).textContent || '' };
}
"""

files = sorted(f for f in os.listdir(BOOK)
               if f.lower().endswith(".html")
               and "fc-card" in open(os.path.join(BOOK, f), encoding="utf-8").read())
bad = 0
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 390, "height": 900})
    for f in files:
        pg.goto("file:///" + os.path.join(BOOK, f).replace("\\", "/"))
        pg.wait_for_timeout(160)
        r = pg.evaluate(PROBE)
        if r.get("err"):
            print(f"   ✗ {f[:30]:<32}{r['err']}"); bad += 1; continue
        ok_front = r["open"]["front"]["vis"]                       # ① 앞면이 남는가
        ok_below = r["open"]["back"]["t"] >= r["open"]["front"]["b"] - 2   # ② 아래에 오는가
        ok_grow = r["open"]["card"]["h"] > r["before"]["card"]["h"] + 20   # ③ 키가 자라는가
        ok_shut = not r["after"]["back"]["vis"]                    # ④ 다시 누르면 접히는가
        ok_hidden = not r["before"]["back"]["vis"]                 # 처음엔 뒤가 숨는가
        allok = ok_front and ok_below and ok_grow and ok_shut and ok_hidden
        if not allok:
            bad += 1
        print(f"   {'O' if allok else '✗'} {f[:30]:<32}"
              f"닫힘 {r['before']['card']['h']:>4}px → 열림 {r['open']['card']['h']:>4}px  "
              f"앞남음 {'O' if ok_front else '✗'} 아래 {'O' if ok_below else '✗'} "
              f"자람 {'O' if ok_grow else '✗'} 접힘 {'O' if ok_shut else '✗'} "
              f"처음숨김 {'O' if ok_hidden else '✗'}  힌트 {r['hint'][:9]}")
    br.close()
print(f"\n■ {len(files)}파일 가운데 어긋남 {bad}개. 0이어야 정상입니다.")

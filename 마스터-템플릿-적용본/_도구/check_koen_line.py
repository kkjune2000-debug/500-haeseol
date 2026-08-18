# -*- coding: utf-8 -*-
"""한국어 문장과 영어가 **같은 줄**에 있는 곳. 2026-08-18 작성.

    python check_koen_line.py                넓은 화면(1280px)
    python check_koen_line.py --width 390    휴대폰 화면

규칙(사용자 지시, 2026-08-18)
    「한국어 한 줄, 영어 한 줄, 한 줄에 한국어 두 문장이 없게 하라」

★★ 왜 소스를 읽지 않고 재는가 — 그물이 양쪽으로 틀렸다
  ① 소스에서 「한국어…<span lang=en>영어」를 찾으면 **헛걸린다**.
     그 span 이 display:block 이면 이미 줄이 갈려 있다
     (.ci-rule-desc .en · .cx-ex em · _음성 확인의 .en 이 그랬다).
  ② 문장 끝(니다.)으로만 찾으면 **놓친다**.
     .cr-en 은 15파일에서 inline 인데 문장 그물에는 1줄만 걸렸다.
  그래서 브라우저에 그려 놓고 **줄상자(line box)** 를 잰다.

재는 법
  글자마디마다 Range 로 사각형을 얻어 (가장 가까운 덩이요소, top) 로 묶는다.
  → 한 묶음 = 화면의 한 줄. 칸이 다르면 top 이 같아도 따로 센다(표는 정상).
  그 줄에 한국어 **문장**이 끝난 뒤 영어 낱말 셋 이상이 오면 걸린다.

★ 세 번째로 틀릴 뻔한 자리 — 접힌 글자마디
  getClientRects() 는 줄마다 사각형을 주지만 **글은 갈라 주지 않는다**.
  마디의 글 전체를 줄마다 넣으면 넉 줄로 접힌 문단이 넉 줄 모두에
  한국어와 영어를 다 가진 것처럼 보인다(390px 76곳 · 1280px 6곳으로 갈려 들켰다).
  그래서 여러 줄에 걸친 마디는 **글자 하나씩** 재어 줄을 가른다.

걸리지 않는 것 (일부러)
  · 낱말 짝  「가다 to go」   — 문장이 아니다
  · 이름표   「어간 + 니까 Stem + 니까」 — 낱말 셋이 안 된다
  · 표의 한국어 칸 · 영어 칸 — 덩이요소가 다르다
"""
import sys, io, os, re, argparse
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

PROBE = r"""
() => {
  const BLOCK = 'td,th,li,p,div,blockquote,h1,h2,h3,h4,h5,h6,section,figcaption,button,summary,dt,dd';
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const frags = new Map();                   // 덩이요소 → [{top,bot,left,text}]
  let n, seq = 0;
  while ((n = walker.nextNode())) {
    const t = n.nodeValue;
    if (!t || !t.trim()) continue;
    const pe = n.parentElement;
    if (!pe || /^(SCRIPT|STYLE|NOSCRIPT|TITLE)$/.test(pe.tagName)) continue;
    const cs = getComputedStyle(pe);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const host = pe.closest(BLOCK) || document.body;
    const key = host.__k || (host.__k = 'b' + (++seq));
    if (!frags.has(key)) frags.set(key, []);
    const list = frags.get(key);
    const put = (r, s) => {
      if (s.trim()) list.push({ top: r.top, bot: r.bottom, left: r.left, text: s });
    };
    const rg = document.createRange();
    rg.selectNodeContents(n);
    const rects = rg.getClientRects();
    if (rects.length <= 1) {                 // 한 줄짜리 — 그대로
      if (rects.length) put(rects[0], t);
      continue;
    }
    // ★접힌 마디는 글자 하나씩 재어 줄을 가른다
    let cur = null, buf = '';
    for (let i = 0; i < t.length; i++) {
      const c = document.createRange();
      c.setStart(n, i); c.setEnd(n, i + 1);
      const b = c.getBoundingClientRect();
      if (b.width === 0 && b.height === 0) { buf += t[i]; continue; }
      if (cur && Math.abs(b.top - cur.top) < 2) { buf += t[i]; cur.bot = Math.max(cur.bot, b.bottom); continue; }
      if (cur) put(cur, buf);
      buf = t[i]; cur = { top: b.top, bot: b.bottom, left: b.left };
    }
    if (cur) put(cur, buf);
  }
  // ★같은 줄인지는 top 이 아니라 **세로 겹침**으로 가른다.
  //   한글과 영문은 글꼴이 달라 같은 줄에서도 top 이 어긋난다(검산에서 들켰다).
  const lines = [];
  for (const list of frags.values()) {
    list.sort((a, b) => a.top - b.top || a.left - b.left);
    let cur = null;
    for (const f of list) {
      const mid = (f.top + f.bot) / 2;
      if (cur && mid > cur.top && mid < cur.bot) {
        cur.items.push(f);
        cur.top = Math.min(cur.top, f.top);
        cur.bot = Math.max(cur.bot, f.bot);
      } else {
        if (cur) lines.push(cur);
        cur = { top: f.top, bot: f.bot, items: [f] };
      }
    }
    if (cur) lines.push(cur);
  }
  return lines.map(L => L.items.sort((a, b) => a.left - b.left)
                              .map(f => f.text).join(' ').replace(/\s+/g, ' ').trim());
}
"""

KOSENT = re.compile(r"[가-힣](?:니다|세요|십시오|어요|아요|해요|군요|네요|잖아요)\s*[.!?]")
ENRUN = re.compile(r"(?:[A-Za-z][A-Za-z'’-]*(?:\s+|$)){3,}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--show", type=int, default=3, help="파일마다 보여 줄 줄 수")
    ap.add_argument("--dir", default=BOOK, help="다른 폴더를 잴 때 (그물 검산용 시험지)")
    a = ap.parse_args()

    book = a.dir
    files = sorted(f for f in os.listdir(book) if f.lower().endswith(".html"))
    tot, nf = 0, 0
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": a.width, "height": 900})
        for f in files:
            pg.goto("file:///" + os.path.join(book, f).replace("\\", "/"))
            pg.wait_for_timeout(120)
            hits = []
            for line in pg.evaluate(PROBE):
                m = KOSENT.search(line)
                if not m:
                    continue
                if ENRUN.search(line[m.end():]):
                    hits.append(line[:120])
            if hits:
                nf += 1
                tot += len(hits)
                print(f"\n=== {f}  ({len(hits)}줄)")
                for h in hits[:a.show]:
                    print("   · " + h)
                if len(hits) > a.show:
                    print(f"   … 밖 {len(hits) - a.show}줄")
        br.close()
    print(f"\n■ 모두 {tot}곳 / {nf}파일. 0곳이어야 정상입니다. (폭 {a.width}px)")


if __name__ == "__main__":
    main()

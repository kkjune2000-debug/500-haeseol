# -*- coding: utf-8 -*-
"""실제 렌더 검수 — 소스만 봐서는 절대 안 보이는 것. 2026-08-13 작성.

    python check_render.py                넓은 화면(1280px)
    python check_render.py --width 390    휴대폰 화면 — ★넘침은 여기서 난다

Playwright 가 필요하다:  pip install playwright && playwright install chromium

보는 것
  열지 못함 · 스크립트 오류 · 가로 넘침 · 상자 밖으로 나간 요소 ·
  깨진 그림 · 안 보이는 글자(글자색=바탕색) · 빈 쪽

★★ 잣대를 두 번 틀렸다 — 되풀이하지 말 것
  ① **그라데이션은 backgroundColor 가 아니라 backgroundImage 에 있다.**
     그것을 안 보면 「흰 글자 + 그라데이션 머리」가 전부 「안 보이는 글자」로 걸린다
     (2026-08-13에 13파일이 그렇게 헛걸렸다).
  ② **opacity:0 은 이 책에서 정상이다** — 필요할 때 나타나는 쪽지(음성 안내)다.

★ 일부러 넓은 쪽 셋은 넘쳐도 결함이 아니다 (check_spec.py 예외표와 같은 자리)
  부록 2 부정법 = A4 인쇄 낱장(210mm) · 부록 8 = 넓은 문법 맵 · _음성 확인 = 본문 아님
"""
import sys, io, os, json, re, argparse
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
BY_DESIGN = {"4 부록 2 부정법.html", "4 부록 8 기초문법총정리.html", "_음성 확인.html"}

PROBE = r"""
() => {
  const de = document.documentElement, body = document.body, vw = de.clientWidth;
  const out = { overflow: de.scrollWidth - vw, textLen: (body.innerText||'').replace(/\s+/g,'').length,
                wide: [], badImg: [], invisible: [] };
  const scrollable = el => {
    for (let p = el.parentElement; p; p = p.parentElement)
      if (/(auto|scroll)/.test(getComputedStyle(p).overflowX)) return true;
    return false;
  };
  document.querySelectorAll('table, div, section, p, h1, h2, h3, ul, pre').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    if (r.right > vw + 2 && !scrollable(el))
      out.wide.push({ tag: el.tagName, cls: (el.className||'').toString().slice(0,40),
                      right: Math.round(r.right) });
  });
  document.querySelectorAll('img').forEach(im => {
    if (im.complete && im.naturalWidth === 0) out.badImg.push((im.getAttribute('src')||'').slice(0,60));
  });
  // ★그라데이션은 backgroundImage 에 있다 — 안 보면 흰 글자가 전부 헛걸린다
  const bgOf = el => {
    for (let p = el; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      if (s.backgroundImage && s.backgroundImage !== 'none') return '(image)';
      const c = s.backgroundColor;
      if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') return c;
    }
    return 'rgb(255, 255, 255)';
  };
  document.querySelectorAll('h1,h2,h3,h4,p,span,small,strong,b,em,td,th,li,div').forEach(el => {
    let own = '';
    el.childNodes.forEach(n => { if (n.nodeType === 3) own += n.textContent; });
    if (own.trim().length < 2) return;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none') return;
    if (parseFloat(s.opacity) < 0.05) return;      // ★나타났다 사라지는 쪽지 — 정상
    if (s.color === bgOf(el) && s.webkitTextFillColor !== 'transparent')
      out.invisible.push({ t: own.trim().slice(0,40), why: s.color });
  });
  return out;
}
"""
# ★망이 안 된 것은 결함이 아니다 — 다시 돌리면 사라진다.
#  글꼴을 밖에서 받아 오므로 망이 잠깐 끊기면 console error 가 올라온다.
NET = (r"ERR_CONNECTION_(RESET|ABORTED|CLOSED|FAILED|REFUSED|TIMED_OUT)"
       r"|ERR_NETWORK_IO_SUSPENDED|ERR_NETWORK_CHANGED"
       r"|ERR_INTERNET_DISCONNECTED|ERR_NAME_NOT_RESOLVED"
       r"|ERR_TIMED_OUT|ERR_ADDRESS_UNREACHABLE|ERR_EMPTY_RESPONSE")
# ★「무엇을 못 받았다」는 console 말은 세지 않는다. 세 가지 까닭이 있다.
#  ① 그 말에는 주소가 안 실린다. 무엇이 안 왔는지 알 수 없으니 고칠 수도 없다.
#  ② 밖에서 받아 오는 것은 글꼴뿐이고, 글꼴이 안 와도 책은 대체 글꼴로 멀쩡히 나온다.
#  ③ 안에 있는 파일을 못 찾은 것은 이 그물이 아니라 다른 그물이 잡는다 —
#     그림은 badImg 가 재서 잡고, 소리는 check_all 이 번호표로 잡는다.
#  2026-08-17 에 이것 때문에 손대지도 않은 103쪽이 걸렸다. 검사기 한 판은
#  페이지 하나를 백 쪽 내내 돌려 쓰므로, 맨 처음 한 번 실패한 글꼴이
#  캐시에 앉아 나머지 전부로 번진다 — 다시 보기로도 안 지워지는 까닭이다.
FETCH = r"Failed to load resource"
IGNORE = re.compile(r"_소리/|\.mp3|net::ERR_FILE_NOT_FOUND|favicon|"
                    + FETCH + "|" + NET, re.I)


def is_bad(r):
    """이 쪽이 어느 갈래로든 걸렸는가 — 아래 groups 의 잣대와 같아야 한다."""
    return bool(r.get("fatal") or r.get("errs") or r.get("overflow", 0) > 2
                or r.get("wide") or r.get("badImg") or r.get("invisible")
                or r.get("textLen", 9999) < 300)


def render(page, fn):
    """한 쪽을 열어 재고 결과를 돌려준다.

    ★듣는 이(listener)를 반드시 걷는다. 예전에는 pageerror 를 걸기만 하고
     안 걷어서, 쪽을 넘길수록 같은 오류가 여러 번 쌓였다.
    ★쪽마다 fonts.googleapis.com 에서 글꼴을 받는다. 망이 늦으면
     「열지 못함」으로 세어져 같은 파일인데 0건과 2건을 오갔다.
     그래서 한 번 다시 열어 본다 — 두 번 다 실패해야 참으로 못 연 것이다.
     글꼴을 막으면 흔들림은 없어지지만 글자 너비가 달라져
     「가로 넘침」의 잣대가 바뀐다. 그래서 글꼴은 그대로 받는다.
    """
    errs, remote = [], []

    def on_console(m):
        if m.type == "error" and not IGNORE.search(m.text):
            errs.append("console: " + m.text[:110])

    def on_pageerror(e):
        errs.append("pageerror: " + str(e)[:110])

    # ★밖에서 받아 오는 것이 실패하면 결함으로 세지는 않되 주소는 적어 둔다.
    #  console 말에는 주소가 없으니, 나중에 「무엇이 안 왔나」를 물을 데가 여기뿐이다.
    def on_bad(u):
        if not u.startswith("file:"):
            remote.append(u[:90])

    def on_response(r):
        if r.status >= 400:
            on_bad(r.url)

    def on_failed(r):
        on_bad(r.url)

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.on("response", on_response)
    page.on("requestfailed", on_failed)
    try:
        r = None
        for tries in (1, 2):
            try:
                page.goto("file:///" + os.path.join(BOOK, fn).replace("\\", "/"),
                          wait_until="load", timeout=60000)
                # 글꼴이 다 앉아야 너비가 안 흔들린다 (늦으면 3초에서 끊는다)
                page.evaluate("() => Promise.race(["
                              "document.fonts.ready,"
                              "new Promise(r => setTimeout(r, 3000))])")
                page.wait_for_timeout(320)
                r = page.evaluate(PROBE)
                break
            except Exception as e:
                if tries == 2:
                    r = {"fatal": str(e)[:120]}
        r["file"] = fn
        r["errs"] = errs[:4]
        r["remote"] = remote[:2]
        return r
    finally:
        page.remove_listener("console", on_console)
        page.remove_listener("pageerror", on_pageerror)
        page.remove_listener("response", on_response)
        page.remove_listener("requestfailed", on_failed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-recheck", action="store_true",
                    help="걸린 쪽을 다시 보지 않는다 (흔들림까지 그대로 센다)")
    a = ap.parse_args()
    files = sorted(f for f in os.listdir(BOOK) if f.lower().endswith(".html"))
    if a.limit:
        files = files[:a.limit]
    rows = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        page = br.new_page(viewport={"width": a.width, "height": 900})
        for i, fn in enumerate(files, 1):
            rows.append(render(page, fn))
            if i % 25 == 0:
                print(f"   … {i}/{len(files)}")
        # ★한 번 걸렸다고 결함이 아니다. OneDrive 가 파일을 잠깐 놓치거나
        #   글꼴 서버가 404 를 뱉으면, 손대지도 않은 쪽 백 개가 한꺼번에 걸린다.
        #   2026-08-17 에 그렇게 103쪽이 걸렸고 다시 돌리니 0쪽이었다.
        #   그래서 걸린 쪽만 한 번 더 본다 — 두 번 다 걸려야 참으로 걸린 것이다.
        #   전부를 두 번 보지 않는 까닭은 값이다. 걸린 쪽은 대개 몇 개뿐이다.
        again = [i for i, r in enumerate(rows)
                 if is_bad(r) and r["file"] not in BY_DESIGN]
        if again and not a.no_recheck:
            print(f"   … 걸린 {len(again)}쪽을 한 번 더 봅니다")
            gone = 0
            for i in again:
                r2 = render(page, rows[i]["file"])
                gone += is_bad(rows[i]) and not is_bad(r2)
                rows[i] = r2
            if gone:
                print(f"   … 그중 {gone}쪽은 두 번째에 멀쩡했습니다 — 흔들림으로 봅니다")
        br.close()

    def pick(f):
        return [r for r in rows if f(r) and r["file"] not in BY_DESIGN]

    groups = [("열지 못함", pick(lambda r: r.get("fatal")), "fatal"),
              ("스크립트 오류", pick(lambda r: r.get("errs")), "errs"),
              ("가로 넘침", pick(lambda r: r.get("overflow", 0) > 2), "overflow"),
              ("상자 밖으로 나간 요소", pick(lambda r: r.get("wide")), "wide"),
              ("깨진 그림", pick(lambda r: r.get("badImg")), "badImg"),
              ("안 보이는 글자", pick(lambda r: r.get("invisible")), "invisible"),
              ("빈 쪽", pick(lambda r: r.get("textLen", 9999) < 300), "textLen")]
    print(f"\n■ 화면 {a.width}px · 렌더한 쪽 {len(rows)}")
    print(f"   (일부러 넓은 쪽 {len(BY_DESIGN)}개는 셈에서 뺍니다)")
    # ★밖에서 받아 오는 것이 실패한 것은 알려만 주고 세지 않는다.
    #  세면 망 사정이 나쁜 날마다 책이 망가진 것처럼 보인다.
    far = [r for r in rows if r.get("remote")]
    if far:
        print(f"   ※ 밖에서 받아 오는 것이 {len(far)}쪽에서 실패했습니다 "
              f"— 책의 결함이 아니라 망 사정입니다.")
        print(f"      보기: {far[0]['remote'][0]}")
    print("■ 결과")
    tot = 0
    for name, rs, _ in groups:
        tot += len(rs)
        print(f"   {'○' if not rs else '★'} {name:18} {len(rs):4}")
    for name, rs, key in groups:
        if not rs:
            continue
        print(f"\n── {name} ({len(rs)}) ──")
        for r in rs[:12]:
            v = r.get(key)
            if isinstance(v, list):
                v = "; ".join(json.dumps(x, ensure_ascii=False) if isinstance(x, dict) else str(x)
                              for x in v[:2])
            print(f"   {r['file'][:36]:38} {str(v)[:100]}")
    print(f"\n■ 모두 {tot}건. 0건이어야 정상입니다.")
    return 1 if tot else 0


if __name__ == "__main__":
    sys.exit(main())

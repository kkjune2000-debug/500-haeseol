# -*- coding: utf-8 -*-
r"""음원 — 소리 단추가 부르는 문장 가운데 아직 없는 것을 굽고 번호표에 잇는다

  여성 ko-KR-SunHiNeural · 남성 ko-KR-HyunsuMultilingualNeural
  edge-tts 는 무료이고 열쇠(API key)가 필요 없다.   pip install edge-tts

  구조
    _소리\f\0001.mp3  여성       _소리\m\0001.mp3  남성
    _소리\list.json 외 *.json    문장 → 번호   (내 기록용)
    각 HTML 안의  var AK_SND = {…}             그 파일이 실제로 쓰는 번호표
  ★ 브라우저가 보는 것은 HTML 안의 AK_SND 다. json 은 번호가 겹치지 않게 하려는 장부일 뿐.

쓰기
    python audio_build.py list          무엇이 없는지만 본다 (굽지 않음)
    python audio_build.py make          없는 것을 굽는다
    python audio_build.py wire          구운 번호를 각 HTML 의 AK_SND 에 잇는다
  보통 list → make → wire → check_structure.py 순으로 한다.

  ★ 소비자는 두 갈래다: ① speakKorean('…') 글자 그대로 박힌 단추
    ② 쓰기 칸(jm-box) — input 의 data-ans 를 읽어 부른다. ②는 자바스크립트가
    조립하므로 렌더해야 보인다(playwright 필요). playwright 가 없으면
    ②를 못 본다고 경고를 찍는다 — 그때의 「0개」는 「없음」이 아니라 「못 봄」이다.
"""
import asyncio, os, re, sys, json, glob, pathlib
import _paths

out = _paths.enter()
SND = _paths.SND
VOICES = {"f": "ko-KR-SunHiNeural", "m": "ko-KR-HyunsuMultilingualNeural"}
CALL = r"speakKorean\(&#39;([^&]+)&#39;\)"
FILES = sorted(glob.glob("*.html"))

# 쓰기 칸(jm-box)은 input 의 data-ans 를 읽어 speakKorean 을 부른다.
# 그 input 은 자바스크립트가 조립하므로 글자 훑기로는 안 보인다 — 렌더해서 본다.
DOM_JS = """() => {
    var snd = window.AK_SND || {};
    var need = [], seen = {};
    document.querySelectorAll('input[data-ans]').forEach(function(i){
        (i.getAttribute('data-ans') || '').split('/').forEach(function(a){
            a = a.trim();
            if (!a || seen[a] || !/[가-힣]/.test(a)) return;
            seen[a] = 1;
            if (!(a in snd)) need.push(a);
        });
    });
    return need;
}"""


def dom_wanted():
    """jm-box 파일들을 실제 브라우저로 렌더해, AK_SND 에 없는 data-ans 를 파일별로 돌려준다.
    playwright 가 없으면 None — 부르는 쪽에서 반드시 경고를 찍을 것(조용한 0 금지)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    files = [f for f in FILES if "jm-box" in open(f, encoding="utf-8").read()]
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page()
        for f in files:
            pg.goto(pathlib.Path(os.path.abspath(f)).as_uri())
            pg.wait_for_load_state("load")
            texts = pg.evaluate(DOM_JS)
            if texts:
                res[f] = texts
        b.close()
    return res


def real(t):
    """자바스크립트가 문자열을 이어 붙이는 자리( ' + e + ' )는 문장이 아니다"""
    return bool(re.search(r"[가-힣]", t)) and not re.search(r"[+\n\r]", t)


def load():
    mp = {}
    for p in sorted(glob.glob(os.path.join(SND, "*.json"))):
        mp.update(json.load(open(p, encoding="utf-8")))
    return mp


def wanted():
    need = {}
    for f in FILES:
        s = open(f, encoding="utf-8").read()
        m = re.search(r"var AK_SND = (\{.*?\});", s, flags=re.S)
        cur = json.loads(m.group(1)) if m else {}
        for t in re.findall(CALL, s):
            if t not in cur and real(t):
                need.setdefault(t, []).append(f)
    dom = dom_wanted()
    if dom is None:
        out.write("   ★ playwright 가 없어 쓰기 칸(data-ans)은 못 보았습니다 — "
                  "이 목록은 일부입니다. pip install playwright · "
                  "python -m playwright install chromium\n")
    else:
        for f, texts in dom.items():
            for t in texts:
                if f not in need.get(t, []):
                    need.setdefault(t, []).append(f)
    return need


def plan():
    mp, need = load(), wanted()
    base = max([int(v) for v in mp.values()] + [0])
    p = {t: "%04d" % (base + i + 1)
         for i, t in enumerate(t for t in need if t not in mp)}
    # 장부에는 있는데 mp3 가 디스크에 없는 것 — 중간에 죽은 make 의 흔적.
    # 장부 번호 그대로 다시 굽는다. (장부만 믿으면 조용히 소리 없는 책이 된다)
    for t in need:
        if t in mp and t not in p:
            n = mp[t]
            if not all(os.path.exists(os.path.join(SND, tag, n + ".mp3"))
                       for tag in VOICES):
                p[t] = n
    return p, need


async def bake(mp):
    import edge_tts
    sem = asyncio.Semaphore(5)

    async def one(text, vid, path):
        if os.path.exists(path) and os.path.getsize(path) > 800:
            return True   # 이미 구웠다 — 건너뛴다
        async with sem:
            for k in range(3):
                try:
                    await edge_tts.Communicate(text, vid).save(path)
                    if os.path.getsize(path) > 800:
                        return True
                except Exception:
                    pass
                await asyncio.sleep(1.0 * (k + 1))
            return False
    jobs = []
    for tag, vid in VOICES.items():
        os.makedirs(os.path.join(SND, tag), exist_ok=True)
        for t, n in mp.items():
            jobs.append(one(t, vid, os.path.join(SND, tag, n + ".mp3")))
    r = await asyncio.gather(*jobs)
    out.write(f"■ 음원 {sum(r)}/{len(r)} 완료\n")
    if sum(r) != len(r):
        out.write("   ★ 실패한 것이 있습니다. 다시 make 하십시오 (이미 구운 것은 건너뜁니다).\n")


def wire():
    mp, tot = load(), 0
    dom = dom_wanted()
    if dom is None:
        out.write("   ★ playwright 가 없어 쓰기 칸(data-ans)은 못 이었습니다 — "
                  "이 연결은 일부입니다.\n")
        dom = {}
    for f in FILES:
        s = open(f, encoding="utf-8").read()
        m = re.search(r"var AK_SND = (\{.*?\});", s, flags=re.S)
        if not m:
            continue
        cur = json.loads(m.group(1))
        add = {t: mp[t] for t in re.findall(CALL, s)
               if t not in cur and t in mp and real(t)}
        for t in dom.get(f, []):
            if t not in cur and t in mp and real(t):
                add[t] = mp[t]
        if not add:
            continue
        cur.update(add)
        s = s[:m.start(1)] + json.dumps(cur, ensure_ascii=False) + s[m.end(1):]
        open(f, "w", encoding="utf-8").write(s)
        tot += len(add)
        out.write(f"   {f[:34]:<36} +{len(add)}\n")
    out.write(f"■ 번호표 추가 {tot}개\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if sys.argv[1:] else "list"
    if cmd in ("list", "make"):
        p, need = plan()
        out.write(f"■ 소리 단추가 부르는데 번호표에 없는 문장 {len(need)}개 "
                  f"· 새로 구울 것 {len(p)}개\n")
        for t in need:
            out.write(f"   {p.get(t, '(음원 있음)'):>10}  {t[:60]}\n")
        if p and cmd == "make":
            fp = os.path.join(SND, "new.json")
            old = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else {}
            old.update(p)
            json.dump(old, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            asyncio.run(bake(p))
    elif cmd == "wire":
        wire()
    else:
        out.write(__doc__)
    out.flush()

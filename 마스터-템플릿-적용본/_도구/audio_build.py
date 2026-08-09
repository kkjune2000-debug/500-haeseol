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
"""
import asyncio, os, re, sys, json, glob
import _paths

out = _paths.enter()
SND = _paths.SND
VOICES = {"f": "ko-KR-SunHiNeural", "m": "ko-KR-HyunsuMultilingualNeural"}
CALL = r"speakKorean\(&#39;([^&]+)&#39;\)"
FILES = sorted(glob.glob("*.html"))


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
    return need


def plan():
    mp, need = load(), wanted()
    base = max([int(v) for v in mp.values()] + [0])
    return {t: "%04d" % (base + i + 1)
            for i, t in enumerate(t for t in need if t not in mp)}, need


async def bake(mp):
    import edge_tts
    sem = asyncio.Semaphore(5)

    async def one(text, vid, path):
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
    for f in FILES:
        s = open(f, encoding="utf-8").read()
        m = re.search(r"var AK_SND = (\{.*?\});", s, flags=re.S)
        if not m:
            continue
        cur = json.loads(m.group(1))
        add = {t: mp[t] for t in re.findall(CALL, s)
               if t not in cur and t in mp and real(t)}
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

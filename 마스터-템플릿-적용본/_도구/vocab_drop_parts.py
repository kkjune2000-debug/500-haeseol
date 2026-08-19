# -*- coding: utf-8 -*-
r"""어휘에서 **부분**을 빼고 **묶음**만 남긴다 (사용자 지시 2026-08-19)

  46번 「전화·하다·전화를 하다」에서 앞 둘을 빼신 것, 39·40 「주말·지난 주말」에서
  「주말」을 빼신 것과 같은 규칙을 남은 상자에 넓힙니다.

  ★빼는 조건 — 두 가지를 **다** 채워야 합니다
    ① 그 표제어가 같은 상자의 다른 표제어 **안에** 들어 있다
    ② 그리고 정답에서 **혼자 나오는 자리가 없다**
  ②가 결정적입니다. 겹쳐 보여도 서로 다른 낱말인 곳이 있습니다 —
    40  「영화관에서 영화를」  영화 ⊂ 영화관 이지만 영화가 따로 나온다 → 둘 다 남김
    351 「한국어를 배우러 한국에」  한국 ⊂ 한국어 이지만 한국이 따로 나온다 → 둘 다 남김
    357 「운전을 하려면 운전면허증이」  운전이 따로 나온다 → 둘 다 남김

사용: python vocab_drop_parts.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv
B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"


def spans(blk):
    got = []
    for im in re.finditer(r'<span class="v-item[^"]*">', blk):
        d, i = 1, im.end()
        while d and i < len(blk):
            t = re.compile(r"</?span\b").search(blk, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        gt = blk.find(">", i - 1)
        got.append((im.start(), gt + 1 if gt >= 0 else i))
    return got


n = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for p in list(re.finditer(r'<h3><span lang="en" translate="yes">(\d+)\)[\s\S]*?'
                              r'(<div class="v-list">[\s\S]*?</div>)', s))[::-1]:
        num, blk = p.group(1), p.group(2)
        am = re.search(r'data-ans="([^"]+)"', s[p.end(2):p.end(2) + 3000])
        if not am:
            continue
        ko = am.group(1)
        sp = spans(blk)
        heads = []
        for a, e in sp:
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            heads.append((a, e, vis(hm.group(1)) if hm else ""))
        drop = []
        def cover(y):
            """묶음이 정답에서 차지하는 구간. 활용해서 통째로는 없을 수 있으므로
            (「담배를 끊다」 ← 「담배를 끊기로」) **가장 긴 앞부분**으로 찾는다."""
            for k in range(len(y), 1, -1):
                sp2 = [(m.start(), m.start() + k) for m in re.finditer(re.escape(y[:k]), ko)]
                if sp2:
                    return sp2
            return []

        # 자동으로 못 잡는 곳 — 묶음이 정답에 활용형으로만 있어 자리를 못 찾는다
        #   108 「당신은 한국어를 할 줄 압니까?」 의 「알다」 ⊂ 「~ㄹ 줄 알다」
        EXTRA = {("108", "알다")}
        for a, e, h in heads:
            # ★한 글자 표제어(봄·살·비)도 대상이다. 앞서 len<2 로 건너뛰어
            #   168 만 「봄」이 남아 145 와 어긋났다.
            if not h:
                continue
            if (num, h) in EXTRA:
                drop.append((a, e, h, "손으로 정함"))
                continue
            outer = [x for _, _, x in heads if x != h and h in x]
            if not outer:
                continue
            covered = [sp2 for y in outer for sp2 in cover(y)]
            # ② 정답에서 혼자 나오는 자리가 있는가
            alone = False
            for m in re.finditer(re.escape(h), ko):
                inside = any(m.start() >= a2 and m.start() + len(h) <= b2
                             for a2, b2 in covered)
                if not inside:
                    alone = True
                    break
            # ★묶음이 정답 어디에 있는지 못 찾으면 **빼지 않는다.**
            #   그렇게 하지 않으면 정답에 혼자 쓰인 낱말이 빠진다 —
            #     461 「병이 다 나았습니다」의 「다」(부사)가 「낫다」의 부분으로 몰렸다
            #     125 「아침을 못 먹습니다」의 「못」이 「~지 못하다」의 부분으로 몰렸다
            if not covered:
                alone = True
            if not alone:
                drop.append((a, e, h, outer[0]))
        if not drop:
            continue
        nb = blk
        for a, e, h, y in drop[::-1]:
            nb = nb[:a] + nb[e:]
        nb = re.sub(r"\s{2,}", " ", nb)
        assert 'class="v-item' in nb, f"{num}: 상자가 비었습니다"
        print(f"   [{num:>3}] {ko}")
        print(f"          전 {' · '.join(h for _, _, h in heads)}")
        print(f"          후 {' · '.join(h for _, _, h in heads if h not in [d[2] for d in drop])}"
              f"   (뺌: {', '.join(d[2] + '⊂' + d[3] for d in drop)})")
        s = s[:p.start(2)] + nb + s[p.end(2):]
        n += len(drop)
    if s != s0:
        for tg in ("span", "b", "div"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y2 = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y2, f"{tg} 짝이 어긋남 {f}"
        assert not re.search(r'<div class="v-list">\s*</div>', s), f"빈 상자 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
print(f"\n■ 뺀 표제어 {n}개")

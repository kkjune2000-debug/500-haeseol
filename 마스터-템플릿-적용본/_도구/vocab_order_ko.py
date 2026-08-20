# -*- coding: utf-8 -*-
r"""어휘 차례를 **한국어 정답 차례**로 (사용자 결정 2026-08-19)

  왜 영어 차례가 아닌가 — 뜻풀이는 translate="yes" 슬롯이라 언어판마다 글자는
  바뀌지만 **차례는 HTML 에 박혀** 안 바뀝니다. 영어 차례로 놓으면 일본어 독자는
  「일본어 뜻풀이가 영어 어순으로 늘어선 상자」를 봅니다 — 어순 해설 표의
  영어 열과 똑같은 함정입니다. 한국어 문장은 어느 판에서나 같으므로 안전합니다.

  차례 정하는 법
    ① 표제어를 정답에서 그대로 찾으면 그 자리
    ② 「~다」로 끝나면 어간(다 뗀 것)으로 찾되 **두 음절 이상일 때만** 인정
       — 한 음절 어간은 엉뚱한 데 걸린다(「오다」의 「오」가 「오늘」에 걸렸다)
    ③ 그래도 못 찾은 「~다」는 **맨 뒤**로. 한국어는 서술어가 문장 끝이다.
    ④ 「~다」도 아닌데 못 찾으면 그 상자는 **건드리지 않는다**(자리를 모르므로)

사용: python vocab_order_ko.py [--apply] [--show 40]
"""
import re, sys, glob, html, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
ap.add_argument("--show", type=int, default=40)
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


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
        # ★`</span` 까지만 맞으므로 닫는 `>` 를 마저 넘겨야 한다.
        #   안 넘기면 잘라 붙일 때 `>` 하나가 떨어져 나간다(45파일에서 들켰다).
        gt = blk.find(">", i - 1)
        got.append((im.start(), gt + 1 if gt >= 0 else i))
    return got


# 딸린 절을 만드는 어미 — 이런 것이 문장 가운데 있으면 서술어가 끝에 있다고
# 단정할 수 없다(320 「배가 아파서 병원에」 · 349 「사러 시장에」 · 360 「하려면」).
CONN = ("아서", "어서", "여서", "러", "려면", "면서", "다가", "거나", "지만",
        "으면", "아도", "어도", "자마자", "려고", "기로", "전에", "후에", "는데")


def place(h, ko):
    """정답에서 그 표제어의 자리. 못 찾으면 None, 서술어로 보이면 'P'"""
    if h in ko:
        return ko.index(h)
    if h.endswith("다") and len(h) > 1:
        stem = h[:-1].strip()
        if len(stem) >= 2 and stem in ko:      # ②
            return ko.index(stem)
        # ★묶음 서술어는 **앞부분**으로 자리를 잡는다.
        #   「배가 아프다」의 「배가」는 정답에 그대로 있다 — 그러면 딸린 절이라도 맞다.
        for k in range(len(stem) - 1, 1, -1):
            if stem[:k] in ko:
                return ko.index(stem[:k])
        return "P"                             # ③
    return None                                # ④


def cho(ch):
    """한글 한 글자의 첫소리 번호. 한글이 아니면 None"""
    return (ord(ch) - 0xAC00) // 588 if "가" <= ch <= "힣" else None


def multi_clause(ko):
    """가운데에 딸린 절을 만드는 어미가 있는가"""
    tk = ko.split()
    return any(t.rstrip(".?!").endswith(CONN) for t in tk[:-1])


stat = Counter()
work = {}
shown = 0

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    s = s0
    for p in list(re.finditer(
            r'<h3><span lang="en" translate="yes">(\d+)\)[\s\S]*?'
            r'(<div class="v-list">[\s\S]*?</div>)', s))[::-1]:
        num, blk = p.group(1), p.group(2)
        # ★data-ans 는 어휘 상자 **뒤**의 쓰기 칸에 있다 — 상자까지만 보면 못 찾는다
        am = re.search(r'data-ans="([^"]+)"', s[p.end(2):p.end(2) + 3000])
        if not am:
            stat["정답 없음"] += 1
            continue
        ko = am.group(1)
        sp = spans(blk)
        if len(sp) < 2:
            stat["한 개 이하"] += 1
            continue
        rows = []
        for idx, (a, e) in enumerate(sp):
            hm = re.search(r"<b>([\s\S]*?)</b>", blk[a:e])
            h = vis(hm.group(1)) if hm else ""
            rows.append({"i": idx, "a": a, "e": e, "h": h,
                         "html": blk[a:e], "p": place(h, ko)})
        if any(r["p"] is None for r in rows):
            stat["자리를 모르는 표제어가 있음"] += 1
            continue
        # ★서술어로 밀어 넣은 것이 **둘 이상이면 손대지 않는다.**
        #   그것들 사이의 차례를 알 길이 없다. 실제로 틀렸다 —
        #     84 「오늘은 춥고 바람이 불고 비가 옵니다」는 절이 셋이라 서술어가 중간에 온다
        #     213 「~것 같다」와 「비가 오다」의 앞뒤를 못 가린다
        #     231 「큰 식당」의 「크다」는 서술어가 아니라 꾸미는 말이다
        if sum(1 for r in rows if r["p"] == "P") >= 2:
            stat["서술어로 보이는 것이 둘 이상"] += 1
            continue
        # ★자리를 못 찾은 서술어를 「끝」으로 미는 것은 **한 절짜리 문장에서만** 맞다.
        if any(r["p"] == "P" for r in rows) and multi_clause(ko):
            stat["딸린 절이 있어 끝인지 알 수 없음"] += 1
            continue
        # ★그리고 그 서술어가 정말 **문장 끝의 그것**인지 확인한다 —
        #   첫소리(초성)가 정답 마지막 낱말과 같아야 한다.
        #     가다 ↔ 갔습니까(ㄱ) ○   팔다 ↔ 팝니다(ㅍ) ○
        #     보다 ↔ 갑니다(ㅂ≠ㄱ) ✗  하다 ↔ 않습니다(ㅎ≠ㅇ) ✗
        #   273 「신문을 보고 회사에 갑니다」와 365 「운동을 해도 … 않습니다」가
        #   그렇게 걸러진다 — 그 서술어는 딸린 절의 것이다.
        bad = False
        for r in rows:
            if r["p"] != "P":
                continue
            stem = r["h"].rstrip("다").lstrip("~").strip()
            last = ko.split()[-1].strip(".?!")
            if not stem or not last or cho(stem[0]) is None or cho(stem[0]) != cho(last[0]):
                bad = True
        if bad:
            stat["끝 서술어가 아닌 듯"] += 1
            continue
        # ★한 표제어가 다른 표제어 안에 든 상자(대학·학생·대학생)는 자리가 겹쳐
        #   차례가 뜻대로 안 정해진다. 그 상자들은 아직 사용자 결정 전이므로 둔다.
        hs = [r["h"] for r in rows]
        if any(a != b and len(a) >= 2 and a in b for a in hs for b in hs):
            stat["표제어가 서로 겹침"] += 1
            continue
        key = lambda r: (1, r["i"]) if r["p"] == "P" else (0, r["p"], r["i"])
        new = sorted(rows, key=key)
        if [r["i"] for r in new] == [r["i"] for r in rows]:
            stat["이미 그 차례"] += 1
            continue
        nb = blk[:sp[0][0]] + " ".join(r["html"] for r in new) + blk[sp[-1][1]:]
        s = s[:p.start(2)] + nb + s[p.end(2):]
        stat["차례 바꿈"] += 1
        if shown < A.show:
            shown += 1
            out.write(f"   [{num:>3}] {ko}\n"
                      f"        전 {' · '.join(r['h'] for r in rows)}\n"
                      f"        후 {' · '.join(r['h'] for r in new)}\n")
    if s != s0:
        work[f] = (s0, s); stat["파일"] += 1

# ── 검산 — 글자는 그대로, 차례만 바뀌어야 한다
for f, (o0, s) in work.items():
    for tg in ("span", "div", "b"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    if len(re.findall(r'class="v-item', s)) != len(re.findall(r'class="v-item', o0)):
        out.write(f"   ★ 어휘 항목 수 {f[:26]}\n"); stat["★"] += 1
    if sorted(vis(o0).split()) != sorted(vis(s).split()):
        out.write(f"   ★ 글자가 바뀜(차례만 바뀌어야 함) {f[:26]}\n"); stat["★"] += 1

if A.apply and not stat["★"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

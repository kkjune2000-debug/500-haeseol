# -*- coding: utf-8 -*-
r"""어휘 차례를 한국어 정답 차례로 — 남은 상자까지 (사용자 결정 2026-08-19)

  1차(vocab_order_ko.py)는 안전한 72상자만 했습니다. 여기서는 자리 찾는 법을
  넓혀 나머지까지 맞춥니다.

  자리 찾는 법
    ⓐ 괄호 주석을 뗀다 — 「부르다 (르 불규칙)」 → 「부르다」
    ⓑ 정답에 그대로 있으면 그 자리
    ⓒ 「~다」면 어간 → 어간의 앞부분(두 글자 이상) 차례로 찾는다
       (「배가 아프다」의 「배가」)
    ⓓ 그래도 못 찾으면 **첫소리로** 찾는다 — 어간 마지막 글자의 첫소리가 같은
       낱말을 정답에서 고른다. 활용으로 글자가 바뀌기 때문이다.
         보다 → 「보고」(ㅂ) · 하다 → 「해도」(ㅎ) · 오다 → 「옵니다」(ㅇ)
       ★단, **다른 표제어로 시작하는 낱말은 건너뛴다.**
         「바람이 불고」에서 「불다」(ㅂ)가 「바람이」에 걸리는 것을 막는다.
    ⓔ 「~」로 시작하거나 「/」가 든 것은 **문법 표현**이다 → 맨 뒤.
       (~아/어서 · ~고 · ~아/어 주세요 · 을/를 위해서 …)
    ⓕ 그래도 모르면 그 상자는 건드리지 않는다.

  겹치는 표제어 (대학 · 학생 · 대학생)
    안쪽 낱말이 정답에 **혼자 나오는 자리가 따로 있으면** 그 자리를 쓴다
      (「영화관에서 영화를」의 영화 — 영화관과 다른 자리).
    없으면 감싼 낱말의 자리를 물려받고 **짧은 것부터**(부분 → 전체) 놓는다.

사용: python vocab_order_ko2.py [--apply] [--show 200]
"""
import re, sys, glob, html, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
ap.add_argument("--show", type=int, default=200)
ap.add_argument("--list", action="store_true")
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
cho = lambda ch: (ord(ch) - 0xAC00) // 588 if "가" <= ch <= "힣" else None
def bare(h):
    """괄호 주석을 뗀다. 단 괄호로 **시작하는** 표제어는 그대로
       — 「(으)ㄹ 때」를 떼면 빈 문자열이 되어 아무 데나 걸린다."""
    if re.match(r"^\s*[(（]", h):
        return h.strip()
    t = re.sub(r"\s*[(（].*$", "", h).strip()
    # ★떼고 나서 두 글자가 안 되면 뗀 것이 주석이 아니었다는 뜻이다.
    #   「~(으)려고」를 떼면 「~」 하나만 남아 아무 데나 걸린다(339).
    return t if len(t) >= 2 else h.strip()
GRAM = lambda h: h.startswith("~") or "/" in h


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


jung = lambda ch: ((ord(ch) - 0xAC00) % 588) // 28 if "가" <= ch <= "힣" else None
# 활용하면서 가운뎃소리가 줄어드는 짝 (어간 → 활용형)
#   하→해 · 오→와 · 주→줘 · 이→여(기다리→기다려) · 으→어/아(쓰→써·바쁘→바빠) · 되→돼
CONTRACT = {(0, 1), (8, 9), (13, 14), (20, 6), (18, 4), (18, 0), (11, 10)}


def fits(a, b):
    """어간 글자 a 가 활용형 글자 b 로 바뀔 수 있는가"""
    ca, cb, ja, jb = cho(a), cho(b), jung(a), jung(b)
    if ca is None or cb is None or ca != cb:
        return False
    return ja == jb or (ja, jb) in CONTRACT


def by_cho(stem, ko, others):
    """어간 마지막 글자가 활용된 낱말을 정답에서 찾는다.
    ★첫소리만 보면 헐겁다 — 「주다」가 「저에게」에 걸렸다(492).
      가운뎃소리까지 보되, 줄어드는 짝(하→해)은 인정한다."""
    if not stem:
        return None
    head, last = stem[:-1], stem[-1]
    if cho(last) is None:
        return None
    pos = 0
    for tok in ko.split():
        if head and not tok.startswith(head):
            pos += len(tok) + 1
            continue
        nxt = tok[len(head):]
        if nxt and fits(last, nxt[0]) and not any(tok.startswith(x) for x in others):
            return pos
        pos += len(tok) + 1
    return None


def alts(t):
    """빗금 표제어의 갈래를 다 만든다.
    ★「아/어도」는 「아/어」+도 이지 「아」/「어도」가 아니다 — 한 음절로도 갈라 본다."""
    got = []
    J = r"[가-힣ㄱ-ㅎㅏ-ㅣ]"
    for pat in (J + r"+/" + J + r"+", J + r"/" + J):
        m = re.search(pat, t)
        if not m:
            continue
        a, b2 = m.group(0).split("/")
        for x in (a, b2):
            c = (t[:m.start()] + x + t[m.end():]).strip()
            if len(c) >= 2:
                got.append(c)
    return got


def place(h, ko, others):
    b = bare(h)
    if not b:
        return None
    if b in ko:
        return ko.index(b)
    nt = b.lstrip("~").strip()          # 「~지 않다」의 어간은 「지 않」이다
    # ★빈 문자열은 어디에나 들어 있다 — ko.index("") 는 0 이다. 반드시 막을 것.
    if nt and nt != b and nt in ko:
        return ko.index(nt)
    if nt.endswith("다") and len(nt) > 1:
        stem = nt[:-1].strip()
        if len(stem) >= 2 and stem in ko:
            return ko.index(stem)
    if b.endswith("다") and len(b) > 1:
        stem = b[:-1].strip()
        if len(stem) >= 2 and stem in ko:
            return ko.index(stem)
        for k in range(len(stem) - 1, 1, -1):
            if stem[:k] in ko:
                return ko.index(stem[:k])
        p = by_cho(stem, ko, others)
        if p is not None:
            return p
    if GRAM(b):
        t = b.lstrip("~").strip()
        if len(t) >= 2 and t in ko:      # 「~는 동안」 ← 「자는 동안」
            return ko.index(t)
        for c in alts(t):               # 「을/를 위해서」 ← 「건강을 위해서」 · 「아/어도」 ← 「많아도」
            if c in ko:
                return ko.index(c)
        return "G"
    return None


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
        am = re.search(r'data-ans="([^"]+)"', s[p.end(2):p.end(2) + 3000])
        if not am:
            stat["정답 없음"] += 1
            continue
        ko = am.group(1)
        sp = spans(blk)
        if len(sp) < 2:
            stat["한 개 이하"] += 1
            continue
        hs = [vis(re.search(r"<b>([\s\S]*?)</b>", blk[a:e]).group(1)) for a, e in sp]
        rows = []
        for idx, ((a, e), h) in enumerate(zip(sp, hs)):
            others = []
            for j, x in enumerate(hs):
                if j == idx:
                    continue
                bx = bare(x)
                if not bx:
                    continue
                others.append(bx)
                if bx.endswith("다") and len(bx) > 1:
                    others.append(bx[:-1].strip())   # 어간도 — 「읽다」의 「읽」
            rows.append({"i": idx, "h": h, "b": bare(h), "html": blk[a:e],
                         "p": place(h, ko, others)})
        if any(r["p"] is None for r in rows):
            stat["자리를 모르는 표제어"] += 1
            if A.list:
                mark = " · ".join(r["h"] + ("  ←못찾음" if r["p"] is None else "")
                                  for r in rows)
                out.write("   [" + num + "] " + ko + "\n        " + mark + "\n")
            continue

        # 겹치는 표제어 — 혼자 나오는 자리가 따로 있으면 그 자리를,
        #   없으면 감싼 것의 자리를 물려받고 **감싼 말 안에서의 차례**로 놓는다.
        #   길이로 가르면 틀린다 — 「내년 봄」의 봄(1자)이 내년(2자)보다 앞서 버렸다(168).
        for r in rows:
            r["sub"] = (1, 0)
            if r["p"] == "G" or not r["b"]:
                continue
            outer = [x for x in rows if x is not r and x["b"] and r["b"] in x["b"]
                     and r["b"] != x["b"] and x["p"] != "G"]
            if not outer:
                continue
            o1 = outer[0]
            alone = [m.start() for m in re.finditer(re.escape(r["b"]), ko)
                     if not (o1["p"] <= m.start() < o1["p"] + len(o1["b"]))]
            if alone:
                r["p"] = alone[0]                       # 혼자 나오는 자리 (영화관 ↔ 영화)
            else:
                r["p"] = o1["p"]                        # 감싼 말의 자리를 물려받고
                r["sub"] = (0, o1["b"].index(r["b"]))   # 그 안에서의 차례로 (부분 → 전체)

        BIG = len(ko) + 99
        key = lambda r: ((BIG if r["p"] == "G" else r["p"]), r["sub"][0], r["sub"][1],
                         r["i"])
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

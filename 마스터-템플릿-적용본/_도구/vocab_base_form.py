# -*- coding: utf-8 -*-
r"""어휘를 **기본형**으로 · 문법 꼬리표 삭제 (사용자 지시 2026-08-19)

  ① 「어제 = yesterday (needs no particle)」 → 「yesterday」
     어휘는 뜻만 알게 하면 됩니다.
  ② 동사·형용사의 **과거형을 기본형으로**. 영어도 그 문장의 동사에 맞춰 기본형으로.
       샀다 bought (the past of 사다)  →  사다 buy
       보았다 saw (the past of 보다)   →  보다 see

  ★문법 표현은 건드리지 않습니다 — 「~ㄹ 수 있다」·「~기로 했다」·「~아/어 보았다」·
    「~았/었으면 좋겠다」·「~ㄴ 적이 있다」·「~아/어졌다」는 그 자체가 배울 꼴입니다.
  ★「있다」·「없다」·「맛있다」는 종성이 ㅆ 이지만 **기본형**입니다 — 그물이 걸어도 아닙니다.
  ★영어는 그 문항의 **원문 문장**에 맞췄습니다(39 saw→see · 40 watched→watch).

사용: python vocab_base_form.py [--apply]
"""
import re, sys, glob, html, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()

# 문항번호 → (옛 표제어, 옛 뜻, 새 표제어, 새 뜻)
#   새 표제어가 None 이면 **그 항목을 지운다** — 기본형이 이미 그 상자에 있기 때문
FIX = [
    ("31",  "샀다",      "bought (the past of 사다)",  None, None),   # 사다 buy 가 이미 있다
    ("39",  "보았다",    "saw (the past of 보다)",     None, None),   # 보다 watch, see 가 이미 있다
    ("40",  "보았다",    "watched (the past of 보다)", None, None),   # 〃
    ("206", "좋아졌다",  "got better",                 "좋아지다", "get better"),
    ("248", "했다",      "did",                        "하다",     "do"),
    ("256", "있었다",    "was (existed)",              "있다",     "be (stay)"),
    ("260", "청소했다",  "cleaned",                    "청소하다", "clean"),
    ("261", "준비했다",  "prepared",                   "준비하다", "prepare"),
    ("263", "여행했다",  "traveled",                   "여행하다", "travel"),
    ("264", "예약했다",  "booked",                     "예약하다", "book"),
    ("266", "만났다",    "met",                        "만나다",   "meet"),
    ("269", "샤워를 했다", "took a shower",            "샤워를 하다", "take a shower"),
    ("270", "썼다",      "wrote",                      "쓰다",     "write"),
    ("368", "없었다",    "there were no",              "없다",     "there is no"),
]
DROP_TAIL = " (needs no particle)"

stat = Counter()
work = {}
gone = {}          # 파일마다 일부러 지운 어휘 항목 수

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    s = s0

    # ① 꼬리표 삭제
    if DROP_TAIL in s:
        n = s.count(DROP_TAIL)
        s = s.replace(DROP_TAIL, "")
        stat["꼬리표 삭제"] += n
        out.write(f"   {f[:26]:<28}꼬리표 {n}개 삭제\n")

    # ② 과거형 → 기본형 (문항 안에서만)
    for num, oh, og, nh, ng in FIX:
        for im in list(re.finditer(
                r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                r'(<div class="v-list">[\s\S]*?</div>)', s))[::-1]:
            blk = im.group(1)
            if f">{oh}</b>" not in blk:
                continue

            if nh is None:                      # 기본형이 이미 있으니 그 항목을 지운다
                pos = blk.rfind('<span class="v-item', 0, blk.index(f"<b>{oh}</b>"))
                d, i = 1, blk.index(">", pos) + 1
                while d and i < len(blk):
                    t = re.compile(r"</?span\b").search(blk, i)
                    if not t:
                        break
                    d += -1 if t.group(0).startswith("</") else 1
                    i = t.end()
                i = blk.find(">", i - 1) + 1 if blk[i - 1] != ">" else i
                nb = re.sub(r"\s{2,}", " ", blk[:pos] + blk[i:])
                s = s[:im.start(1)] + nb + s[im.end(1):]
                out.write(f"   [{num:>3}] {oh} {og}   →   지움 (기본형이 이미 있음)\n")
                stat["기본형"] += 1
                gone[f] = gone.get(f, 0) + 1
                break

            nb = blk.replace(f"<b>{oh}</b>", f"<b>{nh}</b>")
            # 뜻풀이는 그 항목 안에서만 바꾼다
            gpat = re.compile(r'(<b>' + re.escape(nh) + r'</b>\s*'
                              r'<span class="gloss"[^>]*>)([\s\S]*?)(</span>)')
            gm = gpat.search(nb)
            if not gm:
                out.write(f"   X {num} 뜻풀이 자리를 못 찾음\n"); stat["어긋남"] += 1; continue
            if vis(gm.group(2)) != og:
                out.write(f"   X {num} 뜻이 다름: 「{vis(gm.group(2))}」 (바라던 「{og}」)\n")
                stat["어긋남"] += 1; continue
            nb = nb[:gm.start(2)] + ng + nb[gm.end(2):]
            s = s[:im.start(1)] + nb + s[im.end(1):]
            out.write(f"   [{num:>3}] {oh} {og}   →   {nh} {ng}\n")
            stat["기본형"] += 1
            break
        else:
            out.write(f"   X {num} 「{oh}」 못 찾음 ({f[:20]})\n") if False else None

    if s != s0:
        work[f] = (s0, s); stat["파일"] += 1

# ── 검산
for f, (o0, s) in work.items():
    for tg in ("span", "div", "b"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    d = len(re.findall(r'class="v-item', o0)) - len(re.findall(r'class="v-item', s))
    if d != gone.get(f, 0):
        out.write(f"   ★ 어휘 항목이 {d}개 줄었는데 지우려던 것은 "
                  f"{gone.get(f, 0)}개 {f[:26]}\n")
        stat["★"] += 1

done = {x[0] for x in FIX}
if stat["기본형"] != len(FIX):
    out.write(f"   ★ 바꾼 것 {stat['기본형']}개 (바라던 {len(FIX)}개)\n"); stat["★"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

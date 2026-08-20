# -*- coding: utf-8 -*-
r"""어순 해설 표 → 「문장 사다리」 — 책 전체 (사용자 승인 2026-08-19)

  전  표 4열  영어 | 역할 | 한국어 | 해설
      · 영어 열(1,518칸)은 data-reauthor — 언어마다 사람이 **다시 써야** 하는 자리
      · 줄 차례가 영어 어순이라 SOV 언어판에서는 줄을 다시 배열해야 함
      · 500표 × 36언어 = 18,000장

  후  제목(그대로) + 문장 사다리 + 만들기
      · 한 단 = 한국어 한 줄 / 그 언어 한 줄 → **문장 단위 번역**
      · 이름표는 그 문장의 어순 전체, 이번에 늘어난 자리만 진하게
      · 만들기는 자리마다 한 줄, 제목의 어순과 **같은 차례** — 한국어뿐이라 번역 비용 0
      · 표가 아니므로 가로 스크롤(.tbl-scroll)이 필요 없음

★★ 사다리를 아무 데나 놓으면 안 된다 — 기계로 뽑아 보고 알았다
   목적어까지 빼면 한국어도 영어도 망가진다(257곳을 뽑아 눈으로 봤다).
     「저는 듣습니다 / I listen to.」   「그는 영화배우입니다 / He an actor.」
     「시험 범위는 입니다.」            「당신은 갑니까??」
   그래서 사다리는 **다음 두 곳에만** 놓는다.
     ㉠ 교재가 이미 앞 문장을 가진 곳 — 그 문장을 그대로 쓴다 (31→32→33→34)
        · 앞 문장의 낱말이 이번 표의 자리로 **빠짐없이** 덮여야 한다.
          안 그러면 이름표가 거짓말을 한다(123→124 는 확장이 아니라 부정문이다).
     ㉡ **부사어만** 빼서 뼈대가 되는 곳 — 부사어를 빼는 것은 두 언어 모두 안전하다
   그 밖에는 한 단으로 두고 이름표를 붙이지 않는다(제목이 같은 말을 하므로).

사용: python eosun_ladder.py [--apply] [--show 8]
"""
import re, sys, html, glob, argparse
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
ap.add_argument("--show", type=int, default=6)
A = ap.parse_args()

MARK = "/* 어순 표 → 문장 사다리 (2026-08-19) */"
CSS = MARK + """
.wo-box{border:1px solid #dfe1ec;border-radius:12px;overflow:hidden;background:#fff;}
.wo-title{background:#f2f3f9;color:#3a3f57;font-weight:700;text-align:left;
  padding:10px 16px;font-size:0.95rem;line-height:1.5;}
.wo-title span{display:block;font-weight:600;font-size:0.86em;color:#5b6274;}
.wo-steps{list-style:none;margin:0;padding:6px 16px 12px;}
.wo-steps li{padding:10px 0;border-top:1px dashed #e8eaf2;}
.wo-steps li:first-child{border-top:0;}
.wo-add{display:inline-block;font-size:0.78rem;line-height:1.4;font-weight:700;
  color:#9296a5;background:#f5f3ff;border:1px solid #ddd6fe;border-radius:9px;
  padding:3px 10px;margin-bottom:6px;text-align:left;}
.wo-add em{font-style:normal;font-weight:800;color:#6d28d9;}
.wo-add small{display:block;font-weight:600;font-size:0.9em;color:#adb0bd;}
.wo-add small em{font-style:normal;font-weight:700;color:#7c66b8;}
.wo-ko{display:block;font-weight:700;font-size:1.05rem;color:#1f2430;line-height:1.6;}
.wo-en{display:block;color:#5b6274;font-size:0.9rem;margin-top:3px;line-height:1.5;}
.wo-steps li.wo-now{background:#fdfbf6;margin:0 -16px;padding-left:16px;padding-right:16px;}
.wo-now .wo-ko{color:#4c1d95;}
.wo-make{border-top:1px solid #dfe1ec;background:#faf7ff;padding:11px 16px 13px;
  font-size:0.92rem;line-height:1.6;}
.wo-make .wo-lab{display:block;font-weight:800;color:#6d28d9;margin-bottom:5px;}
.wo-make .wo-lab small{font-weight:600;color:#7c66b8;margin-left:6px;}
.wo-mk{display:block;color:#8b8f9e;padding:2px 0 2px 10px;}
.wo-mk strong{font-weight:700;color:#3a3f57;}
"""

ADV = re.compile(r"^(부사어|부사)")
PREP = {"to", "for", "of", "with", "at", "in", "on", "about", "from", "by",
        "into", "up", "out", "off", "over", "and", "or", "the", "a", "an"}

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
inner = lambda c: re.sub(r"^<t[dh][^>]*>|</t[dh]>$", "", c).strip()
toks = lambda x: [w for w in re.sub(r"[.?!]", "", x).split() if w]


def sub_en(sent, drops):
    """원문 영어에서 뺀 자리의 영어를 덜어 낸다. 못 덜면 None(사다리 포기)"""
    s = sent
    for d in sorted([d for d in drops if d], key=len, reverse=True):
        p = re.compile(r"(?:(?<=^)|(?<=\s)|(?<=,))\s*" + re.escape(d) + r"(?=[\s,.?!]|$)", re.I)
        s2 = p.sub(" ", s, count=1)
        if s2 == s:
            return None
        s = s2
    s = re.sub(r"\s*,(\s*,)+", ",", s)
    s = re.sub(r"^[\s,]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.?!,])", r"\1", s)
    s = re.sub(r",\s*([.?!])", r"\1", s)
    if not s:
        return None
    w = toks(s)
    if len(w) < 3 or w[-1].lower() in PREP or ",," in s:
        return None
    return s[0].upper() + s[1:]


def build(num, rows, ensent, ans, items):
    """단계 목록 [(한국어, 영어, 그 단계의 자리들)] — 못 만들면 한 단"""
    one = [(ans, ensent, rows)]
    if len(rows) < 3:
        return one
    if not all((not r["en"]) or r["en"].lower() in ensent.lower() for r in rows):
        return one
    # ★ 조각이 문장을 **빠짐없이 덮어야** 뺄셈이 맞는다.
    #   495 는 한국어가 「지금 고향에」인데 영어는 "in their hometown" 뿐이어서
    #   빼고 나니 "My parents are now." 가 남았다.
    W = lambda x: Counter(w.lower().strip(",.?!'\"") for w in x.split()
                          if w.strip(",.?!'\""))
    cov = Counter()
    for r in rows:
        cov += W(r["en"])
    if cov != W(ensent):
        return one

    def cover(sent):
        """문장을 이번 표의 자리로 빠짐없이 덮는다. 못 덮으면 None"""
        tk, got, i = toks(sent), [], 0
        while i < len(tk):
            for r in rows:
                ft = toks(r["form"])
                if ft and tk[i:i + len(ft)] == ft:
                    got.append(r); i += len(ft); break
            else:
                return None
        return got

    # ㉠ 교재가 가진 앞 문장
    ch = []
    k = num
    while k - 1 in items:
        pa, pb = toks(items[k - 1]["ans"]), toks(items[k]["ans"])
        if not (len(pb) > len(pa) and all(w in pb for w in pa)):
            break
        if cover(items[k - 1]["ans"]) is None:
            break
        ch.insert(0, k - 1); k -= 1
    if ch:
        st = [(items[j]["ans"], items[j]["en"], cover(items[j]["ans"])) for j in ch]
        return st[-3:] + one

    # ㉡ 부사어만 빼기
    #  ★ 걸름망 여섯 — 전수로 뽑아 눈으로 보고 하나씩 알아낸 것들이다
    #    ㉮ 한국어는 자리를 이어 붙이지 말고 **정답에서 지운다**.
    #       이어 붙이면 표의 줄 차례가 문장 차례와 달라 어순이 뒤집힌다
    #       (「당신은 공부합니까 한국어를?」).
    #    ㉯ 마지막 낱말이 정답과 같아야 한다. 서술어가 잘리면 안 된다
    #       (「아버지는 신문을 보고.」 · 「시험 시간은 입니다.」).
    #    ㉰ 빼는 자리의 영어에 **동사·조동사가 있으면 안 된다** — 부사어가 아니다
    #       (「그는 가수이면서」를 빼자 「He an actor.」가 되었다).
    #    ㉱ 남은 영어에 쉼표가 뜨면 안 된다 (「I, so I took a taxi.」).
    #    ㉲ 「부터 ~ 까지」처럼 짝인 자리는 함께 빼거나 함께 둔다
    #       (「Sumi studied Korean hard to night.」).
    #    ㉳ 앞의 sub_en 걸름망(낱말 셋·끝이 전치사)도 그대로 쓴다.
    VERB = {"is", "are", "was", "were", "am", "be", "been", "being", "do", "does",
            "did", "have", "has", "had", "can", "could", "will", "would", "shall",
            "should", "must", "may", "might", "let", "there"}
    # ★ 자리를 덩이로 묶는다 — 관형어는 **뒤따르는 자리**에 붙는다.
    #   안 묶으면 꾸미는 말만 남아 뜻이 바뀐다
    #   (「역 옆에 있는 백화점에서」에서 백화점만 빼자 「역 옆에 있는 옷」이 되었다).
    units, mods = [], []
    for r in rows:
        if "관형" in r["role"]:
            mods.append(r); continue
        units.append((mods, r)); mods = []
    if mods:
        return one

    #   뺄 수 있는 덩이 — ㉠ 부사어는 꾸미는 말까지 통째로 ㉡ 그 밖은 꾸미는 말만
    drops = []
    for md, hd in units:
        if ADV.match(hd["role"]):
            drops.append(md + [hd])
        elif md:
            drops.append(list(md))
    if not drops or len(rows) - sum(len(g) for g in drops) < 2:
        return one

    for g in drops:                                            # ㉰
        for r in g:
            if not r["en"]:      # 영어 칸이 비면 그 자리를 영어에서 뺄 수 없다
                return one       # (495 「My parents are now.」가 그랬다)
            w = set(x.lower().strip(",.?!") for x in r["en"].split())
            if w & VERB or any(x.endswith("n't") for x in w):
                return one
    for g in drops:      # 문장 첫머리에서 빼려면 바로 뒤가 쉼표여야 한다
        for r in g:      # (「No matter how much」를 빼자 「Medicine I take,」가 되었다)
            d = r["en"]
            if d and ensent.lower().startswith(d.lower())                and not ensent[len(d):].lstrip().startswith(","):
                return one

    at = ans.split()
    def cut(dropped):
        """정답에서 그 자리들을 지운다. 못 지우면 None"""
        keep = list(at)
        for r in dropped:
            ft = r["form"].split()
            for i in range(len(keep) - len(ft) + 1):
                if [x.rstrip(".?!") for x in keep[i:i + len(ft)]] ==                    [x.rstrip(".?!") for x in ft]:
                    keep = keep[:i] + keep[i + len(ft):]; break
            else:
                return None
        if len(keep) < 2 or keep[-1] != at[-1]:                # ㉯
            return None
        return " ".join(keep)

    # ㉲ 「부터 ~ 까지」처럼 짝인 덩이는 함께
    units2, used = [], set()
    for i, g in enumerate(drops):
        if i in used:
            continue
        grp = list(g)
        for j in range(i + 1, len(drops)):
            if j in used:
                continue
            ra, rb = g[-1], drops[j][-1]
            if {ra["role"], rb["role"]} == {"부사어(시작점)", "부사어(끝점)"} or                (ra["form"].endswith("부터") and rb["form"].endswith("까지")):
                grp += drops[j]; used.add(j)
        used.add(i); units2.append(grp)
    units = units2

    st, drop = [], list(units)
    while drop:
        flat = [r for g in drop for r in g]
        ko = cut(flat)
        en = sub_en(ensent, [r["en"] for r in flat])
        if ko is None or en is None or ko == ans:
            return one
        if re.match(r"^\S+,", en) or " ," in en:              # ㉱
            return one
        st.append((ko, en, [r for r in rows if r not in flat]))
        drop.pop()
    return (st + one)[-4:]


def render(title, steps):
    lis = []
    for i, (ko, en, cur) in enumerate(steps):
        now = ' class="wo-now"' if i == len(steps) - 1 else ""
        chip = ""
        if len(steps) > 1:
            prev = steps[i - 1][2] if i else []
            add = [r for r in cur if r not in prev]
            # 자리가 다섯을 넘으면 어순 전체를 적을 수 없다 — 늘어난 자리만 적는다
            # (486 은 자리가 아홉이라 이름표가 열 줄이 되었다). 어순은 제목이 말한다.
            if len(cur) > 5 and i:
                show, pre = add, "+ "
            else:
                show, pre = cur, ""
            mk = lambda r, k: (f"<em>{r[k]}</em>" if i and r in add else r[k])
            chip = ('<span class="wo-add">' + pre
                    + " + ".join(mk(r, "role") for r in show)
                    + '<small lang="en" translate="yes">' + pre
                    + " + ".join(mk(r, "rolen") for r in show) + '</small></span>')
        lis.append(f'<li{now}>{chip}<span class="wo-ko">{ko}</span>'
                   f'<span class="wo-en" lang="en" translate="yes">{en}</span></li>')
    make = "".join('<span class="wo-mk">' + (r["make"] or r["formhtml"]) + '</span>'
                   for r in steps[-1][2])
    return ('<div class="wo-box">\n<div class="wo-title">' + title + '</div>\n'
            '<ol class="wo-steps">\n' + "\n".join(lis) + '\n</ol>\n'
            '<div class="wo-make"><span class="wo-lab">만들기'
            '<small lang="en" translate="yes">Word building</small></span>'
            + make + '</div>\n</div>')


BLK = re.compile(r'<div class="tbl-scroll">\s*<table class="exp-table">[\s\S]*?</table>\s*</div>')
stat = Counter()
shown = 0
files = sorted(glob.glob("*.html"))
before = {}

for f in files:
    s0 = open(f, encoding="utf-8").read()
    if not BLK.search(s0):
        continue
    before[f] = s0
    s = s0

    # 이 파일의 문항 목록 (앞 문장 잇기에 쓴다)
    items = {}
    for p in re.split(r'(?=<h3><span lang="en" translate="yes">\d+\))', s0)[1:]:
        m = re.match(r'<h3><span lang="en" translate="yes">(\d+)\)([\s\S]*?)</h3>', p)
        a = re.search(r'data-ans="([^"]+)"', p)
        if m and a:
            items[int(m.group(1))] = {"en": vis(m.group(2)), "ans": a.group(1).strip()}

    for m in reversed(list(BLK.finditer(s))):
        t = m.group(0)
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
        if not hs:
            out.write(f"   X {f[:24]} 문항 번호 못 찾음\n"); stat["어긋남"] += 1; continue
        num = int(hs[-1])
        if num not in items:
            out.write(f"   X {f[:24]} {num}번 정답 없음\n"); stat["어긋남"] += 1; continue

        rows = []
        for r in re.finditer(r"<tr[\s\S]*?</tr>", t):
            if "<th" in r.group(0):
                continue
            cs = re.findall(r"<t[dh][\s\S]*?</t[dh]>", r.group(0))
            if len(cs) < 3:
                continue
            # ★ 역할 한국어 = 칸에서 **영어 슬롯을 걷어낸 나머지**.
            #   <small> 만 걷으면 거꾸로 된 칸에서 영어를 집는다
            #   (166 은 영어가 앞, 한국어가 <small> 안이었다).
            ro = cs[1]
            for _ in range(4):
                ro = re.sub(r'<(span|small|em|b|i)\b[^>]*lang="en"[^>]*>[\s\S]*?</\1>',
                            "", ro)
            ro = vis(ro)
            rn = re.search(r'lang="en" translate="yes">([^<]*)<', cs[1])
            rows.append({"en": vis(cs[0]), "role": ro,
                         "rolen": rn.group(1).strip() if rn else "",
                         "form": vis(cs[2]), "formhtml": inner(cs[2]),
                         "make": inner(cs[3]).strip() if len(cs) > 3 else ""})
        if not rows:
            out.write(f"   X {f[:24]} {num}번 줄 없음\n"); stat["어긋남"] += 1; continue

        steps = build(num, rows, items[num]["en"], items[num]["ans"], items)
        stat[f"{len(steps)}단"] += 1
        title = re.search(r'<th colspan="4"[^>]*>([\s\S]*?)</th>', t).group(1).strip()
        s = s[:m.start()] + render(title, steps) + s[m.end():]
        stat["바꾼 표"] += 1

        if len(steps) > 1 and shown < A.show:
            shown += 1
            out.write(f"   [{num}] {vis(title)[:52]}\n")
            for ko, en, _ in steps:
                out.write(f"        {ko:<34}{en}\n")

    if MARK not in s:
        b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
        e = b[-1].end() - len("</style>")
        s = s[:e] + "\n" + CSS + s[e:]
        stat["CSS"] += 1
    before[f] = (s0, s)

# ── 검산
for f, (o0, s) in before.items():
    if s == o0:
        continue
    for tg in ("div", "span", "ol", "li", "table", "style", "small", "em", "strong"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 안 맞음 {f[:26]}\n"); stat["★"] += 1
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write(f"   ★ CSS 중괄호 {f[:26]}\n"); stat["★"] += 1
    if vis(s).count(">") != vis(o0).count(">") or vis(s).count("<") != vis(o0).count("<"):
        out.write(f"   ★ 보이는 꺾쇠 {f[:26]}\n"); stat["★"] += 1
    if re.search(r'<table class="exp-table">', s):
        out.write(f"   ★ 표가 남음 {f[:26]}\n"); stat["★"] += 1
    if "??" in vis(s) and "??" not in vis(o0):
        out.write(f"   ★ 물음표 겹침 {f[:26]}\n"); stat["★"] += 1
    stat["파일"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in before.items():
        if s != o0:
            open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

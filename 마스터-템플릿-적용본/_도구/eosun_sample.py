# -*- coding: utf-8 -*-
r"""어순 해설 표 → 「문장 사다리」 시안 (㉰안) — 3 031~040 한 파일만

  전  표 4열  영어 | 역할 | 한국어 | 해설      ← 줄 차례가 영어 어순, 영어 열은 언어마다 다시 써야 함
  후  제목 유지 + 문장 사다리(한국어 한 줄 / 그 언어 한 줄) + 만들기 줄(한국어뿐)

  · 사다리 단계는 **교재 문장 그대로** 씁니다(31→32→33→34, 35→36→37→38).
  · 39·40 은 교재에 앞 문장이 없어 뼈대 한 줄을 새로 씁니다 — 나머지 483문항이 이 꼴입니다.
  · 단계마다 무엇이 늘었는지를 역할 이름표로 보입니다(+ 목적어). 이름표는 지금 표의
    역할 열에서 그대로 가져옵니다 — 지어낸 말이 없습니다.
  · 만들기 줄은 지금 표의 해설 열을 이은 것입니다. 한국어뿐이라 36언어에서 번역 비용 0.

사용: python eosun_sample.py [--apply]
"""
import re, sys, html
from collections import Counter
sys.path.insert(0, r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\_도구")
import _paths

out = _paths.enter()
APPLY = "--apply" in sys.argv
F = "3 031~040 문장구조 시간 장소 목적어 동사.html"

MARK = "/* 어순 표 → 문장 사다리 시안 (2026-08-19) */"
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

# ── 교재에 앞 문장이 없는 문항에 새로 쓴 뼈대 (설명 자리이므로 교재 밖도 됨)
BASE = {39: ("우리는 보았습니다.", "We saw."),
        40: ("우리는 보았습니다.", "We saw.")}

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
inner = lambda c: re.sub(r"^<t[dh][^>]*>|</t[dh]>$", "", c).strip()

s = open(F, encoding="utf-8").read()
o = s
stat = Counter()

# ── ① 문항마다 정답·영어·표를 모은다
parts = re.split(r'(?=<h3><span lang="en" translate="yes">\d+\))', s)
items = {}
for p in parts[1:]:
    m = re.match(r'<h3><span lang="en" translate="yes">(\d+)\)([\s\S]*?)</h3>', p)
    a = re.search(r'data-ans="([^"]+)"', p)
    if not m or not a:
        continue
    items[int(m.group(1))] = {"en": vis(m.group(2)), "ans": a.group(1)}
out.write(f"■ 문항 {len(items)}개\n")

words = lambda x: [w for w in re.sub(r"[.?!]", "", x).split() if w]


def chain(n):
    """앞 문항을 늘린 것이면 사다리로 잇는다"""
    c = [n]
    while True:
        k = c[0]
        if k - 1 not in items:
            break
        a, b = words(items[k - 1]["ans"]), words(items[k]["ans"])
        if not (len(b) > len(a) and all(w in b for w in a)):
            break
        c.insert(0, k - 1)
    return c


# ── ② 표를 찾아 사다리로 바꾼다 (뒤에서 앞으로)
tables = [m for m in re.finditer(r'<div class="tbl-scroll">\s*<table class="exp-table">[\s\S]*?</table>\s*</div>', s)]
out.write(f"■ 어순 표 {len(tables)}개\n\n")
if len(tables) != len(items):
    out.write(f"   ✗ 표 수가 문항 수와 다름\n"); stat["어긋남"] += 1

for m in reversed(tables):
    t = m.group(0)
    num = None
    for n in items:                                    # 이 표가 몇 번 문항인지
        if f'>{n})' in s[:m.start()][-4000:] or True:
            pass
    # 표 앞쪽에서 가장 가까운 <h3> 번호
    hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
    num = int(hs[-1])
    it = items[num]

    # 역할·형태·해설 뽑기
    rows = []
    for r in re.finditer(r"<tr[\s\S]*?</tr>", t):
        cs = re.findall(r"<td[\s\S]*?</td>", r.group(0))
        if len(cs) < 4:
            continue
        ko_role = vis(cs[1]).split()[0]
        en_role = re.search(r'lang="en" translate="yes">([^<]*)<', cs[1])
        rows.append({"form": vis(cs[2]), "ko": ko_role,
                     "en": en_role.group(1).strip() if en_role else "",
                     "make": inner(cs[3]).strip()})
    if not rows:
        out.write(f"   ✗ {num}번 표 행 없음\n"); stat["어긋남"] += 1; continue
    forms = [r["form"] for r in rows]

    def chunks(sent):
        """문장에 있는 자리를 표 차례대로 — 낱말이 아니라 **자리** 단위"""
        tk = words(sent)
        got = []
        for r in rows:
            ft = r["form"].split()
            if any(tk[i:i + len(ft)] == ft for i in range(len(tk) - len(ft) + 1)):
                got.append(r)
        return got

    # 사다리 단계 만들기
    ch = chain(num)
    steps = [(items[k]["ans"], items[k]["en"]) for k in ch]
    if num in BASE and BASE[num][0] not in steps[0][0]:
        steps.insert(0, BASE[num])

    # 단계마다 늘어난 자리의 역할
    lis, prev = [], []
    for i, (ko, en) in enumerate(steps):
        cur = chunks(ko)
        add = cur if i == 0 else [r for r in cur if r not in prev]
        if not add:
            out.write(f"   X {num}번 {i+1}단계 늘어난 자리 없음: {ko}" + chr(10)); stat["어긋남"] += 1
        # 어순 전체를 적되 이번에 늘어난 자리는 진하게 — 무엇이 늘었는지도 함께 보인다
        mk = lambda r, k: (f"<em>{r[k]}</em>" if r in add and i else r[k])
        labk = " + ".join(mk(r, "ko") for r in cur)
        labe = " + ".join(mk(r, "en") for r in cur)
        prev = cur
        now = ' class="wo-now"' if i == len(steps) - 1 else ""
        lis.append(
            f'<li{now}><span class="wo-add">{labk}'
            f'<small lang="en" translate="yes">{labe}</small></span>'
            f'<span class="wo-ko">{ko}</span>'
            f'<span class="wo-en" lang="en" translate="yes">{en}</span></li>')

    make = "".join('<span class="wo-mk">' + r["make"] + '</span>'
                   for r in rows if r["make"])
    title = re.search(r'<th colspan="4"[^>]*>([\s\S]*?)</th>', t).group(1)
    title = re.sub(r'<span lang="en" translate="yes">', '<span lang="en" translate="yes">', title).strip()

    new = ('<div class="wo-box">\n<div class="wo-title">' + title + '</div>\n'
           '<ol class="wo-steps">\n' + "\n".join(lis) + '\n</ol>\n'
           '<div class="wo-make"><span class="wo-lab">만들기'
           '<small lang="en" translate="yes">Word building</small></span>'
           + make + '</div>\n</div>')
    s = s[:m.start()] + new + s[m.end():]
    stat["바꾼 표"] += 1

    if num in (34, 36, 40):
        out.write(f"   [{num}번]  {vis(title)[:60]}\n")
        for L in lis:
            out.write("      " + re.sub(r"\s+", " ", vis(L)) + "\n")
        out.write(f"      만들기 · {vis(make)}\n\n")

# ── ③ CSS 붙이기
if MARK not in s:
    b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
    end = b[-1].end() - len("</style>")
    s = s[:end] + "\n" + CSS + s[end:]
    stat["CSS"] += 1

# ── ④ 검산
if s != o:
    for tg in ("div", "span", "ol", "li", "table", "style", "small", "em"):
        if (len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))) != \
           (len(re.findall(rf"<{tg}\b", o)) - len(re.findall(rf"</{tg}\s*>", o))) and tg not in ("table", "ol", "li"):
            out.write(f"   ★ 균형 {tg}\n"); stat["★"] += 1
    for tg in ("table", "ol", "li", "div", "span"):
        op, cl = len(re.findall(rf"<{tg}\b", s)), len(re.findall(rf"</{tg}\s*>", s))
        if op != cl:
            out.write(f"   ★ {tg} 열림 {op} 닫힘 {cl}\n"); stat["★"] += 1
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    if css.count("{") != css.count("}"):
        out.write("   ★ CSS 중괄호\n"); stat["★"] += 1
    if vis(s).count(">") != vis(o).count(">"):
        out.write(f"   ★ 보이는 > 수  {vis(o).count('>')} → {vis(s).count('>')}\n"); stat["★"] += 1
    out.write(f"■ 남은 exp-table {len(re.findall(r'<table class="exp-table"', s))}개 (0이어야 함)\n")

    if APPLY and not stat["★"] and not stat["어긋남"]:
        open(F, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if APPLY else "\n■ 모의\n")
for k, v in stat.most_common():
    out.write(f"   {k}: {v}\n")
out.flush()

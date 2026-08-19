# -*- coding: utf-8 -*-
r"""만들기 줄의 뭉갠 띄어쓰기 되살리기 + 관형어 이름 하나로 (사용자 지시 2026-08-19)

  ① 「역옆에있 + 는」 → 「역 옆에 있 + 는」
     옛 해설 칸이 여러 낱말을 붙여 써 놓은 것을 그대로 옮겨 왔습니다.
     ★근거는 제 감이 아니라 **그 문항의 정답**입니다 — 정답에서 공백만 지운 것과
       같은 덩이를 찾아, 정답의 띄어쓰기를 그대로 되돌립니다.
       (「컴퓨터공학」처럼 정답에도 붙어 있는 것은 건드리지 않습니다.)

  ② 이름표의 관형어 이름을 제목과 같은 꼴로.
     제목은 「관형어(장소)」인데 이름표는 「장소 관형어」였습니다 → 제목 쪽으로 맞춥니다.

사용: python eosun_fix_spacing.py [--apply]
"""
import re, sys, glob, html, argparse
from collections import Counter
sys.path.insert(0, r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\_도구")
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
nosp = lambda x: x.replace(" ", "")

# ② 관형어 이름 — 「X 관형어」를 「관형어(X)」로
NAME = {"주어 관형어": "관형어(주어)", "목적어 관형어": "관형어(목적어)",
        "장소 관형어": "관형어(장소)", "시간 관형어": "관형어(시간)",
        "부사어 관형어": "관형어(부사어)"}

def spaced(ans, run):
    """정답에서 공백만 지운 글자열로 run 을 찾아, 그 자리의 띄어쓰기를 돌려준다.
    두 곳에서 걸리면 어느 것인지 알 수 없으므로 None."""
    keep = [(c, k) for k, c in enumerate(ans) if c != " "]
    flat = "".join(c for c, _ in keep)
    if flat.count(run) != 1:
        return None
    i = flat.find(run)
    return ans[keep[i][1]:keep[i + len(run) - 1][1] + 1]


stat = Counter()
work = {}

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    if 'class="wo-box"' not in s0:
        continue
    s = s0

    # ── ① 띄어쓰기 되살리기 (문항마다 정답을 근거로)
    for im in list(re.finditer(
            r'<h3><span lang="en" translate="yes">(\d+)\)[\s\S]*?'
            r'(<div class="wo-make">[\s\S]*?</div>)', s))[::-1]:
        num, blk = im.group(1), im.group(2)
        seg = s[:im.start()]
        ansm = None
        for am in re.finditer(r'data-ans="([^"]+)"', s[im.start():im.end()]):
            ansm = am
            break
        if not ansm:
            continue
        ans = ansm.group(1).strip()
        anstoks = ans.split()
        new = blk
        for run in sorted(set(re.findall(r"[가-힣]{3,}", vis(blk))), key=len, reverse=True):
            if run in ans:                      # 정답에도 붙어 있으면 그대로
                continue
            # ★정답에서 **공백만 지운 글자열**로 자리를 찾아 그 자리의 띄어쓰기를 돌려준다.
            #   낱말 단위로 맞추면 못 찾는다 — 「역옆에있」은 「역 옆에 있는」의
            #   끝 글자가 잘린 조각이다(어미 「는」이 ` + ` 뒤로 떨어져 있다).
            hit = spaced(ans, run)
            if not hit or " " not in hit:
                continue
            n = new.count(run)
            if n != 1:
                out.write(f"   X {num} 「{run}」 {n}곳 (1이어야 함)\n")
                stat["어긋남"] += 1
                continue
            new = new.replace(run, hit)
            out.write(f"   [{num}] {run}  →  {hit}\n")
            stat["띄어쓰기"] += 1
        if new != blk:
            s = s[:im.start(2)] + new + s[im.end(2):]

    # ── ② 이름표의 관형어 이름
    for old, fix in NAME.items():
        for m in list(re.finditer(r'<span class="wo-add">[\s\S]*?</span>', s))[::-1]:
            if old not in m.group(0):
                continue
            s = s[:m.start()] + m.group(0).replace(old, fix) + s[m.end():]
            stat["이름"] += m.group(0).count(old)

    if s != s0:
        work[f] = (s0, s)

# ── 검산
for f, (o0, s) in work.items():
    for tg in ("div", "span", "ol", "li", "small", "em", "strong"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    if len(re.findall(r'class="wo-mk"', s)) != len(re.findall(r'class="wo-mk"', o0)):
        out.write(f"   ★ 만들기 줄 수가 바뀜 {f[:26]}\n"); stat["★"] += 1
    if vis(s).count(">") != vis(o0).count(">"):
        out.write(f"   ★ 보이는 꺾쇠 {f[:26]}\n"); stat["★"] += 1
    if nosp(vis(s)) != nosp(vis(o0)):
        # 공백만 바뀌어야 한다 (이름 바꾼 것은 빼고)
        a, b = nosp(vis(o0)), nosp(vis(s))
        if len(a) != len(b):
            out.write(f"   ※ 글자 수 {len(a)} → {len(b)} {f[:26]} (이름 바꿈 때문이면 정상)\n")
    stat["파일"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

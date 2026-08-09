# -*- coding: utf-8 -*-
"""검사 ④ 규격 — 폭·여백·글꼴·반응형이 파일마다 같은가

가장 흔한 값을 「규격」으로 보고, 거기서 벗어난 파일을 뽑는다.
2026-08-09 에 폭 940px 이던 한 파일과 CSS 가 죽어 폭이 안 먹던 6파일을 이걸로 찾았다.

쓰기: python check_spec.py
"""
import re, glob
from collections import Counter
import _paths

out = _paths.enter()

# 바깥 상자의 이름이 갈래마다 다릅니다. `.container` 가 표준이고, 아래 셋은 갈래가 다른
# 페이지라 이름도 폭도 다릅니다. 셋 다 `margin:0 auto` 로 가운데 정렬돼 있으므로
# 화면 가득 퍼지지 않습니다 — 옛 검사기가 `.container` 라는 이름만 찾아 "폭=-" 로 잘못 알렸습니다.
# 폭을 함께 적어 두어 이 파일들의 폭이 바뀌면 그때는 잡히게 합니다.
EXCEPT = {
    "4 부록 2 부정법.html":      ("page-container", "210mm",  "A4 인쇄 낱장 (종이로 뽑는 표)"),
    "4 부록 8 기초문법총정리.html": ("sheet",          "1380px", "일부러 넓은 문법 맵"),
    "_음성 확인.html":            ("wrap",           "860px",  "브라우저 음성 진단용 (본문 아님)"),
}


def spec(s, box="container"):
    d = {}
    blocks = re.findall(r"\." + re.escape(box) + r"\s*\{([^}]*)\}", s)
    mw = None
    pads = []
    for b in blocks:
        # 폭은 **맨 처음 것**을 씁니다. 같은 이름이 `@media print` 안에서 다시 선언되며
        # (부록 2 는 인쇄용으로 width:100%) 뒤엣것을 쓰면 인쇄용 값을 화면 폭으로 잘못 읽습니다.
        x = re.search(r"max-width\s*:\s*([^;]+);", b) or re.search(r"(?<!-)\bwidth\s*:\s*([^;]+);", b)
        if x and mw is None:
            mw = x.group(1).strip()
        y = re.search(r"padding\s*:\s*([^;]+);", b)
        if y:
            pads.append(y.group(1).strip())
    d["폭"] = mw or "-"
    d["안여백"] = " / ".join(pads) if pads else "-"
    # .container 가 아닌 다른 이름을 쓰는 파일도 있으므로 파일 전체의 max-width 를 함께 본다
    all_mw = sorted(set(re.findall(r"max-width\s*:\s*(\d+px)", s)))
    d["_그밖의폭"] = ", ".join(all_mw) if all_mw else "없음"
    fs = ff = None
    for b in re.findall(r"(?:^|[}\n>])\s*body\s*\{([^}]*)\}", s):
        x = re.search(r"font-size\s*:\s*([^;]+);", b)
        if x:
            fs = x.group(1).strip()
        y = re.search(r"font-family\s*:\s*([^;]+);", b)
        if y:
            ff = y.group(1).strip()[:28]
    d["본문크기"] = fs or "-"
    d["글꼴"] = ff or "-"
    d["viewport"] = "○" if re.search(r'name="viewport"', s) else "×"
    d["반응형"] = str(len(re.findall(r"@media", s)))
    m = re.search(r'<html[^>]*lang="([^"]+)"', s)
    d["lang"] = m.group(1) if m else "-"
    d["charset"] = "○" if re.search(r'charset="?utf-8"?', s, re.I) else "×"
    return d


rows = {f: spec(open(f, encoding="utf-8").read(),
                EXCEPT[f][0] if f in EXCEPT else "container")
        for f in sorted(glob.glob("*.html"))}
# 엄격 = 같아야 하는 것 / 참고 = 페이지마다 달라도 되는 것(반응형 개수·글꼴 등)
STRICT = ["폭", "안여백", "viewport", "lang", "charset"]
INFO = ["본문크기", "글꼴", "반응형"]
# 규격은 **본문 파일에서만** 셉니다. 예외 셋을 섞으면 분포가 흐려집니다.
body_rows = {f: r for f, r in rows.items() if f not in EXCEPT}

out.write("■ 항목별 값 분포 (가장 흔한 것 = 규격)\n")
norm = {}
for k in STRICT + INFO:
    c = Counter(r[k] for r in body_rows.values())
    norm[k] = c.most_common(1)[0][0]
    out.write(f"\n   [{k}]{'' if k in STRICT else '  (참고)'}\n")
    for v, n in c.most_common(5):
        out.write(f"      {n:>4}파일  {str(v)[:60]}{' ← 규격' if v == norm[k] else ''}\n")

out.write("\n■ 규격에서 벗어난 파일\n")
bad = 0
for f, r in body_rows.items():
    diff = [f"{k}={r[k]}" for k in STRICT if r[k] != norm[k]]
    if diff:
        bad += 1
        out.write(f"   {f[:42]:<44} {' · '.join(diff)[:88]}"
                  f"   (파일 전체 max-width: {r['_그밖의폭']})\n")
out.write(f"   총 {bad}파일 / {len(body_rows)}\n")

out.write("\n■ 알고 있는 예외 (갈래가 다른 페이지 — 폭이 바뀌면 여기서 잡힙니다)\n")
for f, (box, want, why) in EXCEPT.items():
    r = rows.get(f)
    if r is None:
        bad += 1
        out.write(f"   [파일 없음] {f}\n")
        continue
    ok = r["폭"] == want
    if not ok:
        bad += 1
    other = [f"{k}={r[k]}" for k in ("viewport", "lang", "charset") if r[k] != norm[k]]
    if other:
        bad += 1
    out.write(f"   {'○' if ok and not other else '✗'} {f[:34]:<36} .{box} {r['폭']}"
              f"{'' if ok else f' ← {want} 이어야 합니다'}"
              f"{(' · ' + ' · '.join(other)) if other else ''}   {why}\n")

out.write(f"\n■ 규격 문제 {bad}건\n")
out.write("   ※ 폭=- 는 바깥 상자 규칙을 못 찾았다는 뜻입니다. 이름이 다른지, CSS 가 죽었는지 보십시오.\n")
out.flush()

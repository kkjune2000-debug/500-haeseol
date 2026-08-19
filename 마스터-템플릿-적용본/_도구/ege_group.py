# -*- coding: utf-8 -*-
r"""「에게」와 「에」를 바탕색으로 가른다 (사용자 지시 2026-08-19)

  전  줄마다 번갈아 칠하는 얼룩무늬(nth-child even)라 두 무리가 안 갈렸다.
  후  사람·동물(에게) 한 색 · 식물·건물·장소(에) 한 색.

  ★색은 새로 짓지 않고 **책이 이미 쓰는 짝**을 가져온다 —
    「2 조사 C 에게 에.html」의 이름표가
      .pb-badge.pb-p {background:#dbeafe; color:#1e40af}   ← 사람·동물 = 에게 (파랑)
      .pb-badge.pb-t {background:#fef3c7; color:#92400e}   ← 그 밖   = 에   (호박)
    같은 파일의 설명글도 에게를 #1e40af, 에를 #92400e 로 씁니다.
    표에는 그보다 옅은 같은 계열(#eff6ff · #fffbeb)을 깔아 글자가 묻히지 않게 합니다.

사용: python ege_group.py [--apply]
"""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 041~050 문장구조 간접목적어 직접목적어.html")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

MARK = "/* 에게 ↔ 에 를 바탕색으로 가른다 (2026-08-19) */"
CSS = MARK + """
.ege-table tbody tr.grp-ege td{background:#eff6ff;}
.ege-table tbody tr.grp-e   td{background:#fffbeb;}
.ege-table tbody tr.grp-e   td strong{color:#92400e;}
.ege-table tbody tr.grp-e.grp-first td{border-top:2px solid #fde68a;}
"""

s0 = io.open(P, encoding="utf-8").read()
s = s0

# ── 그 표를 찾는다
hits = [m for m in re.finditer(r"<table[\s\S]*?</table>", s) if "to a dog, to a cat" in m.group(0)]
assert len(hits) == 1, f"표 {len(hits)}개 (1이어야 함)"
m = hits[0]
t = m.group(0)

rows = list(re.finditer(r"<tr[\s\S]*?</tr>", t))
body = [r for r in rows if "<td" in r.group(0)]
print(f"■ 표의 몸통 줄 {len(body)}개")

nt = t
first_e = True
for r in body[::-1]:
    cells = re.findall(r"<td[\s\S]*?</td>", r.group(0))
    josa = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cells[1])).strip()
    if josa == "에게":
        cls = "grp-ege"
    elif josa == "에":
        cls = "grp-e"
    else:
        print(f"   X 조사 칸이 「{josa}」 — 에게/에 가 아님"); sys.exit(1)
    new = r.group(0).replace("<tr>", f'<tr class="{cls}">', 1)
    assert new != r.group(0), "tr 를 못 고침"
    nt = nt[:r.start()] + new + nt[r.end():]
    print(f"   {josa:<4} → {cls}")

# 무리가 바뀌는 첫 「에」 줄에 가르는 선
nt = re.sub(r'<tr class="grp-e">', '<tr class="grp-e grp-first">', nt, count=1)
nt = nt.replace('<table class="gstep-table">', '<table class="gstep-table ege-table">', 1)
assert "ege-table" in nt, "표에 클래스를 못 붙임"

s = s[:m.start()] + nt + s[m.end():]

if MARK not in s:
    b = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", s))
    e = b[-1].end() - len("</style>")
    s = s[:e] + "\n" + CSS + s[e:]

# ── 검산
for tg in ("table", "tr", "td", "th", "style"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b2 = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b2, f"{tg} 짝이 어긋남"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", " ", x)   # 스타일 속 글자는 화면 글자가 아니다
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", " ", x)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
assert vis(s) == vis(s0), "보이는 글자가 바뀌었다"
print("■ 검산 통과 — 보이는 글자는 그대로")

if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

# -*- coding: utf-8 -*-
r"""종별사 표의 알약·그러데이션을 걷고 글자만 남깁니다 — 시안 (2026-08-20).

    python pill_strip_419.py [--apply]

무엇을
    419~435 종별사 표의 첫 칸 열셋이 **그러데이션 알약**이었습니다.
        <span style="…border-radius:999px;background:linear-gradient(…);…">명</span>
    어제 관형어 시제 표에서 정한 꼴로 바꿉니다 — **글자만 두고 형태는 `.accent`**.
        <span class="accent">명</span>

왜 이 꼴인가
    어제(`e611805`) 사용자 지시로 관형어 시제 표에서 알약 여덟과 칩 넷을 걷어 냈고,
    그 결과가 지금 이렇습니다 — `<td>+ <span class="accent">ㄴ/은</span></td>`.
    같은 파일 「예문」 칸이 이미 `.accent` 로 종별사를 짚고 있어, 첫 칸도 같은 색이
    되면 **한 표 안에서 같은 것이 같은 모양**이 됩니다.

★ 화면 글자는 한 글자도 바뀌지 않습니다. 파일마다 검산합니다.
★ 시안입니다 — 나머지 일곱 표(§7-13)는 보시고 정하신 뒤에 합니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
P = os.path.join(BOOK, "3 419~435 기타 문법 종별사.html")
APPLY = "--apply" in sys.argv

PILL = re.compile(
    r'<span style="display:inline-block;padding:4px 14px;border-radius:999px;'
    r'background:linear-gradient\(135deg,#fde68a,#fcd34d\);color:#92400e;'
    r'font-weight:800;font-size:0\.9rem;">([^<]+)</span>')


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()


s0 = io.open(P, encoding="utf-8", newline="").read()
found = PILL.findall(s0)
print(f"■ 그러데이션 알약 {len(found)}개 — {' · '.join(found)}")
assert len(found) == 13, f"열셋이어야 합니다(찾은 것 {len(found)})"

s = PILL.sub(lambda m: f'<span class="accent">{m.group(1)}</span>', s0)

# ── 검산
assert vis(s) == vis(s0), "화면 글자가 바뀌었습니다"
for tg in ("span", "td", "tr", "table", "small", "strong", "em"):
    a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
    b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
    assert a == b, f"<{tg}> 짝이 어긋남"
css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
assert css.count("{") == css.count("}"), "CSS 중괄호"
tbl0 = re.search(r"<table[^>]*>(?:(?!</table>)[\s\S])*?종별사[\s\S]*?</table>", s0)
tbl = re.search(r"<table[^>]*>(?:(?!</table>)[\s\S])*?종별사[\s\S]*?</table>", s)
print(f"■ 표 마크업 {len(tbl0.group(0)):,}자 → {len(tbl.group(0)):,}자")
print(f"■ 그러데이션 {s0.count('linear-gradient')} → {s.count('linear-gradient')} (파일 전체)")

if APPLY:
    io.open(P, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 종별사 표 시안")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

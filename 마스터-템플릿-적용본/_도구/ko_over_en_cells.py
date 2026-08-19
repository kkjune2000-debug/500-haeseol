# -*- coding: utf-8 -*-
r"""「한국어 — 영어」가 한 줄인 칸을 한국어 위 · 영어 아래로 (사용자 지시 2026-08-20).

    python ko_over_en_cells.py [--apply]

무엇을
    전  학교 — school                     (한 줄)
    후  학교
        school                            (영어가 아랫줄)

    · 줄을 나누므로 사이의 대시(—)는 뺍니다. 두 줄이 되면 대시는 군더더기입니다.
    · 영어 span 에 `display:block` 을 주는 것뿐이라 **글자는 그대로**입니다.

두 가지 꼴이 있습니다
    ㉮ 단순 — <strong>학교</strong> <span><span lang=en>— school</span></span>
    ㉯ 뒤에 한국어가 더 붙은 것 — 292~295 의 「부사절 — Adverbial clause: 부사어 안에
       주어+서술어」. 한국어끼리 윗줄에 모으고 영어를 아랫줄로 내립니다.
       (영어 끝의 「:」는 줄이 갈리면 뜻이 없어 뗍니다.)

★ 이 손질은 사용자가 157~163 「📍 장소」 상자를 짚어 지시한 것입니다. 같은 꼴을
  책 전체에서 찾아 함께 합니다(규칙 지시는 한 파일이 아니라 같은 꼴 전부에).
★ 「받침 없음 / No final consonant」처럼 **대시 없이** 붙어 있는 25곳은 표 안 이름표라
  생김새가 달라 건드리지 않습니다 — 손대려면 따로 정하십시오.
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

CELL = re.compile(
    r'(<strong[^>]*>)([가-힣][^<]{0,24})(</strong>)\s*'
    r'<span style="([^"]*)">\s*<span lang="en" translate="yes">\s*—\s*([^<]{1,60})</span>'
    r'([^<]*)</span>')


def vis(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x)))


def repl(m):
    s_open, ko, s_close, style, en, tail = m.groups()
    en = en.strip().rstrip(":").strip()
    style = style.rstrip(";")
    if tail.strip():
        # ㉯ 한국어가 더 붙은 칸 — 한국어끼리 윗줄, 영어는 아랫줄
        return (f'{s_open}{ko}{s_close} <span style="{style};">{tail.strip()}'
                f'<span style="display:block;margin-top:2px;">'
                f'<span lang="en" translate="yes">{en}</span></span></span>')
    return (f'{s_open}{ko}{s_close}<span style="{style};display:block;margin-top:2px;">'
            f'<span lang="en" translate="yes">{en}</span></span>')


# ── 대시 없이 붙어 있는 칸 (2026-08-20 둘째 판)
# ★재어 보고 골랐습니다 — 같은 꼴 25곳 가운데 **12곳만** 진짜 한 줄이었습니다.
#   `.rs-sub`(12) 와 `.note-en`(1) 은 CSS 가 이미 `display:block` 이라 아랫줄입니다.
# ★390px 에서는 저절로 접혀 갈려 보입니다 — **900·1280px 에서 재야** 드러납니다.
NODASH = re.compile(
    r'(<strong[^>]*>)([가-힣][^<]{0,24})(</strong>)\s*'
    r'<span style="((?:(?!display:block)[^"])*)">\s*'
    r'<span lang="en" translate="yes">\s*([A-Za-z][^<]{1,60})</span>\s*</span>')


def repl2(m):
    s_open, ko, s_close, style, en = m.groups()
    return (f'{s_open}{ko}{s_close}<span style="{style.rstrip(";")};'
            f'display:block;margin-top:2px;">'
            f'<span lang="en" translate="yes">{en.strip()}</span></span>')


hits, tot = [], 0
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s0 = io.open(p, encoding="utf-8", newline="").read()
    n_dash, n_plain = len(CELL.findall(s0)), len(NODASH.findall(s0))
    n = n_dash + n_plain
    if not n:
        continue
    s = NODASH.sub(repl2, CELL.sub(repl, s0))
    name = os.path.basename(p)
    # ── 검산: 화면 글자에서 대시와 사이 공백만 빠진다
    v, v0 = vis(s), vis(s0)
    # ★대시는 ㉮ 꼴에만 있습니다 — 대시 없는 칸까지 함께 세면 헛경보가 납니다.
    assert v0.count("—") - v.count("—") == n_dash, \
        f"{name}: 뺀 대시 수가 {n_dash}이 아닙니다"
    # ★㉯ 는 한국어를 영어 앞으로 **옮기므로** 글자 차례가 바뀝니다.
    #   차례로 견주면 헛경보가 납니다 — **낱말 꾸러미**로 견줍니다.
    bag = lambda t: sorted(re.findall(r"[가-힣]+|[A-Za-z]+", t))
    assert bag(v) == bag(v0), f"{name}: 낱말이 늘거나 줄었습니다"
    for tg in ("span", "strong", "div"):
        x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert x == y, f"{name}: <{tg}> 짝이 어긋남"
    assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n"), \
        f"{name}: 홑 LF 가 생겼습니다"
    hits.append((p, name, s, n))
    tot += n

print(f"■ 한 줄이던 칸 {tot}곳 / {len(hits)}파일")
for _, name, _, n in hits:
    print(f"     {n:>3}곳  {name}")
if APPLY:
    for p, _, s, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("\n■ 반영했습니다 — 영어가 아랫줄로, 대시만 빠졌습니다")
else:
    print("\n※ 모의 실행입니다. 반영하려면 --apply")

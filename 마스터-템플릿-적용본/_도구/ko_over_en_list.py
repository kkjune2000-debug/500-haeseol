# -*- coding: utf-8 -*-
r"""「한국어(영어) · 한국어(영어)」 목록을 한국어 줄 / 영어 줄로 (사용자 지시 2026-08-20).

    python ko_over_en_list.py [--apply]

전  피아노(piano) · 기타(guitar) · 드럼(drums) · 북(traditional drum)
후  피아노 · 기타 · 드럼 · 북
    piano · guitar · drums · traditional drum

★ 이것이 인수인계 §5 에 적힌 **본보기 그대로**입니다 —
  「한국어 「와/과, 나/이나, ~고」 ↔ 영어 「and, or, and」 (자리끼리 대응)」.
  같은 표의 다른 두 열(동사·악기 종류)이 이미 이 꼴입니다.

함께 고치는 것
    087~096 「이 문장은 여기(here)를 씁니다.」 — **한국어 문장 안에 영어**가 들어 있습니다.
    바로 아랫줄 영어가 「This sentence uses 여기 (here).」로 이미 말하므로 괄호만 뗍니다.

★ 낱말은 하나도 안 바뀝니다 — 자리만 옮깁니다(낱말 꾸러미로 검산).
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

PAIR = re.compile(r'<strong[^>]*>([가-힣][^<]{0,14})</strong>'
                  r'<span lang="en" translate="yes">\(([^)]{1,30})\)\s*(·?)\s*</span>\s*')
CELL = re.compile(r'(<td[^>]*>)((?:' + PAIR.pattern + r')+)(</td>)')
EN = '<small class="en-line" lang="en" translate="yes"><em>%s</em></small>'


def vis(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x)))


def repl(m):
    open_td, inner, close_td = m.group(1), m.group(2), m.group(len(m.groups()))
    pairs = PAIR.findall(inner)
    ko = " · ".join(f"<strong>{k}</strong>" for k, _, _ in pairs)
    en = " · ".join(e.strip() for _, e, _ in pairs)
    return open_td + ko + "<br>" + EN % en + close_td


hits, tot = [], 0
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s0 = io.open(p, encoding="utf-8", newline="").read()
    name = os.path.basename(p)
    s, n = CELL.subn(repl, s0)
    extra = 0
    if "여기</strong><span lang=\"en\" translate=\"yes\">(here)</span>" in s:
        s = s.replace('여기</strong><span lang="en" translate="yes">(here)</span>',
                      "여기</strong>", 1)
        extra = 1
    if not n and not extra:
        continue
    v, v0 = vis(s), vis(s0)
    bag = lambda t: sorted(re.findall(r"[가-힣]+|[A-Za-z]+", t))
    if extra:
        # 「(here)」 하나만 줄어드는 것이 정상입니다
        b, b0 = bag(v), bag(v0)
        b0.remove("here")
        assert b == b0, f"{name}: 낱말이 예상과 다르게 바뀌었습니다"
    else:
        assert bag(v) == bag(v0), f"{name}: 낱말이 늘거나 줄었습니다"
    for tg in ("td", "strong", "span", "small", "em", "tr", "table"):
        x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert x == y, f"{name}: <{tg}> 짝이 어긋남"
    assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n"), \
        f"{name}: 홑 LF"
    hits.append((p, name, s, n, extra))
    tot += n + extra

print(f"■ 고칠 자리 {tot}곳 / 파일 {len(hits)}개")
for _, name, s, n, extra in hits:
    print(f"     칸 {n}개" + (f" · 문장 속 영어 {extra}곳" if extra else "") + f"  {name}")
    for m in CELL.finditer(io.open(os.path.join(BOOK, name), encoding="utf-8",
                                   newline="").read()):
        pairs = PAIR.findall(m.group(2))
        print("        " + " · ".join(k for k, _, _ in pairs)
              + "  /  " + " · ".join(e.strip() for _, e, _ in pairs))

if APPLY:
    for p, _, s, _, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("\n■ 반영했습니다")
else:
    print("\n※ 모의 실행입니다. 반영하려면 --apply")

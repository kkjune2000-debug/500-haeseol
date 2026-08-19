# -*- coding: utf-8 -*-
r"""개조식으로 적힌 설명 셋을 문장으로 (사용자 지시 2026-08-20).

    python gb_gaejosik.py [--apply]

무엇을 (인수인계 §7-14)
    300~306  「~부터 = ~부터 시작해서 (끝점 없이 출발만 명시).」
             「~까지 = until / up to (끝점만 명시).」
    362~365  「~아/어서와 같은 모음 조화 룰: …」 · 「강조 시 아무리 …와 짝.」

왜
    설명·서술은 **격식체 문장**입니다(인수인계 §5 문체). 위 넷은 명사로 끝나는 조각이라
    그 규칙에 어긋났습니다. 「룰」도 이 책이 쓰는 말이 아닙니다 — 책은 「규칙」입니다.

함께 고치는 것
    ★**「~까지」 줄은 한국어 문장 안에 영어(until / up to)를 품고 있었습니다.**
      「한국어 문장 안에 영어를 넣지 마십시오」(§5)에 어긋나고, 번역판에서 무너집니다.
    ★**362~365 상자의 태그가 깨져 있었습니다** — 첫 `<small>` 이 연 `<em>` 을 닫지 않아
      두 문단을 가로지르고, `<small>` 안에 `<small>` 이 들어 있었습니다.
      짝 검산으로는 안 잡힙니다(연 수와 닫은 수가 같아서). 상자마다 제자리에서 닫습니다.

규칙 표기(ㅏ/ㅗ → 아도)는 예문이 아니라 표기라 그대로 둡니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

EN = '<small class="en-line" lang="en" translate="yes"><em>%s</em></small>'
KO = lambda t: f'<span lang="ko" translate="no">{t}</span>'

JOBS = []

# ── 300~306 ① 부터
F1 = "3 300~306 부사어 문법 범위 부터 까지.html"
JOBS.append((F1,
    '<strong>~부터</strong> = <strong>~부터 시작해서</strong> (끝점 없이 출발만 명시).',
    '<strong>~부터</strong>만 쓰면 시작을 말하고 끝은 말하지 않습니다.'))
JOBS.append((F1,
    '<small class="en-line" lang="en" translate="yes"><em><strong>'
    '<span lang="ko" translate="no">부터</span> alone</strong> = '
    '<strong>starting from / since</strong> (no end point).</em></small>',
    EN % (f'{KO("부터")} on its own gives the starting point and leaves the '
          'end unsaid.')))

# ── 300~306 ② 까지
JOBS.append((F1,
    '<strong>~까지</strong> = <strong><span lang="en" translate="yes">until / up to'
    '</span></strong> (끝점만 명시).',
    '<strong>~까지</strong>만 쓰면 끝만 말합니다.'))
JOBS.append((F1,
    '<small class="en-line" lang="en" translate="yes"><em><strong>'
    '<span lang="ko" translate="no">까지</span> alone</strong> = '
    '<strong>until / up to</strong> — only the end point.</em></small>',
    EN % f'{KO("까지")} on its own gives only the end point.'))

# ── 362~365 모음 조화 상자 (태그 깨짐까지 함께)
F2 = "3 362~365 부사어 문법 예상과 다른 결과 아어도.html"
JOBS.append((F2,
    '<strong>~아/어서</strong>와 같은 모음 조화 룰: ㅏ/ㅗ → 아도, 그 외 → 어도, '
    '하다 → 해도.<br><small class="en-line" lang="en" translate="yes"><em>'
    'Same vowel-harmony rules as <strong>~<span lang="ko" translate="no">아/어서</span>'
    '</strong>: <span lang="ko" translate="no">ㅏ/ㅗ</span> → '
    '<span lang="ko" translate="no">아도</span>, other → '
    '<span lang="ko" translate="no">어도</span>, '
    '<span lang="ko" translate="no">하다</span> → '
    '<span lang="ko" translate="no">해도</span>.</small><br>'
    '강조 시 <strong>아무리</strong> <small lang="en" translate="yes">(no matter how)'
    '</small>와 짝.<br><small class="en-line" lang="en" translate="yes">'
    'Often paired with <strong><span lang="ko" translate="no">아무리</span></strong> '
    '<small>(no matter how)</small> for emphasis.</em></small>',

    '모음을 고르는 방법은 <strong>~아/어서</strong>와 같습니다.<br>'
    + EN % f'The vowel is chosen the same way as in {KO("~아/어서")}.' +
    '<br><strong>ㅏ/ㅗ → 아도 · 그 밖 → 어도 · 하다 → 해도</strong><br>'
    '강조할 때는 <strong>아무리</strong>와 함께 씁니다.<br>'
    + EN % f'For emphasis, use it together with {KO("아무리")} (no matter how).'))

# ── 반영
files, ok = {}, True
for fname, old, new in JOBS:
    p = os.path.join(BOOK, fname)
    s = files.get(p) or io.open(p, encoding="utf-8", newline="").read()
    n = s.count(old)
    print(f"  {'○' if n == 1 else '✗'} {fname[:28]}  닻 {n}개  ← {re.sub(r'<[^>]+>', '', old)[:40]}")
    if n != 1:
        ok = False
        continue
    files[p] = s.replace(old, new, 1)
assert ok, "닻이 하나가 아닌 자리가 있습니다"

KOSENT = re.compile(r"[가-힣][^<>]*?(?:니다|습니까|세요)")
for p, s in files.items():
    name = os.path.basename(p)
    s0 = io.open(p, encoding="utf-8", newline="").read()
    for tg in ("span", "small", "em", "strong", "div", "i"):
        a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert a == b, f"{name}: <{tg}> 짝이 어긋남"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
    # ★<small> 안에 <small> 이 남아 있지 않은가 (이번에 고친 결함)
    for m in re.finditer(r"<small\b[^>]*>((?:(?!</?small\b)[\s\S])*)<small\b", s):
        raise AssertionError(f"{name}: <small> 안에 <small> 이 남아 있습니다")
    # ★고친 상자에 한국어 문장이 있는가
    for m in re.finditer(r'<div class="gb[^"]*"[^>]*>[\s\S]*?</div>', s):
        g = m.group(0)
        if "부터</strong>만" in g or "까지</strong>만" in g or "모음을 고르는" in g:
            assert KOSENT.search(re.sub(r"<[^>]+>", "", g)), f"{name}: 문장이 아닙니다"
    assert "룰" not in re.sub(r"<[^>]+>", "", s), f"{name}: 「룰」이 남았습니다"

print(f"\n■ 상자 셋 · 자리 {len(JOBS)}곳 / 파일 {len(files)}개 — 검산 통과")
if APPLY:
    for p, s in files.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

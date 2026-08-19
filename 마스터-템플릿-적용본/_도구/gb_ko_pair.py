# -*- coding: utf-8 -*-
r"""영어 문장만 있던 설명 상자 일곱에 한국어 짝을 채웁니다 (사용자 결정 2026-08-20).

    python gb_ko_pair.py [--apply]

무엇을
    100~500 을 훑어 나온 일곱 상자입니다. 영어 문장은 있는데 그 뜻을 말하는 한국어
    문장이 없어, 이 책의 「한국어 한 줄 / 영어 한 줄」에 어긋나 있었습니다.
    2026-08-18 에 같은 결함 넷을 채운 전례(`7af6aa9`)와 같은 손질입니다.

    353  안 자다 ↔ 잠이 안 오다          362  있다·없다·많다·적다 앞의 이/가
    367  승리·패배는 한자어              452  입다 · 457 닫다 · 458 믿다 · 459 받다

★ 영어를 잣대로 쓰지 않습니다 — 362 의 「Korean takes the subject particle …」은
  영어를 아는 독자만 알아듣는 말이라, 한국어 안에서 가릴 수 있는 말로 다시 썼습니다
  (「가진 것이나 양은 하는 일이 아니라 상태이기 때문입니다」). 인수인계 §5.
★ 한 줄에 한국어 한 문장만 둡니다 — 「규칙 동사입니다. ㅂ이 바뀌지 않습니다」처럼
  두 문장을 한 줄에 두지 않고 한 문장으로 묶었습니다.
★ 낱말은 그 쪽이 이미 쓰는 것만 씁니다 — 「규칙 동사」·「ㄷ 유지」는 그 파일의
  핵심 문법 표에 있는 말입니다. 새 용어를 만들지 않았습니다.
★ 영어 줄 안의 한국어는 <span lang="ko" translate="no"> 로 잠급니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

EN = '<small class="en-line" lang="en" translate="yes"><em>%s</em></small>'
KO = lambda t: f'<span lang="ko" translate="no">{t}</span>'

JOBS = []

# ── 353) 저는 커피를 마시면 잠이 안 옵니다.
JOBS.append((
    "3 352~355 부사어 문법 조건 으면.html",
    '⚠️ <span lang="en" translate="yes">Negative of</span> <strong>자다</strong> '
    '(<strong><span lang="ko" translate="no">안 자다</span></strong>) '
    '<span lang="en" translate="yes">= a deliberate refusal to sleep.</span> '
    '<strong>잠이 안 오다</strong> '
    '<span lang="en" translate="yes">= wanting to sleep but unable to.</span>',
    '⚠️ <strong>안 자다</strong>는 일부러 자지 않는 것입니다.<br>'
    + EN % f'{KO("안 자다")} is choosing not to sleep.' +
    '<br><strong>잠이 안 오다</strong>는 자고 싶은데 잠이 오지 않는 것입니다.<br>'
    + EN % f'{KO("잠이 안 오다")} is wanting to sleep but not being able to.',
))

# ── 362) 돈이 없어도 행복할 수 있습니다.
JOBS.append((
    "3 362~365 부사어 문법 예상과 다른 결과 아어도.html",
    '<span lang="en" translate="yes">⚠️ Korean takes the subject particle</span> '
    '<strong>이/가</strong> (<span lang="en" translate="yes">not</span> '
    '<strong>을/를</strong>) <span lang="en" translate="yes">with these adjectives '
    '— possession/quantity is expressed as a state, not an action.</span>',
    '⚠️ <strong>있다 · 없다 · 많다 · 적다</strong> 앞에는 <strong>을/를</strong>이 아니라 '
    '<strong>이/가</strong>를 씁니다.<br>'
    + EN % (f'With {KO("있다 · 없다 · 많다 · 적다")}, use {KO("이/가")} '
            f'rather than {KO("을/를")}.') +
    '<br>가진 것이나 양은 하는 일이 아니라 상태이기 때문입니다.<br>'
    + EN % 'What you have, and how much of it there is, is a state — not something you do.',
))

# ── 367) 수미와 탁구를 쳤는데 제가 졌습니다.
JOBS.append((
    "3 366~369 부사어 문법 배경 상황 는데.html",
    '📝 <strong>승리/패배</strong> <span lang="en" translate="yes">are Sino-Korean</span> '
    '(<span lang="ko" translate="no">한자어</span>) '
    '<span lang="en" translate="yes">compounds — used in news, sports reports, '
    'formal writing. Daily speech uses</span> <strong>이기다/지다</strong>.',
    '📝 <strong>승리 · 패배</strong>는 한자어라서 신문이나 경기 소식 같은 격식 있는 글에 '
    '씁니다.<br>'
    + EN % (f'{KO("승리 · 패배")} are Sino-Korean words, used in news, sports reports '
            'and formal writing.') +
    '<br>말할 때는 <strong>이기다 · 지다</strong>를 씁니다.<br>'
    + EN % f'In everyday speech, use {KO("이기다 · 지다")}.',
))


def reg(fname, verb, jamo=None, also=False):
    """「입다 is REGULAR!」 꼴 넷 — 한국어 한 문장으로 묶어 짝을 답니다."""
    if also:
        old = (f'<strong>⚠️ <strong>{verb}</strong> '
               f'<span lang="en" translate="yes">is also REGULAR!</span></strong>')
        new_ko = f'<strong>⚠️ <strong>{verb}</strong>도 규칙 동사입니다.</strong>'
        new_en = EN % f'{KO(verb)} is also a regular verb.'
    else:
        old = (f'<strong>⚠️ <strong>{verb}</strong> '
               f'<span lang="en" translate="yes">is REGULAR!</span> {jamo} '
               f'<span lang="en" translate="yes">does NOT change!</span></strong>')
        new_ko = (f'<strong>⚠️ <strong>{verb}</strong>는 {jamo}이 바뀌지 않는 '
                  f'규칙 동사입니다.</strong>')
        new_en = EN % (f'{KO(verb)} is a regular verb — its {KO(jamo)} '
                       'does not change.')
    JOBS.append((fname, old, new_ko + "<br>" + new_en))


reg("3 449~453 기타 문법 ㅂ불규칙.html", "입다", "ㅂ")
reg("3 454~459 기타 문법 ㄷ불규칙.html", "닫다", "ㄷ")
reg("3 454~459 기타 문법 ㄷ불규칙.html", "믿다", also=True)
reg("3 454~459 기타 문법 ㄷ불규칙.html", "받다", also=True)

# ── 반영
KOSENT = re.compile(r"[가-힣][^<>]*?(?:니다|습니까|세요)")
files = {}
for fname, old, new in JOBS:
    p = os.path.join(BOOK, fname)
    s = files.get(p) or io.open(p, encoding="utf-8", newline="").read()
    n = s.count(old)
    print(f"  {'○' if n == 1 else '✗'} {fname[:26]}  닻 {n}개")
    assert n == 1, f"{fname}: 닻이 {n}개입니다(1이어야 합니다)"
    files[p] = s.replace(old, new, 1)

print(f"\n■ 상자 {len(JOBS)}개 / 파일 {len(files)}개")

for p, s in files.items():
    s0 = io.open(p, encoding="utf-8", newline="").read()
    name = os.path.basename(p)
    for tg in ("span", "small", "em", "strong", "div", "i"):
        a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert a == b, f"{name}: <{tg}> 짝이 어긋남"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
    assert "\r\n" in s if "\r\n" in s0 else True, f"{name}: 줄끝이 바뀜"
    # 손댄 상자마다 한국어 문장이 생겼는가
    for m in re.finditer(r'<div class="gb[^"]*"[^>]*>[\s\S]*?</div>', s):
        g = m.group(0)
        if "en-line" in g and ("⚠️" in g or "📝" in g):
            plain = re.sub(r"<[^>]+>", "", g)
            assert KOSENT.search(plain), f"{name}: 한국어 문장이 없는 상자가 남음"

if APPLY:
    for p, s in files.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 일곱 상자에 한국어 짝이 들어갔습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

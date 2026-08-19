# -*- coding: utf-8 -*-
r"""요일 쪽을 새로 만들고, 요일이 나오는 여섯 문항에 링크를 건다 (사용자 결정 2026-08-19)

  ① 「4 부록 9 요일.html」 — 새 쪽
       · 요일 일곱을 「카드 보고 말하기」 꼴로 (영어 → 눌러서 한국어)
       · 「~요일에」 쓰는 법 — 예문은 **교재 문장 그대로** (58·79·159·301)
       · 오늘 · 내일과 함께 쓰는 꼴 (92·93)
       ★교재에 나오는 요일은 월·수·토·일 넷뿐입니다. 요일 쪽에서 셋을 빼면
         쪽이 성립하지 않으므로 일곱을 다 넣고, 교재에 나오는 넷에 표시했습니다.
  ② 여섯 문항(58·79·92·93·159·301)의 해설 상자 **아래**에 링크를 답니다.
       이 책의 gram-link 꼴을 그대로 씁니다.

사용: python make_yoil_page.py [--apply]
"""
import io, re, sys, glob, urllib.parse

B = r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
APPLY = "--apply" in sys.argv
NEW = "4 부록 9 요일.html"

DAYS = [("월요일", "Monday", True), ("화요일", "Tuesday", False),
        ("수요일", "Wednesday", True), ("목요일", "Thursday", False),
        ("금요일", "Friday", False), ("토요일", "Saturday", True),
        ("일요일", "Sunday", True)]

SENT = [("58", "저는 <b>월요일에</b> 어학원에 갑니다.",
         "I go to the language institute on Monday."),
        ("79", "저는 <b>월요일과 수요일에</b> 한국어 학원에 갑니다.",
         "I go to the Korean language school on Monday and Wednesday."),
        ("159", "저는 <b>이번 주 일요일에</b> 영화를 보려고 합니다.",
         "I'm going to watch a movie this Sunday."),
        ("301", "<b>이번 주 월요일부터 다음 주 일요일까지</b> 휴가입니다.",
         "We have a vacation from this Monday to next Sunday.")]
SENT2 = [("92", "오늘은 <b>토요일입니다</b>.", "Today is Saturday."),
         ("93", "내일은 <b>일요일입니다</b>.", "Tomorrow is Sunday.")]


def card(ko, en, in_book):
    tag = ""      # 「교재」 딱지는 넣지 않습니다 — 학습자에게 필요 없는 표시입니다
    return ('<div class="flashcard" onclick="this.classList.toggle(\'flipped\')">'
            '<div class="flashcard-inner">'
            f'<div class="flashcard-front"><div class="flashcard-text">'
            f'<span lang="en" translate="yes">{en}</span></div>'
            '<div class="flashcard-hint">▼ 눌러서 확인</div></div>'
            f'<div class="flashcard-back"><div class="flashcard-text">{ko}{tag}</div>'
            '</div></div></div>')


def line(num, ko, en):
    return (f'<div class="yo-ex"><span class="yo-no">{num}</span>'
            f'<span class="yo-ko">{ko}</span>'
            f'<span class="yo-en" lang="en" translate="yes">{en}</span></div>')


PAGE = """<!DOCTYPE html>
<html lang="ko" translate="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title translate="yes">Amazing Korean 1 — Days of the Week</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Lato:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Noto Sans KR', sans-serif; background: #f1f5f9; color: #1e293b; line-height: 1.8; padding: 20px; word-break: keep-all; }
        .container { max-width: 800px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); padding: 48px 40px; }
        @media (max-width: 600px) { .container { padding: 20px; } body { padding: 0; background: none; } .container { box-shadow: none; } }
        .title-block { margin: 0 0 32px; padding: 8px 0 16px; border-bottom: 3px solid #0f766e; }
        .title-block h1 { font-size: 1.9rem; font-weight: 900; color: #0f766e; }
        .title-block .title-main { font-size: 1rem; font-weight: 700; color: #5b6274; }
        h2 { font-size: 1.35rem; font-weight: 800; color: #0f766e; margin: 34px 0 4px; padding-top: 20px; border-top: 2px solid #e2e8f0; }
        h2:first-of-type { border-top: none; padding-top: 0; margin-top: 0; }
        p.subtitle { color: #5b6274; font-size: 0.92rem; margin-bottom: 12px; }
        p.ko { margin-top: 10px; }
        p.en { color: #5b6274; font-size: 0.92rem; margin-bottom: 10px; }

        .flashcard-grid { display: grid; grid-template-columns: 1fr; gap: 9px; margin: 12px 0 6px; }
        .flashcard { cursor: pointer; display: flex; flex-direction: column; }
        .flashcard-inner { display: flex; flex-direction: column; }
        .flashcard-front, .flashcard-back { position: relative; border-radius: 12px; display: flex;
            flex-direction: column; align-items: center; justify-content: center; padding: 11px 14px; }
        .flashcard-front { background: #f0fdfa; border: 2px solid #99f6e4; color: #115e59; padding-bottom: 26px; }
        .flashcard-back { display: none; background: linear-gradient(135deg,#ccfbf1 0%,#99f6e4 100%); color: #134e4a; }
        .flashcard.flipped .flashcard-back { display: flex; }
        .flashcard.flipped .flashcard-front { border-bottom-left-radius: 0; border-bottom-right-radius: 0; }
        .flashcard.flipped .flashcard-back { border-top-left-radius: 0; border-top-right-radius: 0; }
        .flashcard.flipped .flashcard-hint { display: none; }
        .flashcard-text { font-size: 1rem; font-weight: 700; line-height: 1.4; }
        .flashcard-hint { position: absolute; bottom: 7px; right: 12px; font-size: 0.68rem;
            color: #5a6d87; font-weight: 600; letter-spacing: 0.1em; }
        .yo-tag { display: inline-block; margin-left: 8px; padding: 1px 8px; border-radius: 999px;
            background: rgba(255,255,255,0.7); font-size: 0.68rem; font-weight: 800; color: #0f766e; }
        .yo-tag .gloss { display: block; font-weight: 600; font-size: 0.9em; }

        .yo-ex { padding: 9px 0; border-top: 1px dashed #e8eaf2; }
        .yo-ex:first-of-type { border-top: none; }
        .yo-no { display: inline-block; min-width: 34px; font-family: 'Lato','Noto Sans KR',sans-serif;
            font-weight: 900; color: #0f766e; font-size: 0.86rem; }
        .yo-ko { display: block; font-weight: 700; font-size: 1.03rem; color: #1f2430; line-height: 1.6; }
        .yo-ko b { color: #0f766e; }
        .yo-en { display: block; color: #5b6274; font-size: 0.9rem; margin-top: 2px; }
        .gb { border: 1px solid #e6e8ef; border-left: 4px solid #14b8a6; background: #f8fafc;
            border-radius: 10px; padding: 12px 16px; margin: 12px 0; }
        .gb-lab { display: block; font-weight: 800; color: #0f766e; font-size: 0.88rem; margin-bottom: 4px; }
        .gb-lab i { display: block; font-style: normal; font-weight: 600; color: #5b6274; font-size: 0.85em; }
    </style>
</head>
<body>
<div class="container">

<header class="title-block">
    <h1>요일</h1>
    <p class="title-main" lang="en" translate="yes">Days of the Week</p>
</header>

<h2>요일 일곱<span class="gloss" lang="en" translate="yes"> · Seven days</span></h2>
<p class="ko">영어를 보고 한국어로 말해 보세요.</p>
<p class="en" lang="en" translate="yes">Look at the English and say it in Korean.</p>
<p class="ko">카드를 눌러 답을 확인하세요.</p>
<p class="en" lang="en" translate="yes">Tap the card to check your answer.</p>
<div class="flashcard-grid">{CARDS}</div>

<h2>~요일에<span class="gloss" lang="en" translate="yes"> · on ~day</span></h2>
<div class="gb"><span class="gb-lab">설명<i lang="en" translate="yes">Explanation</i></span>
요일 뒤에는 <b>에</b>를 붙입니다.<br>
<small lang="en" translate="yes">Add <span lang="ko" translate="no">에</span> after a day of the week.</small></div>
{EX1}

<h2>오늘 · 내일<span class="gloss" lang="en" translate="yes"> · Today and tomorrow</span></h2>
<div class="gb"><span class="gb-lab">설명<i lang="en" translate="yes">Explanation</i></span>
「오늘은 · 내일은」 뒤에서는 <b>에</b>를 붙이지 않습니다.<br>
<small lang="en" translate="yes">After <span lang="ko" translate="no">오늘은 · 내일은</span> do not add <span lang="ko" translate="no">에</span>.</small></div>
{EX2}

</div>
</body>
</html>
"""

page = (PAGE.replace("{CARDS}", "".join(card(k, e, b) for k, e, b in DAYS))
            .replace("{EX1}", "".join(line(n, k, e) for n, k, e in SENT))
            .replace("{EX2}", "".join(line(n, k, e) for n, k, e in SENT2)))

# ── 링크
HREF = urllib.parse.quote(NEW)
LINK = ('<a class="gram-link" href="' + HREF + '" target="_blank" rel="noopener">'
        '📘 요일<span class="gloss" lang="en" translate="yes">Days of the week</span></a>')
TARGETS = ["58", "79", "92", "93", "159", "301"]

n_link = 0
for f in sorted(glob.glob(B + r"\*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0
    for num in TARGETS:
        m = re.search(r'<h3><span lang="en" translate="yes">' + num + r'\)[\s\S]*?'
                      r'(<div class="explain-box">[\s\S]*?</div>\s*</div>)', s)
        if not m:
            continue
        if HREF in s[m.end(1):m.end(1) + 400]:
            print(f"   · {num} 이미 있음"); continue
        s = s[:m.end(1)] + "\n" + LINK + s[m.end(1):]
        n_link += 1
        print(f"   [{num}] 링크 붙임")
    if s != s0:
        for tg in ("div", "span", "a"):
            x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert x == y, f"{tg} 짝이 어긋남 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)

print(f"\n■ 새 쪽 {len(page):,}자 · 링크 {n_link}곳")
if APPLY:
    io.open(B + "\\" + NEW, "w", encoding="utf-8").write(page)
    print("■ 씀 " + NEW)

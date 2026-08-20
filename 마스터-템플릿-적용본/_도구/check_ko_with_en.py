# -*- coding: utf-8 -*-
r"""한국어 글 **안에** 영어가 박혀 있는가 (2026-08-21 신설).

    python check_ko_with_en.py

왜 따로 보는가
    `check_audit.py` 의 「슬롯 밖 영어」는 **한글이 하나도 없는** 덩이만 셉니다
    (한국어 원문 속 고유명사 TOPIK 을 거르려고 그렇게 두었습니다).
    그래서 「이 문장은 여기(here)를 씁니다.」처럼 **한국어 문장 안에 영어가 섞인** 자리는
    그 그물을 그냥 지나갑니다 — 2026-08-20 에 한 곳을 눈으로 찾았습니다.
    인수인계 §5: 「한국어 문장 안에 영어를 넣지 마십시오. 번역하면 무너집니다.」

재는 법
    HTML 을 **파서**로 읽어 글자 덩이마다 어느 슬롯 안인지 따라갑니다(정규식은 겹친
    태그에서 끊깁니다). 그리고 **한글과 라틴 낱말이 한 덩이에 함께 있는 것**만 셉니다.

거르는 것 (결함이 아닙니다)
    · `lang="en"` 슬롯 안 — 그쪽은 영어가 본디이고 한국어는 잠급니다
    · 고유명사 BTS · KTX · TOPIK · MP3 따위 대문자 약어
    · 로마자 한 글자(A·B·Ⓐ 같은 표지)와 숫자 단위
"""
import io, os, re, sys, glob, html as H
from html.parser import HTMLParser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

HANGUL = re.compile(r"[가-힣]")
LATIN = re.compile(r"[A-Za-z]{2,}")
SKIP = {"script", "style", "title"}
VOID = {"br", "hr", "img", "input", "meta", "link", "source"}
# 고유명사·표지 — 걸려도 결함이 아닙니다
ALLOW = re.compile(r"^(?:BTS|KTX|TOPIK|MP3|PDF|OK|TV|AI|CD|DVD|USB|EPS|HTML|"
                   r"[A-Z]|[IVX]+)$")


class Walk(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.lang, self.skip = [], "", 0
        self.hits = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
            return
        if tag in VOID:
            return
        d = dict(attrs)
        self.stack.append((tag, self.lang))
        if d.get("lang"):
            self.lang = d["lang"]

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, self.lang = self.stack[i]
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.skip:
            return
        t = data.strip()
        if not t or self.lang.startswith("en"):
            return
        if not HANGUL.search(t):
            return
        words = [w for w in LATIN.findall(t) if not ALLOW.match(w)]
        if words:
            self.hits.append((self.getpos()[0], t[:70], words[:4]))


tot, files = 0, 0
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s = io.open(p, encoding="utf-8", newline="", errors="replace").read()
    w = Walk()
    try:
        w.feed(s)
    except Exception as e:
        print(f"   ✗ 파싱 실패 {os.path.basename(p)}: {e}")
        continue
    if not w.hits:
        continue
    files += 1
    tot += len(w.hits)
    print(f"=== {os.path.basename(p)}  ({len(w.hits)})")
    for line, t, words in w.hits[:6]:
        print(f"   {line:>5}행  {t}   ← {' · '.join(words)}")
    if len(w.hits) > 6:
        print(f"          … 그리고 {len(w.hits)-6}곳 더")

print(f"\n■ 한국어 덩이 안에 영어가 섞인 곳 {tot}곳 / {files}파일")
print("★ 걸린 것이 다 결함은 아닙니다 — 배우는 낱말을 영어로 보이는 자리(어휘 카드 뒷면)와")
print("  가르십시오. 인수인계 §5 는 **한국어 문장 안**을 말합니다.")

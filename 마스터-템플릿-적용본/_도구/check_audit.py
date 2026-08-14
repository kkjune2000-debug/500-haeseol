# -*- coding: utf-8 -*-
"""전수 검수 — 기계가 결정적으로 답할 수 있는 것만. 2026-08-13 작성.

check_all.py 가 「고친 뒤 늘 돌리는 그물」이라면, 이것은 「가끔 전수로 훑는 그물」이다.
대량 편집이 지나간 뒤의 **회귀**를 잡는다.

    python check_audit.py            네 층 전부
    python check_audit.py --layer 슬롯   한 층만 (구조·슬롯·내용·어휘)

★★ 이 도구를 고칠 때 반드시 지킬 것 — 2026-08-13에 잣대를 여섯 번 틀렸다.
  ① 「검사기가 0건」은 「없다」가 아니라 「못 찾았다」일 수 있다. 무엇을 어떻게
     세었는지 함께 찍어라. 실제로 틀렸던 것들:
       · sentence-num 은 속성이 아니라 **클래스** → 500문장이 통째로 빠졌다
       · <header class="title-block sentence"> → class="title-block" 로 찾아 105파일이 「머리 없음」
       · event.stopPropagation 을 「없는 함수」로 세어 102파일이 걸렸다
  ② 「걸렸다」도 곧바로 결함이 아니다. 원문을 보고 갈라라.
       · 「슬롯 밖 영어」에 한국어 원문 속 고유명사(TOPIK·KTX)가 걸린다
       · 「슬롯 안 한국어」에 단추 속 UI(여·남)가 걸린다 — 이건 번역돼야 맞다
  ③ translate 도 lang 도 **물려받는다.** 태그 하나만 보면 안 되고 파서로 훑어라.
     그리고 <html translate="no"> 는 「일부러 잠근 것」이 아니라 **바탕**이다.
"""
import re, sys, io, os, html, json, collections, argparse, unicodedata
from html.parser import HTMLParser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
NOT_BOOK = {"_음성 확인.html"}

HANGUL = re.compile(r"[가-힣]")
LATIN3 = re.compile(r"[A-Za-z]{3,}")
TAG = re.compile(r"<[^>]+>")
GUARD = re.compile(r"(?is)<(style|script)\b[^>]*>.*?</\1\s*>")

FILES = sorted(f for f in os.listdir(BOOK) if f.lower().endswith(".html"))
SRC = {f: open(os.path.join(BOOK, f), encoding="utf-8").read() for f in FILES}
BODY = [f for f in FILES if f.startswith("3 ")]


def txt(h):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", h))).strip()


def screen_text(s):
    return html.unescape(TAG.sub("", GUARD.sub("", s)))


def scripts(s):
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", s, re.S):
        if not re.search(r"\bsrc\s*=", m.group(1)):
            yield m.group(2)


# ── 층 1. 구조 ────────────────────────────────────────────────
def layer_structure(bad):
    MOJI = re.compile(r"[ÃÂâ][\u0080-\u00BF]|ï»¿")
    PAIRED = ("div", "span", "script", "style", "table", "thead", "tbody",
              "tr", "td", "th", "button", "section", "header", "form", "select")
    nums = collections.Counter()
    for f, s in SRC.items():
        if MOJI.search(s):
            bad["인코딩·모지바케"].append((f, MOJI.search(s).group(0)[:20]))
        if "\ufffd" in s:
            bad["인코딩·U+FFFD"].append((f, str(s.count("\ufffd"))))
        if any("\ue000" <= c <= "\uf8ff" for c in s):
            bad["인코딩·사용자영역"].append((f, ""))
        if any(unicodedata.category(c) == "Cc" and c not in "\t\n\r" for c in s):
            bad["인코딩·제어문자"].append((f, ""))
        t = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        for tag in PAIRED:
            o = len(re.findall(rf"<{tag}\b", t, re.I))
            c = len(re.findall(rf"</{tag}\s*>", t, re.I))
            if o != c:
                bad["태그 짝"].append((f, f"{tag} {o} vs {c}"))
        ids = re.findall(r'\bid="([^"]+)"', s)
        dup = [k for k, n in collections.Counter(ids).items() if n > 1]
        if dup:
            bad["id 중복"].append((f, ", ".join(dup[:4])))
        for a in re.findall(r'data-ans="([^"]*)"', s):
            if not a.strip():
                bad["정답 빈 값"].append((f, ""))
            if "undefined" in a or "NaN" in a:
                bad["정답 오염"].append((f, a[:30]))
        # ★ sentence-num 은 클래스다
        for m in re.finditer(r'class="sentence-num"[^>]*>\s*(\d+)\s*<', s):
            nums[int(m.group(1))] += 1
        vis = screen_text(s)
        for w in ("undefined", "NaN", "[object Object]"):
            if w in vis:
                bad["화면 누수"].append((f, w))
        # 없는 id 를 부르는가
        have = set(re.findall(r'\bid="([^"]+)"', s))
        for js in scripts(s):
            have |= set(re.findall(r'id=\\?["\']([^"\'\\]+)', js))
        for js in scripts(s):
            for m in re.finditer(r"getElementById\(\s*(['\"])([^'\"]+)\1\s*\)\s*\.\s*[A-Za-z_]", js):
                if m.group(2) not in have:
                    bad["없는 id 를 부름"].append((f, m.group(2)))
    miss = [n for n in range(1, 501) if n not in nums]
    if miss:
        bad["문장 번호 빠짐"].append(("", str(miss[:20])))
    for n, c in nums.items():
        if c > 1:
            bad["문장 번호 겹침"].append(("", str(n)))
    # 음원
    snd = os.path.join(BOOK, "_소리")
    if os.path.isdir(snd):
        have_f = {os.path.splitext(x)[0] for x in os.listdir(os.path.join(snd, "f"))}
        have_m = {os.path.splitext(x)[0] for x in os.listdir(os.path.join(snd, "m"))}
        for f, s in SRC.items():
            for js in scripts(s):
                for m in re.finditer(r'(["\'])((?:\\.|(?!\1).)*)\1\s*:\s*(["\'])(\d{3,5})\3', js):
                    v = m.group(4)
                    if v not in have_f:
                        bad["여성 음원 없음"].append((f, v))
                    if v not in have_m:
                        bad["남성 음원 없음"].append((f, v))


# ── 층 2. 번역 슬롯 ───────────────────────────────────────────
class Walk(HTMLParser):
    """★translate·lang 은 물려받는다. <html translate=no> 는 바탕이지 잠금이 아니다."""
    SKIP = {"script", "style", "title"}
    VOID = {"br", "hr", "img", "input", "meta", "link", "source", "col", "area", "base"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.tr, self.lang, self.locked, self.skip = [], False, "ko", 0, 0
        self.chunks = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if tag in self.VOID:
            return
        d = dict(attrs)
        self.stack.append((tag, self.tr, self.lang, self.locked))
        v = d.get("translate")
        if v == "no" and tag != "html":
            self.locked += 1
        if v == "yes":
            self.tr = True
        elif v == "no":
            self.tr = False
        if "lang" in d:
            self.lang = d["lang"]

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag in self.VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, self.tr, self.lang, self.locked = self.stack[i]
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        self.chunks.append((data.strip(), self.tr, self.lang, self.locked > 0,
                            self.getpos()[0]))


def layer_slot(bad):
    for f, s in SRC.items():
        w = Walk()
        try:
            w.feed(s)
        except Exception as e:
            bad["파싱 실패"].append((f, str(e)[:40]))
            continue
        for t, opened, lang, locked, line in w.chunks:
            # ★한글이 하나도 없는 것만 — 한국어 원문 속 고유명사(TOPIK)를 거른다
            if not opened and not locked and LATIN3.search(t) and not HANGUL.search(t):
                bad["슬롯 밖 영어"].append((f, f"{line}행 {t[:44]}"))
            # ★lang=en 슬롯만 — 단추 속 UI 한국어(여·남)는 번역돼야 맞다
            if opened and lang.startswith("en") and HANGUL.search(t):
                bad["en 슬롯 속 안 잠긴 한국어"].append((f, f"{line}행 {t[:44]}"))

        # ── <title> — 위 Walk 는 title 을 건너뛴다(SKIP). 따로 본다.
        #    ★<title> 안에는 자식 태그를 못 넣어 <span translate="no"> 로
        #    부분만 잠글 수 없다. 그래서 한국어가 들면 통째로 잠근다 —
        #    안 그러면 브라우저 번역이 문법 항목인 「에」·「은는」까지 옮긴다.
        #    언어판은 lang_build.py ④단계가 제목을 통째로 갈아 끼운다.
        m = re.search(r"<title([^>]*)>(.*?)</title>", s, re.S)
        if m and HANGUL.search(m.group(2)) and 'translate="no"' not in m.group(1):
            bad["제목 속 한국어가 안 잠김"].append(
                (f, m.group(2).strip()[:44]))


# ── 층 3. 내용 ────────────────────────────────────────────────
def norm(s):
    """채점기 wtNormalize 와 같은 잣대 — 띄어쓰기·부호를 지운다."""
    s = html.unescape(TAG.sub("", s))
    return re.sub(r"[\s.?!,·…“”\"'’‘()\[\]~—-]", "", s)


def layer_content(bad, info):
    tot_sent = tot_wt = 0
    for f in BODY:
        s = SRC[f]
        follow = {}
        # ★판형이 둘이다 — 한 줄짜리와 여러 줄짜리
        for m in re.finditer(r'<div class="sentence-item"[^>]*>(.*?)'
                             r'(?=<div class="sentence-item"|\Z)', s, re.S):
            blk = m.group(1)
            num = re.search(r'<div class="sentence-num">\s*(\d+)\s*</div>', blk)
            if not num:
                continue
            kr = re.search(r'<div class="sentence-kr"[^>]*>(.*?)</div>', blk, re.S)
            if kr:
                ko = TAG.sub("", kr.group(1))
            else:
                sp = re.search(r"speakKorean\((?:&#39;|')([^']+?)(?:&#39;|')", m.group(0))
                if not sp:
                    continue
                ko = sp.group(1)
            follow[int(num.group(1))] = html.unescape(ko).strip()
        tot_sent += len(follow)
        fol = {norm(v) for v in follow.values()}
        # ★번호는 <h3> 바로 뒤가 아니라 슬롯 <span> 안에 있다
        titles = set()
        for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", s, re.S):
            n = re.match(r"(\d+)\)", html.unescape(TAG.sub("", m.group(1))).strip())
            if n:
                titles.add(int(n.group(1)))
        for n in follow:
            if n not in titles:
                bad["영어 제목 없는 번호"].append((f, str(n)))
        for m in re.finditer(r'<textarea[^>]*class="[^"]*writing-input[^"]*"[^>]*'
                             r'data-ans="([^"]*)"', s):
            tot_wt += 1
            a = html.unescape(m.group(1)).strip()
            if norm(a) and norm(a) not in fol:
                bad["쓰기 정답이 문장과 다름"].append((f, a[:40]))
        c = collections.Counter(norm(v) for v in follow.values())
        for k, n in c.items():
            if n > 1:
                bad["한 파일 안 문장 겹침"].append((f, k[:30]))
    info["따라 읽기 문장"] = tot_sent
    info["쓰기 시험 문항"] = tot_wt


# ── 층 4. 어휘 ────────────────────────────────────────────────
def span_of(s, start):
    """★비탐욕 정규식은 겹친 span 에서 안쪽 </span> 을 먹어 뜻풀이를 자른다."""
    d = 0
    for m in re.finditer(r"<span\b[^>]*>|</span\s*>", s[start:]):
        d += -1 if m.group(0).startswith("</") else 1
        if d == 0:
            return start + m.start()
    return -1


def layer_vocab(bad, info):
    items = 0
    for f in BODY:
        s = SRC[f]
        page = txt(GUARD.sub("", s))
        for vm in re.finditer(r'<span class="v-item"[^>]*>', s):
            close = span_of(s, vm.start())
            if close < 0:
                continue
            blk = s[vm.start():close]
            items += 1
            head = re.search(r"<b[^>]*>(.*?)</b>", blk, re.S)
            h = txt(head.group(1)) if head else ""
            gm = re.search(r'<span class="gloss"([^>]*)>', blk)
            if not h:
                bad["표제어 비었음"].append((f, blk[:40]))
            if not gm:
                bad["뜻풀이 없음"].append((f, h[:24]))
            elif 'translate="yes"' not in gm.group(1):
                bad["뜻풀이에 슬롯 없음"].append((f, h[:24]))
            if h and HANGUL.search(h):
                stem = h.lstrip("~").rstrip("다").strip()
                if len(stem) >= 2 and stem not in page:
                    bad["파일에 안 나오는 표제어"].append((f, h[:24]))
    info["어휘 항목"] = items
    info["어휘 상자"] = sum(s.count('class="v-item"') for s in SRC.values())


LAYERS = {"구조": layer_structure, "슬롯": layer_slot,
          "내용": layer_content, "어휘": layer_vocab}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", choices=list(LAYERS))
    a = ap.parse_args()
    bad = collections.defaultdict(list)
    info = {}
    for name, fx in LAYERS.items():
        if a.layer and name != a.layer:
            continue
        try:
            fx(bad, info) if fx.__code__.co_argcount == 2 else fx(bad)
        except TypeError:
            fx(bad)
    print(f"■ 대상 {len(FILES)}파일 (본문 {len(BODY)})")
    for k, v in info.items():
        print(f"   {k} {v:,}")
    print("\n■ 결과")
    keys = ["인코딩·모지바케", "인코딩·U+FFFD", "인코딩·사용자영역", "인코딩·제어문자",
            "태그 짝", "id 중복", "정답 빈 값", "정답 오염", "화면 누수",
            "없는 id 를 부름", "문장 번호 빠짐", "문장 번호 겹침",
            "여성 음원 없음", "남성 음원 없음",
            "파싱 실패", "슬롯 밖 영어", "en 슬롯 속 안 잠긴 한국어",
            "제목 속 한국어가 안 잠김",
            "영어 제목 없는 번호", "쓰기 정답이 문장과 다름", "한 파일 안 문장 겹침",
            "표제어 비었음", "뜻풀이 없음", "뜻풀이에 슬롯 없음", "파일에 안 나오는 표제어"]
    n_bad = 0
    for k in keys:
        v = bad.get(k)
        if v is None and a.layer:
            continue
        v = v or []
        n_bad += len(v)
        print(f"   {'○' if not v else '★'} {k:22} {len(v):5}건")
    for k in keys:
        v = bad.get(k) or []
        if not v:
            continue
        print(f"\n── {k} ({len(v)}) ──")
        for f, m in v[:20]:
            print(f"   {f[:36]:38} {m}")
        if len(v) > 20:
            print(f"   … {len(v) - 20}건 더")
    print(f"\n■ 모두 {n_bad}건. 0건이어야 정상입니다.")
    print("   ※ 「슬롯 밖 영어」는 고유명사(BTS·KTX·Amazing Korean 1)와 진단 페이지가")
    print("      남습니다 — 2026-08-13 기준 4건이 정상입니다.")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""다국어 2층 — 스크립트 안에 박힌 문자열을 전수로 뽑아 사전 뼈대를 낸다.

lang_build.py 의 ③단계는 tr.JS 사전을 따옴표째 그대로 치환한다. 그 사전을
손으로 적는 것은 불가능하다 — 106파일 419덩이에 리터럴이 12,000자리가 넘는다.
이 도구가 그 사전의 열쇠를 뽑는다.

★★ 가장 중요한 것 — 「한국어인가 영어인가」로는 절대 못 가른다.
   삽니까? 와 「다시 고르세요.」는 둘 다 한국어지만 하나는 배우는 대상이고
   하나는 화면 안내다. All matched! 와 buy 는 둘 다 영어지만 둘 다 번역 대상이다.
   갈리는 곳은 **어디에 놓였는가(자리)** 뿐이다.

   번역할 자리   innerHTML/textContent 에 대입되거나 + 로 이어 붙는 문구
                자료 칸의 영어 뜻풀이 (["사다","buy",…] 의 buy)
                emPairs 의 en: 쪽
   잠글 자리     AK_SND/AK_SEQ 의 열쇠 — ★바꾸면 음원을 못 찾아 소리가 죽는다
                emPairs 의 ko: 쪽 · data-ans · 자료 칸의 한국어 (활용표)

★ 겹침은 0가지임을 확인했다(2026-08-12) — 한 글자가 번역 자리와 잠글 자리에
  함께 나오는 곳은 없다. 그래서 「글자 → 번역어」 사전 하나로 풀린다.
  ※ 자료 구조를 고치면 이 전제가 깨질 수 있다. --check 로 다시 세어 보라.

쓰기
    python js_extract.py                 → 셈만 하고 보여 준다
    python js_extract.py --dump 뼈대.py   → 사전 뼈대를 낸다 (번역어는 빈칸)
    python js_extract.py --check          → 겹침이 생겼는지만 본다
"""
import re, sys, io, os, html, json, collections, argparse

# ★ 남이 import 할 때는 stdout 을 건드리지 않는다 —
#   감싼 것이 치워지면서 밑바탕 버퍼를 닫아 「I/O operation on closed file」 이 난다
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

HANGUL = re.compile(r"[가-힣]")
LATIN_WORD = re.compile(r"[A-Za-z]{2,}")


# ── 스크립트 꺼내기 ────────────────────────────────────────────
def scripts(s):
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", s, re.S):
        if re.search(r"\bsrc\s*=", m.group(1)):
            continue
        yield m.group(2)


# 뒤에 정규식이 올 수 있는 낱말 — `return /re/` 는 나눗셈이 아니다
RX_KEYWORDS = {"return", "typeof", "instanceof", "in", "of", "new", "delete",
               "void", "case", "do", "else", "yield", "await", "throw"}


def _rx_ok(prev, prev_word):
    """이 자리의 `/` 가 정규식 시작인가 나눗셈인가 — 직전 토큰으로 가른다."""
    if prev == "":
        return True
    if prev == "w":                 # 식별자·숫자 뒤 → 나눗셈 (키워드면 정규식)
        return prev_word in RX_KEYWORDS
    if prev == "x":                 # 문자열·정규식 뒤 → 나눗셈
        return False
    return prev not in ")]"         # ( , = : [ ! ? & | + - 등 뒤 → 정규식


def strip_comments(js):
    """주석과 ★정규식 리터럴★ 을 같은 길이의 빈칸으로 덮는다.
    자리(오프셋)를 지켜야 하므로 지우지 않고 덮는다.

    ★★ 정규식을 건너뛰지 않으면 렉서가 어긋난다 — 이 책에는 따옴표를 품은
      정규식이 165곳 있다. `/[?？!.,'"“”]/g`(쓰기 시험 채점기 wtNormalize)와
      `/speakKorean\\('([^']*)'/`(음원 그물)이 그것이다. 그 따옴표를 문자열
      시작으로 읽으면 뒤따르는 리터럴이 통째로 헛것이 된다.
      2026-08-12에 실제로 이것 때문에 첫 셈이 틀렸다."""
    out = list(js)
    i, n = 0, len(js)
    prev, prev_word = "", ""

    def blank(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = js[i]
        if c in "'\"`":                       # 문자열은 그대로 둔다
            j = i + 1
            while j < n:
                d = js[j]
                if d == "\\":
                    j += 2
                    continue
                if d == c:
                    j += 1
                    break
                if d == "\n" and c != "`":
                    break
                j += 1
            i, prev, prev_word = j, "x", ""
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            j = js.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(i, j)
            i = j
            continue
        if c == "/" and _rx_ok(prev, prev_word):
            j, cls, ok = i + 1, False, False
            while j < n:
                d = js[j]
                if d == "\\":
                    j += 2
                    continue
                if d == "[":
                    cls = True
                elif d == "]":
                    cls = False
                elif d == "/" and not cls:
                    ok = True
                    break
                elif d == "\n":
                    break
                j += 1
            if ok:
                j += 1
                while j < n and js[j].isalpha():   # g·i·m 같은 플래그
                    j += 1
                blank(i, j)
                i, prev, prev_word = j, "x", ""
                continue
        if c.isalnum() or c in "_$":
            j = i
            while j < n and (js[j].isalnum() or js[j] in "_$"):
                j += 1
            prev, prev_word = "w", js[i:j]
            i = j
            continue
        if not c.isspace():
            prev, prev_word = c, ""
        i += 1
    return "".join(out)


def literals(js):
    """(따옴표, 본문, 시작자리). 이스케이프와 템플릿 리터럴을 다룬다."""
    i, n = 0, len(js)
    while i < n:
        c = js[i]
        if c in "'\"`":
            j, buf = i + 1, []
            closed = False
            while j < n:
                d = js[j]
                if d == "\\":
                    buf.append(js[j:j + 2])
                    j += 2
                    continue
                if d == c:
                    closed = True
                    break
                if d == "\n" and c != "`":
                    break            # 안 닫혔다 — 리터럴이 아니었다
                buf.append(d)
                j += 1
            if closed:
                yield c, "".join(buf), i
                i = j + 1
                continue
        i += 1


# ── 글자다운 것만 남기기 ───────────────────────────────────────
SKIP_EXACT = {
    "", " ", "  ", "\\n", "|", ",", ".", "/", "-", "—", "·", ":", ";",
    "px", "block", "none", "inline", "inline-block", "flex", "grid",
    "click", "change", "input", "keyup", "keydown", "load", "ended",
    "end", "error", "submit", "focus", "blur", "beforeunload", "DOMContentLoaded",
    "div", "span", "p", "td", "th", "tr", "button", "audio", "ko-KR",
    "true", "false", "null", "undefined", "text", "html", "hidden",
    "GET", "POST", "add", "remove", "toggle", "contains",
}
SKIP_RX = [
    re.compile(r"^[.#\[]"),                                  # 선택자
    re.compile(r"^[\w-]+$"),                                 # 홑낱말 (클래스·id·열쇠)
    re.compile(r"^#[0-9a-fA-F]{3,8}$"),                      # 색
    re.compile(r"^[\d.]+(px|rem|em|%|s|ms|vh|vw)$"),
    re.compile(r"^[\w./-]+\.(mp3|wav|ogg|png|jpg|svg|json|html|css|js)$", re.I),
    re.compile(r"^https?://"),
    re.compile(r"^data-[\w-]+$"),
    re.compile(r"^[가-힣]$"),                                 # 낱글자 (받침 판별용)
    re.compile(r"^[ㄱ-ㅎㅏ-ㅣ]+$"),                            # 자모만
    re.compile(r"^[\s\d.,%|/·:;()\[\]{}+\-*=<>!?~&$#@^]+$"),  # 부호·숫자만
]


def skip(t):
    k = t.strip()
    if k in SKIP_EXACT:
        return True
    if any(rx.match(k) for rx in SKIP_RX):
        return True
    if ":" in k and ";" in k and not HANGUL.search(k) and "<" not in k:
        return True                                          # CSS 선언 덩이
    return not HANGUL.search(k) and not LATIN_WORD.search(k)


def visible(t):
    """태그·엔티티·이스케이프를 걷어낸 화면 글자.
    ★엔티티를 먼저 풀지 않으면 &nbsp; 의 nbsp 가 영어 낱말로 잡힌다."""
    x = re.sub(r"<[^>]*>", "", t)
    x = html.unescape(x)
    x = re.sub(r"\\u\{?[0-9a-fA-F]+\}?", "", x)
    x = re.sub(r"\\[nrt']", " ", x)
    return x.strip()


# ── 자리 판별 ─────────────────────────────────────────────────
def obj_spans(js, name):
    """`NAME = {` 부터 짝이 맞는 `}` 까지. 문자열 안의 중괄호는 세지 않는다."""
    spans = []
    for m in re.finditer(r"\b" + name + r"\s*=\s*\{", js):
        i, d, q = m.end() - 1, 0, None
        while i < len(js):
            c = js[i]
            if q:
                if c == "\\":
                    i += 2
                    continue
                if c == q:
                    q = None
            elif c in "'\"`":
                q = c
            elif c == "{":
                d += 1
            elif c == "}":
                d -= 1
                if d == 0:
                    spans.append((m.start(), i))
                    break
            i += 1
    return spans


SINK = re.compile(
    r"(innerHTML|outerHTML|textContent|innerText|insertAdjacentHTML|alert)"
    r"\s*(=|\+=|,|\()[^;]{0,400}$", re.S)

# ★ 사람이 아니라 **기계가 읽는** 인수 — 번역하면 기능이 죽는다.
#   querySelector('table.num-table') 을 번역하면 숫자 표를 못 찾는다.
#   이 검사는 SINK 보다 **먼저** 와야 한다 — insertAdjacentHTML 의 첫 인수
#   ('beforeend')는 자리 이름이라 번역 대상이 아닌데 SINK 에 걸리기 때문이다.
#   첫 인수만 잡는다(`( ` 바로 뒤). 둘째 인수의 HTML 은 그대로 번역 대상이다.
MACHINE = re.compile(
    r"(?:querySelector|querySelectorAll|getElementById|getElementsByClassName|"
    r"getElementsByTagName|getElementsByName|closest|matches|createElement|"
    r"createElementNS|setAttribute|getAttribute|hasAttribute|removeAttribute|"
    r"addEventListener|removeEventListener|dispatchEvent|"
    r"getItem|setItem|removeItem|setProperty|getPropertyValue|"
    r"insertAdjacentHTML|insertAdjacentElement|"
    r"classList\.(?:add|remove|toggle|contains|replace))\s*\(\s*$")


def role(js, off, lit, snd):
    if any(a <= off <= b for a, b in snd):
        return "잠글:음원열쇠"
    before = js[max(0, off - 120):off]
    if MACHINE.search(before):
        return "잠글:기계가 읽음"
    if re.search(r"\bko\s*:\s*$", before[-14:]):
        return "잠글:ko"
    if re.search(r"\ben\s*:\s*$", before[-14:]):
        return "번역:en"
    if re.search(r"data-ans=\\?['\"]?$", before[-24:]):
        return "잠글:정답"
    if SINK.search(before):
        return "번역:문구"
    # ★ 자료 칸 판별이 먼저다 — 활용표 안에 태그가 든 칸이 있어도 자료로 남긴다
    if re.search(r"[\[{,]\s*$", before[-6:]):
        return "잠글:자료한국어" if HANGUL.search(lit) else "번역:자료영어"
    # ★ `{"가다":"to go"}` 꼴 객체 값 — 부록 3 의 뜻풀이 21개가 여기 있다.
    #   단 삼항의 else 가지(`has?'받침 O':'받침 X'`)도 `:` 뒤라 생김새가 같다.
    #   갈라 주지 않으면 「받침 X」가 자료로 잠겨 번역에서 빠진다.
    if before.rstrip().endswith(":"):
        head = before.rstrip()[:-1]
        q = head.rfind("?")
        ternary = q >= 0 and not re.search(r"[,;{]", head[q:])
        if ternary:
            return "번역:문구"
        return "잠글:자료한국어" if HANGUL.search(lit) else "번역:자료영어"
    # ★ 삼항의 **앞** 가지 — `has?'받침 O':'받침 X'` 의 왼쪽. `:` 만 보면 짝이 갈린다
    #   (2026-08-12에 「받침 X」만 잡히고 「받침 O」는 모름에 남았다)
    if before.rstrip().endswith("?"):
        return "번역:문구"
    if re.search(r"[+=(]\s*$", before[-4:]) or re.search(r"\breturn\s*$", before):
        return "번역:문구"
    # ★ 태그를 품고 화면 글자가 있는 리터럴은 DOM 으로 갈 수밖에 없다.
    #   긴 이어붙이기 사슬 가운데 토막이라 앞 400자 안에 innerHTML 이 안 보이는 것들
    #   (안 썼습니다 67파일 · ↻ 클릭 28파일)이 여기서 걸린다.
    if re.search(r"<[a-zA-Z/][^>]*>", lit) and visible(lit):
        return "번역:문구"
    return "모름"


# 언어판을 찍지 않는 페이지 — 책이 아니다 (검사기 예외표와 같은 자리)
NOT_BOOK = {"_음성 확인.html"}


def survey():
    """글자 → [(파일, 노릇)] 전수."""
    occ = collections.defaultdict(list)
    for fn in sorted(f for f in os.listdir(BOOK)
                     if f.lower().endswith(".html") and f not in NOT_BOOK):
        s = open(os.path.join(BOOK, fn), encoding="utf-8").read()
        for js in scripts(s):
            clean = strip_comments(js)
            snd = obj_spans(clean, "AK_SND") + obj_spans(clean, "AK_SEQ")
            for q, body, off in literals(clean):
                if not skip(body):
                    occ[body].append((fn, role(clean, off, body, snd)))
    return occ


# ── 사전에 넣지 않을 것 ────────────────────────────────────────
PATHY = re.compile(r"^[\w가-힣 _.-]+/$|^[\w가-힣 _./-]+\.(mp3|wav|json)$", re.I)
ATTR_FRAG = re.compile(r'^\s*("|\')?\s*(readonly|type=|value=|data-|style=|oninput=|onclick=|class=|id=)')
# ★ CSS 함수 조각 — 'rotate(' + d + 'deg)' 처럼 갈라져 있어 글자처럼 보인다
CSS_FRAG = re.compile(r"^(rotate|translate|scale|skew|matrix|rgba?|hsla?|calc|url|var)\($"
                      r"|^(deg|rad|turn|px|em|rem|fr|vh|vw)\)$")
# ★ 안 닫힌 태그 조각 — '<button class="fc-tts" onclick="speakKorean(' 처럼
#   이어붙이기로 갈라져 태그가 반만 든 것. 화면 글자처럼 보이지만 마크업이다
TAG_FRAG = re.compile(r"<[^>]*$")
ATTR_FRAG2 = re.compile(r'^[\s\w-]*=["\']')


def is_frag(k):
    """사전에 넣을 것이 아닌 조각인가."""
    vis = visible(k)
    if PATHY.match(k.strip()):
        return "음원 경로"
    if CSS_FRAG.match(k.strip()):
        return "CSS 조각"
    if ATTR_FRAG.match(k) or ATTR_FRAG2.match(k):
        return "속성 조각"
    if TAG_FRAG.search(k):
        return "태그 조각"
    if not vis or (not HANGUL.search(vis) and not LATIN_WORD.search(vis)):
        return "마크업 조각"
    return None

TR = lambda r: r.startswith("번역")
LK = lambda r: r.startswith("잠글")


def buckets(occ):
    trans, lock, unknown, dropped = {}, {}, {}, collections.defaultdict(list)
    for k, v in occ.items():
        rs = [r for _, r in v]
        if any(TR(r) for r in rs) and any(LK(r) for r in rs):
            dropped["겹침"].append(k)
            continue
        if any(LK(r) for r in rs):
            lock[k] = v
            continue
        # ★ 조각 걸러내기가 「모름」보다 먼저다 — 안 그러면 안 닫힌 태그 토막이
        #   「사람이 봐야 할 것」에 쌓여 진짜 판단거리를 덮는다
        frag = is_frag(k)
        if frag:
            dropped[frag].append(k)
        elif all(r == "모름" for r in rs):
            unknown[k] = v
        else:
            trans[k] = v
    return trans, lock, unknown, dropped


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ★ 번역할 문구 **안에** 배우는 한국어가 든 것 — 그 조각은 옮기면 안 된다.
#   ① 자모(ㄱ~ㅎ·ㅏ~ㅣ)는 보통 글에 안 나오므로 아주 센 표시다 — ㅂ니다 · ㄹ 것입니다 · ㄷ 불규칙
#   ② 화살표 뒤가 **조사만으로 끝나는** 것 — 「받침 O → 은 · 이」
#   ★ 「→ 짝이 되는 영어 문장을 고르세요.」처럼 화살표 뒤가 **문장**인 것은 통째로
#     번역 대상이다. 화살표만 보고 표를 붙이면 이런 것 70여 줄이 헛걸린다.
JOSA = r"(?:은|는|이|가|을|를|와|과|이나|나|에게|에서|에|도|만|의|로|으로)"
MIXED = re.compile(r"[ㄱ-ㅎㅏ-ㅣ]"
                   r"|[→⇒]\s*(?:<[^>]*>\s*)?" + JOSA +
                   r"(?:\s*[·,]\s*" + JOSA + r")*\s*(?:<[^>]*>\s*)*$")


def dump(trans, path):
    """번역어가 빈 사전 뼈대. 사람이 채워 tr_xx.py 의 JS 에 붙인다."""
    common = {k: v for k, v in trans.items() if len({f for f, _ in v}) >= 10}
    local = {k: v for k, v in trans.items() if len({f for f, _ in v}) < 10}
    w = open(path, "w", encoding="utf-8")
    w.write("# -*- coding: utf-8 -*-\n")
    w.write('"""js_extract.py 가 뽑은 사전 뼈대 — 오른쪽을 채워 tr_xx.py 의 JS 에 붙인다.\n\n')
    w.write("★ 열쇠는 소스에 적힌 그대로여야 한다. 태그·빈칸 하나만 달라도 빌더가 못 찾는다.\n")
    w.write("★ 문구 안의 한국어 문법 표지(ㄹ · ‑습니다 · 은/는)는 번역하지 말고 그대로 두라 —\n")
    w.write("  본문에서 lang=\"ko\" translate=\"no\" 로 잠그는 것과 같은 자리다.\n\"\"\"\n\n")
    nmix = sum(1 for k in trans if MIXED.search(k))
    w.write(f"# ★ 아래 {nmix}줄에는 「그대로 두라」 표가 붙어 있습니다 — 문구 안에 배우는\n")
    w.write("#   한국어(ㅂ니다 · ㄹ 것입니다 · 은 · 이)가 들어 있는 자리입니다.\n\n")
    w.write("JS = {\n")
    w.write(f"    # ── 공통 틀 {len(common)}가지 (10파일 이상) — 여기부터 채우면 값이 크다\n")
    for k, v in sorted(common.items(), key=lambda x: -len({f for f, _ in x[1]})):
        w.write(f'    # {len({f for f, _ in v})}파일 · {visible(k)[:60]}\n')
        if MIXED.search(k):
            w.write("    # ★ 한국어 표지는 그대로 두라\n")
        w.write(f'    "{esc(k)}": "",\n')
    w.write(f"\n    # ── 파일 고유 {len(local)}가지 — 대부분 그 파일의 영어 문장·뜻풀이\n")
    for k, v in sorted(local.items(), key=lambda x: sorted({f for f, _ in x[1]})[0]):
        mark = "  ★한국어 표지 그대로" if MIXED.search(k) else ""
        w.write(f'    "{esc(k)}": "",   # {sorted({f for f, _ in v})[0][:30]}{mark}\n')
    w.write("}\n")
    w.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", metavar="파일")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    occ = survey()
    trans, lock, unknown, dropped = buckets(occ)
    nspots = sum(len(v) for v in occ.values())

    print(f"■ 스크립트 안 문자열 — 자리 {nspots:,} · 서로 다른 글자 {len(occ):,}")
    print(f"   번역할 것    {len(trans):5,}가지")
    print(f"   잠글 것      {len(lock):5,}가지   ← 배우는 한국어 · 음원 열쇠")
    print(f"   ★모름        {len(unknown):5,}가지   ← 사람이 봐야 함")
    for k, v in dropped.items():
        print(f"   버림({k})   {len(v):5,}가지")

    if dropped["겹침"]:
        print(f"\n★★ 겹침 {len(dropped['겹침'])}가지 — 사전 하나로는 못 푼다. 자료 구조가 바뀐 것이다.")
        for k in dropped["겹침"][:20]:
            print(f"      {k[:80]}")
    else:
        print("\n■ 겹침 0가지 — 번역 자리와 잠글 자리에 함께 나오는 글자는 없다. 사전 방식이 선다.")
    if a.check:
        return 1 if dropped["겹침"] else 0

    sub = collections.Counter()
    for k, v in trans.items():
        sub[" · ".join(sorted({r for _, r in v}))] += 1
    print("\n■ 번역할 것의 갈래")
    for k, n in sub.most_common():
        print(f"   {k:24} {n:5,}")

    common = [k for k, v in trans.items() if len({f for f, _ in v}) >= 10]
    print(f"\n■ 공통 틀 {len(common)}가지 · 파일 고유 {len(trans) - len(common)}가지")
    for k in sorted(common, key=lambda x: -len({f for f, _ in trans[x]})):
        print(f"   {len({f for f, _ in trans[k]}):3}파일  {visible(k)[:70]}")

    if unknown:
        print(f"\n■ ★모름 {len(unknown)}가지 — 보기 15")
        for k in sorted(unknown, key=lambda x: -len(unknown[x]))[:15]:
            print(f"   {len(unknown[k]):3}회  {visible(k)[:66]}")

    if a.dump:
        dump(trans, a.dump)
        print(f"\n→ 사전 뼈대 {a.dump}  ({len(trans)}줄)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

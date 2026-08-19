# -*- coding: utf-8 -*-
r"""문항 구간을 정해 「지금까지 정한 규칙」에 걸리는 자리를 전수로 셉니다. 2026-08-20 작성.

    python sweep_survey.py                 # 100~500
    python sweep_survey.py --from 1 --to 99
    python sweep_survey.py --rule R5       # 한 갈래만 자세히

보는 규칙 (모두 2026-08-19 사용자 결정 · 인수인계 §5 「어휘 상자에 무엇을 넣는가」)
    R1 어휘에 조사 표제어            ~에서 · 나/이나 · 와/과 …
    R2 어휘에 문법 표현·어미          ~아/어서 · ~고 싶다 · ~ㄴ 적이 있다 …
    R3 표제어가 활용형               했다 · 좋아졌다 · 갔습니다 → 기본형으로
    R4 뜻풀이에 문법 꼬리표           (subject) · the past of · needs no particle …
    R5 어휘가 정답을 미리 보여 줌      다닌 학교 · 아드님 (그 쪽이 가르치는 꼴이 어휘에 완성돼 있음)
    R6 어휘 차례가 정답 차례와 다름
    R7 한 표제어가 다른 표제어 안에 들어 있음
    R8 어휘 상자가 비었음

★ 「걸렸다 ≠ 결함이다」 — 이 스크립트는 **후보만** 냅니다. 반드시 열어 보고 가르십시오.
  R7 은 뺄지 말지가 정답을 봐야 갈리고(인수인계 §5 의 조건 둘), R5 는 명사가 정답에
  그대로 드는 것이 정상이라 활용형·관형형·높임말만 봅니다.
"""
import io, os, re, sys, glob, html as H
import argparse
from collections import OrderedDict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

KO = re.compile(r"[가-힣]")


def vis(x):
    """태그를 빈 문자열로 지우고 화면 글자만 남깁니다(공백으로 바꾸면 오탐이 쏟아집니다)."""
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


# ── 문항 뽑기 ────────────────────────────────────────────────────────────
H3 = re.compile(r"<h3[^>]*>([\s\S]*?)</h3>")
NUM = re.compile(r"^\s*(\d{1,3})\)")
VBOX = re.compile(r'<div class="vocab-box">([\s\S]*?)</div>\s*</div>')
VITEM = re.compile(r'<span class="v-item[^"]*">([\s\S]*?)</span>\s*</span>')
ANS = re.compile(r'data-ans="([^"]*)"')


def items(path):
    """(번호, 표제어·뜻풀이 목록, 정답, 어휘상자 원본) 을 문항 차례로 냅니다."""
    s = io.open(path, encoding="utf-8").read()
    heads = [(m.start(), m.end(), vis(m.group(1))) for m in H3.finditer(s)]
    out = []
    for i, (a, b, txt) in enumerate(heads):
        m = NUM.match(txt)
        if not m:
            continue
        end = heads[i + 1][0] if i + 1 < len(heads) else len(s)
        chunk = s[b:end]
        vb = VBOX.search(chunk)
        pairs = []
        raw = ""
        if vb:
            raw = vb.group(0)
            for it in VITEM.finditer(vb.group(1)):
                inner = it.group(1)
                bm = re.search(r"<b>([\s\S]*?)</b>", inner)
                gm = re.search(r'<span class="gloss"[^>]*>([\s\S]*?)</span>', inner)
                head = vis(bm.group(1)) if bm else ""
                gloss = vis(gm.group(1)) if gm else ""
                if head or gloss:
                    pairs.append((head, gloss))
        am = ANS.search(chunk)
        out.append({
            "num": int(m.group(1)), "en": txt, "v": pairs,
            "ans": H.unescape(am.group(1)) if am else "", "raw": raw,
            "file": os.path.basename(path),
        })
    return out


# ── 규칙 ────────────────────────────────────────────────────────────────
JOSA = ["에서", "에게", "까지", "부터", "으로", "처럼", "보다", "마다", "밖에",
        "이나", "나/이나", "와/과", "과/와", "은/는", "이/가", "을/를", "에"]
GRAM_TAIL = ["아/어서", "으면서", "면서", "자마자", "다가", "고 싶", "것 같", "ㄹ 때",
             "적이 있", "는데", "거나", "지만", "으면", "니까", "려고", "기로",
             "아/어 주", "ㄹ 수 있", "ㄹ 줄", "지 못하", "게 되", "아/어지"]
CONJ_TAIL = re.compile(r"(았다|었다|였다|했다|았습니다|었습니다|했습니다|"
                       r"ㅂ니다|습니다|았어요|었어요)$")
MODIFIER = re.compile(r"[가-힣]+(?:은|ㄴ|는|을|ㄹ)\s+[가-힣]+$")
GRAM_LABEL = re.compile(
    r"\((?:subject|object|direction|location|time|polite|honorific|plain|casual|"
    r"formal|informal|noun|verb|adjective|adverb|particle|counter|question|"
    r"needs no particle|no particle)[^)]*\)|"
    r"\bthe (?:past|present|future|modifier|honorific|plain) (?:of|form)\b|"
    r"\bcomparison particle\b|\bIO marker\b", re.I)


def head_is_base(h):
    """기본형(‑다)이거나 명사 꼴인가 — 활용형 판별용."""
    return h.endswith("다") and not CONJ_TAIL.search(h)


def run(lo, hi, only=None):
    hits = OrderedDict((k, []) for k in
                       ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"])
    seen = set()
    for f in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        for it in items(f):
            n = it["num"]
            if not (lo <= n <= hi) or n in seen:
                continue
            seen.add(n)
            v, ans = it["v"], it["ans"]
            if not it["raw"]:
                continue
            if not v:
                hits["R8"].append((n, it["file"], "어휘 상자가 비었음"))
            for head, gloss in v:
                if not head:
                    continue
                base = head.lstrip("~").strip()
                # R1 조사
                if base in JOSA or (head.startswith("~") and base in JOSA):
                    hits["R1"].append((n, it["file"], f"{head} = {gloss}"))
                # R2 문법 표현
                elif any(t in head for t in GRAM_TAIL) and head.startswith(("~", "(")):
                    hits["R2"].append((n, it["file"], f"{head} = {gloss}"))
                elif head.startswith("~"):
                    hits["R2"].append((n, it["file"], f"{head} = {gloss}"))
                # R3 활용형
                if CONJ_TAIL.search(head):
                    hits["R3"].append((n, it["file"], f"{head} = {gloss}"))
                # R4 문법 꼬리표
                if GRAM_LABEL.search(gloss):
                    hits["R4"].append((n, it["file"], f"{head} = {gloss}"))
                # R5 정답을 미리 보여 줌 — 활용형·관형형·높임말이 정답에 그대로
                if ans and head and head in ans and not head_is_base(head):
                    if MODIFIER.match(head) or CONJ_TAIL.search(head) or \
                       head.endswith(("님", "님의", "께서", "께")):
                        hits["R5"].append((n, it["file"], f"{head}  ← 정답: {ans}"))
            # R6 차례
            if ans and len(v) > 1:
                pos, ok = [], True
                for head, _ in v:
                    key = head.lstrip("~").split("/")[0].rstrip("다") or head
                    p = ans.find(key[:2]) if len(key) >= 2 else -1
                    if p < 0:
                        ok = False
                        break
                    pos.append(p)
                if ok and pos != sorted(pos):
                    order = " · ".join(h for h, _ in v)
                    hits["R6"].append((n, it["file"], f"{order}   ← 정답: {ans}"))
            # R7 겹친 표제어
            heads = [h for h, _ in v if h]
            for a in heads:
                for b in heads:
                    if a != b and a in b:
                        hits["R7"].append((n, it["file"], f"{a} ⊂ {b}"))
    return hits, len(seen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="lo", type=int, default=100)
    ap.add_argument("--to", dest="hi", type=int, default=500)
    ap.add_argument("--rule", default=None)
    ap.add_argument("--all", action="store_true", help="줄여 쓰지 말고 다 보이기")
    A = ap.parse_args()

    hits, cnt = run(A.lo, A.hi)
    names = {"R1": "어휘에 조사 표제어", "R2": "어휘에 문법 표현·어미",
             "R3": "표제어가 활용형", "R4": "뜻풀이에 문법 꼬리표",
             "R5": "어휘가 정답을 미리 보여 줌", "R6": "어휘 차례가 정답 차례와 다름",
             "R7": "한 표제어가 다른 표제어 안에", "R8": "어휘 상자가 비었음"}
    print(f"■ {A.lo}~{A.hi} — 문항 {cnt}개를 보았습니다\n")
    for k, v in hits.items():
        if A.rule and k != A.rule:
            continue
        print(f"── {k} {names[k]} — {len(v)}곳")
        show = v if (A.all or A.rule) else v[:12]
        for n, f, msg in show:
            print(f"   {n:>3})  {msg}")
        if len(v) > len(show):
            print(f"   … 그리고 {len(v) - len(show)}곳 더 (--rule {k} 로 다 보기)")
        print()
    print("★ 걸린 것이 다 결함은 아닙니다 — 열어 보고 가르십시오(인수인계 §3 「그물을 칠 때」).")


if __name__ == "__main__":
    main()

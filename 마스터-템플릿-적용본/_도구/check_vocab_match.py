# -*- coding: utf-8 -*-
"""번호 문장과 그 어휘의 **영어가 어긋나는가**. 2026-08-18 작성.

    python check_vocab_match.py

규칙(사용자 지시, 2026-08-18)
    「원래 문장(번호가 있는 문장)을 기준으로 어휘를 맞춘다」

★ 한국어는 보지 않습니다 — 어휘는 **기본형**(행복하다), 정답은 **활용형**
  (행복합니다)이라 글자로는 늘 다릅니다. 그것이 규칙대로입니다.
  한국어로 세면 438곳이 나오는데 전부 헛것입니다.

★ 어형은 되돌려 봅니다 — slept↔sleep · went↔go · higher↔high.
  이것을 안 하면 173곳이 나오고 대부분 헛것입니다(활용형 차이일 뿐).

★ 문법 항목은 뺍니다 — `~`로 시작하거나 뜻에 counter·honorific·marker·form 이
  든 것. 문장에 대응 낱말이 있을 수 없습니다.

여기 걸린다고 다 결함은 아닙니다. **문장에 대응 낱말이 있는데 다른 말을 쓴
곳만** 고칩니다(2026-08-18에 84곳 가운데 14곳). 나머지는 문장에 대응 낱말이
없어 사전 뜻을 적은 것이라 갈아 끼우면 오히려 나빠집니다
(「Hi, how are you?」 ↔ 안녕하다 = to be at peace).
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

IRR = dict(x.split() for x in """slept sleep|ran run|went go|bought buy|met meet|made make|
sang sing|spoke speak|thought think|saw see|ate eat|drank drink|gave give|took take|came come|
wrote write|sat sit|taught teach|told tell|said say|heard hear|found find|felt feel|left leave|
sent send|built build|began begin|became become|brought bring|caught catch|chose choose|did do|
drove drive|fell fall|flew fly|forgot forget|got get|grew grow|held hold|kept keep|knew know|
lost lose|paid pay|rode ride|sold sell|spent spend|swam swim|threw throw|understood understand|
wore wear|won win|was be|were be|is be|am be|are be|been be|had have|has have|people person|
men man|women woman|withdrew withdraw|woke wake|broke break""".replace("\n", "").split("|")
           if len(x.split()) == 2)
SUF = (("ies", "y"), ("ied", "y"), ("iest", "y"), ("ier", "y"), ("ing", ""),
       ("ed", ""), ("est", ""), ("er", ""), ("es", ""), ("s", ""))
SKIPG = re.compile(r"counter|honorific|marker|particle|modifier form|\bform\b", re.I)
# ★제목 전체를 읽는다 — 462·464·466·470 은 인용부가 붙어 첫 span 으로 끝나지 않는다.
#   첫 span 만 읽으면 그 넷이 감사에서 통째로 빠진다(2026-08-18에 그랬다).
ITEM = re.compile(r'<h3><span lang="en" translate="yes">(\d+)\)([\s\S]*?)</h3>')
VOCAB = re.compile(r'<span class="v-item"><b>([^<]*)</b>'
                   r'<span class="gloss"[^>]*>([\s\S]*?)</span></span>')


def forms(w):
    out = {w, IRR.get(w, w)}
    for sfx, rep in SUF:
        if w.endswith(sfx) and len(w) - len(sfx) >= 2:
            b = w[:-len(sfx)] + rep
            out |= {b, b + "e"}
    return out


def main():
    tot = nf = 0
    for f in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        s = io.open(f, encoding="utf-8").read()
        hits = []
        for p in re.split(r'(?=<h3><span lang="en" translate="yes">\d+\))', s)[1:]:
            m = ITEM.match(p)
            if not m:
                continue
            num = m.group(1)
            en = H.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
            bag = set()
            for w in re.sub(r"[^a-z' ]", " ", en.lower()).split():
                bag |= forms(w)
            for ko, g in VOCAB.findall(p):
                g = H.unescape(re.sub(r"<[^>]+>", "", g)).strip()
                if ko.strip().startswith("~") or "→" in ko or SKIPG.search(g):
                    continue
                core = re.sub(r"\(.*?\)", "", g).strip()
                core = re.sub(r"^to be |^to ", "", core).strip(" .,~")
                cw = [w for w in re.sub(r"[^a-z' ]", " ", core.lower()).split() if len(w) > 2]
                if not cw or any(forms(w) & bag for w in cw):
                    continue
                hits.append((num, en, ko, g))
        if hits:
            nf += 1
            tot += len(hits)
            print(f"\n=== {os.path.basename(f)}  ({len(hits)})")
            for num, en, ko, g in hits:
                print(f"   {num:>4}) {en[:50]:<52}{ko} = {g[:40]}")
    print(f"\n■ 모두 {tot}곳 / {nf}파일.")
    print("  ※ 0이 목표가 아닙니다 — 문장에 대응 낱말이 **있는데** 다른 말을 쓴 곳만 고치십시오.")


if __name__ == "__main__":
    main()

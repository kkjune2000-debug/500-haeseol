# -*- coding: utf-8 -*-
r"""어휘 뜻풀이에 남은 문법 꼬리표를 뺍니다 (사용자 결정 2026-08-20).

    python vocab_drop_tail.py [--apply]

무엇을
    안 = not (short form)                    → not
    못 = can't (short)                       → can't
    사랑하다 = love (a 하다 verb)              → love
    건강하다 = to be healthy (a 하다 adjective) → to be healthy
    돕다 = help (ㅂ irregular)                → help
    말씀하다 = say (honorific)                 → say

왜
    「어휘는 뜻만 알게 하면 됩니다」 — 2026-08-19 사용자 규칙. 그날 「(needs no particle)」·
    「(the past of …)」·「(the modifier form of …)」를 뺐는데, 괄호 안 말이 달라
    그물에 안 걸린 열 곳이 남아 있었습니다(2026-08-20 어휘 35곳을 고치다 나왔습니다).

★ 표제어는 건드리지 않습니다. 괄호 **하나**만 뗍니다.
★ 괄호 안에 잠긴 한국어(`<span lang="ko" translate="no">하다</span>`)가 있어
  글자로만 맞추면 안 걸립니다 — 태그를 지운 화면 글자로 찾습니다.
★ 뜻풀이가 빈 항목이 생기지 않는지 검산합니다.
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

VI = re.compile(r'(<span class="v-item[^"]*"><b>)([\s\S]*?)(</b>'
                r'<span class="gloss"[^>]*>)([\s\S]*?)(</span></span>)')
TAIL = re.compile(r"\((?:[^()]*\b(?:form|verb|adjective|noun|particle|counter|"
                  r"honorific|plain|polite|informal|short|long|irregular|past|"
                  r"present|future|marker)\b[^()]*)\)\s*$", re.I)


def vis(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


hits, log = {}, []
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s0 = io.open(p, encoding="utf-8", newline="").read()
    name = os.path.basename(p)
    out, last, n = [], 0, 0

    for m in VI.finditer(s0):
        gloss = m.group(4)
        seen = vis(gloss)
        if not TAIL.search(seen):
            continue
        # ★화면 글자에서 꼬리를 떼고, 그 자리에 해당하는 원본을 잘라 냅니다.
        #   괄호 앞까지의 화면 글자 길이를 세어 원본에서 같은 자리를 찾습니다.
        head_txt = TAIL.sub("", seen).strip()
        cut, acc = None, ""
        for i in range(len(gloss) + 1):
            if vis(gloss[:i]) == head_txt:
                cut = i
                break
        if cut is None:
            print(f"  ✗ {name}: 자를 자리를 못 찾음 — {seen}")
            continue
        new_gloss = gloss[:cut].rstrip()
        assert vis(new_gloss) == head_txt, f"{name}: 자른 뒤 글자가 다름"
        assert head_txt, f"{name}: 뜻풀이가 비게 됩니다 — {seen}"
        out.append(s0[last:m.start(4)])
        out.append(new_gloss)
        last = m.end(4)
        n += 1
        log.append((name, vis(m.group(2)), seen, head_txt))
    if not n:
        continue
    out.append(s0[last:])
    s = "".join(out)
    for tg in ("span", "b"):
        a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert a == b, f"{name}: <{tg}> 짝이 어긋남"
    assert s.count("\r\n") == s0.count("\r\n"), f"{name}: 줄끝이 바뀜"
    hits[p] = s

print(f"■ 꼬리표를 뗄 자리 {len(log)}곳 / 파일 {len(hits)}개\n")
for name, head, before, after in log:
    print(f"  [{name[:24]}] {head}")
    print(f"      {before}  →  {after}")

if APPLY:
    for p, s in hits.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("\n■ 반영했습니다")
else:
    print("\n※ 모의 실행입니다. 반영하려면 --apply")

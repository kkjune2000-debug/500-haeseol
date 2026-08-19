# -*- coding: utf-8 -*-
r"""`<small>` 안에 든 `<small>` 을 풉니다 — 영어 줄이 두 겹으로 작아지던 곳.

    python small_unnest.py [--apply]

무엇이 문제였나
    `<small>` 은 글자를 한 단계 줄입니다. 두 겹이면 0.8 × 0.8 = **64%** 가 되어
    같은 자리의 다른 영어 줄보다 눈에 띄게 작습니다. 2026-08-20에 362~365 상자에서
    처음 걸렸고(그쪽은 `<em>` 까지 안 닫혀 있었습니다) 책을 훑으니 일곱 곳이 더
    있었습니다.

어떻게
    안쪽 `<small>` 의 **껍데기만** 벗깁니다. 글자는 하나도 건드리지 않습니다.
    앞에 이미 내용이 있으면 `<br>` 을 넣어 줄을 나눕니다 — 안 그러면 두 영어 줄이
    한 줄로 붙습니다.

★ 화면 글자가 바뀌지 않는 것을 파일마다 검산합니다(`<br>` 은 줄만 나눕니다).
★ 이 책의 파일은 CRLF 입니다. newline="" 로 읽고 씁니다.
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

OPEN = re.compile(r"<small\b[^>]*>", re.I)
CLOSE = re.compile(r"</small\s*>", re.I)


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


def unnest(s):
    """가장 안쪽부터 한 겹씩 벗깁니다. (바뀐 글자, 벗긴 수)"""
    n = 0
    while True:
        # 열린 <small> 안에서 다시 <small> 이 열리는 자리 찾기
        depth, stack, hit = 0, [], None
        for m in re.finditer(r"<small\b[^>]*>|</small\s*>", s, re.I):
            if m.group(0).lower().startswith("</"):
                if stack:
                    stack.pop()
            else:
                if stack:                       # 이미 <small> 안이다
                    hit = (stack[-1], m)
                    break
                stack.append(m)
        if not hit:
            return s, n
        outer_open, inner_open = hit
        # 안쪽의 짝 찾기
        d, close = 1, None
        for m in re.finditer(r"<small\b[^>]*>|</small\s*>", s[inner_open.end():], re.I):
            d += -1 if m.group(0).lower().startswith("</") else 1
            if d == 0:
                close = m
                break
        assert close, "안쪽 <small> 의 짝을 못 찾았습니다"
        a, b = inner_open.start(), inner_open.end()
        c = inner_open.end() + close.start()
        d2 = inner_open.end() + close.end()
        before = s[outer_open.end():a]
        # 앞에 내용이 있고 이미 줄이 나뉘어 있지 않으면 <br> 로 나눕니다
        sep = "" if (not vis(before) or before.rstrip().endswith("<br>")) else "<br>"
        s = s[:a] + sep + s[b:c] + s[d2:]
        n += 1


def main():
    hits = []
    for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        s0 = io.open(p, encoding="utf-8", newline="").read()
        if not re.search(r"<small\b[^>]*>((?:(?!</?small\b)[\s\S])*)<small\b", s0):
            continue
        s, n = unnest(s0)
        name = os.path.basename(p)
        assert vis(s) == vis(s0), f"{name}: 화면 글자가 바뀌었습니다"
        assert s0.count("<small") - s.count("<small") == n, f"{name}: 벗긴 수가 안 맞음"
        assert not re.search(r"<small\b[^>]*>((?:(?!</?small\b)[\s\S])*)<small\b", s), \
            f"{name}: 겹친 <small> 이 남음"
        for tg in ("small", "span", "strong", "em", "div"):
            a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert a == b, f"{name}: <{tg}> 짝이 어긋남"
        hits.append((p, name, s, n))

    print(f"■ 겹친 <small> {sum(h[3] for h in hits)}곳 / {len(hits)}파일")
    for _, name, _, n in hits:
        print(f"     {n}곳  {name}")
    if not APPLY:
        print("\n※ 모의 실행입니다. 반영하려면 --apply")
        return
    for p, _, s, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("\n■ 반영했습니다 — 화면 글자는 그대로입니다")


if __name__ == "__main__":
    main()

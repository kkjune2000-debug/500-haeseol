# -*- coding: utf-8 -*-
r"""어순 해설 표를 걷어낸 뒤 남은 죽은 CSS(`.exp-*`)를 지웁니다 (사용자 결정 2026-08-20).

    python css_dead_exp.py [--apply]

무엇을
    2026-08-19 에 어순 해설 표 500개가 「문장 사다리」로 바뀌면서 `.exp-en` ·
    `.exp-role` · `.exp-form` · `.exp-table` 마크업이 사라졌습니다. 그런데 그 표를
    꾸미던 CSS 규칙은 파일마다 그대로 남아 있습니다. 화면에는 아무 일도 하지
    않지만, 스타일을 고칠 때마다 죽은 규칙을 함께 읽게 됩니다.

★★ **한 파일은 아직 씁니다** — `3 051~060 문장구조 의문사 누구 언제.html` 의
   `<table class="exp-table">`(무슨 + 명사 표). 그 파일의 `.exp-table` 규칙은
   **남깁니다.** 「이름이 같으니 다 죽었겠지」로 지우면 표 하나가 무너집니다.

★ 지우는 잣대 — 그 **파일 안에서** 마크업에 한 번도 안 나오는 `.exp-*` 만 죽은 것으로
  봅니다. 파일마다 따로 셉니다(책은 자족 파일이라 파일이 곧 경계입니다).
★ 선택자가 죽은 것과 산 것을 함께 겨누면 지우지 않습니다(2026-08-20 전수 확인: 0곳).
★ `@media` 같은 묶음(`@`로 시작하는 것)은 건드리지 않습니다.
★ 화면 글자는 바뀌지 않습니다 — CSS 만 지웁니다.
"""
import io, os, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()


def dead_classes(s):
    css = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    body = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s)
    out = set()
    for n in set(re.findall(r"\.(exp-[a-z0-9-]+)", css)):
        if not re.search(rf'class="[^"]*\b{re.escape(n)}\b', body):
            out.add(n)
    return out


def strip(s, dead):
    """죽은 것만 겨누는 규칙을 통째로 지웁니다. (바뀐 글자, 지운 수)"""
    n = 0

    def one(block):
        nonlocal n
        res, last = [], 0
        for m in RULE.finditer(block):
            sel = m.group(1)
            if sel.lstrip().startswith("@"):
                continue
            names = set(re.findall(r"\.([a-zA-Z][\w-]*)", sel))
            if not (names & dead):
                continue
            if names - dead:            # 산 것을 함께 겨눔 — 건드리지 않습니다
                continue
            res.append(block[last:m.start()])
            last = m.end()
            n += 1
        res.append(block[last:])
        return "".join(res)

    out, last = [], 0
    for m in re.finditer(r"(<style[^>]*>)([\s\S]*?)(</style>)", s):
        out.append(s[last:m.start()])
        out.append(m.group(1) + one(m.group(2)) + m.group(3))
        last = m.end()
    out.append(s[last:])
    return "".join(out), n


hits, tot, alive = [], 0, []
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s0 = io.open(p, encoding="utf-8", newline="").read()
    dead = dead_classes(s0)
    if not dead:
        continue
    body = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s0)
    still = sorted({n for n in re.findall(r"class=\"[^\"]*\b(exp-[a-z0-9-]+)", body)})
    if still:
        # ★아직 쓰는 것이 있는 파일 — 그 이름을 겨눈 규칙은 손대지 않습니다.
        alive.append((os.path.basename(p), still))
    s, n = strip(s0, dead)
    if not n:
        continue
    name = os.path.basename(p)
    assert vis(s) == vis(s0), f"{name}: 화면 글자가 바뀌었습니다"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
    for d in dead:
        assert not re.search(rf"\.{re.escape(d)}\b", css), f"{name}: {d} 가 남았습니다"
    live = {x for x in re.findall(r"\.(exp-[a-z0-9-]+)", css)}
    hits.append((p, name, s, n, sorted(dead), sorted(live)))
    tot += n

print(f"■ 지울 죽은 규칙 {tot}개 / {len(hits)}파일")
for _, name, _, n, dead, live in hits[:6]:
    print(f"     {n:>3}개  {name[:34]}  죽은 것 {','.join(dead)}"
          + (f"  · 남기는 것 {','.join(live)}" if live else ""))
if len(hits) > 6:
    print(f"     … 그리고 {len(hits)-6}파일 더")
if alive:
    print("\n★ 아직 쓰는 exp-* 가 있어 그 규칙을 남긴 파일")
    for name, still in alive:
        print(f"     {name}  ← {','.join(still)} (마크업에 살아 있음)")

if APPLY:
    for p, _, s, _, _, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print(f"\n■ 반영했습니다 — {len(hits)}파일에서 {tot}개")
else:
    print("\n※ 모의 실행입니다. 반영하려면 --apply")

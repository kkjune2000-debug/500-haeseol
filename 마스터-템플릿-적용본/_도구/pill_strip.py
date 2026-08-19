# -*- coding: utf-8 -*-
r"""표의 그러데이션 알약을 걷고 글자만 남깁니다 — 종별사 시안을 다섯 파일로 (2026-08-20).

    python pill_strip.py [--apply]

무엇을
    이 책의 표 첫 칸에 같은 style 문자열의 그러데이션 알약이 스물셋 남아 있습니다.
        <span style="display:inline-block;padding:4px 14px;border-radius:999px;
          background:linear-gradient(135deg,#fde68a,#fcd34d);color:#92400e;…">…</span>
    2026-08-19 관형어 시제 표 · 2026-08-20 종별사 표에서 정한 꼴로 바꿉니다.

★★ 알약이라고 다 같은 것을 가리키지 않습니다 — 어제 관형어 표가 이미 둘을 갈랐습니다.
      형태·어미·조사  → `<span class="accent">`   (그 표의 「형태」 열이 그랬습니다)
      이름·분류·명사  → `<strong>`                (그 표의 「품사」 열이 그랬습니다)
    그래서 표마다 무엇을 담은 열인지 보고 갈랐습니다.

      436~440  어미 ~(으)면 · ~(으)면서 · ~(으)러 · ~(으)려고      → accent
      489~500  조사 께서 · 께서는 · 께서도 · 께                    → accent
      408~413  의미 갈래 방향 · 수단 · 재료 · 원인 · 신분 · 변화    → strong
      414~418  시간 명사 아침 · 날 · 주말 · 해                     → strong
      462~473  문장 종류 평서문 · 이다 · 명령문 · 의문문 · 청유문   → strong

    ※ 419~435 종별사(13개)는 시안으로 먼저 했습니다(`0981bc6`).
    ※ 370~383 은 알약이 아니라 42×42 동그라미 안의 = · &gt; · &lt; 라 손대지 않습니다.
      436~440 의 다른 표 하나도 알약 글자가 0이라(줄 바탕 그러데이션) 그대로 둡니다.

★ 화면 글자는 한 글자도 바뀌지 않습니다. 파일마다 검산합니다.
★ 이 책의 파일은 CRLF 입니다. newline="" 로 읽고 씁니다.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

# ★글자 크기만 0.9rem · 0.92rem 두 가지입니다 — 하나로 잡지 않으면 둘이 남습니다
#   (2026-08-20에 370~383 의 두 개를 그렇게 놓칠 뻔했습니다).
PILL = re.compile(
    r'<span style="display:inline-block;padding:4px 14px;border-radius:999px;'
    r'background:linear-gradient\(135deg,#fde68a,#fcd34d\);color:#92400e;'
    r'font-weight:800;font-size:0\.9\d?rem;">(?:<strong>)?([^<]+?)(?:</strong>)?</span>')
# ★알약 속에 <strong> 이 든 것도 있습니다(436~440 의 자모 ㄴ·ㅂ·ㅅ). 안 감싸면 안 걸립니다.

PLAN = [
    # ★436~440 은 두 번에 걸쳐 걷었습니다 — 첫 판에서 어미 4개(맨 아래 표),
    #   그 뒤 알약 속에 <strong> 이 든 자모 3개(위 표)를 찾아 함께 걷었습니다.
    ("3 489~500 기타 문법 존댓말.html",     "accent", 4, "조사"),
    ("3 408~413 기타 문법 로 으로.html",    "strong", 6, "의미 갈래"),
    ("3 414~418 기타 문법 빈도부사.html",   "strong", 4, "시간 명사"),
    ("3 462~473 기타 문법 간접화법.html",   "strong", 5, "문장 종류"),
    ("3 370~383 기타 문법 비교급 최상급.html", "strong", 2, "범위 갈래"),
    # 같은 파일의 다른 표 — 알약 속에 <strong> 이 들어 앞선 그물에 안 걸렸습니다.
    ("3 436~440 기타 문법 ㄹ불규칙.html",   "accent", 3, "앞 글자 자모 ㄴ·ㅂ·ㅅ"),
]


def vis(x):
    x = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", x, flags=re.I)
    x = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", x, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()


done, hits = 0, []
for name, kind, want, what in PLAN:
    p = os.path.join(BOOK, name)
    s0 = io.open(p, encoding="utf-8", newline="").read()
    words = PILL.findall(s0)
    if not words:
        # ★두 번 돌려도 되도록 — 이미 걷은 파일은 건너뜁니다.
        #   0 이 아닌 다른 숫자는 그대로 걸립니다(파일이 바뀌었다는 뜻이므로).
        print(f"  · {name[:26]}  {what} — 이미 걷었습니다")
        continue
    print(f"  {'○' if len(words) == want else '✗'} {name[:26]}  {what} {len(words)}개 "
          f"→ {kind}   {' · '.join(words)}")
    assert len(words) == want, f"{name}: {want}개여야 합니다(찾은 것 {len(words)})"
    if kind == "accent":
        s = PILL.sub(lambda m: f'<span class="accent">{m.group(1)}</span>', s0)
    else:
        s = PILL.sub(lambda m: f'<strong>{m.group(1)}</strong>', s0)
    assert vis(s) == vis(s0), f"{name}: 화면 글자가 바뀌었습니다"
    for tg in ("span", "td", "tr", "table", "small", "strong", "em"):
        a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert a == b, f"{name}: <{tg}> 짝이 어긋남"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
    if kind == "accent":
        assert ".accent" in css, f"{name}: 이 파일에 .accent 규칙이 없습니다"
    assert not PILL.search(s), f"{name}: 알약이 남았습니다"
    hits.append((p, s, len(words)))
    done += len(words)

print(f"\n■ 알약 {done}개 / 파일 {len(hits)}개")
if APPLY:
    for p, s, _ in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 화면 글자는 그대로입니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

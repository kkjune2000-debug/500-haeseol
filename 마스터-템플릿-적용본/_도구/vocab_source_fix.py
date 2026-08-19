# -*- coding: utf-8 -*-
r"""어휘를 그 문항의 500문장 원문(영어)에 맞춥니다 — check_vocab_match 35곳 (사용자 결정 2026-08-20).

    python vocab_source_fix.py [--apply]

두 가지로 고칩니다 (사용자 결정: 「35곳 전부 · ㉯는 묶음 어휘로」)
    SET    뜻풀이만 원문 낱말로 바꿉니다        참 = really → so
    MERGE  둘을 묶어 원문 표현에 맞춥니다        비 · 오다 → 비가 오다 = rain

★ 묶음 표제어는 **정답 문장에 실제로 있는 말**만 씁니다(교재 밖 낱말 금지).
  「비가 오다」는 정답 「비가 안 왔으면 좋겠습니다」의 말이고, 08-19 에 320 을
  「배가 아프다 = have a stomachache」로 바꾼 것과 같은 꼴입니다.
★ 묶을 때는 08-19 의 조건을 지킵니다 — **부분이 정답에서 혼자 나오는 자리가 없을 때만**
  묶습니다. (비는 「비가」로만, 오다는 「왔으면·오려고」로만 나옵니다.)
★ 차례는 건드리지 않습니다 — 묶은 것은 **앞엣것 자리**에 그대로 둡니다(어휘 차례는
  한국어 정답 차례라는 규칙을 지키기 위해서입니다).

★★ 손대지 않는 열 곳 — 검사기 오탐입니다(원문에 이미 맞습니다)
    59 당신(=your) · 211 병원 · 234 11시 · 383 어머니 · 449·450 너무(= too, so) ·
    494 죽다 · 495 있다 · 500 아들·딸
    494·495 는 그 쪽이 가르치는 것이 **돌아가시다·계시다**이고 어휘는 바탕말입니다.
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv

ITEM = '<span class="%s"><b>%s</b><span class="gloss" lang="en" translate="yes">%s</span></span>'
# ★클래스가 두 가지입니다 — `v-item` 과 `v-item v-none`(「새 어휘 없음」 표시).
#   `v-item` 만 잡으면 v-none 이 안 걸려, 상자를 다시 쓸 때 **그것이 지워집니다.**
VI = re.compile(r'<span class="(v-item[^"]*)"><b>([\s\S]*?)</b>'
                r'<span class="gloss"[^>]*>([\s\S]*?)</span></span>')

# (문항, 갈래, 대상, 새 표제어, 새 뜻풀이)
JOBS = [
    (65,  "SET",   ["저기"],        None,          "that place, over there"),
    (96,  "SET",   ["저기"],        None,          "that place, over there"),
    (137, "SET",   ["말다"],        None,          "do not"),
    (223, "SET",   ["참"],          None,          "so"),
    (225, "SET",   ["참"],          None,          "so"),
    (229, "SET",   ["정말"],        None,          "so"),
    (229, "SET",   ["많이"],        None,          "much"),
    (235, "SET",   ["너무"],        None,          "really, so"),
    (341, "SET",   ["받다"],        None,          "get"),
    (354, "SET",   ["받다"],        None,          "get"),
    (358, "SET",   ["자다"],        None,          "go to bed, sleep"),
    (368, "SET",   ["타다"],        None,          "get on, ride"),

    (155, "MERGE", ["비", "오다"],      "비가 오다",       "rain"),
    (162, "MERGE", ["비", "오다"],      "비가 오다",       "rain"),
    (229, "MERGE", ["눈", "오다"],      "눈이 오다",       "snow"),
    (259, "MERGE", ["눈", "오다"],      "눈이 오다",       "snow"),
    (230, "MERGE", ["노래", "잘하다"],   "노래를 잘하다",    "sing well"),
    (252, "MERGE", ["노래", "부르다"],   "노래를 부르다",    "sing"),
    (309, "MERGE", ["교통사고", "나다"], "교통사고가 나다",  "have a car accident"),
    (332, "MERGE", ["담배", "끊다"],     "담배를 끊다",      "quit smoking"),
    (353, "MERGE", ["잠", "안 오다"],    "잠이 안 오다",     "can't sleep"),
    (362, "MERGE", ["돈", "없다"],       "돈이 없다",        "have no money"),
    (389, "MERGE", ["맛있게", "먹다"],   "맛있게 먹다",      "enjoy a meal"),
    (432, "MERGE", ["한", "다발"],       "한 다발",          "a bouquet"),
]


def vis(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()


def find_box(s, num):
    """그 문항의 v-list 구간 (시작, 끝) 을 냅니다."""
    heads = [(m.start(), m.end(), vis(m.group(1)))
             for m in re.finditer(r"<h3[^>]*>([\s\S]*?)</h3>", s)]
    for i, (a, b, t) in enumerate(heads):
        m = re.match(r"(\d{1,3})\)", t)
        if not m or int(m.group(1)) != num:
            continue
        end = heads[i + 1][0] if i + 1 < len(heads) else len(s)
        vm = re.search(r'<div class="v-list">([\s\S]*?)</div>', s[b:end])
        if vm:
            return b + vm.start(1), b + vm.end(1)
    return None


files, log = {}, []
for num, kind, targets, newhead, gloss in JOBS:
    hit = None
    for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        s = files.get(p) or io.open(p, encoding="utf-8", newline="").read()
        span = find_box(s, num)
        if not span:
            continue
        a, b = span
        inner = s[a:b]
        items = VI.findall(inner)
        heads = [h for _, h, _ in items]
        if not all(t in heads for t in targets):
            continue
        hit = (p, s, a, b, inner, items)
        break
    assert hit, f"{num}: 어휘 상자에서 {targets} 를 못 찾았습니다"
    p, s, a, b, inner, items = hit

    new_items, dropped = [], 0
    for cls, h, g in items:
        if kind == "SET" and h == targets[0]:
            new_items.append((cls, h, gloss))
        elif kind == "MERGE" and h == targets[0]:
            new_items.append((cls, newhead, gloss))
        elif kind == "MERGE" and h in targets[1:]:
            dropped += 1
        else:
            new_items.append((cls, h, g))
    assert len(new_items) == len(items) - dropped
    if kind == "MERGE":
        assert dropped == len(targets) - 1, f"{num}: 묶을 것을 다 못 찾았습니다"
    body = "\n        " + " ".join(ITEM % it for it in new_items) + "\n    "
    files[p] = s[:a] + body + s[b:]
    log.append((num, kind,
                " · ".join(f"{h} = {g}" for _, h, g in items if h in targets),
                " · ".join(f"{h} = {g}" for _, h, g in new_items
                           if h == (newhead or targets[0]))))

print(f"■ 고칠 자리 {len(JOBS)}개 / 파일 {len(files)}개\n")
for num, kind, before, after in log:
    print(f"  {num:>3} {kind:<6} {before}")
    print(f"      →     {after}")

# ── 검산
KO = re.compile(r"[가-힣]")
for p, s in files.items():
    name = os.path.basename(p)
    s0 = io.open(p, encoding="utf-8", newline="").read()
    for tg in ("span", "b", "div"):
        x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        assert x == y, f"{name}: <{tg}> 짝이 어긋남"
    for m in re.finditer(r'<div class="v-list">([\s\S]*?)</div>', s):
        got = VI.findall(m.group(1))
        assert got, f"{name}: 빈 어휘 상자"
        hs = [h for _, h, _ in got]
        assert len(hs) == len(set(hs)), f"{name}: 표제어가 겹칩니다 {hs}"
        for _, h, g in got:
            assert g.strip(), f"{name}: 뜻풀이가 빈 표제어 {h}"
            # ★뜻풀이 속 한국어는 <span lang="ko" translate="no"> 로 **잠가서** 씁니다
            #   (「love (a 하다 verb)」). 잠긴 것을 뺀 뒤에 세야 합니다.
            bare = re.sub(r'<span lang="ko" translate="no">[\s\S]*?</span>', "", g)
            assert not KO.search(bare), f"{name}: 안 잠긴 한국어가 뜻풀이에 {h} = {g}"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
print("\n■ 검산 통과 — 태그 짝 · 빈 상자 0 · 겹친 표제어 0 · 뜻풀이 속 한국어 0")

if APPLY:
    for p, s in files.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

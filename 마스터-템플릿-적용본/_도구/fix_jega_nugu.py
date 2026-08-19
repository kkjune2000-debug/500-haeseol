# -*- coding: utf-8 -*-
r"""① 만들기 「저 + 가」 → 「저 + 가 = 제가」  ② 어휘 「누구를」 → 「누구」 (사용자 지시)

  ① 정답이 「제가 …」인데 만들기는 「저 + 가」에서 멈춰 있었습니다.
     같은 파일 51번이 이미 「누구 + 가 = 누구가 = 누가」로 바뀜을 보여 줍니다.
     52·367 두 곳입니다.
  ② 표제어에 조사가 붙어 있었습니다 — 「누구를」 → 「누구」.
     뜻풀이의 「(object)」도 뗍니다(조사가 없어졌으므로 틀린 말이 됩니다).
     53·148 두 곳입니다.

  ※ 51번의 「누가 who (subject)」는 그대로 두었습니다 — 「누가」는 조사가 붙은
    꼴 그대로가 표제어이고 뜻풀이도 맞습니다. 함께 바꿀지는 사용자 결정입니다.

사용: python fix_jega_nugu.py [--apply]
"""
import io, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
vis = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
APPLY = "--apply" in sys.argv

OLD_MK = "<strong>저</strong> + <strong>가</strong>"
NEW_MK = "<strong>저</strong> + <strong>가</strong> = <strong>제가</strong>"
OLD_V = "<b>누구를</b>"
NEW_V = "<b>누구</b>"
OLD_G = "who (object)"
NEW_G = "who"

n_mk = n_v = n_g = 0
for f in sorted(glob.glob("*.html")):
    s0 = io.open(f, encoding="utf-8").read()
    s = s0

    # ① 만들기 — wo-mk 안에 있는 것만
    for m in list(re.finditer(r'<span class="wo-mk">([\s\S]*?)</span>\s*'
                              r'(?=<span class="wo-mk"|</div>)', s))[::-1]:
        if vis(m.group(1)) != "저 + 가":
            continue
        if OLD_MK not in m.group(1):
            print(f"   X {f[:26]} 만들기 글자가 다름: {m.group(1)[:60]}")
            continue
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:m.start()])
        nb = m.group(1).replace(OLD_MK, NEW_MK)
        s = s[:m.start(1)] + nb + s[m.end(1):]
        n_mk += 1
        print(f"   [{hs[-1]}] 만들기  저 + 가  →  저 + 가 = 제가")

    # ② 어휘 표제어와 뜻풀이
    #   ★표제어에서 **뒤로 걸어가** 그 항목의 시작을 찾는다.
    #     앞에서부터 비탐욕으로 잡으면 앞 항목부터 물어 구간이 엉뚱해진다.
    for m in list(re.finditer(re.escape(OLD_V), s))[::-1]:
        a = s.rfind('<span class="v-item', 0, m.start())
        if a < 0:
            print(f"   X {f[:26]} 항목 시작을 못 찾음"); continue
        d, i = 1, s.index(">", a) + 1
        while d and i < len(s):
            t = re.compile(r"</?span\b").search(s, i)
            if not t:
                break
            d += -1 if t.group(0).startswith("</") else 1
            i = t.end()
        e = s.find(">", i - 1) + 1
        hs = re.findall(r'<h3><span lang="en" translate="yes">(\d+)\)', s[:a])
        nb = s[a:e].replace(OLD_V, NEW_V)
        if OLD_G in nb:
            nb = nb.replace(OLD_G, NEW_G); n_g += 1
        s = s[:a] + nb + s[e:]
        n_v += 1
        print(f"   [{hs[-1]}] 어휘    {vis(s[a:a + (e - a) + 20])[:26]}  ←  누구를 who (object)")

    if s != s0:
        for tg in ("span", "b", "strong", "div"):
            a = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
            b = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
            assert a == b, f"{tg} 짝이 어긋남 {f}"
        assert len(re.findall(r'class="v-item', s)) == \
               len(re.findall(r'class="v-item', s0)), f"어휘 수가 바뀜 {f}"
        if APPLY:
            io.open(f, "w", encoding="utf-8").write(s)
            print(f"   ■ 씀 {f[:32]}")

print(f"\n■ 만들기 {n_mk}곳 · 어휘 표제어 {n_v}곳 · 뜻풀이 {n_g}곳")
assert n_mk == 2 and n_v == 2, "만들기 2곳·어휘 2곳이어야 합니다"

# -*- coding: utf-8 -*-
r"""검사 ⑤ 다국어 — 표 머리 순서 · 번역 슬롯이 부호를 가르는가

  글자만 보면 되므로 빠릅니다(브라우저가 필요 없습니다). 대량 편집 뒤에 돌리십시오.

  ① 표 머리에서 영어가 한국어보다 먼저 오는가
     이 책의 머리는 한국어가 위입니다 — 「역할 / Role」·「의미 / Meaning」.
     ★ 헛걸림을 막는 잣대: 한국어가 **아예 없는** 머리(Examples · Verbs)는
       대상이 아닙니다. 그것이 옳습니다. 둘 다 있을 때만 순서를 봅니다.
     ★ 2026-08-18 에 69곳을 고쳤습니다. 그때 「Korean order: …」 11곳을
       「영어 문장이라 오탐」이라고 잘못 판단했는데, 세어 보니 같은 제목 행이
       489개는 한국어 먼저 · 11개만 영어 먼저였습니다. 짐작하지 말고 세십시오.

  ② 번역 슬롯이 부호 짝을 반으로 가르는가
     나쁜 꼴  <span lang="en">Present (~</span>게 되다)
              → 일본어판에서 「現在 (~」 뒤에 「게 되다)」 가 남습니다.
     ★★ 잣대가 결정적입니다. 「슬롯 안에서 짝이 안 맞으면」으로 세면 564곳이
       나오는데 대부분 **문장 번호 「489)」** 입니다. 모자란 짝이 **슬롯 바로
       밖에** 있을 때만 세야 진짜만 남습니다(2026-08-18 기준 0곳).

쓰기: python check_i18n.py
"""
import re, glob, html
from collections import Counter
import _paths

out = _paths.enter()
KO = re.compile(r"[가-힣]")
EN = re.compile(r"[A-Za-z]{2,}")
SLOT = re.compile(r'<(\w+)([^>]*\btranslate="yes"[^>]*)>')
PAIRS = [("(", ")"), ("「", "」"), ("『", "』"), ("[", "]")]
NEAR = 40


def body_of(s):
    return re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->", " ", s)


def plain(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x))


def vis(x):
    """잠긴 한국어(영어 안의 인용)는 순서 판정에서 뺀다"""
    x = re.sub(r'<span lang="ko" translate="no">[\s\S]*?</span>', " ", x)
    return re.sub(r"\s+", " ", plain(x)).strip()


def close_of(s, i, tag):
    d, j = 1, i
    pat = re.compile(rf"<{tag}\b|</{tag}\s*>")
    while d:
        m = pat.search(s, j)
        if not m:
            return None, None
        d += 1 if m.group(0)[1] != "/" else -1
        j = m.end()
    return s[i:m.start()], m.end()


th_bad, sl_bad = [], []
n_th = n_slot = 0
for f in sorted(glob.glob("*.html")):
    body = body_of(open(f, encoding="utf-8").read())

    for m in re.finditer(r"<th\b[^>]*>([\s\S]*?)</th>", body):
        n_th += 1
        t = vis(m.group(1))
        ko, en = KO.search(t), EN.search(t)
        if ko and en and en.start() < ko.start():
            th_bad.append((f, body[:m.start()].count("\n") + 1, t[:60]))

    for m in SLOT.finditer(body):
        inner, end = close_of(body, m.end(), m.group(1))
        if inner is None:
            continue
        n_slot += 1
        txt = plain(inner)
        pre = plain(body[max(0, m.start() - NEAR):m.start()])
        post = plain(body[end:end + NEAR])
        for a, b in PAIRS:
            na, nb = txt.count(a), txt.count(b)
            if na == nb:
                continue
            # ★ 모자란 짝이 슬롯 **바로 밖**에 있어야 진짜다
            if (na > nb and b in post and a not in post.split(b)[0]) or \
               (nb > na and a in pre and b not in pre.split(a)[-1]):
                sl_bad.append((f, body[:m.start()].count("\n") + 1,
                               f"{a}…|…{b}", txt.strip()[:52]))
            break

out.write(f"■ 표 머리 {n_th}개 · 번역 슬롯 {n_slot}개\n\n")
out.write(f"── 표 머리에 영어가 먼저 ({len(th_bad)}) ──\n")
for f, ln, t in th_bad[:30]:
    out.write(f"   {f[:34]:<36} {ln:>5}행  {t}\n")
if len(th_bad) > 30:
    out.write(f"   … {len(th_bad)-30}건 더\n")
out.write(f"\n── 슬롯이 부호를 가름 ({len(sl_bad)}) ──\n")
for f, ln, k, t in sl_bad[:30]:
    out.write(f"   {f[:34]:<36} {ln:>5}행 [{k}]  {t}\n")
if len(sl_bad) > 30:
    out.write(f"   … {len(sl_bad)-30}건 더\n")
out.write(f"\n■ 모두 {len(th_bad)+len(sl_bad)}건. 0건이어야 정상입니다.\n")
out.flush()

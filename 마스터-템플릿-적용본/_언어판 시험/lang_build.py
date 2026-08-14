# -*- coding: utf-8 -*-
"""언어판 빌더 — 기본 책은 한 글자도 고치지 않고 언어판 파일만 새로 만든다.
세 가지를 처리한다.
  ① 번역 슬롯 (translate="yes")            — 영어 → 그 언어
  ② UI 라벨 (한국어 + .gloss 짝)            — 한국어 줄을 그 언어로 바꾸고 gloss 는 지운다
  ③ 스크립트 안 문구 · 문장 데이터           — 문자열 리터럴을 표대로 바꾼다
사용: python lang_build.py <원본> <번역표.py> <낼파일>
"""
import re, sys, io, os, importlib.util
out = io.TextIOWrapper(open(sys.stdout.fileno(), "wb", closefd=False), encoding="utf-8")

LOCK = re.compile(r'<span[^>]*translate="no"[^>]*>.*?</span>', re.S)
ATTRS = ("title", "placeholder", "alt")


def close_of(s, start, tag):
    d = 0
    for m in re.finditer(rf"<{tag}\b[^>]*>|</{tag}\s*>", s[start:]):
        d += -1 if m.group(0).startswith("</") else 1
        if d == 0:
            return start + m.start()
    return -1


def guard(s):
    g = []
    for rx in (r"<script\b.*?</script>", r"<style\b.*?</style>"):
        g += [(m.start(), m.end()) for m in re.finditer(rx, s, flags=re.S)]
    return g


def slots(s):
    g = guard(s)
    hits = []
    for m in re.finditer(r'<(\w+)\b[^>]*\btranslate="yes"[^>]*>', s):
        if any(x <= m.start() < y for x, y in g):
            continue
        e = close_of(s, m.start(), m.group(1))
        if e < 0:
            continue
        hits.append((m.start(), m.end(), e, m.group(0)))
    hits.sort(key=lambda h: (h[0], -h[2]))
    kept, last = [], -1
    for h in hits:
        if h[0] < last:
            continue
        kept.append(h); last = h[2]
    return kept


def build(src, tr, dst):
    s = open(src, encoding="utf-8").read()
    rep = {"슬롯": 0, "슬롯 빠짐": 0, "UI 라벨": 0, "속성": 0, "스크립트": 0}
    miss = set()

    # ── ① 번역 슬롯 ────────────────────────────────────
    edits = []
    for a, b, e, opentag in slots(s):
        inner = s[b:e]
        locks = []
        masked = LOCK.sub(lambda m: (locks.append(m.group(0)), "{%d}" % (len(locks) - 1))[1], inner)
        key = masked.strip()
        newinner = inner
        if key and re.search(r"[A-Za-z]", key):
            if key in tr.TEXT:
                v = tr.TEXT[key]
                for i, lk in enumerate(locks):
                    v = v.replace("{%d}" % i, lk)
                newinner = v
                rep["슬롯"] += 1
            else:
                miss.add(key); rep["슬롯 빠짐"] += 1
        newopen = opentag
        for at in ATTRS:
            am = re.search(at + r'="([^"]*)"', opentag)
            if am and am.group(1) in tr.TEXT:
                newopen = newopen.replace(am.group(0), at + '="' + tr.TEXT[am.group(1)] + '"')
                rep["속성"] += 1
        edits.append((a, e, newopen + newinner))
    for a, e, r in sorted(edits, reverse=True):
        s = s[:a] + r + s[e:]

    # ── ② UI 라벨: 「한국어 + .gloss 영어」 짝 ─────────
    #    한국어 줄을 그 언어로 바꾸고, 뜻이 겹치는 gloss 는 지운다
    #    한국어 라벨 뒤에 <br>·<small> 이 낄 수 있고, gloss 클래스가 없는 슬롯도 있다
    keys = sorted(tr.UI, key=len, reverse=True)
    # ★UI 표가 비면 "|".join 이 빈 갈래가 되어 빈 글자에 걸린다 (KeyError: '').
    #   표를 갓 만들어 UI 가 아직 빈 언어판에서 터진다.
    KEY = re.compile(r"(>|\A)(\s*)(" + "|".join(re.escape(k) for k in keys) +
                     r")(\s*)(<br\s*/?>)?\s*(<small[^>]*>)?\s*(<span[^>]*translate=\"yes\"[^>]*>)") if keys else None
    parts, pos = [], 0
    while KEY:
        m = KEY.search(s, pos)
        if not m:
            break
        d, end = 0, None
        for mm in re.finditer(r"<span\b[^>]*>|</span\s*>", s[m.start(7):]):
            d += -1 if mm.group(0).startswith("</") else 1
            if d == 0:
                end = m.start(7) + mm.end()
                break
        if end is None:
            pos = m.end(); continue
        if m.group(6):                       # <small> 을 열었으면 </small> 도 먹는다
            cm = re.match(r"\s*</small\s*>", s[end:])
            if cm:
                end += cm.end()
        parts.append(s[pos:m.start(2)] + m.group(2) + tr.UI[m.group(3)])
        pos = end
        rep["UI 라벨"] += 1
    parts.append(s[pos:])
    s = "".join(parts)

    # ── ②-ㄴ 영어 짝이 없는 한국어 전용 UI ─────────────
    #    글자 조각 전체가 표의 열쇠와 똑같을 때만 바꾼다 (학습 내용 오염 방지)
    solo = getattr(tr, "SOLO", {})
    if solo:
        g2 = guard(s)
        parts, pos = [], 0
        for m in re.finditer(r">([^<>]+)<", s):
            if any(x <= m.start() < y for x, y in g2):
                continue
            body = m.group(1)
            k = body.strip()
            if k not in solo:
                continue
            head = body[:len(body) - len(body.lstrip())]
            tail = body[len(body.rstrip()):]
            parts.append(s[pos:m.start(1)] + head + solo[k] + tail)
            pos = m.end(1)
            rep["한국어 전용 UI"] = rep.get("한국어 전용 UI", 0) + 1
        parts.append(s[pos:])
        s = "".join(parts)

    # ── ③ 스크립트 안 문자열 ───────────────────────────
    def fix_js(m):
        js = m.group(0)
        for k, v in tr.JS.items():
            for q in ("'", '"'):
                if q + k + q in js:
                    js = js.replace(q + k + q, q + v + q)
                    rep["스크립트"] += 1
        return js
    s = re.sub(r"<script\b.*?</script>", fix_js, s, flags=re.S)

    # ── ④ <title> ─────────────────────────────────────
    #    ★<title> 안에는 자식 태그를 못 넣어 <span translate="no"> 로 부분만 잠글 수 없다.
    #    그래서 한국어가 든 제목 80개는 통째로 잠갔다(translate="no") — 안 그러면
    #    브라우저 번역이 문법 항목인 「에」·「은는」·「ㄹ받침」까지 옮겨 버린다.
    #    잠긴 제목은 ①번 슬롯에 안 걸리므로 여기서 통째로 갈아 끼운다.
    #    아직 열려 있는 제목(영어뿐)은 ①이 이미 했으므로 건드리지 않는다.
    def fix_title(m):
        if 'translate="yes"' in m.group(1):
            return m.group(0)
        key = m.group(2).strip()
        v = getattr(tr, "TITLE", {}).get(key) or tr.TEXT.get(key)
        if not v:
            rep["제목 빠짐"] = rep.get("제목 빠짐", 0) + 1
            miss.add(key)
            return m.group(0)
        rep["제목"] = rep.get("제목", 0) + 1
        return "<title" + m.group(1) + ">" + v + "</title>"
    s = re.sub(r"<title([^>]*)>(.*?)</title>", fix_title, s, count=1, flags=re.S)

    s = re.sub(r'<html lang="ko"', '<html lang="%s"' % tr.LANG, s, count=1)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(s)
    out.write("■ " + os.path.basename(dst) + "\n")
    for k, v in rep.items():
        out.write(f"   {k}: {v}\n")
    if miss:
        out.write(f"   ★ 번역표에 없는 슬롯 {len(miss)}가지\n")
        for x in sorted(miss)[:20]:
            out.write(f"      {x[:90]}\n")
    return miss


if __name__ == "__main__":
    src, trpath, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = importlib.util.spec_from_file_location("tr", trpath)
    tr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tr)
    build(src, tr, dst)
    out.flush()

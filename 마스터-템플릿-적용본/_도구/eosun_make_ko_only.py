# -*- coding: utf-8 -*-
r"""만들기 줄에서 영어 주석을 지운다 — 한국어만 남긴다 (사용자 지시 2026-08-19)

  왜  옛 해설 칸에서 딸려 온 영어 주석 24곳이 만들기 안에 남아 있었다.
      「만들기는 한국어뿐이라 36언어 번역 비용 0」이라던 말이 그만큼 틀렸다.

  ★ 세어 보고 말할 것 — 처음에 「21곳이 같은 줄에 섞였다」고 보고했는데 **틀렸다.**
    브라우저로 재니 **정말 같은 줄인 것은 6곳뿐**(262·345·461 네 줄)이고,
    나머지는 <br> 뒤라 이미 아래 줄이었다. 거친 잣대가 「영어 줄 안의
    ko-guard 한국어」(「(no ㄷ-irregular before 고)」)까지 세었다.
    check_koen_line.py 는 이 함정을 이미 알고 「줄의 첫 조각이 영어 슬롯이면
    영어 줄」로 거르는데, 내가 급히 만든 잣대는 그 걸름을 빠뜨렸다.

  꼴  거의 다 이 모양이다 —
        <strong>한국어 사슬</strong> <br> <small class="en-line" lang="en" translate="yes">영어</small>
      그 <small> 과 앞의 <br> 을 지운다.

  ★ 남는 이음표를 정리해야 한다
      262  …<small>(plan to)</small> - <strong>따려고 하다</strong>   → 「-」를 지우고 <br> 는 남긴다(두 줄)
      345  …<small>(negative)</small> + <strong>으려고</strong>      → <br> 을 지워 한 줄로 잇는다
  ★ 461 첫 줄은 영어가 문장 사이사이에 박혀 있어 지우기만 하면 한국어가 깨진다
      「병이 낫다 is a 서술절 … — functions as … 그는. 병이 = …」
      → 뜻을 그대로 두고 한국어 사슬로 다시 적는다(설명 자리이므로 한국어 작성 가능).

사용: python eosun_make_ko_only.py [--apply]
"""
import re, sys, glob, html, argparse
from collections import Counter
sys.path.insert(0, r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본\_도구")
import _paths

out = _paths.enter()
ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
A = ap.parse_args()

vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()

SMALL = re.compile(r'\s*<small class="en-line"[^>]*>[\s\S]*?</small>\s*')
ENSPAN = re.compile(r'\s*<span lang="en" translate="yes">[^<]*</span>\s*')

# 461 첫 줄 — 영어를 걷어내면 한국어가 깨지므로 뜻 그대로 한국어 사슬로
OLD461 = ('<strong>병이 낫다</strong> <span lang="en" translate="yes">is a</span> '
          '<strong>서술절</strong>')
NEW461 = ('<strong>병이 낫다</strong> = <strong>서술절</strong> · '
          '<strong>그는</strong> = 바깥 주어 · <strong>병이</strong> = '
          '<strong>서술절의 주어</strong> → <strong>이중주어 구문</strong>')

stat = Counter()
work = {}

for f in sorted(glob.glob("*.html")):
    s0 = open(f, encoding="utf-8").read()
    if 'class="wo-mk"' not in s0:
        continue
    s = s0
    for m in list(re.finditer(r'<span class="wo-mk">(.*?)</span>\s*'
                              r'(?=<span class="wo-mk"|</div>)', s, re.S))[::-1]:
        body = m.group(1)
        if not re.search(r"[A-Za-z]{2,}", vis(body)):
            continue
        if re.fullmatch(r"[^A-Za-z]*(BTS|KTX)[^A-Za-z]*", vis(body)):
            stat["고유명사 그대로"] += 1
            continue

        new = body
        if OLD461 in new:                      # 461 첫 줄 — 다시 적는다
            head = new[:new.index(OLD461)]
            new = head + NEW461
            stat["다시 적음"] += 1
        else:
            new = SMALL.sub(" ", new)
            new = ENSPAN.sub(" ", new)
            # 남는 이음표 정리
            new = re.sub(r"<br>\s*-\s*", "<br> ", new)      # 262 「-」
            new = re.sub(r"<br>\s*(?=[+→=])", " ", new)     # 345 이어지는 줄
            new = re.sub(r"\s*<br>\s*$", "", new)           # 끝에 남은 <br>
            new = re.sub(r"\s{2,}", " ", new).strip()
            stat["영어 지움"] += 1

        if re.search(r"[A-Za-z]{2,}", re.sub(r"BTS|KTX", "", vis(new))):
            out.write(f"   X 영어가 남음 {f[:24]} : {vis(new)[:70]}\n")
            stat["어긋남"] += 1
            continue
        out.write(f"   {vis(body)[:62]:<64}→  {vis(new)[:56]}\n")
        s = s[:m.start(1)] + new + s[m.end(1):]

    if s != s0:
        work[f] = (s0, s)

# ── 검산
for f, (o0, s) in work.items():
    for tg in ("span", "strong", "small", "em", "div", "ol", "li"):
        if len(re.findall(rf"<{tg}\b", s)) != len(re.findall(rf"</{tg}\s*>", s)):
            out.write(f"   ★ {tg} 짝 {f[:26]}\n"); stat["★"] += 1
    if len(re.findall(r'class="wo-mk"', s)) != len(re.findall(r'class="wo-mk"', o0)):
        out.write(f"   ★ 만들기 줄 수 {f[:26]}\n"); stat["★"] += 1
    if vis(s).count(">") != vis(o0).count(">"):
        out.write(f"   ★ 보이는 꺾쇠 {f[:26]}\n"); stat["★"] += 1
    stat["파일"] += 1

if A.apply and not stat["★"] and not stat["어긋남"]:
    for f, (o0, s) in work.items():
        open(f, "w", encoding="utf-8").write(s); stat["파일 씀"] += 1

out.write("\n■ 반영\n" if A.apply else "\n■ 모의\n")
for k, v in sorted(stat.items()):
    out.write(f"   {k}: {v}\n")
out.flush()

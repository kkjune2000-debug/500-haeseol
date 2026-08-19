# -*- coding: utf-8 -*-
"""어순 해설 표의 **해설 칸**에 한국어와 영어가 한 줄에 있는가. 2026-08-19 작성.

    python check_exp_line.py

규칙(사용자 지시, 2026-08-19)
    「해설에 영어 해석을 넣을 때에는 반드시 같은 줄에 넣지 말고 아래 줄에」

★ check_koen_line.py 로는 못 잡습니다 — 그 그물은 **한국어 문장**(니다./세요. …)이
  끝난 뒤 영어가 오는 줄을 봅니다. 해설 칸은 「~보다 = comparison particle」처럼
  **문장이 아닌 조각**이라 통과해 버립니다. 그래서 칸을 따로 봅니다.

재는 법 (소스로 봅니다 — 이 칸은 짜임이 하나뿐이라 그려 볼 것 없습니다)
  어순 해설 표의 넷째 칸(해설)에 한국어와 영어가 **둘 다** 있는데
  <br> · en-line · gloss 가 하나도 없으면 = 한 줄에 섞인 것.

고치는 꼴 (이 책의 관례)
  <td>한국어<br><small class="en-line" lang="en" translate="yes"><em>영어</em></small></td>
  ★영어 줄 안의 한국어는 ko-guard 로 잠급니다 — <span lang="ko" translate="no">ㅅ</span>
"""
import io, os, re, sys, glob, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
KO = re.compile(r"[가-힣]")
EN = re.compile(r"[A-Za-z]{2,}")


def vis(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def main():
    tot = nf = 0
    for f in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
        s = io.open(f, encoding="utf-8").read()
        hits = []
        for tm in re.finditer(r"<table[\s\S]*?</table>", s):
            if "해설" not in tm.group(0):
                continue
            for r in re.finditer(r"<tr[\s\S]*?</tr>", tm.group(0)):
                cs = re.findall(r"<td[\s\S]*?</td>", r.group(0))
                if len(cs) < 4:
                    continue
                c = cs[3]
                v = vis(c)
                if not (KO.search(v) and EN.search(v)):
                    continue
                if "<br>" in c or "en-line" in c or 'class="gloss"' in c:
                    continue          # 이미 줄이 나뉨
                hits.append((vis(cs[2])[:18], v[:74]))
        if hits:
            nf += 1
            tot += len(hits)
            print(f"\n=== {os.path.basename(f)}  ({len(hits)})")
            for ko, v in hits:
                print(f"   {ko:<20}{v}")
    print(f"\n■ 모두 {tot}곳 / {nf}파일. 0곳이어야 정상입니다.")


if __name__ == "__main__":
    main()

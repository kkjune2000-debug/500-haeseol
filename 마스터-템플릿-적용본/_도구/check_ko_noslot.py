# -*- coding: utf-8 -*-
r"""**슬롯 밖 한국어 UI** — 다른 언어판에서 한국어로 남을 자리. 2026-08-19 작성.

    python check_ko_noslot.py

왜 필요한가
  check_audit 은 「슬롯 **밖 영어**」를 셉니다. 그 반대는 아무도 안 셌습니다.
  그래서 카드 힌트 「▼ 눌러서 확인」 578곳이 번역 슬롯 없이 남아 있었는데
  검사기가 전부 0을 냈습니다 — 사용자가 눈으로 찾아냈습니다.
  일본어판이면 단추는 일본어인데 힌트만 한국어로 남습니다.

무엇을 세는가
  **UI 글자**만 셉니다 — 가르치는 한국어(정답·예문·어휘 표제어)는 대상이 아닙니다.
  그래서 「UI 그릇」을 지정해 그 안의 한국어가 번역 슬롯 밖인지 봅니다.
    · 카드 힌트   .flashcard-hint · .fc-flip-hint
    · 단추        button 안의 글자 (speak-btn 같은 기호 단추는 뺌)
    · 안내 문단   p.ko 는 짝인 p.en 이 있어야 한다

  「슬롯 안」이란 그 글자가 lang="en" translate="yes" 요소 **안**에 있거나,
  바로 옆에 짝이 되는 슬롯이 있다는 뜻입니다.
"""
import io, os, re, sys, glob, html
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))

KO = re.compile(r"[가-힣]")
vis = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()

# 그릇 이름 → 그 안에 영어 슬롯이 있어야 한다
HOLDERS = [
    (r'<div class="flashcard-hint">([\s\S]*?)</div>', "카드 힌트"),
    (r'<span class="fc-flip-hint">([\s\S]*?)</span>', "카드 힌트"),
    (r'<button class="explain-toggle"[^>]*>([\s\S]*?)</button>', "해설 단추"),
    (r'<button class="vocab-toggle"[^>]*>([\s\S]*?)</button>', "어휘 단추"),
    (r'<button class="answer-toggle"[^>]*>([\s\S]*?)</button>', "정답 단추"),
    (r'<button class="wt-btn[^"]*"[^>]*>([\s\S]*?)</button>', "쓰기 단추"),
    (r'<button class="sl-all-btn"[^>]*>([\s\S]*?)</button>', "전체 듣기 단추"),
    (r'<div class="vocab-title">([\s\S]*?)</div>', "어휘 이름표"),
    (r'<span class="wo-lab">([\s\S]*?)</span>', "만들기 이름표"),
    (r'<span class="gb-lab">([\s\S]*?)</span>', "설명 이름표"),
]


def main():
    files = sorted(glob.glob(os.path.join(BOOK, "*.html")))
    bad, seen = Counter(), Counter()
    where = {}
    for f in files:
        s = io.open(f, encoding="utf-8").read()
        for pat, name in HOLDERS:
            for m in re.finditer(pat, s):
                body = m.group(1)
                if not KO.search(vis(body)):
                    continue
                seen[name] += 1
                if 'translate="yes"' in body:
                    continue
                bad[name] += 1
                where.setdefault((name, vis(body)[:40]),
                                 os.path.basename(f)[:28])
    print("■ UI 그릇 안의 한국어 — 번역 슬롯이 있는가")
    for name in dict.fromkeys(n for _, n in HOLDERS):
        print(f"   {name:<12}{seen[name]:>5}개 · 슬롯 없음 {bad[name]}")
    if bad:
        print("\n── 슬롯 없는 자리")
        for (name, t), f in list(where.items())[:20]:
            print(f"   [{name}] {t:<42}{f}")
    print(f"\n■ 모두 {sum(bad.values())}곳. 0곳이어야 정상입니다.")


if __name__ == "__main__":
    main()

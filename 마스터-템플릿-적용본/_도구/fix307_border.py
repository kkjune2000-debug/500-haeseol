# -*- coding: utf-8 -*-
r"""307~313 만 줄 바탕색 규칙이 border-color 까지 정해 왼쪽 강조선을 덮었다.
   다른 66파일은 바탕색만 정한다 — 기준(문장구조 2)에 맞춰 border-color 를 걷는다."""
import io, re, sys

P = (r"D:\OneDrive\놀라운 한국어 500 해설집\마스터-템플릿-적용본"
     r"\놀라운 한국어 500문장 해설 최종\3 307~313 부사어 문법 원인 때문에.html")
s0 = io.open(P, encoding="utf-8").read()
s = s0
hit = 0
for m in list(re.finditer(r"([^{}]+)\{([^{}]*)\}", s))[::-1]:
    sel = re.sub(r"\s+", " ", m.group(1)).strip()
    if "nth-child" not in sel or "writing-item" not in sel:
        continue
    body = m.group(2)
    if "border-color" not in body:
        continue
    nb = re.sub(r"\s*border-color\s*:[^;]*;?", "", body)
    s = s[:m.start(2)] + nb + s[m.end(2):]
    hit += 1
    print(f"   {sel[-46:]}  →  {re.sub(chr(10),' ',nb).strip()}")

css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
print(f"\n■ 고친 규칙 {hit}개 · CSS 중괄호 {css.count('{')}/{css.count('}')}")
if hit == 7 and css.count("{") == css.count("}") and "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8").write(s)
    print("■ 씀")

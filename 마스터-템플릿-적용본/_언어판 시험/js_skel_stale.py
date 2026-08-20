# -*- coding: utf-8 -*-
r"""사전 뼈대가 얼마나 낡았는가 — 죽은 열쇠를 셉니다 (2026-08-21).

    python js_skel_stale.py

왜
    `js_사전_뼈대.py` 는 **2026-08-12 스냅숏**입니다. 빌더는 열쇠가 **소스에 적힌 그대로**
    여야 찾습니다 — 그 뒤에 스크립트 문자열을 한 글자라도 고쳤으면 **그 줄은 오류 없이
    조용히 죽습니다.** 08-19 에 카드 힌트 33곳(`▼ 눌러서 확인` → `▼ Tap to check`)을
    바꿨고 그 뒤로도 손댄 곳이 있습니다.

    이 도구는 고치지 않습니다. **몇 줄이 죽었는지만** 셉니다.
"""
import io, os, re, sys, glob, ast

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.normpath(os.path.join(HERE, "..", "놀라운 한국어 500문장 해설 최종"))

# ★인수로 받은 파일을 읽습니다 — 2026-08-21에 여기서 인수를 무시하고 뼈대만 읽어
#   tr_ja 를 본다고 하고선 뼈대를 다시 보고 있었습니다.
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "js_사전_뼈대.py")
if not os.path.isabs(path):
    p2 = os.path.join(HERE, path)
    if os.path.isfile(p2):
        path = p2
skel = io.open(path, encoding="utf-8", errors="replace").read()
print(f"■ 보는 파일: {os.path.basename(path)}")

# ★파이썬 소스이므로 **정규식이 아니라 파서**로 읽습니다 — 따옴표가 든 열쇠에서
#   정규식은 끊깁니다(오늘 여러 번 겪었습니다).
keys = []
try:
    tree = ast.parse(skel)
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.append(k.value)
except SyntaxError as e:
    print("뼈대를 파싱하지 못했습니다:", e)
    sys.exit(1)

keys = [k for k in keys if k.strip()]
uniq = sorted(set(keys))
src = "".join(io.open(f, encoding="utf-8", newline="", errors="replace").read()
              for f in glob.glob(os.path.join(BOOK, "*.html")))

dead = [k for k in uniq if k not in src]
print(f"■ 뼈대 열쇠 {len(uniq):,}가지 (자리 {len(keys):,})")
print(f"■ 지금 소스에 **없는** 열쇠 {len(dead)}가지 — 그 줄은 조용히 죽습니다")
for k in dead[:20]:
    print("     " + repr(k)[:100])
if len(dead) > 20:
    print(f"     … 그리고 {len(dead)-20}가지 더")

# 거꾸로 — 소스에는 있는데 뼈대에 없는 것(새로 생긴 문자열)은 빌더가 못 옮깁니다
print("\n※ 반대쪽(소스에 새로 생겼는데 뼈대에 없는 것)은 js_extract.py 가 셉니다 —")
print("   지금 번역할 것 908가지 · 뼈대 열쇠와 견주려면 --dump 로 새로 내야 합니다.")

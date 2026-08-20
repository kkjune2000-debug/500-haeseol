# -*- coding: utf-8 -*-
r"""번역 목록에서 **사람이 읽을 글자가 하나도 없는** 것만 골라냅니다 (2026-08-21).

    python js_trans_pure.py [뼈대.py]

앞선 `js_trans_smell.py` 는 생김새로 훑어 139가지를 냈는데, 대부분은 **화면 문장이
마크업을 품은 것**이라 결함이 아니었습니다. 이 도구는 잣대를 좁힙니다 —
태그·속성·CSS 를 걷어낸 뒤 **남는 글자가 없으면** 그것은 기계가 읽는 것입니다.
번역하면 기능이 죽습니다.
"""
import io, os, re, sys, ast, html as H

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "js_사전_뼈대.py")

src = io.open(path, encoding="utf-8", errors="replace").read()
keys = []
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Dict):
        for k in node.keys:
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                keys.append(k.value)
keys = sorted({k for k in keys if k.strip()})


def human(t):
    """태그를 걷어낸 뒤 남는 사람 글자 (한글 또는 두 글자 이상 라틴 낱말)."""
    t = re.sub(r"<[^>]*>", " ", t)
    t = H.unescape(t)
    return re.findall(r"[가-힣]+|[A-Za-z]{2,}", t)


pure, near = [], []
for k in keys:
    words = human(k)
    if not words:
        pure.append(k)
        continue
    # CSS 값처럼 생겼는데 낱말이 단위뿐인 것
    if all(w.lower() in {"px", "em", "rem", "rgba", "rgb", "inset", "solid",
                         "none", "auto", "block", "flex", "true", "false"}
           for w in words):
        near.append(k)

print(f"■ 번역 목록 {len(keys):,}가지 — {os.path.basename(path)}")
print(f"\n── 사람이 읽을 글자가 **하나도 없는 것** : {len(pure)}가지  ★번역하면 죽습니다")
for k in pure:
    print("     " + repr(k)[:100])
print(f"\n── 낱말이 단위·값뿐인 것 : {len(near)}가지  ★같이 보십시오")
for k in near:
    print("     " + repr(k)[:100])
if not pure and not near:
    print("\n■ 없습니다 — 번역 목록에 기계가 읽는 글자는 섞이지 않았습니다.")

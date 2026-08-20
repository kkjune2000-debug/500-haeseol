# -*- coding: utf-8 -*-
r"""번역 목록에 **번역하면 기능이 죽을 글자**가 섞였는지 봅니다 (2026-08-21).

    python js_trans_smell.py [뼈대.py]

왜
    사전은 「그 글자를 만나면 이 말로 바꾸라」입니다. 그 목록에 **기계가 읽는 글자**
    (선택자·id·클래스·음원 열쇠·정답)가 섞이면 번역판에서 기능이 죽습니다.
    2026-08-18 에 14가지를 그렇게 빼냈습니다. 그 뒤로 새로 샌 것이 없는지 봅니다.

    `js_extract.py` 는 자리(문맥)로 가릅니다 — 이 도구는 **글자 생김새**로 다시 봅니다.
    잣대가 둘이면 한쪽이 놓친 것을 다른 쪽이 잡습니다.
"""
import io, os, re, sys, ast

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

SMELL = [
    ("선택자·태그", re.compile(r"(?:^|\s)(?:table|div|span|button|input|td|th)\."
                            r"[a-z][\w-]*|#[a-zA-Z][\w-]{2,}")),
    ("클래스 이름만", re.compile(r"^[a-z][a-z0-9-]{2,}(?:\s+[a-z][a-z0-9-]{2,})*$")),
    ("파일·경로", re.compile(r"\.(?:mp3|png|jpg|html|json)\b|_소리/")),
    ("속성 이름", re.compile(r"\bdata-[a-z-]+\b|\baria-[a-z-]+\b")),
    ("코드 조각", re.compile(r"[();{}]|=>|function\s|querySelector|classList")),
    ("숫자·단위뿐", re.compile(r"^[\d\s.,:%px+-]+$")),
]

hits = []
for k in keys:
    for name, rx in SMELL:
        if rx.search(k):
            hits.append((name, k))
            break

print(f"■ 번역 목록 {len(keys):,}가지 — {os.path.basename(path)}")
print(f"■ 냄새나는 것 {len(hits)}가지\n")
seen = {}
for name, k in hits:
    seen.setdefault(name, []).append(k)
for name, ks in seen.items():
    print(f"── {name} : {len(ks)}가지")
    for k in ks[:8]:
        print("     " + repr(k)[:96])
    if len(ks) > 8:
        print(f"     … 그리고 {len(ks)-8}가지 더")
    print()
print("★ 걸린 것이 다 결함은 아닙니다 — 화면에 보이는 문장이 괄호를 품을 수도 있습니다.")
print("  하나씩 열어 「사람이 읽는 말인가, 기계가 읽는 글자인가」로 가르십시오.")

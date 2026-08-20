# -*- coding: utf-8 -*-
r"""박아 둔 경로(sys.path.insert)를 걷어냅니다 — 2026-08-20 폴더가 바뀌었습니다.

    python _fix_hardpath.py [--apply]

왜 급한가
    작업 폴더가 `D:\한국어 클로드\놀라운 한국어 500 해설집 클로드` 로 바뀌었는데,
    옛 폴더(`D:\OneDrive\놀라운 한국어 500 해설집`)가 **파일 그대로 남아 있습니다.**
    경로를 박은 스크립트는 `import _paths` 를 **옛 폴더에서** 가져오고, `_paths` 는
    제 위치에서 책을 찾으므로 — **새 폴더에서 돌려도 옛 폴더를 고칩니다.**
    오늘 아침 인수인계 사본을 고쳐 하루치를 잃을 뻔한 것과 같은 갈래입니다.
"""
import io, os, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
APPLY = "--apply" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))

OLD = re.compile(r'sys\.path\.insert\(0, r"[A-Za-z]:[^"]*"\)\r?\n?')
NEW = ('sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))'
       '  # ★경로를 박지 않는다 (2026-08-20 폴더 바뀜)\n')

todo = []
for p in sorted(glob.glob(os.path.join(HERE, "*.py"))):
    name = os.path.basename(p)
    if name == os.path.basename(__file__):
        continue
    s = io.open(p, encoding="utf-8", newline="").read()
    if not OLD.search(s):
        continue
    nl = "\r\n" if "\r\n" in s else "\n"
    new = NEW.replace("\n", nl)
    s2 = OLD.sub(new, s, count=1)
    # ★os 를 안 부른 스크립트면 함께 넣어 준다
    if not re.search(r"^\s*import[^\n]*\bos\b", s2, re.M):
        s2 = s2.replace(new, "import os" + nl + new, 1)
    assert "D:\\OneDrive" not in s2 and "sys.path.insert(0, r" not in s2, name
    # ★줄이 하나 늘므로 줄 수는 달라집니다. 봐야 할 것은 **줄끝이 섞이지 않았는가**입니다
    #   (도구 스크립트는 LF 가 64개 · CRLF 가 14개로 갈려 있습니다).
    mixed = lambda t: (t.count("\r\n") > 0) and (t.count("\n") - t.count("\r\n") > 0)
    assert not mixed(s2), f"{name}: 줄끝이 섞였습니다"
    todo.append((p, name, s2))

print(f"■ 경로가 박힌 스크립트 {len(todo)}개")
for _, name, _ in todo:
    print("     " + name)
if APPLY:
    for p, _, s2 in todo:
        io.open(p, "w", encoding="utf-8", newline="").write(s2)
    print("■ 걷어냈습니다 — 이제 제 위치에서 _paths 를 찾습니다")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

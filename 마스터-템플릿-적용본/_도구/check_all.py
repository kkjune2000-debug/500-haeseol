# -*- coding: utf-8 -*-
"""검사 넷을 한 번에 돌린다 — 무엇을 고치든 **반영한 뒤 반드시** 이것부터

쓰기: python check_all.py
"""
import subprocess, sys, os
import _paths

out = _paths.stdout()
HERE = _paths.HERE
for name, title in (("check_structure.py", "① 구조·정답·음원"),
                    ("check_script_order.py", "② 스크립트 선후"),
                    ("check_style.py", "③ 스타일"),
                    ("check_spec.py", "④ 규격")):
    out.write(f"\n{'='*64}\n{title}\n{'='*64}\n")
    out.flush()
    r = subprocess.run([sys.executable, os.path.join(HERE, name)],
                       capture_output=True, cwd=HERE)
    txt = r.stdout.decode("utf-8", "replace")
    if name == "check_spec.py":          # 분포표는 길어서 결론만
        i = txt.find("■ 규격에서 벗어난 파일")
        txt = txt[i:] if i > 0 else txt
    out.write(txt)
    if r.returncode:
        out.write("   ★ 검사기가 오류로 멈췄습니다\n")
        out.write(r.stderr.decode("utf-8", "replace")[-800:] + "\n")
out.write("\n■ 모두 0건이어야 정상입니다.\n")
out.flush()

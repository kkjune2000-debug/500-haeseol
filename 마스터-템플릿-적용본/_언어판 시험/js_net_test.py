# -*- coding: utf-8 -*-
r"""그물 시험 — js_extract.role() 이 물어야 할 것을 물고, 물면 안 되는 것은 놓아 주는가

  ★ 검사기를 고친 뒤에는 반드시 이것을 돌리십시오.
    초록불이 된 것과 그물이 살아 있는 것은 다릅니다.
  ★ 「물면 안 되는 것」(★ 표)이 더 중요합니다 — 지나친 그물은 번역돼야 할 문구를
    잠가 버리고, 그러면 언어판에 한국어·영어가 그대로 남습니다.

사용: python js_net_test.py      (이 폴더 안에서)
"""
import sys, io, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
out = io.TextIOWrapper(open(sys.stdout.fileno(), "wb", closefd=False), encoding="utf-8")
import js_extract as JE

CASES = [
    # (js 조각, 잡을 리터럴, 바라는 노릇 앞머리, 설명)
    ("var a=document.querySelector('td.e');", "td.e", "잠글", "선택자 — 기계가 읽음"),
    ("var a=document.querySelectorAll('table.numt, table.symt');",
     "table.numt, table.symt", "잠글", "선택자 여럿"),
    ("el.classList.add('correct');", "correct", "잠글", "클래스 이름"),
    ("el.setAttribute('data-say','안녕');", "data-say", "잠글", "속성 이름"),
    ("localStorage.setItem('akVoiceSex','f');", "akVoiceSex", "잠글", "저장 열쇠"),
    ("el.addEventListener('click',fn);", "click", "잠글", "사건 이름"),
    ("el.insertAdjacentHTML('beforeend','<b>Correct!</b>');",
     "beforeend", "잠글", "끼울 자리 이름 (첫 인수)"),
    # ── 물면 안 되는 것 (되돌이 검사) ──
    ("el.insertAdjacentHTML('beforeend','<b>Correct!</b>');",
     "<b>Correct!</b>", "번역", "★끼워 넣는 HTML (둘째 인수) — 번역 대상"),
    ("box.innerHTML = 'All matched!';", "All matched!", "번역", "★화면 문구"),
    ("var p={ko:'가다',en:'to go'};", "가다", "잠글", "★배우는 한국어"),
    ("var p={ko:'가다',en:'to go'};", "to go", "번역", "★영어 뜻풀이"),
    ("t.textContent = has ? '받침 O' : '받침 X';", "받침 O", "번역", "★삼항 앞가지"),
    ("t.textContent = has ? '받침 O' : '받침 X';", "받침 X", "번역", "★삼환 뒷가지"),
    ("return '다시 고르세요.';", "다시 고르세요.", "번역", "★return 문구"),
]

ok = bad = 0
for js, lit, want, why in CASES:
    off = js.index("'" + lit + "'")   # literals() 는 여는 따옴표 자리를 넘긴다
    got = JE.role(js, off, lit, [])
    hit = got.startswith(want)
    out.write(f"   {'○' if hit else '✗'}  {why:<34} '{lit[:26]}' → [{got}]\n")
    ok, bad = (ok + 1, bad) if hit else (ok, bad + 1)

out.write(f"\n■ 맞음 {ok} · 틀림 {bad}\n")
if bad:
    out.write("   ★ 그물이 새거나 지나칩니다. 고치십시오.\n")
out.flush()

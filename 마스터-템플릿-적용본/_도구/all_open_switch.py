# -*- coding: utf-8 -*-
r"""저자용 「모두 펼치기」 스위치를 심습니다 (사용자 결정 2026-08-20).

    python all_open_switch.py [--apply]
    python all_open_switch.py --remove [--apply]      # 도로 뺄 때

무엇을
    쪽을 열 때 **학생 화면에는 아무것도 보이지 않습니다.** 다음 둘 중 하나를 하면
    오른쪽 아래에 단추가 나타나고 그 쪽의 모든 것이 펼쳐집니다.
        · 주소 끝에 **#all** 을 붙여 연다        (…/3 142~149 서술어 문법 희망.html#all)
        · 쪽에서 **Alt + A** 를 누른다
    단추를 다시 누르면 모두 접힙니다.

무엇이 열리는가 (사용자 결정: 넷 다)
    정답 `.answer-content` · 해설 `.explain-content` · 어휘 `.vocab-box` ·
    카드 `.flashcard`(뒤집힘)

★ 이 책이 이미 쓰는 방식 그대로 엽니다 — 새 규칙을 만들지 않았습니다.
      정답  inline style.display (단추가 그렇게 합니다)
      해설·어휘  class="shown"    카드  class="flipped"
★ **JS 에 한국어를 새로 박지 않았습니다.** 「모두 펼치기 / 모두 접기」 두 말은 HTML 안
  `translate="yes"` 단추에 두고 CSS 로 갈아 보입니다(다국어 2층에 짐을 더하지 않습니다).
★ 인쇄에서는 숨깁니다(`@media print`).
★ 스크립트는 `</body>` 바로 앞, 제 안에서만 도는 덩이라 다른 함수를 건드리지 않습니다
  (`check_script_order.py` 의 「정의보다 먼저 부르기」에 걸리지 않습니다).
"""
import io, os, re, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BOOK = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "놀라운 한국어 500문장 해설 최종"))
APPLY = "--apply" in sys.argv
REMOVE = "--remove" in sys.argv

MARK = "<!-- 저자용 모두 펼치기 (2026-08-20) — 학생 화면에는 안 보인다 -->"
END = "<!-- /저자용 모두 펼치기 -->"

BLOCK = MARK + """
<style>
#akAll{display:none;position:fixed;right:14px;bottom:14px;z-index:9999;padding:9px 14px;
 border-radius:999px;border:1px solid #c7d2fe;background:#eef2ff;color:#3730a3;
 font-weight:800;font-size:0.85rem;font-family:inherit;cursor:pointer;
 box-shadow:0 2px 8px rgba(55,48,163,0.18);}
#akAll.on{display:block;}
#akAll .ak-c{display:none;}
#akAll.open .ak-o{display:none;}
#akAll.open .ak-c{display:inline;}
@media print{#akAll{display:none !important;}}
</style>
<button id="akAll" translate="yes" title="Alt+A"><span class="ak-o">▼ 모두 펼치기</span><span class="ak-c">▲ 모두 접기</span></button>
<script>
(function(){
  var b=document.getElementById('akAll'), open=false;
  function each(sel,fn){ Array.prototype.forEach.call(document.querySelectorAll(sel),fn); }
  function all(on){
    each('.answer-content',function(e){ e.style.display = on ? 'block' : ''; });
    each('.explain-content',function(e){ e.classList.toggle('shown',on); });
    each('.vocab-toggle + .vocab-box',function(e){ e.classList.toggle('shown',on); });
    each('.flashcard',function(e){ e.classList.toggle('flipped',on); });
    open = on; b.classList.toggle('open',on);
  }
  b.addEventListener('click',function(){ all(!open); });
  document.addEventListener('keydown',function(ev){
    if(ev.altKey && !ev.ctrlKey && (ev.key==='a'||ev.key==='A')){
      ev.preventDefault(); b.classList.add('on'); all(!open);
    }
  });
  if(location.hash==='#all'){ b.classList.add('on'); all(true); }
})();
</script>
""" + END


def strip_old(s):
    return re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\s*", "", s)


hits, added, removed = [], 0, 0
for p in sorted(glob.glob(os.path.join(BOOK, "*.html"))):
    s0 = io.open(p, encoding="utf-8", newline="").read()
    name = os.path.basename(p)
    nl = "\r\n" if "\r\n" in s0 else "\n"
    s = strip_old(s0)
    had = s != s0
    if not REMOVE:
        i = s.rfind("</body>")
        assert i > 0, f"{name}: </body> 를 못 찾았습니다"
        s = s[:i] + BLOCK.replace("\n", nl) + nl + s[i:]
    if s == s0:
        continue
    # ── 검산
    for tg in ("button", "style", "script", "span", "div", "body"):
        x = len(re.findall(rf"<{tg}\b", s)) - len(re.findall(rf"</{tg}\s*>", s))
        y = len(re.findall(rf"<{tg}\b", s0)) - len(re.findall(rf"</{tg}\s*>", s0))
        exp = 0 if (had or REMOVE) else {"button": 0, "style": 0, "script": 0,
                                         "span": 0, "div": 0, "body": 0}[tg]
        assert x == y + exp, f"{name}: <{tg}> 짝이 어긋남 ({x} vs {y})"
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    assert css.count("{") == css.count("}"), f"{name}: CSS 중괄호"
    assert s.count("\n") - s.count("\r\n") == s0.count("\n") - s0.count("\r\n"), \
        f"{name}: 홑 LF"
    assert s.count(MARK) == (0 if REMOVE else 1), f"{name}: 스위치가 겹쳤습니다"
    hits.append((p, s))
    if REMOVE:
        removed += 1
    else:
        added += 1

print(f"■ {'뺄' if REMOVE else '심을'} 파일 {len(hits)}개")
if APPLY:
    for p, s in hits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("■ 반영했습니다 — 주소 끝에 #all 또는 Alt+A")
else:
    print("※ 모의 실행입니다. 반영하려면 --apply")

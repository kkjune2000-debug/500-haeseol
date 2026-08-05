import sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = '시제_문법설명_v1.html'
with open(PATH,'r',encoding='utf-8') as f:
    txt = f.read()

# ---------- 1. Add explanatory note + regular-ㄷ table after the irregular ㄷ table ----------
ADD_NOTE = '''

<div style="margin:14px 0 4px 0;padding:10px 14px;background:#fff8e6;border-left:4px solid #e8c97a;border-radius:6px;">
  <p class="ko" style="margin:0 0 4px 0;font-weight:800;color:#8a6a26;">⚠️ 주의: 모든 'ㄷ' 받침 동사가 불규칙은 아닙니다.</p>
  <p class="ko" style="margin:0 0 2px 0;">아래 동사들은 <strong>규칙형</strong>입니다. 'ㄷ'이 변하지 않고 그대로 '았/었습니다'가 붙습니다.</p>
  <p class="en" style="margin:0;font-style:italic;color:#8a7a26;">Not all ㄷ-ending verbs are irregular — these are regular; 'ㄷ' stays as-is and takes 았/었.</p>
</div>

<div class="conj-ir ir-slate">
  <div class="ci-rule">
    <span class="ci-rule-chip" style="background:#64748b;">규칙 · REGULAR</span>
    <span class="ci-rule-desc">받침 'ㄷ'이 <strong>그대로 유지</strong>되고 '았/었습니다'가 붙습니다
      <span class="en">'ㄷ' batchim stays; just add 았/었습니다</span>
    </span>
  </div>
  <div class="ci-coltitles"><div>기본형 · Base</div><div></div><div>변화 · Change</div><div></div><div>결과 · Result</div></div>
  <div class="ci-row">
    <div class="ci-base"><span class="chip">믿다</span><small>believe · ㅣ</small></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-proc"><span class="chip chip-proc">믿 + 었 → 믿었</span></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-result"><span class="chip chip-decl">믿었습니다</span><span class="chip chip-ques">믿었습니까?</span></div>
  </div>
  <div class="ci-row">
    <div class="ci-base"><span class="chip">받다</span><small>receive · ㅏ</small></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-proc"><span class="chip chip-proc">받 + 았 → 받았</span></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-result"><span class="chip chip-decl">받았습니다</span><span class="chip chip-ques">받았습니까?</span></div>
  </div>
  <div class="ci-row">
    <div class="ci-base"><span class="chip">닫다</span><small>close · ㅏ</small></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-proc"><span class="chip chip-proc">닫 + 았 → 닫았</span></div>
    <div class="ci-arrow">➜</div>
    <div class="ci-result"><span class="chip chip-decl">닫았습니다</span><span class="chip chip-ques">닫았습니까?</span></div>
  </div>
</div>
'''

# Anchor: the closing </div> of the ㄷ irregular conj-ir, which is immediately followed by blank line and <!-- Quiz: 과거형 ㄷ 불규칙 -->.
OLD_ANCHOR = '''    <div class="ci-result"><span class="chip chip-decl">물었습니다</span><span class="chip chip-ques">물었습니까?</span></div>
  </div>
</div>



<!-- Quiz: 과거형 ㄷ 불규칙 -->'''

NEW_ANCHOR = '''    <div class="ci-result"><span class="chip chip-decl">물었습니다</span><span class="chip chip-ques">물었습니까?</span></div>
  </div>
</div>
''' + ADD_NOTE + '''

<!-- Quiz: 과거형 ㄷ 불규칙 -->'''

assert txt.count(OLD_ANCHOR) == 1, txt.count(OLD_ANCHOR)
txt = txt.replace(OLD_ANCHOR, NEW_ANCHOR, 1)

# ---------- 2. Add 3 MC questions (for 믿다, 받다, 닫다) ----------
# Insert before the closing </div> of mcQuizPDI, right after question 5 (깨닫다).
def mcq(n, base_eng_note, correct, opts):
    """Build an mc-q div. opts: list of 4 options"""
    parts = ''.join(
        '<div class="mc-opt-wrap">'
        f'<button class="mc-btn" onclick="mcPDI(this,&#39;{o}&#39;)">{o}</button>'
        '<div class="mc-fb"></div></div>'
        for o in opts
    )
    return (
        f'<div class="mc-q" data-answers="{correct}">'
        f'<div class="mc-sentence">{base_eng_note} →</div>'
        f'<div class="mc-opts">{parts}</div></div>'
    )

new_mc_rows = '\n'.join([
    mcq('6) 믿다 (to believe)', '믿었습니다',
        ['믿었습니다','믿았습니다','밀었습니다','밀었습니다']),
    mcq('7) 받다 (to receive)', '받았습니다',
        ['받았습니다','받었습니다','발았습니다','발었습니다']),
    mcq('8) 닫다 (to close)',  '닫았습니다',
        ['닫았습니다','닫었습니다','달았습니다','달었습니다']),
])
# Fix duplicate option in 믿다 (밀었습니다 appears twice) — replace one with 믿았습니다 variant
# Actually let me rebuild cleanly with unique distractors
new_mc_rows = '\n'.join([
    mcq('6) 믿다 (to believe)', '믿었습니다',
        ['믿었습니다','믿았습니다','밀었습니다','밀렸습니다']),
    mcq('7) 받다 (to receive)', '받았습니다',
        ['받았습니다','받었습니다','발았습니다','바다았습니다']),
    mcq('8) 닫다 (to close)',  '닫았습니다',
        ['닫았습니다','닫었습니다','달았습니다','다닸습니다']),
])

# Insert after the existing mcQuiz block (before the closing </div> that closes mcQuizPDI)
OLD_MC_CLOSE = '''<div class="mc-q" data-answers="깨달았습니다"><div class="mc-sentence">5) 깨닫다 (to realize) →</div><div class="mc-opts"><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨닫았습니다&#39;)">깨닫았습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨닫었습니다&#39;)">깨닫었습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨달았습니다&#39;)">깨달았습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨달었습니다&#39;)">깨달었습니다</button><div class="mc-fb"></div></div></div></div>
</div>'''
NEW_MC_CLOSE = '''<div class="mc-q" data-answers="깨달았습니다"><div class="mc-sentence">5) 깨닫다 (to realize) →</div><div class="mc-opts"><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨닫았습니다&#39;)">깨닫았습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨닫었습니다&#39;)">깨닫었습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨달았습니다&#39;)">깨달았습니다</button><div class="mc-fb"></div></div><div class="mc-opt-wrap"><button class="mc-btn" onclick="mcPDI(this,&#39;깨달었습니다&#39;)">깨달었습니다</button><div class="mc-fb"></div></div></div></div>
''' + new_mc_rows + '''
</div>'''
assert txt.count(OLD_MC_CLOSE) == 1
txt = txt.replace(OLD_MC_CLOSE, NEW_MC_CLOSE, 1)

# Update mcPDIT from 5 to 8
old_total = 'var mcPDIT=5,mcPDID=0,mcPDIC=0;'
new_total = 'var mcPDIT=8,mcPDID=0,mcPDIC=0;'
assert txt.count(old_total) == 1
txt = txt.replace(old_total, new_total, 1)

# ---------- 3. Add to flashcards (fcGridPDI data array) ----------
OLD_FC = '''    ["걷다","walk","걸었습니다","걸었습니까?"],
    ["듣다","listen","들었습니다","들었습니까?"],
    ["묻다","ask","물었습니다","물었습니까?"],
    ["싣다","load","실었습니다","실었습니까?"],
    ["깨닫다","realize","깨달았습니다","깨달았습니까?"]
  ];
  const grid = document.getElementById('fcGridPDI');'''
NEW_FC = '''    ["걷다","walk","걸었습니다","걸었습니까?"],
    ["듣다","listen","들었습니다","들었습니까?"],
    ["묻다","ask","물었습니다","물었습니까?"],
    ["싣다","load","실었습니다","실었습니까?"],
    ["깨닫다","realize","깨달았습니다","깨달았습니까?"],
    ["믿다","believe (regular)","믿었습니다","믿었습니까?"],
    ["받다","receive (regular)","받았습니다","받았습니까?"],
    ["닫다","close (regular)","닫았습니다","닫았습니까?"]
  ];
  const grid = document.getElementById('fcGridPDI');'''
assert txt.count(OLD_FC) == 1
txt = txt.replace(OLD_FC, NEW_FC, 1)

# ---------- 4. Add to typing (pditBody words array) ----------
OLD_TYPING = '''  const words = [
    ["걷다","walk","걸었습니다","걸었습니까?"],
    ["듣다","listen","들었습니다","들었습니까?"],
    ["묻다","ask","물었습니다","물었습니까?"],
    ["싣다","load","실었습니다","실었습니까?"],
    ["깨닫다","realize","깨달았습니다","깨달았습니까?"]
  ];
  const body = document.getElementById('pditBody');'''
NEW_TYPING = '''  const words = [
    ["걷다","walk","걸었습니다","걸었습니까?"],
    ["듣다","listen","들었습니다","들었습니까?"],
    ["묻다","ask","물었습니다","물었습니까?"],
    ["싣다","load","실었습니다","실었습니까?"],
    ["깨닫다","realize","깨달았습니다","깨달았습니까?"],
    ["믿다","believe (regular)","믿었습니다","믿었습니까?"],
    ["받다","receive (regular)","받았습니다","받았습니까?"],
    ["닫다","close (regular)","닫았습니다","닫았습니까?"]
  ];
  const body = document.getElementById('pditBody');'''
assert txt.count(OLD_TYPING) == 1
txt = txt.replace(OLD_TYPING, NEW_TYPING, 1)

# Update pdit score total: 10 → 16 (8 × 2)
old_pdit_total = 'id="pditCorrect">0</span> <span class="pt-total">/ 10</span>'
new_pdit_total = 'id="pditCorrect">0</span> <span class="pt-total">/ 16</span>'
assert txt.count(old_pdit_total) == 1
txt = txt.replace(old_pdit_total, new_pdit_total, 1)

with open(PATH,'w',encoding='utf-8') as f:
    f.write(txt)
print('OK')

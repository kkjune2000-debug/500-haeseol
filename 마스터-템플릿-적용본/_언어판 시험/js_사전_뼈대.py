# -*- coding: utf-8 -*-
"""js_extract.py 가 뽑은 사전 뼈대 — 오른쪽을 채워 tr_xx.py 의 JS 에 붙인다.

★ 열쇠는 소스에 적힌 그대로여야 한다. 태그·빈칸 하나만 달라도 빌더가 못 찾는다.
★ 문구 안의 한국어 문법 표지(ㄹ · ‑습니다 · 은/는)는 번역하지 말고 그대로 두라 —
  본문에서 lang="ko" translate="no" 로 잠그는 것과 같은 자리다.
"""

# ★ 아래 47줄에는 「그대로 두라」 표가 붙어 있습니다 — 문구 안에 배우는
#   한국어(ㅂ니다 · ㄹ 것입니다 · 은 · 이)가 들어 있는 자리입니다.

JS = {
    # ── 공통 틀 36가지 (10파일 이상) — 여기부터 채우면 값이 크다
    # 103파일 · 남성 음성 ·
    "남성 음성 · ": "",
    # 103파일 · 이 브라우저에는 한국어 남성 음성이 없어 목소리를 낮춰 읽습니다. Microsoft Edge 에서 진짜 남성
    "이 브라우저에는 한국어 남성 음성이 없어 목소리를 낮춰 읽습니다. Microsoft Edge 에서 진짜 남성 음성(InJoon)이 나옵니다.": "",
    # 103파일 · 여성 음성 ·
    "여성 음성 · ": "",
    # 101파일 · 남성 음성 · Hyunsu (구워 둔 음원)
    "남성 음성 · Hyunsu (구워 둔 음원)": "",
    # 100파일 · Stop
    "\\u25a0 \\uba48\\ucda4<span class=\"gloss\" lang=\"en\" translate=\"yes\">Stop</span>": "",
    # 72파일 · 정답!
    "</strong> 정답!": "",
    # 72파일 · 영어 선택을 취소했습니다. 다시 고르세요.
    "영어 선택을 취소했습니다. 다시 고르세요.": "",
    # 72파일 · 영어 선택:
    "영어 선택: <strong>": "",
    # 72파일 · → 짝이 되는 한국어 문장을 고르세요.
    "</strong> → 짝이 되는 한국어 문장을 고르세요.": "",
    # 72파일 · 한국어 선택을 취소했습니다. 다시 고르세요.
    "한국어 선택을 취소했습니다. 다시 고르세요.": "",
    # 72파일 · 한국어 선택:
    "한국어 선택: <strong>": "",
    # 72파일 · → 짝이 되는 영어 문장을 고르세요.
    "</strong> → 짝이 되는 영어 문장을 고르세요.": "",
    # 72파일 · 🎉 완료! 모든 문장을 맞췄습니다. All matched!
    "🎉 완료! 모든 문장을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",
    # 72파일 · — 짝이 아닙니다. 다시 고르세요. Not a match.
    "</strong> — 짝이 아닙니다. 다시 고르세요. <span style=\"color:#5a6d87;\">Not a match.</span>": "",
    # 69파일 · 정답!Correct!
    "\\u{1F389} 정답!<small>Correct!</small>": "",
    # 68파일 · Stop
    "\\u25a0 \\uba48\\ucda4<span class=\\\"gloss\\\" lang=\\\"en\\\" translate=\\\"yes\\\">Stop</span>": "",
    # 67파일 · 안 썼습니다
    "<div class=\"wt-diff\"><div class=\"wt-dline\"><b>안 썼습니다</b>": "",
    # 67파일 · Not answered
    "<span class=\"gloss\" lang=\"en\" translate=\"yes\">Not answered</span></div>": "",
    # 67파일 · 정답
    "<div class=\"wt-dline\"><b>정답</b><span>": "",
    # 67파일 · 내가 쓴 것
    "<div class=\"wt-dline\"><b>내가 쓴 것</b><span>": "",
    # 67파일 · ↺ 다시 풀기
    "<button type=\"button\" translate=\"yes\" class=\"wt-rbtn\" onclick=\"wtAgain(this)\">↺ 다시 풀기": "",
    # 67파일 · Try again
    "<span class=\"gloss\" lang=\"en\" translate=\"yes\">Try again</span></button>": "",
    # 67파일 · 조사만 다릅니다
    "<b>조사만 다릅니다</b> ": "",
    # 67파일 · 둘 다 주어를 표시하므로 정답으로 셉니다.
    "<div class=\"wt-nline\">둘 다 주어를 표시하므로 정답으로 셉니다. ": "",
    # 67파일 · 은/는은 이야기의 주제를 잡을 때, 이/가는 새로 알릴 때 씁니다.
    "은/는은 이야기의 주제를 잡을 때, 이/가는 새로 알릴 때 씁니다.</div>": "",
    # 67파일 · Only the particle differs — both mark the subject, so this c
    "Only the particle differs — both mark the subject, so this counts as correct.</span></div>": "",
    # 28파일 · ▼ Tap to check
    "<span class=\"fc-flip-hint\">▼ <span lang=\"en\" translate=\"yes\">Tap to check</span></span>": "",
    # 22파일 · 정답! Correct
    "정답! <small>Correct</small>": "",
    # 20파일 · to
    "<div class=\"fc-english\">to ": "",
    # 17파일 · = to
    " = to ": "",
    # 10파일 · 평서형Statement
    "<span class=\"fc-back-label\">평서형<span class=\"gloss\" lang=\"en\" translate=\"yes\">Statement</span></span>": "",
    # 10파일 · 의문형Question
    "<span class=\"fc-back-label\">의문형<span class=\"gloss\" lang=\"en\" translate=\"yes\">Question</span></span>": "",
    # 10파일 · 현재
    "<div class=\"fcm-grp\"><span class=\"fcm-t\">현재</span>": "",
    # 10파일 · 평서
    "<div class=\"fcm-row\"><span class=\"fcm-l\">평서</span><span class=\"fcm-f\">": "",
    # 10파일 · 의문
    "<div class=\"fcm-row\"><span class=\"fcm-l\">의문</span><span class=\"fcm-f\">": "",
    # 10파일 · 과거
    "<div class=\"fcm-grp\"><span class=\"fcm-t\">과거</span>": "",

    # ── 파일 고유 872가지 — 대부분 그 파일의 영어 문장·뜻풀이
    "run, jump": "",   # 1 시제 1 현재형 A 받침없음.html
    "be small": "",   # 1 시제 1 현재형 A 받침없음.html
    "be few": "",   # 1 시제 1 현재형 A 받침없음.html
    "be late": "",   # 1 시제 1 현재형 A 받침없음.html
    "be same": "",   # 1 시제 1 현재형 A 받침없음.html
    "be good": "",   # 1 시제 1 현재형 A 받침없음.html
    "exist, have": "",   # 1 시제 1 현재형 A 받침없음.html
    "not exist": "",   # 1 시제 1 현재형 A 받침없음.html
    "be many": "",   # 1 시제 1 현재형 A 받침없음.html
    "be cheap": "",   # 1 시제 1 현재형 A 받침없음.html
    "be expensive": "",   # 1 시제 1 현재형 A 받침없음.html
    "have a meal": "",   # 1 시제 1 현재형 A 받침없음.html
    "be clean": "",   # 1 시제 1 현재형 A 받침없음.html
    "be happy": "",   # 1 시제 1 현재형 A 받침없음.html
    "be healthy": "",   # 1 시제 1 현재형 A 받침없음.html
    "do well": "",   # 1 시제 1 현재형 A 받침없음.html
    "be big": "",   # 1 시제 1 현재형 A 받침없음.html
    "be sick": "",   # 1 시제 1 현재형 A 받침없음.html
    "be hungry": "",   # 1 시제 1 현재형 A 받침없음.html
    "be busy": "",   # 1 시제 1 현재형 A 받침없음.html
    "be bad": "",   # 1 시제 1 현재형 A 받침없음.html
    "be pretty": "",   # 1 시제 1 현재형 A 받침없음.html
    "be different": "",   # 1 시제 1 현재형 A 받침없음.html
    "be fast": "",   # 1 시제 1 현재형 A 받침없음.html
    "not know": "",   # 1 시제 1 현재형 A 받침없음.html
    "be hot": "",   # 1 시제 1 현재형 A 받침없음.html
    "be cold": "",   # 1 시제 1 현재형 A 받침없음.html
    "be heavy": "",   # 1 시제 1 현재형 A 받침없음.html
    "be light": "",   # 1 시제 1 현재형 A 받침없음.html
    "be thankful": "",   # 1 시제 1 현재형 A 받침없음.html
    "be glad": "",   # 1 시제 1 현재형 A 받침없음.html
    "be narrow": "",   # 1 시제 1 현재형 A 받침없음.html
    "<b>하다</b> 동사입니다 → \\'‑하다\\'를 <b>\\'‑합니다\\'</b>로 바꿉니다.": "",   # 1 시제 1 현재형 A 받침없음.html
    "A <b>하다</b>-verb → change ‑하다 to <b>‑합니다</b>.": "",   # 1 시제 1 현재형 A 받침없음.html
    "ㄹ 받침": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "어간이 받침 <b>ㄹ</b>로 끝납니다 → <b>ㄹ이 빠지고</b> \\'‑ㅂ니다\\'가 붙습니다.": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "Stem ends in <b>ㄹ</b> → drop ㄹ, then add ‑ㅂ니다.": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "받침 없음": "",   # 1 시제 1 현재형 A 받침없음.html
    "어간에 받침이 <b>없습니다</b> → 어간 + <b>\\'‑ㅂ니다\\'</b>.": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "\\' + ㅂ니다 → <b>": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "No final consonant (받침) → stem + <b>‑ㅂ니다</b>.": "",   # 1 시제 1 현재형 A 받침없음.html  ★한국어 표지 그대로
    "받침 있음": "",   # 1 시제 1 현재형 A 받침없음.html
    "어간에 받침이 <b>있습니다</b> → 어간 + <b>\\'‑습니다\\'</b>.": "",   # 1 시제 1 현재형 A 받침없음.html
    "\\' + 습니다 → <b>": "",   # 1 시제 1 현재형 A 받침없음.html
    "Has a final consonant (받침) → stem + <b>‑습니다</b>.": "",   # 1 시제 1 현재형 A 받침없음.html
    "<td style=\"text-align:center;width:18%;white-space:nowrap;\"><button class=\"ans-btn\" onclick=\"pr80One(this)\">✓ 정답<span class=\"gloss\" lang=\"en\" translate=\"yes\">Answer</span></button><button class=\"pre-btn\" onclick=\"pr80Toggle(this)\">💡 설명<span class=\"gloss\" lang=\"en\" translate=\"yes\">Explanation</span></button></td>": "",   # 1 시제 1 현재형 A 받침없음.html
    "■ 멈춤<span class=\"gloss\" lang=\"en\" translate=\"yes\">Stop</span>": "",   # 1 시제 1 현재형 전체 시험.html
    "<b>하다</b> 동사입니다 → \\'‑하다\\'를 <b>\\'‑했습니다\\'</b>로 바꿉니다.": "",   # 1 시제 2 과거형 A 규칙.html
    "A <b>하다</b>-verb → ‑하다 becomes <b>‑했습니다</b>.": "",   # 1 시제 2 과거형 A 규칙.html
    "ㅡ 불규칙": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "어간 끝 <b>ㅡ</b>가 <b>탈락</b>하고 았/었이 붙습니다.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "Stem-final <b>ㅡ</b> drops, then 았/었 attaches.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "ㅂ 불규칙": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "받침 <b>ㅂ</b>이 <b>\\'우\\'</b>로 바뀌고 \\'었습니다\\'가 붙습니다.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "<b>ㅂ</b> changes to 우, then ‑었습니다.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "밝은 모음 · 받침 O": "",   # 1 시제 2 과거형 A 규칙.html
    "어간 끝 모음이 <b>밝은 모음(ㅏ·ㅗ)</b> + 받침 <b>있음</b> → 어간 + <b>\\'았습니다\\'</b>.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "\\' + 았습니다 → <b>": "",   # 1 시제 2 과거형 A 규칙.html
    "Bright vowel (ㅏ/ㅗ) + 받침 → stem + <b>았습니다</b>.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "어두운 모음 · 받침 O": "",   # 1 시제 2 과거형 A 규칙.html
    "어간 끝 모음이 <b>어두운 모음</b> + 받침 <b>있음</b> → 어간 + <b>\\'었습니다\\'</b>.": "",   # 1 시제 2 과거형 A 규칙.html
    "\\' + 었습니다 → <b>": "",   # 1 시제 2 과거형 A 규칙.html
    "Dark vowel + 받침 → stem + <b>었습니다</b>.": "",   # 1 시제 2 과거형 A 규칙.html
    "밝은 모음 · 받침 X": "",   # 1 시제 2 과거형 A 규칙.html
    "어간 끝 모음이 <b>밝은 모음(ㅏ·ㅗ)</b> + 받침 <b>없음</b> → \\'았\\'과 합쳐져 <b>줄어듭니다</b>.": "",   # 1 시제 2 과거형 A 규칙.html  ★한국어 표지 그대로
    "\\' + 았 → <b>": "",   # 1 시제 2 과거형 A 규칙.html
    "Bright vowel, no 받침 → contracts with 았.": "",   # 1 시제 2 과거형 A 규칙.html
    "어두운 모음 · 받침 X": "",   # 1 시제 2 과거형 A 규칙.html
    "어간 끝 모음이 <b>어두운 모음</b> + 받침 <b>없음</b> → \\'었\\'과 합쳐집니다.": "",   # 1 시제 2 과거형 A 규칙.html
    "\\' + 었 → <b>": "",   # 1 시제 2 과거형 A 규칙.html
    "Dark vowel, no 받침 → contracts with 었.": "",   # 1 시제 2 과거형 A 규칙.html
    ")\">💡 설명<span class=\"gloss\" lang=\"en\" translate=\"yes\">Explanation</span></button></td>": "",   # 1 시제 2 과거형 A 규칙.html
    "<span class=\"pr-cat\">줄임<span class=\"gloss\" lang=\"en\" translate=\"yes\">contraction</span></span>어간이 <b>모음</b>으로 끝나서 \\'았/었\\'과 <b>합쳐져 줄어듭니다</b>.<span class=\"pr-d\">": "",   # 1 시제 2 과거형 B 줄임.html
    "</b></span><br><small class=\"pr-en\">Stem ends in a vowel → 았/었 merges (contraction). &nbsp;<span class=\"pr-en-w\">": "",   # 1 시제 2 과거형 B 줄임.html
    "</td><td style=\"text-align:center;width:18%;white-space:nowrap;\"><button class=\"ans-btn\" onclick=\"pr80One(this)\">✓ 정답<span class=\"gloss\" lang=\"en\" translate=\"yes\">Answer</span></button><button class=\"pre-btn\" onclick=\"pr80Toggle(this)\">💡 설명<span class=\"gloss\" lang=\"en\" translate=\"yes\">Explanation</span></button></td></tr><tr class=\"pre-row\" style=\"display:none;\"><td colspan=\"5\"><div class=\"pre\">": "",   # 1 시제 2 과거형 B 줄임.html
    "<span class=\"pr-cat\">하다<span class=\"gloss\" lang=\"en\" translate=\"yes\"><span lang=\"ko\" translate=\"no\">하다</span>-verb</span></span>\\'하다\\'로 끝나는 단어는 언제나 <b>\\'했습니다\\'</b>로 바뀝니다.<span class=\"pr-d\">": "",   # 1 시제 2 과거형 C 하다.html
    "</b></span><br><small class=\"pr-en\">~하다 verbs always become 했습니다. &nbsp;<span class=\"pr-en-w\">": "",   # 1 시제 2 과거형 C 하다.html
    "Stem-final <b>ㅡ</b> drops, then 았/었.": "",   # 1 시제 2 과거형 D ㅡ불규칙.html  ★한국어 표지 그대로
    "르 불규칙": "",   # 1 시제 2 과거형 E 르불규칙.html
    "<b>르</b>의 <b>ㅡ</b>가 빠지고 <b>ㄹ</b>이 둘로 나뉩니다. 하나는 앞 글자의 <b>받침</b>, 하나는 <b>랐/렀</b>의 첫소리가 됩니다.": "",   # 1 시제 2 과거형 E 르불규칙.html  ★한국어 표지 그대로
    "The <b>ㅡ</b> drops and <b>ㄹ</b> doubles — one becomes the final consonant of the syllable before, the other starts <b>랐/렀</b>.": "",   # 1 시제 2 과거형 E 르불규칙.html  ★한국어 표지 그대로
    "believe (regular)": "",   # 1 시제 2 과거형 F ㄷ불규칙.html
    "close (regular)": "",   # 1 시제 2 과거형 F ㄷ불규칙.html
    "ㄷ 불규칙": "",   # 1 시제 2 과거형 F ㄷ불규칙.html  ★한국어 표지 그대로
    "받침 <b>ㄷ</b>이 <b>ㄹ</b>로 바뀐 뒤 모음에 따라 았/었습니다가 붙습니다(ㅏ·ㅗ→았).": "",   # 1 시제 2 과거형 F ㄷ불규칙.html  ★한국어 표지 그대로
    "<b>ㄷ</b> changes to ㄹ, then 았/었.": "",   # 1 시제 2 과거형 F ㄷ불규칙.html  ★한국어 표지 그대로
    "help (exception)": "",   # 1 시제 2 과거형 G ㅂ불규칙.html
    "narrow (regular)": "",   # 1 시제 2 과거형 G ㅂ불규칙.html
    "wear (regular)": "",   # 1 시제 2 과거형 G ㅂ불규칙.html
    "받침 <b>ㅂ</b>이 <b>우</b>(돕다·곱다는 오)로 바뀝니다. 우 뒤에는 \\'었\\'(→웠), 오 뒤에는 \\'았\\'(→왔)이 붙습니다.": "",   # 1 시제 2 과거형 G ㅂ불규칙.html  ★한국어 표지 그대로
    "<b>ㅂ</b> → 우 (돕/곱 → 오); 우 takes 었 (→웠), 오 takes 았 (→왔).": "",   # 1 시제 2 과거형 G ㅂ불규칙.html  ★한국어 표지 그대로
    "ㅅ 불규칙": "",   # 1 시제 2 과거형 H ㅅ불규칙.html  ★한국어 표지 그대로
    "받침 <b>ㅅ</b>이 모음 앞에서 <b>탈락</b>하고 았/었이 붙습니다.": "",   # 1 시제 2 과거형 H ㅅ불규칙.html  ★한국어 표지 그대로
    "<b>ㅅ</b> drops before a vowel, then 았/었.": "",   # 1 시제 2 과거형 H ㅅ불규칙.html  ★한국어 표지 그대로
    "<span class=\"wqg-all\"><button translate=\"yes\" class=\"wqg-allbtn\" onclick=\"alltSeq(this,\\'f\\')\">🔊 여성<span class=\"gloss\" lang=\"en\" translate=\"yes\">Female</span></button><button translate=\"yes\" class=\"wqg-allbtn\" onclick=\"alltSeq(this,\\'m\\')\">🔊 남성<span class=\"gloss\" lang=\"en\" translate=\"yes\">Male</span></button></span></div>": "",   # 1 시제 2 과거형 전체 시험.html
    "<b>하다</b> 동사입니다 → \\'‑하다\\'를 <b>\\'‑할 것입니다\\'</b>로 바꿉니다.": "",   # 1 시제 3 미래형 A 받침없음.html
    "A <b>하다</b>-verb → ‑하다 becomes <b>‑할 것입니다</b>.": "",   # 1 시제 3 미래형 A 받침없음.html
    "어간이 받침 <b>ㄹ</b>로 끝납니다 → <b>그대로</b> \\'것입니다\\'를 붙입니다.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "Stem ends in <b>ㄹ</b> → keep it, then add 것입니다.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "받침 <b>ㅂ</b>이 <b>\\'우\\'</b>로 바뀌고 \\'ㄹ 것입니다\\'가 붙습니다.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "<b>ㅂ</b> changes to 우, then ‑ㄹ 것입니다.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "어간에 받침이 <b>없습니다</b> → 어간 + <b>\\'ㄹ 것입니다\\'</b>.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "\\' + ㄹ 것입니다 → <b>": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "No final consonant (받침) → stem + <b>ㄹ 것입니다</b>.": "",   # 1 시제 3 미래형 A 받침없음.html  ★한국어 표지 그대로
    "어간에 받침이 <b>있습니다</b> → 어간 + <b>\\'을 것입니다\\'</b>.": "",   # 1 시제 3 미래형 A 받침없음.html
    "\\' + 을 것입니다 → <b>": "",   # 1 시제 3 미래형 A 받침없음.html
    "Has a final consonant (받침) → stem + <b>을 것입니다</b>.": "",   # 1 시제 3 미래형 A 받침없음.html
    "<b>\\'하다\\'</b>로 끝나는 단어입니다 → \\'‑하다\\'를 <b>\\'‑할 것입니다\\'</b>로 바꿉니다.": "",   # 1 시제 3 미래형 B 하다.html
    "A word ending in <b>하다</b> → ‑하다 becomes <b>‑할 것입니다</b>.": "",   # 1 시제 3 미래형 B 하다.html
    "받침 <b>ㄷ</b>이 모음 앞에서 <b>ㄹ</b>로 바뀌고 \\'을 것입니다\\'가 붙습니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "<b>ㄷ</b> → ㄹ before a vowel, then ‑을 것입니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "받침 <b>ㅂ</b>이 <b>우</b>로 바뀌고 \\'을\\'과 합쳐 <b>울</b>이 됩니다 → ~울 것입니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "<b>ㅂ</b> → 우, merges with 을 → 울 것입니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "받침 <b>ㅅ</b>이 모음 앞에서 <b>탈락</b>하고 \\'을 것입니다\\'가 붙습니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "<b>ㅅ</b> drops before a vowel, then ‑을 것입니다.": "",   # 1 시제 3 미래형 불규칙.html  ★한국어 표지 그대로
    "<button translate=\"yes\" class=\"fc-tts-all\" onclick=\"event.stopPropagation();fcSeq(this,&#39;f&#39;)\">🔊 여성<span class=\"gloss\" lang=\"en\" translate=\"yes\">Female</span></button>": "",   # 1 시제 종합 시험.html
    "<button translate=\"yes\" class=\"fc-tts-all\" onclick=\"event.stopPropagation();fcSeq(this,&#39;m&#39;)\">🔊 남성<span class=\"gloss\" lang=\"en\" translate=\"yes\">Male</span></button>": "",   # 1 시제 종합 시험.html
    "<div class=\"fcm-grp\"><span class=\"fcm-t\">미래</span>": "",   # 1 시제 종합 시험.html
    "받침 O": "",   # 2 조사 A 은는 이가.html
    "받침 X": "",   # 2 조사 A 은는 이가.html
    "받침이 <b>있습니다</b> → '<b>은</b>' · '<b>이</b>'를 붙입니다.": "",   # 2 조사 A 은는 이가.html
    "받침이 <b>없습니다</b> → '<b>는</b>' · '<b>가</b>'를 붙입니다.": "",   # 2 조사 A 은는 이가.html
    "Has a final consonant (받침) → add <b>은</b> / <b>이</b>.": "",   # 2 조사 A 은는 이가.html
    "No final consonant (받침) → add <b>는</b> / <b>가</b>.": "",   # 2 조사 A 은는 이가.html
    "</td><td style=\"text-align:center;white-space:nowrap;\"><button class=\"ans-btn\" onclick=\"prJOne(this)\">✓ 정답<span class=\"gloss\" lang=\"en\" translate=\"yes\">Answer</span></button><button class=\"pre-btn\" onclick=\"prJToggle(this)\">💡 설명<span class=\"gloss\" lang=\"en\" translate=\"yes\">Explanation</span></button></td></tr><tr class=\"pre-row\" style=\"display:none;\"><td colspan=\"5\"><div class=\"pre\">": "",   # 2 조사 A 은는 이가.html
    "받침 O → 은 · 이": "",   # 2 조사 A 은는 이가.html  ★한국어 표지 그대로
    "받침 X → 는 · 가": "",   # 2 조사 A 은는 이가.html  ★한국어 표지 그대로
    "<span class=\"fc-back-label\">은/는</span>": "",   # 2 조사 A 은는 이가.html
    "<span class=\"fc-back-label\">이/가<span class=\"gloss\" lang=\"en\" translate=\"yes\">Subject</span></span>": "",   # 2 조사 A 은는 이가.html
    "받침이 <b>있습니다</b> → '<b>을</b>'을 붙입니다.": "",   # 2 조사 B 을를.html
    "받침이 <b>없습니다</b> → '<b>를</b>'을 붙입니다.": "",   # 2 조사 B 을를.html
    "Has a final consonant (받침) → add <b>을</b>.": "",   # 2 조사 B 을를.html
    "No final consonant (받침) → add <b>를</b>.": "",   # 2 조사 B 을를.html
    "</td><td style=\"text-align:center;white-space:nowrap;\"><button class=\"ans-btn\" onclick=\"prJOne(this)\">✓ 정답<span class=\"gloss\" lang=\"en\" translate=\"yes\">Answer</span></button><button class=\"pre-btn\" onclick=\"prJToggle(this)\">💡 설명<span class=\"gloss\" lang=\"en\" translate=\"yes\">Explanation</span></button></td></tr><tr class=\"pre-row\" style=\"display:none;\"><td colspan=\"4\"><div class=\"pre\">": "",   # 2 조사 B 을를.html
    "받침 O → 을": "",   # 2 조사 B 을를.html  ★한국어 표지 그대로
    "받침 X → 를": "",   # 2 조사 B 을를.html  ★한국어 표지 그대로
    "flower pot": "",   # 2 조사 C 에게 에.html
    "입니다 (사람·동물) → '<b>에게</b>'를 붙입니다.": "",   # 2 조사 C 에게 에.html
    "입니다 (사람·동물이 아님) → '<b>에</b>'를 붙입니다.": "",   # 2 조사 C 에게 에.html
    "A person/animal → add <b>에게</b>.": "",   # 2 조사 C 에게 에.html
    "Not a person or animal → add <b>에</b>.": "",   # 2 조사 C 에게 에.html
    "받침이 <b>있습니다</b> → '<b>과</b>'를 붙입니다.": "",   # 2 조사 D 와과.html
    "받침이 <b>없습니다</b> → '<b>와</b>'를 붙입니다.": "",   # 2 조사 D 와과.html
    "Has a final consonant (받침) → add <b>과</b>.": "",   # 2 조사 D 와과.html
    "No final consonant (받침) → add <b>와</b>.": "",   # 2 조사 D 와과.html
    "받침 O → 과": "",   # 2 조사 D 와과.html  ★한국어 표지 그대로
    "받침 X → 와": "",   # 2 조사 D 와과.html  ★한국어 표지 그대로
    "받침이 <b>있습니다</b> → '<b>이나</b>'를 붙입니다.": "",   # 2 조사 E 나 이나.html
    "받침이 <b>없습니다</b> → '<b>나</b>'를 붙입니다.": "",   # 2 조사 E 나 이나.html
    "Has a final consonant (받침) → add <b>이나</b>.": "",   # 2 조사 E 나 이나.html
    "No final consonant (받침) → add <b>나</b>.": "",   # 2 조사 E 나 이나.html
    "받침 O → 이나": "",   # 2 조사 E 나 이나.html  ★한국어 표지 그대로
    "받침 X → 나": "",   # 2 조사 E 나 이나.html  ★한국어 표지 그대로
    "1 o'clock": "",   # 2 조사 F 에 시간.html
    "3 o'clock": "",   # 2 조사 F 에 시간.html
    "next year": "",   # 2 조사 F 에 시간.html
    "시간 단어입니다 → 받침과 관계없이 <b>'에'</b>를 붙입니다.": "",   # 2 조사 F 에 시간.html
    "A time word → always add <b>에</b>.": "",   # 2 조사 F 에 시간.html
    "<span class=\"pr-cat pr-cat-p\">시간</span>": "",   # 2 조사 F 에 시간.html
    "<span class=\"pb-badge pb-p\">시간 + 에</span>": "",   # 2 조사 F 에 시간.html
    "coffee shop": "",   # 2 조사 G 에서 장소.html
    "<span class=\"pb-badge pb-p\">장소 + 에서</span>": "",   # 2 조사 G 에서 장소.html
    "은/는": "",   # 2 조사 전체 시험.html
    "이/가": "",   # 2 조사 전체 시험.html
    "을/를": "",   # 2 조사 전체 시험.html
    "와/과": "",   # 2 조사 전체 시험.html
    "나/이나": "",   # 2 조사 전체 시험.html
    "은/는 · Topic": "",   # 2 조사 전체 시험.html
    "이/가 · Subject": "",   # 2 조사 전체 시험.html
    "을/를 · Object": "",   # 2 조사 전체 시험.html
    "와/과 · And": "",   # 2 조사 전체 시험.html
    "나/이나 · Or": "",   # 2 조사 전체 시험.html
    "선택: <strong>": "",   # 3 001~010 문장구조 주어 형용사.html
    "</strong> → 반대말을 고르세요. <span style=\"color:#5a6d87;\">Pick its antonym.</span>": "",   # 3 001~010 문장구조 주어 형용사.html
    "선택을 취소했습니다. 다시 고르세요.": "",   # 3 001~010 문장구조 주어 형용사.html
    "🎉 완료! 모든 반대말을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 001~010 문장구조 주어 형용사.html
    "</strong>의 반대말이 아닙니다. 다시 고르세요. <span style=\"color:#5a6d87;\">Not its antonym.</span>": "",   # 3 001~010 문장구조 주어 형용사.html
    "반대말이 되는 두 형용사를 차례로 클릭하세요.": "",   # 3 001~010 문장구조 주어 형용사.html
    "I am happy.": "",   # 3 001~010 문장구조 주어 형용사.html
    "She is kind.": "",   # 3 001~010 문장구조 주어 형용사.html
    "Sumi is busy.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The weather is nice.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The mountain is high.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The room is small.": "",   # 3 001~010 문장구조 주어 형용사.html
    "There are a lot of people.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The bag is heavy.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The train is fast.": "",   # 3 001~010 문장구조 주어 형용사.html
    "The movie is fun.": "",   # 3 001~010 문장구조 주어 형용사.html
    "He slept.": "",   # 3 011~020 문장구조 주어 동사.html
    "He got up.": "",   # 3 011~020 문장구조 주어 동사.html
    "He walked.": "",   # 3 011~020 문장구조 주어 동사.html
    "He ran.": "",   # 3 011~020 문장구조 주어 동사.html
    "He worked.": "",   # 3 011~020 문장구조 주어 동사.html
    "He rested.": "",   # 3 011~020 문장구조 주어 동사.html
    "He thought.": "",   # 3 011~020 문장구조 주어 동사.html
    "He spoke.": "",   # 3 011~020 문장구조 주어 동사.html
    "He listened.": "",   # 3 011~020 문장구조 주어 동사.html
    "He went.": "",   # 3 011~020 문장구조 주어 동사.html
    "I eat breakfast.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I exercise.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I draw a picture.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I listen to music.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I watch a movie.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I wear clothes.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I clean.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I read a book.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I learn Korean.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I meet a friend.": "",   # 3 021~030 문장구조 주어 목적어 동사.html
    "I bought.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I bought a gift.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I bought a gift at the department store.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I bought a gift at the department store yesterday.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I met.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I met a friend.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I met a friend at the café.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I met a friend at the café last weekend.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "We saw a movie last weekend.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "We watched a movie at the theater last weekend.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "the day after tomorrow": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "the day before yesterday": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "every day": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "when (interrogative)": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "영어 선택을 취소했습니다.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "</strong> → 짝이 되는 한국어를 고르세요.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "한국어 선택을 취소했습니다.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "</strong> → 짝이 되는 영어를 고르세요.": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "🎉 완료! 모든 시간 명사를 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 031~040 문장구조 시간 장소 목적어 동사.ht
    "I gave.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I gave a gift.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I gave her a gift.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I gave the cat a fish.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I gave water to the flowers.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I made a call.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I called my friend.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I called home.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I called the office.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "I called the office from home.": "",   # 3 041~050 문장구조 간접목적어 직접목적어.htm
    "Who is Sumi?": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "I am Sumi.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "Who did you meet yesterday?": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "I met Kyoungjin yesterday.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "Who is that person?": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "That person is my boyfriend.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "When do you go to the language institute?": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "I go to the language institute on Monday.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "When is your birthday?": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "My birthday is January 1st.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "숫자 선택을 취소했습니다.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "숫자 선택: <strong>": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "</strong> → 짝이 되는 한자어를 고르세요.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "한자어 선택을 취소했습니다.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "한자어 선택: <strong>": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "</strong> → 짝이 되는 숫자를 고르세요.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "🎉 완료! 모든 숫자를 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "Pick the Korean word that matches the digit. · 숫자에 맞는 한국어를 선택하세요.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "</strong> → 짝이 되는 고유어를 고르세요.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "고유어 선택을 취소했습니다.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "고유어 선택: <strong>": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "🎉 완료! 모든 고유어 숫자를 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "Pick the Native Korean word that matches the digit. · 숫자에 맞는 고유어를 선택하세요.": "",   # 3 051~060 문장구조 의문사 누구 언제.html
    "Where did you go yesterday?": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "I went to Seoul yesterday.": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "Where do you study Korean?": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "I study Korean at the language institute.": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "Where is that place?": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "That place is a market.": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "What is this?": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "This is a traditional Korean fan (Buchae).": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "What do you like?": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "I like K-pop.": "",   # 3 061~070 문장구조 의문사 어디 무엇.html
    "What kind of food do you like?": "",   # 3 071~078 문장구조 의문사 어떤.html
    "I like bulgogi.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "What kind of music do you like?": "",   # 3 071~078 문장구조 의문사 어떤.html
    "What color do you like?": "",   # 3 071~078 문장구조 의문사 어떤.html
    "I like blue.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "What kind of men do you like?": "",   # 3 071~078 문장구조 의문사 어떤.html
    "I like a kind man.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "inset 0 0 0 1px #e2e8f0": "",   # 3 071~078 문장구조 의문사 어떤.html
    "색 선택을 취소했습니다.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "색 선택됨 → 한국어 이름을 고르세요. <span style=\"color:#5a6d87;\">Pick its Korean name.</span>": "",   # 3 071~078 문장구조 의문사 어떤.html
    "</strong> → 짝이 되는 색을 고르세요.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "🎉 완료! 모든 색을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 071~078 문장구조 의문사 어떤.html
    "Pick the Korean color name that matches the swatch. · 색에 맞는 한국어 이름을 선택하세요.": "",   # 3 071~078 문장구조 의문사 어떤.html
    "I go to the Korean language school on Monday and Wednesday.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "I bought fruits, vegetables, and fish at the market yesterday.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "I eat bread or rice in the morning.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "I watch movies or dramas at home on weekends.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "She is pretty and smart.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "Today it is cold, the wind is blowing, and it is raining.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "I meet friends or exercise on weekends.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "Kimchi is spicy but delicious.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "</strong> → 짝이 되는 한국어 형용사를 고르세요.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "</strong> → 짝이 되는 영어 표현을 고르세요.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "🎉 완료! 모든 맛 표현을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "왼쪽 영어 표현 하나와 오른쪽 한국어 표현 하나를 선택하세요.": "",   # 3 079~086 문장구조 접속 과와 이나나.html
    "I am Kim Kyoungjin.": "",   # 3 087~096 서술어 문법 이다.html
    "I am a university student.": "",   # 3 087~096 서술어 문법 이다.html
    "My major is computer science.": "",   # 3 087~096 서술어 문법 이다.html
    "My hometown is Seoul.": "",   # 3 087~096 서술어 문법 이다.html
    "My hobby is traveling.": "",   # 3 087~096 서술어 문법 이다.html
    "Today is Saturday.": "",   # 3 087~096 서술어 문법 이다.html
    "Tomorrow is Sunday.": "",   # 3 087~096 서술어 문법 이다.html
    "This is my laptop.": "",   # 3 087~096 서술어 문법 이다.html
    "Here is Seoul Station.": "",   # 3 087~096 서술어 문법 이다.html
    "That is Namsan Mountain.": "",   # 3 087~096 서술어 문법 이다.html
    "Korean Education": "",   # 3 087~096 서술어 문법 이다.html
    "English Education": "",   # 3 087~096 서술어 문법 이다.html
    "Fine Arts": "",   # 3 087~096 서술어 문법 이다.html
    "Chemical Engineering": "",   # 3 087~096 서술어 문법 이다.html
    "Business Administration": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 한국어 전공을 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 영어 전공을 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "🎉 완료! 모든 전공을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 087~096 서술어 문법 이다.html
    "왼쪽 영어 전공 하나와 오른쪽 한국어 전공 하나를 선택하세요.": "",   # 3 087~096 서술어 문법 이다.html
    "watching movies": "",   # 3 087~096 서술어 문법 이다.html
    "listening to music": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 한국어 취미를 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 영어 취미를 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "🎉 완료! 모든 취미를 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 087~096 서술어 문법 이다.html
    "왼쪽 영어 취미 하나와 오른쪽 한국어 취미 하나를 선택하세요.": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 한국어 요일을 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "</strong> → 짝이 되는 영어 요일을 고르세요.": "",   # 3 087~096 서술어 문법 이다.html
    "🎉 완료! 모든 요일을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 087~096 서술어 문법 이다.html
    "왼쪽 영어 요일 하나와 오른쪽 한국어 요일 하나를 선택하세요.": "",   # 3 087~096 서술어 문법 이다.html
    "I am going to school.": "",   # 3 097~104 서술어 문법 현재진행.html
    "I am waiting for my friend at the coffee shop.": "",   # 3 097~104 서술어 문법 현재진행.html
    "I am listening to music.": "",   # 3 097~104 서술어 문법 현재진행.html
    "Snow is falling from the sky.": "",   # 3 097~104 서술어 문법 현재진행.html
    "I am learning Korean these days.": "",   # 3 097~104 서술어 문법 현재진행.html
    "She lives in Seoul.": "",   # 3 097~104 서술어 문법 현재진행.html
    "The boss is in a meeting now.": "",   # 3 097~104 서술어 문법 현재진행.html
    "The manager is on a business trip now.": "",   # 3 097~104 서술어 문법 현재진행.html
    "Can you speak Korean?": "",   # 3 105~114 서술어 문법 능력 가능.html
    "Yes, I can speak Korean.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "No, I can\\'t speak Korean.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "Do you know how to speak Korean?": "",   # 3 105~114 서술어 문법 능력 가능.html
    "Yes, I know how to speak Korean.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "No, I don\\'t know how to speak Korean.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "I can swim.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "I know how to swim.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "I don\\'t know how to swim.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "I can go to Seoul tomorrow.": "",   # 3 105~114 서술어 문법 능력 가능.html
    "Shall we watch a movie this weekend?": "",   # 3 115~122 서술어 문법 청유.html
    "Let\\'s watch a movie this weekend.": "",   # 3 115~122 서술어 문법 청유.html
    "Where shall we meet tomorrow?": "",   # 3 115~122 서술어 문법 청유.html
    "Let\\'s meet at a coffee shop.": "",   # 3 115~122 서술어 문법 청유.html
    "What shall we eat?": "",   # 3 115~122 서술어 문법 청유.html
    "Let\\'s eat bulgogi.": "",   # 3 115~122 서술어 문법 청유.html
    "Shall we leave now?": "",   # 3 115~122 서술어 문법 청유.html
    "Let\\'s leave now.": "",   # 3 115~122 서술어 문법 청유.html
    "I don\\'t eat breakfast.": "",   # 3 123~141 서술어 문법 부정.html
    "I can\\'t eat breakfast.": "",   # 3 123~141 서술어 문법 부정.html
    "He plays the piano.": "",   # 3 123~141 서술어 문법 부정.html
    "He doesn\\'t play the piano.": "",   # 3 123~141 서술어 문법 부정.html
    "He can\\'t play the piano.": "",   # 3 123~141 서술어 문법 부정.html
    "I love him.": "",   # 3 123~141 서술어 문법 부정.html
    "I don\\'t love him.": "",   # 3 123~141 서술어 문법 부정.html
    "I can\\'t love him.": "",   # 3 123~141 서술어 문법 부정.html
    "He is my friend.": "",   # 3 123~141 서술어 문법 부정.html
    "He is not my friend.": "",   # 3 123~141 서술어 문법 부정.html
    "He is healthy.": "",   # 3 123~141 서술어 문법 부정.html
    "He is not healthy.": "",   # 3 123~141 서술어 문법 부정.html
    "Please go to the mountain tomorrow.": "",   # 3 123~141 서술어 문법 부정.html
    "Don\\'t go to the mountain tomorrow.": "",   # 3 123~141 서술어 문법 부정.html
    "Shall we go to the mountain tomorrow?": "",   # 3 123~141 서술어 문법 부정.html
    "Shall we not go to the mountain tomorrow?": "",   # 3 123~141 서술어 문법 부정.html
    "Let\\'s go to the mountain tomorrow.": "",   # 3 123~141 서술어 문법 부정.html
    "Let\\'s not go to the mountain tomorrow.": "",   # 3 123~141 서술어 문법 부정.html
    "🎉 정답!<small>Correct!</small>": "",   # 3 142~149 서술어 문법 희망.html
    "Where do you want to go?": "",   # 3 142~149 서술어 문법 희망.html
    "I want to go to Korea.": "",   # 3 142~149 서술어 문법 희망.html
    "When do you want to go?": "",   # 3 142~149 서술어 문법 희망.html
    "I want to go next fall.": "",   # 3 142~149 서술어 문법 희망.html
    "What do you want to eat?": "",   # 3 142~149 서술어 문법 희망.html
    "I want to eat kimchi.": "",   # 3 142~149 서술어 문법 희망.html
    "Who do you want to meet?": "",   # 3 142~149 서술어 문법 희망.html
    "I want to meet BTS.": "",   # 3 142~149 서술어 문법 희망.html
    "I wish I had a car.": "",   # 3 150~156 서술어 문법 소망.html
    "I wish I had a lot of money.": "",   # 3 150~156 서술어 문법 소망.html
    "I wish I had no worries.": "",   # 3 150~156 서술어 문법 소망.html
    "I hope my parents are healthy.": "",   # 3 150~156 서술어 문법 소망.html
    "I wish I could speak Korean well.": "",   # 3 150~156 서술어 문법 소망.html
    "I hope it doesn\\'t rain tomorrow.": "",   # 3 150~156 서술어 문법 소망.html
    "I hope our team wins.": "",   # 3 150~156 서술어 문법 소망.html
    "I\\'m going to go to Korea next year.": "",   # 3 157~163 서술어 문법 계획.html
    "I\\'m going to meet my friend this weekend.": "",   # 3 157~163 서술어 문법 계획.html
    "I\\'m going to watch a movie this Sunday.": "",   # 3 157~163 서술어 문법 계획.html
    "I\\'m going to buy a car next month.": "",   # 3 157~163 서술어 문법 계획.html
    "I\\'m going to go to the library this afternoon.": "",   # 3 157~163 서술어 문법 계획.html
    "It\\'s about to rain now.": "",   # 3 157~163 서술어 문법 계획.html
    "The train is about to depart now.": "",   # 3 157~163 서술어 문법 계획.html
    "I have decided to study abroad next year.": "",   # 3 164~168 서술어 문법 결정.html
    "I have decided to lose weight this year.": "",   # 3 164~168 서술어 문법 결정.html
    "I have decided to quit smoking.": "",   # 3 164~168 서술어 문법 결정.html
    "We decided to meet again tomorrow.": "",   # 3 164~168 서술어 문법 결정.html
    "We decided to get married next spring.": "",   # 3 164~168 서술어 문법 결정.html
    "May I take a picture?": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "Yes, you may take a picture.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "No, you must not take a picture.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "Don\\'t take a picture.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You must take a picture.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You don\\'t have to take a picture.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "May I sit here?": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You may sit here.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You must not sit here.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "Don\\'t sit here.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You must sit here.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "You don\\'t have to sit here.": "",   # 3 169~180 서술어 문법 허락 금지 의무 면제.h
    "Please help me.": "",   # 3 181~189 서술어 문법 부탁.html
    "Could you please help me?": "",   # 3 181~189 서술어 문법 부탁.html
    "Please say it again.": "",   # 3 181~189 서술어 문법 부탁.html
    "Could you please say it again?": "",   # 3 181~189 서술어 문법 부탁.html
    "Please explain it again.": "",   # 3 181~189 서술어 문법 부탁.html
    "Could you please explain it again?": "",   # 3 181~189 서술어 문법 부탁.html
    "Please wait a moment.": "",   # 3 181~189 서술어 문법 부탁.html
    "Could you please wait a moment?": "",   # 3 181~189 서술어 문법 부탁.html
    "Could you exchange dollars for Korean won?": "",   # 3 181~189 서술어 문법 부탁.html
    "Have you ever been to Korea?": "",   # 3 190~198 서술어 문법 경험.html
    "I have been to Korea.": "",   # 3 190~198 서술어 문법 경험.html
    "I have never been to Korea.": "",   # 3 190~198 서술어 문법 경험.html
    "Have you ever tried going to Korea?": "",   # 3 190~198 서술어 문법 경험.html
    "I have tried going to Korea.": "",   # 3 190~198 서술어 문법 경험.html
    "I haven\\'t tried going to Korea.": "",   # 3 190~198 서술어 문법 경험.html
    "Please try this food.": "",   # 3 190~198 서술어 문법 경험.html
    "I have tried making kimchi.": "",   # 3 190~198 서술어 문법 경험.html
    "I want to visit Jeju Island someday.": "",   # 3 190~198 서술어 문법 경험.html
    "I helped my friend.": "",   # 3 199~203 서술어 문법 위한 행동.html
    "He waited for me.": "",   # 3 199~203 서술어 문법 위한 행동.html
    "He sang a song for me.": "",   # 3 199~203 서술어 문법 위한 행동.html
    "He made Korean food for me.": "",   # 3 199~203 서술어 문법 위한 행동.html
    "The father read a book to his son.": "",   # 3 199~203 서술어 문법 위한 행동.html
    "The weather got hot.": "",   # 3 204~208 서술어 문법 변화1.html
    "The weather got cold.": "",   # 3 204~208 서술어 문법 변화1.html
    "His grades got better.": "",   # 3 204~208 서술어 문법 변화1.html
    "Her skin has improved.": "",   # 3 204~208 서술어 문법 변화1.html
    "His health became bad.": "",   # 3 204~208 서술어 문법 변화1.html
    "I came to like K-pop.": "",   # 3 209~212 서술어 문법 변화2.html
    "I came to understand Korean culture.": "",   # 3 209~212 서술어 문법 변화2.html
    "I ended up being hospitalized.": "",   # 3 209~212 서술어 문법 변화2.html
    "I came to work at another company.": "",   # 3 209~212 서술어 문법 변화2.html
    "It seems like it rained last night.": "",   # 3 213~217 서술어 문법 추측.html
    "It seems like it\\'s raining now.": "",   # 3 213~217 서술어 문법 추측.html
    "It looks like it will rain tomorrow.": "",   # 3 213~217 서술어 문법 추측.html
    "I think this exam will be difficult.": "",   # 3 213~217 서술어 문법 추측.html
    "I think the movie will be fun.": "",   # 3 213~217 서술어 문법 추측.html
    "You must feel good.": "",   # 3 218~222 서술어 문법 공감.html
    "That must be heartbreaking.": "",   # 3 218~222 서술어 문법 공감.html
    "You must be hungry.": "",   # 3 218~222 서술어 문법 공감.html
    "You must be happy.": "",   # 3 218~222 서술어 문법 공감.html
    "You must be worried.": "",   # 3 218~222 서술어 문법 공감.html
    "The flowers are so beautiful.": "",   # 3 223~231 서술어 문법 감탄.html
    "The scenery is really nice.": "",   # 3 223~231 서술어 문법 감탄.html
    "The weather is so cold!": "",   # 3 223~231 서술어 문법 감탄.html
    "This food is really delicious.": "",   # 3 223~231 서술어 문법 감탄.html
    "The room is really clean!": "",   # 3 223~231 서술어 문법 감탄.html
    "The price is really cheap.": "",   # 3 223~231 서술어 문법 감탄.html
    "It\\'s snowing so much!": "",   # 3 223~231 서술어 문법 감탄.html
    "You sing really well.": "",   # 3 223~231 서술어 문법 감탄.html
    "A big restaurant opened over there.": "",   # 3 223~231 서술어 문법 감탄.html
    "The weather is really nice today, isn\\'t it?": "",   # 3 232~236 서술어 문법 확인.html
    "This coffee is really good, isn\\'t it?": "",   # 3 232~236 서술어 문법 확인.html
    "The class is at 11 tomorrow, right?": "",   # 3 232~236 서술어 문법 확인.html
    "You were really tired yesterday, weren\\'t you?": "",   # 3 232~236 서술어 문법 확인.html
    "This song is really good, isn\\'t it?": "",   # 3 232~236 서술어 문법 확인.html
    "Hi, how are you?": "",   # 3 237~247 서술어 문법 정중표현.html
    "Welcome.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Please sit down here.": "",   # 3 237~247 서술어 문법 정중표현.html
    "One bibimbap, please.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Enjoy your meal.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Goodbye. (to person leaving)": "",   # 3 237~247 서술어 문법 정중표현.html
    "Goodbye. (to person staying)": "",   # 3 237~247 서술어 문법 정중표현.html
    "Have a nice day.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Always be happy.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Stay healthy always.": "",   # 3 237~247 서술어 문법 정중표현.html
    "Happy new year!": "",   # 3 237~247 서술어 문법 정중표현.html
    "What did you do during the vacation?": "",   # 3 248~252 부사어 문법 시간 때.html
    "I went backpacking during the vacation.": "",   # 3 248~252 부사어 문법 시간 때.html
    "He did volunteer work during his vacation.": "",   # 3 248~252 부사어 문법 시간 때.html
    "He listens to music when he studies.": "",   # 3 248~252 부사어 문법 시간 때.html
    "I sing when I'm in a good mood.": "",   # 3 248~252 부사어 문법 시간 때.html
    "How long did you live in Korea?": "",   # 3 253~259 부사어 문법 기간 동안.html
    "I lived in Korea for two years.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "She studied Korean for three hours.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "He was in the hospital for a week.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "I worked part-time during the vacation.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "I couldn\\'t eat anything for two days.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "It snowed while we were sleeping.": "",   # 3 253~259 부사어 문법 기간 동안.html
    "The students cleaned the classroom before class.": "",   # 3 260~265 부사어 문법 전에.html
    "She prepared the materials before the meeting.": "",   # 3 260~265 부사어 문법 전에.html
    "Sumi plans to get TOPIK Level 6 before graduation.": "",   # 3 260~265 부사어 문법 전에.html
    "She traveled around Southeast Asia before coming to Korea.": "",   # 3 260~265 부사어 문법 전에.html
    "We booked a hotel before going on the trip.": "",   # 3 260~265 부사어 문법 전에.html
    "He says a prayer before eating.": "",   # 3 260~265 부사어 문법 전에.html
    "I met my friend after class.": "",   # 3 266~270 부사어 문법 후에.html
    "My father drinks coffee after a meal.": "",   # 3 266~270 부사어 문법 후에.html
    "After cleaning, the street became clean.": "",   # 3 266~270 부사어 문법 후에.html
    "He took a shower after exercising.": "",   # 3 266~270 부사어 문법 후에.html
    "She wrote a book report after reading the book.": "",   # 3 266~270 부사어 문법 후에.html
    "My father eats breakfast and then drinks coffee.": "",   # 3 271~276 부사어 문법 순서 고.html
    "My father drinks coffee and reads the newspaper.": "",   # 3 271~276 부사어 문법 순서 고.html
    "My father reads the newspaper and then goes to work.": "",   # 3 271~276 부사어 문법 순서 고.html
    "She washed her face and then put on makeup.": "",   # 3 271~276 부사어 문법 순서 고.html
    "He finished work and met his friend.": "",   # 3 271~276 부사어 문법 순서 고.html
    "He cleaned, did laundry, and met a friend on the weekend.": "",   # 3 271~276 부사어 문법 순서 고.html
    "Sumi went to a café and met her friend.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "Sumi met her friend and went to the theater.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "Sumi went to the theater and watched a movie.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "Sujae went to the department store and bought a gift.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "Sujae bought flowers and gave them to his friend.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "She went to the gym and exercised.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "He went to the bank and withdrew money.": "",   # 3 277~283 부사어 문법 순서원인 아어서.html
    "I study while listening to music.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "Father eats a meal while watching the news.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "Mother cooks while singing a song.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "She reads a book while drinking coffee.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "We talked while drinking coffee.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "You should not call while driving.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "He met many good people while traveling.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "He is both a singer and an actor.": "",   # 3 284~291 부사어 문법 동시 동작 으면서.htm
    "He drank water as soon as he woke up.": "",   # 3 292~295 부사어 문법 즉시 자마자.html
    "The power went out as soon as I turned on the computer.": "",   # 3 292~295 부사어 문법 즉시 자마자.html
    "He checked in as soon as he arrived at the airport.": "",   # 3 292~295 부사어 문법 즉시 자마자.html
    "We parted as soon as we met.": "",   # 3 292~295 부사어 문법 즉시 자마자.html
    "She fell asleep while watching TV.": "",   # 3 296~299 부사어 문법 동작 전환 다가.html
    "He met a friend while walking on the street.": "",   # 3 296~299 부사어 문법 동작 전환 다가.html
    "He broke a dish while washing the dishes.": "",   # 3 296~299 부사어 문법 동작 전환 다가.html
    "He had a nightmare while sleeping.": "",   # 3 296~299 부사어 문법 동작 전환 다가.html
    "Summer vacation starts today.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "We have a vacation from this Monday to next Sunday.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "Sumi studied Korean hard from morning to night.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "The exam range is from number 1 to 100.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "The exam time is from 9 AM to 1 PM.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "It takes three hours from Seoul to Busan by KTX.": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "How much is the taxi fare from Incheon Airport to Seoul City Hall?": "",   # 3 300~306 부사어 문법 범위 부터 까지.html
    "The airport was paralyzed because of the heavy snow.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "The trip was canceled because of the typhoon.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "There was a car accident because of the fog.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "The road is blocked because of the car accident.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "It is noisy because of the roadwork.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "He got lung cancer because of smoking.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "These days, the economy is bad because of the exchange rate.": "",   # 3 307~313 부사어 문법 원인 때문에.html
    "I passed the TOPIK exam thanks to my teacher.": "",   # 3 314~315 부사어 문법 원인 덕분에.html
    "The world became convenient thanks to AI.": "",   # 3 314~315 부사어 문법 원인 덕분에.html
    "Nice to meet you.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "I\\'m sorry for being late.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "Sumi has many friends because she has a good personality.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "Why are you going to the hospital?": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "I\\'m going to the hospital because I have a stomachache.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "Why are you studying Korean?": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "I study Korean because I like K-pop.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "The road is heavily congested, so I think I will be late.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "I didn\\'t know the way, so I took a taxi.": "",   # 3 316~324 부사어 문법 원인 아어서.html
    "Since it\\'s raining a lot, shall we leave work early?": "",   # 3 325~331 부사어 문법 원인 니까.html
    "Since it\\'s raining a lot, let\\'s leave work early.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "Since it\\'s raining a lot, please leave work early.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "Since it\\'s cold, let\\'s close the window.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "Since it\\'s hot, let\\'s turn on the air conditioner.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "Since it\\'s dangerous, be careful.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "When I opened the bag, the passport was not there.": "",   # 3 325~331 부사어 문법 원인 니까.html
    "He quit smoking for his health.": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "He bought a gift for his friend.": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "The husband bought a gift for his wife.": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "He watches Korean dramas to understand Korean culture.": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "He studied hard to achieve his dream.": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "What do you live for?": "",   # 3 332~337 부사어 문법 목적 위해서.html
    "Why do you study Korean?": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "I study Korean to get a job at a Korean company.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "Why do you go to the hospital?": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "I go to the hospital to get a health check-up.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "He bought a gift to give to his wife.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "He went to a coffee shop to meet his friend.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "She exercises every day to lose weight.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "She always wears a mask not to catch a cold.": "",   # 3 338~345 부사어 문법 목적 으려고.html
    "I went to a coffee shop to meet a friend.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "She went to the library to borrow a book.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "She went to the hair salon to get a haircut.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "She went to the market to buy fruit.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "She went to the bank to withdraw money.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "He came to Korea to learn Korean.": "",   # 3 346~351 부사어 문법 목적 으러 가다.html
    "If I earn a lot of money, I want to travel the world.": "",   # 3 352~355 부사어 문법 조건 으면.html
    "If I drink coffee, I can\\'t sleep.": "",   # 3 352~355 부사어 문법 조건 으면.html
    "If you are a member, you can get a discount.": "",   # 3 352~355 부사어 문법 조건 으면.html
    "If you enter the password, the door will open.": "",   # 3 352~355 부사어 문법 조건 으면.html
    "To be good at Korean, you need to like the language.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "To drive, you must have a driver\\'s license.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "To get up early, you need to go to bed early.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "To get a scholarship, your grades must be good.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "To travel abroad, you must have a passport and visa.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "To meet good people, you need to become a good person.": "",   # 3 356~361 부사어 문법 필수 조건 으려면.htm
    "Even without money, you can still be happy.": "",   # 3 362~365 부사어 문법 예상과 다른 결과 아어도
    "Even if you have a lot of money, you might not be happy.": "",   # 3 362~365 부사어 문법 예상과 다른 결과 아어도
    "No matter how much medicine I take, my cold doesn\\'t get better.": "",   # 3 362~365 부사어 문법 예상과 다른 결과 아어도
    "No matter how much I exercise, I don\\'t lose weight.": "",   # 3 362~365 부사어 문법 예상과 다른 결과 아어도
    "It is raining, but I don\\'t have an umbrella.": "",   # 3 366~369 부사어 문법 배경 상황 는데.html
    "I played table tennis with Sumi, but I lost.": "",   # 3 366~369 부사어 문법 배경 상황 는데.html
    "I got on the bus, but there were no seats.": "",   # 3 366~369 부사어 문법 배경 상황 는데.html
    "I am busy today, so can you call me tomorrow?": "",   # 3 366~369 부사어 문법 배경 상황 는데.html
    "This apple is big.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "This apple is as big as a watermelon.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "This apple is bigger than a watermelon.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "This apple is less big than a watermelon.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "This apple is the biggest in Korea.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "This apple is the biggest among the apples.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Sumi sings well.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Sumi sings well like a singer.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Sumi sings better than a singer.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Sumi sings the best in our class.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Sumi sings the best among the students.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Today is colder than yesterday.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "I like fall more than spring.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Mother\\'s love is higher than the sky and deeper than the sea.": "",   # 3 370~383 기타 문법 비교급 최상급.html
    "Learning Korean is fun.": "",   # 3 384~387 기타 문법 명사형.html
    "He likes cooking.": "",   # 3 384~387 기타 문법 명사형.html
    "Tomorrow, we have speaking, listening, reading, and writing tests.": "",   # 3 384~387 기타 문법 명사형.html
    "Love is waiting.": "",   # 3 384~387 기타 문법 명사형.html
    "I enjoyed the meal.": "",   # 3 388~396 기타 문법 부사형.html
    "She writes beautifully.": "",   # 3 388~396 기타 문법 부사형.html
    "That store sells clothes cheaply.": "",   # 3 388~396 기타 문법 부사형.html
    "He explained it to me kindly.": "",   # 3 388~396 기타 문법 부사형.html
    "She washed the apple cleanly.": "",   # 3 388~396 기타 문법 부사형.html
    "Please rest comfortably.": "",   # 3 388~396 기타 문법 부사형.html
    "He earned a lot of money.": "",   # 3 388~396 기타 문법 부사형.html
    "He threw the ball far.": "",   # 3 388~396 기타 문법 부사형.html
    "I like him.": "",   # 3 397~400 기타 문법 동사화.html
    "He dislikes me.": "",   # 3 397~400 기타 문법 동사화.html
    "My grandmother adores me.": "",   # 3 397~400 기타 문법 동사화.html
    "She is afraid of snakes.": "",   # 3 397~400 기타 문법 동사화.html
    "There is milk in the refrigerator.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "There is only milk in the refrigerator.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "There is nothing except milk in the refrigerator.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "I exercise in the morning.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "Only I exercise in the morning.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "I exercise only in the morning.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "I only exercise in the morning.": "",   # 3 401~407 기타 문법 한정 만 밖에.html
    "He went back to his hometown.": "",   # 3 408~413 기타 문법 로 으로.html
    "He goes to school by bicycle.": "",   # 3 408~413 기타 문법 로 으로.html
    "Kimchi is made with cabbage.": "",   # 3 408~413 기타 문법 로 으로.html
    "Because of COVID-19, the trip was canceled.": "",   # 3 408~413 기타 문법 로 으로.html
    "He is working as an interpreter.": "",   # 3 408~413 기타 문법 로 으로.html
    "I\\'d like to exchange dollars for Korean won, please.": "",   # 3 408~413 기타 문법 로 으로.html
    "He sometimes goes to the beach.": "",   # 3 414~418 기타 문법 빈도부사.html
    "He often goes to the coffee shop.": "",   # 3 414~418 기타 문법 빈도부사.html
    "He always sings.": "",   # 3 414~418 기타 문법 빈도부사.html
    "He exercises every morning.": "",   # 3 414~418 기타 문법 빈도부사.html
    "He goes to a coffee shop every day.": "",   # 3 414~418 기타 문법 빈도부사.html
    "There are four students in the classroom.": "",   # 3 419~435 기타 문법 종별사.html
    "There are two apples in the refrigerator.": "",   # 3 419~435 기타 문법 종별사.html
    "There is one dog in the house.": "",   # 3 419~435 기타 문법 종별사.html
    "He bought two books.": "",   # 3 419~435 기타 문법 종별사.html
    "She booked two movie tickets.": "",   # 3 419~435 기타 문법 종별사.html
    "Kyoungjin drank two bottles of cola.": "",   # 3 419~435 기타 문법 종별사.html
    "Please give me one cup of water.": "",   # 3 419~435 기타 문법 종별사.html
    "Please give me one cup of coffee.": "",   # 3 419~435 기타 문법 종별사.html
    "Please give me one sheet of paper.": "",   # 3 419~435 기타 문법 종별사.html
    "There are five cars in the parking lot.": "",   # 3 419~435 기타 문법 종별사.html
    "There is one ship in the sea.": "",   # 3 419~435 기타 문법 종별사.html
    "There are ten trees in the garden.": "",   # 3 419~435 기타 문법 종별사.html
    "He gave me one flower.": "",   # 3 419~435 기타 문법 종별사.html
    "I gave him a bouquet of flowers.": "",   # 3 419~435 기타 문법 종별사.html
    "I\\'m going to watch two movies this weekend.": "",   # 3 419~435 기타 문법 종별사.html
    "There are three pairs of shoes at home.": "",   # 3 419~435 기타 문법 종별사.html
    "He had one suit tailored.": "",   # 3 419~435 기타 문법 종별사.html
    "명사 선택을 취소했습니다. 다시 고르세요.": "",   # 3 419~435 기타 문법 종별사.html
    "명사 선택: <strong>": "",   # 3 419~435 기타 문법 종별사.html
    "</strong> → 짝이 되는 종별사를 고르세요.": "",   # 3 419~435 기타 문법 종별사.html
    "종별사 선택을 취소했습니다. 다시 고르세요.": "",   # 3 419~435 기타 문법 종별사.html
    "종별사 선택: <strong>": "",   # 3 419~435 기타 문법 종별사.html
    "</strong> → 짝이 되는 명사를 고르세요.": "",   # 3 419~435 기타 문법 종별사.html
    "🎉 완료! 모든 명사-종별사 짝을 맞췄습니다. <span style=\"color:#0f5e2c;\">All matched!</span>": "",   # 3 419~435 기타 문법 종별사.html
    "왼쪽 명사 하나와 오른쪽 종별사 하나를 선택하세요.": "",   # 3 419~435 기타 문법 종별사.html
    "I know her.": "",   # 3 436~440 기타 문법 ㄹ불규칙.html
    "What are you making now?": "",   # 3 436~440 기타 문법 ㄹ불규칙.html
    "He sells vegetables and fruits at the market.": "",   # 3 436~440 기타 문법 ㄹ불규칙.html
    "The children play in the park.": "",   # 3 436~440 기타 문법 ㄹ불규칙.html
    "I live in Seoul.": "",   # 3 436~440 기타 문법 ㄹ불규칙.html
    "I was heartbroken.": "",   # 3 441~444 기타 문법 ㅡ불규칙.html
    "I was very happy to meet my hometown friend.": "",   # 3 441~444 기타 문법 ㅡ불규칙.html
    "I was busy last week, so I couldn\\'t exercise.": "",   # 3 441~444 기타 문법 ㅡ불규칙.html
    "I wrote a letter to her.": "",   # 3 441~444 기타 문법 ㅡ불규칙.html
    "He cut the tree.": "",   # 3 445~448 기타 문법 르불규칙.html
    "He was different from ordinary people.": "",   # 3 445~448 기타 문법 르불규칙.html
    "He sang a song.": "",   # 3 445~448 기타 문법 르불규칙.html
    "He was faster than me.": "",   # 3 445~448 기타 문법 르불규칙.html
    "It was so hot yesterday.": "",   # 3 449~453 기타 문법 ㅂ불규칙.html
    "It was so cold yesterday.": "",   # 3 449~453 기타 문법 ㅂ불규칙.html
    "He helped me.": "",   # 3 449~453 기타 문법 ㅂ불규칙.html
    "He wore a hanbok.": "",   # 3 449~453 기타 문법 ㅂ불규칙.html
    "The road was narrow.": "",   # 3 449~453 기타 문법 ㅂ불규칙.html
    "He asked me my name.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "I have heard that song before.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "He goes to school on foot.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "He closed the window.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "He trusted me.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "I received a book as a birthday present.": "",   # 3 454~459 기타 문법 ㄷ불규칙.html
    "He cooked rice.": "",   # 3 460~461 기타 문법 ㅅ불규칙.html
    "He has fully recovered from his illness.": "",   # 3 460~461 기타 문법 ㅅ불규칙.html
    "He said, <strong>The weather is too hot.</strong>": "",   # 3 462~473 기타 문법 간접화법.html
    "He said the weather was too hot.": "",   # 3 462~473 기타 문법 간접화법.html
    "He said, <strong>I am an office worker.</strong>": "",   # 3 462~473 기타 문법 간접화법.html
    "He said that he was an office worker.": "",   # 3 462~473 기타 문법 간접화법.html
    "He told me, <strong>Please come quickly.</strong>": "",   # 3 462~473 기타 문법 간접화법.html
    "He told me to come quickly.": "",   # 3 462~473 기타 문법 간접화법.html
    "He asked me what time I would come tomorrow.": "",   # 3 462~473 기타 문법 간접화법.html
    "He told me not to drink alcohol.": "",   # 3 462~473 기타 문법 간접화법.html
    "He said to me, <strong>Let\\'s get married.</strong>": "",   # 3 462~473 기타 문법 간접화법.html
    "He asked me to marry him.": "",   # 3 462~473 기타 문법 간접화법.html
    "She said that she is busy now.": "",   # 3 462~473 기타 문법 간접화법.html
    "They say it will rain tomorrow.": "",   # 3 462~473 기타 문법 간접화법.html
    "This is the school I attended.": "",   # 3 474~488 기타 문법 관형어.html
    "This is the school I attend.": "",   # 3 474~488 기타 문법 관형어.html
    "This is the school I will attend.": "",   # 3 474~488 기타 문법 관형어.html
    "This is my favorite place.": "",   # 3 474~488 기타 문법 관형어.html
    "This is the book I am reading.": "",   # 3 474~488 기타 문법 관형어.html
    "This is the book I will read.": "",   # 3 474~488 기타 문법 관형어.html
    "This is the book that I read.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi bought clothes at the department store yesterday.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi with long hair bought clothes at the department store yesterday.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi bought clothes at the department store yesterday when it rained a lot.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi bought clothes at the department store next to the station yesterday.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi bought clothes at the department store yesterday to wear at her friend\\'s wedding.": "",   # 3 474~488 기타 문법 관형어.html
    "Sumi with long hair bought clothes at the department store next to the station yesterday, when it rained a lot, to wear at her friend\\'s wedding.": "",   # 3 474~488 기타 문법 관형어.html
    "The most important moment in life is now.": "",   # 3 474~488 기타 문법 관형어.html
    "The most important person in life is the person I am meeting now.": "",   # 3 474~488 기타 문법 관형어.html
    "My mother is cooking.": "",   # 3 489~500 기타 문법 존댓말.html
    "My grandmother is having a meal.": "",   # 3 489~500 기타 문법 존댓말.html
    "I gave a gift to my mother.": "",   # 3 489~500 기타 문법 존댓말.html
    "My mother gave me a gift.": "",   # 3 489~500 기타 문법 존댓말.html
    "The boss spoke to the employees.": "",   # 3 489~500 기타 문법 존댓말.html
    "My great-grandmother passed away this morning.": "",   # 3 489~500 기타 문법 존댓말.html
    "My parents are now in their hometown.": "",   # 3 489~500 기타 문법 존댓말.html
    "My grandfather is sleeping.": "",   # 3 489~500 기타 문법 존댓말.html
    "I\\'m going to meet my teacher tomorrow.": "",   # 3 489~500 기타 문법 존댓말.html
    "My grandmother is sick these days.": "",   # 3 489~500 기타 문법 존댓말.html
    "I took my grandmother to the hospital.": "",   # 3 489~500 기타 문법 존댓말.html
    "Boss, congratulations on your son\\'s wedding and your daughter\\'s graduation.": "",   # 3 489~500 기타 문법 존댓말.html
    "</div><div class=\"hint\">읽고 확인 ↻<br><span style=\"font-size:0.85em;\">Read &amp; check</span></div></div><div class=\"numfc-b\"><small>": "",   # 4 부록 1 숫자.html
    "8 (고유어)": "",   # 4 부록 1 숫자.html
    "20 (고유어)": "",   # 4 부록 1 숫자.html
    "70 (한자어)": "",   # 4 부록 1 숫자.html
    "3:00 PM": "",   # 4 부록 1 숫자.html
    "<button class=\"ans-btn\" onclick=\"qAll(this,true)\">💡 모두 보기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Show all</span></button><button class=\"ans-btn\" onclick=\"qAll(this,false)\">🔄 다시 가리기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Hide again</span></button><span class=\"ans-hint\">노란 테두리 칸은 보기입니다. 나머지 ?를 눌러 확인<span class=\"gloss\" lang=\"en\" translate=\"yes\">Highlighted cells are examples</span></span>": "",   # 4 부록 1 숫자.html
    "<button class=\"ans-btn\" onclick=\"qAll(this,true)\">💡 모두 보기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Show all</span></button><button class=\"ans-btn\" onclick=\"qAll(this,false)\">🔄 다시 가리기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Hide again</span></button><span class=\"ans-hint\">각 칸의 ?를 눌러 정답 확인, 정답을 다시 누르면 가려집니다<span class=\"gloss\" lang=\"en\" translate=\"yes\">Tap ? to reveal, tap again to hide</span></span>": "",   # 4 부록 2 부정법.html
    "<br><small style=\"color:#966106;font-weight:800;\">보기</small>": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to go": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to meet": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to eat": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to exist / have": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to not exist": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to know": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to make": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to come": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to learn": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to drink": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to draw": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to pay": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to do": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to love": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to be": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to be big": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to be different": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to be easy": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to be good": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to listen": "",   # 4 부록 3 격식체 구어체 문어체.html
    "to believe": "",   # 4 부록 3 격식체 구어체 문어체.html
    "</div></div><div class=\"flashcard-hint\">▼ <span lang=\"en\" translate=\"yes\">Tap to check</span></div></div>": "",   # 4 부록 3 격식체 구어체 문어체.html
    "<button class=\"ans-btn\" onclick=\"qAll(this,true)\">💡 모두 보기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Show all</span></button><button class=\"ans-btn\" onclick=\"qAll(this,false)\">🔄 다시 가리기<span class=\"gloss\" lang=\"en\" translate=\"yes\">Hide again</span></button><span class=\"ans-hint\">첫 줄 <b>가다</b>는 보기입니다. 나머지는 ?를 눌러 정답 확인(다시 누르면 가려짐)<br><span class=\"en-line\" lang=\"en\" translate=\"yes\">First row (<span lang=\"ko\" translate=\"no\">가다</span>) is a worked example</span></span>": "",   # 4 부록 3 격식체 구어체 문어체.html
    "go (present)": "",   # 4 부록 4 기초문법연습 01.html
    "went (past)": "",   # 4 부록 4 기초문법연습 01.html
    "will go (future)": "",   # 4 부록 4 기초문법연습 01.html
    "is going (progressive)": "",   # 4 부록 4 기초문법연습 01.html
    "go and… (and)": "",   # 4 부록 4 기초문법연습 01.html
    "can go (ability)": "",   # 4 부록 4 기초문법연습 01.html
    "Let's go (suggestion)": "",   # 4 부록 4 기초문법연습 01.html
    "Shall we go?": "",   # 4 부록 4 기초문법연습 01.html
    "don't go (negation)": "",   # 4 부록 4 기초문법연습 01.html
    "can't go (impossible)": "",   # 4 부록 4 기초문법연습 01.html
    "please don't go (command)": "",   # 4 부록 4 기초문법연습 01.html
    "want to go (hope)": "",   # 4 부록 4 기초문법연습 01.html
    " · EN</div><div class=\"flashcard-text\">": "",   # 4 부록 4 기초문법연습 01.html
    "</div><div class=\"flashcard-hint\">▼ <span lang=\"en\" translate=\"yes\">Tap to check</span></div></div>": "",   # 4 부록 4 기초문법연습 01.html
    " · KR</div><div class=\"flashcard-text\">": "",   # 4 부록 4 기초문법연습 01.html
    "\\')\" title=\"Listen\">🔊</button></div>": "",   # 4 부록 4 기초문법연습 01.html
    "Let's": "",   # 4 부록 4 기초문법연습 01.html
    "Shall we?": "",   # 4 부록 4 기초문법연습 01.html
    "don't (short)": "",   # 4 부록 4 기초문법연습 01.html
    "don't (long)": "",   # 4 부록 4 기초문법연습 01.html
    "can't (short)": "",   # 4 부록 4 기초문법연습 01.html
    "can't (long)": "",   # 4 부록 4 기초문법연습 01.html
    "Don't": "",   # 4 부록 4 기초문법연습 01.html
    "Let's not": "",   # 4 부록 4 기초문법연습 01.html
    "Shall we not?": "",   # 4 부록 4 기초문법연습 01.html
    "want to": "",   # 4 부록 4 기초문법연습 01.html
    "Let\\'s go (suggestion)": "",   # 4 부록 4 기초문법연습 01.html
    "don\\'t go (negation)": "",   # 4 부록 4 기초문법연습 01.html
    "can\\'t go (impossible)": "",   # 4 부록 4 기초문법연습 01.html
    "do not want to go": "",   # 4 부록 5 기초문법연습 02.html
    "I wish I could go": "",   # 4 부록 5 기초문법연습 02.html
    "plan to go": "",   # 4 부록 5 기초문법연습 02.html
    "have a plan to go": "",   # 4 부록 5 기초문법연습 02.html
    "decided to go": "",   # 4 부록 5 기초문법연습 02.html
    "may go (allowed)": "",   # 4 부록 5 기초문법연습 02.html
    "must not go": "",   # 4 부록 5 기초문법연습 02.html
    "must go": "",   # 4 부록 5 기초문법연습 02.html
    "do not have to go": "",   # 4 부록 5 기초문법연습 02.html
    "please go for me": "",   # 4 부록 5 기초문법연습 02.html
    "have been there": "",   # 4 부록 5 기초문법연습 02.html
    "have tried going": "",   # 4 부록 5 기초문법연습 02.html
    "do not want to": "",   # 4 부록 5 기초문법연습 02.html
    "I wish": "",   # 4 부록 5 기초문법연습 02.html
    "plan (intend)": "",   # 4 부록 5 기초문법연습 02.html
    "prohibition (command)": "",   # 4 부록 5 기초문법연습 02.html
    "favor, request": "",   # 4 부록 5 기초문법연습 02.html
    "favor (polite Q)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (tried)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (couldn't try)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (have done)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (never done)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (have tried)": "",   # 4 부록 5 기초문법연습 02.html
    "experience (never tried)": "",   # 4 부록 5 기초문법연습 02.html
    "went for someone (favor)": "",   # 4 부록 6 기초문법연습 03.html
    "came to go": "",   # 4 부록 6 기초문법연습 03.html
    "will go (intend)": "",   # 4 부록 6 기초문법연습 03.html
    "you go, right?": "",   # 4 부록 6 기초문법연습 03.html
    "please go": "",   # 4 부록 6 기초문법연습 03.html
    "do you go? (polite)": "",   # 4 부록 6 기초문법연습 03.html
    "when going": "",   # 4 부록 6 기초문법연습 03.html
    "while going": "",   # 4 부록 6 기초문법연습 03.html
    "before going": "",   # 4 부록 6 기초문법연습 03.html
    "after going": "",   # 4 부록 6 기초문법연습 03.html
    "while going (at once)": "",   # 4 부록 6 기초문법연습 03.html
    "as soon as going": "",   # 4 부록 6 기초문법연습 03.html
    "an action for others": "",   # 4 부록 6 기초문법연습 03.html
    "change (become)": "",   # 4 부록 6 기초문법연습 03.html
    "change (come to)": "",   # 4 부록 6 기초문법연습 03.html
    "will, guess, promise": "",   # 4 부록 6 기초문법연습 03.html
    "confirm, agree": "",   # 4 부록 6 기초문법연습 03.html
    "soft command": "",   # 4 부록 6 기초문법연습 03.html
    "polite question": "",   # 4 부록 6 기초문법연습 03.html
    "when, while": "",   # 4 부록 6 기초문법연습 03.html
    "sequential (and then)": "",   # 4 부록 6 기초문법연습 03.html
    "sequential (after ~ing)": "",   # 4 부록 6 기초문법연습 03.html
    "sequential (after done)": "",   # 4 부록 6 기초문법연습 03.html
    "as soon as": "",   # 4 부록 6 기초문법연습 03.html
    "transition while going": "",   # 4 부록 7 기초문법연습 04.html
    "from when going": "",   # 4 부록 7 기초문법연습 04.html
    "until going": "",   # 4 부록 7 기초문법연습 04.html
    "because of going": "",   # 4 부록 7 기초문법연습 04.html
    "thanks to going": "",   # 4 부록 7 기초문법연습 04.html
    "going, so": "",   # 4 부록 7 기초문법연습 04.html
    "since going": "",   # 4 부록 7 기초문법연습 04.html
    "in order to go": "",   # 4 부록 7 기초문법연습 04.html
    "if going": "",   # 4 부록 7 기초문법연습 04.html
    "if you want to go": "",   # 4 부록 7 기초문법연습 04.html
    "even if going": "",   # 4 부록 7 기초문법연습 04.html
    "the act of going": "",   # 4 부록 7 기초문법연습 04.html
    "action transition": "",   # 4 부록 7 기초문법연습 04.html
    "from (starting)": "",   # 4 부록 7 기초문법연습 04.html
    "to (until)": "",   # 4 부록 7 기초문법연습 04.html
    "cause (because)": "",   # 4 부록 7 기초문법연습 04.html
    "cause (thanks to)": "",   # 4 부록 7 기초문법연습 04.html
    "cause (so)": "",   # 4 부록 7 기초문법연습 04.html
    "cause (since)": "",   # 4 부록 7 기초문법연습 04.html
    "purpose (for the sake of)": "",   # 4 부록 7 기초문법연습 04.html
    "purpose (in order to)": "",   # 4 부록 7 기초문법연습 04.html
    "purpose (to go and)": "",   # 4 부록 7 기초문법연습 04.html
    "assumption, condition": "",   # 4 부록 7 기초문법연습 04.html
    "essential condition": "",   # 4 부록 7 기초문법연습 04.html
    "unexpected outcome": "",   # 4 부록 7 기초문법연습 04.html
    "background, context": "",   # 4 부록 7 기초문법연습 04.html
    "verb/adj to noun (act)": "",   # 4 부록 7 기초문법연습 04.html
    "adjective to adverb": "",   # 4 부록 7 기초문법연습 04.html
    "adjective to verb": "",   # 4 부록 7 기초문법연습 04.html
}

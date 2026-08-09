# -*- coding: utf-8 -*-
"""일본어판 번역표
  TEXT : 번역 슬롯(translate="yes")의 영어 → 일본어. {0}{1} 은 잠긴 한국어 자리다.
  UI   : 「한국어 라벨 + 영어 gloss」 짝의 한국어 → 일본어. gloss 는 지워진다.
  JS   : 스크립트 안 문자열 리터럴 → 일본어.
"""
LANG = "ja"

# ── ② UI 라벨 (한국어 → 일본어) ─────────────────────────────
UI = {
    "어휘": "語彙", "📚 어휘": "📚 語彙",
    "해설": "解説", "📖 해설": "📖 解説",
    "정답 보기": "答えを見る", "정답": "正解", "오답": "不正解",
    "💡 정답": "💡 答え", "💡 전체 정답": "💡 全部の答え",
    "✅ 채점": "✅ 採点", "✅ 점수": "✅ 点数",
    "🔄 다시 시작": "🔄 もう一度", "🔄 초기화": "🔄 やり直す",
    "닫기": "閉じる", "결과": "結果", "요약": "まとめ",
    "한국어": "韓国語", "영어": "日本語", "역할": "役割",
    "주어": "主語", "서술어": "述語", "서술어(동사)": "述語(動詞)",
    "기본형": "基本形", "단어": "単語", "변화": "変化",
    "평서": "平叙", "의문": "疑問", "평서형": "平叙形", "의문형": "疑問形",
    "음성": "音声",
    "한국어 어순: 주어 + 서술어(동사)": "韓国語の語順: 主語 + 述語(動詞)",
    "문항에 필요한 과거형 규칙": "各文に必要な過去形の規則",
    "ㄷ 불규칙": "ㄷ 不規則",
    "✅ ㄷ이 ㄹ로 바뀝니다": "✅ ㄷ が ㄹ に変わります",
    "⚠️ ㄷ이 그대로입니다": "⚠️ ㄷ のままです",
    "📘 과거형 Ⓐ 규칙": "📘 過去形 Ⓐ 規則",
    "📘 과거형 Ⓑ 줄임": "📘 過去形 Ⓑ 縮約",
    "📘 과거형 Ⓒ 하다": "📘 過去形 Ⓒ 하다",
    "📘 과거형 Ⓕ ㄷ 불규칙": "📘 過去形 Ⓕ ㄷ 不規則",
}

# ── ②-ㄴ 영어 짝이 아예 없는 한국어 전용 UI ─────────────────
#    글자 조각 전체가 열쇠와 같을 때만 바뀐다
SOLO = {
    "왼쪽 영어 문장과 오른쪽 한국어 문장을 짝 맞추기":
        "左の日本語の文と右の韓国語の文を組み合わせる",
    "영어-한국어 문장 맞추기": "日本語-韓国語 文のマッチング",
    "왼쪽 영어 문장을 클릭하고, 그 뜻에 맞는 오른쪽 한국어 문장을 클릭하세요. 짝이 맞으면 두 문장이 사라집니다.":
        "左の日本語の文をクリックし、意味の合う右の韓国語の文をクリックしてください。合うと二つの文が消えます。",
    "영어를 보고 한국어로 써 보세요": "日本語を見て韓国語で書いてみましょう",
    "정답": "正解", "오답": "不正解", "✓ 점수": "✓ 点数", "영어": "日本語",
    "연습: 한국어 문장을 만들어 보세요!": "練習: 韓国語の文を作りましょう！",
    "한국어 문장 읽기": "韓国語の文を読む",
    "그림을 보고 한국어로 말해 보세요": "絵を見て韓国語で言ってみましょう",
}

# ── ③ 스크립트 안 문자열 ────────────────────────────────────
JS = {
    "영어 선택: <strong>": "日本語の文: <strong>",
    "</strong> → 짝이 되는 한국어 문장을 고르세요.": "</strong> → 対応する韓国語の文を選んでください。",
    "한국어 선택: <strong>": "韓国語の文: <strong>",
    "</strong> → 짝이 되는 영어 문장을 고르세요.": "</strong> → 対応する日本語の文を選んでください。",
    "영어 선택을 취소했습니다. 다시 고르세요.": "日本語の選択を取り消しました。もう一度選んでください。",
    "한국어 선택을 취소했습니다. 다시 고르세요.": "韓国語の選択を取り消しました。もう一度選んでください。",
    "</strong> 정답!": "</strong> 正解！",
    '</strong> — 짝이 아닙니다. 다시 고르세요. <span style="color:#94a3b8;">Not a match.</span>':
        '</strong> — 合いません。もう一度選んでください。<span style="color:#94a3b8;">合いません。</span>',
    '🎉 완료! 모든 문장을 맞췄습니다. <span style="color:#15803d;">All matched!</span>':
        '🎉 完了！すべての文がそろいました。<span style="color:#15803d;">全部そろいました！</span>',
    '모든 문장을 맞췄습니다!<br><span style="color:#94a3b8;font-size:0.9rem;">All sentences matched!</span>':
        'すべての文がそろいました！<br><span style="color:#94a3b8;font-size:0.9rem;">全文マッチ完了！</span>',
    '모든 문장을 정확히 작성했습니다!<br><span style="color:#94a3b8;font-size:0.9rem;">All sentences correct!</span>':
        'すべての文を正しく書けました！<br><span style="color:#94a3b8;font-size:0.9rem;">全文正解！</span>',
    "\\u{1F389} 정답!<small>Correct!</small>": "\\u{1F389} 正解！<small>正解！</small>",
    "정답! <small>Correct</small>": "正解！<small>正解</small>",
    '<span class="fc-flip-hint">↻ 클릭</span>': '<span class="fc-flip-hint">↻ タップ</span>',
    "여성 음성 · ": "女性の声 · ",
    "남성 음성 · ": "男性の声 · ",
    "이 브라우저에는 한국어 남성 음성이 없어 목소리를 낮춰 읽습니다. Microsoft Edge 에서 진짜 남성 음성(InJoon)이 나옵니다.":
        "このブラウザには韓国語の男性音声がないため、女性音声を低くして読み上げます。"
        "本物の男性音声は Microsoft Edge で再生されます。",
    # 문장 맞추기의 「독자 언어」 쪽 데이터
    "He slept.": "彼は寝ました。", "He got up.": "彼は起きました。",
    "He walked.": "彼は歩きました。", "He ran.": "彼は走りました。",
    "He worked.": "彼は働きました。", "He rested.": "彼は休みました。",
    "He thought.": "彼は考えました。", "He spoke.": "彼は話しました。",
    "He listened.": "彼は聞きました。", "He went.": "彼は行きました。",
}

# ── ① 번역 슬롯 (영어 → 일본어) ─────────────────────────────
TEXT = {
    "Listen": "聞く",
    "Listen — female voice": "聞く — 女性の声",
    "Listen — male voice": "聞く — 男性の声",
    '🔊<span class="spk-tag">여</span>': '🔊<span class="spk-tag">女</span>',
    '🔊<span class="spk-tag">남</span>': '🔊<span class="spk-tag">男</span>',
    "🔊": "🔊",
    "Explanation": "解説", "Vocabulary": "語彙",
    "Write in Korean.": "韓国語で書いてください。",
    "Show Answer": "答えを見る", "Answer": "答え",
    "Tap to flip": "タップしてめくる",
    "Restart": "もう一度", "Reset": "やり直す", "Grade": "採点", "Close": "閉じる",
    "Correct": "正解", "Wrong": "不正解", "All matched!": "全部そろいました！",
    "· Score:": "",  # 앞에 「✓ 점수」 가 있다
    "English": "日本語", "English ·": "",  # 뒤에 「영어」 라벨이 이어진다
    "Click an English sentence, then its Korean match — both disappear when matched.": "",
    "Korean": "韓国語", "Role": "役割", "Subject": "主語", "Predicate": "述語",
    "Predicate (Verb)": "述語(動詞)", "Verb": "動詞", "Noun + Particle": "名詞 + 助詞",
    "Korean order: Subject + Predicate(Verb)": "韓国語の語順: 主語 + 述語(動詞)",
    "Subject + Predicate (Verb)": "主語 + 述語(動詞)",
    "Subject + Verb": "主語 + 動詞",
    "Amazing Korean 1 — Sentence Structure 2: Subject + Verb":
        "Amazing Korean 1 — 文の構造 2: 主語 + 動詞",
    "Amazing Korean 1 — Sentence Structure 2: Subject + Verb (":
        "Amazing Korean 1 — 文の構造 2: 主語 + 動詞 (",
    "Sentence Structure 2": "文の構造 2",
    "The Basic Pattern": "基本パターン",
    "Practice: Make Korean sentences!": "練習: 韓国語の文を作りましょう！",
    "1. Read Along": "1. 音読", "2. Look &amp; Speak": "2. 見て話す",
    "3. Sentence Matching": "3. 文のマッチング", "4. Writing Test": "4. 書き取りテスト",
    "🔗 Sentence Matching ·": "🔗",  # 뒤에 한국어 제목이 이어져 겹친다
    "10 sentences — past tense conversion": "10 文 — 過去形に変える",
    "<em>The most basic Korean sentence is <strong>Subject + Predicate</strong>. "
    "In Structure 2, the predicate is a <strong>verb</strong>, describing what someone does (or did).</em>":
        "<em>韓国語の最も基本的な文は <strong>主語 + 述語</strong> です。文の構造 2 では述語が "
        "<strong>動詞</strong> で、誰かが何をするか(したか)を表します。</em>",
    "<em>All 10 sentences below are in <strong>past tense</strong>, using the same subject "
    "<strong>{0}</strong> (he). Open the rule each sentence needs below.</em>":
        "<em>下の 10 文はすべて <strong>過去形</strong> で、主語はどれも <strong>{0}</strong>(彼は)です。"
        "各文に必要な規則は下のリンクから開いてください。</em>",
    "The past-tense rule each sentence needs": "各文に必要な過去形の規則",
    "Regular — {0}": "規則 — {0}", "Contraction": "縮約",
    "{0} verbs — {1}": "{0} 動詞 — {1}", "{0} irregular": "{0} 不規則",
    "The {0} irregular": "{0} 不規則",
    "It changes — irregular": "変わります — 不規則",
    "No change — regular": "変わりません — 規則",
    "When a stem ending in {0} meets an ending that begins with a vowel, such as {1}, "
    "the {2} becomes {3}.":
        "語幹の末尾が {0} の語が、{1} のように母音で始まる語尾に続くと、{2} は {3} に変わります。",
    "A final {0} does not always mean the verb is irregular — learn the two groups side by side.":
        "終声が {0} だからといって必ず不規則とは限りません。二つのグループを並べて覚えてください。",
    "This browser has no Korean male voice, so the female voice is pitched down. "
    "Open the page in Microsoft Edge for a real male voice.":
        "このブラウザには韓国語の男性音声がないため、女性音声を低くして読み上げます。"
        "本物の男性音声は Microsoft Edge で再生されます。",
    "He": "彼は", "he": "彼", "<strong>He</strong>": "<strong>彼は</strong>",
    "He slept.": "彼は寝ました。", "11) He slept.": "11) 彼は寝ました。",
    "He got up.": "彼は起きました。", "12) He got up.": "12) 彼は起きました。",
    "He walked.": "彼は歩きました。", "13) He walked.": "13) 彼は歩きました。",
    "He ran.": "彼は走りました。", "14) He ran.": "14) 彼は走りました。",
    "He worked.": "彼は働きました。", "15) He worked.": "15) 彼は働きました。",
    "He rested.": "彼は休みました。", "16) He rested.": "16) 彼は休みました。",
    "He thought.": "彼は考えました。", "17) He thought.": "17) 彼は考えました。",
    "He spoke.": "彼は話しました。", "18) He spoke.": "18) 彼は話しました。",
    "He listened.": "彼は聞きました。", "19) He listened.": "19) 彼は聞きました。",
    "He went.": "彼は行きました。", "20) He went.": "20) 彼は行きました。",
    "<strong>slept</strong>": "<strong>寝ました</strong>",
    "<strong>got up</strong>": "<strong>起きました</strong>",
    "<strong>walked</strong>": "<strong>歩きました</strong>",
    "<strong>ran</strong>": "<strong>走りました</strong>",
    "<strong>worked</strong>": "<strong>働きました</strong>",
    "<strong>rested</strong>": "<strong>休みました</strong>",
    "<strong>thought</strong>": "<strong>考えました</strong>",
    "<strong>spoke</strong>": "<strong>話しました</strong>",
    "<strong>listened</strong>": "<strong>聞きました</strong>",
    "<strong>went</strong>": "<strong>行きました</strong>",
    "slept": "寝ました",
    "sleep": "寝る", "get up": "起きる", "walk": "歩く", "run": "走る",
    "work": "働く", "rest": "休む", "think": "考える", "speak": "話す",
    "listen": "聞く", "listen, hear": "聞く", "go": "行く",
    "ask": "尋ねる", "close": "閉める", "receive": "受け取る",
}
for n in range(11, 21):
    TEXT[f"{n} · EN"] = f"{n} · 日"
    TEXT[f"{n} · KR"] = f"{n} · 韓"

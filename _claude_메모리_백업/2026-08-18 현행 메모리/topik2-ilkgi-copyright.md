---
name: topik2-ilkgi-copyright
description: "토픽2 읽기 — 문학 지문 저작권 비공개 문항(96·102) 처리: 안내+정답 카드"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6ef7c53f-3fb0-4912-a320-2be45f2ec0ff
  modified: 2026-07-29T22:00:45.069Z
---

토픽2 읽기 해설집은 유형01~18(1~50번) 전 12회차. 파이프라인 `t2r_build{1..18}.py` + `t2r_raw*/content*` (각 유형 독립 파일). 데이터는 HTML 안 `const ITEMS=[{"hoe":N,"no":M,...}]` 에 임베드(회차 세려면 이걸 파싱).

**★저작권 비공개 문항(2026-07-28 처리)★**: 모의고사 96·102회의 **문학(소설·수필) 지문**은 **공식 문제지 자체가 「저작권 관련 법령에 따라 지문은 공개하지 않습니다 / passage is NOT disclosed」** 안내 박스로 지문을 뺐다(원자료에 지문이 아예 없음 — 지어낼 수 없음). 해당 문항:
- **유형09(23~24, 밑줄 심정)**: 102회
- **유형15(42~43, 한 지문 두 물음)**: 96회·102회

처음엔 이 회차들을 그냥 **제외**했다가(유형09=11회차, 유형15=10회차), 사용자 요청으로 **「안내+정답」 카드**로 채웠다. 카드 = 공식 비공개 안내 박스 + 문항 + 선택지(+영어 뜻) + **공식 정답만 ✓ 초록 표시**, 해설은 없음(지문이 없어 심정·내용일치 근거를 못 씀 — 날조 금지). 비인터랙티브·진도 카운트 제외.

구현: 각 build 에 `WITHHELD=[dict(...withheld=True...)]` 를 메인 루프 뒤 `items += WITHHELD`, JS `renderWithheld()`+`noticeBox()` 분기(`if(it.withheld){renderWithheld(it);return;}`), meta 에 「지문 비공개 N」 표기. 정답 출처=해당 회차 「정답 및 배점표」(이미지→렌더 판독). **원자료 위치: `토픽6급 과정/모의고사/토픽2 NN회/제NN회_문제지…읽기….pdf`(전 쪽 이미지)**. `t2r_survey2324.py` 에 `DROP={102:...}` 로 이미 표시돼 있었음.

교훈: 문학 지문이 「비공개」로 빠진 건 내 실수가 아니라 **공식 원본이 그렇게 배포**된 것. 지문을 다른 데서 가져와 기출인 척 넣지 말 것.

**★읽기 해설 문장별 이중언어(2026-07-28, 사용자 요청)★**: 해설이 「한국어 문단 + 영어 요약 한 덩이」였던 걸 **「한국어 한 문장 / 그 아래 영어 한 줄」**로 바꿈(전 유형01~18). 파이프라인:
1. `t2r_prose_extract.py` — 완성 HTML의 `const ITEMS`에서 실제 렌더 프로즈(sol·rightnote·feel)를 뽑아 `t2r_prose{NN}.json`(hoe→no→field→{ko,en}). 콘텐츠 필드명(sol/sol19/sol23…) 무관하게 추출.
2. 유형당 하위에이전트 1개가 문장별 영어 재번역 → `t2r_pairs{NN}.json`(hoe→no→field→[[ko,en]]). ★한국어는 그대로(낱말 보존 검증: 구두점 뺀 대조), 영어만 1:1 새 번역(기존 요약 재사용 금지). ①②③④·㉠㉢·「」·`<b>` 보존.★
3. `t2r_pairsplit.py` — 한 쌍에 ②③④가 뭉치면 옵션별로 분리(가드: 조각이 **조사(를/을/이/가/은/는/에/도/의/로/와/과/만)로 끝나면** 서술어 공유라 안 쪼갬 → 미완성 방지). hoe→field(옛09) / hoe→no→field(신) 둘 다 처리.
4. `t2r_pairpatch.py` — 빌드에 `const PAIRS` 주입 + `pairHtml`/`gp(it,f)` + `.bip` CSS + 렌더 교체(`${it.sol}<span class=en>…` → 쌍 있으면 pairHtml, 없으면 폴백). **17빌드 앵커 균일**(sol=`<p>`통째, rightnote/feel=안쪽).
5. `t2r_pairs_apply.py` — 검증→분리(1회, `t2r_applied.txt`)→패치→빌드 자동. FIELDS 맵 내장(09/13/15 제외=수동 완료).
검증: 전 1300+쌍 미완성 조각 0 · 낱말 보존 0어긋남 · 유형별 DOM bip>0·JS오류0. **★프로즈는 「이미 만든 HTML」에서 뽑으므로, 콘텐츠(t2r_content*) 바꾸면 재추출·재번역 필요★**.

**★듣기·쓰기도 적용 완료(2026-07-28)★** — ★상세 문서: `_스크립트/README 이중언어 문장쌍.md`★.
- **듣기(유형01~20)**: `t2l_prose_pair.py`(HTML서 sol/solEn 추출 → **auto-pair**: 기존 영어가 완역이라 문장수 맞으면 그대로 짝, 안 맞는 것만 `t2l_unmatched.json`) → 재번역(청크 a/b/c 하위에이전트) → `t2l_merge_repairs.py`(병합·분리·재빌드). 패처 `t2l_pairpatch.py`(★한국어도 esc, gp는 set.hoe/q.no★). **짝문항06~20은 `t2l_pair_build.py` 한 파일**(TP 인자)이라 패치 1번. ★유형06은 raw06 옛형식이라 재빌드 불가 → `t2l_patch06_html.py`로 HTML 직접 패치★.
- **쓰기(51~54)**: `t2w_prose_pair.py`(content서 note/model/alt auto-pair) → 재번역(`t2w_repairs.json`) → 병합. 빌드는 `t2w_build.py` 직접 수정(pairHtmlW/wp, note는 blankAns에 H·qk 인자 추가). ★whyA/whyB는 영어짝 없어 그대로.★
- 최종: 읽기+듣기+쓰기 **3,252쌍 · 미완성 조각 0 · 전 파일 DOM bip>0·JS오류0**. [[haeseol-esc-nae-geul]] [[haeseol-hwagin-an-han-geot]] [[haeseol-yeongeo-jeokdae]] [[topik2-deutgi-source]] [[topik2-sseugi-write]]

**★듣기 대본(대사)도 이중언어 완료(2026-07-30)★** — 해설 말고 **대본(담화 대사)**도 「화자·한국어 문장/그 아래 영어」로. 기존 대본 영어 `lineEn`은 **3인칭 요약**이라 못 씀 → **전량 직역 재번역**(20유형 5청크 하위에이전트 5개, 문장별 1인칭). 파이프라인 `t2l_script_extract.py`(SETS서 turns 추출, key=회차[짝]·회차_번호[앞]) → 병합·검증 `t2l_script_merge.py`(한국어 공백뺀 전수대조) → 패처 `t2l_scriptpatch.py`(SCRIPTPAIRS 주입+`scriptHtml`+`.lnko/.lnen`, 렌더 3종: 앞01 scriptLns / 앞02~05 turnLns+대본블록 repLn·lineEn 별도 / 짝 turnLns) → 재빌드, ★06은 재빌드 불가라 `t2l_scriptpatch06_html.py` 직접(gp가 h2)★ → DOM검증 `t2l_scriptdomcheck.py`(★.lnko/.lnen 셀 때 `<script>` 소스 빼기—scriptHtml 리터럴이 +1★). **2,711 문장쌍·한국어 0어긋남·DOM .lnko==.lnen==데이터·JS오류0**. 정답표시줄(repLn: 이어질말/행동/일치/중심생각)은 대본 뒤 그대로(한국어만). 상세: `_스크립트/README 이중언어 문장쌍.md`.

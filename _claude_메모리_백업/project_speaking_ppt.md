---
name: project_speaking_ppt
description: "말하기 PPT — 500문장 PPTX(문장당 2슬라이드). v3 시제품 완성, PowerShell COM 파이프라인. 다음 = 전체 생산."
metadata: 
  node_type: memory
  type: project
  originSessionId: 243aa644-b2dd-4ec3-97c9-53b3042d0fe5
---

**말하기 PPT 프로젝트**(2026-06-13 시작) = 학생이 현지어(영어)를 보고 한국어로 말하는 연습용 PPTX. [[project_canonical_folder]]의 `말하기_PPT\` 폴더.

**확정 형식 — 문장당 2슬라이드**: ① 문제 = 영어만 + 이모지 삽화 + 하단 힌트(어순 골격) ② 정답 = 영어 작게 + 한국어 특대.

**v3 디자인(시제품 `말하기연습_v3.pptx`, 10장 = 5문장)**:
- 교재 디자인 언어: 연슬레이트 배경(#f1f5f9) + 흰 라운드 카드 + 그림자 + 카드 왼쪽 카테고리색 세로 바(문장구조 파랑 #3b82f6) + 연파랑 알약 칩(번호/단원명)
- 폰트: 영어 60pt **Segoe UI Black** / 한국어 76pt **맑은 고딕 굵게** / 이모지 115pt(Segoe UI Emoji) / 정답 영어 26pt Semibold. 넘침은 TextFrame2.AutoSize=2(자동 축소)
- **마스터 커스텀 레이아웃 2종**("문제 (영어)"/"정답 (영어+한국어)") + 자리표시자(ppPlaceholderBody) 기반 → 보기→슬라이드 마스터에서 폰트·크기 일괄 변경 가능(사용자 요구사항). 테마 글꼴도 연결(영문 Segoe UI/한글 맑은 고딕). 띠·카드·칩·힌트는 레이아웃 소유
- v1(텍스트박스 직접, 마스터 미제어)·v2(자리표시자 1차)는 구버전

**파이프라인(PowerShell COM)**:
- 문장 추출: 레슨 HTML의 `sentence-en">(…)</div>\s*<div class="sentence-kr">(…)` 정규식 — 67레슨 전체 자동 추출 가능
- 생성: `New-Object -ComObject PowerPoint.Application` → CustomLayouts.Add → Shapes.AddPlaceholder(2,…) → Slides.AddSlide(idx,layout) → 자리표시자는 Top 좌표 매칭으로 채움(FillSlide) → SaveAs
- ⚠️ **생성 전 PowerPoint 창 전부 닫기** — 열린 인스턴스와 COM 충돌로 전면 실패. 강제종료(Stop-Process) 직후엔 Presentations.Add가 비정상 반환 가능 → $pp.Visible=-1 + Sleep 후 진단(CustomLayouts.Count 접근) 통과 확인하고 본 실행
- 슬라이드 크기는 기본 16:9(960×540pt) 그대로 사용(PageSetup.SlideWidth는 PS 후기바인딩에서 실패)

**⬜ 다음 단계**: ① 사용자 v3 확인/조정 ② 500문장 전체 생산 — 분할 단위(레슨별 67파일 권장) 결정, 카테고리별 색(파랑/보라/초록/앰버)·단원 라벨·힌트 자동 적용 ③ 문장별 이모지 500개 매핑 데이터 작성 ④ 이미지 폴더 규칙(`삽화\001.png` 있으면 이모지 대신 그림 자동 삽입) ⑤ 다국어: 데이터의 영어 열만 교체해 재생성.

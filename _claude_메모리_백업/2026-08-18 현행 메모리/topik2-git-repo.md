---
name: topik2-git-repo
description: 토픽2는 이번에 자체 git 저장소로 init됨 — 토픽1과 별개. 저장소 경로·커밋법·CRLF
metadata: 
  node_type: memory
  type: project
  originSessionId: 6ef7c53f-3fb0-4912-a320-2be45f2ec0ff
  modified: 2026-08-03T18:32:24.280Z
---

★**토픽2 프로젝트는 2026-08-04에 자체 git 저장소로 처음 init됐다.** 그 전에는 git 추적이 없었고 OneDrive 동기화로만 보관됐다.★

- **토픽1과 별개 저장소다.** git 루트는 각 프로젝트 폴더. 형제 관계라 서로의 저장소 밖이다:
  - `놀라운 한국어 2026/놀라운 한국어 토픽1 해설 _ 클로드/.git` (원래 있던 것 — 이력의 「인수인계」 커밋들은 여기)
  - `놀라운 한국어 2026/놀라운 한국어 토픽2 해설 _ 클로드/.git` (2026-08-04 신설)
  - 상위 `놀라운 한국어 2026/`엔 .git 없음.
- **함정: 툴 셸의 cwd가 토픽1일 수 있다** — `git rev-parse --show-toplevel`이 토픽1을 가리키면 착각한다. 토픽2 작업은 반드시 **`git -C "…/놀라운 한국어 토픽2 해설 _ 클로드"`** 로.
- 설정(토픽2 로컬): `user.name=놀라운 한국어`, `user.email=kkjune2000@gmail.com`, 브랜치 `master`. (전역 config엔 user가 없어 로컬로 넣었다.)
- 첫 커밋 b28efe5 = **3,155파일 전부**(HTML·스크립트·데이터 + mp3·pdf·이미지 원자료까지, 사용자 「전부 포함」 선택).
- ★CRLF: `git add` 때 LF→CRLF 경고가 뜬다(무해, git 정규화). .gitattributes는 아직 없음. [[workflow-args-cr-gotcha]]의 CR 함정과 별개.★
- 커밋은 사용자가 요청할 때만. 인수인계 파일도 이제 이 저장소로 커밋된다.

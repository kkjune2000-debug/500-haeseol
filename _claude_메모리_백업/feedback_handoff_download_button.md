---
name: feedback_handoff_download_button
description: 인수인계 시작 멘트를 만들 때마다 다운로드 버튼이 담긴 HTML 파일도 함께 만들/갱신
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 500ffcd6-3727-4bad-981e-f9e19813f79d
---

"다른 컴에서 작업 이어가기"용 **인수인계 시작 멘트**를 만들거나 갱신할 때는, 채팅 텍스트뿐 아니라 **다운로드 버튼이 있는 HTML 파일**도 함께 생성/갱신할 것.

**Why:** 사용자가 멘트를 매번 손으로 옮기지 않고 버튼으로 받아쓰길 원함("다운로드 받을 수 있는 버튼을 만들어라").

**How to apply:** 파일 = `D:\OneDrive\놀라운 한국어 500 해설집\_인수인계_시작멘트.html` (OneDrive 루트라 어느 컴에서나 열림). 안에 시작 멘트 textarea + **⬇️ 다운로드(.txt) 버튼**(Blob+download) + 📋 복사 버튼 + 체크리스트. 멘트 내용이 바뀌면 textarea와 "최종 업데이트" 날짜를 갱신. [[project_canonical_folder]]

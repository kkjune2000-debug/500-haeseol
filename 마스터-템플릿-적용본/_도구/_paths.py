# -*- coding: utf-8 -*-
r"""공통 경로 — 드라이브 문자에 매이지 않게 자기 위치에서 거슬러 올라간다.

  <저장소>\마스터-템플릿-적용본\_도구\_paths.py   ← 이 파일
  <저장소>\마스터-템플릿-적용본\놀라운 한국어 500문장 해설 최종\  ← BOOK

컴퓨터마다 D:\OneDrive… 이기도 하고 C:\Users\…\OneDrive… 이기도 하므로
경로를 절대 글자로 박아 두지 마십시오.
"""
import os, sys, io

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.dirname(HERE)                      # 마스터-템플릿-적용본
ROOT = os.path.dirname(TEMPLATE)                      # 저장소 뿌리 (git)
BOOK = os.path.join(TEMPLATE, "놀라운 한국어 500문장 해설 최종")
SND = os.path.join(BOOK, "_소리")
# git show 에 쓸 저장소 안쪽 상대 경로 (슬래시)
REL = "마스터-템플릿-적용본/놀라운 한국어 500문장 해설 최종/"

if not os.path.isdir(BOOK):
    raise SystemExit(f"본문 폴더를 찾지 못했습니다: {BOOK}")


def stdout():
    """한글이 깨지지 않는 출력 통로. PowerShell 기본 코드페이지(cp949) 회피."""
    return io.TextIOWrapper(open(sys.stdout.fileno(), "wb", closefd=False),
                            encoding="utf-8")


def enter():
    """본문 폴더로 이동하고 출력 통로를 돌려준다."""
    os.chdir(BOOK)
    return stdout()

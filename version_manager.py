#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
버전 관리 CLI - 게임 패치처럼 버전 전환

사용법:
    python version_manager.py list              # 버전 목록 보기
    python version_manager.py info              # 현재 버전 정보
    python version_manager.py switch v2         # v2로 전환
    python version_manager.py test v2           # v2 테스트 (실제 전송 안함)
"""

import os
import sys
from publishers.telegram_formatters import list_versions, get_version_info


def print_versions():
    """사용 가능한 버전 목록 출력"""
    print("=" * 70)
    print("[Available Telegram Format Versions]")
    print("=" * 70)

    versions = list_versions()
    info = get_version_info()
    current = os.getenv('TELEGRAM_FORMAT_VERSION', 'v1')

    for ver in versions:
        ver_info = info.get(ver, {})
        marker = " <- CURRENT" if ver == current else ""

        print(f"\n[{ver}]{marker}")
        print(f"   Name: {ver_info.get('name', 'N/A')}")
        print(f"   Status: {ver_info.get('status', 'N/A')}")
        print(f"   Description: {ver_info.get('description', 'N/A')}")

    print("\n" + "=" * 70)


def show_current_info():
    """현재 설정 정보"""
    current = os.getenv('TELEGRAM_FORMAT_VERSION', 'v1')
    info = get_version_info()
    ver_info = info.get(current, {})

    print("=" * 70)
    print("[Current Configuration]")
    print("=" * 70)
    print(f"Version: {current}")
    print(f"Name: {ver_info.get('name', 'N/A')}")
    print(f"Status: {ver_info.get('status', 'N/A')}")
    print(f"Description: {ver_info.get('description', 'N/A')}")
    print("=" * 70)


def switch_version(version: str):
    """버전 전환 (환경변수 업데이트)"""
    versions = list_versions()

    if version not in versions:
        print(f"❌ 버전 '{version}'을 찾을 수 없습니다.")
        print(f"   사용 가능한 버전: {', '.join(versions)}")
        return False

    # .env 파일 업데이트
    env_path = '.env'
    lines = []

    # 기존 .env 읽기
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    # TELEGRAM_FORMAT_VERSION 찾아서 교체
    found = False
    new_lines = []
    for line in lines:
        if line.startswith('TELEGRAM_FORMAT_VERSION='):
            new_lines.append(f'TELEGRAM_FORMAT_VERSION={version}\n')
            found = True
        else:
            new_lines.append(line)

    # 없으면 추가
    if not found:
        new_lines.append(f'\nTELEGRAM_FORMAT_VERSION={version}\n')

    # .env 파일 쓰기
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ 버전 전환 완료: {version}")
    print(f"   .env 파일이 업데이트되었습니다.")
    print(f"   다음 실행부터 {version}이 적용됩니다.")
    return True


def test_version(version: str):
    """버전 테스트 (실제 전송 안함)"""
    print(f"[Testing version {version}]")

    try:
        from publishers.telegram_formatters import get_formatter
        formatter = get_formatter(version)

        # 테스트 데이터
        test_article = {
            'title': '테스트 뉴스 제목',
            'date': '2025년 10월 10일',
            'summary': '이것은 테스트 요약입니다.',
            'keywords': ['테스트', '키워드'],
            'easy_explanation': '이것은 쉬운 설명입니다. 테스트용 내용입니다.',
            'coupang_recommendations': [
                {'category': '테스트', 'hook_title': '테스트 상품', 'affiliate_link': 'https://test.com'}
            ],
            'coupang_disclosure': '테스트 준수문구'
        }

        print(f"\n버전 {version} 포맷 미리보기:")
        print("=" * 70)

        # 타이틀 메시지
        if hasattr(formatter, 'format_title_message'):
            title_msg = formatter.format_title_message(test_article)
            print("[타이틀 메시지]")
            print(title_msg)
            print("\n" + "-" * 70 + "\n")

        # 본문 메시지
        messages = formatter.format_article(test_article)
        for i, msg in enumerate(messages, 1):
            print(f"[메시지 {i}]")
            print(msg)
            if i < len(messages):
                print("\n" + "-" * 70 + "\n")

        print("=" * 70)
        print(f"✅ 버전 {version} 테스트 완료!")
        print(f"   총 {len(messages)}개 메시지 생성됨")

    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

    return True


def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python version_manager.py list         # 버전 목록")
        print("  python version_manager.py info         # 현재 버전 정보")
        print("  python version_manager.py switch v2    # 버전 전환")
        print("  python version_manager.py test v2      # 버전 테스트")
        return

    command = sys.argv[1]

    if command == 'list':
        print_versions()
    elif command == 'info':
        show_current_info()
    elif command == 'switch':
        if len(sys.argv) < 3:
            print("❌ 버전을 지정해주세요. 예: python version_manager.py switch v2")
        else:
            switch_version(sys.argv[2])
    elif command == 'test':
        if len(sys.argv) < 3:
            print("❌ 버전을 지정해주세요. 예: python version_manager.py test v2")
        else:
            test_version(sys.argv[2])
    else:
        print(f"❌ 알 수 없는 명령어: {command}")


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
텔레그램 포맷터 버전 관리 시스템

사용법:
    from publishers.telegram_formatters import get_formatter

    formatter = get_formatter('v1')  # 현재 버전
    formatter = get_formatter('v2')  # 실험 버전 (미구현시 에러)
"""

from .v1_basic import TelegramFormatterV1
from .v2_short import TelegramFormatterV2


# 버전 레지스트리
FORMATTERS = {
    'v1': TelegramFormatterV1,
    'v2': TelegramFormatterV2,
    # 'v3': TelegramFormatterV3,
}

# 기본 버전
DEFAULT_VERSION = 'v1'


def get_formatter(version: str = None):
    """
    버전에 맞는 포맷터 반환

    Args:
        version: 버전 문자열 ('v1', 'v2', etc.)
                 None이면 환경변수 또는 기본값 사용

    Returns:
        TelegramFormatter 인스턴스

    Raises:
        ValueError: 존재하지 않는 버전
    """
    if version is None:
        # 환경변수에서 버전 읽기
        import os
        version = os.getenv('TELEGRAM_FORMAT_VERSION', DEFAULT_VERSION)

    if version not in FORMATTERS:
        available = ', '.join(FORMATTERS.keys())
        raise ValueError(
            f"버전 '{version}'을 찾을 수 없습니다.\n"
            f"사용 가능한 버전: {available}"
        )

    formatter_class = FORMATTERS[version]
    return formatter_class()


def list_versions():
    """사용 가능한 모든 버전 리스트"""
    return list(FORMATTERS.keys())


def get_version_info():
    """버전별 설명"""
    info = {
        'v1': {
            'name': 'Basic Format',
            'description': '타이틀 → 이미지 → 텍스트 순서, 마크다운 없음, 쿠팡 1개',
            'status': 'stable'
        },
        'v2': {
            'name': 'Short Format (핵심 3줄)',
            'description': '3줄 요약: 무슨일/내투자/주목점, 10초 읽기, 쿠팡 1개',
            'status': 'experimental'
        },
    }
    return info

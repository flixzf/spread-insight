#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Spread Insight - 메인 실행 스크립트

사용법:
    python main.py              # 스케줄러 시작 (9시/12시/18시 자동 실행)
    python main.py --now        # 즉시 1회 실행
    python main.py --test       # 테스트 모드 (텔레그램 전송 없이 분석만)
"""

import sys
import asyncio
from scheduler import NewsScheduler


def main():
    """메인 실행"""
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    scheduler = NewsScheduler()

    if '--now' in args:
        # 즉시 1회 실행
        print("Running news scraping and sending NOW...\n")
        asyncio.run(scheduler.scrape_and_send())

    elif '--test' in args:
        # 테스트 모드 (TODO: 구현 필요)
        print("Test mode not implemented yet.")
        print("Use: python main.py --now")

    else:
        # 스케줄러 시작 (기본)
        scheduler.start()


if __name__ == '__main__':
    main()

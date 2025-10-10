#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
v2 포맷 미리보기 (실제 전송 없음)
"""

import json
from publishers.telegram_formatters.v2_short import TelegramFormatterV2


def main():
    print("=" * 70)
    print("v2 Short Format Preview")
    print("=" * 70)

    # 실제 데이터 로드
    with open('./data/processed/article_with_coupang.json', 'r', encoding='utf-8') as f:
        article_data = json.load(f)

    formatter = TelegramFormatterV2()

    # 1. 타이틀 메시지
    print("\n[Step 1: Title Message]")
    print("-" * 70)
    title_msg = formatter.format_title_message(article_data)
    print(title_msg)

    # 2. (이미지는 여기 전송)
    print("\n[Step 2: Main Image]")
    print("-" * 70)
    print("(Image would be sent here)")

    # 3. 본문 메시지
    print("\n[Step 3: Content Messages]")
    print("-" * 70)
    messages = formatter.format_article(article_data)

    for i, msg in enumerate(messages, 1):
        if i > 1:
            print("\n" + "-" * 70)
            print(f"[Message {i}]")
            print("-" * 70)
        print(msg)

    print("\n" + "=" * 70)
    print(f"Total: {len(messages)} message(s)")
    print("=" * 70)


if __name__ == '__main__':
    main()

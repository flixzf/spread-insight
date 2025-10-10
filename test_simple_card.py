#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
간단한 카드 생성 + 텔레그램 전송 테스트
타이틀 이미지 1장 + 텍스트 메시지들
"""

import asyncio
import json
from generators.simple_card_generator import SimpleCardGenerator
from publishers.telegram_publisher import TelegramPublisher


async def main():
    print("=" * 70)
    print("간단한 카드 생성 + 텔레그램 전송 테스트")
    print("=" * 70)

    # 1. 분석된 기사 데이터 로드
    print("\n[1] 기사 데이터 로드...")
    try:
        with open('./data/processed/article_with_coupang.json', 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        print(f"   제목: {article_data.get('title', 'N/A')[:50]}...")
    except FileNotFoundError:
        print("   [ERROR] article_with_coupang.json 파일이 없습니다.")
        print("   먼저 test_gemini.py와 test_coupang.py를 실행하세요.")
        return

    # 2. 타이틀 카드 생성
    print("\n[2] 타이틀 카드 생성...")
    generator = SimpleCardGenerator()

    title = article_data.get('title', '경제 뉴스')
    keywords = article_data.get('keywords', [])[:5]  # 최대 5개

    print(f"   제목: {title}")
    print(f"   키워드: {', '.join(keywords)}")

    card_path = generator.create_title_card(title, keywords)
    print(f"   [OK] 카드 생성 완료: {card_path}")

    # 3. 텔레그램 전송
    print("\n[3] 텔레그램 전송...")
    publisher = TelegramPublisher()

    # 연결 테스트
    connected = await publisher.test_connection()
    if not connected:
        print("   [ERROR] 텔레그램 연결 실패")
        return

    # 타이틀 이미지 + 텍스트 전송
    success = await publisher.send_article_with_image(
        article_data=article_data,
        title_image_path=card_path,
        delay=1.0
    )

    if success:
        print("\n[OK] 모든 메시지 전송 완료!")
    else:
        print("\n[FAIL] 전송 실패")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

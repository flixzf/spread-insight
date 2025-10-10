"""
뉴스 카드 생성 + 텔레그램 전송 테스트
"""

import json
import asyncio
from generators.firefly_card_generator import FireflyCardGenerator  # Firefly로 변경
from publishers.telegram_publisher import TelegramPublisher
from utils.config import Config


async def main():
    print("=" * 70)
    print("뉴스 카드 생성 및 텔레그램 전송 (Adobe Firefly)")
    print("=" * 70)

    # 1. 분석된 기사 로드
    print("\n[1단계] 분석된 기사 로드 중...")
    with open('./data/processed/article_with_coupang.json', 'r', encoding='utf-8') as f:
        article_data = json.load(f)

    print(f"[OK] 제목: {article_data.get('title', '')[:50]}...")

    # 2. 카드 생성 (Firefly)
    print("\n[2단계] 이미지 카드 생성 중 (Firefly API)...")
    generator = FireflyCardGenerator()
    card_paths = generator.generate_full_card_set(article_data)

    print(f"\n[OK] {len(card_paths)}개 카드 생성 완료")
    for i, path in enumerate(card_paths, 1):
        print(f"  {i}. {path}")

    # 3. 텔레그램 전송
    print("\n[3단계] 텔레그램으로 카드 전송 중...")
    publisher = TelegramPublisher(
        bot_token=Config.TELEGRAM_BOT_TOKEN,
        chat_id=Config.TELEGRAM_CHAT_ID
    )

    # 카드들을 전송
    try:
        # 첫 번째 카드는 캡션과 함께
        caption = f"*{article_data.get('title', '')}*\n\n"
        caption += " ".join([f"#{kw}" for kw in article_data.get('keywords', [])])

        await publisher.send_photo(card_paths[0], caption=caption)
        print(f"[OK] 메인 카드 전송 완료")

        # 나머지 카드들
        for i, card_path in enumerate(card_paths[1:], 2):
            await publisher.send_photo(card_path)
            print(f"[OK] 카드 {i} 전송 완료")
            await asyncio.sleep(0.5)  # 짧은 지연

        print("\n" + "=" * 70)
        print("Success! 텔레그램에서 확인하세요")
        print("=" * 70)

    except Exception as e:
        print(f"[ERROR] 전송 실패: {e}")


if __name__ == '__main__':
    asyncio.run(main())

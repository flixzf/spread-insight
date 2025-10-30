# -*- coding: utf-8 -*-
"""
시장 현황 텔레그램 발송 모듈
"""

from scrapers.market_data_scraper import MarketDataScraper
from publishers.telegram_publisher import TelegramPublisher
import asyncio


class MarketStatusPublisher:
    """실시간 시장 현황을 텔레그램으로 발송"""

    def __init__(self):
        self.scraper = MarketDataScraper()

    async def send_market_status(self) -> bool:
        """
        실시간 시장 현황을 텔레그램으로 전송

        Returns:
            성공 여부
        """
        try:
            # 시장 데이터 수집
            print("\n[Market Status] 시장 데이터 수집 중...")
            data = self.scraper.get_all_market_data()

            # 데이터 검증
            if not data.get('kospi') and not data.get('exchange_rate'):
                print("[WARNING] 시장 데이터를 가져올 수 없습니다.")
                return False

            # 메시지 포맷팅
            message = self.scraper.format_market_status(data)

            # 텔레그램 전송
            print("[Market Status] 텔레그램 전송 중...")
            publisher = TelegramPublisher()
            success = await publisher.send_simple_message(message)

            if success:
                print("[Market Status] ✅ 시장 현황 전송 완료")
            else:
                print("[Market Status] ❌ 전송 실패")

            return success

        except Exception as e:
            print(f"[ERROR] 시장 현황 발송 실패: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """테스트 실행"""
    print("=" * 70)
    print("Market Status Publisher Test")
    print("=" * 70)

    publisher = MarketStatusPublisher()
    success = await publisher.send_market_status()

    if success:
        print("\n✅ 테스트 성공!")
    else:
        print("\n❌ 테스트 실패")


if __name__ == '__main__':
    asyncio.run(main())

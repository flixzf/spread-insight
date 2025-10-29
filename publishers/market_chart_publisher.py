# -*- coding: utf-8 -*-
"""
시장 차트 텔레그램 발송 모듈
"""

from visualizers.market_chart_generator import MarketChartGenerator
from publishers.telegram_publisher import TelegramPublisher
import asyncio
import os


class MarketChartPublisher:
    """시장 차트를 텔레그램으로 발송"""

    def __init__(self):
        self.generator = MarketChartGenerator()

    async def send_exchange_chart(self, caption: str = "📊 이번 주 환율 흐름") -> bool:
        """
        환율 차트 전송

        Args:
            caption: 차트 캡션

        Returns:
            성공 여부
        """
        try:
            # 차트 생성
            print("[Chart Publisher] 환율 차트 생성 중...")
            chart_path = self.generator.create_weekly_exchange_chart(days=5)

            # 텔레그램 전송
            print("[Chart Publisher] 텔레그램 전송 중...")
            publisher = TelegramPublisher()
            success = await publisher.send_photo(chart_path, caption=caption)

            # 파일 정리
            if os.path.exists(chart_path):
                os.remove(chart_path)

            if success:
                print("[Chart Publisher] ✅ 환율 차트 전송 완료")
            else:
                print("[Chart Publisher] ❌ 환율 차트 전송 실패")

            return success

        except Exception as e:
            print(f"[ERROR] 환율 차트 발송 실패: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def send_kospi_chart(self, caption: str = "📈 이번 주 코스피 지수") -> bool:
        """
        코스피 차트 전송

        Args:
            caption: 차트 캡션

        Returns:
            성공 여부
        """
        try:
            # 차트 생성
            print("[Chart Publisher] 코스피 차트 생성 중...")
            chart_path = self.generator.create_kospi_chart(days=5)

            # 텔레그램 전송
            print("[Chart Publisher] 텔레그램 전송 중...")
            publisher = TelegramPublisher()
            success = await publisher.send_photo(chart_path, caption=caption)

            # 파일 정리
            if os.path.exists(chart_path):
                os.remove(chart_path)

            if success:
                print("[Chart Publisher] ✅ 코스피 차트 전송 완료")
            else:
                print("[Chart Publisher] ❌ 코스피 차트 전송 실패")

            return success

        except Exception as e:
            print(f"[ERROR] 코스피 차트 발송 실패: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def send_daily_summary_chart(self, caption: str = "📊 일일 시장 마감 요약") -> bool:
        """
        일일 종합 차트 전송

        Args:
            caption: 차트 캡션

        Returns:
            성공 여부
        """
        try:
            # 차트 생성
            print("[Chart Publisher] 일일 종합 차트 생성 중...")
            chart_path = self.generator.create_daily_summary_chart()

            # 텔레그램 전송
            print("[Chart Publisher] 텔레그램 전송 중...")
            publisher = TelegramPublisher()
            success = await publisher.send_photo(chart_path, caption=caption)

            # 파일 정리
            if os.path.exists(chart_path):
                os.remove(chart_path)

            if success:
                print("[Chart Publisher] ✅ 일일 종합 차트 전송 완료")
            else:
                print("[Chart Publisher] ❌ 일일 종합 차트 전송 실패")

            return success

        except Exception as e:
            print(f"[ERROR] 일일 종합 차트 발송 실패: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """테스트 실행"""
    print("=" * 70)
    print("Market Chart Publisher Test")
    print("=" * 70)

    publisher = MarketChartPublisher()

    # 환율 차트 전송 테스트
    print("\n1. 환율 차트 전송 테스트...")
    success1 = await publisher.send_exchange_chart()

    # 코스피 차트 전송 테스트
    print("\n2. 코스피 차트 전송 테스트...")
    success2 = await publisher.send_kospi_chart()

    # 일일 종합 차트 전송 테스트
    print("\n3. 일일 종합 차트 전송 테스트...")
    success3 = await publisher.send_daily_summary_chart()

    print("\n" + "=" * 70)
    if all([success1, success2, success3]):
        print("✅ 모든 차트 전송 성공!")
    else:
        print("❌ 일부 차트 전송 실패")


if __name__ == '__main__':
    asyncio.run(main())

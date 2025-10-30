#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
시장 차트 퍼블리셔
- 차트 생성 및 텔레그램 전송
"""

import asyncio
import os
from datetime import datetime
import pytz
from visualizers.market_chart_generator import MarketChartGenerator
from publishers.telegram_publisher import TelegramPublisher


class MarketChartPublisher:
    """시장 차트를 생성하고 텔레그램으로 발송"""

    def __init__(self):
        self.generator = MarketChartGenerator()
        self.kst = pytz.timezone('Asia/Seoul')

    async def send_morning_chart(self) -> bool:
        """
        오전 시장 요약 차트 전송 (14:00 KST)

        Returns:
            성공 여부
        """
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending morning market chart...")
            print(f"{'='*70}\n")

            # 1. 복합 차트 생성
            print("[Step 1] Creating combined chart...")
            chart_path = self.generator.create_combined_chart(days=7)

            if not chart_path:
                print("  [ERROR] Failed to create chart")
                return False

            print(f"  [OK] Chart created: {chart_path}")

            # 2. 캡션 작성
            caption = f"📊 오전 시장 요약\n\n"
            caption += f"주간 흐름을 한눈에!\n"
            caption += f"⏰ {datetime.now(self.kst).strftime('%Y년 %m월 %d일 %H:%M')}"

            # 3. 텔레그램 전송
            print("\n[Step 2] Sending chart to Telegram...")
            publisher = TelegramPublisher()
            success = await publisher.send_photo(
                photo_path=chart_path,
                caption=caption
            )

            # 4. 임시 파일 삭제
            try:
                os.remove(chart_path)
                print(f"  [INFO] Deleted temp file: {chart_path}")
            except:
                pass

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Morning chart sent to Telegram!")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
                return True
            else:
                print(f"\n[ERROR] Failed to send chart to Telegram\n")
                return False

        except Exception as e:
            print(f"\n[ERROR] Morning chart publishing failed: {e}\n")
            import traceback
            traceback.print_exc()
            return False

    async def send_closing_chart(self) -> bool:
        """
        일일 마감 차트 전송 (20:00 KST)

        Returns:
            성공 여부
        """
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending closing market chart...")
            print(f"{'='*70}\n")

            # 1. 복합 차트 생성
            print("[Step 1] Creating combined chart...")
            chart_path = self.generator.create_combined_chart(days=7)

            if not chart_path:
                print("  [ERROR] Failed to create chart")
                return False

            print(f"  [OK] Chart created: {chart_path}")

            # 2. 캡션 작성
            caption = f"📊 장 마감 종합 차트\n\n"
            caption += f"오늘 하루도 수고하셨습니다!\n"
            caption += f"⏰ {datetime.now(self.kst).strftime('%Y년 %m월 %d일 %H:%M')}"

            # 3. 텔레그램 전송
            print("\n[Step 2] Sending chart to Telegram...")
            publisher = TelegramPublisher()
            success = await publisher.send_photo(
                photo_path=chart_path,
                caption=caption
            )

            # 4. 임시 파일 삭제
            try:
                os.remove(chart_path)
                print(f"  [INFO] Deleted temp file: {chart_path}")
            except:
                pass

            # 5. 오래된 차트 정리
            self.generator.cleanup_old_charts(max_age_hours=24)

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Closing chart sent to Telegram!")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
                return True
            else:
                print(f"\n[ERROR] Failed to send chart to Telegram\n")
                return False

        except Exception as e:
            print(f"\n[ERROR] Closing chart publishing failed: {e}\n")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """테스트용 메인 함수"""
    publisher = MarketChartPublisher()

    print("Testing morning chart...")
    await publisher.send_morning_chart()

    print("\n\nTesting closing chart...")
    await publisher.send_closing_chart()


if __name__ == '__main__':
    asyncio.run(main())

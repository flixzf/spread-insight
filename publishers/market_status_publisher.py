#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
시장 상태 퍼블리셔
- 실시간 시장 데이터를 텔레그램으로 전송
"""

import asyncio
from datetime import datetime
import pytz
from scrapers.market_data_scraper import MarketDataScraper
from publishers.telegram_publisher import TelegramPublisher


class MarketStatusPublisher:
    """시장 현황을 텔레그램으로 발송"""

    def __init__(self):
        self.scraper = MarketDataScraper()
        self.kst = pytz.timezone('Asia/Seoul')

    def format_market_status(self, data: dict) -> str:
        """
        시장 데이터를 텔레그램 메시지로 포맷팅

        Args:
            data: get_all_market_data() 결과

        Returns:
            포맷팅된 메시지 문자열
        """
        current_time = datetime.now(self.kst).strftime('%Y년 %m월 %d일 %H:%M')

        # 헤더
        message = f"📈 실시간 시장 현황\n\n"
        message += f"⏰ {current_time}\n\n"

        # 코스피
        if data['kospi']:
            k = data['kospi']
            arrow = "▲" if k['status'] == 'up' else "▼" if k['status'] == 'down' else "━"
            message += f"🇰🇷 코스피: {k['value']:,.2f} ({arrow}{abs(k['change_percent']):.2f}%)\n"
        else:
            message += f"🇰🇷 코스피: 데이터 없음\n"

        # 달러/원 환율
        if data['usdkrw']:
            u = data['usdkrw']
            arrow = "▲" if u['status'] == 'up' else "▼" if u['status'] == 'down' else "━"
            message += f"💱 달러/원: {u['value']:,.2f}원 ({arrow}{abs(u['change']):.2f}원)\n"
        else:
            message += f"💱 달러/원: 데이터 없음\n"

        # 기준금리
        if data['interest_rate']:
            i = data['interest_rate']
            message += f"💰 기준금리: {i['value']}% (보합)\n"
        else:
            message += f"💰 기준금리: 데이터 없음\n"

        # 한마디 코멘트
        message += f"\n💡 오늘의 한마디: "

        if data['kospi'] and data['kospi']['status'] == 'up':
            if data['usdkrw'] and data['usdkrw']['status'] == 'down':
                message += "외국인 매수세 유입 중 🚀"
            else:
                message += "상승세 지속 중 📈"
        elif data['kospi'] and data['kospi']['status'] == 'down':
            message += "조정 국면, 진입 타이밍 주목 👀"
        else:
            message += "안정적인 흐름 유지 중 📊"

        return message

    async def send_market_status(self) -> bool:
        """
        시장 현황 수집 및 텔레그램 전송

        Returns:
            성공 여부
        """
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending market status...")
            print(f"{'='*70}\n")

            # 1. 시장 데이터 수집
            print("[Step 1] Collecting market data...")
            data = self.scraper.get_all_market_data()

            if not data['success']:
                print("  [WARNING] Failed to collect some market data")

            # 2. 메시지 포맷팅
            print("\n[Step 2] Formatting message...")
            message = self.format_market_status(data)
            print(f"Message preview:\n{message[:100]}...\n")

            # 3. 텔레그램 전송
            print("[Step 3] Sending to Telegram...")
            publisher = TelegramPublisher()
            success = await publisher.send_text(message)

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Market status sent to Telegram!")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
                return True
            else:
                print(f"\n[ERROR] Failed to send to Telegram\n")
                return False

        except Exception as e:
            print(f"\n[ERROR] Market status publishing failed: {e}\n")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """테스트용 메인 함수"""
    publisher = MarketStatusPublisher()
    await publisher.send_market_status()


if __name__ == '__main__':
    asyncio.run(main())

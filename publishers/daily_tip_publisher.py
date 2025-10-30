#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
일일 경제 꿀팁 퍼블리셔
- 11:00 KST: 경제 용어 설명
- 16:00 KST: 투자 꿀팁
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Optional, Dict
import pytz
from publishers.telegram_publisher import TelegramPublisher


class DailyTipPublisher:
    """매일 경제 용어와 투자 꿀팁을 텔레그램으로 발송"""

    def __init__(self):
        self.kst = pytz.timezone('Asia/Seoul')

        # JSON 파일 경로
        self.terms_file = os.path.join('data', 'economic_terms.json')
        self.tips_file = os.path.join('data', 'investment_tips.json')

        # 데이터 로드
        self.terms = self._load_terms()
        self.tips = self._load_tips()

    def _load_terms(self) -> list:
        """경제 용어 JSON 로드"""
        try:
            with open(self.terms_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('terms', [])
        except Exception as e:
            print(f"[ERROR] Failed to load economic terms: {e}")
            return []

    def _load_tips(self) -> list:
        """투자 꿀팁 JSON 로드"""
        try:
            with open(self.tips_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tips', [])
        except Exception as e:
            print(f"[ERROR] Failed to load investment tips: {e}")
            return []

    def _get_daily_index(self, total: int) -> int:
        """
        날짜 기반 순환 인덱스 계산

        Args:
            total: 전체 아이템 개수

        Returns:
            오늘의 인덱스 (0 ~ total-1)
        """
        now = datetime.now(self.kst)
        # 연도의 몇 번째 날인지 (1-365/366)
        day_of_year = now.timetuple().tm_yday
        # 순환 인덱스
        return (day_of_year - 1) % total

    def format_economic_term(self, term: Dict) -> str:
        """
        경제 용어를 텔레그램 메시지로 포맷팅

        Args:
            term: 용어 데이터

        Returns:
            포맷팅된 메시지
        """
        message = f"💰 오늘의 경제 용어\n\n"
        message += f'"{term["term"]}"\n\n'
        message += f"{term['definition']}\n\n"
        message += f"{term['explanation']}\n\n"

        if 'example' in term:
            message += f"📌 {term['example']}\n\n"

        message += f"#경제용어 #투자기초"

        return message

    def format_investment_tip(self, tip: Dict) -> str:
        """
        투자 꿀팁을 텔레그램 메시지로 포맷팅

        Args:
            tip: 팁 데이터

        Returns:
            포맷팅된 메시지
        """
        message = f"💡 오늘의 투자 꿀팁\n\n"
        message += f"📚 [{tip['category']}]\n"
        message += f"**{tip['title']}**\n\n"
        message += f"{tip['content']}\n\n"
        message += f"✨ {tip['tip']}\n\n"
        message += f"#투자꿀팁 #{tip['category']}"

        return message

    async def send_economic_term(self) -> bool:
        """
        오늘의 경제 용어 전송 (11:00 KST)

        Returns:
            성공 여부
        """
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending daily economic term...")
            print(f"{'='*70}\n")

            if not self.terms:
                print("[ERROR] No economic terms available")
                return False

            # 오늘의 용어 선택 (순환)
            index = self._get_daily_index(len(self.terms))
            term = self.terms[index]

            print(f"[INFO] Selected term #{index + 1}/{len(self.terms)}: {term['term']}")

            # 메시지 포맷팅
            message = self.format_economic_term(term)
            print(f"\nMessage preview:\n{message[:150]}...\n")

            # 텔레그램 전송
            print("[Step] Sending to Telegram...")
            publisher = TelegramPublisher()
            success = await publisher.send_text(message)

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Economic term sent to Telegram!")
                print(f"Term: {term['term']}")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
                return True
            else:
                print(f"\n[ERROR] Failed to send to Telegram\n")
                return False

        except Exception as e:
            print(f"\n[ERROR] Economic term publishing failed: {e}\n")
            import traceback
            traceback.print_exc()
            return False

    async def send_investment_tip(self) -> bool:
        """
        오늘의 투자 꿀팁 전송 (16:00 KST)

        Returns:
            성공 여부
        """
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending daily investment tip...")
            print(f"{'='*70}\n")

            if not self.tips:
                print("[ERROR] No investment tips available")
                return False

            # 오늘의 팁 선택 (순환)
            index = self._get_daily_index(len(self.tips))
            tip = self.tips[index]

            print(f"[INFO] Selected tip #{index + 1}/{len(self.tips)}: {tip['title']}")

            # 메시지 포맷팅
            message = self.format_investment_tip(tip)
            print(f"\nMessage preview:\n{message[:150]}...\n")

            # 텔레그램 전송
            print("[Step] Sending to Telegram...")
            publisher = TelegramPublisher()
            success = await publisher.send_text(message)

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Investment tip sent to Telegram!")
                print(f"Tip: {tip['title']}")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
                return True
            else:
                print(f"\n[ERROR] Failed to send to Telegram\n")
                return False

        except Exception as e:
            print(f"\n[ERROR] Investment tip publishing failed: {e}\n")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """테스트용 메인 함수"""
    publisher = DailyTipPublisher()

    print("Testing Economic Term:")
    await publisher.send_economic_term()

    print("\n\nTesting Investment Tip:")
    await publisher.send_investment_tip()


if __name__ == '__main__':
    asyncio.run(main())

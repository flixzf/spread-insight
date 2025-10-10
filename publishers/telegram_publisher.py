# -*- coding: utf-8 -*-
import os
import asyncio
from telegram import Bot
from publishers.telegram_formatters import get_formatter


class TelegramPublisher:
    def __init__(self, bot_token: str = None, chat_id: str = None, format_version: str = None):
        """
        텔레그램 퍼블리셔

        Args:
            bot_token: 봇 토큰 (None이면 환경변수 사용)
            chat_id: 채팅 ID (None이면 환경변수 사용)
            format_version: 포맷 버전 ('v1', 'v2', etc. None이면 환경변수 또는 기본값)
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')

        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        if not self.chat_id:
            raise ValueError("TELEGRAM_CHAT_ID not set")

        self.bot = Bot(token=self.bot_token)

        # 버전별 포맷터 선택
        self.format_version = format_version or os.getenv('TELEGRAM_FORMAT_VERSION', 'v1')
        self.formatter = get_formatter(self.format_version)
        print(f"Using Telegram Format: {self.format_version}")
    
    async def send_article(self, article_data: dict, delay: float = 1.0) -> bool:
        try:
            messages = self.formatter.format_article(article_data)
            print(f"Sending {len(messages)} messages...")

            for i, message in enumerate(messages, 1):
                await self.send_message(message, parse_mode=None)
                print(f"Message {i}/{len(messages)} sent")
                if i < len(messages):
                    await asyncio.sleep(delay)

            print("All messages sent!")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    async def send_article_with_image(self, article_data: dict, title_image_path: str = None, delay: float = 3.0) -> bool:
        """
        타이틀 메시지 → 텍스트 내용 순서로 전송 (이미지 제거됨)

        Args:
            article_data: 기사 데이터
            title_image_path: (사용 안 함, 호환성 유지용)
            delay: 메시지 간 딜레이 (초, 기본 3초)

        Returns:
            성공 여부
        """
        try:
            # 1. 타이틀 메시지 전송
            print("Step 1: Sending title message...")
            title_msg = self.formatter.format_title_message(article_data)
            await self.send_message(title_msg, parse_mode=None)
            print("  [OK] Title sent")
            await asyncio.sleep(delay)

            # 2. 텍스트 내용 전송
            print("Step 2: Sending content...")
            messages = self.formatter.format_article(article_data)
            print(f"  Sending {len(messages)} text messages...")

            for i, message in enumerate(messages, 1):
                await self.send_message(message, parse_mode=None)
                print(f"  [OK] Message {i}/{len(messages)} sent")
                if i < len(messages):
                    await asyncio.sleep(delay)

            print("\n[OK] All messages sent!")
            return True
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    async def send_message(self, text: str, parse_mode=None) -> bool:
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode
            )
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    async def send_simple_message(self, text: str) -> bool:
        return await self.send_message(text, parse_mode=None)
    
    async def send_photo(self, photo_path: str, caption: str = None) -> bool:
        """
        사진 전송

        Args:
            photo_path: 이미지 파일 경로
            caption: 캡션 (선택사항)

        Returns:
            성공 여부
        """
        try:
            with open(photo_path, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='Markdown' if caption else None
                )
            return True
        except Exception as e:
            print(f"Photo send error: {e}")
            return False

    async def test_connection(self) -> bool:
        try:
            bot_info = await self.bot.get_me()
            print(f"Bot connected!")
            print(f"  Name: {bot_info.first_name}")
            print(f"  Username: @{bot_info.username}")
            print(f"  Chat ID: {self.chat_id}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

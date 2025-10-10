# -*- coding: utf-8 -*-
"""
Telegram message sending test
"""

import asyncio
import json
from dotenv import load_dotenv
from publishers.telegram_publisher import TelegramPublisher


async def main():
    print("=" * 70)
    print("Spread Insight - Telegram Test")
    print("=" * 70)

    load_dotenv()

    try:
        publisher = TelegramPublisher()
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        print("[!] Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
        return

    print("\n[Step 1] Bot connection test")
    if not await publisher.test_connection():
        print("[ERROR] Connection failed")
        return

    print("\n[Step 2] Sending simple message")
    await publisher.send_simple_message("Test message from Spread Insight!")

    print("\n[Step 3] Reading article data")
    json_path = './data/processed/article_with_coupang.json'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        print(f"[OK] Title: {article_data.get('title', 'N/A')}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_path}")
        return

    print("\n[Step 4] Sending article...")
    success = await publisher.send_article(article_data, delay=1.0)

    if success:
        print("\n" + "=" * 70)
        print("Success! Check Telegram")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("Failed")
        print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())

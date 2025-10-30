#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
뉴스 스크래핑 및 텔레그램 발송 스케줄러

한국시간(KST) 기준:
- 매일 09:00 - 아침 뉴스
- 매일 12:00 - 점심 뉴스
- 매일 18:00 - 저녁 뉴스
"""

import schedule
import time
import asyncio
import json
from datetime import datetime
import pytz

from scrapers.naver_scraper import NaverScraper
from analyzers.ai_news_selector import AINewsSelector
from analyzers.gemini_analyzer import GeminiAnalyzer
from publishers.coupang_partners import CoupangPartners
from publishers.telegram_publisher import TelegramPublisher
from publishers.market_status_publisher import MarketStatusPublisher
from publishers.market_chart_publisher import MarketChartPublisher
from publishers.daily_tip_publisher import DailyTipPublisher


class NewsScheduler:
    """뉴스 자동 스크래핑 및 발송 스케줄러"""

    def __init__(self):
        self.scraper = NaverScraper()
        self.selector = AINewsSelector()
        self.gemini = GeminiAnalyzer()
        self.coupang = CoupangPartners()
        self.daily_tip_publisher = DailyTipPublisher()
        # publisher는 매번 새로 생성 (연결 풀 문제 방지)
        self.kst = pytz.timezone('Asia/Seoul')

    async def scrape_and_send(self):
        """뉴스 스크래핑 → AI 선택 → 분석 → 텔레그램 발송"""
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Starting news scraping and sending...")
            print(f"{'='*70}\n")

            # 1. 뉴스 메타데이터 수집 (빠름)
            print("[Step 1] Collecting article metadata from Naver...")
            metadata_list = self.scraper.get_article_metadata(limit=30)
            print(f"  [OK] Collected {len(metadata_list)} article metadata")

            if not metadata_list:
                print("  [WARNING] No articles found. Skipping...")
                return

            # 2. AI가 메타데이터에서 가장 중요한 뉴스 선택
            print("\n[Step 2] AI selecting most important news from metadata...")
            selected_url = self.selector.select_best_news_from_metadata(metadata_list, verbose=False)

            if not selected_url:
                print("  [ERROR] AI failed to select news. Skipping...")
                return

            # 3. 선택된 뉴스만 본문 스크래핑
            print("\n[Step 3] Scraping full article content...")
            selected_article = self.scraper.scrape_article(selected_url)
            print(f"  [OK] Article scraped: {selected_article.title[:50]}...")

            # 4. Gemini 분석
            print("\n[Step 4] Analyzing with Gemini...")
            selected_article.summary = self.gemini.summarize(selected_article)
            selected_article.easy_explanation = self.gemini.explain_simple(selected_article)
            selected_article.keywords = self.gemini.extract_keywords(selected_article)
            print(f"  [OK] Analysis done")
            print(f"  Keywords: {', '.join(selected_article.keywords)}")

            # 5. 쿠팡 파트너스 추천
            print("\n[Step 5] Generating Coupang recommendations...")
            coupang_data = {
                'title': selected_article.title,
                'content': selected_article.content[:1000],
                'keywords': selected_article.keywords
            }
            recommendations = self.coupang.analyze_and_recommend(coupang_data, max_items=1)
            disclosure = self.coupang.disclosure_text
            print(f"  [OK] {len(recommendations)} products recommended")

            # 5. 데이터 준비
            current_date = datetime.now(self.kst).strftime('%Y년 %m월 %d일')
            article_data = {
                'title': selected_article.title,
                'date': current_date,
                'summary': selected_article.summary,
                'keywords': selected_article.keywords,
                'easy_explanation': selected_article.easy_explanation,
                'coupang_recommendations': recommendations,
                'coupang_disclosure': disclosure
            }

            # 6. 텔레그램 발송 (매번 새 인스턴스 생성)
            print("\n[Step 6] Sending to Telegram...")
            publisher = TelegramPublisher()  # 연결 풀 문제 방지
            success = await publisher.send_article_with_image(article_data)

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] News sent to Telegram!")
                print(f"Time: {current_time}")
                print(f"Title: {selected_article.title}")
                print(f"{'='*70}\n")
            else:
                print(f"\n[ERROR] Failed to send to Telegram\n")

        except Exception as e:
            print(f"\n[ERROR] Scheduler job failed: {e}\n")
            import traceback
            traceback.print_exc()

    async def send_market_status(self):
        """시장 현황 전송 (10시, 15시)"""
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending market status...")
            print(f"{'='*70}\n")

            # 시장 현황 발송
            publisher = MarketStatusPublisher()
            success = await publisher.send_market_status()

            if success:
                print(f"\n{'='*70}")
                print("[SUCCESS] Market status sent!")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
            else:
                print(f"\n[ERROR] Failed to send market status\n")

        except Exception as e:
            print(f"\n[ERROR] Market status job failed: {e}\n")
            import traceback
            traceback.print_exc()

    async def send_market_chart(self, chart_type: str = "daily"):
        """시장 차트 전송 (14시, 20시)"""
        try:
            current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
            print(f"\n{'='*70}")
            print(f"[{current_time}] Sending market chart ({chart_type})...")
            print(f"{'='*70}\n")

            # 차트 발송
            publisher = MarketChartPublisher()

            if chart_type == "daily":
                success = await publisher.send_daily_summary_chart()
            elif chart_type == "exchange":
                success = await publisher.send_exchange_chart()
            elif chart_type == "kospi":
                success = await publisher.send_kospi_chart()
            else:
                success = await publisher.send_daily_summary_chart()

            if success:
                print(f"\n{'='*70}")
                print(f"[SUCCESS] Market chart ({chart_type}) sent!")
                print(f"Time: {current_time}")
                print(f"{'='*70}\n")
            else:
                print(f"\n[ERROR] Failed to send market chart\n")

        except Exception as e:
            print(f"\n[ERROR] Market chart job failed: {e}\n")
            import traceback
            traceback.print_exc()

    def run_job(self):
        """스케줄 작업 실행 (동기 래퍼) - 뉴스 발송"""
        try:
            # 새로운 이벤트 루프 생성 (Pool timeout 방지)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.scrape_and_send())
            loop.close()
        except Exception as e:
            print(f"[ERROR] Job execution failed: {e}")
            import traceback
            traceback.print_exc()

    def run_market_status_job(self):
        """시장 현황 작업 실행 (동기 래퍼)"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.send_market_status())
            loop.close()
        except Exception as e:
            print(f"[ERROR] Market status job execution failed: {e}")
            import traceback
            traceback.print_exc()

    def run_market_chart_job(self):
        """시장 차트 작업 실행 (동기 래퍼)"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.send_market_chart("daily"))
            loop.close()
        except Exception as e:
            print(f"[ERROR] Market chart job execution failed: {e}")
            import traceback
            traceback.print_exc()

    async def send_economic_term(self):
        """경제 용어 전송"""
        try:
            await self.daily_tip_publisher.send_economic_term()
        except Exception as e:
            print(f"[ERROR] Economic term job failed: {e}")
            import traceback
            traceback.print_exc()

    async def send_investment_tip(self):
        """투자 꿀팁 전송"""
        try:
            await self.daily_tip_publisher.send_investment_tip()
        except Exception as e:
            print(f"[ERROR] Investment tip job failed: {e}")
            import traceback
            traceback.print_exc()

    def run_economic_term_job(self):
        """경제 용어 작업 실행 (동기 래퍼)"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.send_economic_term())
            loop.close()
        except Exception as e:
            print(f"[ERROR] Economic term job execution failed: {e}")
            import traceback
            traceback.print_exc()

    def run_investment_tip_job(self):
        """투자 꿀팁 작업 실행 (동기 래퍼)"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.send_investment_tip())
            loop.close()
        except Exception as e:
            print(f"[ERROR] Investment tip job execution failed: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        """스케줄러 시작"""
        print(f"\n{'='*70}")
        print("Spread Insight Scheduler Started")
        print(f"{'='*70}")
        print("📰 News Schedule:")
        print("  - 09:00 KST (00:00 UTC) - Morning news")
        print("  - 12:00 KST (03:00 UTC) - Lunch news")
        print("  - 18:00 KST (09:00 UTC) - Evening news")
        print("\n📈 Market Status Schedule:")
        print("  - 10:00 KST (01:00 UTC) - Market open status")
        print("  - 15:00 KST (06:00 UTC) - Real-time indicators")
        print("\n📊 Market Chart Schedule:")
        print("  - 14:00 KST (05:00 UTC) - Morning market summary chart")
        print("  - 20:00 KST (11:00 UTC) - Daily closing chart")
        print("\n💡 Daily Tips Schedule:")
        print("  - 11:00 KST (02:00 UTC) - Economic term")
        print("  - 16:00 KST (07:00 UTC) - Investment tip")
        print(f"{'='*70}\n")

        # UTC 시간으로 스케줄 등록 (Railway는 UTC 기준)
        # KST = UTC + 9시간

        # 뉴스 스케줄
        schedule.every().day.at("00:00").do(self.run_job)  # 09:00 KST
        schedule.every().day.at("03:00").do(self.run_job)  # 12:00 KST
        schedule.every().day.at("09:00").do(self.run_job)  # 18:00 KST

        # 시장 현황 스케줄
        schedule.every().day.at("01:00").do(self.run_market_status_job)  # 10:00 KST
        schedule.every().day.at("06:00").do(self.run_market_status_job)  # 15:00 KST

        # 시장 차트 스케줄
        schedule.every().day.at("05:00").do(self.run_market_chart_job)  # 14:00 KST
        schedule.every().day.at("11:00").do(self.run_market_chart_job)  # 20:00 KST

        # 경제 꿀팁 스케줄 (Phase 2B)
        schedule.every().day.at("02:00").do(self.run_economic_term_job)  # 11:00 KST - 경제 용어
        schedule.every().day.at("07:00").do(self.run_investment_tip_job)  # 16:00 KST - 투자 꿀팁

        # 현재 시간 출력
        current_time = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S KST')
        print(f"Current time: {current_time}")
        print("Waiting for scheduled time...\n")

        # 무한 루프로 스케줄 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크


def main():
    """메인 실행"""
    scheduler = NewsScheduler()
    scheduler.start()


if __name__ == '__main__':
    main()

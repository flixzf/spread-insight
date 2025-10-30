#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
시장 데이터 스크래퍼
- 코스피 지수
- 달러/원 환율
- 기준금리
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional


class MarketDataScraper:
    """실시간 시장 데이터 수집"""

    def __init__(self):
        # 티커 심볼
        self.kospi_ticker = "^KS11"  # 코스피 지수
        self.usdkrw_ticker = "KRW=X"  # 달러/원 환율

    def get_kospi_data(self) -> Optional[Dict]:
        """
        코스피 지수 및 등락률 조회

        Returns:
            {
                'value': 2650.5,
                'change': 20.5,
                'change_percent': 0.78,
                'status': 'up' or 'down' or 'flat'
            }
        """
        try:
            ticker = yf.Ticker(self.kospi_ticker)
            hist = ticker.history(period="2d")

            if len(hist) < 1:
                return None

            current = hist['Close'].iloc[-1]

            # 전일 종가가 있으면 등락률 계산
            if len(hist) >= 2:
                previous = hist['Close'].iloc[-2]
                change = current - previous
                change_percent = (change / previous) * 100
            else:
                change = 0
                change_percent = 0

            # 상태 판단
            if change > 0:
                status = 'up'
            elif change < 0:
                status = 'down'
            else:
                status = 'flat'

            return {
                'value': round(current, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'status': status
            }

        except Exception as e:
            print(f"[ERROR] Failed to fetch KOSPI data: {e}")
            return None

    def get_exchange_rate(self) -> Optional[Dict]:
        """
        달러/원 환율 및 변동폭 조회

        Returns:
            {
                'value': 1320.5,
                'change': -5.0,
                'change_percent': -0.38,
                'status': 'up' or 'down' or 'flat'
            }
        """
        try:
            ticker = yf.Ticker(self.usdkrw_ticker)
            hist = ticker.history(period="2d")

            if len(hist) < 1:
                return None

            current = hist['Close'].iloc[-1]

            # 전일 종가가 있으면 등락 계산
            if len(hist) >= 2:
                previous = hist['Close'].iloc[-2]
                change = current - previous
                change_percent = (change / previous) * 100
            else:
                change = 0
                change_percent = 0

            # 상태 판단 (환율은 상승=원화약세, 하락=원화강세)
            if change > 0:
                status = 'up'
            elif change < 0:
                status = 'down'
            else:
                status = 'flat'

            return {
                'value': round(current, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'status': status
            }

        except Exception as e:
            print(f"[ERROR] Failed to fetch USD/KRW data: {e}")
            return None

    def get_interest_rate(self) -> Optional[Dict]:
        """
        한국 기준금리 조회

        Note:
            실시간 API가 없어서 최근 발표된 금리를 사용
            한국은행 금리는 자주 변경되지 않으므로 하드코딩 또는 캐싱 가능

        Returns:
            {
                'value': 3.5,
                'last_updated': '2025-10-01'
            }
        """
        try:
            # TODO: 한국은행 API 연동 또는 웹 스크래핑
            # 현재는 최근 공지된 기준금리를 하드코딩
            # 추후 한국은행 경제통계시스템(ECOS) API 활용 가능

            return {
                'value': 3.5,  # 2025년 10월 기준 (예시)
                'last_updated': '2025-10-01',
                'note': '한국은행 기준금리'
            }

        except Exception as e:
            print(f"[ERROR] Failed to fetch interest rate: {e}")
            return None

    def get_all_market_data(self) -> Dict:
        """
        모든 시장 데이터를 한번에 조회

        Returns:
            {
                'kospi': {...},
                'usdkrw': {...},
                'interest_rate': {...},
                'timestamp': '2025-10-30 15:30:00'
            }
        """
        try:
            kospi = self.get_kospi_data()
            usdkrw = self.get_exchange_rate()
            interest_rate = self.get_interest_rate()

            return {
                'kospi': kospi,
                'usdkrw': usdkrw,
                'interest_rate': interest_rate,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'success': all([kospi, usdkrw, interest_rate])
            }

        except Exception as e:
            print(f"[ERROR] Failed to get market data: {e}")
            return {
                'kospi': None,
                'usdkrw': None,
                'interest_rate': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'success': False
            }

    def get_historical_data(self, ticker: str, days: int = 7) -> Optional[Dict]:
        """
        과거 데이터 조회 (차트용)

        Args:
            ticker: 티커 심볼 ('kospi' or 'usdkrw')
            days: 조회 기간 (일)

        Returns:
            {
                'dates': ['2025-10-24', ...],
                'values': [2600.5, 2615.3, ...]
            }
        """
        try:
            symbol = self.kospi_ticker if ticker == 'kospi' else self.usdkrw_ticker

            yf_ticker = yf.Ticker(symbol)
            hist = yf_ticker.history(period=f"{days}d")

            if hist.empty:
                return None

            dates = [d.strftime('%Y-%m-%d') for d in hist.index]
            values = hist['Close'].tolist()

            return {
                'dates': dates,
                'values': values
            }

        except Exception as e:
            print(f"[ERROR] Failed to get historical data for {ticker}: {e}")
            return None


def main():
    """테스트용 메인 함수"""
    scraper = MarketDataScraper()

    print("=" * 70)
    print("Market Data Scraper Test")
    print("=" * 70)

    # 전체 데이터 조회
    data = scraper.get_all_market_data()

    print("\n📈 KOSPI:")
    if data['kospi']:
        k = data['kospi']
        print(f"  Value: {k['value']:,.2f}")
        print(f"  Change: {k['change']:+.2f} ({k['change_percent']:+.2f}%)")
        print(f"  Status: {k['status']}")
    else:
        print("  Failed to fetch")

    print("\n💱 USD/KRW:")
    if data['usdkrw']:
        u = data['usdkrw']
        print(f"  Value: {u['value']:,.2f}원")
        print(f"  Change: {u['change']:+.2f}원 ({u['change_percent']:+.2f}%)")
        print(f"  Status: {u['status']}")
    else:
        print("  Failed to fetch")

    print("\n💰 Interest Rate:")
    if data['interest_rate']:
        i = data['interest_rate']
        print(f"  Value: {i['value']}%")
        print(f"  Updated: {i['last_updated']}")
    else:
        print("  Failed to fetch")

    print(f"\n⏰ Timestamp: {data['timestamp']}")
    print("=" * 70)


if __name__ == '__main__':
    main()

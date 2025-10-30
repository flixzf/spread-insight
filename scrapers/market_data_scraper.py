# -*- coding: utf-8 -*-
"""
실시간 시장 데이터 스크래퍼

코스피, 환율, 금리 등 주요 경제 지표를 실시간으로 수집
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup

# pykrx 추가 (한국거래소 공식 데이터)
try:
    from pykrx import stock
    PYKRX_AVAILABLE = True
except ImportError:
    PYKRX_AVAILABLE = False
    print("[WARNING] pykrx not available, falling back to yfinance")


class MarketDataScraper:
    """실시간 시장 데이터 수집"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_kospi_data(self) -> Optional[Dict]:
        """
        코스피 지수 및 등락률 조회

        Returns:
            {'price': float, 'change': float, 'change_percent': float, 'status': str}
            status: 'up', 'down', 'flat'
        """
        try:
            # pykrx 우선 사용 (한국거래소 공식 데이터)
            if PYKRX_AVAILABLE:
                try:
                    today = datetime.now().strftime("%Y%m%d")
                    yesterday = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")

                    # 코스피 지수 데이터 가져오기
                    df = stock.get_index_ohlcv_by_date(yesterday, today, "1001")  # 1001 = KOSPI

                    if not df.empty and len(df) >= 2:
                        current_price = df['종가'].iloc[-1]
                        previous_close = df['종가'].iloc[-2]

                        change = current_price - previous_close
                        change_percent = (change / previous_close) * 100 if previous_close else 0

                        status = 'up' if change > 0 else 'down' if change < 0 else 'flat'

                        return {
                            'price': round(current_price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_percent, 2),
                            'status': status
                        }
                except Exception as pykrx_error:
                    print(f"[WARNING] pykrx KOSPI 조회 실패, yfinance로 재시도: {pykrx_error}")

            # yfinance fallback
            ticker = yf.Ticker("^KS11")
            data = ticker.history(period="1d")

            if data.empty:
                # 대체 티커 시도
                ticker = yf.Ticker("^KOSPI")
                data = ticker.history(period="1d")

            if data.empty:
                return None

            current_price = data['Close'].iloc[-1]
            previous_close = ticker.info.get('previousClose', current_price)

            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close else 0

            status = 'up' if change > 0 else 'down' if change < 0 else 'flat'

            return {
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'status': status
            }

        except Exception as e:
            print(f"[ERROR] KOSPI 데이터 조회 실패: {e}")
            return None

    def get_exchange_rate(self) -> Optional[Dict]:
        """
        달러/원 환율 조회

        Returns:
            {'rate': float, 'change': float, 'status': str}
        """
        try:
            # 네이버 금융에서 환율 스크래핑 (더 안정적)
            try:
                url = "https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW"
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # 현재 환율
                rate_elem = soup.select_one('.rate_value')
                if rate_elem:
                    current_rate = float(rate_elem.text.replace(',', ''))

                    # 전일 대비
                    change_elem = soup.select_one('.change_value')
                    if change_elem:
                        change = float(change_elem.text.replace(',', ''))
                    else:
                        change = 0

                    status = 'up' if change > 0 else 'down' if change < 0 else 'flat'

                    return {
                        'rate': round(current_rate, 2),
                        'change': round(change, 2),
                        'status': status
                    }
            except Exception as naver_error:
                print(f"[WARNING] 네이버 환율 조회 실패, yfinance로 재시도: {naver_error}")

            # yfinance fallback
            ticker = yf.Ticker("KRW=X")
            data = ticker.history(period="1d")

            if data.empty:
                return None

            current_rate = data['Close'].iloc[-1]
            previous_close = ticker.info.get('previousClose', current_rate)

            change = current_rate - previous_close
            status = 'up' if change > 0 else 'down' if change < 0 else 'flat'

            return {
                'rate': round(current_rate, 2),
                'change': round(change, 2),
                'status': status
            }

        except Exception as e:
            print(f"[ERROR] 환율 데이터 조회 실패: {e}")
            return None

    def get_interest_rate(self) -> Optional[Dict]:
        """
        한국 기준금리 조회 (한국은행 웹 스크래핑)

        Returns:
            {'rate': float, 'status': str}
        """
        try:
            # 네이버 금융에서 기준금리 정보 스크래핑
            url = "https://finance.naver.com/marketindex/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 기준금리는 고정값으로 반환 (실시간 API 없음)
            # 대신 최근 발표된 금리 사용
            # TODO: 한국은행 공식 API 연동 고려

            return {
                'rate': 3.5,  # 2024년 기준 (수동 업데이트 필요)
                'status': 'flat'
            }

        except Exception as e:
            print(f"[ERROR] 금리 데이터 조회 실패: {e}")
            return {
                'rate': 3.5,
                'status': 'flat'
            }

    def get_all_market_data(self) -> Dict:
        """
        모든 시장 데이터를 한 번에 조회

        Returns:
            {
                'kospi': {...},
                'exchange_rate': {...},
                'interest_rate': {...},
                'timestamp': str
            }
        """
        return {
            'kospi': self.get_kospi_data(),
            'exchange_rate': self.get_exchange_rate(),
            'interest_rate': self.get_interest_rate(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def format_market_status(self, data: Dict) -> str:
        """
        시장 데이터를 텔레그램 메시지 형식으로 포맷팅

        Args:
            data: get_all_market_data() 결과

        Returns:
            포맷팅된 문자열
        """
        lines = ["📈 실시간 시장 현황\n"]

        # 코스피
        if data.get('kospi'):
            kospi = data['kospi']
            symbol = "▲" if kospi['status'] == 'up' else "▼" if kospi['status'] == 'down' else "━"
            lines.append(
                f"• 코스피: {kospi['price']:,.2f} "
                f"({symbol}{abs(kospi['change_percent'])}%)"
            )

        # 환율
        if data.get('exchange_rate'):
            ex = data['exchange_rate']
            symbol = "▲" if ex['status'] == 'up' else "▼" if ex['status'] == 'down' else "━"
            lines.append(
                f"• 달러/원: {ex['rate']:,.2f}원 "
                f"({symbol}{abs(ex['change']):.2f}원)"
            )

        # 금리
        if data.get('interest_rate'):
            ir = data['interest_rate']
            lines.append(f"• 기준금리: {ir['rate']}% (보합)")

        # 타임스탬프
        lines.append(f"\n⏰ {data['timestamp']}")

        # 한마디 코멘트
        if data.get('kospi'):
            if data['kospi']['status'] == 'up':
                lines.append("\n💡 오늘의 한마디: 상승세 지속 중!")
            elif data['kospi']['status'] == 'down':
                lines.append("\n💡 오늘의 한마디: 조정 국면 진입")
            else:
                lines.append("\n💡 오늘의 한마디: 보합세 유지")

        return "\n".join(lines)


def main():
    """테스트 실행"""
    scraper = MarketDataScraper()

    print("=" * 60)
    print("Market Data Scraper Test")
    print("=" * 60)

    # 전체 데이터 조회
    data = scraper.get_all_market_data()

    # 포맷팅된 메시지 출력
    message = scraper.format_market_status(data)
    print("\n" + message)

    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()

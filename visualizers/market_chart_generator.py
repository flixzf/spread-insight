# -*- coding: utf-8 -*-
"""
시장 차트 생성기

환율, 코스피 등의 주간/일간 차트를 생성하여 텔레그램으로 전송
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import yfinance as yf


class MarketChartGenerator:
    """시장 차트 생성"""

    def __init__(self, output_dir: str = "./data/charts"):
        """
        Args:
            output_dir: 차트 이미지 저장 경로
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 한글 폰트 설정
        self._setup_korean_font()

        # 차트 스타일 설정
        plt.style.use('seaborn-v0_8-darkgrid')

    def _setup_korean_font(self):
        """한글 폰트 설정 (OS별)"""
        system = platform.system()

        if system == 'Windows':
            font_path = 'C:/Windows/Fonts/malgun.ttf'
        elif system == 'Linux':
            font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        elif system == 'Darwin':  # macOS
            font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
        else:
            font_path = None

        if font_path and os.path.exists(font_path):
            try:
                font_prop = fm.FontProperties(fname=font_path)
                plt.rcParams['font.family'] = font_prop.get_name()
            except Exception:
                pass

        # 마이너스 기호 깨짐 방지
        plt.rcParams['axes.unicode_minus'] = False

    def create_weekly_exchange_chart(
        self,
        days: int = 5,
        save_path: Optional[str] = None
    ) -> str:
        """
        주간 환율 차트 생성

        Args:
            days: 표시할 일수 (기본 5일)
            save_path: 저장 경로 (None이면 자동 생성)

        Returns:
            생성된 차트 파일 경로
        """
        try:
            # 환율 데이터 가져오기
            ticker = yf.Ticker("KRW=X")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+2)  # 여유분

            data = ticker.history(start=start_date, end=end_date)

            if data.empty:
                raise ValueError("환율 데이터를 가져올 수 없습니다.")

            # 차트 생성
            fig, ax = plt.subplots(figsize=(10, 6))

            dates = data.index[-days:]
            prices = data['Close'].iloc[-days:]

            # 라인 차트
            ax.plot(dates, prices, marker='o', linewidth=2, markersize=8, color='#4CAF50')

            # 데이터 레이블
            for i, (date, price) in enumerate(zip(dates, prices)):
                ax.annotate(
                    f"{price:.1f}",
                    xy=(date, price),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=10,
                    fontweight='bold'
                )

            # 차트 스타일링
            ax.set_title('📊 이번 주 환율 흐름 (달러/원)', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('날짜', fontsize=12)
            ax.set_ylabel('환율 (원)', fontsize=12)
            ax.grid(True, alpha=0.3)

            # 날짜 포맷
            date_labels = [d.strftime('%m/%d') for d in dates]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(date_labels)

            # 추세 표시
            if len(prices) >= 2:
                trend = "⬇ 하락 추세" if prices.iloc[-1] < prices.iloc[0] else "⬆ 상승 추세"
                ax.text(
                    0.5, 0.02, trend,
                    transform=ax.transAxes,
                    ha='center',
                    fontsize=14,
                    fontweight='bold',
                    color='red' if '⬇' in trend else 'green'
                )

            plt.tight_layout()

            # 저장
            if not save_path:
                save_path = os.path.join(self.output_dir, f"exchange_rate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"[Chart] 환율 차트 생성 완료: {save_path}")
            return save_path

        except Exception as e:
            print(f"[ERROR] 환율 차트 생성 실패: {e}")
            plt.close()
            raise

    def create_kospi_chart(
        self,
        days: int = 5,
        save_path: Optional[str] = None
    ) -> str:
        """
        주간 코스피 차트 생성

        Args:
            days: 표시할 일수
            save_path: 저장 경로

        Returns:
            생성된 차트 파일 경로
        """
        try:
            # 코스피 데이터 가져오기
            ticker = yf.Ticker("^KS11")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+2)

            data = ticker.history(start=start_date, end=end_date)

            if data.empty:
                raise ValueError("코스피 데이터를 가져올 수 없습니다.")

            # 차트 생성
            fig, ax = plt.subplots(figsize=(10, 6))

            dates = data.index[-days:]
            prices = data['Close'].iloc[-days:]

            # 라인 차트
            ax.plot(dates, prices, marker='o', linewidth=2, markersize=8, color='#2196F3')

            # 데이터 레이블
            for i, (date, price) in enumerate(zip(dates, prices)):
                ax.annotate(
                    f"{price:.0f}",
                    xy=(date, price),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=10,
                    fontweight='bold'
                )

            # 차트 스타일링
            ax.set_title('📈 이번 주 코스피 지수', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('날짜', fontsize=12)
            ax.set_ylabel('지수', fontsize=12)
            ax.grid(True, alpha=0.3)

            # 날짜 포맷
            date_labels = [d.strftime('%m/%d') for d in dates]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(date_labels)

            # 추세 표시
            if len(prices) >= 2:
                change_pct = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
                trend = f"⬇ 주간 {abs(change_pct):.2f}% 하락" if change_pct < 0 else f"⬆ 주간 {change_pct:.2f}% 상승"
                ax.text(
                    0.5, 0.02, trend,
                    transform=ax.transAxes,
                    ha='center',
                    fontsize=14,
                    fontweight='bold',
                    color='red' if '⬇' in trend else 'green'
                )

            plt.tight_layout()

            # 저장
            if not save_path:
                save_path = os.path.join(self.output_dir, f"kospi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"[Chart] 코스피 차트 생성 완료: {save_path}")
            return save_path

        except Exception as e:
            print(f"[ERROR] 코스피 차트 생성 실패: {e}")
            plt.close()
            raise

    def create_daily_summary_chart(self, save_path: Optional[str] = None) -> str:
        """
        일일 종합 차트 (환율 + 코스피)

        Returns:
            생성된 차트 파일 경로
        """
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            days = 5

            # 1. 환율 차트
            ticker_krw = yf.Ticker("KRW=X")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+2)
            data_krw = ticker_krw.history(start=start_date, end=end_date)

            if not data_krw.empty:
                dates_krw = data_krw.index[-days:]
                prices_krw = data_krw['Close'].iloc[-days:]

                ax1.plot(dates_krw, prices_krw, marker='o', linewidth=2, color='#4CAF50')
                ax1.set_title('환율 (달러/원)', fontsize=14, fontweight='bold')
                ax1.set_xlabel('날짜', fontsize=10)
                ax1.grid(True, alpha=0.3)

                date_labels_krw = [d.strftime('%m/%d') for d in dates_krw]
                ax1.set_xticks(range(len(dates_krw)))
                ax1.set_xticklabels(date_labels_krw)

            # 2. 코스피 차트
            ticker_kospi = yf.Ticker("^KS11")
            data_kospi = ticker_kospi.history(start=start_date, end=end_date)

            if not data_kospi.empty:
                dates_kospi = data_kospi.index[-days:]
                prices_kospi = data_kospi['Close'].iloc[-days:]

                ax2.plot(dates_kospi, prices_kospi, marker='o', linewidth=2, color='#2196F3')
                ax2.set_title('코스피 지수', fontsize=14, fontweight='bold')
                ax2.set_xlabel('날짜', fontsize=10)
                ax2.grid(True, alpha=0.3)

                date_labels_kospi = [d.strftime('%m/%d') for d in dates_kospi]
                ax2.set_xticks(range(len(dates_kospi)))
                ax2.set_xticklabels(date_labels_kospi)

            plt.suptitle('📊 일일 시장 마감 요약', fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()

            # 저장
            if not save_path:
                save_path = os.path.join(self.output_dir, f"daily_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"[Chart] 일일 종합 차트 생성 완료: {save_path}")
            return save_path

        except Exception as e:
            print(f"[ERROR] 일일 종합 차트 생성 실패: {e}")
            plt.close()
            raise


def main():
    """테스트 실행"""
    print("=" * 70)
    print("Market Chart Generator Test")
    print("=" * 70)

    generator = MarketChartGenerator()

    try:
        # 1. 환율 차트
        print("\n1. 환율 차트 생성 중...")
        exchange_chart = generator.create_weekly_exchange_chart(days=5)
        print(f"✅ 생성 완료: {exchange_chart}")

        # 2. 코스피 차트
        print("\n2. 코스피 차트 생성 중...")
        kospi_chart = generator.create_kospi_chart(days=5)
        print(f"✅ 생성 완료: {kospi_chart}")

        # 3. 일일 종합
        print("\n3. 일일 종합 차트 생성 중...")
        summary_chart = generator.create_daily_summary_chart()
        print(f"✅ 생성 완료: {summary_chart}")

        print("\n" + "=" * 70)
        print("✅ 모든 차트 생성 완료!")

    except Exception as e:
        print(f"\n❌ 차트 생성 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

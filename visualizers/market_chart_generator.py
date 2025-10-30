#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
시장 데이터 차트 생성기
- matplotlib 기반 차트 생성
- 텔레그램 전송용 이미지 생성
"""

import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경용

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import Optional, Tuple
import os
from scrapers.market_data_scraper import MarketDataScraper


class MarketChartGenerator:
    """시장 데이터 차트 생성"""

    def __init__(self):
        self.scraper = MarketDataScraper()
        self.output_dir = "temp_charts"

        # 출력 디렉토리 생성
        os.makedirs(self.output_dir, exist_ok=True)

        # 한글 폰트 설정 (fallback 처리)
        self._setup_font()

    def _setup_font(self):
        """한글 폰트 설정 (Railway 환경 고려)"""
        try:
            # 시스템에 한글 폰트가 있으면 사용
            plt.rcParams['font.family'] = 'DejaVu Sans'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            # 없으면 기본 폰트 사용 (영문으로 대체)
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['axes.unicode_minus'] = False

    def create_weekly_exchange_chart(self, days: int = 7) -> Optional[str]:
        """
        주간 환율 차트 생성

        Args:
            days: 조회 기간 (일)

        Returns:
            생성된 차트 파일 경로
        """
        try:
            # 데이터 수집
            data = self.scraper.get_historical_data('usdkrw', days=days)
            if not data:
                print("[ERROR] No historical data for USD/KRW")
                return None

            # 차트 생성
            fig, ax = plt.subplots(figsize=(10, 6))

            dates = [datetime.strptime(d, '%Y-%m-%d') for d in data['dates']]
            values = data['values']

            ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='#2E86DE')
            ax.fill_between(dates, values, alpha=0.3, color='#2E86DE')

            # 차트 스타일링
            ax.set_title('USD/KRW Weekly Trend', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('KRW', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')

            # X축 날짜 포맷
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.xticks(rotation=45)

            # 최신 값 표시
            if len(values) > 0:
                latest_value = values[-1]
                ax.text(dates[-1], latest_value, f'{latest_value:,.0f}',
                       ha='left', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()

            # 파일 저장
            filepath = os.path.join(self.output_dir, f'usdkrw_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"[ERROR] Failed to create USD/KRW chart: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_weekly_kospi_chart(self, days: int = 7) -> Optional[str]:
        """
        주간 코스피 차트 생성

        Args:
            days: 조회 기간 (일)

        Returns:
            생성된 차트 파일 경로
        """
        try:
            # 데이터 수집
            data = self.scraper.get_historical_data('kospi', days=days)
            if not data:
                print("[ERROR] No historical data for KOSPI")
                return None

            # 차트 생성
            fig, ax = plt.subplots(figsize=(10, 6))

            dates = [datetime.strptime(d, '%Y-%m-%d') for d in data['dates']]
            values = data['values']

            ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='#E74C3C')
            ax.fill_between(dates, values, alpha=0.3, color='#E74C3C')

            # 차트 스타일링
            ax.set_title('KOSPI Weekly Trend', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Index', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')

            # X축 날짜 포맷
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.xticks(rotation=45)

            # 최신 값 표시
            if len(values) > 0:
                latest_value = values[-1]
                ax.text(dates[-1], latest_value, f'{latest_value:,.0f}',
                       ha='left', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()

            # 파일 저장
            filepath = os.path.join(self.output_dir, f'kospi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"[ERROR] Failed to create KOSPI chart: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_combined_chart(self, days: int = 7) -> Optional[str]:
        """
        환율 + 코스피 복합 차트 생성

        Args:
            days: 조회 기간 (일)

        Returns:
            생성된 차트 파일 경로
        """
        try:
            # 데이터 수집
            usdkrw_data = self.scraper.get_historical_data('usdkrw', days=days)
            kospi_data = self.scraper.get_historical_data('kospi', days=days)

            if not usdkrw_data or not kospi_data:
                print("[ERROR] Failed to get historical data")
                return None

            # 차트 생성 (2개의 서브플롯)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

            # 1. 환율 차트
            dates1 = [datetime.strptime(d, '%Y-%m-%d') for d in usdkrw_data['dates']]
            values1 = usdkrw_data['values']

            ax1.plot(dates1, values1, marker='o', linewidth=2, markersize=5, color='#2E86DE')
            ax1.fill_between(dates1, values1, alpha=0.3, color='#2E86DE')
            ax1.set_title('USD/KRW', fontsize=14, fontweight='bold')
            ax1.set_ylabel('KRW', fontsize=11)
            ax1.grid(True, alpha=0.3, linestyle='--')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

            # 최신 값 표시
            if len(values1) > 0:
                ax1.text(dates1[-1], values1[-1], f'{values1[-1]:,.0f}',
                        ha='left', va='bottom', fontsize=9, fontweight='bold')

            # 2. 코스피 차트
            dates2 = [datetime.strptime(d, '%Y-%m-%d') for d in kospi_data['dates']]
            values2 = kospi_data['values']

            ax2.plot(dates2, values2, marker='o', linewidth=2, markersize=5, color='#E74C3C')
            ax2.fill_between(dates2, values2, alpha=0.3, color='#E74C3C')
            ax2.set_title('KOSPI', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Date', fontsize=11)
            ax2.set_ylabel('Index', fontsize=11)
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

            # 최신 값 표시
            if len(values2) > 0:
                ax2.text(dates2[-1], values2[-1], f'{values2[-1]:,.0f}',
                        ha='left', va='bottom', fontsize=9, fontweight='bold')

            # 전체 제목
            fig.suptitle(f'Market Summary ({datetime.now().strftime("%Y-%m-%d")})',
                        fontsize=16, fontweight='bold', y=0.995)

            plt.tight_layout()

            # 파일 저장
            filepath = os.path.join(self.output_dir, f'combined_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"[ERROR] Failed to create combined chart: {e}")
            import traceback
            traceback.print_exc()
            return None

    def cleanup_old_charts(self, max_age_hours: int = 24):
        """
        오래된 차트 파일 삭제

        Args:
            max_age_hours: 보관 기간 (시간)
        """
        try:
            import time
            now = time.time()
            cutoff = now - (max_age_hours * 3600)

            for filename in os.listdir(self.output_dir):
                filepath = os.path.join(self.output_dir, filename)
                if os.path.isfile(filepath):
                    if os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
                        print(f"[INFO] Deleted old chart: {filename}")

        except Exception as e:
            print(f"[ERROR] Failed to cleanup old charts: {e}")


def main():
    """테스트용 메인 함수"""
    generator = MarketChartGenerator()

    print("=" * 70)
    print("Market Chart Generator Test")
    print("=" * 70)

    # 1. 환율 차트
    print("\n[1] Creating USD/KRW chart...")
    usdkrw_chart = generator.create_weekly_exchange_chart()
    if usdkrw_chart:
        print(f"  [OK] Saved to: {usdkrw_chart}")
    else:
        print("  [FAIL] Failed to create chart")

    # 2. 코스피 차트
    print("\n[2] Creating KOSPI chart...")
    kospi_chart = generator.create_weekly_kospi_chart()
    if kospi_chart:
        print(f"  [OK] Saved to: {kospi_chart}")
    else:
        print("  [FAIL] Failed to create chart")

    # 3. 복합 차트
    print("\n[3] Creating combined chart...")
    combined_chart = generator.create_combined_chart()
    if combined_chart:
        print(f"  [OK] Saved to: {combined_chart}")
    else:
        print("  [FAIL] Failed to create chart")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()

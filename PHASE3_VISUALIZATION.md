# Phase 3: 데이터 시각화 (Week 3)

> Matplotlib/Plotly를 사용한 경제 그래프 생성

---

## ✅ Step 3.1: 기본 그래프 생성 (더미 데이터)
**목표:** Matplotlib으로 선 그래프 PNG 생성
**소요 시간:** 45분

### 📝 체크리스트
- [ ] Matplotlib, Plotly 설치
- [ ] 한글 폰트 설정
- [ ] `visualizers/chart_generator.py` 작성
- [ ] 더미 데이터로 테스트

### 🛠️ 실행 순서

**1. requirements.txt 업데이트**
```
# 기존 라이브러리들...
beautifulsoup4==4.12.3
requests==2.31.0
lxml==5.1.0
python-dotenv==1.0.1
google-generativeai==0.4.0

# 시각화 라이브러리 추가
matplotlib==3.8.3
plotly==5.19.0
kaleido==0.2.1
```

설치:
```bash
pip install matplotlib==3.8.3 plotly==5.19.0 kaleido==0.2.1
```

**2. 차트 생성기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\visualizers\chart_generator.py`
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os


class ChartGenerator:
    """그래프 생성 (Matplotlib 기반)"""

    def __init__(self, output_dir: str = './data/charts'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 한글 폰트 설정
        self._setup_korean_font()

    def _setup_korean_font(self):
        """한글 폰트 설정 (OS별)"""
        import platform

        system = platform.system()

        try:
            if system == 'Windows':
                plt.rcParams['font.family'] = 'Malgun Gothic'
            elif system == 'Darwin':  # macOS
                plt.rcParams['font.family'] = 'AppleGothic'
            else:  # Linux
                plt.rcParams['font.family'] = 'NanumGothic'

            # 마이너스 기호 깨짐 방지
            plt.rcParams['axes.unicode_minus'] = False

            print("✅ 한글 폰트 설정 완료")

        except Exception as e:
            print(f"⚠️  한글 폰트 설정 실패: {e}")
            print("   영어로 대체됩니다.")

    def create_line_chart(
        self,
        dates: list[datetime],
        values: list[float],
        title: str,
        ylabel: str,
        filename: str,
        xlabel: str = '날짜'
    ) -> str:
        """선 그래프 생성"""
        fig, ax = plt.subplots(figsize=(12, 6))

        # 그래프 그리기
        ax.plot(dates, values, marker='o', linewidth=2.5, markersize=5, color='#2E86AB')

        # 제목 및 라벨
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.set_ylabel(ylabel, fontsize=13)
        ax.set_xlabel(xlabel, fontsize=13)

        # 날짜 포맷
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
        plt.xticks(rotation=45, ha='right')

        # 그리드
        ax.grid(True, alpha=0.3, linestyle='--')

        # Y축 포맷 (천 단위 쉼표)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        # 레이아웃 조정
        plt.tight_layout()

        # 저장
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"  ✅ 그래프 저장: {filepath}")
        return filepath

    def create_bar_chart(
        self,
        labels: list[str],
        values: list[float],
        title: str,
        ylabel: str,
        filename: str
    ) -> str:
        """막대 그래프 생성"""
        fig, ax = plt.subplots(figsize=(10, 6))

        # 막대 그래프
        bars = ax.bar(labels, values, color='#A23B72', width=0.6)

        # 막대 위에 값 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{height:,.1f}',
                ha='center',
                va='bottom',
                fontsize=10
            )

        # 제목 및 라벨
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.set_ylabel(ylabel, fontsize=13)

        # 그리드
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')

        # 레이아웃 조정
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # 저장
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"  ✅ 그래프 저장: {filepath}")
        return filepath
```

**3. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_chart.py`
```python
from visualizers.chart_generator import ChartGenerator
from datetime import datetime, timedelta


if __name__ == '__main__':
    print("=" * 60)
    print("차트 생성 테스트 (더미 데이터)")
    print("=" * 60)

    chart_gen = ChartGenerator()

    # === 1. 선 그래프 테스트 ===
    print("\n1. 선 그래프 생성 중...")

    # 더미 데이터: 최근 30일 환율
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]
    values = [1300 + i * 2 + (i % 7) * 15 for i in range(30)]  # 약간의 변동

    chart_gen.create_line_chart(
        dates=dates,
        values=values,
        title='최근 30일 원/달러 환율 추이 (테스트)',
        ylabel='환율 (원)',
        filename='test_exchange_rate.png'
    )

    # === 2. 막대 그래프 테스트 ===
    print("\n2. 막대 그래프 생성 중...")

    labels = ['1분기', '2분기', '3분기', '4분기']
    values = [2.3, 2.8, 2.1, 3.5]

    chart_gen.create_bar_chart(
        labels=labels,
        values=values,
        title='2024년 분기별 GDP 성장률 (테스트)',
        ylabel='성장률 (%)',
        filename='test_gdp_growth.png'
    )

    print("\n" + "=" * 60)
    print("✅ 모든 차트 생성 완료")
    print("=" * 60)
    print("\n생성된 파일:")
    print("  1. data/charts/test_exchange_rate.png")
    print("  2. data/charts/test_gdp_growth.png")
    print("\n파일 탐색기로 확인하세요!")
```

**4. 실행**
```bash
python test_chart.py
```

### ✅ 성공 기준
- [ ] `data/charts/test_exchange_rate.png` 생성
- [ ] `data/charts/test_gdp_growth.png` 생성
- [ ] 한글 제목 정상 표시
- [ ] 그래프가 깔끔하고 읽기 쉬움

### ⚠️ 예상 오류 및 해결

**오류 1:** `findfont: Font family ['Malgun Gothic'] not found`
- **원인:** 한글 폰트 없음
- **해결 (Windows):**
  1. 제어판 → 글꼴에서 "맑은 고딕" 확인
  2. 없으면 나눔고딕 설치: https://hangeul.naver.com/font
  3. 코드 수정:
     ```python
     plt.rcParams['font.family'] = 'NanumGothic'
     ```

**오류 2:** 한글이 □□□ 로 표시
- **원인:** 폰트 캐시 문제
- **해결:**
  ```bash
  # 캐시 삭제
  rm -rf ~/.matplotlib
  ```
  또는
  ```python
  import matplotlib.font_manager as fm
  fm._rebuild()
  ```

**오류 3:** 마이너스 기호가 깨짐
- **해결:** 이미 코드에 포함 (`plt.rcParams['axes.unicode_minus'] = False`)

---

## ✅ Step 3.2: 실제 경제 데이터 수집 (환율)
**목표:** Yahoo Finance API로 실제 환율/주가 데이터 가져오기
**소요 시간:** 2시간

### 📝 체크리스트
- [ ] yfinance 설치
- [ ] `visualizers/data_fetcher.py` 작성
- [ ] 환율 데이터 가져오기 테스트
- [ ] 코스피 데이터 가져오기 테스트

### 🛠️ 실행 순서

**1. requirements.txt 업데이트**
```
# ... 기존 라이브러리들 ...
matplotlib==3.8.3
plotly==5.19.0
kaleido==0.2.1

# 경제 데이터 추가
yfinance==0.2.36
pandas==2.2.0
```

설치:
```bash
pip install yfinance==0.2.36 pandas==2.2.0
```

**2. 데이터 수집기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\visualizers\data_fetcher.py`
```python
import yfinance as yf
from datetime import datetime, timedelta
from typing import Tuple, List


class EconomicDataFetcher:
    """경제 데이터 수집 (Yahoo Finance 기반)"""

    def __init__(self):
        pass

    def get_exchange_rate(
        self,
        days: int = 30,
        currency_pair: str = 'KRW=X'  # USD/KRW
    ) -> Tuple[List[datetime], List[float]]:
        """환율 데이터 가져오기"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 10)  # 여유 있게

            print(f"  환율 데이터 수집 중... ({currency_pair}, 최근 {days}일)")

            # Yahoo Finance에서 데이터 가져오기
            ticker = yf.Ticker(currency_pair)
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                raise ValueError("데이터가 없습니다.")

            # 날짜와 종가 추출
            dates = [date.to_pydatetime() for date in hist.index]
            values = hist['Close'].tolist()

            # 최근 N일만
            if len(dates) > days:
                dates = dates[-days:]
                values = values[-days:]

            print(f"  ✅ {len(dates)}개 데이터 포인트 수집 완료")
            return dates, values

        except Exception as e:
            print(f"  ❌ 환율 데이터 수집 실패: {e}")
            raise

    def get_kospi(self, days: int = 30) -> Tuple[List[datetime], List[float]]:
        """코스피 지수 데이터"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 10)

            print(f"  코스피 데이터 수집 중... (최근 {days}일)")

            # ^KS11 = KOSPI Composite Index
            ticker = yf.Ticker('^KS11')
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                raise ValueError("데이터가 없습니다.")

            dates = [date.to_pydatetime() for date in hist.index]
            values = hist['Close'].tolist()

            if len(dates) > days:
                dates = dates[-days:]
                values = values[-days:]

            print(f"  ✅ {len(dates)}개 데이터 포인트 수집 완료")
            return dates, values

        except Exception as e:
            print(f"  ❌ 코스피 데이터 수집 실패: {e}")
            raise

    def get_kosdaq(self, days: int = 30) -> Tuple[List[datetime], List[float]]:
        """코스닥 지수 데이터"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 10)

            print(f"  코스닥 데이터 수집 중... (최근 {days}일)")

            # ^KQ11 = KOSDAQ Composite Index
            ticker = yf.Ticker('^KQ11')
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                raise ValueError("데이터가 없습니다.")

            dates = [date.to_pydatetime() for date in hist.index]
            values = hist['Close'].tolist()

            if len(dates) > days:
                dates = dates[-days:]
                values = values[-days:]

            print(f"  ✅ {len(dates)}개 데이터 포인트 수집 완료")
            return dates, values

        except Exception as e:
            print(f"  ❌ 코스닥 데이터 수집 실패: {e}")
            raise

    def get_stock_price(self, ticker: str, days: int = 30) -> Tuple[List[datetime], List[float]]:
        """특정 주식 가격 데이터"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 10)

            print(f"  {ticker} 주가 데이터 수집 중...")

            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)

            if hist.empty:
                raise ValueError(f"{ticker} 데이터가 없습니다.")

            dates = [date.to_pydatetime() for date in hist.index]
            values = hist['Close'].tolist()

            if len(dates) > days:
                dates = dates[-days:]
                values = values[-days:]

            print(f"  ✅ {len(dates)}개 데이터 포인트 수집 완료")
            return dates, values

        except Exception as e:
            print(f"  ❌ {ticker} 주가 데이터 수집 실패: {e}")
            raise
```

**3. 실제 데이터로 차트 생성 테스트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_real_chart.py`
```python
from visualizers.chart_generator import ChartGenerator
from visualizers.data_fetcher import EconomicDataFetcher


if __name__ == '__main__':
    print("=" * 60)
    print("실제 경제 데이터로 차트 생성 테스트")
    print("=" * 60)

    # 초기화
    fetcher = EconomicDataFetcher()
    chart_gen = ChartGenerator()

    # === 1. 환율 차트 ===
    print("\n1. 원/달러 환율 차트")
    print("-" * 60)

    try:
        dates, values = fetcher.get_exchange_rate(days=30)

        chart_gen.create_line_chart(
            dates=dates,
            values=values,
            title='최근 30일 원/달러 환율 추이',
            ylabel='환율 (원)',
            filename='real_usd_krw.png'
        )
    except Exception as e:
        print(f"❌ 환율 차트 생성 실패: {e}")

    # === 2. 코스피 차트 ===
    print("\n2. 코스피 지수 차트")
    print("-" * 60)

    try:
        kospi_dates, kospi_values = fetcher.get_kospi(days=30)

        chart_gen.create_line_chart(
            dates=kospi_dates,
            values=kospi_values,
            title='최근 30일 코스피 지수',
            ylabel='지수',
            filename='real_kospi.png'
        )
    except Exception as e:
        print(f"❌ 코스피 차트 생성 실패: {e}")

    # === 3. 코스닥 차트 ===
    print("\n3. 코스닥 지수 차트")
    print("-" * 60)

    try:
        kosdaq_dates, kosdaq_values = fetcher.get_kosdaq(days=30)

        chart_gen.create_line_chart(
            dates=kosdaq_dates,
            values=kosdaq_values,
            title='최근 30일 코스닥 지수',
            ylabel='지수',
            filename='real_kosdaq.png'
        )
    except Exception as e:
        print(f"❌ 코스닥 차트 생성 실패: {e}")

    # === 4. 삼성전자 주가 ===
    print("\n4. 삼성전자 주가 차트")
    print("-" * 60)

    try:
        samsung_dates, samsung_values = fetcher.get_stock_price('005930.KS', days=30)

        chart_gen.create_line_chart(
            dates=samsung_dates,
            values=samsung_values,
            title='최근 30일 삼성전자 주가',
            ylabel='주가 (원)',
            filename='real_samsung.png'
        )
    except Exception as e:
        print(f"❌ 삼성전자 차트 생성 실패: {e}")

    print("\n" + "=" * 60)
    print("✅ 실제 데이터 차트 생성 완료")
    print("=" * 60)
    print("\ndata/charts/ 폴더를 확인하세요!")
```

**4. 실행**
```bash
python test_real_chart.py
```

### ✅ 성공 기준
- [ ] 환율 데이터 수집 성공
- [ ] 코스피 데이터 수집 성공
- [ ] 코스닥 데이터 수집 성공
- [ ] 실제 데이터로 4개 차트 생성
- [ ] 그래프가 최신 데이터 반영

### ⚠️ 예상 오류 및 해결

**오류 1:** `데이터가 없습니다`
- **원인:** Yahoo Finance 접속 불가 또는 티커 심볼 오류
- **해결:**
  - 인터넷 연결 확인
  - 티커 심볼 확인 (KRW=X, ^KS11, ^KQ11)
  - VPN 사용 시 해제

**오류 2:** `SSLError` 또는 인증서 오류
- **해결:**
  ```bash
  pip install --upgrade certifi
  ```

**오류 3:** 데이터가 너무 적음 (5개 미만)
- **원인:** 주말/공휴일 제외
- **해결:** `days` 파라미터를 더 크게 (예: 45일)

---

## ✅ Step 3.3: 뉴스 키워드 기반 자동 그래프 선택
**목표:** 뉴스 내용을 분석해 적절한 그래프 자동 생성
**소요 시간:** 2시간

### 📝 체크리스트
- [ ] `visualizers/auto_visualizer.py` 작성
- [ ] 키워드 → 차트 타입 매핑 로직
- [ ] 뉴스별 그래프 자동 생성 테스트

### 🛠️ 실행 순서

**1. 자동 시각화기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\visualizers\auto_visualizer.py`
```python
from models.news_article import NewsArticle
from visualizers.data_fetcher import EconomicDataFetcher
from visualizers.chart_generator import ChartGenerator
from typing import Optional
import re


class AutoVisualizer:
    """뉴스 키워드 기반 자동 그래프 생성"""

    # 키워드별 시각화 매핑
    KEYWORD_TO_CHART = {
        # 환율 관련
        '환율': ('exchange_rate', '원/달러 환율 추이', '환율 (원)'),
        '달러': ('exchange_rate', '원/달러 환율 추이', '환율 (원)'),
        '원화': ('exchange_rate', '원/달러 환율 추이', '환율 (원)'),
        'USD': ('exchange_rate', '원/달러 환율 추이', '환율 (원)'),

        # 코스피 관련
        '코스피': ('kospi', '코스피 지수 추이', '지수'),
        'KOSPI': ('kospi', '코스피 지수 추이', '지수'),
        '주가': ('kospi', '코스피 지수 추이', '지수'),
        '증시': ('kospi', '코스피 지수 추이', '지수'),
        '주식': ('kospi', '코스피 지수 추이', '지수'),

        # 코스닥 관련
        '코스닥': ('kosdaq', '코스닥 지수 추이', '지수'),
        'KOSDAQ': ('kosdaq', '코스닥 지수 추이', '지수'),

        # 개별 종목 (추가 가능)
        '삼성전자': ('stock_samsung', '삼성전자 주가 추이', '주가 (원)'),
        '삼성': ('stock_samsung', '삼성전자 주가 추이', '주가 (원)'),
    }

    def __init__(self):
        self.fetcher = EconomicDataFetcher()
        self.chart_gen = ChartGenerator()

    def detect_chart_type(self, article: NewsArticle) -> Optional[tuple]:
        """기사 내용을 분석해 적절한 차트 타입 감지"""
        # 제목 + 본문 앞 500자
        text = (article.title + ' ' + article.content[:500]).lower()

        # 우선순위: 제목에서 매칭 > 본문에서 매칭
        matched_in_title = []
        matched_in_content = []

        for keyword, chart_info in self.KEYWORD_TO_CHART.items():
            if keyword.lower() in article.title.lower():
                matched_in_title.append((keyword, chart_info))
            elif keyword.lower() in text:
                matched_in_content.append((keyword, chart_info))

        # 제목에서 매칭된 것 우선
        if matched_in_title:
            keyword, chart_info = matched_in_title[0]
            print(f"  키워드 '{keyword}' 감지 (제목)")
            return chart_info

        if matched_in_content:
            keyword, chart_info = matched_in_content[0]
            print(f"  키워드 '{keyword}' 감지 (본문)")
            return chart_info

        print(f"  ⚠️  매칭되는 차트 타입 없음")
        return None

    def generate_chart_for_article(self, article: NewsArticle, days: int = 30) -> Optional[str]:
        """기사에 적합한 차트 자동 생성"""
        chart_info = self.detect_chart_type(article)

        if not chart_info:
            return None

        chart_type, title, ylabel = chart_info

        try:
            # 데이터 가져오기
            if chart_type == 'exchange_rate':
                dates, values = self.fetcher.get_exchange_rate(days=days)
            elif chart_type == 'kospi':
                dates, values = self.fetcher.get_kospi(days=days)
            elif chart_type == 'kosdaq':
                dates, values = self.fetcher.get_kosdaq(days=days)
            elif chart_type == 'stock_samsung':
                dates, values = self.fetcher.get_stock_price('005930.KS', days=days)
            else:
                return None

            # 파일명 생성 (안전한 파일명)
            safe_title = re.sub(r'[^\w\s-]', '', article.title[:30])
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title}_{chart_type}.png"

            # 차트 생성
            filepath = self.chart_gen.create_line_chart(
                dates=dates,
                values=values,
                title=f"{title} (최근 {days}일)",
                ylabel=ylabel,
                filename=filename
            )

            return filepath

        except Exception as e:
            print(f"  ❌ 차트 생성 실패: {e}")
            return None

    def generate_charts_for_articles(self, articles: list[NewsArticle]) -> dict[str, Optional[str]]:
        """여러 기사에 대한 차트 일괄 생성"""
        results = {}

        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] {article.title[:50]}")

            chart_path = self.generate_chart_for_article(article)
            results[article.url] = chart_path

        return results
```

**2. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_auto_visualizer.py`
```python
from utils.file_manager import FileManager
from visualizers.auto_visualizer import AutoVisualizer


if __name__ == '__main__':
    print("=" * 80)
    print("자동 그래프 생성 테스트")
    print("=" * 80)

    # 초기화
    file_manager = FileManager()
    auto_viz = AutoVisualizer()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다.")
        exit(1)

    # top_news.json이 있으면 그걸 사용, 없으면 최신 파일
    target_file = 'top_news.json' if 'top_news.json' in saved_files else saved_files[0]

    print(f"\n로드 파일: {target_file}")
    articles = file_manager.load_articles(target_file)
    print(f"총 {len(articles)}개 기사\n")

    # 각 기사별 그래프 생성
    print("=" * 80)
    print("그래프 생성 중...")
    print("=" * 80)

    results = auto_viz.generate_charts_for_articles(articles)

    # 결과 요약
    print("\n" + "=" * 80)
    print("결과 요약")
    print("=" * 80)

    success_count = sum(1 for path in results.values() if path is not None)
    fail_count = len(results) - success_count

    print(f"\n총 {len(articles)}개 기사:")
    print(f"  ✅ 그래프 생성 성공: {success_count}개")
    print(f"  ⚠️  그래프 없음: {fail_count}개")

    # 성공한 기사 목록
    if success_count > 0:
        print(f"\n생성된 그래프:")
        for i, (url, path) in enumerate(results.items(), 1):
            if path:
                article = next(a for a in articles if a.url == url)
                print(f"  {i}. {article.title[:50]}")
                print(f"     → {path}")

    print("\n" + "=" * 80)
```

**3. 실행**
```bash
python test_auto_visualizer.py
```

### ✅ 성공 기준
- [ ] 환율 관련 뉴스 → 환율 그래프 자동 생성
- [ ] 주가 관련 뉴스 → 코스피 그래프 자동 생성
- [ ] 코스닥 관련 뉴스 → 코스닥 그래프 자동 생성
- [ ] 매칭 안 되는 뉴스는 None 반환
- [ ] 생성된 그래프 개수 정확히 카운트

### ⚠️ 예상 오류 및 해결

**오류 1:** 모든 기사에서 차트 타입 감지 안 됨
- **원인:** 키워드 매칭 실패
- **해결:** `KEYWORD_TO_CHART`에 더 많은 키워드 추가
  ```python
  '금리': ('interest_rate', ...),
  '물가': ('cpi', ...),
  ```

**오류 2:** 파일명에 특수문자 포함으로 저장 실패
- **원인:** 제목에 특수문자 (`/`, `:` 등)
- **해결:** 이미 코드에 `re.sub()` 로 처리 포함

**오류 3:** 같은 기사에 여러 키워드 매칭
- **원인:** 우선순위 없음
- **해결:** 제목 매칭 우선 로직 이미 구현됨

---

## 🎉 Phase 3 완료!

다음 단계: [Phase 4: 웹 페이지 생성](PHASE4_WEB_GENERATION.md)

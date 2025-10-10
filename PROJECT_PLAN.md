# Spread Insight 프로젝트 계획서

## 프로젝트 개요
여러 뉴스 사이트를 스크래핑하여 핵심 경제 뉴스를 수집하고, AI(Gemini 2.0/2.5 Flash)를 활용해 일반인도 이해하기 쉬운 인사이트로 재구성하여 텔레그램으로 배포하는 시스템. 쿠팡 파트너스 활동을 통한 수익화 포함.

### 🎯 핵심 가치 제안
**단순 뉴스 전달이 아닌, 매일 성장하는 독자 만들기**

- **Learn (배움):** 하루 1개의 경제 이슈 + 핵심 용어 학습
- **Insight (통찰):** 과거 데이터와 비교하여 패턴 파악
- **Action (실천):** "나는 어떻게 해야 할까?"로 이어지는 구체적 행동 제시

> 자세한 콘텐츠 전략은 [CONTENT_STRATEGY.md](CONTENT_STRATEGY.md) 참조

---

## 기술 스택 선정

### 프로그래밍 언어: Python
**선정 이유:**
- 웹 스크래핑 라이브러리 생태계가 가장 풍부 (BeautifulSoup4, Selenium, Scrapy)
- AI API 연동이 간편 (Gemini, OpenAI 등 공식 SDK 제공)
- 데이터 처리 및 시각화 도구 성숙 (Pandas, Matplotlib, Plotly)
- 텔레그램 봇 라이브러리 안정적 (python-telegram-bot)
- 배포 및 스케줄링 용이 (APScheduler, cron)
- 클라우드 배포 옵션 다양 (AWS Lambda, GCP Cloud Functions)

**C/C++ 제외 이유:**
- 웹 스크래핑, AI API 연동 라이브러리 부족
- 개발 속도 느림, 복잡도 높음

**C# 제외 이유:**
- 스크래핑 라이브러리가 Python보다 제한적
- Linux 환경 배포 시 .NET Core 의존성
- AI/데이터 분석 생태계가 Python보다 약함

### AI 모델: Google Gemini 2.0/2.5 Flash
- 빠른 응답 속도 (Flash 모델)
- 무료 할당량 충분 (분당 15 요청)
- Claude 대비 1/10 가격
- 한국어 지원 양호
- 긴 컨텍스트 처리 가능

### 핵심 라이브러리
```
# 웹 스크래핑
beautifulsoup4==4.12.3
selenium==4.18.1
requests==2.31.0
lxml==5.1.0

# AI 처리
google-generativeai==0.4.0

# 데이터 처리
pandas==2.2.0
numpy==1.26.4

# 시각화
plotly==5.19.0
matplotlib==3.8.3

# 텔레그램
python-telegram-bot==20.8

# 웹 서버 (옵션)
flask==3.0.2

# 데이터베이스
sqlalchemy==2.0.27

# 스케줄링
apscheduler==3.10.4

# 유틸리티
python-dotenv==1.0.1
pydantic==2.6.1
```

---

## 시스템 아키텍처

```
┌─────────────────┐
│  뉴스 스크래퍼   │ (네이버, 다음, 조선비즈, 한경)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   뉴스 선정      │ (키워드 점수 + Gemini 최종 선택)
└────────┬────────┘     ← 하루 1개 선정
         │
         ▼
┌─────────────────┐
│   데이터 저장    │ (JSON/SQLite)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  과거 데이터 수집│ (ECOS API, yfinance, 자체 DB)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini AI 분석 │ (요약, 과거 비교, 인사이트, 행동 제안)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  용어 추출/설명  │ (용어 DB + Gemini 쉬운 설명)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  시각화 생성     │ (Plotly - 과거 패턴 차트)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTML 페이지     │ (Learn → Insight → Action 구조)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Pages 배포│ (무료 호스팅)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  텔레그램 전송   │ (봇 API - 링크 포함 메시지)
└─────────────────┘
```

---

## 프로젝트 디렉토리 구조

```
spread_insight/
├── scrapers/                  # 뉴스 수집 모듈
│   ├── __init__.py
│   ├── base_scraper.py       # 추상 클래스
│   ├── naver_scraper.py      # 네이버 뉴스
│   ├── daum_scraper.py       # 다음 뉴스
│   ├── chosun_scraper.py     # 조선비즈
│   └── hankyung_scraper.py   # 한국경제
│
├── analyzers/                 # AI 분석 모듈
│   ├── __init__.py
│   ├── gemini_analyzer.py    # Gemini API 연동
│   ├── context_builder.py    # 과거 맥락 구성
│   ├── summarizer.py         # 요약 생성
│   └── terminology.py        # 용어 해설 생성
│
├── visualizers/               # 데이터 시각화
│   ├── __init__.py
│   ├── chart_generator.py    # 그래프 생성
│   ├── data_fetcher.py       # 경제 데이터 수집
│   └── templates/            # 그래프 템플릿
│
├── publishers/                # 배포 모듈
│   ├── __init__.py
│   ├── html_generator.py     # HTML 생성
│   ├── github_deployer.py    # GitHub Pages 배포
│   ├── telegram_bot.py       # 텔레그램 봇
│   └── coupang_partner.py    # 쿠팡 파트너스 연동
│
├── models/                    # 데이터 모델
│   ├── __init__.py
│   ├── news_article.py       # 뉴스 기사 모델
│   └── insight.py            # 인사이트 모델
│
├── database/                  # 데이터베이스
│   ├── __init__.py
│   ├── db_manager.py         # DB 관리
│   └── news.db               # SQLite DB
│
├── utils/                     # 유틸리티
│   ├── __init__.py
│   ├── config.py             # 설정 관리
│   ├── logger.py             # 로깅
│   └── exceptions.py         # 커스텀 예외
│
├── templates/                 # HTML 템플릿
│   ├── base.html
│   ├── news_detail.html
│   └── assets/
│       ├── style.css
│       └── script.js
│
├── data/                      # 임시 데이터
│   ├── raw/                  # 원본 뉴스
│   ├── processed/            # 처리된 데이터
│   └── charts/               # 생성된 그래프
│
├── tests/                     # 테스트 코드
│   ├── test_scrapers.py
│   ├── test_analyzers.py
│   └── test_publishers.py
│
├── .env                       # 환경 변수 (API 키)
├── .gitignore
├── requirements.txt           # 의존성
├── main.py                    # 메인 실행 스크립트
├── scheduler.py               # 스케줄러
└── README.md
```

---

## 워크플로우 상세

### 1단계: 뉴스 수집
1. 스케줄러 트리거 (매일 오전 7시, 오후 6시)
2. 각 스크래퍼가 최근 24시간 뉴스 수집
3. 중복 제거 (URL 기준)
4. SQLite DB 저장

### 2단계: AI 분석
1. 수집된 뉴스 중 중요도 점수 계산 (키워드, 조회수 기반)
2. 상위 5개 선정
3. Gemini API 호출:
   - 3줄 요약 생성
   - 과거 관련 뉴스 검색 (DB에서)
   - 시계열 맥락 구성
   - 쉬운 언어로 재작성 (중학생 눈높이)
   - 전문 용어 자동 추출 및 해설 생성

### 3단계: 시각화
1. 뉴스 키워드 기반 관련 경제 지표 식별
2. 한국은행 Open API 또는 Yahoo Finance에서 데이터 수집
3. Plotly로 인터랙티브 그래프 생성 (PNG + HTML)

### 4단계: 웹 페이지 생성
1. HTML 템플릿에 데이터 삽입
2. 각 뉴스마다 고유 HTML 파일 생성
3. 그래프 이미지 포함
4. 쿠팡 파트너스 링크 삽입

### 5단계: 배포
1. GitHub Pages 저장소에 HTML 파일 push
2. 고유 URL 생성 (예: `https://username.github.io/news/20250110_news1.html`)

### 6단계: 텔레그램 전송
1. 각 뉴스마다 메시지 구성:
   - 제목 + 한줄 요약
   - 버튼 1: "상세 인사이트 보기" (GitHub Pages URL)
   - 버튼 2: "관련 상품 보기" (쿠팡 파트너스 URL)
2. 구독자 리스트에 일괄 전송

---

## Phase 1: 뉴스 수집 (Week 1)

### Step 1.1: 프로젝트 초기 설정
**목표:** 개발 환경 구축
**소요 시간:** 30분

**세부 작업:**
1. 폴더 구조 생성
   ```bash
   mkdir -p spread_insight/{scrapers,analyzers,visualizers,publishers,models,database,utils,templates,data,tests}
   cd spread_insight
   ```

2. Git 초기화
   ```bash
   git init
   ```

3. `.gitignore` 작성
   ```
   .env
   __pycache__/
   *.pyc
   data/
   *.db
   venv/
   .vscode/
   ```

4. 가상환경 생성
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

5. `requirements.txt` 작성 (Phase 1용)
   ```
   beautifulsoup4==4.12.3
   requests==2.31.0
   lxml==5.1.0
   python-dotenv==1.0.1
   ```

6. 라이브러리 설치
   ```bash
   pip install -r requirements.txt
   ```

7. `.env` 파일 생성
   ```
   # 나중에 추가할 API 키들
   GEMINI_API_KEY=
   TELEGRAM_BOT_TOKEN=
   COUPANG_ACCESS_KEY=
   ```

**성공 기준:**
- 폴더 구조 완성
- 가상환경 활성화
- 라이브러리 설치 완료

---

### Step 1.2: 단일 기사 스크래핑 (네이버)
**목표:** 네이버 경제 뉴스 1개 기사의 제목, 본문, 날짜 추출
**소요 시간:** 1시간

**세부 작업:**

1. `scrapers/base_scraper.py` 작성
   ```python
   from abc import ABC, abstractmethod
   from dataclasses import dataclass
   from datetime import datetime

   @dataclass
   class NewsArticle:
       url: str
       title: str
       content: str
       published_at: datetime
       source: str
       keywords: list[str] = None

   class BaseScraper(ABC):
       @abstractmethod
       def scrape_article(self, url: str) -> NewsArticle:
           pass
   ```

2. `scrapers/naver_scraper.py` 작성
   ```python
   import requests
   from bs4 import BeautifulSoup
   from .base_scraper import BaseScraper, NewsArticle
   from datetime import datetime

   class NaverScraper(BaseScraper):
       def scrape_article(self, url: str) -> NewsArticle:
           # User-Agent 설정 (차단 방지)
           headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
           }

           # 페이지 요청
           response = requests.get(url, headers=headers)
           response.raise_for_status()

           # HTML 파싱
           soup = BeautifulSoup(response.text, 'lxml')

           # 제목 추출
           title = soup.select_one('#title_area span').get_text(strip=True)

           # 본문 추출
           content_elem = soup.select('#dic_area')
           content = '\n'.join([p.get_text(strip=True) for p in content_elem])

           # 날짜 추출
           date_str = soup.select_one('.media_end_head_info_datestamp_time').get('data-date-time')
           published_at = datetime.fromisoformat(date_str)

           return NewsArticle(
               url=url,
               title=title,
               content=content,
               published_at=published_at,
               source='네이버'
           )
   ```

3. `test_scraper.py` 작성 (루트 디렉토리)
   ```python
   from scrapers.naver_scraper import NaverScraper

   if __name__ == '__main__':
       # 테스트용 네이버 뉴스 URL (실제 URL로 교체)
       test_url = 'https://n.news.naver.com/article/...'

       scraper = NaverScraper()
       article = scraper.scrape_article(test_url)

       print(f"제목: {article.title}")
       print(f"날짜: {article.published_at}")
       print(f"본문: {article.content[:200]}...")  # 앞 200자만
   ```

4. 실행 및 검증
   ```bash
   python test_scraper.py
   ```

**예상 이슈 및 해결:**
- **이슈 1:** 네이버 HTML 구조가 달라서 선택자가 안 맞음
  - **해결:** 브라우저 개발자 도구로 실제 HTML 구조 확인 후 선택자 수정

- **이슈 2:** 403 Forbidden 에러
  - **해결:** User-Agent 헤더 추가 또는 더 복잡한 헤더 설정

- **이슈 3:** 동적 콘텐츠라 requests로 안 됨
  - **해결:** Selenium으로 전환 (나중에)

**성공 기준:**
- 콘솔에 제목, 날짜, 본문 일부 출력
- 에러 없이 실행 완료

---

### Step 1.3: 여러 기사 목록 수집
**목표:** 네이버 경제 섹션 메인 페이지에서 최신 10개 기사 URL 추출
**소요 시간:** 1시간

**세부 작업:**

1. `scrapers/naver_scraper.py`에 메서드 추가
   ```python
   def get_article_list(self, category_url: str, limit: int = 10) -> list[str]:
       """
       카테고리 페이지에서 기사 URL 리스트 추출

       Args:
           category_url: 네이버 경제 섹션 URL
           limit: 가져올 기사 수

       Returns:
           기사 URL 리스트
       """
       headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
       }

       response = requests.get(category_url, headers=headers)
       soup = BeautifulSoup(response.text, 'lxml')

       # 기사 링크 추출 (실제 선택자는 확인 필요)
       article_links = []
       for link in soup.select('.sa_text_title')[:limit]:
           href = link.get('href')
           if href:
               article_links.append(href)

       return article_links
   ```

2. `test_scraper.py` 업데이트
   ```python
   from scrapers.naver_scraper import NaverScraper

   if __name__ == '__main__':
       scraper = NaverScraper()

       # 네이버 경제 섹션 URL
       economy_url = 'https://news.naver.com/section/101'

       # 기사 목록 수집
       article_urls = scraper.get_article_list(economy_url, limit=10)

       print(f"총 {len(article_urls)}개 기사 발견")
       for i, url in enumerate(article_urls, 1):
           print(f"{i}. {url}")

       # 첫 번째 기사 상세 정보 가져오기
       if article_urls:
           print("\n첫 번째 기사 상세:")
           article = scraper.scrape_article(article_urls[0])
           print(f"제목: {article.title}")
           print(f"본문: {article.content[:100]}...")
   ```

3. 실행
   ```bash
   python test_scraper.py
   ```

**성공 기준:**
- 10개의 유효한 URL 출력
- 첫 번째 기사의 상세 정보 출력

---

### Step 1.4: 데이터 모델 정의 및 JSON 저장
**목표:** 수집한 기사를 구조화된 형태로 JSON 파일에 저장
**소요 시간:** 45분

**세부 작업:**

1. `models/news_article.py` 작성 (더 완성도 높게)
   ```python
   from dataclasses import dataclass, asdict
   from datetime import datetime
   from typing import Optional
   import json

   @dataclass
   class NewsArticle:
       url: str
       title: str
       content: str
       published_at: datetime
       source: str
       keywords: Optional[list[str]] = None
       summary: Optional[str] = None
       easy_explanation: Optional[str] = None
       terminology: Optional[dict[str, str]] = None

       def to_dict(self) -> dict:
           """datetime을 ISO 포맷 문자열로 변환"""
           data = asdict(self)
           data['published_at'] = self.published_at.isoformat()
           return data

       @classmethod
       def from_dict(cls, data: dict) -> 'NewsArticle':
           """딕셔너리에서 객체 복원"""
           data['published_at'] = datetime.fromisoformat(data['published_at'])
           return cls(**data)

       def save_to_json(self, filepath: str):
           """JSON 파일로 저장"""
           with open(filepath, 'w', encoding='utf-8') as f:
               json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

       @classmethod
       def load_from_json(cls, filepath: str) -> 'NewsArticle':
           """JSON 파일에서 로드"""
           with open(filepath, 'r', encoding='utf-8') as f:
               data = json.load(f)
           return cls.from_dict(data)
   ```

2. `utils/file_manager.py` 작성
   ```python
   import json
   import os
   from typing import List
   from models.news_article import NewsArticle

   class FileManager:
       def __init__(self, data_dir: str = './data'):
           self.data_dir = data_dir
           self.raw_dir = os.path.join(data_dir, 'raw')
           os.makedirs(self.raw_dir, exist_ok=True)

       def save_articles(self, articles: List[NewsArticle], filename: str = 'news_data.json'):
           """여러 기사를 하나의 JSON 파일로 저장"""
           filepath = os.path.join(self.raw_dir, filename)
           data = [article.to_dict() for article in articles]

           with open(filepath, 'w', encoding='utf-8') as f:
               json.dump(data, f, ensure_ascii=False, indent=2)

           print(f"✅ {len(articles)}개 기사를 {filepath}에 저장했습니다.")

       def load_articles(self, filename: str = 'news_data.json') -> List[NewsArticle]:
           """JSON 파일에서 기사 로드"""
           filepath = os.path.join(self.raw_dir, filename)

           with open(filepath, 'r', encoding='utf-8') as f:
               data = json.load(f)

           return [NewsArticle.from_dict(item) for item in data]
   ```

3. `test_scraper.py` 업데이트
   ```python
   from scrapers.naver_scraper import NaverScraper
   from utils.file_manager import FileManager
   from datetime import datetime

   if __name__ == '__main__':
       scraper = NaverScraper()
       file_manager = FileManager()

       # 기사 목록 수집
       economy_url = 'https://news.naver.com/section/101'
       article_urls = scraper.get_article_list(economy_url, limit=5)  # 테스트용 5개

       # 각 기사 상세 정보 수집
       articles = []
       for i, url in enumerate(article_urls, 1):
           try:
               print(f"[{i}/{len(article_urls)}] {url} 수집 중...")
               article = scraper.scrape_article(url)
               articles.append(article)
           except Exception as e:
               print(f"❌ 에러: {e}")
               continue

       # JSON 파일로 저장
       timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
       filename = f'naver_news_{timestamp}.json'
       file_manager.save_articles(articles, filename)

       # 저장된 파일 다시 읽기 (검증)
       loaded_articles = file_manager.load_articles(filename)
       print(f"\n✅ {len(loaded_articles)}개 기사 로드 완료")
       print(f"첫 번째 기사: {loaded_articles[0].title}")
   ```

4. 실행
   ```bash
   python test_scraper.py
   ```

**성공 기준:**
- `data/raw/naver_news_YYYYMMDD_HHMMSS.json` 파일 생성
- JSON 파일 내용 확인 (UTF-8, 들여쓰기 정상)
- 다시 로드했을 때 데이터 일치

---

### Step 1.5: 다음(Daum) 스크래퍼 추가
**목표:** 네이버와 동일한 방식으로 다음 뉴스 수집
**소요 시간:** 1.5시간

**세부 작업:**

1. `scrapers/daum_scraper.py` 작성
   ```python
   import requests
   from bs4 import BeautifulSoup
   from .base_scraper import BaseScraper
   from models.news_article import NewsArticle
   from datetime import datetime

   class DaumScraper(BaseScraper):
       def get_article_list(self, category_url: str, limit: int = 10) -> list[str]:
           """다음 경제 섹션에서 기사 URL 추출"""
           headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
           }

           response = requests.get(category_url, headers=headers)
           soup = BeautifulSoup(response.text, 'lxml')

           # 다음 뉴스 링크 선택자 (실제 확인 필요)
           article_links = []
           for link in soup.select('.link_txt')[:limit]:
               href = link.get('href')
               if href and href.startswith('http'):
                   article_links.append(href)

           return article_links

       def scrape_article(self, url: str) -> NewsArticle:
           """다음 뉴스 기사 상세 정보 추출"""
           headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
           }

           response = requests.get(url, headers=headers)
           response.raise_for_status()
           soup = BeautifulSoup(response.text, 'lxml')

           # 제목 (다음 뉴스 구조에 맞게)
           title = soup.select_one('h3.tit_view').get_text(strip=True)

           # 본문
           content_elem = soup.select('#harmonyContainer p')
           content = '\n'.join([p.get_text(strip=True) for p in content_elem])

           # 날짜
           date_str = soup.select_one('.num_date').get_text(strip=True)
           # 날짜 파싱 (예: "2025.01.10. 오후 3:24")
           published_at = datetime.strptime(date_str.replace('.', '').strip(), '%Y%m%d 오후 %H:%M')

           return NewsArticle(
               url=url,
               title=title,
               content=content,
               published_at=published_at,
               source='다음'
           )
   ```

2. `test_multi_scraper.py` 작성 (여러 소스 통합 테스트)
   ```python
   from scrapers.naver_scraper import NaverScraper
   from scrapers.daum_scraper import DaumScraper
   from utils.file_manager import FileManager
   from datetime import datetime

   if __name__ == '__main__':
       file_manager = FileManager()
       all_articles = []

       # 네이버 수집
       print("=== 네이버 뉴스 수집 ===")
       naver_scraper = NaverScraper()
       naver_urls = naver_scraper.get_article_list('https://news.naver.com/section/101', limit=3)
       for url in naver_urls:
           try:
               article = naver_scraper.scrape_article(url)
               all_articles.append(article)
               print(f"✅ {article.title[:30]}...")
           except Exception as e:
               print(f"❌ {e}")

       # 다음 수집
       print("\n=== 다음 뉴스 수집 ===")
       daum_scraper = DaumScraper()
       daum_urls = daum_scraper.get_article_list('https://news.daum.net/economy', limit=3)
       for url in daum_urls:
           try:
               article = daum_scraper.scrape_article(url)
               all_articles.append(article)
               print(f"✅ {article.title[:30]}...")
           except Exception as e:
               print(f"❌ {e}")

       # 통합 저장
       timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
       filename = f'combined_news_{timestamp}.json'
       file_manager.save_articles(all_articles, filename)

       print(f"\n총 {len(all_articles)}개 기사 저장 완료")
   ```

3. 실행
   ```bash
   python test_multi_scraper.py
   ```

**성공 기준:**
- 네이버 3개 + 다음 3개 = 총 6개 기사 수집
- `data/raw/combined_news_YYYYMMDD_HHMMSS.json` 파일 생성

---

### Step 1.6: 중복 제거 및 데이터 정제
**목표:** 동일 기사(URL 기준) 중복 제거, 빈 본문 필터링
**소요 시간:** 45분

**세부 작업:**

1. `utils/data_cleaner.py` 작성
   ```python
   from typing import List
   from models.news_article import NewsArticle

   class DataCleaner:
       @staticmethod
       def remove_duplicates(articles: List[NewsArticle]) -> List[NewsArticle]:
           """URL 기준 중복 제거"""
           seen_urls = set()
           unique_articles = []

           for article in articles:
               if article.url not in seen_urls:
                   seen_urls.add(article.url)
                   unique_articles.append(article)

           print(f"중복 제거: {len(articles)} → {len(unique_articles)}개")
           return unique_articles

       @staticmethod
       def filter_invalid(articles: List[NewsArticle]) -> List[NewsArticle]:
           """유효하지 않은 기사 필터링"""
           valid_articles = []

           for article in articles:
               # 본문이 너무 짧으면 제외
               if len(article.content) < 100:
                   print(f"❌ 본문 너무 짧음: {article.title[:30]}")
                   continue

               # 제목이 비어있으면 제외
               if not article.title.strip():
                   print(f"❌ 제목 없음: {article.url}")
                   continue

               valid_articles.append(article)

           print(f"유효성 검증: {len(articles)} → {len(valid_articles)}개")
           return valid_articles

       @staticmethod
       def clean(articles: List[NewsArticle]) -> List[NewsArticle]:
           """전체 정제 파이프라인"""
           articles = DataCleaner.remove_duplicates(articles)
           articles = DataCleaner.filter_invalid(articles)
           return articles
   ```

2. `test_multi_scraper.py`에 정제 로직 추가
   ```python
   # ... (이전 코드)
   from utils.data_cleaner import DataCleaner

   # 통합 저장 전에 정제
   print("\n=== 데이터 정제 ===")
   cleaned_articles = DataCleaner.clean(all_articles)

   timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
   filename = f'cleaned_news_{timestamp}.json'
   file_manager.save_articles(cleaned_articles, filename)
   ```

**성공 기준:**
- 중복 제거 동작 확인
- 짧은 본문 필터링 동작 확인

---

### Step 1.7: 에러 핸들링 및 로깅
**목표:** 스크래핑 실패 시 로그 기록, 재시도 로직
**소요 시간:** 1시간

**세부 작업:**

1. `utils/logger.py` 작성
   ```python
   import logging
   import os
   from datetime import datetime

   def setup_logger(name: str = 'spread_insight') -> logging.Logger:
       """로거 설정"""
       # 로그 디렉토리 생성
       log_dir = './logs'
       os.makedirs(log_dir, exist_ok=True)

       # 로그 파일명 (날짜별)
       log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y%m%d")}.log')

       # 로거 생성
       logger = logging.getLogger(name)
       logger.setLevel(logging.DEBUG)

       # 파일 핸들러
       file_handler = logging.FileHandler(log_file, encoding='utf-8')
       file_handler.setLevel(logging.DEBUG)

       # 콘솔 핸들러
       console_handler = logging.StreamHandler()
       console_handler.setLevel(logging.INFO)

       # 포매터
       formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       )
       file_handler.setFormatter(formatter)
       console_handler.setFormatter(formatter)

       logger.addHandler(file_handler)
       logger.addHandler(console_handler)

       return logger
   ```

2. `scrapers/base_scraper.py`에 재시도 로직 추가
   ```python
   import time
   from utils.logger import setup_logger

   class BaseScraper(ABC):
       def __init__(self):
           self.logger = setup_logger(self.__class__.__name__)

       def scrape_with_retry(self, url: str, max_retries: int = 3) -> NewsArticle:
           """재시도 로직 포함 스크래핑"""
           for attempt in range(1, max_retries + 1):
               try:
                   self.logger.info(f"[시도 {attempt}/{max_retries}] {url}")
                   article = self.scrape_article(url)
                   self.logger.info(f"✅ 성공: {article.title}")
                   return article
               except Exception as e:
                   self.logger.error(f"❌ 실패: {e}")
                   if attempt < max_retries:
                       wait_time = 2 ** attempt  # 지수 백오프
                       self.logger.info(f"⏳ {wait_time}초 대기 후 재시도...")
                       time.sleep(wait_time)
                   else:
                       self.logger.error(f"최종 실패: {url}")
                       raise
   ```

3. `test_multi_scraper.py` 업데이트 (재시도 적용)
   ```python
   # scraper.scrape_article(url) 대신
   article = scraper.scrape_with_retry(url)
   ```

**성공 기준:**
- `logs/YYYYMMDD.log` 파일 생성
- 실패 시 재시도 동작 확인
- 로그에 시간, 레벨, 메시지 정상 기록

---

## Phase 2: AI 분석 (Week 2)

### Step 2.1: Gemini API 연동
**목표:** 1개 기사를 3줄로 요약
**소요 시간:** 1시간

**세부 작업:**

1. `requirements.txt`에 추가
   ```
   google-generativeai==0.4.0
   ```

2. `.env`에 API 키 추가
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. `utils/config.py` 작성
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   class Config:
       GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
       GEMINI_MODEL = 'gemini-2.0-flash-exp'  # 또는 'gemini-2.5-flash'

       # 스크래핑 설정
       MAX_ARTICLES_PER_SITE = 10
       SCRAPING_DELAY = 1  # 초

       # 데이터 경로
       DATA_DIR = './data'
       RAW_DIR = './data/raw'
       PROCESSED_DIR = './data/processed'
   ```

4. `analyzers/gemini_analyzer.py` 작성
   ```python
   import google.generativeai as genai
   from utils.config import Config
   from utils.logger import setup_logger
   from models.news_article import NewsArticle

   class GeminiAnalyzer:
       def __init__(self):
           genai.configure(api_key=Config.GEMINI_API_KEY)
           self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
           self.logger = setup_logger(self.__class__.__name__)

       def summarize(self, article: NewsArticle, num_sentences: int = 3) -> str:
           """기사를 지정된 문장 수로 요약"""
           prompt = f"""
           다음 뉴스 기사를 정확히 {num_sentences}문장으로 요약해주세요.
           핵심 내용만 간결하게 담아주세요.

           제목: {article.title}
           본문: {article.content}

           요약:
           """

           try:
               response = self.model.generate_content(prompt)
               summary = response.text.strip()
               self.logger.info(f"✅ 요약 완료: {article.title[:30]}")
               return summary
           except Exception as e:
               self.logger.error(f"❌ 요약 실패: {e}")
               raise
   ```

5. `test_gemini.py` 작성
   ```python
   from utils.file_manager import FileManager
   from analyzers.gemini_analyzer import GeminiAnalyzer

   if __name__ == '__main__':
       # 저장된 기사 로드
       file_manager = FileManager()
       articles = file_manager.load_articles('cleaned_news_20250110_120000.json')  # 실제 파일명

       # Gemini 분석기 초기화
       analyzer = GeminiAnalyzer()

       # 첫 번째 기사 요약
       article = articles[0]
       print(f"원본 제목: {article.title}")
       print(f"원본 본문 길이: {len(article.content)}자\n")

       summary = analyzer.summarize(article, num_sentences=3)
       print(f"요약:\n{summary}")

       # 기사 객체에 요약 추가
       article.summary = summary

       # 저장
       file_manager.save_articles([article], 'summarized_news.json')
   ```

6. 실행
   ```bash
   pip install google-generativeai
   python test_gemini.py
   ```

**성공 기준:**
- 3줄 요약문 생성
- `data/raw/summarized_news.json`에 summary 필드 포함

---

### Step 2.2: 쉬운 언어로 재작성
**목표:** 전문 용어를 중학생도 이해할 수 있게 변환
**소요 시간:** 1.5시간

**세부 작업:**

1. `analyzers/gemini_analyzer.py`에 메서드 추가
   ```python
   def simplify_language(self, article: NewsArticle) -> str:
       """전문 용어를 쉬운 언어로 변환"""
       prompt = f"""
       다음 경제 뉴스를 중학생도 이해할 수 있도록 쉽게 다시 작성해주세요.

       규칙:
       1. 전문 용어는 괄호 안에 쉬운 설명 추가
       2. 예시: "기준금리(한국은행이 정하는 기본 이자율)"
       3. 문장은 짧고 명확하게
       4. 비유나 예시를 활용

       원본:
       제목: {article.title}
       본문: {article.content}

       쉬운 설명:
       """

       try:
           response = self.model.generate_content(prompt)
           easy_text = response.text.strip()
           self.logger.info(f"✅ 쉬운 설명 생성: {article.title[:30]}")
           return easy_text
       except Exception as e:
           self.logger.error(f"❌ 쉬운 설명 생성 실패: {e}")
           raise
   ```

2. `test_gemini.py` 업데이트
   ```python
   # 요약 후에 추가
   easy_explanation = analyzer.simplify_language(article)
   print(f"\n쉬운 설명:\n{easy_explanation}")

   article.easy_explanation = easy_explanation
   ```

**성공 기준:**
- 전문 용어가 괄호로 설명됨
- 중학생 수준에서 이해 가능한 문장

---

### Step 2.3: 용어 자동 추출 및 해설
**목표:** 어려운 단어를 자동으로 찾아서 용어집 생성
**소요 시간:** 1.5시간

**세부 작업:**

1. `analyzers/terminology.py` 작성
   ```python
   import google.generativeai as genai
   from utils.config import Config
   from utils.logger import setup_logger
   import json

   class TerminologyExtractor:
       def __init__(self):
           genai.configure(api_key=Config.GEMINI_API_KEY)
           self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
           self.logger = setup_logger(self.__class__.__name__)

       def extract_and_explain(self, text: str) -> dict[str, str]:
           """텍스트에서 전문 용어 추출 및 설명"""
           prompt = f"""
           다음 경제 뉴스에서 일반인이 어려워할 만한 전문 용어를 찾아서
           JSON 형식으로 설명해주세요.

           텍스트:
           {text}

           출력 형식 (반드시 유효한 JSON):
           {{
               "기준금리": "한국은행이 정하는 기본 이자율로, 은행들이 대출할 때 참고하는 기준",
               "환율": "다른 나라 돈과 우리나라 돈을 바꿀 때의 비율"
           }}

           JSON:
           """

           try:
               response = self.model.generate_content(prompt)
               # JSON 파싱
               json_text = response.text.strip()
               # Markdown 코드 블록 제거
               if json_text.startswith('```'):
                   json_text = json_text.split('```')[1]
                   if json_text.startswith('json'):
                       json_text = json_text[4:]

               terminology = json.loads(json_text)
               self.logger.info(f"✅ {len(terminology)}개 용어 추출")
               return terminology
           except Exception as e:
               self.logger.error(f"❌ 용어 추출 실패: {e}")
               return {}
   ```

2. `test_gemini.py`에 추가
   ```python
   from analyzers.terminology import TerminologyExtractor

   # ... (이전 코드)

   # 용어 추출
   term_extractor = TerminologyExtractor()
   terminology = term_extractor.extract_and_explain(article.content)

   print(f"\n용어 해설:")
   for term, explanation in terminology.items():
       print(f"  • {term}: {explanation}")

   article.terminology = terminology
   ```

**성공 기준:**
- 3~5개의 전문 용어 자동 추출
- 각 용어에 대한 쉬운 설명
- JSON 파싱 오류 없음

---

### Step 2.4: 과거 맥락 구성 (타임라인)
**목표:** 현재 뉴스와 관련된 과거 뉴스를 찾아 시계열 맥락 생성
**소요 시간:** 2시간

**세부 작업:**

1. `database/db_manager.py` 작성 (SQLite)
   ```python
   import sqlite3
   from typing import List
   from models.news_article import NewsArticle
   from datetime import datetime
   import json

   class DatabaseManager:
       def __init__(self, db_path: str = './database/news.db'):
           self.db_path = db_path
           self._create_table()

       def _create_table(self):
           """뉴스 테이블 생성"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS articles (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT UNIQUE,
                   title TEXT,
                   content TEXT,
                   published_at TEXT,
                   source TEXT,
                   keywords TEXT,
                   summary TEXT,
                   easy_explanation TEXT,
                   terminology TEXT,
                   created_at TEXT DEFAULT CURRENT_TIMESTAMP
               )
           ''')
           conn.commit()
           conn.close()

       def insert_article(self, article: NewsArticle):
           """기사 삽입 (중복 시 무시)"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()

           try:
               cursor.execute('''
                   INSERT OR IGNORE INTO articles
                   (url, title, content, published_at, source, keywords, summary, easy_explanation, terminology)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ''', (
                   article.url,
                   article.title,
                   article.content,
                   article.published_at.isoformat(),
                   article.source,
                   json.dumps(article.keywords) if article.keywords else None,
                   article.summary,
                   article.easy_explanation,
                   json.dumps(article.terminology) if article.terminology else None
               ))
               conn.commit()
           finally:
               conn.close()

       def search_by_keyword(self, keyword: str, limit: int = 10) -> List[NewsArticle]:
           """키워드로 기사 검색"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()

           cursor.execute('''
               SELECT url, title, content, published_at, source, keywords, summary, easy_explanation, terminology
               FROM articles
               WHERE title LIKE ? OR content LIKE ?
               ORDER BY published_at DESC
               LIMIT ?
           ''', (f'%{keyword}%', f'%{keyword}%', limit))

           rows = cursor.fetchall()
           conn.close()

           articles = []
           for row in rows:
               article = NewsArticle(
                   url=row[0],
                   title=row[1],
                   content=row[2],
                   published_at=datetime.fromisoformat(row[3]),
                   source=row[4],
                   keywords=json.loads(row[5]) if row[5] else None,
                   summary=row[6],
                   easy_explanation=row[7],
                   terminology=json.loads(row[8]) if row[8] else None
               )
               articles.append(article)

           return articles
   ```

2. `analyzers/context_builder.py` 작성
   ```python
   import google.generativeai as genai
   from utils.config import Config
   from utils.logger import setup_logger
   from database.db_manager import DatabaseManager
   from models.news_article import NewsArticle

   class ContextBuilder:
       def __init__(self):
           genai.configure(api_key=Config.GEMINI_API_KEY)
           self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
           self.logger = setup_logger(self.__class__.__name__)
           self.db = DatabaseManager()

       def extract_keywords(self, article: NewsArticle) -> list[str]:
           """기사에서 핵심 키워드 추출"""
           prompt = f"""
           다음 경제 뉴스에서 핵심 키워드 3~5개를 추출해주세요.
           쉼표로 구분하여 출력하세요.

           제목: {article.title}
           본문: {article.content[:500]}

           키워드:
           """

           try:
               response = self.model.generate_content(prompt)
               keywords = [k.strip() for k in response.text.strip().split(',')]
               self.logger.info(f"✅ 키워드 추출: {keywords}")
               return keywords
           except Exception as e:
               self.logger.error(f"❌ 키워드 추출 실패: {e}")
               return []

       def build_timeline(self, article: NewsArticle) -> str:
           """과거 관련 뉴스를 기반으로 타임라인 생성"""
           # 1. 키워드 추출
           keywords = self.extract_keywords(article)
           article.keywords = keywords

           # 2. 과거 관련 기사 검색
           related_articles = []
           for keyword in keywords:
               articles = self.db.search_by_keyword(keyword, limit=3)
               related_articles.extend(articles)

           # 중복 제거
           seen_urls = {article.url}
           unique_related = []
           for rel_article in related_articles:
               if rel_article.url not in seen_urls:
                   seen_urls.add(rel_article.url)
                   unique_related.append(rel_article)

           if not unique_related:
               self.logger.info("관련 과거 기사 없음")
               return "이 뉴스는 최근에 등장한 새로운 이슈입니다."

           # 3. 타임라인 생성
           related_text = "\n\n".join([
               f"[{rel.published_at.strftime('%Y-%m-%d')}] {rel.title}\n{rel.summary or rel.content[:200]}"
               for rel in unique_related[:5]
           ])

           prompt = f"""
           현재 뉴스와 관련된 과거 기사들을 바탕으로 이 이슈가 어떻게 발전해왔는지
           시계열 타임라인으로 설명해주세요.

           현재 뉴스:
           제목: {article.title}
           내용: {article.content[:300]}

           과거 관련 기사:
           {related_text}

           타임라인 (3~5문장):
           """

           try:
               response = self.model.generate_content(prompt)
               timeline = response.text.strip()
               self.logger.info(f"✅ 타임라인 생성 완료")
               return timeline
           except Exception as e:
               self.logger.error(f"❌ 타임라인 생성 실패: {e}")
               return ""
   ```

3. `test_context.py` 작성
   ```python
   from utils.file_manager import FileManager
   from analyzers.context_builder import ContextBuilder
   from database.db_manager import DatabaseManager

   if __name__ == '__main__':
       # 과거 기사들을 DB에 저장 (최초 1회)
       file_manager = FileManager()
       db = DatabaseManager()

       # 이전에 수집한 기사들 로드
       articles = file_manager.load_articles('cleaned_news_20250110_120000.json')
       for article in articles:
           db.insert_article(article)

       print(f"✅ {len(articles)}개 기사 DB 저장 완료\n")

       # 새 기사의 타임라인 생성
       context_builder = ContextBuilder()
       new_article = articles[0]  # 테스트용

       timeline = context_builder.build_timeline(new_article)
       print(f"타임라인:\n{timeline}")
   ```

**성공 기준:**
- `database/news.db` 파일 생성
- 과거 기사 검색 동작
- 타임라인 텍스트 생성

---

### Step 2.5: 중요도 점수 계산
**목표:** 수집된 뉴스 중 상위 5개 선정
**소요 시간:** 1.5시간

**세부 작업:**

1. `analyzers/importance_ranker.py` 작성
   ```python
   from typing import List
   from models.news_article import NewsArticle
   import re

   class ImportanceRanker:
       # 중요 키워드 (가중치 부여)
       HIGH_PRIORITY_KEYWORDS = {
           '한국은행': 3,
           '기준금리': 3,
           '환율': 2,
           '주가': 2,
           '코스피': 2,
           'GDP': 3,
           '무역수지': 2,
           '실업률': 2,
           '물가': 2,
           '인플레이션': 3
       }

       @staticmethod
       def calculate_score(article: NewsArticle) -> float:
           """기사 중요도 점수 계산"""
           score = 0.0

           # 1. 키워드 매칭 (제목 2배 가중치)
           title_lower = article.title.lower()
           content_lower = article.content.lower()

           for keyword, weight in ImportanceRanker.HIGH_PRIORITY_KEYWORDS.items():
               if keyword.lower() in title_lower:
                   score += weight * 2
               elif keyword.lower() in content_lower:
                   score += weight

           # 2. 본문 길이 (너무 짧거나 길면 감점)
           content_len = len(article.content)
           if 500 <= content_len <= 3000:
               score += 1

           # 3. 숫자/데이터 포함 여부 (통계 기사 우대)
           numbers = re.findall(r'\d+\.?\d*%?', article.content)
           if len(numbers) >= 3:
               score += 1

           return score

       @staticmethod
       def rank_articles(articles: List[NewsArticle], top_n: int = 5) -> List[NewsArticle]:
           """기사들을 중요도 순으로 정렬 후 상위 N개 반환"""
           # 점수 계산
           scored_articles = [(article, ImportanceRanker.calculate_score(article)) for article in articles]

           # 정렬
           scored_articles.sort(key=lambda x: x[1], reverse=True)

           # 상위 N개 반환
           top_articles = [article for article, score in scored_articles[:top_n]]

           print(f"중요도 랭킹:")
           for i, (article, score) in enumerate(scored_articles[:top_n], 1):
               print(f"  {i}. [{score:.1f}점] {article.title[:40]}")

           return top_articles
   ```

2. `test_ranking.py` 작성
   ```python
   from utils.file_manager import FileManager
   from analyzers.importance_ranker import ImportanceRanker

   if __name__ == '__main__':
       file_manager = FileManager()
       articles = file_manager.load_articles('cleaned_news_20250110_120000.json')

       print(f"총 {len(articles)}개 기사 중 상위 5개 선정:\n")
       top_articles = ImportanceRanker.rank_articles(articles, top_n=5)

       # 결과 저장
       file_manager.save_articles(top_articles, 'top_news.json')
   ```

**성공 기준:**
- 점수 기반 정렬 동작
- 상위 5개 선정
- 점수와 제목 출력

---

## Phase 3: 데이터 시각화 (Week 3)

### Step 3.1: 기본 그래프 생성 (더미 데이터)
**목표:** Matplotlib으로 선 그래프 PNG 생성
**소요 시간:** 45분

**세부 작업:**

1. `requirements.txt`에 추가
   ```
   matplotlib==3.8.3
   plotly==5.19.0
   ```

2. `visualizers/chart_generator.py` 작성
   ```python
   import matplotlib.pyplot as plt
   import matplotlib.dates as mdates
   from datetime import datetime, timedelta
   import os

   class ChartGenerator:
       def __init__(self, output_dir: str = './data/charts'):
           self.output_dir = output_dir
           os.makedirs(output_dir, exist_ok=True)

           # 한글 폰트 설정 (Windows)
           plt.rcParams['font.family'] = 'Malgun Gothic'
           plt.rcParams['axes.unicode_minus'] = False

       def create_line_chart(
           self,
           dates: list[datetime],
           values: list[float],
           title: str,
           ylabel: str,
           filename: str
       ) -> str:
           """선 그래프 생성"""
           fig, ax = plt.subplots(figsize=(10, 6))

           # 그래프 그리기
           ax.plot(dates, values, marker='o', linewidth=2, markersize=6)

           # 제목 및 라벨
           ax.set_title(title, fontsize=16, fontweight='bold')
           ax.set_ylabel(ylabel, fontsize=12)
           ax.set_xlabel('날짜', fontsize=12)

           # 날짜 포맷
           ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
           ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
           plt.xticks(rotation=45)

           # 그리드
           ax.grid(True, alpha=0.3)

           # 레이아웃 조정
           plt.tight_layout()

           # 저장
           filepath = os.path.join(self.output_dir, filename)
           plt.savefig(filepath, dpi=300, bbox_inches='tight')
           plt.close()

           print(f"✅ 그래프 저장: {filepath}")
           return filepath
   ```

3. `test_chart.py` 작성
   ```python
   from visualizers.chart_generator import ChartGenerator
   from datetime import datetime, timedelta

   if __name__ == '__main__':
       # 더미 데이터 생성
       start_date = datetime(2025, 1, 1)
       dates = [start_date + timedelta(days=i) for i in range(30)]
       values = [1300 + i * 2 + (i % 5) * 10 for i in range(30)]  # 환율 가정

       # 그래프 생성
       chart_gen = ChartGenerator()
       chart_gen.create_line_chart(
           dates=dates,
           values=values,
           title='최근 30일 원/달러 환율 추이',
           ylabel='환율 (원)',
           filename='test_exchange_rate.png'
       )

       print("그래프 파일을 확인하세요: data/charts/test_exchange_rate.png")
   ```

4. 실행
   ```bash
   pip install matplotlib plotly
   python test_chart.py
   ```

**성공 기준:**
- `data/charts/test_exchange_rate.png` 생성
- 한글 제목 정상 표시
- 선 그래프 시각적으로 깔끔

---

### Step 3.2: 실제 경제 데이터 수집 (환율)
**목표:** 한국은행 Open API 또는 Yahoo Finance에서 실제 환율 데이터 가져오기
**소요 시간:** 2시간

**세부 작업:**

1. `requirements.txt`에 추가
   ```
   yfinance==0.2.36
   ```

2. `visualizers/data_fetcher.py` 작성
   ```python
   import yfinance as yf
   from datetime import datetime, timedelta
   from typing import Tuple, List
   from utils.logger import setup_logger

   class EconomicDataFetcher:
       def __init__(self):
           self.logger = setup_logger(self.__class__.__name__)

       def get_exchange_rate(
           self,
           days: int = 30,
           currency_pair: str = 'KRW=X'  # USD/KRW
       ) -> Tuple[List[datetime], List[float]]:
           """환율 데이터 가져오기"""
           try:
               end_date = datetime.now()
               start_date = end_date - timedelta(days=days)

               # Yahoo Finance에서 데이터 가져오기
               ticker = yf.Ticker(currency_pair)
               hist = ticker.history(start=start_date, end=end_date)

               # 날짜와 종가 추출
               dates = [date.to_pydatetime() for date in hist.index]
               values = hist['Close'].tolist()

               self.logger.info(f"✅ 환율 데이터 {len(dates)}개 수집")
               return dates, values
           except Exception as e:
               self.logger.error(f"❌ 환율 데이터 수집 실패: {e}")
               raise

       def get_kospi(self, days: int = 30) -> Tuple[List[datetime], List[float]]:
           """코스피 지수 데이터"""
           try:
               end_date = datetime.now()
               start_date = end_date - timedelta(days=days)

               ticker = yf.Ticker('^KS11')  # KOSPI
               hist = ticker.history(start=start_date, end=end_date)

               dates = [date.to_pydatetime() for date in hist.index]
               values = hist['Close'].tolist()

               self.logger.info(f"✅ 코스피 데이터 {len(dates)}개 수집")
               return dates, values
           except Exception as e:
               self.logger.error(f"❌ 코스피 데이터 수집 실패: {e}")
               raise
   ```

3. `test_real_chart.py` 작성
   ```python
   from visualizers.chart_generator import ChartGenerator
   from visualizers.data_fetcher import EconomicDataFetcher

   if __name__ == '__main__':
       # 실제 데이터 수집
       fetcher = EconomicDataFetcher()
       dates, values = fetcher.get_exchange_rate(days=30)

       # 그래프 생성
       chart_gen = ChartGenerator()
       chart_gen.create_line_chart(
           dates=dates,
           values=values,
           title='최근 30일 원/달러 환율 추이 (실제 데이터)',
           ylabel='환율 (원)',
           filename='real_exchange_rate.png'
       )

       # 코스피도 생성
       kospi_dates, kospi_values = fetcher.get_kospi(days=30)
       chart_gen.create_line_chart(
           dates=kospi_dates,
           values=kospi_values,
           title='최근 30일 코스피 지수',
           ylabel='지수',
           filename='kospi_index.png'
       )
   ```

**성공 기준:**
- 실제 환율 데이터로 그래프 생성
- 코스피 지수 그래프 생성

---

### Step 3.3: 뉴스 키워드 기반 자동 그래프 선택
**목표:** 뉴스 내용을 분석해 적절한 그래프 자동 생성
**소요 시간:** 2시간

**세부 작업:**

1. `visualizers/auto_visualizer.py` 작성
   ```python
   from models.news_article import NewsArticle
   from visualizers.data_fetcher import EconomicDataFetcher
   from visualizers.chart_generator import ChartGenerator
   from typing import Optional
   from utils.logger import setup_logger

   class AutoVisualizer:
       # 키워드별 시각화 매핑
       KEYWORD_TO_CHART = {
           '환율': ('exchange_rate', '원/달러 환율'),
           '달러': ('exchange_rate', '원/달러 환율'),
           '코스피': ('kospi', '코스피 지수'),
           '주가': ('kospi', '코스피 지수'),
           '증시': ('kospi', '코스피 지수'),
       }

       def __init__(self):
           self.fetcher = EconomicDataFetcher()
           self.chart_gen = ChartGenerator()
           self.logger = setup_logger(self.__class__.__name__)

       def detect_chart_type(self, article: NewsArticle) -> Optional[tuple[str, str]]:
           """기사 내용을 분석해 적절한 차트 타입 감지"""
           text = (article.title + ' ' + article.content).lower()

           for keyword, (chart_type, title) in self.KEYWORD_TO_CHART.items():
               if keyword in text:
                   self.logger.info(f"키워드 '{keyword}' 감지 → {chart_type} 차트")
                   return chart_type, title

           return None

       def generate_chart_for_article(self, article: NewsArticle) -> Optional[str]:
           """기사에 적합한 차트 자동 생성"""
           chart_info = self.detect_chart_type(article)

           if not chart_info:
               self.logger.info("적합한 차트 없음")
               return None

           chart_type, title = chart_info

           try:
               if chart_type == 'exchange_rate':
                   dates, values = self.fetcher.get_exchange_rate(days=30)
                   ylabel = '환율 (원)'
               elif chart_type == 'kospi':
                   dates, values = self.fetcher.get_kospi(days=30)
                   ylabel = '지수'
               else:
                   return None

               # 파일명 생성 (기사 제목 기반)
               safe_title = "".join(c for c in article.title[:30] if c.isalnum() or c in (' ', '_')).rstrip()
               filename = f"{safe_title}_{chart_type}.png"

               # 차트 생성
               filepath = self.chart_gen.create_line_chart(
                   dates=dates,
                   values=values,
                   title=title,
                   ylabel=ylabel,
                   filename=filename
               )

               return filepath
           except Exception as e:
               self.logger.error(f"차트 생성 실패: {e}")
               return None
   ```

2. `test_auto_visualizer.py` 작성
   ```python
   from utils.file_manager import FileManager
   from visualizers.auto_visualizer import AutoVisualizer

   if __name__ == '__main__':
       file_manager = FileManager()
       articles = file_manager.load_articles('top_news.json')

       auto_viz = AutoVisualizer()

       for article in articles:
           print(f"\n기사: {article.title}")
           chart_path = auto_viz.generate_chart_for_article(article)
           if chart_path:
               print(f"  ✅ 차트 생성: {chart_path}")
           else:
               print(f"  ⚠️  적합한 차트 없음")
   ```

**성공 기준:**
- 환율 관련 뉴스 → 환율 그래프 자동 생성
- 주가 관련 뉴스 → 코스피 그래프 자동 생성
- 매칭 안 되면 None 반환

---

## Phase 4: 웹 페이지 생성 (Week 3-4)

### Step 4.1: HTML 템플릿 디자인
**목표:** 보기 좋은 HTML 템플릿 작성
**소요 시간:** 2시간

**세부 작업:**

1. `templates/base.html` 작성
   ```html
   <!DOCTYPE html>
   <html lang="ko">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>{{ title }} | Spread Insight</title>
       <style>
           * {
               margin: 0;
               padding: 0;
               box-sizing: border-box;
           }

           body {
               font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, sans-serif;
               line-height: 1.6;
               color: #333;
               background: #f5f5f5;
           }

           .container {
               max-width: 800px;
               margin: 0 auto;
               padding: 20px;
               background: white;
               box-shadow: 0 2px 10px rgba(0,0,0,0.1);
           }

           header {
               border-bottom: 3px solid #007bff;
               margin-bottom: 30px;
               padding-bottom: 20px;
           }

           h1 {
               font-size: 2em;
               color: #222;
               margin-bottom: 10px;
           }

           .meta {
               color: #666;
               font-size: 0.9em;
           }

           .summary {
               background: #e3f2fd;
               padding: 20px;
               border-left: 4px solid #007bff;
               margin: 30px 0;
               font-size: 1.1em;
           }

           .content {
               font-size: 1.05em;
               line-height: 1.8;
               margin: 30px 0;
           }

           .terminology {
               background: #fff3cd;
               padding: 20px;
               margin: 30px 0;
               border-radius: 5px;
           }

           .terminology h2 {
               font-size: 1.3em;
               margin-bottom: 15px;
               color: #856404;
           }

           .term-item {
               margin-bottom: 10px;
           }

           .term-word {
               font-weight: bold;
               color: #856404;
           }

           .timeline {
               background: #f8f9fa;
               padding: 20px;
               margin: 30px 0;
               border-left: 4px solid #28a745;
           }

           .timeline h2 {
               font-size: 1.3em;
               margin-bottom: 15px;
               color: #155724;
           }

           .chart {
               margin: 30px 0;
               text-align: center;
           }

           .chart img {
               max-width: 100%;
               height: auto;
               border: 1px solid #ddd;
           }

           .coupang-link {
               display: block;
               background: #ff6f61;
               color: white;
               text-align: center;
               padding: 15px;
               text-decoration: none;
               border-radius: 5px;
               font-size: 1.1em;
               font-weight: bold;
               margin: 30px 0;
           }

           .coupang-link:hover {
               background: #e55a50;
           }

           footer {
               margin-top: 50px;
               padding-top: 20px;
               border-top: 1px solid #ddd;
               text-align: center;
               color: #666;
               font-size: 0.9em;
           }
       </style>
   </head>
   <body>
       <div class="container">
           <header>
               <h1>{{ title }}</h1>
               <div class="meta">
                   {{ source }} | {{ date }}
               </div>
           </header>

           {% if summary %}
           <div class="summary">
               <strong>📌 한줄 요약</strong><br>
               {{ summary }}
           </div>
           {% endif %}

           {% if chart_path %}
           <div class="chart">
               <img src="{{ chart_path }}" alt="관련 차트">
           </div>
           {% endif %}

           <div class="content">
               <h2>쉽게 풀어보기</h2>
               {{ easy_explanation }}
           </div>

           {% if timeline %}
           <div class="timeline">
               <h2>📅 이슈 타임라인</h2>
               {{ timeline }}
           </div>
           {% endif %}

           {% if terminology %}
           <div class="terminology">
               <h2>💡 용어 해설</h2>
               {% for term, explanation in terminology.items() %}
               <div class="term-item">
                   <span class="term-word">{{ term }}</span>: {{ explanation }}
               </div>
               {% endfor %}
           </div>
           {% endif %}

           {% if coupang_link %}
           <a href="{{ coupang_link }}" target="_blank" class="coupang-link">
               🛒 관련 추천 상품 보러가기
           </a>
           {% endif %}

           <footer>
               <p>이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
               <p>&copy; 2025 Spread Insight. All rights reserved.</p>
           </footer>
       </div>
   </body>
   </html>
   ```

2. `publishers/html_generator.py` 작성
   ```python
   from jinja2 import Template
   from models.news_article import NewsArticle
   from typing import Optional
   import os
   from utils.logger import setup_logger

   class HTMLGenerator:
       def __init__(self, template_path: str = './templates/base.html', output_dir: str = './data/html'):
           self.template_path = template_path
           self.output_dir = output_dir
           os.makedirs(output_dir, exist_ok=True)
           self.logger = setup_logger(self.__class__.__name__)

           # 템플릿 로드
           with open(template_path, 'r', encoding='utf-8') as f:
               self.template = Template(f.read())

       def generate(
           self,
           article: NewsArticle,
           chart_path: Optional[str] = None,
           timeline: Optional[str] = None,
           coupang_link: Optional[str] = None
       ) -> str:
           """HTML 파일 생성"""
           # 파일명 생성
           safe_title = "".join(c for c in article.title[:50] if c.isalnum() or c in (' ', '_')).rstrip()
           filename = f"{safe_title}.html".replace(' ', '_')
           filepath = os.path.join(self.output_dir, filename)

           # HTML 렌더링
           html_content = self.template.render(
               title=article.title,
               source=article.source,
               date=article.published_at.strftime('%Y년 %m월 %d일'),
               summary=article.summary,
               easy_explanation=article.easy_explanation,
               timeline=timeline,
               terminology=article.terminology,
               chart_path=os.path.basename(chart_path) if chart_path else None,
               coupang_link=coupang_link
           )

           # 파일 저장
           with open(filepath, 'w', encoding='utf-8') as f:
               f.write(html_content)

           self.logger.info(f"✅ HTML 생성: {filepath}")
           return filepath
   ```

3. `requirements.txt`에 추가
   ```
   jinja2==3.1.3
   ```

4. `test_html.py` 작성
   ```python
   from utils.file_manager import FileManager
   from publishers.html_generator import HTMLGenerator

   if __name__ == '__main__':
       file_manager = FileManager()
       articles = file_manager.load_articles('top_news.json')

       html_gen = HTMLGenerator()

       # 첫 번째 기사 HTML 생성
       article = articles[0]
       html_path = html_gen.generate(
           article=article,
           chart_path='./data/charts/test_exchange_rate.png',
           timeline='이것은 테스트 타임라인입니다.',
           coupang_link='https://www.coupang.com/np/search?q=test'
       )

       print(f"HTML 파일을 브라우저로 열어보세요: {html_path}")
   ```

**성공 기준:**
- HTML 파일 생성
- 브라우저에서 보기 좋게 표시
- 한글 깨짐 없음

---

### Step 4.2: GitHub Pages 배포
**목표:** 생성된 HTML을 인터넷에 공개
**소요 시간:** 1.5시간

**세부 작업:**

1. GitHub 저장소 생성
   - `spread-insight-pages` 이름으로 public 저장소 생성

2. `publishers/github_deployer.py` 작성
   ```python
   import os
   import subprocess
   from utils.logger import setup_logger
   from typing import List

   class GitHubDeployer:
       def __init__(self, repo_dir: str = './github_pages'):
           self.repo_dir = repo_dir
           self.logger = setup_logger(self.__class__.__name__)

       def setup_repo(self, repo_url: str):
           """저장소 초기 설정 (최초 1회)"""
           if not os.path.exists(self.repo_dir):
               # 클론
               subprocess.run(['git', 'clone', repo_url, self.repo_dir], check=True)
               self.logger.info(f"✅ 저장소 클론 완료")
           else:
               # Pull
               subprocess.run(['git', '-C', self.repo_dir, 'pull'], check=True)
               self.logger.info(f"✅ 저장소 업데이트 완료")

       def deploy(self, html_files: List[str], chart_files: List[str]):
           """HTML 및 차트 파일 배포"""
           # HTML 파일 복사
           for html_file in html_files:
               dest = os.path.join(self.repo_dir, os.path.basename(html_file))
               subprocess.run(['cp', html_file, dest], check=True)
               self.logger.info(f"✅ 복사: {html_file}")

           # 차트 파일 복사
           charts_dir = os.path.join(self.repo_dir, 'charts')
           os.makedirs(charts_dir, exist_ok=True)
           for chart_file in chart_files:
               dest = os.path.join(charts_dir, os.path.basename(chart_file))
               subprocess.run(['cp', chart_file, dest], check=True)

           # Git 커밋 및 푸시
           subprocess.run(['git', '-C', self.repo_dir, 'add', '.'], check=True)
           subprocess.run(['git', '-C', self.repo_dir, 'commit', '-m', 'Update news'], check=True)
           subprocess.run(['git', '-C', self.repo_dir, 'push'], check=True)

           self.logger.info(f"✅ GitHub Pages 배포 완료")
   ```

3. `test_deploy.py` 작성
   ```python
   from publishers.github_deployer import GitHubDeployer

   if __name__ == '__main__':
       deployer = GitHubDeployer()

       # 최초 1회 실행 (저장소 URL 입력)
       repo_url = 'https://github.com/YOUR_USERNAME/spread-insight-pages.git'
       deployer.setup_repo(repo_url)

       # 배포
       html_files = ['./data/html/test_article.html']
       chart_files = ['./data/charts/test_exchange_rate.png']
       deployer.deploy(html_files, chart_files)

       print("\n배포 완료! 다음 URL에서 확인하세요:")
       print("https://YOUR_USERNAME.github.io/spread-insight-pages/test_article.html")
   ```

**성공 기준:**
- GitHub Pages에서 HTML 접속 가능
- 이미지 정상 표시

---

## Phase 5: 텔레그램 연동 (Week 4)

### Step 5.1: 텔레그램 봇 생성 및 메시지 전송
**목표:** "Hello World" 메시지 전송
**소요 시간:** 1시간

**세부 작업:**

1. 텔레그램 봇 생성
   - 텔레그램에서 @BotFather 검색
   - `/newbot` 명령어
   - 봇 이름 입력
   - 토큰 복사 → `.env`에 저장

2. `.env`에 추가
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

3. `publishers/telegram_bot.py` 작성
   ```python
   from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
   from utils.config import Config
   from utils.logger import setup_logger
   import asyncio

   class TelegramPublisher:
       def __init__(self):
           self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
           self.logger = setup_logger(self.__class__.__name__)

       async def send_message(self, chat_id: str, text: str):
           """단순 메시지 전송"""
           try:
               await self.bot.send_message(chat_id=chat_id, text=text)
               self.logger.info(f"✅ 메시지 전송 완료")
           except Exception as e:
               self.logger.error(f"❌ 메시지 전송 실패: {e}")

       async def send_news(
           self,
           chat_id: str,
           title: str,
           summary: str,
           detail_url: str,
           coupang_url: str
       ):
           """뉴스 메시지 (버튼 포함) 전송"""
           message = f"📰 <b>{title}</b>\n\n{summary}"

           # 버튼 생성
           keyboard = [
               [InlineKeyboardButton("📄 상세 인사이트 보기", url=detail_url)],
               [InlineKeyboardButton("🛒 관련 상품 보기", url=coupang_url)]
           ]
           reply_markup = InlineKeyboardMarkup(keyboard)

           try:
               await self.bot.send_message(
                   chat_id=chat_id,
                   text=message,
                   parse_mode='HTML',
                   reply_markup=reply_markup
               )
               self.logger.info(f"✅ 뉴스 전송 완료: {title}")
           except Exception as e:
               self.logger.error(f"❌ 뉴스 전송 실패: {e}")
   ```

4. `test_telegram.py` 작성
   ```python
   from publishers.telegram_bot import TelegramPublisher
   from utils.config import Config
   import asyncio

   async def main():
       bot = TelegramPublisher()

       # 단순 메시지 테스트
       await bot.send_message(
           chat_id=Config.TELEGRAM_CHAT_ID,
           text="Hello World from Spread Insight!"
       )

       # 뉴스 메시지 테스트
       await bot.send_news(
           chat_id=Config.TELEGRAM_CHAT_ID,
           title="환율 급등, 달러당 1400원 돌파",
           summary="최근 미국 금리 인상으로 원/달러 환율이 1400원을 넘어섰습니다.",
           detail_url="https://YOUR_USERNAME.github.io/spread-insight-pages/test.html",
           coupang_url="https://www.coupang.com/np/search?q=환전"
       )

   if __name__ == '__main__':
       asyncio.run(main())
   ```

5. 실행
   ```bash
   pip install python-telegram-bot
   python test_telegram.py
   ```

**성공 기준:**
- 텔레그램에 메시지 도착
- 버튼 클릭 시 URL 이동

---

### Step 5.2: 구독자 관리
**목표:** 여러 사용자에게 일괄 전송
**소요 시간:** 1시간

**세부 작업:**

1. `database/subscriber_manager.py` 작성
   ```python
   import sqlite3
   from typing import List

   class SubscriberManager:
       def __init__(self, db_path: str = './database/news.db'):
           self.db_path = db_path
           self._create_table()

       def _create_table(self):
           """구독자 테이블 생성"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS subscribers (
                   chat_id TEXT PRIMARY KEY,
                   username TEXT,
                   subscribed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                   active INTEGER DEFAULT 1
               )
           ''')
           conn.commit()
           conn.close()

       def add_subscriber(self, chat_id: str, username: str = None):
           """구독자 추가"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           cursor.execute('''
               INSERT OR IGNORE INTO subscribers (chat_id, username)
               VALUES (?, ?)
           ''', (chat_id, username))
           conn.commit()
           conn.close()

       def get_active_subscribers(self) -> List[str]:
           """활성 구독자 목록"""
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           cursor.execute('SELECT chat_id FROM subscribers WHERE active = 1')
           rows = cursor.fetchall()
           conn.close()
           return [row[0] for row in rows]
   ```

2. `publishers/telegram_bot.py`에 추가
   ```python
   async def broadcast_news(
       self,
       subscribers: List[str],
       title: str,
       summary: str,
       detail_url: str,
       coupang_url: str
   ):
       """여러 구독자에게 뉴스 전송"""
       for chat_id in subscribers:
           await self.send_news(chat_id, title, summary, detail_url, coupang_url)
           await asyncio.sleep(0.5)  # 스팸 방지 딜레이

       self.logger.info(f"✅ {len(subscribers)}명에게 전송 완료")
   ```

**성공 기준:**
- 구독자 DB 관리
- 여러 사용자에게 동시 전송

---

## Phase 6: 쿠팡 파트너스 통합 (Week 4)

### Step 6.1: 쿠팡 링크 생성
**목표:** 뉴스 키워드 기반 쿠팡 상품 링크 생성
**소요 시간:** 2시간

**세부 작업:**

1. `publishers/coupang_partner.py` 작성
   ```python
   from typing import Optional
   from utils.logger import setup_logger

   class CoupangPartner:
       # 키워드 → 상품 검색어 매핑
       KEYWORD_TO_PRODUCT = {
           '환율': '여행 가방',
           '달러': '환전',
           '주가': '재테크 책',
           '부동산': '인테리어',
           '금리': '적금 통장',
       }

       def __init__(self, partner_id: str = 'YOUR_PARTNER_ID'):
           self.partner_id = partner_id
           self.base_url = 'https://www.coupang.com/np/search'
           self.logger = setup_logger(self.__class__.__name__)

       def generate_link(self, keywords: list[str]) -> Optional[str]:
           """키워드 기반 쿠팡 링크 생성"""
           # 키워드 매칭
           for keyword in keywords:
               if keyword in self.KEYWORD_TO_PRODUCT:
                   product_query = self.KEYWORD_TO_PRODUCT[keyword]
                   link = f"{self.base_url}?q={product_query}&channel=user"
                   self.logger.info(f"✅ 쿠팡 링크 생성: {keyword} → {product_query}")
                   return link

           # 기본 링크 (매칭 안 될 경우)
           default_link = f"{self.base_url}?q=생활용품&channel=user"
           return default_link
   ```

2. `test_coupang.py` 작성
   ```python
   from publishers.coupang_partner import CoupangPartner

   if __name__ == '__main__':
       coupang = CoupangPartner()

       test_keywords = ['환율', '금리', '부동산']

       for keywords in [test_keywords[:1], test_keywords[1:2], ['알수없음']]:
           link = coupang.generate_link(keywords)
           print(f"키워드: {keywords} → 링크: {link}")
   ```

**성공 기준:**
- 키워드별 다른 상품 링크 생성
- 매칭 안 될 경우 기본 링크

---

## Phase 7: 전체 통합 및 자동화 (Week 5)

### Step 7.1: 메인 파이프라인 구축
**목표:** 전체 워크플로우를 1번에 실행
**소요 시간:** 3시간

**세부 작업:**

1. `main.py` 작성
   ```python
   from scrapers.naver_scraper import NaverScraper
   from scrapers.daum_scraper import DaumScraper
   from analyzers.gemini_analyzer import GeminiAnalyzer
   from analyzers.context_builder import ContextBuilder
   from analyzers.importance_ranker import ImportanceRanker
   from visualizers.auto_visualizer import AutoVisualizer
   from publishers.html_generator import HTMLGenerator
   from publishers.telegram_bot import TelegramPublisher
   from publishers.coupang_partner import CoupangPartner
   from publishers.github_deployer import GitHubDeployer
   from database.db_manager import DatabaseManager
   from database.subscriber_manager import SubscriberManager
   from utils.data_cleaner import DataCleaner
   from utils.logger import setup_logger
   import asyncio

   class SpreadInsight:
       def __init__(self):
           self.logger = setup_logger('SpreadInsight')

           # 컴포넌트 초기화
           self.scrapers = [NaverScraper(), DaumScraper()]
           self.analyzer = GeminiAnalyzer()
           self.context_builder = ContextBuilder()
           self.visualizer = AutoVisualizer()
           self.html_gen = HTMLGenerator()
           self.telegram = TelegramPublisher()
           self.coupang = CoupangPartner()
           self.deployer = GitHubDeployer()
           self.db = DatabaseManager()
           self.sub_manager = SubscriberManager()

       async def run(self):
           """전체 파이프라인 실행"""
           self.logger.info("=== Spread Insight 시작 ===")

           # 1. 뉴스 수집
           self.logger.info("1단계: 뉴스 수집")
           all_articles = []
           for scraper in self.scrapers:
               urls = scraper.get_article_list(limit=5)
               for url in urls:
                   try:
                       article = scraper.scrape_with_retry(url)
                       all_articles.append(article)
                   except Exception as e:
                       self.logger.error(f"스크래핑 실패: {e}")

           # 2. 데이터 정제
           self.logger.info("2단계: 데이터 정제")
           articles = DataCleaner.clean(all_articles)

           # 3. 중요도 랭킹
           self.logger.info("3단계: 중요도 랭킹")
           top_articles = ImportanceRanker.rank_articles(articles, top_n=5)

           # 4. AI 분석
           self.logger.info("4단계: AI 분석")
           for article in top_articles:
               # 요약
               article.summary = self.analyzer.summarize(article)

               # 쉬운 설명
               article.easy_explanation = self.analyzer.simplify_language(article)

               # 용어 해설
               from analyzers.terminology import TerminologyExtractor
               term_extractor = TerminologyExtractor()
               article.terminology = term_extractor.extract_and_explain(article.content)

               # DB 저장
               self.db.insert_article(article)

           # 5. 시각화 및 HTML 생성
           self.logger.info("5단계: 시각화 및 HTML 생성")
           html_files = []
           chart_files = []

           for article in top_articles:
               # 타임라인
               timeline = self.context_builder.build_timeline(article)

               # 차트
               chart_path = self.visualizer.generate_chart_for_article(article)
               if chart_path:
                   chart_files.append(chart_path)

               # 쿠팡 링크
               coupang_link = self.coupang.generate_link(article.keywords or [])

               # HTML 생성
               html_path = self.html_gen.generate(
                   article=article,
                   chart_path=chart_path,
                   timeline=timeline,
                   coupang_link=coupang_link
               )
               html_files.append(html_path)

           # 6. GitHub Pages 배포
           self.logger.info("6단계: GitHub Pages 배포")
           self.deployer.deploy(html_files, chart_files)

           # 7. 텔레그램 전송
           self.logger.info("7단계: 텔레그램 전송")
           subscribers = self.sub_manager.get_active_subscribers()

           for i, article in enumerate(top_articles):
               detail_url = f"https://YOUR_USERNAME.github.io/spread-insight-pages/{os.path.basename(html_files[i])}"
               coupang_url = self.coupang.generate_link(article.keywords or [])

               await self.telegram.broadcast_news(
                   subscribers=subscribers,
                   title=article.title,
                   summary=article.summary,
                   detail_url=detail_url,
                   coupang_url=coupang_url
               )

           self.logger.info("=== 완료 ===")

   if __name__ == '__main__':
       app = SpreadInsight()
       asyncio.run(app.run())
   ```

2. 실행
   ```bash
   python main.py
   ```

**성공 기준:**
- 전체 파이프라인이 에러 없이 완료
- 텔레그램에 뉴스 도착
- GitHub Pages에 HTML 배포

---

### Step 7.2: 스케줄러 추가
**목표:** 매일 오전 7시, 오후 6시 자동 실행
**소요 시간:** 1시간

**세부 작업:**

1. `scheduler.py` 작성
   ```python
   from apscheduler.schedulers.blocking import BlockingScheduler
   from main import SpreadInsight
   import asyncio
   from utils.logger import setup_logger

   logger = setup_logger('Scheduler')

   def job():
       """스케줄러 작업"""
       logger.info("⏰ 스케줄러 작업 시작")
       app = SpreadInsight()
       asyncio.run(app.run())

   if __name__ == '__main__':
       scheduler = BlockingScheduler()

       # 매일 오전 7시, 오후 6시 실행
       scheduler.add_job(job, 'cron', hour=7, minute=0)
       scheduler.add_job(job, 'cron', hour=18, minute=0)

       logger.info("스케줄러 시작 (오전 7시, 오후 6시 실행)")

       try:
           scheduler.start()
       except (KeyboardInterrupt, SystemExit):
           logger.info("스케줄러 종료")
   ```

2. 백그라운드 실행 (Linux/Mac)
   ```bash
   nohup python scheduler.py > scheduler.log 2>&1 &
   ```

**성공 기준:**
- 설정한 시간에 자동 실행
- 로그 파일에 실행 기록

---

## 예상 비용 및 배포 옵션

### 비용
- **Gemini API:** 무료 할당량 내 (분당 15 요청)
- **GitHub Pages:** 무료
- **텔레그램 봇:** 무료
- **서버 (옵션):**
  - 로컬 PC: 무료
  - AWS EC2 t3.micro: ~$10/월
  - GCP Compute Engine f1-micro: 무료 (1개)

### 배포 옵션
1. **로컬 PC:** 가장 저렴, 24시간 켜둬야 함
2. **클라우드 VM:** 안정적, 월 $10 내외
3. **AWS Lambda:** 서버리스, 실행 시간만 과금

---

이상입니다! 각 단계를 작은 성공 단위로 쪼개서 하나씩 달성하면 됩니다.

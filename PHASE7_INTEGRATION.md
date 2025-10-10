# Phase 7: 전체 통합 및 자동화 (Week 5)

> 모든 컴포넌트를 하나로 통합하고 자동화

---

## ✅ Step 7.1: 메인 파이프라인 구축
**목표:** 전체 워크플로우를 1번에 실행
**소요 시간:** 3시간

### 📝 체크리스트
- [ ] `main.py` 작성
- [ ] 전체 파이프라인 통합
- [ ] 에러 핸들링
- [ ] 로깅

### 🛠️ 실행 순서

**1. 로거 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\utils\logger.py`
```python
import logging
import os
from datetime import datetime


def setup_logger(name: str = 'spread_insight', log_dir: str = './logs') -> logging.Logger:
    """로거 설정"""
    # 로그 디렉토리 생성
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일명 (날짜별)
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y%m%d")}.log')

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 중복 핸들러 방지
    if logger.handlers:
        return logger

    # 파일 핸들러
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 포매터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

**2. 메인 파이프라인 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\main.py`
```python
"""
Spread Insight - 경제 뉴스 인사이트 자동 생성 및 배포

전체 워크플로우:
1. 뉴스 수집 (네이버, 다음)
2. AI 분석 (요약, 쉬운 설명, 용어 해설, 타임라인)
3. 중요도 랭킹 (상위 5개 선정)
4. 시각화 (그래프 생성)
5. HTML 페이지 생성
6. GitHub Pages 배포
7. 텔레그램 전송
"""

import asyncio
from datetime import datetime

# Scrapers
from scrapers.naver_scraper import NaverScraper
from scrapers.daum_scraper import DaumScraper

# Analyzers
from analyzers.gemini_analyzer import GeminiAnalyzer
from analyzers.context_builder import ContextBuilder
from analyzers.importance_ranker import ImportanceRanker
from analyzers.terminology import TerminologyExtractor

# Visualizers
from visualizers.auto_visualizer import AutoVisualizer

# Publishers
from publishers.html_generator import HTMLGenerator
from publishers.telegram_bot import TelegramPublisher
from publishers.coupang_partner import CoupangPartner
from publishers.github_deployer import GitHubDeployer

# Database
from database.db_manager import DatabaseManager
from database.subscriber_manager import SubscriberManager

# Utils
from utils.file_manager import FileManager
from utils.logger import setup_logger
from utils.config import Config

import time


class SpreadInsight:
    """Spread Insight 메인 애플리케이션"""

    def __init__(self):
        self.logger = setup_logger('SpreadInsight')

        # 컴포넌트 초기화
        self.logger.info("컴포넌트 초기화 중...")

        self.scrapers = [NaverScraper(), DaumScraper()]
        self.analyzer = GeminiAnalyzer()
        self.context_builder = ContextBuilder()
        self.term_extractor = TerminologyExtractor()
        self.ranker = ImportanceRanker()
        self.visualizer = AutoVisualizer()
        self.html_gen = HTMLGenerator()
        self.telegram = TelegramPublisher()
        self.coupang = CoupangPartner()
        self.deployer = GitHubDeployer()
        self.db = DatabaseManager()
        self.sub_manager = SubscriberManager()
        self.file_manager = FileManager()

        self.logger.info("✅ 초기화 완료")

    async def run(self, num_articles: int = 5, github_username: str = None):
        """전체 파이프라인 실행

        Args:
            num_articles: 선정할 상위 뉴스 개수
            github_username: GitHub 사용자명 (URL 생성용)
        """
        start_time = time.time()
        self.logger.info("=" * 80)
        self.logger.info("🚀 Spread Insight 파이프라인 시작")
        self.logger.info("=" * 80)

        try:
            # ===== 1. 뉴스 수집 =====
            self.logger.info("\n📰 1단계: 뉴스 수집")
            all_articles = await self._collect_news()

            if not all_articles:
                self.logger.error("❌ 수집된 기사가 없습니다.")
                return

            self.logger.info(f"✅ 총 {len(all_articles)}개 기사 수집 완료")

            # ===== 2. 중요도 랭킹 =====
            self.logger.info("\n⭐ 2단계: 중요도 랭킹")
            top_articles = self.ranker.rank_articles(all_articles, top_n=num_articles)
            self.logger.info(f"✅ 상위 {len(top_articles)}개 선정 완료")

            # ===== 3. AI 분석 =====
            self.logger.info("\n🤖 3단계: AI 분석")
            await self._analyze_articles(top_articles)
            self.logger.info(f"✅ {len(top_articles)}개 기사 분석 완료")

            # DB 저장
            inserted = self.db.insert_articles(top_articles)
            self.logger.info(f"✅ {inserted}개 기사 DB 저장")

            # ===== 4. 시각화 =====
            self.logger.info("\n📊 4단계: 시각화")
            chart_paths = self._generate_charts(top_articles)
            self.logger.info(f"✅ {len([p for p in chart_paths.values() if p])}개 그래프 생성")

            # ===== 5. HTML 생성 =====
            self.logger.info("\n🌐 5단계: HTML 페이지 생성")
            html_files = self._generate_html(top_articles, chart_paths)
            self.logger.info(f"✅ {len(html_files)}개 HTML 생성")

            # ===== 6. GitHub Pages 배포 =====
            self.logger.info("\n🚀 6단계: GitHub Pages 배포")
            self._deploy_to_github(html_files, chart_paths)
            self.logger.info(f"✅ 배포 완료")

            # ===== 7. 텔레그램 전송 =====
            self.logger.info("\n📨 7단계: 텔레그램 전송")
            await self._send_to_telegram(top_articles, html_files, github_username)
            self.logger.info(f"✅ 전송 완료")

            # 완료
            elapsed = time.time() - start_time
            self.logger.info("\n" + "=" * 80)
            self.logger.info(f"✅ 파이프라인 완료 (소요 시간: {elapsed:.1f}초)")
            self.logger.info("=" * 80)

        except Exception as e:
            self.logger.error(f"❌ 파이프라인 실패: {e}", exc_info=True)
            raise

    async def _collect_news(self) -> list:
        """뉴스 수집"""
        all_articles = []

        for scraper in self.scrapers:
            scraper_name = scraper.__class__.__name__.replace('Scraper', '')
            self.logger.info(f"\n  [{scraper_name}] 수집 중...")

            try:
                urls = scraper.get_article_list(limit=5)
                self.logger.info(f"    URL {len(urls)}개 발견")

                for i, url in enumerate(urls, 1):
                    try:
                        article = scraper.scrape_article(url)
                        all_articles.append(article)
                        self.logger.info(f"    [{i}/{len(urls)}] {article.title[:40]}")
                        time.sleep(1)  # 서버 부담 방지
                    except Exception as e:
                        self.logger.warning(f"    ❌ {url}: {e}")

            except Exception as e:
                self.logger.error(f"  ❌ {scraper_name} 수집 실패: {e}")

        return all_articles

    async def _analyze_articles(self, articles: list):
        """AI 분석"""
        for i, article in enumerate(articles, 1):
            self.logger.info(f"\n  [{i}/{len(articles)}] {article.title[:40]}")

            try:
                # 요약
                if not article.summary:
                    article.summary = self.analyzer.summarize(article, num_sentences=3)
                    self.logger.info("    ✅ 요약 생성")

                # 쉬운 설명
                if not article.easy_explanation:
                    article.easy_explanation = self.analyzer.simplify_language(article)
                    self.logger.info("    ✅ 쉬운 설명 생성")

                # 용어 해설
                if not article.terminology:
                    article.terminology = self.term_extractor.extract_and_explain(article.content)
                    self.logger.info(f"    ✅ 용어 {len(article.terminology or {})}개 추출")

                # 키워드 추출 (타임라인용)
                if not article.keywords:
                    article.keywords = self.context_builder.extract_keywords(article)
                    self.logger.info(f"    ✅ 키워드: {', '.join(article.keywords)}")

                time.sleep(2)  # API 제한 방지

            except Exception as e:
                self.logger.error(f"    ❌ 분석 실패: {e}")

    def _generate_charts(self, articles: list) -> dict:
        """그래프 생성"""
        chart_paths = {}

        for i, article in enumerate(articles, 1):
            self.logger.info(f"  [{i}/{len(articles)}] {article.title[:40]}")

            try:
                chart_path = self.visualizer.generate_chart_for_article(article, days=30)
                chart_paths[article.url] = chart_path

                if chart_path:
                    self.logger.info(f"    ✅ 그래프 생성")
                else:
                    self.logger.info(f"    ⚠️  적합한 그래프 없음")

            except Exception as e:
                self.logger.error(f"    ❌ 그래프 생성 실패: {e}")
                chart_paths[article.url] = None

        return chart_paths

    def _generate_html(self, articles: list, chart_paths: dict) -> list:
        """HTML 페이지 생성"""
        html_files = []

        for i, article in enumerate(articles, 1):
            self.logger.info(f"  [{i}/{len(articles)}] {article.title[:40]}")

            try:
                # 타임라인 생성
                timeline = self.context_builder.build_timeline(article)

                # 쿠팡 링크 생성
                coupang_link = self.coupang.generate_link(keywords=article.keywords)

                # HTML 생성
                chart_path = chart_paths.get(article.url)
                html_path = self.html_gen.generate(
                    article=article,
                    chart_path=chart_path,
                    timeline=timeline,
                    coupang_link=coupang_link
                )

                html_files.append(html_path)

            except Exception as e:
                self.logger.error(f"    ❌ HTML 생성 실패: {e}")

        return html_files

    def _deploy_to_github(self, html_files: list, chart_paths: dict):
        """GitHub Pages 배포"""
        try:
            # 차트 파일 목록
            chart_files = [path for path in chart_paths.values() if path]

            self.deployer.deploy(
                html_files=html_files,
                chart_files=chart_files,
                commit_message=f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )

        except Exception as e:
            self.logger.warning(f"  ⚠️  배포 실패 (계속 진행): {e}")

    async def _send_to_telegram(self, articles: list, html_files: list, github_username: str):
        """텔레그램 전송"""
        try:
            # 구독자 목록
            subscribers = self.sub_manager.get_active_subscribers()
            self.logger.info(f"  구독자: {len(subscribers)}명")

            if not subscribers:
                self.logger.warning("  ⚠️  구독자가 없습니다.")
                return

            # 각 기사 전송
            for i, article in enumerate(articles):
                self.logger.info(f"\n  [{i+1}/{len(articles)}] {article.title[:40]}")

                # URL 생성
                if github_username and i < len(html_files):
                    import os
                    filename = os.path.basename(html_files[i])
                    detail_url = self.deployer.get_url(github_username, filename)
                else:
                    detail_url = f"https://example.com/news/{i+1}"

                # 쿠팡 링크
                coupang_url = self.coupang.generate_link(keywords=article.keywords)

                # 전송
                results = await self.telegram.broadcast_news(
                    chat_ids=subscribers,
                    title=article.title,
                    summary=article.summary or article.content[:200],
                    detail_url=detail_url,
                    coupang_url=coupang_url,
                    delay=1.0  # 스팸 방지
                )

                self.logger.info(f"    전송: 성공 {results['success']} / 실패 {results['fail']}")

                # 뉴스 간 딜레이
                if i < len(articles) - 1:
                    await asyncio.sleep(3)

        except Exception as e:
            self.logger.error(f"  ❌ 텔레그램 전송 실패: {e}")


async def main():
    """메인 함수"""
    app = SpreadInsight()

    # GitHub 사용자명 입력
    github_username = input("GitHub 사용자명 입력 (선택, Enter로 스킵): ").strip()
    if not github_username:
        github_username = None

    # 실행
    await app.run(num_articles=5, github_username=github_username)


if __name__ == '__main__':
    asyncio.run(main())
```

**3. 실행**
```bash
python main.py
```

### ✅ 성공 기준
- [ ] 전체 파이프라인 에러 없이 완료
- [ ] 로그 파일 생성 (`logs/YYYYMMDD.log`)
- [ ] 상위 5개 뉴스 선정
- [ ] AI 분석 완료
- [ ] HTML 및 그래프 생성
- [ ] 텔레그램 메시지 전송

---

## ✅ Step 7.2: 스케줄러 추가
**목표:** 매일 자동 실행
**소요 시간:** 1시간

### 🛠️ 실행 순서

**1. requirements.txt 업데이트**
```
# ... 기존 라이브러리들 ...
python-telegram-bot==20.8

# 스케줄러 추가
apscheduler==3.10.4
```

설치:
```bash
pip install apscheduler==3.10.4
```

**2. 스케줄러 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\scheduler.py`
```python
"""
Spread Insight 스케줄러

매일 지정된 시간에 자동으로 뉴스 수집 및 배포
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from main import SpreadInsight
from utils.logger import setup_logger
import asyncio


logger = setup_logger('Scheduler')


def job():
    """스케줄러 작업"""
    logger.info("=" * 80)
    logger.info("⏰ 스케줄 작업 시작")
    logger.info("=" * 80)

    try:
        app = SpreadInsight()

        # GitHub 사용자명 (환경변수 또는 설정 파일에서)
        github_username = "YOUR_GITHUB_USERNAME"  # 여기에 실제 사용자명 입력

        # 비동기 실행
        asyncio.run(app.run(num_articles=5, github_username=github_username))

        logger.info("✅ 스케줄 작업 완료")

    except Exception as e:
        logger.error(f"❌ 스케줄 작업 실패: {e}", exc_info=True)


if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("Spread Insight 스케줄러 시작")
    logger.info("=" * 80)

    scheduler = BlockingScheduler()

    # 매일 오전 7시 실행
    scheduler.add_job(
        job,
        trigger=CronTrigger(hour=7, minute=0),
        id='morning_news',
        name='아침 뉴스 (오전 7시)'
    )

    # 매일 오후 6시 실행
    scheduler.add_job(
        job,
        trigger=CronTrigger(hour=18, minute=0),
        id='evening_news',
        name='저녁 뉴스 (오후 6시)'
    )

    logger.info("\n스케줄 목록:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}: {job.next_run_time}")

    logger.info("\n스케줄러 실행 중... (Ctrl+C로 종료)")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n스케줄러 종료")
```

**3. 백그라운드 실행 (Windows)**

**방법 1: pythonw 사용**
```bash
# 백그라운드 실행 (콘솔 창 안 띄움)
pythonw scheduler.py
```

**방법 2: 작업 스케줄러 등록**
1. `작업 스케줄러` 실행
2. 우측 `작업 만들기` 클릭
3. 일반 탭:
   - 이름: `Spread Insight`
   - 최고 권한으로 실행 체크
4. 트리거 탭:
   - `새로 만들기` → 매일 → 시간 설정
5. 동작 탭:
   - 프로그램: `python.exe` 경로
   - 인수: `scheduler.py` 전체 경로
   - 시작 위치: 프로젝트 폴더
6. 확인

**방법 3: nohup (Linux/Mac)**
```bash
nohup python scheduler.py > scheduler.log 2>&1 &
```

### ✅ 성공 기준
- [ ] 스케줄러 정상 시작
- [ ] 설정한 시간에 자동 실행
- [ ] 로그 파일 생성

---

## ✅ Step 7.3: 최종 테스트 및 문서화
**목표:** 전체 시스템 테스트 및 README 작성
**소요 시간:** 2시간

### 🛠️ 실행 순서

**1. 최종 통합 테스트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_full_pipeline.py`
```python
"""
전체 파이프라인 통합 테스트
"""

import asyncio
from main import SpreadInsight


async def main():
    print("=" * 80)
    print("전체 파이프라인 통합 테스트")
    print("=" * 80)
    print("\n⚠️  실제 API 호출이 발생합니다.")
    print("   Gemini API 할당량 소모")
    print("   텔레그램 메시지 전송")
    print("   GitHub Pages 배포")

    confirm = input("\n계속하시겠습니까? (y/N): ").strip().lower()

    if confirm != 'y':
        print("테스트 취소")
        return

    # GitHub 사용자명
    github_username = input("\nGitHub 사용자명: ").strip()

    if not github_username:
        print("❌ GitHub 사용자명이 필요합니다.")
        return

    # 실행
    app = SpreadInsight()
    await app.run(num_articles=3, github_username=github_username)  # 테스트용 3개

    print("\n" + "=" * 80)
    print("✅ 통합 테스트 완료!")
    print("=" * 80)


if __name__ == '__main__':
    asyncio.run(main())
```

**2. README 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\README.md`
```markdown
# Spread Insight

경제 뉴스를 AI로 분석하여 쉽게 이해할 수 있는 인사이트를 제공하고, 텔레그램으로 자동 배포하는 시스템입니다.

## 주요 기능

- 📰 **뉴스 자동 수집** (네이버, 다음)
- 🤖 **AI 분석** (Gemini 2.0 Flash)
  - 3줄 요약
  - 쉬운 언어로 재작성
  - 전문 용어 자동 해설
  - 과거 맥락 타임라인
- 📊 **데이터 시각화** (환율, 주가 그래프)
- 🌐 **HTML 페이지 자동 생성** (GitHub Pages)
- 📨 **텔레그램 자동 배포**
- 🛒 **쿠팡 파트너스 연동**

## 설치

### 1. Python 환경
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```
GEMINI_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. GitHub 저장소 설정
```bash
# GitHub에서 저장소 생성 후
python
>>> from publishers.github_deployer import GitHubDeployer
>>> deployer = GitHubDeployer()
>>> deployer.setup_repo('https://github.com/username/spread-insight-pages.git')
```

## 사용법

### 수동 실행
```bash
python main.py
```

### 자동 실행 (스케줄러)
```bash
python scheduler.py
```

매일 오전 7시, 오후 6시에 자동 실행됩니다.

## 프로젝트 구조
```
spread_insight/
├── scrapers/          # 뉴스 수집
├── analyzers/         # AI 분석
├── visualizers/       # 그래프 생성
├── publishers/        # 배포 (HTML, 텔레그램)
├── database/          # 데이터베이스
├── utils/             # 유틸리티
├── templates/         # HTML 템플릿
├── main.py            # 메인 파이프라인
├── scheduler.py       # 스케줄러
└── README.md
```

## 라이선스
MIT License
```

**3. 실행**
```bash
python test_full_pipeline.py
```

### ✅ 성공 기준
- [ ] 전체 파이프라인 에러 없이 완료
- [ ] 뉴스 3개 처리
- [ ] 텔레그램 메시지 전송
- [ ] GitHub Pages 배포
- [ ] README.md 작성 완료

---

## 🎉🎉🎉 전체 프로젝트 완료! 🎉🎉🎉

### 다음 단계 (선택사항)

1. **성능 최적화**
   - 비동기 처리 확대
   - 캐싱 추가

2. **기능 확장**
   - 더 많은 뉴스 사이트
   - 카테고리별 분류
   - 사용자 피드백 수집

3. **배포 개선**
   - Docker 컨테이너화
   - 클라우드 배포 (AWS, GCP)
   - CI/CD 파이프라인

축하합니다! 🎊

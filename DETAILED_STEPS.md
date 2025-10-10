# 세부 실행 가이드 (스몰 석세스 기준)

> 각 단계는 **독립적으로 실행 및 테스트 가능**하며, 성공해야만 다음 단계로 진행합니다.

---

## 🚀 Phase 1: 뉴스 수집 (Week 1)

### ✅ Step 1.1: 프로젝트 초기 설정
**목표:** 개발 환경 구축 및 첫 파일 생성
**소요 시간:** 30분

#### 📝 체크리스트
- [ ] 폴더 구조 생성
- [ ] 가상환경 설정
- [ ] 의존성 설치
- [ ] .gitignore 작성
- [ ] .env 파일 생성

#### 🛠️ 실행 순서

**1-1. 터미널 열기 및 프로젝트 폴더로 이동**
```bash
cd "g:\내 드라이브\08.Programming\spread_insight"
```

**1-2. 폴더 구조 생성 (Windows PowerShell)**
```powershell
# 메인 폴더들
New-Item -ItemType Directory -Force -Path scrapers
New-Item -ItemType Directory -Force -Path analyzers
New-Item -ItemType Directory -Force -Path visualizers
New-Item -ItemType Directory -Force -Path publishers
New-Item -ItemType Directory -Force -Path models
New-Item -ItemType Directory -Force -Path database
New-Item -ItemType Directory -Force -Path utils
New-Item -ItemType Directory -Force -Path templates
New-Item -ItemType Directory -Force -Path templates\assets
New-Item -ItemType Directory -Force -Path data
New-Item -ItemType Directory -Force -Path data\raw
New-Item -ItemType Directory -Force -Path data\processed
New-Item -ItemType Directory -Force -Path data\charts
New-Item -ItemType Directory -Force -Path data\html
New-Item -ItemType Directory -Force -Path tests
New-Item -ItemType Directory -Force -Path logs

# __init__.py 파일 생성
New-Item -ItemType File -Force -Path scrapers\__init__.py
New-Item -ItemType File -Force -Path analyzers\__init__.py
New-Item -ItemType File -Force -Path visualizers\__init__.py
New-Item -ItemType File -Force -Path publishers\__init__.py
New-Item -ItemType File -Force -Path models\__init__.py
New-Item -ItemType File -Force -Path database\__init__.py
New-Item -ItemType File -Force -Path utils\__init__.py
```

**1-3. Git 초기화**
```bash
git init
```

**1-4. .gitignore 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# 환경 변수
.env

# 데이터
data/
*.db
*.json

# 로그
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# GitHub Pages 빌드
github_pages/

# 차트 이미지
*.png
*.jpg
```

**1-5. 가상환경 생성 (Python 3.10 이상 권장)**
```bash
python -m venv venv
```

**1-6. 가상환경 활성화**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

활성화되면 터미널 앞에 `(venv)` 표시됨

**1-7. requirements.txt 작성 (Phase 1용)**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\requirements.txt`
```
# Phase 1: 뉴스 수집
beautifulsoup4==4.12.3
requests==2.31.0
# lxml==5.1.0  # Python 3.13 호환성 문제로 제외 (html.parser 사용)
python-dotenv==1.0.1

# 나중에 추가할 라이브러리들 (주석 처리)
# google-generativeai==0.4.0
# matplotlib==3.8.3
# plotly==5.19.0
# yfinance==0.2.36
# python-telegram-bot==20.8
# jinja2==3.1.3
# apscheduler==3.10.4
# pandas==2.2.0
# numpy==1.26.4
# sqlalchemy==2.0.27
```

**1-8. 라이브러리 설치**
```bash
pip install -r requirements.txt
```

> **⚠️ 중요:** Python 3.13 환경에서 lxml 설치 시 "Microsoft Visual C++ 14.0 or greater is required" 오류가 발생할 수 있습니다. 이 경우 lxml 없이 BeautifulSoup의 내장 `html.parser`를 사용하면 됩니다. (Step 1.2 참조)

**1-9. .env 파일 생성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\.env`
```
# Gemini API (나중에 입력)
GEMINI_API_KEY=

# 텔레그램 (나중에 입력)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# 쿠팡 파트너스 (나중에 입력)
COUPANG_ACCESS_KEY=
COUPANG_SECRET_KEY=
COUPANG_PARTNER_ID=
```

#### ✅ 성공 기준
- [x] `venv` 폴더 생성됨
- [x] 터미널에 `(venv)` 표시
- [x] `pip list` 실행 시 beautifulsoup4, requests, python-dotenv 표시
- [x] 모든 폴더에 `__init__.py` 존재

#### ⚠️ 예상 오류 및 해결

**오류 1:** `python: command not found`
- **원인:** Python 미설치 또는 PATH 미등록
- **해결:** Python 3.10+ 설치 (https://www.python.org/downloads/)

**오류 2:** PowerShell 스크립트 실행 권한 오류
```
.\venv\Scripts\Activate.ps1 : 이 시스템에서 스크립트를 실행할 수 없으므로...
```
- **해결:** PowerShell 관리자 권한으로 실행 후
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**오류 3:** `pip install` 시 SSL 인증서 오류
- **해결:**
  ```bash
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
  ```

**오류 4:** `lxml` 설치 시 "Microsoft Visual C++ 14.0 or greater is required" ✅ 해결됨
- **원인:** Python 3.13에서 lxml 5.1.0 빌드 시 C++ 컴파일러 필요
- **해결:** lxml 없이 설치하고 BeautifulSoup에서 `html.parser` 사용
  ```python
  # 변경 전: soup = BeautifulSoup(response.text, 'lxml')
  # 변경 후: soup = BeautifulSoup(response.text, 'html.parser')
  ```
- **참고:** html.parser는 Python 내장 파서로 별도 설치 불필요하며, 한글 뉴스 파싱에 충분한 성능 제공

---

### ✅ Step 1.2: 뉴스 자동 선정 및 스크래핑
**목표:** CONTENT_STRATEGY.md 기준에 따라 가장 좋은 뉴스 1개 자동 선정
**소요 시간:** 2시간

> **변경 사항:** 단순히 첫 번째 기사를 가져오는 것이 아니라, 여러 기사를 분석하여 영향력, 실천 가능성, 학습 가치가 높은 기사를 자동 선정합니다.

#### 📝 체크리스트
- [x] `models/news_article.py` 작성
- [x] `scrapers/base_scraper.py` 작성
- [x] `scrapers/naver_scraper.py` 작성
- [x] `analyzers/news_selector.py` 작성 (뉴스 선정 로직)
- [x] `test_scraper.py` 업그레이드 (자동 선정 기능)

#### 🛠️ 실행 순서

**2-1. 데이터 모델 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\models\news_article.py`
```python
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class NewsArticle:
    """뉴스 기사 데이터 모델"""
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

    def __str__(self):
        return f"[{self.source}] {self.title} ({self.published_at.strftime('%Y-%m-%d')})"
```

**2-2. 추상 스크래퍼 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\scrapers\base_scraper.py`
```python
from abc import ABC, abstractmethod
from models.news_article import NewsArticle


class BaseScraper(ABC):
    """모든 스크래퍼의 추상 클래스"""

    @abstractmethod
    def scrape_article(self, url: str) -> NewsArticle:
        """단일 기사 스크래핑"""
        pass

    @abstractmethod
    def get_article_list(self, category_url: str, limit: int = 10) -> list[str]:
        """기사 URL 리스트 수집"""
        pass
```

**2-3. 네이버 스크래퍼 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\scrapers\naver_scraper.py`
```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper
from models.news_article import NewsArticle


class NaverScraper(BaseScraper):
    """네이버 뉴스 스크래퍼"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape_article(self, url: str) -> NewsArticle:
        """네이버 뉴스 기사 상세 정보 추출"""
        try:
            # 페이지 요청
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            # HTML 파싱 (lxml 대신 html.parser 사용)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 제목 추출
            title_elem = soup.select_one('#title_area span, #articleTitle, h2.media_end_head_headline')
            if not title_elem:
                raise ValueError("제목을 찾을 수 없습니다.")
            title = title_elem.get_text(strip=True)

            # 본문 추출
            content_elem = soup.select('#dic_area, #articeBody, #newsct_article')
            if not content_elem:
                raise ValueError("본문을 찾을 수 없습니다.")

            # 본문 내 모든 텍스트 추출 (광고 제거)
            paragraphs = []
            for elem in content_elem:
                # script, style 태그 제거
                for tag in elem.find_all(['script', 'style', 'iframe']):
                    tag.decompose()

                # 텍스트 추출
                text = elem.get_text(separator='\n', strip=True)
                if text:
                    paragraphs.append(text)

            content = '\n\n'.join(paragraphs)

            if not content or len(content) < 50:
                raise ValueError("본문 내용이 너무 짧습니다.")

            # 날짜 추출
            date_elem = soup.select_one('.media_end_head_info_datestamp_time, .author_info em, span.t11')
            if date_elem:
                date_str = date_elem.get('data-date-time') or date_elem.get_text(strip=True)

                # 여러 날짜 포맷 시도
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y.%m.%d. %H:%M', '%Y.%m.%d %H:%M']:
                    try:
                        published_at = datetime.strptime(date_str.replace('오전', '').replace('오후', '').strip(), fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # ISO 포맷 시도
                    try:
                        published_at = datetime.fromisoformat(date_str)
                    except:
                        published_at = datetime.now()  # 파싱 실패 시 현재 시간
            else:
                published_at = datetime.now()

            return NewsArticle(
                url=url,
                title=title,
                content=content,
                published_at=published_at,
                source='네이버'
            )

        except requests.RequestException as e:
            raise Exception(f"네트워크 오류: {e}")
        except Exception as e:
            raise Exception(f"파싱 오류: {e}")

    def get_article_list(self, category_url: str = 'https://news.naver.com/section/101', limit: int = 10) -> list[str]:
        """네이버 경제 섹션에서 기사 URL 리스트 추출"""
        try:
            response = requests.get(category_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 기사 링크 추출 (네이버 뉴스 구조에 따라 선택자 조정 필요)
            article_links = []

            # 방법 1: sa_text 클래스 (데스크톱)
            for link in soup.select('.sa_text_title'):
                href = link.get('href')
                if href and href.startswith('http') and 'news.naver.com' in href:
                    article_links.append(href)

            # 방법 2: 리스트 형식
            for link in soup.select('a.news_tit'):
                href = link.get('href')
                if href and href.startswith('http'):
                    article_links.append(href)

            # 중복 제거
            article_links = list(dict.fromkeys(article_links))

            return article_links[:limit]

        except Exception as e:
            raise Exception(f"목록 수집 오류: {e}")
```

**2-4. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_scraper.py`
```python
from scrapers.naver_scraper import NaverScraper


if __name__ == '__main__':
    print("=" * 50)
    print("네이버 뉴스 스크래퍼 테스트")
    print("=" * 50)

    scraper = NaverScraper()

    # 테스트용 네이버 뉴스 URL (최신 경제 뉴스로 교체하세요)
    # 예시: https://n.news.naver.com/article/009/0005393847
    test_url = ""  # 자동 수집 모드

    if not test_url:
        print("[!] URL을 입력하지 않았습니다.")
        print("\n자동으로 경제 섹션에서 첫 번째 기사 가져오기...")
        try:
            urls = scraper.get_article_list(limit=1)
            if urls:
                test_url = urls[0]
                print(f"[OK] URL: {test_url}")
            else:
                print("[ERROR] 기사를 찾을 수 없습니다.")
                exit(1)
        except Exception as e:
            print(f"[ERROR] URL 수집 실패: {e}")
            exit(1)

    print(f"\n[검색중] 스크래핑 중: {test_url}\n")

    try:
        article = scraper.scrape_article(test_url)

        print("[OK] 스크래핑 성공!")
        print(f"\n제목: {article.title}")
        print(f"출처: {article.source}")
        print(f"날짜: {article.published_at.strftime('%Y년 %m월 %d일 %H:%M')}")
        print(f"본문 길이: {len(article.content)}자")
        print(f"\n본문 미리보기:")
        print("-" * 50)
        print(article.content[:300])
        print("...")
        print("-" * 50)

        # JSON 저장 테스트
        article.save_to_json('./data/raw/test_article.json')
        print(f"\n[저장완료] JSON 저장 완료: ./data/raw/test_article.json")

    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        exit(1)
```

> **⚠️ Windows 콘솔 인코딩 이슈:** 이모지 문자(✅, ❌, 🔍 등)는 Windows 콘솔(cp949 인코딩)에서 `UnicodeEncodeError`를 발생시킬 수 있습니다. 위 코드는 이모지 대신 `[OK]`, `[ERROR]`, `[!]` 등의 텍스트 마커를 사용합니다.

**2-5. 실행**
```bash
python test_scraper.py
```

#### ✅ 성공 기준
- [x] 제목, 본문, 날짜가 정상 출력됨
- [x] 본문 길이가 최소 100자 이상
- [x] `data/raw/test_article.json` 파일 생성
- [x] JSON 파일을 텍스트 편집기로 열었을 때 한글 정상 표시

#### ✅ 완료 결과
- **실행 일자:** 2025-10-10
- **수집된 기사:** "산업차관, 철강 관세 대응 등 수출 지원체계 확인…해상물류 점검"
- **기사 URL:** https://n.news.naver.com/mnews/article/003/0013525645
- **본문 길이:** 2728자
- **저장 파일:** [./data/raw/test_article.json](./data/raw/test_article.json)

#### ⚠️ 예상 오류 및 해결

**오류 1:** `ModuleNotFoundError: No module named 'models'`
- **원인:** Python 경로 문제
- **해결:** `__init__.py` 파일이 모든 폴더에 있는지 확인

**오류 2:** `제목을 찾을 수 없습니다`
- **원인:** 네이버 HTML 구조 변경
- **해결:**
  1. 브라우저로 해당 URL 접속
  2. F12 눌러 개발자 도구
  3. Elements 탭에서 제목 요소 찾기
  4. 선택자 수정 (예: `#title_area span` → 실제 선택자)

**오류 3:** `본문 내용이 너무 짧습니다`
- **원인:** 본문 선택자 잘못됨
- **해결:** 위와 동일하게 개발자 도구로 본문 영역 확인 후 선택자 수정

**오류 4:** 날짜 파싱 오류
- **원인:** 날짜 포맷 다양
- **해결:** 이미 코드에 여러 포맷 처리 포함, 실패 시 현재 시간 사용

**오류 5:** `UnicodeEncodeError: 'cp949' codec can't encode character` ✅ 해결됨
- **원인:** Windows 콘솔이 cp949 인코딩을 사용하여 이모지 문자(✅, ❌, 🔍 등) 출력 불가
- **해결:** 이모지 대신 ASCII 텍스트 마커 사용
  - ❌ → `[ERROR]`
  - ✅ → `[OK]`
  - 🔍 → `[검색중]`
  - 💾 → `[저장완료]`
  - ⚠️ → `[!]`
- **참고:** UTF-8 콘솔 환경(Linux, macOS)에서는 이모지 사용 가능

---

## 🎉 Phase 1 완료!

**완료 일자:** 2025-10-10

### 주요 성과
- ✅ 뉴스 자동 선정 시스템 구축
- ✅ CONTENT_STRATEGY.md의 "1️⃣ 어떤 뉴스를 골라낼 것인가?" 완전 구현
- ✅ 점수 기반 투명한 선정 프로세스
- ✅ 5개 후보 중 최고 품질 1개 자동 선정

### 결정 사항: Step 1.3~1.5 건너뜀
**이유:**
- Step 1.3 (여러 기사 목록 수집): Step 1.2에 이미 포함됨
- Step 1.4 (데이터 저장): Step 1.2에서 JSON 저장 완료
- Step 1.5 (다음 스크래퍼): 네이버만으로 충분, 추후 데이터 풀 확장 시 고려

**원칙:**
> "전체적인 틀을 모두 세운 뒤 데이터 풀을 늘리는 건 추가로 결정"

---

### ~~Step 1.3: 여러 기사 목록 수집~~ (건너뜀)
**목표:** 네이버 경제 섹션에서 최신 10개 기사 URL 추출
**소요 시간:** 1시간
**상태:** ❌ Step 1.2에 이미 포함되어 불필요

#### 🛠️ 실행 순서

**3-1. 목록 수집 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_article_list.py`
```python
from scrapers.naver_scraper import NaverScraper


if __name__ == '__main__':
    print("=" * 50)
    print("네이버 뉴스 목록 수집 테스트")
    print("=" * 50)

    scraper = NaverScraper()

    # 네이버 경제 섹션 URL
    economy_url = 'https://news.naver.com/section/101'

    print(f"\n🔍 수집 중: {economy_url}\n")

    try:
        article_urls = scraper.get_article_list(economy_url, limit=10)

        print(f"✅ 총 {len(article_urls)}개 기사 URL 수집 완료\n")

        for i, url in enumerate(article_urls, 1):
            print(f"{i:2d}. {url}")

        # 첫 번째 기사 상세 정보 가져오기
        if article_urls:
            print(f"\n{'=' * 50}")
            print("첫 번째 기사 상세 정보:")
            print('=' * 50)

            article = scraper.scrape_article(article_urls[0])
            print(f"\n제목: {article.title}")
            print(f"날짜: {article.published_at}")
            print(f"본문: {article.content[:200]}...")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        exit(1)
```

**3-2. 실행**
```bash
python test_article_list.py
```

#### ✅ 성공 기준
- [ ] 10개의 유효한 네이버 뉴스 URL 출력
- [ ] 첫 번째 기사의 제목, 날짜, 본문 일부 출력
- [ ] URL이 모두 `https://n.news.naver.com/article/` 형식

---

### ✅ Step 1.4: 데이터 저장 (JSON)
**목표:** 여러 기사를 하나의 JSON 파일로 저장
**소요 시간:** 45분

#### 🛠️ 실행 순서

**4-1. 파일 매니저 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\utils\file_manager.py`
```python
import json
import os
from typing import List
from models.news_article import NewsArticle
from datetime import datetime


class FileManager:
    """파일 저장/로드 관리"""

    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, 'raw')
        self.processed_dir = os.path.join(data_dir, 'processed')

        # 디렉토리 생성
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def save_articles(self, articles: List[NewsArticle], filename: str = None) -> str:
        """여러 기사를 하나의 JSON 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'news_{timestamp}.json'

        filepath = os.path.join(self.raw_dir, filename)
        data = [article.to_dict() for article in articles]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(articles)}개 기사를 {filepath}에 저장했습니다.")
        return filepath

    def load_articles(self, filename: str) -> List[NewsArticle]:
        """JSON 파일에서 기사 로드"""
        filepath = os.path.join(self.raw_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"파일이 존재하지 않습니다: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        articles = [NewsArticle.from_dict(item) for item in data]
        print(f"✅ {len(articles)}개 기사를 {filepath}에서 로드했습니다.")
        return articles

    def list_saved_files(self) -> list[str]:
        """저장된 JSON 파일 목록"""
        files = [f for f in os.listdir(self.raw_dir) if f.endswith('.json')]
        return sorted(files, reverse=True)
```

**4-2. 저장 테스트 스크립트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_save_articles.py`
```python
from scrapers.naver_scraper import NaverScraper
from utils.file_manager import FileManager
import time


if __name__ == '__main__':
    print("=" * 50)
    print("뉴스 수집 및 저장 테스트")
    print("=" * 50)

    scraper = NaverScraper()
    file_manager = FileManager()

    # 기사 목록 수집
    print("\n1단계: 기사 URL 수집 중...")
    article_urls = scraper.get_article_list(limit=5)  # 테스트용 5개
    print(f"✅ {len(article_urls)}개 URL 수집 완료")

    # 각 기사 상세 정보 수집
    print("\n2단계: 기사 상세 정보 수집 중...")
    articles = []

    for i, url in enumerate(article_urls, 1):
        try:
            print(f"[{i}/{len(article_urls)}] {url[:60]}...")
            article = scraper.scrape_article(url)
            articles.append(article)
            print(f"  ✅ {article.title[:40]}")
            time.sleep(1)  # 서버 부담 방지
        except Exception as e:
            print(f"  ❌ 에러: {e}")
            continue

    # JSON 파일로 저장
    print(f"\n3단계: JSON 저장 중...")
    filepath = file_manager.save_articles(articles)

    # 저장된 파일 다시 읽기 (검증)
    print(f"\n4단계: 검증 중...")
    loaded_articles = file_manager.load_articles(os.path.basename(filepath))

    print(f"\n✅ 모든 단계 완료!")
    print(f"저장된 기사: {len(loaded_articles)}개")
    print(f"\n첫 번째 기사:")
    print(f"  제목: {loaded_articles[0].title}")
    print(f"  날짜: {loaded_articles[0].published_at}")
    print(f"  본문 길이: {len(loaded_articles[0].content)}자")
```

**4-3. 실행**
```bash
python test_save_articles.py
```

#### ✅ 성공 기준
- [ ] 5개 기사 수집 성공
- [ ] `data/raw/news_YYYYMMDD_HHMMSS.json` 파일 생성
- [ ] JSON 파일 열었을 때 배열 형태로 5개 기사 존재
- [ ] 로드 시 데이터 일치

---

### ✅ Step 1.5: 다음(Daum) 스크래퍼 추가
**목표:** 다음 뉴스도 동일하게 수집
**소요 시간:** 1.5시간

#### 🛠️ 실행 순서

**5-1. 다음 스크래퍼 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\scrapers\daum_scraper.py`
```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper
from models.news_article import NewsArticle
import re


class DaumScraper(BaseScraper):
    """다음 뉴스 스크래퍼"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_article(self, url: str) -> NewsArticle:
        """다음 뉴스 기사 상세 정보 추출"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 제목
            title_elem = soup.select_one('h3.tit_view, h2.screen_out')
            if not title_elem:
                raise ValueError("제목을 찾을 수 없습니다.")
            title = title_elem.get_text(strip=True)

            # 본문
            content_elems = soup.select('#harmonyContainer p, #mArticle p')
            if not content_elems:
                # 대체 선택자
                content_elems = soup.select('div[dmcf-ptype="general"] p')

            paragraphs = []
            for p in content_elems:
                text = p.get_text(strip=True)
                if text and len(text) > 10:  # 짧은 텍스트 제외
                    paragraphs.append(text)

            content = '\n\n'.join(paragraphs)

            if not content or len(content) < 50:
                raise ValueError("본문 내용이 너무 짧습니다.")

            # 날짜
            date_elem = soup.select_one('.num_date, .txt_info')
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                # 예: "2025.01.10. 오후 3:24"
                date_text = date_text.replace('입력', '').replace('수정', '').strip()

                # 정규식으로 날짜 추출
                match = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})\.\s*(오전|오후)?\s*(\d{1,2}):(\d{2})', date_text)
                if match:
                    year, month, day, ampm, hour, minute = match.groups()
                    hour = int(hour)
                    if ampm == '오후' and hour != 12:
                        hour += 12
                    elif ampm == '오전' and hour == 12:
                        hour = 0

                    published_at = datetime(int(year), int(month), int(day), hour, int(minute))
                else:
                    published_at = datetime.now()
            else:
                published_at = datetime.now()

            return NewsArticle(
                url=url,
                title=title,
                content=content,
                published_at=published_at,
                source='다음'
            )

        except Exception as e:
            raise Exception(f"파싱 오류: {e}")

    def get_article_list(self, category_url: str = 'https://news.daum.net/economy', limit: int = 10) -> list[str]:
        """다음 경제 섹션에서 기사 URL 리스트 추출"""
        try:
            response = requests.get(category_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            article_links = []

            # 다음 뉴스 링크 선택자
            for link in soup.select('a.link_txt'):
                href = link.get('href')
                if href and href.startswith('http') and 'v.daum.net' in href:
                    article_links.append(href)

            # 중복 제거
            article_links = list(dict.fromkeys(article_links))

            return article_links[:limit]

        except Exception as e:
            raise Exception(f"목록 수집 오류: {e}")
```

**5-2. 다중 소스 수집 테스트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_multi_scraper.py`
```python
from scrapers.naver_scraper import NaverScraper
from scrapers.daum_scraper import DaumScraper
from utils.file_manager import FileManager
import time


if __name__ == '__main__':
    print("=" * 60)
    print("다중 소스 뉴스 수집 테스트 (네이버 + 다음)")
    print("=" * 60)

    file_manager = FileManager()
    all_articles = []

    # ===== 네이버 수집 =====
    print("\n🔵 네이버 뉴스 수집")
    print("-" * 60)
    naver_scraper = NaverScraper()

    try:
        naver_urls = naver_scraper.get_article_list(limit=3)
        print(f"✅ {len(naver_urls)}개 URL 수집")

        for i, url in enumerate(naver_urls, 1):
            try:
                print(f"[{i}/{len(naver_urls)}] 수집 중...")
                article = naver_scraper.scrape_article(url)
                all_articles.append(article)
                print(f"  ✅ {article.title[:50]}")
                time.sleep(1)
            except Exception as e:
                print(f"  ❌ {e}")
    except Exception as e:
        print(f"❌ 네이버 수집 실패: {e}")

    # ===== 다음 수집 =====
    print("\n🟢 다음 뉴스 수집")
    print("-" * 60)
    daum_scraper = DaumScraper()

    try:
        daum_urls = daum_scraper.get_article_list(limit=3)
        print(f"✅ {len(daum_urls)}개 URL 수집")

        for i, url in enumerate(daum_urls, 1):
            try:
                print(f"[{i}/{len(daum_urls)}] 수집 중...")
                article = daum_scraper.scrape_article(url)
                all_articles.append(article)
                print(f"  ✅ {article.title[:50]}")
                time.sleep(1)
            except Exception as e:
                print(f"  ❌ {e}")
    except Exception as e:
        print(f"❌ 다음 수집 실패: {e}")

    # ===== 통합 저장 =====
    print(f"\n{'=' * 60}")
    print(f"총 {len(all_articles)}개 기사 수집 완료")
    print('=' * 60)

    if all_articles:
        filepath = file_manager.save_articles(all_articles, filename='combined_news.json')
        print(f"\n저장 위치: {filepath}")

        # 소스별 통계
        naver_count = sum(1 for a in all_articles if a.source == '네이버')
        daum_count = sum(1 for a in all_articles if a.source == '다음')
        print(f"\n통계:")
        print(f"  네이버: {naver_count}개")
        print(f"  다음: {daum_count}개")
    else:
        print("❌ 수집된 기사가 없습니다.")
```

**5-3. 실행**
```bash
python test_multi_scraper.py
```

#### ✅ 성공 기준
- [ ] 네이버 3개 + 다음 3개 = 총 6개 기사 수집
- [ ] `data/raw/combined_news.json` 파일 생성
- [ ] JSON에서 source 필드가 '네이버', '다음'으로 구분

---

## 🤖 Phase 2: AI 분석 (Week 2)

### ✅ Step 2.1: Gemini API 연동 및 요약
**목표:** 1개 기사를 3줄로 요약
**소요 시간:** 1시간

#### 📝 준비 사항
- [ ] Gemini API 키 발급 (https://makersuite.google.com/app/apikey)
- [ ] `.env`에 API 키 등록

#### 🛠️ 실행 순서

**1. requirements.txt 업데이트**
```
# 기존 라이브러리
beautifulsoup4==4.12.3
requests==2.31.0
lxml==5.1.0
python-dotenv==1.0.1

# Gemini API 추가
google-generativeai==0.4.0
```

설치:
```bash
pip install google-generativeai==0.4.0
```

**2. .env 파일에 API 키 추가**
```
GEMINI_API_KEY=여기에_발급받은_API_키_입력
```

**3. Config 파일 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\utils\config.py`
```python
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """프로젝트 설정"""

    # Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.0-flash-exp'  # 또는 'gemini-2.5-flash'

    # 텔레그램
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    # 쿠팡 파트너스
    COUPANG_ACCESS_KEY = os.getenv('COUPANG_ACCESS_KEY')
    COUPANG_PARTNER_ID = os.getenv('COUPANG_PARTNER_ID')

    # 스크래핑 설정
    MAX_ARTICLES_PER_SITE = 10
    SCRAPING_DELAY = 1  # 초

    # 데이터 경로
    DATA_DIR = './data'
    RAW_DIR = './data/raw'
    PROCESSED_DIR = './data/processed'
    CHARTS_DIR = './data/charts'
    HTML_DIR = './data/html'

    @classmethod
    def validate(cls):
        """필수 설정 검증"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")
```

**4. Gemini 분석기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\analyzers\gemini_analyzer.py`
```python
import google.generativeai as genai
from utils.config import Config
from models.news_article import NewsArticle


class GeminiAnalyzer:
    """Gemini API를 사용한 뉴스 분석"""

    def __init__(self):
        # API 키 검증
        Config.validate()

        # Gemini 설정
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def summarize(self, article: NewsArticle, num_sentences: int = 3) -> str:
        """기사를 지정된 문장 수로 요약"""
        prompt = f"""
다음 뉴스 기사를 정확히 {num_sentences}문장으로 요약해주세요.
핵심 내용만 간결하게 담아주세요.

제목: {article.title}

본문:
{article.content}

요약 ({num_sentences}문장):
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            return summary

        except Exception as e:
            raise Exception(f"요약 생성 실패: {e}")

    def test_connection(self) -> bool:
        """API 연결 테스트"""
        try:
            response = self.model.generate_content("안녕하세요. 테스트 메시지입니다. '성공'이라고 답해주세요.")
            return '성공' in response.text
        except Exception as e:
            print(f"API 연결 실패: {e}")
            return False
```

**5. 테스트 스크립트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_gemini.py`
```python
from utils.file_manager import FileManager
from analyzers.gemini_analyzer import GeminiAnalyzer
import os


if __name__ == '__main__':
    print("=" * 60)
    print("Gemini API 연동 및 요약 테스트")
    print("=" * 60)

    # API 연결 테스트
    print("\n1단계: API 연결 테스트...")
    analyzer = GeminiAnalyzer()

    if analyzer.test_connection():
        print("✅ API 연결 성공")
    else:
        print("❌ API 연결 실패 - .env 파일의 GEMINI_API_KEY를 확인하세요.")
        exit(1)

    # 저장된 기사 로드
    print("\n2단계: 저장된 기사 로드...")
    file_manager = FileManager()

    # 가장 최근 저장된 파일 찾기
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다. 먼저 test_save_articles.py를 실행하세요.")
        exit(1)

    latest_file = saved_files[0]
    print(f"✅ 파일: {latest_file}")

    articles = file_manager.load_articles(latest_file)
    article = articles[0]

    # 기사 정보 출력
    print(f"\n{'=' * 60}")
    print("원본 기사")
    print('=' * 60)
    print(f"제목: {article.title}")
    print(f"출처: {article.source}")
    print(f"본문 길이: {len(article.content)}자")
    print(f"\n본문 미리보기:")
    print(article.content[:200] + "...")

    # 요약 생성
    print(f"\n{'=' * 60}")
    print("3단계: 요약 생성 중...")
    print('=' * 60)

    try:
        summary = analyzer.summarize(article, num_sentences=3)
        print(f"\n✅ 요약 (3문장):\n")
        print(summary)

        # 기사 객체에 저장
        article.summary = summary

        # 저장
        file_manager.save_articles([article], filename='summarized_article.json')
        print(f"\n💾 요약이 포함된 기사 저장 완료: summarized_article.json")

    except Exception as e:
        print(f"❌ 요약 실패: {e}")
        exit(1)
```

**6. 실행**
```bash
python test_gemini.py
```

#### ✅ 성공 기준
- [ ] API 연결 성공 메시지 출력
- [ ] 3문장 요약 생성
- [ ] `data/raw/summarized_article.json`에 summary 필드 포함

#### ⚠️ 예상 오류

**오류 1:** `GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다`
- **해결:** `.env` 파일 열어서 `GEMINI_API_KEY=실제_키` 입력

**오류 2:** `API key not valid`
- **해결:** https://makersuite.google.com/app/apikey 에서 새 키 발급

**오류 3:** `Quota exceeded`
- **해결:** 무료 할당량 초과, 내일 다시 시도 또는 유료 전환

---

이런 식으로 **모든 단계를 상세히 작성**하면 약 200페이지 분량이 됩니다.

나머지 Phase도 동일한 형식으로 계속 작성할까요? 아니면 특정 Phase를 더 자세히 설명해드릴까요?

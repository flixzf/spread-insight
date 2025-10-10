# Phase 2: AI 분석 (Week 2)

> Gemini 2.0/2.5 Flash를 사용한 뉴스 분석 및 인사이트 생성

---

## ✅ Step 2.1: Gemini API 연동 및 요약 (완료)

*(이미 DETAILED_STEPS.md에 작성되어 있음)*

---

## ✅ Step 2.2: 쉬운 언어로 재작성
**목표:** 전문 용어를 중학생도 이해할 수 있게 변환
**소요 시간:** 1.5시간

### 📝 체크리스트
- [ ] `gemini_analyzer.py`에 `simplify_language()` 메서드 추가
- [ ] 프롬프트 최적화 (중학생 눈높이)
- [ ] 테스트 스크립트 작성
- [ ] 실행 및 검증

### 🛠️ 실행 순서

**1. gemini_analyzer.py 업데이트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\analyzers\gemini_analyzer.py`

기존 파일에 다음 메서드를 추가:
```python
def simplify_language(self, article: NewsArticle) -> str:
    """전문 용어를 쉬운 언어로 변환"""
    prompt = f"""
다음 경제 뉴스를 중학생도 이해할 수 있도록 쉽게 다시 작성해주세요.

**규칙:**
1. 전문 용어는 괄호 안에 쉬운 설명 추가
   예: "기준금리(한국은행이 정하는 기본 이자율)"
2. 문장은 짧고 명확하게 (한 문장에 한 가지 내용)
3. 비유나 구체적 예시를 활용
4. "~입니다", "~됩니다" 같은 정중한 어투 사용
5. 숫자가 나오면 비교 대상 제시 (예: "작년보다 10% 증가")

원본 기사:
제목: {article.title}
본문: {article.content}

쉬운 설명:
    """.strip()

    try:
        response = self.model.generate_content(prompt)
        easy_text = response.text.strip()
        return easy_text

    except Exception as e:
        raise Exception(f"쉬운 설명 생성 실패: {e}")
```

**2. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_simplify.py`
```python
from utils.file_manager import FileManager
from analyzers.gemini_analyzer import GeminiAnalyzer


if __name__ == '__main__':
    print("=" * 60)
    print("쉬운 언어로 재작성 테스트")
    print("=" * 60)

    # 파일 매니저 및 분석기 초기화
    file_manager = FileManager()
    analyzer = GeminiAnalyzer()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다. 먼저 test_save_articles.py를 실행하세요.")
        exit(1)

    latest_file = saved_files[0]
    print(f"로드 파일: {latest_file}\n")

    articles = file_manager.load_articles(latest_file)
    article = articles[0]

    # 원본 기사 출력
    print("=" * 60)
    print("원본 기사")
    print("=" * 60)
    print(f"제목: {article.title}")
    print(f"\n본문 (앞 500자):")
    print(article.content[:500])
    print("...\n")

    # 쉬운 언어로 변환
    print("=" * 60)
    print("변환 중...")
    print("=" * 60)

    try:
        easy_explanation = analyzer.simplify_language(article)

        print("\n✅ 쉬운 설명:\n")
        print("=" * 60)
        print(easy_explanation)
        print("=" * 60)

        # 기사 객체에 저장
        article.easy_explanation = easy_explanation

        # 기존 요약도 함께 저장
        if not article.summary:
            print("\n요약도 함께 생성 중...")
            article.summary = analyzer.summarize(article, num_sentences=3)

        # 저장
        file_manager.save_articles([article], filename='simplified_article.json')
        print(f"\n💾 저장 완료: simplified_article.json")

    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        exit(1)
```

**3. 실행**
```bash
python test_simplify.py
```

### ✅ 성공 기준
- [ ] 전문 용어가 괄호로 설명됨
- [ ] 문장이 원본보다 짧고 명확함
- [ ] 중학생 수준에서 이해 가능
- [ ] `data/raw/simplified_article.json`에 easy_explanation 필드 포함

### ⚠️ 예상 오류 및 해결

**오류 1:** 응답이 너무 길어서 잘림
- **원인:** 본문이 너무 김 (Gemini의 출력 제한)
- **해결:** 본문을 2000자로 제한
  ```python
  content_preview = article.content[:2000]
  prompt = f"본문: {content_preview}..."
  ```

**오류 2:** 여전히 어려운 용어 사용
- **원인:** 프롬프트 불충분
- **해결:** 프롬프트에 구체적 예시 추가
  ```python
  예시:
  원본: "한국은행은 기준금리를 3.5%로 동결했다"
  쉬운 버전: "한국은행은 기준금리(은행들이 대출할 때 참고하는 기본 이자율)를 3.5%로 유지하기로 했습니다."
  ```

---

## ✅ Step 2.3: 용어 자동 추출 및 해설
**목표:** 어려운 단어를 자동으로 찾아서 용어집 생성
**소요 시간:** 1.5시간

### 📝 체크리스트
- [ ] `analyzers/terminology.py` 작성
- [ ] JSON 파싱 안전하게 처리
- [ ] 테스트 스크립트 작성
- [ ] 실행 및 검증

### 🛠️ 실행 순서

**1. 용어 추출기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\analyzers\terminology.py`
```python
import google.generativeai as genai
from utils.config import Config
import json
import re


class TerminologyExtractor:
    """전문 용어 자동 추출 및 설명 생성"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def extract_and_explain(self, text: str, max_terms: int = 7) -> dict[str, str]:
        """텍스트에서 전문 용어 추출 및 설명"""
        prompt = f"""
다음 경제 뉴스에서 일반인이 어려워할 만한 전문 용어를 최대 {max_terms}개 찾아서
JSON 형식으로 설명해주세요.

**선정 기준:**
- 경제/금융 전문 용어
- 약어 (GDP, IMF 등)
- 일반인이 잘 모를 법한 단어
- 중요도가 높은 순서대로

**설명 기준:**
- 중학생도 이해할 수 있게
- 1~2문장으로 간결하게
- 구체적 예시나 비유 포함

텍스트:
{text[:2000]}

**출력 형식 (반드시 유효한 JSON):**
{{
    "기준금리": "한국은행이 정하는 기본 이자율로, 은행들이 대출할 때 참고하는 기준입니다.",
    "환율": "다른 나라 돈과 우리나라 돈을 바꿀 때의 비율입니다. 예: 달러당 1,300원",
    "GDP": "국내총생산의 약자로, 한 나라가 1년 동안 만들어낸 모든 상품과 서비스의 가치를 합친 것입니다."
}}

JSON:
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            json_text = response.text.strip()

            # Markdown 코드 블록 제거
            if '```' in json_text:
                # ```json ... ``` 형태 처리
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', json_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)
                else:
                    # ``` 이후 첫 번째 { 부터 마지막 } 까지
                    json_text = re.sub(r'^```(?:json)?', '', json_text)
                    json_text = re.sub(r'```$', '', json_text)

            # JSON 파싱
            json_text = json_text.strip()
            terminology = json.loads(json_text)

            # 딕셔너리 검증
            if not isinstance(terminology, dict):
                raise ValueError("응답이 딕셔너리 형태가 아닙니다.")

            print(f"✅ {len(terminology)}개 용어 추출")
            return terminology

        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 실패: {e}")
            print(f"응답: {response.text[:500]}")
            return {}
        except Exception as e:
            print(f"❌ 용어 추출 실패: {e}")
            return {}

    def get_terminology_for_article(self, article) -> dict[str, str]:
        """기사 전체에서 용어 추출 (제목 + 본문)"""
        full_text = f"{article.title}\n\n{article.content}"
        return self.extract_and_explain(full_text)
```

**2. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_terminology.py`
```python
from utils.file_manager import FileManager
from analyzers.terminology import TerminologyExtractor


if __name__ == '__main__':
    print("=" * 60)
    print("용어 추출 및 해설 테스트")
    print("=" * 60)

    # 파일 매니저 및 추출기 초기화
    file_manager = FileManager()
    term_extractor = TerminologyExtractor()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다.")
        exit(1)

    latest_file = saved_files[0]
    print(f"로드 파일: {latest_file}\n")

    articles = file_manager.load_articles(latest_file)
    article = articles[0]

    # 원본 기사 출력
    print("=" * 60)
    print("원본 기사")
    print("=" * 60)
    print(f"제목: {article.title}")
    print(f"본문 길이: {len(article.content)}자\n")

    # 용어 추출
    print("=" * 60)
    print("용어 추출 중...")
    print("=" * 60)

    terminology = term_extractor.get_terminology_for_article(article)

    if terminology:
        print(f"\n✅ 추출된 용어 ({len(terminology)}개):\n")
        for i, (term, explanation) in enumerate(terminology.items(), 1):
            print(f"{i}. {term}")
            print(f"   → {explanation}\n")

        # 기사 객체에 저장
        article.terminology = terminology

        # 저장
        file_manager.save_articles([article], filename='article_with_terminology.json')
        print(f"💾 저장 완료: article_with_terminology.json")
    else:
        print("❌ 용어를 추출하지 못했습니다.")
```

**3. 실행**
```bash
python test_terminology.py
```

### ✅ 성공 기준
- [ ] 3~7개의 전문 용어 추출
- [ ] 각 용어에 대한 쉬운 설명
- [ ] JSON 파싱 오류 없음
- [ ] `data/raw/article_with_terminology.json` 생성

### ⚠️ 예상 오류 및 해결

**오류 1:** `JSON 파싱 실패`
- **원인:** Gemini가 JSON 외에 다른 텍스트도 함께 출력
- **해결:** 정규식으로 JSON 부분만 추출 (이미 코드에 포함)

**오류 2:** 응답이 딕셔너리가 아닌 리스트
- **원인:** 프롬프트 해석 오류
- **해결:** 프롬프트에 예시 더 명확히 제시

**오류 3:** 용어가 너무 적음 (1~2개)
- **원인:** `max_terms` 파라미터 무시
- **해결:** 프롬프트에 "정확히 5~7개" 같이 구체적으로 명시

---

## ✅ Step 2.4: 과거 맥락 구성 (타임라인)
**목표:** 현재 뉴스와 관련된 과거 뉴스를 찾아 시계열 맥락 생성
**소요 시간:** 2시간

### 📝 체크리스트
- [ ] `database/db_manager.py` 작성 (SQLite)
- [ ] `analyzers/context_builder.py` 작성
- [ ] 테스트 스크립트 작성
- [ ] 실행 및 검증

### 🛠️ 실행 순서

**1. 데이터베이스 매니저 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\database\db_manager.py`
```python
import sqlite3
from typing import List
from models.news_article import NewsArticle
from datetime import datetime
import json
import os


class DatabaseManager:
    """SQLite 데이터베이스 관리"""

    def __init__(self, db_path: str = './database/news.db'):
        self.db_path = db_path

        # database 폴더 생성
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self._create_table()

    def _create_table(self):
        """뉴스 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                published_at TEXT NOT NULL,
                source TEXT NOT NULL,
                keywords TEXT,
                summary TEXT,
                easy_explanation TEXT,
                terminology TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 인덱스 생성 (검색 성능 향상)
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_published_at
            ON articles(published_at DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_title
            ON articles(title)
        ''')

        conn.commit()
        conn.close()
        print("✅ 데이터베이스 테이블 생성 완료")

    def insert_article(self, article: NewsArticle) -> bool:
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
                json.dumps(article.keywords, ensure_ascii=False) if article.keywords else None,
                article.summary,
                article.easy_explanation,
                json.dumps(article.terminology, ensure_ascii=False) if article.terminology else None
            ))

            inserted = cursor.rowcount > 0
            conn.commit()

            if inserted:
                print(f"  ✅ DB 저장: {article.title[:40]}")
            else:
                print(f"  ⚠️  중복: {article.title[:40]}")

            return inserted

        except Exception as e:
            print(f"  ❌ DB 저장 실패: {e}")
            return False
        finally:
            conn.close()

    def insert_articles(self, articles: List[NewsArticle]) -> int:
        """여러 기사 일괄 삽입"""
        count = 0
        for article in articles:
            if self.insert_article(article):
                count += 1
        return count

    def search_by_keyword(self, keyword: str, limit: int = 10, exclude_url: str = None) -> List[NewsArticle]:
        """키워드로 기사 검색 (제목 + 본문)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''
            SELECT url, title, content, published_at, source, keywords, summary, easy_explanation, terminology
            FROM articles
            WHERE (title LIKE ? OR content LIKE ?)
        '''
        params = [f'%{keyword}%', f'%{keyword}%']

        # 현재 기사 제외
        if exclude_url:
            query += ' AND url != ?'
            params.append(exclude_url)

        query += ' ORDER BY published_at DESC LIMIT ?'
        params.append(limit)

        cursor.execute(query, params)
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

    def get_total_count(self) -> int:
        """전체 기사 수"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM articles')
        count = cursor.fetchone()[0]
        conn.close()
        return count
```

**2. 컨텍스트 빌더 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\analyzers\context_builder.py`
```python
import google.generativeai as genai
from utils.config import Config
from database.db_manager import DatabaseManager
from models.news_article import NewsArticle
from typing import List


class ContextBuilder:
    """과거 맥락 구성 및 타임라인 생성"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.db = DatabaseManager()

    def extract_keywords(self, article: NewsArticle, max_keywords: int = 5) -> list[str]:
        """기사에서 핵심 키워드 추출"""
        prompt = f"""
다음 경제 뉴스에서 핵심 키워드를 정확히 {max_keywords}개 추출해주세요.

**선정 기준:**
- 기사의 주제를 대표하는 단어
- 검색에 유용한 명사 (고유명사, 경제 용어 등)
- 너무 일반적인 단어 제외 (예: "경제", "뉴스")

제목: {article.title}
본문 앞부분: {article.content[:500]}

**출력 형식:** 쉼표로 구분된 키워드만 출력
예: 기준금리, 한국은행, 인플레이션, 물가상승률, 통화정책

키워드:
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            keywords_text = response.text.strip()

            # 쉼표로 분리
            keywords = [k.strip() for k in keywords_text.split(',')]
            keywords = [k for k in keywords if k]  # 빈 문자열 제거

            print(f"  ✅ 키워드 추출: {', '.join(keywords)}")
            return keywords[:max_keywords]

        except Exception as e:
            print(f"  ❌ 키워드 추출 실패: {e}")
            return []

    def find_related_articles(self, article: NewsArticle) -> List[NewsArticle]:
        """관련 과거 기사 검색"""
        if not article.keywords:
            article.keywords = self.extract_keywords(article)

        if not article.keywords:
            return []

        # 각 키워드로 검색
        related_articles = []
        seen_urls = {article.url}

        for keyword in article.keywords:
            articles = self.db.search_by_keyword(
                keyword=keyword,
                limit=3,
                exclude_url=article.url
            )

            for art in articles:
                if art.url not in seen_urls:
                    seen_urls.add(art.url)
                    related_articles.append(art)

        # 날짜순 정렬 (오래된 것부터)
        related_articles.sort(key=lambda a: a.published_at)

        print(f"  ✅ 관련 기사 {len(related_articles)}개 발견")
        return related_articles[:5]  # 최대 5개

    def build_timeline(self, article: NewsArticle) -> str:
        """과거 관련 뉴스를 기반으로 타임라인 생성"""
        # 1. 키워드 추출
        if not article.keywords:
            article.keywords = self.extract_keywords(article)

        # 2. 과거 관련 기사 검색
        related_articles = self.find_related_articles(article)

        if not related_articles:
            print("  ⚠️  관련 과거 기사 없음")
            return "이 뉴스는 최근에 등장한 새로운 이슈입니다."

        # 3. 타임라인 생성
        related_text = "\n\n".join([
            f"[{art.published_at.strftime('%Y년 %m월 %d일')}] {art.title}\n{art.summary or art.content[:200]}"
            for art in related_articles
        ])

        prompt = f"""
현재 뉴스와 관련된 과거 기사들을 바탕으로 이 이슈가 어떻게 발전해왔는지
시계열 타임라인으로 설명해주세요.

**규칙:**
- 3~5문장으로 작성
- 시간 흐름에 따라 설명
- 중학생도 이해할 수 있게
- "처음에는...", "이후...", "최근에는..." 같은 연결어 사용

**현재 뉴스:**
[{article.published_at.strftime('%Y년 %m월 %d일')}] {article.title}
내용: {article.content[:300]}

**과거 관련 기사:**
{related_text}

타임라인 설명:
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            timeline = response.text.strip()
            print(f"  ✅ 타임라인 생성 완료")
            return timeline

        except Exception as e:
            print(f"  ❌ 타임라인 생성 실패: {e}")
            return "타임라인을 생성할 수 없습니다."
```

**3. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_context.py`
```python
from utils.file_manager import FileManager
from analyzers.context_builder import ContextBuilder
from database.db_manager import DatabaseManager


if __name__ == '__main__':
    print("=" * 60)
    print("과거 맥락 구성 및 타임라인 테스트")
    print("=" * 60)

    # 초기화
    file_manager = FileManager()
    db = DatabaseManager()
    context_builder = ContextBuilder()

    # 1단계: 과거 기사들을 DB에 저장
    print("\n1단계: 과거 기사 DB 저장")
    print("-" * 60)

    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다. 먼저 test_multi_scraper.py를 실행하세요.")
        exit(1)

    # 모든 저장된 파일의 기사를 DB에 추가
    total_inserted = 0
    for filename in saved_files[:3]:  # 최근 3개 파일만
        try:
            articles = file_manager.load_articles(filename)
            inserted = db.insert_articles(articles)
            total_inserted += inserted
            print(f"  {filename}: {inserted}/{len(articles)}개 저장")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")

    print(f"\n✅ 총 {total_inserted}개 기사 DB 저장")
    print(f"전체 DB 기사 수: {db.get_total_count()}개\n")

    # 2단계: 최신 기사 선택
    print("2단계: 최신 기사 선택")
    print("-" * 60)

    latest_file = saved_files[0]
    articles = file_manager.load_articles(latest_file)
    test_article = articles[0]

    print(f"선택된 기사: {test_article.title}\n")

    # 3단계: 키워드 추출
    print("3단계: 키워드 추출")
    print("-" * 60)

    keywords = context_builder.extract_keywords(test_article)
    test_article.keywords = keywords
    print(f"키워드: {', '.join(keywords)}\n")

    # 4단계: 관련 기사 검색
    print("4단계: 관련 과거 기사 검색")
    print("-" * 60)

    related_articles = context_builder.find_related_articles(test_article)

    if related_articles:
        for i, art in enumerate(related_articles, 1):
            print(f"{i}. [{art.published_at.strftime('%Y-%m-%d')}] {art.title[:50]}")
    else:
        print("⚠️  관련 기사 없음")

    print()

    # 5단계: 타임라인 생성
    print("5단계: 타임라인 생성")
    print("-" * 60)

    timeline = context_builder.build_timeline(test_article)

    print("\n✅ 타임라인:\n")
    print("=" * 60)
    print(timeline)
    print("=" * 60)

    # 저장
    print("\n6단계: 저장")
    print("-" * 60)

    # 타임라인 정보를 어디에 저장할지는 나중에 결정
    # 지금은 콘솔에만 출력
    print(f"✅ 테스트 완료")
```

**4. 실행**
```bash
python test_context.py
```

### ✅ 성공 기준
- [ ] `database/news.db` 파일 생성
- [ ] 과거 기사들이 DB에 저장됨
- [ ] 키워드 기반 관련 기사 검색 동작
- [ ] 타임라인 텍스트 생성 (3~5문장)

### ⚠️ 예상 오류 및 해결

**오류 1:** `no such table: articles`
- **원인:** DB 테이블 생성 안 됨
- **해결:** `database` 폴더가 존재하는지 확인, `_create_table()` 호출 확인

**오류 2:** 관련 기사가 하나도 없음
- **원인:** DB에 기사가 너무 적음 또는 키워드 매칭 안 됨
- **해결:** 먼저 `test_multi_scraper.py`를 여러 번 실행해서 기사 축적

**오류 3:** 키워드가 너무 일반적 (예: "경제", "뉴스")
- **원인:** Gemini가 구체적인 키워드 추출 안 함
- **해결:** 프롬프트에 "구체적이고 고유한 키워드" 강조

---

## ✅ Step 2.5: 중요도 점수 계산 및 상위 뉴스 선정
**목표:** 수집된 뉴스 중 중요도가 높은 상위 5개 선정
**소요 시간:** 1.5시간

### 📝 체크리스트
- [ ] `analyzers/importance_ranker.py` 작성
- [ ] 점수 계산 로직 구현
- [ ] 테스트 스크립트 작성
- [ ] 실행 및 검증

### 🛠️ 실행 순서

**1. 중요도 랭커 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\analyzers\importance_ranker.py`
```python
from typing import List
from models.news_article import NewsArticle
import re


class ImportanceRanker:
    """기사 중요도 점수 계산 및 랭킹"""

    # 중요 키워드 (가중치 부여)
    HIGH_PRIORITY_KEYWORDS = {
        # 금융/통화
        '한국은행': 4,
        '기준금리': 4,
        '금리': 3,
        '통화정책': 3,

        # 환율/무역
        '환율': 3,
        '달러': 2,
        '원화': 2,
        '무역수지': 3,
        '수출': 2,
        '수입': 2,

        # 주식/증시
        '코스피': 3,
        '코스닥': 3,
        '주가': 2,
        '증시': 2,
        '주식': 2,

        # 경제지표
        'GDP': 4,
        '성장률': 3,
        '물가': 3,
        '인플레이션': 4,
        'CPI': 3,
        '소비자물가': 3,
        '실업률': 3,
        '고용': 2,

        # 부동산
        '부동산': 2,
        '집값': 2,
        '아파트': 2,

        # 기업/산업
        '삼성': 2,
        '현대': 2,
        'LG': 2,
        '반도체': 2,
        '자동차': 2,
    }

    @staticmethod
    def calculate_score(article: NewsArticle) -> float:
        """기사 중요도 점수 계산 (0~100점)"""
        score = 0.0

        # === 1. 키워드 매칭 점수 (최대 50점) ===
        title_lower = article.title.lower()
        content_lower = article.content.lower()

        keyword_score = 0
        for keyword, weight in ImportanceRanker.HIGH_PRIORITY_KEYWORDS.items():
            if keyword.lower() in title_lower:
                keyword_score += weight * 3  # 제목에 있으면 3배 가중
            elif keyword.lower() in content_lower:
                keyword_score += weight

        # 키워드 점수 정규화 (최대 50점)
        keyword_score = min(keyword_score, 50)
        score += keyword_score

        # === 2. 본문 품질 점수 (최대 20점) ===
        content_len = len(article.content)

        if content_len < 300:
            quality_score = 0  # 너무 짧음
        elif 300 <= content_len < 800:
            quality_score = 10  # 짧음
        elif 800 <= content_len < 3000:
            quality_score = 20  # 적당
        else:
            quality_score = 15  # 너무 김 (요약하기 어려움)

        score += quality_score

        # === 3. 숫자/데이터 포함 점수 (최대 15점) ===
        # 통계 기사는 신뢰도가 높음
        numbers = re.findall(r'\d+\.?\d*%?', article.content)

        if len(numbers) >= 5:
            data_score = 15
        elif len(numbers) >= 3:
            data_score = 10
        elif len(numbers) >= 1:
            data_score = 5
        else:
            data_score = 0

        score += data_score

        # === 4. 제목 품질 점수 (최대 15점) ===
        title_len = len(article.title)

        if 15 <= title_len <= 50:
            title_score = 15  # 적당한 길이
        elif 10 <= title_len < 15 or 50 < title_len <= 70:
            title_score = 10  # 약간 짧거나 김
        else:
            title_score = 5  # 너무 짧거나 김

        score += title_score

        return round(score, 1)

    @staticmethod
    def rank_articles(articles: List[NewsArticle], top_n: int = 5) -> List[NewsArticle]:
        """기사들을 중요도 순으로 정렬 후 상위 N개 반환"""
        if not articles:
            return []

        # 점수 계산
        scored_articles = []
        for article in articles:
            score = ImportanceRanker.calculate_score(article)
            scored_articles.append((article, score))

        # 점수 내림차순 정렬
        scored_articles.sort(key=lambda x: x[1], reverse=True)

        # 결과 출력
        print(f"\n중요도 랭킹 (상위 {min(top_n, len(scored_articles))}개):")
        print("=" * 80)

        for i, (article, score) in enumerate(scored_articles[:top_n], 1):
            print(f"{i}. [{score:5.1f}점] {article.source:6s} | {article.title[:50]}")

        print("=" * 80)

        # 상위 N개 반환
        top_articles = [article for article, score in scored_articles[:top_n]]
        return top_articles

    @staticmethod
    def get_score_breakdown(article: NewsArticle) -> dict:
        """점수 세부 내역 확인용"""
        breakdown = {
            'total': 0,
            'keyword': 0,
            'quality': 0,
            'data': 0,
            'title': 0
        }

        # 키워드 점수
        title_lower = article.title.lower()
        content_lower = article.content.lower()

        keyword_score = 0
        matched_keywords = []
        for keyword, weight in ImportanceRanker.HIGH_PRIORITY_KEYWORDS.items():
            if keyword.lower() in title_lower:
                keyword_score += weight * 3
                matched_keywords.append(f"{keyword}(제목)")
            elif keyword.lower() in content_lower:
                keyword_score += weight
                matched_keywords.append(keyword)

        breakdown['keyword'] = min(keyword_score, 50)
        breakdown['matched_keywords'] = matched_keywords

        # 본문 품질
        content_len = len(article.content)
        if content_len < 300:
            breakdown['quality'] = 0
        elif 300 <= content_len < 800:
            breakdown['quality'] = 10
        elif 800 <= content_len < 3000:
            breakdown['quality'] = 20
        else:
            breakdown['quality'] = 15

        # 데이터 점수
        numbers = re.findall(r'\d+\.?\d*%?', article.content)
        if len(numbers) >= 5:
            breakdown['data'] = 15
        elif len(numbers) >= 3:
            breakdown['data'] = 10
        elif len(numbers) >= 1:
            breakdown['data'] = 5

        # 제목 점수
        title_len = len(article.title)
        if 15 <= title_len <= 50:
            breakdown['title'] = 15
        elif 10 <= title_len < 15 or 50 < title_len <= 70:
            breakdown['title'] = 10
        else:
            breakdown['title'] = 5

        # 총점
        breakdown['total'] = breakdown['keyword'] + breakdown['quality'] + breakdown['data'] + breakdown['title']

        return breakdown
```

**2. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_ranking.py`
```python
from utils.file_manager import FileManager
from analyzers.importance_ranker import ImportanceRanker


if __name__ == '__main__':
    print("=" * 80)
    print("중요도 점수 계산 및 랭킹 테스트")
    print("=" * 80)

    # 파일 매니저 및 랭커 초기화
    file_manager = FileManager()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다. 먼저 test_multi_scraper.py를 실행하세요.")
        exit(1)

    # 여러 파일의 기사를 모두 로드
    all_articles = []
    print("\n기사 로드 중...")
    for filename in saved_files[:3]:  # 최근 3개 파일
        try:
            articles = file_manager.load_articles(filename)
            all_articles.extend(articles)
            print(f"  ✅ {filename}: {len(articles)}개")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")

    print(f"\n총 {len(all_articles)}개 기사 로드 완료\n")

    # 중요도 랭킹
    top_articles = ImportanceRanker.rank_articles(all_articles, top_n=5)

    # 상위 3개 기사의 점수 세부 내역
    print("\n\n상위 3개 기사 점수 세부 내역:")
    print("=" * 80)

    for i, article in enumerate(top_articles[:3], 1):
        breakdown = ImportanceRanker.get_score_breakdown(article)

        print(f"\n{i}. {article.title}")
        print(f"   출처: {article.source} | 날짜: {article.published_at.strftime('%Y-%m-%d')}")
        print(f"   본문 길이: {len(article.content)}자")
        print(f"\n   점수 세부:")
        print(f"     • 키워드: {breakdown['keyword']}/50점")
        if breakdown.get('matched_keywords'):
            print(f"       매칭: {', '.join(breakdown['matched_keywords'][:5])}")
        print(f"     • 본문 품질: {breakdown['quality']}/20점")
        print(f"     • 데이터: {breakdown['data']}/15점")
        print(f"     • 제목: {breakdown['title']}/15점")
        print(f"     ---")
        print(f"     총점: {breakdown['total']}/100점")
        print("-" * 80)

    # 상위 5개 저장
    print("\n\n상위 5개 기사 저장 중...")
    file_manager.save_articles(top_articles, filename='top_news.json')
    print("✅ 저장 완료: top_news.json")
```

**3. 실행**
```bash
python test_ranking.py
```

### ✅ 성공 기준
- [ ] 모든 기사의 점수 계산 완료
- [ ] 점수 기반 정렬 동작
- [ ] 상위 5개 기사 선정
- [ ] 점수 세부 내역 표시
- [ ] `data/raw/top_news.json` 파일 생성

### ⚠️ 예상 오류 및 해결

**오류 1:** 모든 기사 점수가 낮음 (10점 미만)
- **원인:** 키워드 매칭이 안 됨
- **해결:** `HIGH_PRIORITY_KEYWORDS`에 더 다양한 키워드 추가

**오류 2:** 특정 출처의 기사만 상위권
- **원인:** 해당 출처가 키워드를 많이 사용
- **해결:** 출처 다양성 보너스 추가 (고급 기능)

**오류 3:** 점수가 너무 비슷함 (차이 1점 미만)
- **원인:** 가중치 조정 필요
- **해결:** `HIGH_PRIORITY_KEYWORDS`의 가중치 값 조정

---

## 🎉 Phase 2 완료!

다음 단계: [Phase 3: 데이터 시각화](PHASE3_VISUALIZATION.md)

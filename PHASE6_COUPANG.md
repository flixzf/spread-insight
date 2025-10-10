# Phase 6: 쿠팡 파트너스 통합 (Week 4)

> 뉴스 키워드 기반 상품 링크 생성

---

## ✅ Step 6.1: 쿠팡 파트너스 링크 생성
**목표:** 뉴스 키워드에 맞는 쿠팡 상품 링크 생성
**소요 시간:** 2시간

### 📝 체크리스트
- [ ] 쿠팡 파트너스 가입
- [ ] `publishers/coupang_partner.py` 작성
- [ ] 키워드 → 상품 매핑 테이블 작성
- [ ] 테스트

### 🛠️ 실행 순서

**1. 쿠팡 파트너스 가입 (옵션)**

> **참고:** 실제 수익화를 원할 경우에만 진행하세요. 테스트 단계에서는 일반 쿠팡 검색 URL을 사용해도 됩니다.

1. https://partners.coupang.com/ 접속
2. 회원가입 및 승인 대기 (1~3일 소요)
3. 승인 후 파트너스 ID 발급받기

**2. Coupang Partner 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\publishers\coupang_partner.py`
```python
from typing import Optional
import urllib.parse


class CoupangPartner:
    """쿠팡 파트너스 링크 생성"""

    # 키워드 → 상품 검색어 매핑
    KEYWORD_TO_PRODUCT = {
        # 환율 관련
        '환율': '여행 가방',
        '달러': '환전',
        '엔화': '일본 여행',

        # 주식/투자 관련
        '주가': '재테크 책',
        '코스피': '주식 투자 책',
        '코스닥': '주식 투자',
        '투자': '재테크',
        '증시': '경제 도서',

        # 금리/대출 관련
        '금리': '재테크 책',
        '대출': '금융 도서',
        '이자': '적금',

        # 부동산 관련
        '부동산': '인테리어',
        '집값': '부동산 책',
        '아파트': '인테리어 소품',

        # 물가/소비 관련
        '물가': '생활용품',
        '소비': '가계부',
        'CPI': '경제 도서',

        # 기업/산업 관련
        '삼성': '삼성 전자제품',
        '현대': '자동차 용품',
        '반도체': '전자제품',
        '자동차': '자동차 용품',

        # 기본 (매칭 안 될 경우)
        'default': '경제 도서'
    }

    def __init__(self, partner_id: str = None):
        """
        partner_id: 쿠팡 파트너스 ID (옵션)
                   없으면 일반 검색 URL 생성
        """
        self.partner_id = partner_id
        self.base_url = 'https://www.coupang.com/np/search'

    def _encode_query(self, query: str) -> str:
        """URL 인코딩"""
        return urllib.parse.quote(query)

    def generate_link(self, keywords: list[str] = None, article_keywords: list[str] = None) -> str:
        """키워드 기반 쿠팡 링크 생성

        Args:
            keywords: 우선순위 높은 키워드 (제목에서 추출)
            article_keywords: 일반 키워드 (본문에서 추출)

        Returns:
            쿠팡 검색 URL
        """
        # 키워드 매칭 시도
        product_query = None

        # 1차: 우선순위 키워드에서 매칭
        if keywords:
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in self.KEYWORD_TO_PRODUCT:
                    product_query = self.KEYWORD_TO_PRODUCT[keyword_lower]
                    print(f"  매칭: '{keyword}' → '{product_query}'")
                    break

        # 2차: 일반 키워드에서 매칭
        if not product_query and article_keywords:
            for keyword in article_keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in self.KEYWORD_TO_PRODUCT:
                    product_query = self.KEYWORD_TO_PRODUCT[keyword_lower]
                    print(f"  매칭: '{keyword}' → '{product_query}'")
                    break

        # 3차: 기본값
        if not product_query:
            product_query = self.KEYWORD_TO_PRODUCT['default']
            print(f"  기본값: '{product_query}'")

        # URL 생성
        encoded_query = self._encode_query(product_query)
        link = f"{self.base_url}?q={encoded_query}"

        # 파트너스 ID 추가 (옵션)
        if self.partner_id:
            link += f"&channel={self.partner_id}"

        return link

    def generate_links_for_articles(self, articles: list) -> dict[str, str]:
        """여러 기사에 대한 링크 일괄 생성

        Returns:
            {article_url: coupang_link}
        """
        links = {}

        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] {article.title[:40]}")

            # 기사 키워드 사용
            link = self.generate_link(
                keywords=article.keywords,
                article_keywords=None
            )

            links[article.url] = link

        return links
```

**3. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_coupang.py`
```python
from publishers.coupang_partner import CoupangPartner
from utils.file_manager import FileManager


if __name__ == '__main__':
    print("=" * 60)
    print("쿠팡 파트너스 링크 생성 테스트")
    print("=" * 60)

    # 초기화
    coupang = CoupangPartner()  # partner_id는 옵션
    file_manager = FileManager()

    # === 1. 개별 키워드 테스트 ===
    print("\n1단계: 개별 키워드 테스트")
    print("-" * 60)

    test_keywords = [
        ['환율', '달러'],
        ['코스피', '주가'],
        ['부동산', '집값'],
        ['삼성전자'],
        ['알수없음']  # 기본값 테스트
    ]

    for keywords in test_keywords:
        print(f"\n키워드: {keywords}")
        link = coupang.generate_link(keywords=keywords)
        print(f"링크: {link}")

    # === 2. 실제 기사로 테스트 ===
    print("\n\n2단계: 실제 기사로 테스트")
    print("=" * 60)

    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("⚠️  저장된 기사가 없습니다.")
        return

    target_file = 'top_news.json' if 'top_news.json' in saved_files else saved_files[0]
    articles = file_manager.load_articles(target_file)

    print(f"\n로드 파일: {target_file}")
    print(f"총 {len(articles)}개 기사\n")

    links = coupang.generate_links_for_articles(articles)

    # === 3. 결과 요약 ===
    print("\n\n" + "=" * 60)
    print("생성된 링크 요약")
    print("=" * 60)

    for i, (url, link) in enumerate(links.items(), 1):
        article = next(a for a in articles if a.url == url)
        print(f"\n{i}. {article.title[:50]}")
        print(f"   → {link}")

    print(f"\n✅ 총 {len(links)}개 링크 생성 완료")
```

**4. 실행**
```bash
python test_coupang.py
```

### ✅ 성공 기준
- [ ] 키워드별 다른 상품 링크 생성
- [ ] 매칭 안 되는 키워드는 기본값 사용
- [ ] URL 인코딩 정상 (한글 깨짐 없음)
- [ ] 링크 클릭 시 쿠팡 검색 페이지 정상 표시

### ⚠️ 예상 오류 및 해결

**오류 1:** 모든 기사가 '경제 도서'로 매칭
- **원인:** 키워드 매칭 실패
- **해결:** `KEYWORD_TO_PRODUCT`에 더 많은 키워드 추가

**오류 2:** 한글 깨짐
- **원인:** URL 인코딩 안 됨
- **해결:** `urllib.parse.quote()` 사용 (이미 코드에 포함)

---

## ✅ Step 6.2: 키워드 기반 상품 매칭 고도화
**목표:** Gemini AI를 사용해 더 정확한 상품 추천
**소요 시간:** 1시간

### 🛠️ 실행 순서

**1. coupang_partner.py 업데이트**

기존 파일에 다음 메서드 추가:
```python
import google.generativeai as genai
from utils.config import Config

class CoupangPartner:
    # ... (기존 코드) ...

    def __init__(self, partner_id: str = None, use_ai: bool = False):
        self.partner_id = partner_id
        self.base_url = 'https://www.coupang.com/np/search'
        self.use_ai = use_ai

        if use_ai:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def _ai_suggest_product(self, title: str, keywords: list[str]) -> str:
        """AI를 사용해 상품 추천"""
        if not self.use_ai:
            return None

        prompt = f"""
다음 경제 뉴스를 읽은 사람이 관심 가질 만한 쿠팡 상품을 1개 추천해주세요.

뉴스 제목: {title}
키워드: {', '.join(keywords) if keywords else '없음'}

**규칙:**
- 뉴스와 연관성이 있어야 함
- 실용적인 상품
- 한 단어 또는 짧은 구문 (예: "여행 가방", "재테크 책")

추천 상품:
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            product = response.text.strip()
            print(f"  AI 추천: '{product}'")
            return product
        except Exception as e:
            print(f"  AI 추천 실패: {e}")
            return None

    def generate_link_with_ai(self, article) -> str:
        """AI 기반 링크 생성"""
        # AI 추천 시도
        product_query = None

        if self.use_ai:
            product_query = self._ai_suggest_product(
                title=article.title,
                keywords=article.keywords
            )

        # AI 실패 시 기존 방식
        if not product_query:
            return self.generate_link(keywords=article.keywords)

        # URL 생성
        encoded_query = self._encode_query(product_query)
        link = f"{self.base_url}?q={encoded_query}"

        if self.partner_id:
            link += f"&channel={self.partner_id}"

        return link
```

**2. AI 기반 추천 테스트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_coupang_ai.py`
```python
from publishers.coupang_partner import CoupangPartner
from utils.file_manager import FileManager


if __name__ == '__main__':
    print("=" * 60)
    print("AI 기반 상품 추천 테스트")
    print("=" * 60)

    # AI 모드 활성화
    coupang = CoupangPartner(use_ai=True)
    file_manager = FileManager()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다.")
        exit(1)

    target_file = 'top_news.json' if 'top_news.json' in saved_files else saved_files[0]
    articles = file_manager.load_articles(target_file)

    print(f"\n로드 파일: {target_file}")
    print(f"총 {len(articles)}개 기사\n")

    # 각 기사에 대해 AI 추천
    print("=" * 60)
    print("AI 기반 상품 추천")
    print("=" * 60)

    for i, article in enumerate(articles[:3], 1):  # 상위 3개만 테스트
        print(f"\n[{i}] {article.title}")
        print(f"키워드: {', '.join(article.keywords) if article.keywords else '없음'}")

        link = coupang.generate_link_with_ai(article)
        print(f"링크: {link}\n")

    print("✅ 테스트 완료")
```

**3. 실행**
```bash
python test_coupang_ai.py
```

### ✅ 성공 기준
- [ ] AI가 뉴스 내용 기반 상품 추천
- [ ] 추천 상품이 뉴스와 연관성 있음
- [ ] AI 실패 시 기존 방식으로 폴백

### ⚠️ 예상 오류 및 해결

**오류 1:** AI 추천이 너무 추상적 (예: "경제 관련 상품")
- **해결:** 프롬프트에 "구체적인 상품명" 강조

**오류 2:** Gemini API 할당량 초과
- **해결:** `use_ai=False`로 설정하여 기존 방식 사용

---

## 🎉 Phase 6 완료!

다음 단계: [Phase 7: 전체 통합 및 자동화](PHASE7_INTEGRATION.md)

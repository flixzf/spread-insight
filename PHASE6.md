# Phase 6: 쿠팡 파트너스 연동

> 목표: 기사 주제에 맞는 도서/제품 추천 및 수익화

---

## 개요

쿠팡 파트너스는 쿠팡의 상품을 추천하고 구매 시 수수료를 받는 제휴 마케팅 프로그램입니다.

**핵심 기능:**
1. 기사 주제 분석 → 관련 도서/제품 추출
2. 쿠팡 파트너스 링크 생성
3. HTML 및 텔레그램 메시지에 링크 삽입
4. 클릭/구매 추적 (쿠팡 대시보드)

---

## Step 6.1: 쿠팡 파트너스 가입 ⏳

### 1. 가입 절차

1. **쿠팡 파트너스 사이트 방문**
   - https://partners.coupang.com/

2. **회원 가입**
   - 쿠팡 계정으로 로그인
   - 파트너스 약관 동의
   - 정산 정보 입력 (계좌번호)

3. **승인 대기**
   - 보통 1-3일 소요
   - 웹사이트/블로그/SNS 정보 필요
   - GitHub Pages 링크 제출 가능

### 2. API 키 발급

**참고:** 쿠팡 파트너스는 공식 API를 제공하지 않습니다.

**대안 방식:**
- **딥링크 생성기**: 수동으로 링크 생성
- **상품 검색**: 쿠팡 웹사이트에서 직접 검색
- **링크 템플릿**: 파트너스 ID를 포함한 URL 패턴 사용

### 3. 파트너스 ID 확인

파트너스 대시보드에서 확인:
```
https://partners.coupang.com/
→ [내 정보]
→ 파트너스 ID (예: your_partner_id)
```

`.env` 파일에 추가:
```env
COUPANG_PARTNERS_ID=your_partner_id
```

---

## Step 6.2: 도서 추천 시스템 구현 ⏳

**목표:** 기사 주제에 맞는 도서 자동 추천

### 도서 데이터베이스 구조

**파일:** `data/recommended_books.json`

```json
{
  "금리": [
    {
      "title": "금리의 모든 것",
      "author": "홍길동",
      "description": "금리를 쉽게 이해하는 책",
      "coupang_url": "https://www.coupang.com/vp/products/123456",
      "keywords": ["금리", "기준금리", "금융"]
    }
  ],
  "부동산": [
    {
      "title": "부동산 투자 입문",
      "author": "김철수",
      "description": "부동산 시장을 분석하는 방법",
      "coupang_url": "https://www.coupang.com/vp/products/789012",
      "keywords": ["부동산", "아파트", "전세"]
    }
  ]
}
```

### 추천 로직

**파일:** `publishers/book_recommender.py`

```python
class BookRecommender:
    def __init__(self, books_db_path: str):
        """도서 DB 로드"""

    def recommend(self, article_data: dict, max_books: int = 2) -> list:
        """
        기사 키워드 기반으로 관련 도서 추천

        1. 기사 키워드 추출
        2. 각 카테고리의 도서와 매칭
        3. 관련성 점수 계산
        4. 상위 N개 반환
        """
```

---

## Step 6.3: 파트너스 링크 생성기 구현 ⏳

**파일:** `publishers/coupang_partners.py`

### 링크 생성 방식

#### 방법 1: 직접 링크 (권장)
쿠팡 상품 URL에 파트너스 ID 추가:

```
원본: https://www.coupang.com/vp/products/123456
파트너스: https://link.coupang.com/a/123456?lptag=AF1234567&subid=your_subid
```

#### 방법 2: 쿠팡 딥링크 생성기
파트너스 대시보드에서 수동 생성:
1. 상품 URL 입력
2. 딥링크 생성 클릭
3. 생성된 링크 복사

### 구현 예시

```python
class CoupangPartners:
    def __init__(self, partner_id: str):
        self.partner_id = partner_id

    def generate_link(self, product_url: str, subid: str = "") -> str:
        """
        쿠팡 파트너스 링크 생성

        Args:
            product_url: 원본 상품 URL
            subid: 추적용 서브 ID (선택)

        Returns:
            파트너스 링크
        """
        # URL에서 상품 ID 추출
        product_id = self._extract_product_id(product_url)

        # 파트너스 링크 생성
        return f"https://link.coupang.com/a/{product_id}?lptag={self.partner_id}&subid={subid}"

    def _extract_product_id(self, url: str) -> str:
        """URL에서 상품 ID 추출"""
        import re
        match = re.search(r'/products/(\d+)', url)
        return match.group(1) if match else ""
```

---

## Step 6.4: 콘텐츠 통합 ⏳

### HTML 템플릿 수정

**파일:** `templates/components/more.html`

```html
<div class="coupang-section">
    <h3>추천 도서</h3>

    {% for book in recommended_books %}
    <div class="book-card">
        <h4>{{ book.title }}</h4>
        <p class="author">{{ book.author }}</p>
        <p class="description">{{ book.description }}</p>
        <a href="{{ book.affiliate_link }}"
           target="_blank"
           class="coupang-button">
            쿠팡에서 보기
        </a>
    </div>
    {% endfor %}

    <p class="coupang-disclaimer">
        이 포스팅은 쿠팡 파트너스 활동의 일환으로,
        이에 따른 일정액의 수수료를 제공받습니다.
    </p>
</div>
```

### 텔레그램 메시지 수정

**파일:** `publishers/telegram_formatter.py`

```python
def _format_more(self, article_data: dict) -> str:
    """More 섹션 (도서 추천 포함)"""
    url = article_data.get('url', '')
    source = self.escape(article_data.get('source', ''))

    message = f"*🔗 더 알아보기*\n\n"
    message += f"[{source} 기사 원문]({url})\n\n"

    # 추천 도서
    books = article_data.get('recommended_books', [])
    if books:
        message += "*📚 추천 도서*\n\n"
        for book in books:
            title = self.escape(book['title'])
            link = book['affiliate_link']
            message += f"• [{title}]({link})\n"

    message += "\n━━━━━━━━━━━━━━━━━━━━\n"
    message += "_이 포스팅은 쿠팡 파트너스 활동의 일환으로,_\n"
    message += "_이에 따른 일정액의 수수료를 제공받습니다._"

    return message
```

---

## Step 6.5: 도서 DB 구축 ⏳

### 초기 도서 목록 (예시)

**카테고리별 추천 도서:**

#### 1. 금리/금융
- 금리의 모든 것
- 한국은행이 말하는 금융정책
- 돈의 흐름이 보이는 세계사

#### 2. 부동산
- 부동산 투자 무작정 따라하기
- 부의 지도
- 똑똑한 부동산 투자

#### 3. 주식/투자
- 주식투자 무작정 따라하기
- 현명한 투자자
- 부자 아빠 가난한 아빠

#### 4. 경제 입문
- 경제학 콘서트
- 괴짜 경제학
- 넛지

#### 5. 물가/인플레이션
- 인플레이션의 시대
- 돈의 역사
- 화폐전쟁

### 도서 추가 프로세스

1. 쿠팡에서 도서 검색
2. 상품 URL 복사
3. `recommended_books.json`에 추가
4. 키워드 매칭 설정

---

## Step 6.6: 수익 추적 ⏳

### 쿠팡 파트너스 대시보드

**확인 가능한 지표:**
- 클릭 수
- 구매 전환율
- 수수료 금액
- 인기 상품

**접속 방법:**
```
https://partners.coupang.com/
→ [실적 관리]
→ [일별 실적]
```

### 내부 추적 (선택)

**파일:** `database/tracking.db` (SQLite)

```sql
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY,
    article_id TEXT,
    book_title TEXT,
    affiliate_link TEXT,
    clicked_at TIMESTAMP
);
```

**구현:** Phase 7 전체 통합 시 추가

---

## 완료 기준

- [ ] 쿠팡 파트너스 가입 및 승인
- [ ] 파트너스 ID 발급
- [ ] 도서 데이터베이스 구축 (최소 20권)
- [ ] BookRecommender 클래스 구현
- [ ] CoupangPartners 링크 생성기 구현
- [ ] HTML 템플릿에 도서 섹션 추가
- [ ] 텔레그램 메시지에 도서 링크 추가
- [ ] 실제 기사로 테스트

---

## 현재 상태

- **Phase 1-5:** ✅ 완료
- **Phase 6:** 🔜 시작 예정

---

## 다음 단계

Phase 7: 전체 통합
- 엔드투엔드 자동화 파이프라인
- 일일 스케줄링
- GitHub Actions 배포

---

## 참고 자료

- [쿠팡 파트너스 공식 사이트](https://partners.coupang.com/)
- [쿠팡 파트너스 가이드](https://partners.coupang.com/hc/ko)
- [쿠팡 파트너스 정책](https://partners.coupang.com/hc/ko/articles/360034789354)

---

## 중요 사항

### 쿠팡 파트너스 정책 준수

1. **정직한 리뷰**
   - 실제로 추천할 만한 도서만 선정
   - 과장 금지

2. **명확한 고지**
   - 파트너스 수수료를 받는다는 사실 명시
   - "이 포스팅은 쿠팡 파트너스..." 문구 필수

3. **금지 사항**
   - 자동 클릭 유도
   - 거짓 정보
   - 쿠팡 상표권 침해

위반 시 파트너스 자격 박탈 가능

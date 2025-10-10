# 쿠팡 파트너스 준수사항 가이드

## ⚠️ 필독: 제휴 링크 생성 요구사항

이 문서는 쿠팡 파트너스 프로그램의 준수사항을 정리한 것입니다.
**반드시 이 가이드를 따라야 정상적으로 수익이 집계됩니다.**

---

## 1. 제휴 링크 생성 방법

### ❌ 잘못된 방법 (수익 집계 안 됨)

다음 방법으로 생성한 링크는 **수익이 집계되지 않습니다**:

1. **쿠팡 페이지 URL 직접 복사**
   ```
   https://www.coupang.com/vp/products/1234567
   ```

2. **쿠팡 앱/웹의 공유 기능 사용**
   - 상품 페이지의 "공유" 버튼으로 생성된 링크
   - 카카오톡, 문자 등으로 공유된 링크

3. **URL 패턴을 수동으로 조합**
   ```python
   # ❌ 이렇게 하면 안 됩니다!
   link = f"https://link.coupang.com/a/{product_id}"
   ```

### ✅ 올바른 방법 (수익 집계 됨)

**반드시 쿠팡 파트너스 시스템을 통해 링크를 생성해야 합니다:**

1. **파트너스 대시보드 접속**
   - URL: https://partners.coupang.com
   - 로그인 후 "링크 생성" 메뉴 선택

2. **링크 생성 도구 사용**

   파트너스 대시보드에서 제공하는 3가지 방법:

   #### a) 상품 링크 (Product Link)
   - 특정 상품 페이지로 연결
   - 상품 URL을 입력하면 파트너스 링크 생성
   - 예시: `https://link.coupang.com/a/bSHxyz123`

   #### b) 간편 링크 (Simple Link)
   - 빠르게 링크 생성
   - 검색어 또는 카테고리 기반
   - 예시: `https://link.coupang.com/re/CATEXYZ`

   #### c) 이벤트/프로모션 링크
   - 쿠팡 기획전 페이지 링크
   - 예시: 로켓배송 기획전, 특가 이벤트 등

3. **API 사용 (선택사항)**
   - 파트너스 API 문서 참고 (대시보드 내 제공)
   - Product API, Deep Link API 등
   - 대량 링크 생성 시 유용

---

## 2. 대가성 문구 (필수)

### 법적 요구사항

공정거래위원회 가이드라인에 따라:
- **모든 제휴 링크 사용 시 대가성 문구를 명시해야 합니다**
- 대가성 문구 없이 링크만 게시하면 법적 문제 발생 가능

### 권장 문구

```
이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
```

### HTML 템플릿 예시

```html
<div class="coupang-section">
    <h3>추천 도서</h3>
    <a href="https://link.coupang.com/a/xxxxx" target="_blank">
        도서 제목
    </a>

    <!-- 대가성 문구 (필수) -->
    <p class="coupang-disclaimer">
        이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
    </p>
</div>
```

---

## 3. 수익 정산 정책

### 기본 규칙

- **쿠키 유효 기간**: 24시간
  - 사용자가 링크 클릭 후 24시간 내 구매한 상품에 대해 수수료 발생

- **최소 정산 금액**: 10,000원
  - 누적 수수료가 10,000원 이상일 때 정산 신청 가능

- **정산 주기**: 월 1회
  - 매월 초 전월 실적 정산

- **최종 승인 후 정산**
  - 구매 확정 → 반품 기간 경과 → 최종 승인 → 정산

### 수익이 발생하지 않는 경우

1. 링크가 파트너스 시스템을 통해 생성되지 않은 경우
2. 대가성 문구가 없는 경우 (법적 제재 가능)
3. 금지된 홍보 방식 (스팸, 허위 정보 등)

---

## 4. 코드 구현 가이드

### 현재 프로젝트 적용 방법

#### Step 1: 파트너스 대시보드에서 링크 생성

```python
# 1. https://partners.coupang.com 접속
# 2. 링크 생성 도구에서 상품 검색
# 3. 생성된 파트너스 링크 복사
# 예: https://link.coupang.com/a/bSHxyz123
```

#### Step 2: 도서 정보에 링크 추가

```python
books = [
    {
        'title': '경제학 콘서트',
        'author': '팀 하포드',
        'description': '경제학의 기본 원리를 쉽게 설명',
        'coupang_url': 'https://link.coupang.com/a/bSHxyz123'  # 파트너스에서 생성한 링크
    }
]
```

#### Step 3: CoupangPartners 클래스로 검증 및 처리

```python
from publishers.coupang_partners import CoupangPartners

partners = CoupangPartners()

# 링크 검증 및 affiliate_link 필드 추가
books_with_links = partners.validate_and_add_affiliate_links(books)

# 유효하지 않은 링크는 경고 메시지 출력
# [WARNING] 도서 'XXX': 유효하지 않은 파트너스 링크입니다.
# 파트너스 대시보드(https://partners.coupang.com)에서 링크를 생성해주세요.
```

#### Step 4: HTML 생성 시 대가성 문구 자동 포함

템플릿(`templates/components/more.html`)에서 자동으로 처리됩니다:

```html
<div class="coupang-section">
    <h3>추천 도서</h3>

    {% if article.recommended_books %}
    <div class="books-grid">
        {% for book in article.recommended_books %}
        <div class="book-card">
            <h4>{{ book.title }}</h4>
            <p>{{ book.description }}</p>
            <a href="{{ book.affiliate_link }}" target="_blank">
                쿠팡에서 보기 →
            </a>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- 대가성 문구 (자동 포함) -->
    <p class="coupang-disclaimer">
        이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
    </p>
</div>
```

---

## 5. 자주 묻는 질문 (FAQ)

### Q1. 테스트 단계에서 어떻게 해야 하나요?

**A:** 두 가지 방법:
1. **실제 파트너스 링크 사용** (권장)
   - 파트너스 가입 후 실제 링크 생성
   - 클릭 통계 등을 확인 가능

2. **더미 링크 사용** (테스트용)
   ```python
   'coupang_url': ''  # 빈 문자열
   # 또는
   'coupang_url': 'https://link.coupang.com/a/test123'  # 형식만 맞춤
   ```

### Q2. 파트너스 가입 없이 개발할 수 있나요?

**A:** 가능합니다. 코드 개발과 테스트는 가입 없이 진행 가능하지만:
- 실제 수익화를 원하면 반드시 가입 필요
- 파트너스 ID 승인까지 1~3일 소요

### Q3. 링크 유효성 검증은 어떻게 하나요?

**A:** `CoupangPartners.validate_partner_link()` 메서드 사용:
```python
partners = CoupangPartners()
is_valid = partners.validate_partner_link('https://link.coupang.com/a/xxxxx')

# 유효한 패턴:
# - https://link.coupang.com/a/xxxxx
# - https://link.coupang.com/re/xxxxx
```

### Q4. 대가성 문구를 커스터마이징할 수 있나요?

**A:** 가능합니다:
```python
custom_text = "본 포스팅은 쿠팡 파트너스 프로그램의 일환으로 수수료를 받을 수 있습니다."
partners = CoupangPartners(disclosure_text=custom_text)
```

단, 공정거래위원회 가이드라인을 준수해야 하므로 기본 문구 사용을 권장합니다.

---

## 6. 체크리스트

프로젝트에 파트너스를 적용하기 전에 다음을 확인하세요:

- [ ] 쿠팡 파트너스 가입 완료 (실제 수익화 시)
- [ ] 파트너스 대시보드에서 링크 생성 방법 숙지
- [ ] `CoupangPartners` 클래스 이해
- [ ] 대가성 문구가 HTML 템플릿에 포함되어 있는지 확인
- [ ] 링크 검증 로직 테스트 완료
- [ ] 금지된 링크 생성 방식(URL 직접 조합 등)을 사용하지 않음

---

## 7. 참고 자료

- **쿠팡 파트너스 공식 사이트**: https://partners.coupang.com
- **파트너스 가이드 PDF**: `partners-guide.pdf` (프로젝트 루트)
- **공정거래위원회 가이드**: 검색어 "공정거래위원회 제휴 마케팅"
- **프로젝트 구현 파일**:
  - `publishers/coupang_partners.py`: 핵심 로직
  - `templates/components/more.html`: HTML 템플릿
  - `test_coupang.py`: 테스트 스크립트

---

## 8. 문제 해결

### 링크가 작동하지 않을 때

1. **링크 형식 확인**
   ```bash
   python publishers/coupang_partners.py
   ```
   - 유효한 파트너스 링크 형식인지 검증

2. **파트너스 대시보드 확인**
   - 링크가 정상적으로 생성되었는지 확인
   - 링크 클릭 통계가 집계되는지 확인

3. **브라우저 테스트**
   - 링크를 직접 클릭해서 쿠팡 페이지로 이동하는지 확인
   - 개발자 도구로 리다이렉트 확인

### 수익이 집계되지 않을 때

1. 파트너스 시스템으로 생성한 링크인지 확인
2. 대가성 문구가 표시되는지 확인
3. 쿠키가 정상적으로 설정되는지 확인 (브라우저 개발자 도구)

---

**마지막 업데이트**: 2025-10-10
**작성자**: Claude
**문서 버전**: 1.0

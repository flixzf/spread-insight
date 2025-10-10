# Phase 4: HTML 페이지 생성

> 목표: 분석된 뉴스 데이터를 CONTENT_STRATEGY.md에 정의된 7섹션 구조로 표시하는 HTML 페이지 생성

---

## Step 4.1: 템플릿 시스템 구축 ⏳

**목표:**
- Jinja2 기반 HTML 템플릿 엔진 설정
- 재사용 가능한 컴포넌트 구조 설계

**필요 라이브러리:**
```
jinja2==3.1.3
```

**파일 구조:**
```
templates/
├── base.html              # 기본 레이아웃 (헤더, 푸터)
├── news_template.html     # 뉴스 메인 템플릿
└── components/
    ├── header.html        # 헤드라인 섹션
    ├── what.html          # What 섹션
    ├── learn.html         # Learn 섹션 (용어 설명)
    ├── past.html          # Past 섹션 (과거 데이터)
    ├── insight.html       # Insight 섹션
    ├── action.html        # Action 섹션
    └── more.html          # More 섹션
```

---

## Step 4.2: 7섹션 HTML 템플릿 작성 ⏳

**CONTENT_STRATEGY.md 매핑:**

### 1. 헤드라인 (Header)
- 기사 제목 (강조)
- 한 줄 요약
- 출처, 날짜
- 대표 이미지 영역 (현재는 placeholder)

### 2. What (무슨 일이?)
- 3문장 요약 (article.summary)
- 쉬운 설명 (article.easy_explanation)
- 핵심 키워드 태그

### 3. Learn (오늘의 용어)
- 추출된 용어 설명 (article.terminology)
- [용어], [쉽게], [중요] 형식
- 최대 1개 (CONTENT_STRATEGY 기준)

### 4. Past (과거에는 어땠을까?) - 준비 단계
```html
<!-- Phase 3에서 구현 예정 -->
<div class="past-section placeholder">
  <p>🚧 과거 데이터 연동 준비 중...</p>
</div>
```

### 5. Insight (이번엔 다를 수 있다) - 준비 단계
```html
<!-- Gemini 고급 분석 추가 예정 -->
<div class="insight-section placeholder">
  <p>🚧 심층 인사이트 기능 준비 중...</p>
</div>
```

### 6. Action (나는 어떻게?)
- 실천 가능한 행동 제안
- 체크리스트 형태
- **현재:** 템플릿만 준비 (하드코딩 샘플)

### 7. More (더 알아보기)
- 원문 링크
- 관련 키워드 링크
- 쿠팡 파트너스 링크 영역 (준비)

---

## Step 4.3: HTML 생성기 구현 ⏳

**파일:** `generators/html_generator.py`

**클래스 설계:**
```python
class HTMLGenerator:
    def __init__(self, template_dir: str = './templates'):
        """Jinja2 환경 초기화"""

    def generate_from_json(self, json_path: str, output_path: str):
        """JSON 파일에서 HTML 생성"""

    def generate_from_article(self, article_data: dict, output_path: str):
        """딕셔너리에서 직접 HTML 생성"""

    def _prepare_template_data(self, article_data: dict) -> dict:
        """템플릿에 전달할 데이터 준비"""
        # 날짜 포맷팅
        # 본문 단락 나누기
        # placeholder 데이터 추가
```

---

## Step 4.4: CSS 스타일링 ⏳

**파일:** `templates/static/style.css`

**디자인 원칙:**
- 모바일 우선 (반응형)
- 읽기 편한 타이포그래피
- 섹션별 명확한 구분
- 텔레그램에서 보기 좋은 레이아웃
- 쿠팡 파트너스 배너 영역

**색상 팔레트 (예시):**
```css
:root {
  --primary: #2c3e50;
  --accent: #3498db;
  --learn: #f39c12;
  --action: #27ae60;
  --bg: #ecf0f1;
}
```

---

## Step 4.5: 통합 테스트 ⏳

**테스트 파일:** `test_html_generation.py`

**테스트 시나리오:**
1. `article_with_terminology.json` 읽기
2. HTML 생성
3. 출력 파일: `./output/article_2025-10-09.html`
4. 브라우저에서 확인

**검증 항목:**
- [x] 모든 섹션 렌더링
- [x] 한글 인코딩 정상
- [x] 용어 설명 포맷팅
- [x] 반응형 레이아웃 동작
- [x] 외부 링크 작동

---

## Step 4.6: GitHub Pages 배포 준비 ⏳

**목표:**
- 정적 HTML을 GitHub Pages로 호스팅
- 매일 자동 업데이트 구조 설계

**준비사항:**
1. `docs/` 폴더 생성 (GitHub Pages 소스)
2. `index.html` = 최신 기사
3. `archive/` = 과거 기사들
4. GitHub Actions 워크플로우 설계 (Phase 7에서 구현)

---

## 완료 기준

- [ ] Jinja2 템플릿 엔진 설정 완료
- [ ] 7개 섹션 HTML 템플릿 작성
- [ ] HTMLGenerator 클래스 구현
- [ ] CSS 스타일 적용
- [ ] 실제 기사로 HTML 생성 테스트 성공
- [ ] 브라우저에서 정상 표시 확인

---

## 현재 상태

- **Phase 1:** ✅ 완료 (뉴스 선정)
- **Phase 2:** ✅ 완료 (AI 분석)
- **Phase 3:** ⏭️ 건너뜀 (프로토타입 우선)
- **Phase 4:** 🔜 시작 예정

---

## 다음 단계

Phase 5: 텔레그램 봇 연동
- HTML을 텔레그램 메시지로 전송
- MarkdownV2 포맷 변환
- 일일 자동 발송 스케줄링

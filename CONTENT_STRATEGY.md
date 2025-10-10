# 콘텐츠 전략 (Content Strategy)

> **핵심 목표:** 단순 뉴스 전달이 아닌, 하루 1개의 "배움과 실용적 인사이트"를 제공하여 독자가 "오늘 이것을 배웠다"는 뿌듯함과 "나는 어떻게 해야 할까?"라는 실천으로 이어지도록 함.

---

## 🎯 콘텐츠 철학

### "Learn → Insight → Action"
1. **Learn (배움):** 오늘의 경제 이슈와 핵심 용어 1개 학습
2. **Insight (통찰):** 과거 데이터와 비교하여 패턴과 의미 파악
3. **Action (실천):** 개인이 취할 수 있는 구체적 행동 제시

### 예시 시나리오: "미국 금리 인하 뉴스"

**기존 방식 (단순 뉴스):**
```
미국 연준(Fed)이 기준금리를 0.25%p 인하했습니다.
현재 금리는 4.75%입니다.
```

**Spread Insight 방식:**
```
📊 오늘의 핵심: 미국 금리 인하, 당신의 투자는?

💡 무슨 일이?
미국 연준이 기준금리를 4.75%로 0.25%p 인하했습니다.

📚 알아두면 좋은 용어
"기준금리": 중앙은행이 시중은행에 돈을 빌려줄 때의 이자율.
금리가 내려가면 → 대출 이자 ↓, 예금 이자 ↓, 주식/부동산 투자 증가 경향

📈 과거에는 어땠을까?
[차트] 2019년 금리 인하 사이클 vs 주요 자산 변화
- S&P 500: +15% (6개월 후)
- 달러 가치: -3%
- 금 가격: +8%

⚠️ 이번엔 다를 수 있다 (Insight)
- 2019년과 달리 현재 인플레이션 3.2%로 여전히 높음
- 과거 금리 인하 후 주식 상승했지만, 인플레이션 재발 시 역효과
- 전문가 의견: "섣불리 위험자산 확대하지 말고, 분산 투자 유지"

✅ 나는 어떻게 할까?
1. 대출 상환 계획이 있다면 → 금리가 더 내려가기 전에 고정금리 전환 고려
2. 예금 중심 투자자 → 일부 배당주/채권 혼합 고려
3. 달러 보유자 → 환율 하락 가능성 있으니 분할 환전 검토

🔗 관련 상품 (쿠팡 파트너스)
- 경제 공부 도서: "금리의 모든 것"
- 재테크 강의 쿠폰
```

---

## 1️⃣ 어떤 뉴스를 골라낼 것인가?

### 선정 기준

#### A. **영향력 (Impact)**
- ✅ 대부분의 사람들에게 직접 영향을 주는가?
  - 금리, 환율, 물가, 부동산 정책, 세금
- ❌ 특정 업종/기업에만 해당하는 뉴스
  - 예: "○○전자, 신제품 출시" (제외)

#### B. **실천 가능성 (Actionable)**
- ✅ 독자가 직접 행동할 수 있는가?
  - 대출 전환, 투자 조정, 소비 전략 변경
- ❌ 정보만 있고 행동 불가능한 뉴스
  - 예: "전문가들의 의견 분분" (제외)

#### C. **학습 가치 (Educational)**
- ✅ 경제 용어 1개 이상 포함되어 있는가?
  - 기준금리, 인플레이션, GDP, 유동성, 스태그플레이션
- ✅ 과거 데이터와 비교 가능한가?
  - 역사적 패턴, 통계적 경향성

#### D. **시의성 (Timeliness)**
- ✅ 오늘/이번 주에 발표된 뉴스인가?
- ❌ 1개월 이상 지난 뉴스

### 뉴스 선정 프로세스 (자동화)

```python
# analyzers/news_selector.py

class NewsSelector:
    """뉴스 선정 로직"""

    PRIORITY_KEYWORDS = [
        # 금융
        "금리", "환율", "연준", "한국은행", "기준금리",
        # 부동산
        "부동산", "아파트", "전세", "집값", "대출",
        # 물가/세금
        "물가", "인플레이션", "소비자물가", "세금", "세제",
        # 투자
        "주식", "코스피", "다우", "나스닥", "채권",
        # 정책
        "정부", "정책", "법안", "규제"
    ]

    def calculate_score(self, article: NewsArticle) -> float:
        """뉴스 점수 계산 (0~100)"""
        score = 0

        # 1. 키워드 매칭 (40점)
        title_keywords = sum(1 for kw in self.PRIORITY_KEYWORDS if kw in article.title)
        content_keywords = sum(1 for kw in self.PRIORITY_KEYWORDS if kw in article.content)
        score += min(40, (title_keywords * 10) + (content_keywords * 2))

        # 2. 시의성 (20점)
        hours_old = (datetime.now() - article.published_at).total_seconds() / 3600
        if hours_old < 6:
            score += 20
        elif hours_old < 24:
            score += 15
        elif hours_old < 48:
            score += 10

        # 3. 신뢰도 (20점) - 주요 언론사
        trusted_sources = ["한국경제", "매일경제", "조선일보", "중앙일보"]
        if any(src in article.source for src in trusted_sources):
            score += 20

        # 4. 본문 길이 (10점) - 너무 짧거나 길지 않은 것
        content_length = len(article.content)
        if 500 <= content_length <= 3000:
            score += 10

        # 5. 숫자/통계 포함 여부 (10점) - 데이터 기반 뉴스
        import re
        numbers = re.findall(r'\d+\.?\d*%', article.content)
        if len(numbers) >= 3:
            score += 10

        return score

    def select_top_news(self, articles: list[NewsArticle], top_n: int = 1) -> list[NewsArticle]:
        """상위 N개 뉴스 선정"""
        scored = [(article, self.calculate_score(article)) for article in articles]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [article for article, score in scored[:top_n]]
```

### Gemini를 활용한 2차 필터링

뉴스 선정 점수가 높은 상위 3~5개 기사를 Gemini에게 보내 최종 1개 선택:

```python
# analyzers/gemini_selector.py

def select_best_news_with_ai(self, candidates: list[NewsArticle]) -> NewsArticle:
    """Gemini에게 최종 뉴스 선택 요청"""
    prompt = f"""
다음은 오늘의 경제 뉴스 후보입니다.
일반인이 "오늘 이것을 배웠다"는 뿌듯함을 느끼고,
"나는 어떻게 해야할까?"로 이어질 수 있는 가장 적합한 기사 1개를 선택해주세요.

선택 기준:
1. 대부분의 사람에게 직접 영향
2. 과거 데이터와 비교 가능
3. 구체적 행동으로 연결 가능
4. 핵심 경제 용어 1개 이상 포함

후보:
{self._format_candidates(candidates)}

답변 형식:
선택한 기사 번호: [번호]
선택 이유: [1~2문장]
핵심 용어: [추출할 경제 용어]
    """

    response = self.model.generate_content(prompt)
    # 파싱 후 해당 기사 반환
```

---

## 2️⃣ 어떻게 내용을 전달할 것인가?

### 콘텐츠 구조 (템플릿)

#### **섹션 1: 헤드라인 (Hook)**
```
📊 오늘의 핵심: [한 줄 요약]
```
- 목적: 3초 안에 관심 유도
- 길이: 20자 이내
- 예시: "미국 금리 인하, 당신의 투자는?"

#### **섹션 2: What (무슨 일이?)**
```
💡 무슨 일이 일어났나요?
[3문장 요약]
```
- 목적: 핵심 사실 전달
- 길이: 3~5문장
- 톤: 뉴스 진행자처럼 객관적

#### **섹션 3: Learn (오늘의 용어)**
```
📚 알아두면 좋은 용어
"[용어]": [초등학생도 이해할 설명]

예시를 들면?
[구체적 사례]
```
- 목적: 경제 문해력 향상
- 길이: 2~3문장 + 예시 1개
- 톤: 친구가 설명해주는 느낌

#### **섹션 4: Past (과거에는?)**
```
📈 과거에는 어땠을까?
[차트 이미지]

요약:
- [패턴 1]
- [패턴 2]
- [패턴 3]
```
- 목적: 맥락 이해, 데이터 기반 판단력
- 시각화: 필수
- 데이터 출처: 명시

#### **섹션 5: Insight (이번엔 다를 수 있다)**
```
⚠️ 이번엔 다를 수 있어요

과거와 다른 점:
1. [차이점 1]
2. [차이점 2]

전문가 의견:
"[핵심 인용]" - [출처]
```
- 목적: 비판적 사고, 맹신 방지
- 톤: 균형잡힌 시각

#### **섹션 6: Action (나는 어떻게?)**
```
✅ 나는 어떻게 할까요?

[독자 유형 1]
→ [구체적 행동 1]

[독자 유형 2]
→ [구체적 행동 2]

[독자 유형 3]
→ [구체적 행동 3]
```
- 목적: 실천으로 연결
- 독자 세분화:
  - 예금 중심 / 대출 있음 / 투자 중심 / 직장인 / 자영업자

#### **섹션 7: 더 알아보기 (선택)**
```
🔗 더 알아보고 싶다면?
- 관련 도서: [쿠팡 링크]
- 관련 강의: [쿠팡 링크]
```

---

## 3️⃣ 과거 내용과 어떻게 연결할 것인가?

### 데이터 소스

#### A. **공공 데이터 API**
- 한국은행 경제통계시스템 (ECOS API)
  - 금리, 환율, 물가지수, GDP
  - URL: https://ecos.bok.or.kr/api/
- 통계청 KOSIS API
  - 고용, 가계소득, 소비자물가
- 국토교통부 실거래가 API
  - 아파트 매매/전세 가격

#### B. **금융 데이터**
- `yfinance` 라이브러리 (주가)
  ```python
  import yfinance as yf

  # S&P 500 과거 6개월 데이터
  sp500 = yf.Ticker("^GSPC")
  hist = sp500.history(period="6mo")
  ```

- `pandas_datareader` (경제 지표)
  ```python
  from pandas_datareader import data as pdr

  # 미국 10년물 국채 금리
  treasury = pdr.get_data_fred('DGS10', start='2020-01-01')
  ```

#### C. **자체 데이터베이스**
- 과거 분석한 뉴스 저장
- 주요 이벤트 타임라인 구축
  ```sql
  -- database/schema.sql
  CREATE TABLE historical_events (
      id INTEGER PRIMARY KEY,
      event_date DATE,
      event_type VARCHAR(50), -- 'rate_cut', 'rate_hike', 'policy_change'
      description TEXT,
      impact_score FLOAT
  );
  ```

### 비교 분석 자동화

```python
# analyzers/historical_analyzer.py

class HistoricalAnalyzer:
    """과거 데이터와 비교 분석"""

    def find_similar_events(self, current_news: NewsArticle) -> list[dict]:
        """유사한 과거 이벤트 찾기"""

        # 1. 뉴스에서 이벤트 타입 추출 (Gemini)
        event_type = self._extract_event_type(current_news)
        # 예: "금리 인하"

        # 2. DB에서 유사 이벤트 조회
        past_events = self.db.query(
            "SELECT * FROM historical_events WHERE event_type = ? ORDER BY event_date DESC LIMIT 5",
            (event_type,)
        )

        # 3. 각 이벤트 발생 후 주요 지표 변화 계산
        analysis = []
        for event in past_events:
            after_6m = self._get_market_change(event['event_date'], months=6)
            analysis.append({
                'date': event['event_date'],
                'description': event['description'],
                'sp500_change': after_6m['sp500'],
                'dollar_change': after_6m['dollar'],
                'gold_change': after_6m['gold']
            })

        return analysis

    def _get_market_change(self, start_date: date, months: int) -> dict:
        """특정 날짜 이후 N개월간 시장 변화율"""
        end_date = start_date + timedelta(days=months*30)

        # yfinance로 데이터 가져오기
        sp500 = yf.Ticker("^GSPC").history(start=start_date, end=end_date)
        change_pct = ((sp500['Close'][-1] - sp500['Close'][0]) / sp500['Close'][0]) * 100

        return {
            'sp500': round(change_pct, 2),
            # ... 다른 지표들
        }
```

### Gemini를 활용한 맥락 생성

```python
def generate_historical_context(self, current_news: NewsArticle, past_events: list[dict]) -> str:
    """과거 데이터를 기반으로 맥락 설명 생성"""

    prompt = f"""
현재 뉴스:
{current_news.title}
{current_news.content[:500]}

과거 유사한 사건들:
{json.dumps(past_events, ensure_ascii=False, indent=2)}

위 정보를 바탕으로 아래 형식으로 답변해주세요:

1. 과거 패턴 (3줄 이내):
- [패턴 1]
- [패턴 2]
- [패턴 3]

2. 이번에 다른 점 (2~3문장):
[과거와 현재의 차이점]

3. 예상되는 시나리오 (낙관/비관):
[간결한 전망]
    """

    response = self.gemini.generate_content(prompt)
    return response.text
```

---

## 4️⃣ 어떤 것을 어떻게 차트로 보여줄 것인가?

### 차트 종류별 사용 시나리오

#### A. **선 그래프 (Line Chart)** - 시간 흐름
**사용 사례:**
- 금리 변화 추이
- 주가 지수 변화
- 환율 추이

**예시 코드:**
```python
# visualizers/line_chart.py

import plotly.graph_objects as go

def create_rate_history_chart(dates: list, rates: list, events: list[dict]) -> str:
    """금리 변화 + 주요 이벤트 표시"""

    fig = go.Figure()

    # 금리 선
    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        mode='lines+markers',
        name='기준금리',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=6)
    ))

    # 주요 이벤트 표시 (수직선)
    for event in events:
        fig.add_vline(
            x=event['date'],
            line_dash="dash",
            line_color="red",
            annotation_text=event['name']
        )

    fig.update_layout(
        title="미국 기준금리 변화 (최근 5년)",
        xaxis_title="날짜",
        yaxis_title="금리 (%)",
        template="plotly_white",
        font=dict(family="Noto Sans KR", size=12),
        hovermode='x unified'
    )

    # HTML로 저장
    html_path = "./data/charts/rate_history.html"
    fig.write_html(html_path)
    return html_path
```

#### B. **막대 그래프 (Bar Chart)** - 비교
**사용 사례:**
- 과거 금리 인하 후 자산별 수익률 비교
- 국가별 금리 비교

```python
def create_asset_comparison_chart(assets: dict) -> str:
    """자산별 수익률 비교"""

    fig = go.Figure(data=[
        go.Bar(
            x=list(assets.keys()),
            y=list(assets.values()),
            marker_color=['#10b981' if v > 0 else '#ef4444' for v in assets.values()],
            text=[f"{v:+.1f}%" for v in assets.values()],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title="금리 인하 후 6개월간 자산 수익률",
        yaxis_title="수익률 (%)",
        template="plotly_white"
    )

    return fig
```

#### C. **히트맵 (Heatmap)** - 패턴
**사용 사례:**
- 요일별/월별 주가 변화 패턴
- 금리 구간별 자산 성과

#### D. **캔들스틱 (Candlestick)** - 주가
**사용 사례:**
- 이벤트 전후 주가 흐름

### 차트 자동 선택 로직

```python
# visualizers/chart_selector.py

class ChartSelector:
    """뉴스 내용에 맞는 차트 자동 선택"""

    def select_chart_type(self, news: NewsArticle, data_type: str) -> str:
        """
        data_type: 'rate', 'price', 'comparison', 'stock'
        """

        if data_type == 'rate':
            # 금리 → 시계열 라인 차트
            return 'line_with_events'

        elif data_type == 'comparison':
            # 비교 → 막대 그래프
            return 'bar_comparison'

        elif data_type == 'stock':
            # 주가 → 캔들스틱
            return 'candlestick'

        else:
            # 기본: 라인 차트
            return 'line'
```

### 시각화 가이드라인

1. **색상 팔레트**
   - 상승/긍정: `#10b981` (초록)
   - 하락/부정: `#ef4444` (빨강)
   - 중립/정보: `#3b82f6` (파랑)

2. **한글 폰트**
   ```python
   import plotly.io as pio

   pio.templates["korean"] = go.layout.Template(
       layout=go.Layout(
           font=dict(family="Noto Sans KR"),
           title_font_size=16
       )
   )
   pio.templates.default = "korean"
   ```

3. **모바일 최적화**
   - 차트 크기: 800x500px (텔레그램 적합)
   - 텍스트 크기: 12px 이상
   - 범례 위치: 하단

---

## 5️⃣ 어떤 용어를 쉽게 전달할 것인가?

### 용어 선정 기준

#### A. **필수 용어 (Tier 1)** - 일상 생활 직결
- 기준금리, 인플레이션, 환율, GDP
- 전세가율, 담보대출비율(LTV)
- 주가지수 (코스피, 다우, 나스닥)

#### B. **권장 용어 (Tier 2)** - 뉴스 이해 필수
- 양적완화(QE), 긴축, 유동성
- 배당수익률, PER, PBR
- 모기지, 스프레드

#### C. **심화 용어 (Tier 3)** - 전문성
- 스태그플레이션, 역마진
- 콜옵션, 풋옵션
- 통화스와프

### 용어 자동 추출 및 난이도 판단

```python
# analyzers/terminology_extractor.py

class TerminologyExtractor:
    """경제 용어 추출 및 설명 생성"""

    TERM_DATABASE = {
        "기준금리": {
            "tier": 1,
            "category": "금융",
            "simple_def": "중앙은행이 시중은행에 돈을 빌려줄 때의 이자율",
            "example": "기준금리가 5%에서 4.75%로 내려가면, 은행 대출 이자도 함께 낮아지는 경향이 있어요."
        },
        "인플레이션": {
            "tier": 1,
            "category": "물가",
            "simple_def": "물가가 지속적으로 오르는 현상",
            "example": "작년에 1000원이던 라면이 올해 1100원이 되었다면, 10% 인플레이션이 발생한 거예요."
        }
        # ... 100개 이상 등록
    }

    def extract_terms(self, article: NewsArticle, max_terms: int = 1) -> list[dict]:
        """기사에서 중요 용어 추출"""

        # 1. 기사에서 등록된 용어 찾기
        found_terms = []
        for term, info in self.TERM_DATABASE.items():
            if term in article.content:
                found_terms.append({
                    'term': term,
                    'tier': info['tier'],
                    'count': article.content.count(term)
                })

        # 2. Tier 1 우선, 출현 빈도 고려하여 정렬
        found_terms.sort(key=lambda x: (x['tier'], -x['count']))

        # 3. 상위 N개 반환
        return found_terms[:max_terms]

    def generate_explanation(self, term: str) -> dict:
        """용어 쉬운 설명 생성"""

        if term in self.TERM_DATABASE:
            info = self.TERM_DATABASE[term]
            return {
                'term': term,
                'definition': info['simple_def'],
                'example': info['example'],
                'tier': info['tier']
            }

        # 데이터베이스에 없으면 Gemini에게 요청
        return self._generate_with_gemini(term)

    def _generate_with_gemini(self, term: str) -> dict:
        """Gemini로 새로운 용어 설명 생성"""

        prompt = f"""
다음 경제 용어를 초등학생도 이해할 수 있게 설명해주세요:

용어: {term}

답변 형식:
1. 한 줄 정의 (20자 이내):
2. 구체적 예시 (일상생활 비유):
3. 왜 중요한가? (1문장):
        """

        response = self.gemini.generate_content(prompt)
        # 파싱 후 반환
```

### 용어 설명 템플릿

```markdown
📚 알아두면 좋은 용어

**"[용어]"**
[한 줄 정의]

💡 쉽게 말하면?
[일상생활 비유]

📌 예를 들면?
[구체적 사례]

⚠️ 왜 중요할까요?
[실생활 영향]
```

**예시:**
```markdown
📚 알아두면 좋은 용어

**"기준금리"**
중앙은행이 시중은행에 돈을 빌려줄 때의 이자율

💡 쉽게 말하면?
경제의 "수도꼭지"입니다.
꼭지를 잠그면(금리 인상) → 돈의 흐름이 줄어들고
꼭지를 열면(금리 인하) → 돈의 흐름이 늘어나요.

📌 예를 들면?
기준금리 5% → 4.75%로 하락
→ 은행 대출 이자 하락 (5.5% → 5.25%)
→ 예금 이자도 하락 (4% → 3.8%)

⚠️ 왜 중요할까요?
기준금리가 바뀌면 내 대출 이자, 예금 이자,
주식 시장, 부동산 가격이 모두 영향을 받아요.
```

---

## 🤖 AI 프롬프트 전략

### 종합 콘텐츠 생성 프롬프트

```python
# analyzers/content_generator.py

class ContentGenerator:
    """최종 콘텐츠 생성"""

    def generate_full_content(
        self,
        news: NewsArticle,
        historical_data: dict,
        chart_path: str,
        terminology: dict
    ) -> str:
        """모든 섹션을 종합하여 최종 콘텐츠 생성"""

        prompt = f"""
당신은 경제 뉴스를 일반인에게 쉽게 전달하는 교육 콘텐츠 작가입니다.

원본 뉴스:
제목: {news.title}
내용: {news.content}

과거 데이터:
{json.dumps(historical_data, ensure_ascii=False, indent=2)}

핵심 용어:
{terminology['term']}: {terminology['definition']}

다음 형식으로 콘텐츠를 작성해주세요:

---
📊 오늘의 핵심: [20자 이내 한 줄 요약]

💡 무슨 일이 일어났나요?
[3~5문장으로 핵심 사실 전달]

📚 알아두면 좋은 용어
"{terminology['term']}": {terminology['definition']}

💡 쉽게 말하면?
[일상생활 비유로 설명]

📈 과거에는 어땠을까?
[과거 데이터 기반 패턴 3가지]

⚠️ 이번엔 다를 수 있어요
과거와 다른 점:
1. [차이점 1]
2. [차이점 2]

전문가 의견:
[균형잡힌 전망]

✅ 나는 어떻게 할까요?

💰 예금 중심 투자자라면?
→ [구체적 행동]

🏠 대출이 있다면?
→ [구체적 행동]

📈 투자를 하고 있다면?
→ [구체적 행동]
---

작성 시 주의사항:
1. 존댓말 사용 (친근한 톤)
2. 전문용어는 {terminology['term']} 하나만 사용
3. 구체적 수치와 예시 포함
4. 불안 조장하지 말고 균형잡힌 시각
5. 행동 제안은 "~하세요" 대신 "~고려해보세요" 사용
        """

        response = self.gemini.generate_content(prompt)
        return response.text
```

---

## 📊 성공 지표 (KPI)

### 콘텐츠 품질
- [ ] 용어 설명 이해도: 90% 이상 (독자 설문)
- [ ] 차트 가독성: 5점 만점에 4점 이상
- [ ] 행동 실천율: 독자의 30% 이상이 제안 행동 실천

### 독자 참여
- [ ] 텔레그램 채널 구독자 증가율: 월 10%
- [ ] 콘텐츠 공유율: 독자의 15% 이상
- [ ] 쿠팡 링크 클릭률: 5% 이상

### 학습 효과
- [ ] 독자 경제 문해력 향상 (용어 테스트)
- [ ] "도움 되었다" 피드백: 80% 이상

---

## 🚀 다음 단계

1. **Step 2.6 (신규):** 뉴스 선정 로직 구현
2. **Step 2.7 (신규):** 과거 데이터 수집 자동화
3. **Step 2.8 (신규):** 용어 데이터베이스 구축
4. **Step 3.4 (신규):** 차트 자동 생성 시스템

---

이 전략을 바탕으로 단순 뉴스 전달이 아닌, **매일 성장하는 독자**를 만드는 것이 목표입니다.

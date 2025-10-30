# Spread Insight - 압축 플로우 가이드 (n8n 자동화용)

## 프로젝트 개요
AI 기반 경제 뉴스 자동 큐레이션 시스템. 네이버 뉴스 → AI 분석 → 텔레그램 자동 전송 (하루 9회)

## 핵심 플로우 (6단계, 총 ~40초)

### STEP 1: 메타데이터 수집 (~5초)
- URL: `https://news.naver.com/section/101`
- 추출: 30개 기사의 제목/요약/URL
- 도구: BeautifulSoup (셀렉터: `.sa_item .sa_text_title`)

### STEP 2: AI 뉴스 선정 (~3초)
- API: Gemini Flash Lite
- 입력: 30개 메타데이터
- 프롬프트: "경제 편집장 역할. 경제 영향력/시의성/실용성 기준으로 1개 선정"
- 출력: 선정 번호 (정규식 추출: `선정\s*번호\s*[:：]\s*(\d+)`)

### STEP 3: 전체 스크래핑 (~2초)
- 입력: 선정된 URL
- 셀렉터: 제목 `#title_area span`, 본문 `#dic_area`, 날짜 `.media_end_head_info_datestamp_time`

### STEP 4: Gemini 3중 분석 (~8초)
**A. 요약**: "3문장으로 요약"
**B. 투자 인사이트**:
```
Q. 무슨 일이야? A. [2-3문장: 핵심+중요성]
Q. 내 투자엔 어떤 영향? A. [3-4문장: 수혜종목, 타격종목, 과거사례, 연관자산]
Q. 뭘 주목해야 해? A. [2-3문장: 다음이벤트, 기관시각, 등락시나리오]
```
**C. 키워드**: 보편적 카테고리 5개 (고유명사X)

### STEP 5: 쿠팡 추천 (~2초, 선택)
- 키워드 기반 상품 검색 (1개)
- 제휴 공시 추가

### STEP 6: 텔레그램 발송 (~15초)
- 타이틀 전송 → 3초 대기
- 본문 메시지 순차 전송 (각 3초 간격)

## n8n 워크플로우 구성

### WF1: 메인 뉴스 (09:00, 12:00, 18:00)
```
Cron(0 9,12,18 * * *)
→ HTTP(네이버)
→ HTMLExtract(.sa_item, limit=30)
→ HTTP(Gemini 선정, POST, body={contents:[{parts:[{text:prompt}]}]})
→ Code(번호추출)
→ HTTP(기사스크래핑)
→ HTMLExtract(#title_area, #dic_area)
→ HTTP(Gemini 요약)
→ HTTP(Gemini 설명)
→ HTTP(Gemini 키워드)
→ HTTP(쿠팡API, optional)
→ Code(메시지포맷)
→ Telegram(타이틀)
→ Wait(3s)
→ Loop(본문메시지들) → Telegram → Wait(3s)
```

### WF2: 시장 현황 (10:00, 15:00)
```
Cron(0 10,15 * * *)
→ HTTP(Yahoo KOSPI: ^KS11)
→ HTTP(Yahoo 환율: USDKRW=X)
→ Code(등락률계산+포맷)
→ Telegram
```

### WF3: 시장 차트 (14:00, 20:00)
```
Cron(0 14,20 * * *)
→ HTTP(Yahoo 30일데이터)
→ HTTP(QuickChart.io/chart, type:line, data:{{values}})
→ Telegram(send_photo)
```

### WF4: 경제 용어 (11:00)
```
Cron(0 11 * * *)
→ Code(JSON로드: economic_terms.json, 날짜%개수)
→ Telegram
```

### WF5: 투자 꿀팁 (16:00)
```
Cron(0 16 * * *)
→ Code(JSON로드: investment_tips.json, 날짜%개수)
→ Telegram
```

## API 엔드포인트

### Gemini API
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent
Headers:
  Content-Type: application/json
  x-goog-api-key: {{GEMINI_API_KEY}}
Body: {"contents":[{"parts":[{"text":"프롬프트"}]}]}
```

### Yahoo Finance
```
GET https://query1.finance.yahoo.com/v8/finance/chart/^KS11  # KOSPI
GET https://query1.finance.yahoo.com/v8/finance/chart/USDKRW=X  # 환율
```

### QuickChart (차트 생성)
```
POST https://quickchart.io/chart
Body: {"chart":{"type":"line","data":{"labels":[],"datasets":[{"data":[]}]}}}
```

### Telegram
```
POST https://api.telegram.org/bot{{TOKEN}}/sendMessage
Body: {"chat_id":"{{CHAT_ID}}","text":"{{MESSAGE}}"}

POST https://api.telegram.org/bot{{TOKEN}}/sendPhoto
Body: {"chat_id":"{{CHAT_ID}}","photo":"{{URL}}"}
```

## 환경 변수
```
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-lite
TELEGRAM_BOT_TOKEN=1234:ABC...
TELEGRAM_CHAT_ID=-1001234...
```

## 실행 스케줄 (KST)
| 시간 | 작업 | 소요 |
|-----|------|-----|
| 09:00 | 뉴스 | 40초 |
| 10:00 | 시장현황 | 5초 |
| 11:00 | 경제용어 | 3초 |
| 12:00 | 뉴스 | 40초 |
| 14:00 | 차트 | 10초 |
| 15:00 | 시장현황 | 5초 |
| 16:00 | 투자팁 | 3초 |
| 18:00 | 뉴스 | 40초 |
| 20:00 | 차트 | 10초 |

## 핵심 프롬프트

### 뉴스 선정
```
당신은 경제 뉴스 편집장. 다음 30개 뉴스 중 경제적으로 가장 중요한 뉴스 1개 선정.
기준: 경제영향력(금리/환율/관세/무역/증시), 시의성, 실용성(재테크도움), 학습가치
제외: 부고/인사이동/광고/지엽적뉴스
답변: "선정 번호: [번호]\n선정 이유: [50자]"
뉴스목록: {{metadata_list}}
```

### 투자 인사이트
```
10초 안에 이해할 핵심 Q&A 작성:
Q. 무슨 일이야?
A. [첫문장: 한마디 핵심, 둘째: 구체숫자, 셋째: 왜중요]

Q. 내 투자엔 어떤 영향?
A. [첫: 수혜종목명, 둘: 타격종목, 셋: 과거사례(연도+수치), 넷: 연관자산]

Q. 뭘 주목해야 해?
A. [첫: 다음이벤트, 둘: 기관시각, 셋: 등락시나리오]

원칙: 구체숫자필수, 고유명사명확, 과거사례는연도+수치, 명사형종결
본문: {{content}}
```

## 메시지 포맷 (v2)
```
═══════════════
📰 경제 뉴스
═══════════════
{{title}}
{{date}}
═══════════════

📌 핵심 3줄 요약
{{summary}}

💡 핵심 3줄
{{easy_explanation}}

🏷️ 키워드
{{keywords}}

🛒 관련 상품
{{coupang_recommendations}}
{{disclosure}}
```

## 데이터 구조

### NewsArticle
```json
{
  "url": "https://...",
  "title": "제목",
  "content": "본문",
  "published_at": "2025-10-30T09:00:00",
  "source": "네이버",
  "summary": "3문장 요약",
  "easy_explanation": "Q&A 형식",
  "keywords": ["키워드1", "키워드2", ...]
}
```

### economic_terms.json
```json
{
  "금리": "돈을 빌려줄 때 받는 이자의 비율...",
  "환율": "서로 다른 나라 화폐 교환 비율..."
}
```

### investment_tips.json
```json
[
  {
    "title": "달러 비용 평균법",
    "content": "매월 같은 금액으로 투자하여..."
  }
]
```

## 에러 핸들링
- AI 선정 실패 → 첫 번째 뉴스 선택
- API 타임아웃 → 재시도 1회 (2초 대기)
- 스크래핑 실패 → 로그 출력 후 스킵

## 비용
- Gemini Flash Lite: ~$0/월 (무료 한도)
- Telegram: 무료
- Yahoo Finance: 무료
- **총: $0-5/월**

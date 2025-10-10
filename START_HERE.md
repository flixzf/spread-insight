# 🚀 Spread Insight - 시작 가이드

> **단순 뉴스 전달이 아닌, 매일 성장하는 독자 만들기**
>
> 경제 뉴스 + 과거 데이터 + AI 인사이트 → "오늘 이것을 배웠다!"

---

## 🎯 프로젝트 핵심 가치

이 프로젝트는 단순히 뉴스를 스크래핑하는 것이 아닙니다.

### Learn → Insight → Action
1. **Learn (배움):** 하루 1개의 경제 이슈 + 핵심 용어 학습
2. **Insight (통찰):** 과거 데이터와 비교하여 패턴 파악
3. **Action (실천):** "나는 어떻게 해야 할까?"로 이어지는 구체적 행동 제시

**예시:**
```
"미국 금리 인하" 뉴스
→ 과거 금리 인하 후 자산별 수익률 차트 제공
→ 2019년과 현재의 차이점 분석
→ 대출/예금/투자자별 구체적 행동 제안
```

---

## 📚 문서 구조

이 프로젝트는 **스몰 석세스(Small Success)** 방식으로 진행됩니다.
각 단계를 성공해야만 다음 단계로 진행할 수 있습니다.

### 📖 읽는 순서

1. **[PROJECT_PLAN.md](PROJECT_PLAN.md)** ← 먼저 읽기!
   - 전체 프로젝트 개요
   - 기술 스택 선정 이유
   - 시스템 아키텍처

2. **[CONTENT_STRATEGY.md](CONTENT_STRATEGY.md)** ← 핵심 전략!
   - 어떤 뉴스를 골라낼 것인가?
   - 어떻게 내용을 전달할 것인가?
   - 과거 데이터와 어떻게 연결할 것인가?
   - 어떤 차트를 보여줄 것인가?
   - 어떤 용어를 쉽게 전달할 것인가?

3. **Phase별 상세 가이드** (순서대로 진행)
   - [DETAILED_STEPS.md](DETAILED_STEPS.md) - Phase 1 상세 (뉴스 수집) ✅ 완료
   - [PHASE2_AI_ANALYSIS.md](PHASE2_AI_ANALYSIS.md) - AI 분석 🔜 진행 중
   - [PHASE3_VISUALIZATION.md](PHASE3_VISUALIZATION.md) - 데이터 시각화
   - [PHASE4_WEB_GENERATION.md](PHASE4_WEB_GENERATION.md) - 웹 페이지 생성
   - [PHASE5_TELEGRAM.md](PHASE5_TELEGRAM.md) - 텔레그램 연동
   - [PHASE6_COUPANG.md](PHASE6_COUPANG.md) - 쿠팡 파트너스
   - [PHASE7_INTEGRATION.md](PHASE7_INTEGRATION.md) - 전체 통합

4. **[PROGRESS.md](PROGRESS.md)** - 프로젝트 진행 상황 ⭐
   - 완료된 작업 기록
   - 현재 상태 및 다음 단계
   - 핵심 기술 결정 사항

5. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - 문제 해결
   - 발생한 오류와 해결 방법 기록
   - 환경 설정 이슈
   - 베스트 프랙티스

---

## 🎯 빠른 시작

### 1️⃣ 개발 환경 설정 (30분)

```bash
# 1. 프로젝트 폴더로 이동
cd "g:\내 드라이브\08.Programming\spread_insight"

# 2. 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화 (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 4. 의존성 설치 (Phase 1만)
pip install beautifulsoup4 requests lxml python-dotenv
```

**성공 확인:**
```bash
pip list
# beautifulsoup4, requests, lxml, python-dotenv 확인
```

👉 **다음:** [DETAILED_STEPS.md](DETAILED_STEPS.md) Step 1.2로 이동

---

### 2️⃣ 첫 번째 성공: 뉴스 1개 수집 (1시간)

**목표:** 네이버 뉴스 1개 기사 스크래핑

```bash
# 1. 필요한 파일 작성 (DETAILED_STEPS.md 참고)
# - models/news_article.py
# - scrapers/base_scraper.py
# - scrapers/naver_scraper.py
# - test_scraper.py

# 2. 실행
python test_scraper.py
```

**성공 화면:**
```
✅ 스크래핑 성공!

제목: 환율 급등, 달러당 1,400원 돌파
출처: 네이버
날짜: 2025년 01월 10일 15:30
본문 길이: 1524자
...
```

👉 **다음:** [DETAILED_STEPS.md](DETAILED_STEPS.md) Step 1.3으로 이동

---

## 📅 권장 학습 일정 (5주)

### Week 1: 뉴스 수집
- [ ] Day 1-2: 환경 설정 + 네이버 스크래퍼
- [ ] Day 3-4: 다음 스크래퍼 + 데이터 저장
- [ ] Day 5: 데이터 정제 및 검증

### Week 2: AI 분석
- [ ] Day 1: Gemini API 연동 + 요약
- [ ] Day 2: 쉬운 언어 변환
- [ ] Day 3: 용어 추출
- [ ] Day 4: 과거 맥락 (타임라인)
- [ ] Day 5: 중요도 랭킹

### Week 3: 시각화 + 웹
- [ ] Day 1: 그래프 기본 (더미 데이터)
- [ ] Day 2: 실제 데이터 (환율, 주가)
- [ ] Day 3: HTML 템플릿 + 생성
- [ ] Day 4-5: GitHub Pages 배포

### Week 4: 배포
- [ ] Day 1-2: 텔레그램 봇
- [ ] Day 3: 쿠팡 파트너스
- [ ] Day 4-5: 구독자 관리

### Week 5: 통합 + 자동화
- [ ] Day 1-3: 전체 파이프라인 통합
- [ ] Day 4: 스케줄러
- [ ] Day 5: 최종 테스트

---

## ✅ 체크리스트

### Phase 1: 뉴스 수집
- [ ] 네이버 스크래퍼 동작
- [ ] 다음 스크래퍼 동작
- [ ] JSON 저장 성공
- [ ] 중복 제거 동작

### Phase 2: AI 분석
- [ ] Gemini API 연결
- [ ] 요약 생성
- [ ] 쉬운 설명 생성
- [ ] 용어 해설 생성
- [ ] 타임라인 생성
- [ ] 중요도 점수 계산

### Phase 3: 시각화
- [ ] 그래프 생성 (한글 정상)
- [ ] 실제 환율 데이터 수집
- [ ] 실제 주가 데이터 수집
- [ ] 자동 그래프 선택

### Phase 4: 웹 페이지
- [ ] HTML 템플릿 작성
- [ ] HTML 생성 동작
- [ ] GitHub Pages 배포

### Phase 5: 텔레그램
- [ ] 봇 생성 및 연결
- [ ] 메시지 전송
- [ ] 버튼 UI 동작
- [ ] 구독자 관리

### Phase 6: 쿠팡
- [ ] 링크 생성
- [ ] 키워드 매칭

### Phase 7: 통합
- [ ] 전체 파이프라인 동작
- [ ] 스케줄러 동작
- [ ] 최종 테스트 성공

---

## 🆘 문제 해결

### 자주 발생하는 오류

**1. `ModuleNotFoundError`**
```bash
# 가상환경이 활성화되어 있는지 확인
# 터미널 앞에 (venv) 표시 확인

# 라이브러리 재설치
pip install -r requirements.txt
```

**2. 한글 깨짐**
- 모든 파일을 UTF-8 인코딩으로 저장
- 코드에 `encoding='utf-8'` 확인

**3. API 연결 실패**
- `.env` 파일 확인
- API 키 유효성 확인
- 인터넷 연결 확인

---

## 📞 도움말

### 각 Phase별 상세 가이드에는:
- ✅ 체크리스트
- 🛠️ 실행 순서 (복사 가능한 전체 코드)
- ✅ 성공 기준
- ⚠️ 예상 오류 및 해결책

### 파일 구조:
```
spread_insight/
├── START_HERE.md           ← 지금 여기!
├── PROJECT_PLAN.md         ← 전체 개요
├── DETAILED_STEPS.md       ← Phase 1 상세
├── PHASE2_AI_ANALYSIS.md   ← Phase 2 상세
├── PHASE3_VISUALIZATION.md ← Phase 3 상세
├── PHASE4_WEB_GENERATION.md← Phase 4 상세
├── PHASE5_TELEGRAM.md      ← Phase 5 상세
├── PHASE6_COUPANG.md       ← Phase 6 상세
└── PHASE7_INTEGRATION.md   ← Phase 7 상세
```

---

## 🎓 학습 팁

1. **한 번에 하나씩**
   - 각 단계를 완전히 이해하고 성공한 후 다음으로

2. **실제로 코드 작성하기**
   - 복사/붙여넣기만 하지 말고 직접 타이핑
   - 각 줄이 무엇을 하는지 이해

3. **에러는 친구**
   - 에러 메시지를 꼼꼼히 읽기
   - 예상 오류 섹션 확인

4. **테스트, 테스트, 테스트**
   - 각 단계마다 테스트 스크립트 실행
   - 로그 확인

---

## 🚀 시작하기

👉 **[PROJECT_PLAN.md](PROJECT_PLAN.md)** 를 먼저 읽고 전체 구조를 이해하세요.

👉 그 다음 **[DETAILED_STEPS.md](DETAILED_STEPS.md)** Step 1.1부터 시작하세요!

**행운을 빕니다! 🍀**

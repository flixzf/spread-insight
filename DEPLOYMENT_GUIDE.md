# 🚀 Spread Insight 배포 가이드

Phase 2A 업데이트 포함 - 시장 데이터 및 차트 기능 추가

---

## 📋 현재 버전 정보

```
v1.0-phase1-complete: 기본 뉴스 스크래핑 + 텔레그램 발송
Phase 2A (최신): 실시간 시장 현황 + 차트 자동 발송
```

### 롤백 방법
```bash
# Phase 1으로 되돌리기
git checkout v1.0-phase1-complete

# 최신 버전으로 복구
git checkout claude/session-011CUYr83ghk6X2kLHsAG8YP
```

---

## 🎯 배포 전 체크리스트

### ✅ 필수 환경변수

| 변수명 | 설명 | 필수 | 예시 |
|--------|------|------|------|
| `GEMINI_API_KEY` | Gemini AI API 키 | ✅ | `AIzaSy...` |
| `GEMINI_MODEL` | Gemini 모델 | ✅ | `gemini-2.0-flash-lite` |
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 토큰 | ✅ | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | 텔레그램 채팅 ID | ✅ | `-1001234567890` |
| `TELEGRAM_FORMAT_VERSION` | 메시지 포맷 버전 | ⭕ | `v2` (기본값: `v1`) |

### 📦 의존성 패키지

**Phase 1 (기존):**
- `google-generativeai` - Gemini AI
- `python-telegram-bot` - 텔레그램 봇
- `beautifulsoup4` - 웹 스크래핑
- `schedule` - 스케줄링

**Phase 2A (신규):**
- `yfinance` - 시장 데이터 API ⭐ NEW
- `pykrx` - 한국 시장 데이터 ⭐ NEW
- `matplotlib` - 차트 생성 ⭐ NEW

---

## 🕐 스케줄 구성

### 📰 뉴스 발송 (기존)
- **09:00 KST** (00:00 UTC) - 아침 뉴스
- **12:00 KST** (03:00 UTC) - 점심 뉴스
- **18:00 KST** (09:00 UTC) - 저녁 뉴스

### 📈 시장 현황 (NEW)
- **10:00 KST** (01:00 UTC) - 시장 오픈 현황
- **15:00 KST** (06:00 UTC) - 실시간 지표

### 📊 차트 발송 (NEW)
- **14:00 KST** (05:00 UTC) - 오전 시장 요약 차트
- **20:00 KST** (11:00 UTC) - 일일 마감 차트

**총 7회 자동 발송 (기존 3회 → 7회)**

---

## 🚂 Railway 배포 단계

### Step 1: Repository 준비

```bash
# 최신 코드 확인
git log --oneline -3

# 다음이 보여야 함:
# a133070 Phase 2A: Add market data features
# bd2e126 Phase 1: Fix critical code quality issues
```

### Step 2: Railway 프로젝트 설정

1. **Railway 대시보드** 접속
2. 기존 프로젝트 선택 (또는 새로 생성)
3. **Settings** → **GitHub Repo** 연결 확인

### Step 3: 환경변수 입력

Railway 대시보드 → **Variables** 탭:

```bash
# 필수 변수
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-lite
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# 선택 변수
TELEGRAM_FORMAT_VERSION=v2
```

⚠️ **주의사항:**
- 따옴표 없이 값만 입력
- 공백 제거
- API 키 오타 주의

### Step 4: 배포 확인

1. **Deployments** 탭 → 자동 배포 시작
2. **Logs** 탭 → 로그 확인

**정상 로그 예시:**
```
Spread Insight Scheduler Started
======================================================================
📰 News Schedule:
  - 09:00 KST (00:00 UTC) - Morning news
  - 12:00 KST (03:00 UTC) - Lunch news
  - 18:00 KST (09:00 UTC) - Evening news

📈 Market Status Schedule:
  - 10:00 KST (01:00 UTC) - Market open status
  - 15:00 KST (06:00 UTC) - Real-time indicators

📊 Market Chart Schedule:
  - 14:00 KST (05:00 UTC) - Morning market summary chart
  - 20:00 KST (11:00 UTC) - Daily closing chart
======================================================================
Current time: 2025-10-30 15:30:00 KST
Waiting for scheduled time...
```

---

## 🧪 배포 후 테스트

### 1. 즉시 테스트 (Railway CLI)

```bash
# Railway CLI 설치 (한 번만)
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 즉시 실행 테스트
railway run python main.py --now
```

### 2. 텔레그램 확인

다음 시간에 메시지가 자동 발송됩니다:
- ✅ 09:00 - 뉴스 (기존)
- ✅ 10:00 - 시장 현황 ⭐ NEW
- ✅ 12:00 - 뉴스 (기존)
- ✅ 14:00 - 차트 ⭐ NEW
- ✅ 15:00 - 시장 현황 ⭐ NEW
- ✅ 18:00 - 뉴스 (기존)
- ✅ 20:00 - 차트 ⭐ NEW

---

## 🔍 문제 해결

### 문제 1: yfinance 데이터 오류

**증상:**
```
[ERROR] KOSPI 데이터 조회 실패
[ERROR] 환율 데이터 조회 실패
```

**원인:** Railway 서버에서 yfinance API 접근 제한

**해결:**
1. pykrx로 대체 (한국 데이터만)
2. API 타임아웃 설정 확인
3. 재시도 로직 추가 (향후 개선)

### 문제 2: matplotlib 폰트 오류

**증상:**
```
RuntimeWarning: Glyph missing from current font
```

**원인:** Linux 서버에 한글 폰트 없음

**해결:** 이미 구현됨
- `visualizers/market_chart_generator.py`에서 OS별 폰트 자동 감지
- Linux: Nanum 폰트 사용
- 폰트 없으면 기본 폰트 대체

### 문제 3: 차트 생성 실패

**증상:**
```
[ERROR] 차트 생성 실패: No module named 'matplotlib'
```

**원인:** matplotlib 미설치

**해결:**
```bash
# Railway에서 자동으로 requirements.txt 읽어서 설치
# 수동 확인:
railway run pip list | grep matplotlib
```

### 문제 4: 스케줄 미실행

**증상:** 정해진 시간에 메시지 안 옴

**확인 사항:**
1. Railway Logs에서 현재 시간 확인
   ```
   Current time: 2025-10-30 09:00:00 KST
   ```
2. UTC/KST 변환 확인
   - 09:00 KST = 00:00 UTC
   - 시차 9시간 맞는지 확인

---

## 📊 모니터링

### Railway 대시보드

1. **Metrics** 탭
   - CPU 사용률
   - 메모리 사용량
   - 네트워크 트래픽

2. **Logs** 탭
   - 실시간 로그
   - 에러 추적

### 예상 리소스 사용량

**Phase 1 (기존):**
- CPU: ~5%
- RAM: ~100MB
- 실행 시간: 3회 × 45초 = ~2.5분/일

**Phase 2A (현재):**
- CPU: ~10% (차트 생성 시 일시적 증가)
- RAM: ~150MB (matplotlib 로드)
- 실행 시간: 7회 × 30초 = ~3.5분/일

**Railway 무료 플랜:** 충분함 ✅

---

## 🔄 업데이트 배포

새로운 기능을 추가했을 때:

```bash
# 1. 코드 수정 후 커밋
git add .
git commit -m "Add new feature"

# 2. 푸시
git push origin claude/session-011CUYr83ghk6X2kLHsAG8YP

# 3. Railway가 자동으로 재배포
# (GitHub 연동 시)
```

**재배포 소요 시간:** 약 2-3분

---

## 💡 최적화 팁

### 1. 스케줄 조정

원하는 시간으로 변경:
```python
# scheduler.py 수정
schedule.every().day.at("02:00").do(self.run_market_status_job)  # 11:00 KST
```

### 2. 차트 품질 조정

메모리 절약:
```python
# visualizers/market_chart_generator.py
plt.savefig(save_path, dpi=100)  # 기본 150 → 100으로 낮춤
```

### 3. 데이터 캐싱

API 호출 줄이기 (향후 개선):
```python
# Redis 또는 SQLite로 일일 데이터 캐싱
# 동일한 데이터 재사용
```

---

## 📞 지원

### 에러 발생 시

1. **Railway Logs 캡처**
2. **환경변수 확인** (값 제외)
3. **로컬 테스트 실행**
   ```bash
   python test_phase2a.py
   ```

### 참고 문서

- Railway 공식 문서: https://docs.railway.app
- yfinance 문서: https://pypi.org/project/yfinance/
- matplotlib 문서: https://matplotlib.org

---

**마지막 업데이트:** 2025-10-30
**작성자:** Claude
**버전:** Phase 2A

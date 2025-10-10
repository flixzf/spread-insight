# Railway 배포 가이드

Railway에 Spread Insight를 배포하여 매일 9시/12시/18시에 자동으로 뉴스를 발송합니다.

## 📋 사전 준비

### 1. API 키 준비
다음 API 키들을 미리 발급받으세요:

- **Gemini API** (필수)
  - https://aistudio.google.com/app/apikey
  - 무료 사용 가능

- **Telegram Bot Token** (필수)
  - Telegram에서 @BotFather 검색
  - `/newbot` 명령으로 봇 생성
  - 토큰 복사

- **Telegram Chat ID** (필수)
  - 봇을 채널/그룹에 추가
  - https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates 접속
  - `chat.id` 값 확인

### 2. GitHub 계정
- GitHub 계정 생성 (없다면)
- 이 프로젝트를 GitHub에 푸시

---

## 🚀 Railway 배포 단계

### Step 1: Railway 계정 생성
1. https://railway.app 접속
2. **Login with GitHub** 클릭
3. GitHub 연동 승인

### Step 2: 새 프로젝트 생성
1. Railway 대시보드에서 **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. `spread_insight` 레포지토리 선택
4. **Deploy Now** 클릭

### Step 3: 환경변수 설정 (중요!)
1. 프로젝트 클릭 → **Variables** 탭
2. 다음 환경변수들을 **하나씩** 추가:

```
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-lite
TELEGRAM_BOT_TOKEN=your_actual_telegram_bot_token
TELEGRAM_CHAT_ID=your_actual_telegram_chat_id
TELEGRAM_FORMAT_VERSION=v2
```

⚠️ **주의**:
- `your_actual_*` 부분을 실제 키로 교체
- 따옴표 없이 값만 입력
- 복사할 때 앞뒤 공백 주의

### Step 4: 배포 확인
1. **Deployments** 탭에서 배포 로그 확인
2. "News Scheduler Started" 메시지 확인
3. "Waiting for scheduled time..." 확인되면 성공!

---

## 📊 동작 확인

### 로그 확인
- Railway 대시보드 → **Logs** 탭
- 실시간 로그 모니터링 가능

### 예상 로그 메시지
```
News Scheduler Started
======================================================================
Schedule:
  - 09:00 KST (Morning news)
  - 12:00 KST (Lunch news)
  - 18:00 KST (Evening news)
======================================================================
Current time: 2025-10-10 16:40:00 KST
Waiting for scheduled time...
```

### 실행 시 로그
```
[2025-10-10 09:00:05 KST] Starting news scraping and sending...
[Step 1] Collecting article metadata from Naver...
  [OK] Collected 30 article metadata
[Step 2] AI selecting most important news from metadata...
[Step 3] Scraping full article content...
  [OK] Article scraped: ...
[Step 4] Analyzing with Gemini...
  [OK] Analysis done
[Step 5] Generating Coupang recommendations...
  [OK] 1 products recommended
[Step 6] Sending to Telegram...
  [OK] All messages sent!
[SUCCESS] News sent to Telegram!
```

---

## ⚙️ 스케줄 시간 변경

시간을 변경하고 싶다면:

1. Railway에서 프로젝트 클릭
2. **Code** → 파일 편집 가능
3. `scheduler.py` 수정:

```python
# 현재
schedule.every().day.at("09:00").do(self.run_job)
schedule.every().day.at("12:00").do(self.run_job)
schedule.every().day.at("18:00").do(self.run_job)

# 예: 8시/13시/19시로 변경
schedule.every().day.at("08:00").do(self.run_job)
schedule.every().day.at("13:00").do(self.run_job)
schedule.every().day.at("19:00").do(self.run_job)
```

4. 커밋하면 자동 재배포

---

## 💰 비용 관리

### Railway 무료 플랜
- 매달 **$5 크레딧** 무료
- 약 **500시간** 실행 가능
- 이 프로젝트는 월 **730시간**(24시간×30일) 필요

### 예상 비용
- 소형 인스턴스: **$5/월** (크레딧 소진 후)
- 크레딧 활용 시: **$0/월** (첫 500시간)

### 비용 절감 팁
1. **Hobby Plan 구독**: $5/월 → 완전 무료
2. **대안**: Render.com 무료 플랜 사용

---

## 🔧 트러블슈팅

### 배포가 안 돼요
- **원인**: requirements.txt 문제
- **해결**: Railway 로그에서 에러 확인

### 환경변수가 안 먹혀요
- **원인**: 오타 또는 공백
- **해결**: Variables 탭에서 재입력

### 메시지가 안 와요
- **원인 1**: Telegram Chat ID 오류
  - `getUpdates` 다시 확인
- **원인 2**: 시간대 문제
  - 로그에서 "Current time" 확인
  - KST(한국시간) 맞는지 확인

### 로그에서 에러가 나요
```
[ERROR] Scheduler job failed: ...
```
- Railway Logs 전체 복사
- 에러 메시지 확인 후 수정

---

## 🎯 다음 단계

배포 성공 후:

1. ✅ 09:00/12:00/18:00에 메시지 오는지 확인
2. ✅ 로그에서 정상 동작 확인
3. ✅ 비용 모니터링 (Railway Dashboard)

---

## 📞 문의

문제가 생기면:
1. Railway Logs 캡처
2. 환경변수 설정 확인 (키 값 제외)
3. GitHub Issues에 문의

---

**Happy Deploying! 🚀**

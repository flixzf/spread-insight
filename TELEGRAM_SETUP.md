# 텔레그램 봇 설정 가이드

## 1. 텔레그램 봇 생성

### Step 1: BotFather 찾기
1. 텔레그램 앱 열기
2. 검색창에 `@BotFather` 입력
3. 공식 BotFather 선택 (파란색 체크마크 확인)

### Step 2: 새 봇 생성
1. `/start` 명령어 입력
2. `/newbot` 명령어 입력
3. **봇 이름** 입력 (예: `Spread Insight`)
4. **봇 사용자명** 입력 (예: `spread_insight_news_bot`)
   - 반드시 `bot`으로 끝나야 함
   - 이미 사용 중이면 다른 이름 시도

### Step 3: API 토큰 받기
- BotFather가 다음과 같은 형식의 토큰 제공:
  ```
  1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789
  ```
- **⚠️ 이 토큰은 절대 공개하지 말 것!**

---

## 2. Chat ID 확인

### 방법 1: 봇에게 메시지 보내기
1. 생성한 봇 검색 (예: `@spread_insight_news_bot`)
2. `/start` 명령어 또는 아무 메시지 보내기
3. 브라우저에서 다음 URL 접속:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. JSON 응답에서 `"chat":{"id":123456789}` 찾기
5. 이 숫자가 Chat ID

### 방법 2: userinfobot 사용
1. 텔레그램에서 `@userinfobot` 검색
2. `/start` 입력
3. Chat ID 확인

---

## 3. .env 파일 설정

프로젝트 루트의 `.env` 파일에 다음 추가:

```env
# 텔레그램 봇 설정
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789
TELEGRAM_CHAT_ID=123456789
```

**보안 주의사항:**
- `.env` 파일은 절대 Git에 커밋하지 말 것
- `.gitignore`에 `.env`가 포함되어 있는지 확인

---

## 4. 봇 권한 설정 (선택)

### 봇 설명 설정
```
/setdescription
→ 봇 선택
→ "오늘 하나, 제대로 배우는 경제 뉴스" 입력
```

### 봇 프로필 사진 설정
```
/setuserpic
→ 봇 선택
→ 이미지 업로드
```

### 봇 명령어 설정
```
/setcommands
→ 봇 선택
→ 다음 입력:
start - 봇 시작
today - 오늘의 뉴스
help - 도움말
```

---

## 5. 테스트

### 간단한 테스트 스크립트

`test_telegram_connection.py`:
```python
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

load_dotenv()

async def test():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    await bot.send_message(
        chat_id=chat_id,
        text="✅ 텔레그램 봇 연결 성공!"
    )
    print("[OK] 메시지 전송 완료!")

asyncio.run(test())
```

실행:
```bash
python test_telegram_connection.py
```

---

## 6. 문제 해결

### 오류: "Unauthorized"
- 봇 토큰이 잘못되었습니다
- BotFather에서 토큰 재확인

### 오류: "Chat not found"
- Chat ID가 잘못되었습니다
- getUpdates로 다시 확인
- 봇에게 먼저 메시지를 보냈는지 확인

### 오류: "Bad Request: can't parse entities"
- MarkdownV2 문법 오류
- 특수문자 이스케이프 확인

---

## 다음 단계

1. ✅ 봇 토큰 발급
2. ✅ Chat ID 확인
3. ✅ .env 설정
4. ⏳ 메시지 포맷터 구현
5. ⏳ 뉴스 전송 테스트

**준비 완료 후:** `test_telegram.py` 실행

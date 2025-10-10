# Phase 5: 텔레그램 봇 연동

> 목표: 분석된 뉴스를 텔레그램 메시지로 전송하는 시스템 구축

---

## Step 5.1: 텔레그램 봇 설정 ⏳

**목표:**
- 텔레그램 봇 생성 및 API 토큰 발급
- python-telegram-bot 라이브러리 설치

### 1. 텔레그램 봇 생성

1. 텔레그램에서 `@BotFather` 검색
2. `/newbot` 명령어 입력
3. 봇 이름 설정 (예: `Spread Insight Bot`)
4. 봇 사용자명 설정 (예: `spread_insight_bot`)
5. API 토큰 받기 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. 환경 변수 설정

`.env` 파일에 추가:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**Chat ID 확인 방법:**
1. 봇에게 아무 메시지 보내기
2. `https://api.telegram.org/bot<TOKEN>/getUpdates` 접속
3. `chat.id` 값 확인

### 3. 라이브러리 설치

```bash
pip install python-telegram-bot==21.0
```

---

## Step 5.2: 메시지 포맷터 구현 ⏳

**목표:**
- HTML 콘텐츠를 텔레그램 MarkdownV2 형식으로 변환
- 텔레그램 메시지 길이 제한 처리 (4096자)

**파일:** `publishers/telegram_formatter.py`

### 텔레그램 포맷 특징

1. **MarkdownV2 문법:**
   - 굵게: `*bold*`
   - 기울임: `_italic_`
   - 코드: `` `code` ``
   - 링크: `[text](url)`

2. **특수 문자 이스케이프:**
   - `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!`

3. **메시지 길이 제한:**
   - 최대 4096자
   - 긴 콘텐츠는 여러 메시지로 분할

### 7섹션 포맷 예시

```markdown
*📰 빵순이 울리는 빵플레이션*

🏷️ #빵플레이션 #베이글가격 #소금빵

━━━━━━━━━━━━━━━━━━━━

*❓ 무슨 일이?*

📌 *3줄 요약*
최근 3년간 베이글 가격이 44% 급등...

💡 *쉽게 말하면?*
빵값이 급격히 올라서...

━━━━━━━━━━━━━━━━━━━━

*📚 오늘의 용어*

*소비자물가지수 (Tier 1)*
카테고리: 물가

[용어] 알아두면 좋은 용어
소비자가 구매하는...

━━━━━━━━━━━━━━━━━━━━

*🔗 더 알아보기*
[원문 보기](https://...)
```

---

## Step 5.3: 텔레그램 발행자 구현 ⏳

**파일:** `publishers/telegram_publisher.py`

**클래스 설계:**
```python
class TelegramPublisher:
    def __init__(self, bot_token: str, chat_id: str):
        """텔레그램 봇 초기화"""

    async def send_article(self, article_data: dict):
        """기사 전체 전송"""
        # 1. 포맷팅
        # 2. 길이 체크
        # 3. 분할 전송 (필요시)

    async def send_message(self, text: str, parse_mode='MarkdownV2'):
        """단일 메시지 전송"""

    def _split_message(self, text: str, max_length=4000) -> list[str]:
        """긴 메시지 분할"""
```

---

## Step 5.4: 통합 테스트 ⏳

**테스트 파일:** `test_telegram.py`

**테스트 시나리오:**
1. 봇 연결 테스트
2. 간단한 메시지 전송
3. 전체 기사 전송
4. 긴 콘텐츠 분할 전송

**테스트 체크리스트:**
- [ ] 봇 토큰 정상 작동
- [ ] Chat ID 정확
- [ ] MarkdownV2 파싱 성공
- [ ] 한글 인코딩 정상
- [ ] 링크 클릭 가능
- [ ] 이모지 정상 표시

---

## Step 5.5: 자동 발송 스케줄링 (선택) ⏳

**목표:**
- 매일 정해진 시간에 자동 발송
- APScheduler 활용

**파일:** `main.py`

**스케줄 예시:**
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 매일 오전 9시 발송
scheduler.add_job(
    daily_news_job,
    trigger='cron',
    hour=9,
    minute=0
)

scheduler.start()
```

**필요 라이브러리:**
```
apscheduler==3.10.4
```

---

## 완료 기준

- [ ] 텔레그램 봇 생성 및 토큰 발급
- [ ] python-telegram-bot 설치
- [ ] TelegramFormatter 구현
- [ ] TelegramPublisher 구현
- [ ] 실제 기사 전송 테스트 성공
- [ ] 메시지 포맷 정상 (MarkdownV2)
- [ ] 긴 메시지 분할 처리

---

## 현재 상태

- **Phase 1:** ✅ 완료
- **Phase 2:** ✅ 완료
- **Phase 3:** ⏭️ 건너뜀
- **Phase 4:** ✅ 완료
- **Phase 5:** 🔜 시작 예정

---

## 다음 단계

Phase 6: 쿠팡 파트너스 연동
- 관련 도서/제품 추천
- 파트너스 링크 생성
- 수익 추적

Phase 7: 전체 통합 및 자동화
- 엔드투엔드 파이프라인
- 일일 자동 실행
- 로그 및 모니터링
- GitHub Actions 배포

---

## 참고 자료

- [python-telegram-bot 공식 문서](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [MarkdownV2 문법](https://core.telegram.org/bots/api#markdownv2-style)

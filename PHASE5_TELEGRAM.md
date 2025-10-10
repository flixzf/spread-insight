# Phase 5: 텔레그램 봇 연동 (Week 4)

> python-telegram-bot을 사용한 뉴스 배포

---

## ✅ Step 5.1: 텔레그램 봇 생성 및 메시지 전송
**목표:** 텔레그램 봇으로 "Hello World" 메시지 전송
**소요 시간:** 1시간

### 📝 체크리스트
- [ ] 텔레그램 봇 생성 (BotFather)
- [ ] 봇 토큰 및 Chat ID 획득
- [ ] python-telegram-bot 설치
- [ ] 테스트 메시지 전송

### 🛠️ 실행 순서

**1. 텔레그램 봇 생성**

1. 텔레그램 앱 설치 (스마트폰 또는 PC)
2. 텔레그램에서 `@BotFather` 검색
3. 대화 시작 후 다음 명령어 입력:
   ```
   /newbot
   ```
4. 봇 이름 입력 (예: `Spread Insight Bot`)
5. 봇 사용자명 입력 (예: `spread_insight_bot`)
   - 반드시 `bot`으로 끝나야 함
6. 봇 토큰 복사 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**2. Chat ID 획득**

1. 생성한 봇과 대화 시작
2. 아무 메시지 전송 (예: `/start`)
3. 브라우저에서 다음 URL 접속:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   `<YOUR_BOT_TOKEN>` 부분을 실제 토큰으로 교체
4. JSON 응답에서 `"chat":{"id":123456789}` 부분 찾기
5. Chat ID 복사 (예: `123456789`)

**3. .env 파일 업데이트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\.env`
```
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# 텔레그램 (여기에 입력)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# 쿠팡 파트너스
COUPANG_ACCESS_KEY=
COUPANG_SECRET_KEY=
COUPANG_PARTNER_ID=
```

**4. requirements.txt 업데이트**
```
# ... 기존 라이브러리들 ...
jinja2==3.1.3

# 텔레그램 봇 추가
python-telegram-bot==20.8
```

설치:
```bash
pip install python-telegram-bot==20.8
```

**5. 텔레그램 Publisher 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\publishers\telegram_bot.py`
```python
from telegram import Bot
from telegram.error import TelegramError
from utils.config import Config
import asyncio


class TelegramPublisher:
    """텔레그램 봇을 통한 뉴스 배포"""

    def __init__(self):
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN이 .env 파일에 설정되지 않았습니다.")

        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.default_chat_id = Config.TELEGRAM_CHAT_ID

    async def send_message(self, chat_id: str, text: str) -> bool:
        """단순 텍스트 메시지 전송"""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            print(f"  ✅ 메시지 전송 완료 (Chat ID: {chat_id})")
            return True

        except TelegramError as e:
            print(f"  ❌ 메시지 전송 실패: {e}")
            return False

    async def test_connection(self) -> bool:
        """봇 연결 테스트"""
        try:
            me = await self.bot.get_me()
            print(f"  ✅ 봇 연결 성공: @{me.username}")
            return True
        except Exception as e:
            print(f"  ❌ 봇 연결 실패: {e}")
            return False
```

**6. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_telegram.py`
```python
from publishers.telegram_bot import TelegramPublisher
from utils.config import Config
import asyncio


async def main():
    print("=" * 60)
    print("텔레그램 봇 테스트")
    print("=" * 60)

    # 초기화
    try:
        bot = TelegramPublisher()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n.env 파일에 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 설정하세요.")
        return

    # 1. 연결 테스트
    print("\n1단계: 봇 연결 테스트")
    print("-" * 60)

    if not await bot.test_connection():
        print("❌ 봇 연결 실패. 토큰을 확인하세요.")
        return

    # 2. 메시지 전송
    print("\n2단계: 테스트 메시지 전송")
    print("-" * 60)

    test_message = """
🎉 Spread Insight 봇 테스트

안녕하세요! 텔레그램 봇이 정상적으로 작동하고 있습니다.

📰 경제 뉴스를 쉽게 이해할 수 있도록 도와드리겠습니다.
    """.strip()

    success = await bot.send_message(
        chat_id=Config.TELEGRAM_CHAT_ID,
        text=test_message
    )

    if success:
        print("\n✅ 텔레그램 앱에서 메시지를 확인하세요!")
    else:
        print("\n❌ 메시지 전송 실패. Chat ID를 확인하세요.")


if __name__ == '__main__':
    asyncio.run(main())
```

**7. 실행**
```bash
python test_telegram.py
```

### ✅ 성공 기준
- [ ] 봇 연결 성공 메시지
- [ ] 텔레그램 앱에 메시지 도착
- [ ] 한글 정상 표시

### ⚠️ 예상 오류 및 해결

**오류 1:** `TELEGRAM_BOT_TOKEN이 .env 파일에 설정되지 않았습니다`
- **해결:** `.env` 파일 열어서 토큰 입력 확인

**오류 2:** `Unauthorized`
- **원인:** 봇 토큰이 잘못됨
- **해결:** BotFather에서 토큰 다시 확인

**오류 3:** `Chat not found`
- **원인:** Chat ID가 잘못됨
- **해결:** `/getUpdates` API로 Chat ID 재확인

---

## ✅ Step 5.2: 버튼 UI 추가
**목표:** 메시지에 인라인 버튼 추가 (상세 보기, 상품 보기)
**소요 시간:** 1시간

### 🛠️ 실행 순서

**1. telegram_bot.py 업데이트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\publishers\telegram_bot.py`

기존 파일에 다음 메서드 추가:
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ... (기존 코드) ...

async def send_news(
    self,
    chat_id: str,
    title: str,
    summary: str,
    detail_url: str,
    coupang_url: str = None
) -> bool:
    """뉴스 메시지 (버튼 포함) 전송"""
    try:
        # 메시지 본문 (HTML 형식)
        message = f"<b>📰 {title}</b>\n\n{summary}"

        # 버튼 생성
        buttons = [
            [InlineKeyboardButton("📄 상세 인사이트 보기", url=detail_url)]
        ]

        if coupang_url:
            buttons.append(
                [InlineKeyboardButton("🛒 관련 상품 보기", url=coupang_url)]
            )

        reply_markup = InlineKeyboardMarkup(buttons)

        # 메시지 전송
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup,
            disable_web_page_preview=True  # 링크 미리보기 비활성화
        )

        print(f"  ✅ 뉴스 전송 완료: {title[:30]}")
        return True

    except TelegramError as e:
        print(f"  ❌ 뉴스 전송 실패: {e}")
        return False

async def broadcast_news(
    self,
    chat_ids: list[str],
    title: str,
    summary: str,
    detail_url: str,
    coupang_url: str = None,
    delay: float = 0.5
) -> dict:
    """여러 사용자에게 뉴스 전송"""
    results = {'success': 0, 'fail': 0}

    for i, chat_id in enumerate(chat_ids, 1):
        print(f"  [{i}/{len(chat_ids)}] Chat ID: {chat_id}")

        success = await self.send_news(
            chat_id=chat_id,
            title=title,
            summary=summary,
            detail_url=detail_url,
            coupang_url=coupang_url
        )

        if success:
            results['success'] += 1
        else:
            results['fail'] += 1

        # 스팸 방지 딜레이
        if i < len(chat_ids):
            await asyncio.sleep(delay)

    print(f"\n  전송 완료: 성공 {results['success']}개 / 실패 {results['fail']}개")
    return results
```

**2. 버튼 테스트 스크립트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_telegram_buttons.py`
```python
from publishers.telegram_bot import TelegramPublisher
from utils.config import Config
import asyncio


async def main():
    print("=" * 60)
    print("텔레그램 버튼 UI 테스트")
    print("=" * 60)

    bot = TelegramPublisher()

    # 버튼 연결 테스트
    if not await bot.test_connection():
        print("❌ 봇 연결 실패")
        return

    # 뉴스 메시지 전송 (버튼 포함)
    print("\n뉴스 메시지 전송 중...")
    print("-" * 60)

    await bot.send_news(
        chat_id=Config.TELEGRAM_CHAT_ID,
        title="환율 급등, 달러당 1,400원 돌파",
        summary="최근 미국 금리 인상으로 원/달러 환율이 1,400원을 넘어섰습니다. 전문가들은 당분간 고환율이 지속될 것으로 전망하고 있습니다.",
        detail_url="https://example.com/news/20250110_exchange_rate.html",
        coupang_url="https://www.coupang.com/np/search?q=환전"
    )

    print("\n✅ 텔레그램 앱에서 버튼을 확인하세요!")


if __name__ == '__main__':
    asyncio.run(main())
```

**3. 실행**
```bash
python test_telegram_buttons.py
```

### ✅ 성공 기준
- [ ] 메시지에 2개 버튼 표시
- [ ] "상세 인사이트 보기" 버튼 클릭 시 URL 이동
- [ ] "관련 상품 보기" 버튼 클릭 시 쿠팡 페이지 이동

---

## ✅ Step 5.3: 구독자 관리
**목표:** 여러 사용자에게 일괄 전송
**소요 시간:** 1시간

### 🛠️ 실행 순서

**1. 구독자 매니저 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\database\subscriber_manager.py`
```python
import sqlite3
from typing import List
import os


class SubscriberManager:
    """텔레그램 구독자 관리"""

    def __init__(self, db_path: str = './database/news.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def _create_table(self):
        """구독자 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id TEXT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                subscribed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                active INTEGER DEFAULT 1
            )
        ''')

        conn.commit()
        conn.close()

    def add_subscriber(
        self,
        chat_id: str,
        username: str = None,
        first_name: str = None
    ) -> bool:
        """구독자 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO subscribers (chat_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (chat_id, username, first_name))

            conn.commit()
            print(f"  ✅ 구독자 추가: {chat_id}")
            return True

        except Exception as e:
            print(f"  ❌ 구독자 추가 실패: {e}")
            return False
        finally:
            conn.close()

    def remove_subscriber(self, chat_id: str) -> bool:
        """구독자 제거 (비활성화)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE subscribers
                SET active = 0
                WHERE chat_id = ?
            ''', (chat_id,))

            conn.commit()
            print(f"  ✅ 구독자 제거: {chat_id}")
            return True

        except Exception as e:
            print(f"  ❌ 구독자 제거 실패: {e}")
            return False
        finally:
            conn.close()

    def get_active_subscribers(self) -> List[str]:
        """활성 구독자 목록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT chat_id FROM subscribers WHERE active = 1')
        rows = cursor.fetchall()
        conn.close()

        return [row[0] for row in rows]

    def get_total_count(self) -> int:
        """전체 구독자 수"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM subscribers WHERE active = 1')
        count = cursor.fetchone()[0]
        conn.close()

        return count
```

**2. 구독자 관리 테스트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_subscribers.py`
```python
from database.subscriber_manager import SubscriberManager
from publishers.telegram_bot import TelegramPublisher
from utils.config import Config
import asyncio


async def main():
    print("=" * 60)
    print("구독자 관리 테스트")
    print("=" * 60)

    # 초기화
    sub_manager = SubscriberManager()
    bot = TelegramPublisher()

    # 1. 구독자 추가
    print("\n1단계: 구독자 추가")
    print("-" * 60)

    # 본인을 구독자로 추가
    sub_manager.add_subscriber(
        chat_id=Config.TELEGRAM_CHAT_ID,
        username="test_user",
        first_name="테스트"
    )

    # 테스트용 더미 구독자 (실제로는 전송 안 함)
    # sub_manager.add_subscriber(chat_id="999999999", username="dummy")

    total = sub_manager.get_total_count()
    print(f"\n총 구독자 수: {total}명")

    # 2. 구독자 목록 조회
    print("\n2단계: 구독자 목록")
    print("-" * 60)

    subscribers = sub_manager.get_active_subscribers()
    for i, chat_id in enumerate(subscribers, 1):
        print(f"  {i}. Chat ID: {chat_id}")

    # 3. 일괄 전송
    print("\n3단계: 일괄 전송")
    print("-" * 60)

    results = await bot.broadcast_news(
        chat_ids=subscribers,
        title="[테스트] 구독자 일괄 전송",
        summary="이것은 일괄 전송 테스트 메시지입니다.",
        detail_url="https://example.com/test",
        coupang_url="https://www.coupang.com"
    )

    print(f"\n✅ 일괄 전송 완료")
    print(f"   성공: {results['success']}명")
    print(f"   실패: {results['fail']}명")


if __name__ == '__main__':
    asyncio.run(main())
```

**3. 실행**
```bash
python test_subscribers.py
```

### ✅ 성공 기준
- [ ] 구독자 DB 저장
- [ ] 활성 구독자 목록 조회
- [ ] 여러 구독자에게 동시 전송
- [ ] 전송 성공/실패 카운트

### ⚠️ 예상 오류 및 해결

**오류 1:** `table subscribers already exists`
- **원인:** 테이블이 이미 존재
- **해결:** `CREATE TABLE IF NOT EXISTS` 사용 (이미 코드에 포함)

**오류 2:** 전송 속도 제한 (429 Too Many Requests)
- **원인:** 텔레그램 API 제한 (초당 30개)
- **해결:** `delay` 파라미터 증가 (0.5초 → 1초)

---

## 🎉 Phase 5 완료!

다음 단계: [Phase 6: 쿠팡 파트너스](PHASE6_COUPANG.md)

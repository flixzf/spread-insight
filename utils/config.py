"""
프로젝트 설정 관리
.env 파일에서 환경 변수 로드 및 검증
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """프로젝트 전역 설정"""

    # ===== Gemini API =====
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-lite')  # 기본값

    # ===== OpenAI API (DALL-E) =====
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # ===== Adobe Firefly API =====
    ADOBE_CLIENT_ID = os.getenv('ADOBE_CLIENT_ID')
    ADOBE_CLIENT_SECRET = os.getenv('ADOBE_CLIENT_SECRET')
    ADOBE_ORG_ID = os.getenv('ADOBE_ORG_ID')

    # ===== 텔레그램 =====
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    # ===== 쿠팡 파트너스 =====
    COUPANG_ACCESS_KEY = os.getenv('COUPANG_ACCESS_KEY')
    COUPANG_SECRET_KEY = os.getenv('COUPANG_SECRET_KEY')
    COUPANG_PARTNER_ID = os.getenv('COUPANG_PARTNER_ID')

    # ===== 스크래핑 설정 =====
    MAX_ARTICLES_PER_SITE = int(os.getenv('MAX_ARTICLES_PER_SITE', '10'))
    SCRAPING_DELAY = float(os.getenv('SCRAPING_DELAY', '0.3'))  # 초

    # ===== 데이터 경로 =====
    DATA_DIR = './data'
    RAW_DIR = './data/raw'
    PROCESSED_DIR = './data/processed'
    CHARTS_DIR = './data/charts'
    HTML_DIR = './data/html'
    LOGS_DIR = './logs'

    # ===== AI 설정 =====
    SUMMARY_SENTENCES = int(os.getenv('SUMMARY_SENTENCES', '3'))  # 요약 문장 수
    MAX_TERMS_TO_EXPLAIN = int(os.getenv('MAX_TERMS_TO_EXPLAIN', '1'))  # 설명할 용어 수

    @classmethod
    def validate_gemini(cls) -> bool:
        """Gemini API 설정 검증"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.\n"
                "https://makersuite.google.com/app/apikey 에서 API 키를 발급받으세요."
            )
        return True

    @classmethod
    def validate_telegram(cls) -> bool:
        """텔레그램 설정 검증"""
        if not cls.TELEGRAM_BOT_TOKEN or not cls.TELEGRAM_CHAT_ID:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 .env 파일에 설정되지 않았습니다."
            )
        return True

    @classmethod
    def validate_coupang(cls) -> bool:
        """쿠팡 파트너스 설정 검증"""
        if not all([cls.COUPANG_ACCESS_KEY, cls.COUPANG_SECRET_KEY, cls.COUPANG_PARTNER_ID]):
            raise ValueError(
                "쿠팡 파트너스 설정(ACCESS_KEY, SECRET_KEY, PARTNER_ID)이 완전하지 않습니다."
            )
        return True

    @classmethod
    def validate_all(cls):
        """모든 필수 설정 검증"""
        cls.validate_gemini()
        cls.validate_telegram()
        cls.validate_coupang()

    @classmethod
    def print_config(cls):
        """현재 설정 출력 (디버깅용)"""
        print("=" * 60)
        print("Spread Insight - 현재 설정")
        print("=" * 60)
        print(f"Gemini Model: {cls.GEMINI_MODEL}")
        print(f"Gemini API Key: {'설정됨' if cls.GEMINI_API_KEY else '미설정'}")
        print(f"Telegram Bot Token: {'설정됨' if cls.TELEGRAM_BOT_TOKEN else '미설정'}")
        print(f"Telegram Chat ID: {'설정됨' if cls.TELEGRAM_CHAT_ID else '미설정'}")
        print(f"Coupang Partner ID: {'설정됨' if cls.COUPANG_PARTNER_ID else '미설정'}")
        print(f"\n최대 수집 기사 수: {cls.MAX_ARTICLES_PER_SITE}")
        print(f"스크래핑 지연 시간: {cls.SCRAPING_DELAY}초")
        print(f"요약 문장 수: {cls.SUMMARY_SENTENCES}")
        print(f"설명할 용어 수: {cls.MAX_TERMS_TO_EXPLAIN}")
        print("=" * 60)


if __name__ == '__main__':
    # 설정 테스트
    Config.print_config()

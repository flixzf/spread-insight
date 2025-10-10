"""
Gemini API를 사용한 뉴스 분석
요약, 쉬운 설명, 인사이트 생성
"""

import google.generativeai as genai
from utils.config import Config
from models.news_article import NewsArticle


class GeminiAnalyzer:
    """Gemini API 래퍼"""

    def __init__(self):
        """Gemini API 초기화"""
        # API 키 검증
        Config.validate_gemini()

        # Gemini 설정
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # 안전 설정 (뉴스 분석이므로 관대하게)
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]

    def summarize(self, article: NewsArticle, num_sentences: int = 3) -> str:
        """
        기사를 지정된 문장 수로 요약

        Args:
            article: 뉴스 기사 객체
            num_sentences: 요약 문장 수 (기본 3)

        Returns:
            요약문
        """
        prompt = f"""
다음 뉴스 기사를 정확히 {num_sentences}문장으로 요약해주세요.
핵심 내용만 간결하게 담아주세요.

제목: {article.title}

본문:
{article.content}

요약 ({num_sentences}문장):
        """.strip()

        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            summary = response.text.strip()
            return summary

        except Exception as e:
            raise Exception(f"요약 생성 실패: {e}")

    def explain_simple(self, article: NewsArticle) -> str:
        """
        기사를 핵심 3줄 Q&A 형식으로 인사이트 있게 설명

        Args:
            article: 뉴스 기사 객체

        Returns:
            Q&A 형식 핵심 3줄 설명
        """
        prompt = f"""
당신은 경제 뉴스를 투자 인사이트로 변환하는 전문 애널리스트입니다.
독자가 10초 안에 핵심을 이해하고, "아 그래서 이게 중요하구나", "내 투자에 이렇게 적용하면 되겠네"를 느끼도록 작성하세요.

**출력 형식**: 정확히 아래 3개 질문에 대한 답변만 작성하세요.

Q. 무슨 일이야?
A. [2-3문장으로 핵심 요약 + 왜 중요한지]
   - 첫 문장: 한 마디로 무슨 일인지 (중학생도 이해 가능하게)
   - 둘째 문장: 구체적 숫자/규모 (예: "코스피 1.73% 급등", "외국인 1조원 매수")
   - 셋째 문장: 왜 이 뉴스가 중요한지 (시장 의미, 시그널)

Q. 내 투자엔 어떤 영향?
A. [3-4문장으로 실전 투자 전략 + 과거 사례 비교]
   - 첫 문장: 수혜 종목/섹터 (구체적 종목명, 예: "삼성전자, SK하이닉스 같은 반도체주")
   - 둘째 문장: 타격 종목/섹터 (반대 케이스, 예: "배터리, 전기차 관련주는 소외")
   - 셋째 문장: 과거 비슷한 상황 때 어땠는지 (연도 + 구체적 수치, 예: "2020년 AI 붐 때 반도체주 30% 급등")
   - 넷째 문장: 환율/금리/원자재 등 연관 자산 영향 (있다면)

Q. 뭘 주목해야 해?
A. [2-3문장으로 앞으로의 경제 흐름 + 관련주 등락 포인트]
   - 첫 문장: 다음 주목 이벤트/지표 (예: "다음 주 미국 CPI 발표", "삼성전자 실적 발표")
   - 둘째 문장: 기관/외국인 투자자들의 시각 (예: "외국인은 반도체 쏠림 지속 전망")
   - 셋째 문장: 관련주 등락 시나리오 (예: "상승 지속 시 장비주도 동반 상승, 조정 시 5% 하락 가능")
   - 알아두면 폼 나는 인사이트 하나 (있다면 자연스럽게 포함)

**작성 원칙:**
1. 구체적 숫자 필수 (%, 금액, 비율 등)
2. 고유명사 명확히 (기업명, 지수명, 지표명)
3. 과거 사례는 연도 + 구체적 수치와 함께
4. "예상", "전망" 등 추측 표현은 근거와 함께
5. 문장 끝은 명사형 종결어미 ("~한 상황", "~인 셈", "~로 분석", "~될 전망")
6. 전문 용어는 괄호로 쉽게 풀어쓰기 (예: "KOSPI(한국종합주가지수)")
7. 각 답변은 간결하지만 인사이트 풍부하게

제목: {article.title}

본문:
{article.content[:1500]}

핵심 3줄:
        """.strip()

        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            explanation = response.text.strip()
            return explanation

        except Exception as e:
            raise Exception(f"쉬운 설명 생성 실패: {e}")

    def extract_keywords(self, article: NewsArticle, max_keywords: int = 5) -> list[str]:
        """
        기사에서 핵심 키워드 추출 (보편적 카테고리)

        Args:
            article: 뉴스 기사 객체
            max_keywords: 최대 키워드 수

        Returns:
            키워드 리스트
        """
        prompt = f"""
다음 뉴스 기사에서 핵심 키워드를 {max_keywords}개 추출해주세요.

**중요**: 키워드는 보편적인 카테고리로 작성하세요. 고유명사보다는 일반 명사를 사용하세요.

예시:
- ❌ "최창걸 명예회장", "고려아연" (너무 specific)
- ✅ "기업", "경영", "비철금속산업" (보편적 카테고리)

- ❌ "연준 의장", "제롬 파월" (너무 specific)
- ✅ "금리", "통화정책", "미국경제" (보편적 카테고리)

뉴스를 모아볼 수 있는 태그로 사용될 키워드를 추출하세요.

제목: {article.title}

본문:
{article.content[:1000]}

답변 형식 (쉼표로 구분):
키워드1, 키워드2, 키워드3, ...
        """.strip()

        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            keywords_text = response.text.strip()

            # 쉼표로 분리하여 리스트로 변환
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            return keywords[:max_keywords]

        except Exception as e:
            raise Exception(f"키워드 추출 실패: {e}")

    def test_connection(self) -> bool:
        """
        API 연결 테스트

        Returns:
            연결 성공 여부
        """
        try:
            response = self.model.generate_content(
                "안녕하세요. 테스트 메시지입니다. '성공'이라고 답해주세요.",
                safety_settings=self.safety_settings
            )
            return '성공' in response.text

        except Exception as e:
            print(f"[ERROR] API 연결 실패: {e}")
            return False


if __name__ == '__main__':
    # 간단한 테스트
    print("Gemini API 연결 테스트...")

    try:
        analyzer = GeminiAnalyzer()

        if analyzer.test_connection():
            print("[OK] API 연결 성공!")
        else:
            print("[ERROR] API 연결 실패!")

    except Exception as e:
        print(f"[ERROR] {e}")

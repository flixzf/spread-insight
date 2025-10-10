# -*- coding: utf-8 -*-
import re
import os
from typing import Dict, List
import google.generativeai as genai


class CoupangPartners:
    """
    Coupang Partners 제휴 활동 관리 (AI 기반)

    ⚠️ 중요 준수사항 (partners-guide.pdf 참고):

    1. 제휴 링크 생성 방법:
       - 반드시 쿠팡 파트너스 시스템(https://partners.coupang.com)에서 생성해야 함
       - 현재는 단일 파트너스 링크 사용, API 승인 후 동적 생성 예정

    2. 대가성 문구 (필수):
       - 모든 제휴 링크 사용 시 공정거래위원회 가이드라인에 따른 대가성 문구 필수

    3. 추천 프로세스:
       - 뉴스 내용 분석 → Gemini로 관련 상품/카테고리 선정
       - Gemini로 후킹 가능한 강렬한 한줄 타이틀 생성
       - 파트너스 링크 + 준수사항 포함

    사용 방법:
        partners = CoupangPartners(api_key=GEMINI_API_KEY)
        recommendations = partners.generate_recommendations(article_data, max_items=3)
    """

    # 공정거래위원회 권장 대가성 문구
    DEFAULT_DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."

    # 파트너스 승인 전 사용할 기본 제휴 링크
    # TODO: API 승인 후 상품별 동적 링크 생성으로 변경
    DEFAULT_PARTNER_LINK = "https://link.coupang.com/a/cVz6PI"

    def __init__(self, api_key: str = None, disclosure_text: str = None, partner_link: str = None):
        """
        Args:
            api_key: Gemini API 키 (선택사항, 환경변수에서 자동 로드)
            disclosure_text: 사용자 정의 대가성 문구 (선택사항, 기본값 사용 권장)
            partner_link: 사용할 파트너스 링크 (선택사항, 기본값 사용)
        """
        self.disclosure_text = disclosure_text or self.DEFAULT_DISCLOSURE
        self.partner_link = partner_link or self.DEFAULT_PARTNER_LINK

        # Gemini API 설정
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        else:
            self.model = None
            print("[WARNING] Gemini API key not found. AI features disabled.")

    def analyze_and_recommend(self, article_data: dict, max_items: int = 3) -> List[Dict]:
        """
        뉴스 내용을 분석하여 쿠팡 파트너스 추천 생성 (AI 기반)

        Args:
            article_data: 뉴스 기사 데이터 (title, content, keywords 등)
            max_items: 최대 추천 개수

        Returns:
            추천 목록 [{'category': '카테고리', 'hook_title': '후킹 타이틀', 'affiliate_link': '링크'}]
        """
        if not self.model:
            print("[ERROR] Gemini API not configured. Cannot generate recommendations.")
            return []

        title = article_data.get('title', '')
        content = article_data.get('content', '')
        keywords = article_data.get('keywords', [])

        prompt = f"""
당신은 쿠팡 파트너스 마케팅 전문가입니다.
다음 뉴스 기사를 읽은 독자가 관심 가질 만한 쿠팡 상품을 {max_items}개 추천하고, 각각에 대해 클릭을 유도하는 강렬한 한 줄 타이틀을 작성해주세요.

**뉴스 제목**: {title}
**키워드**: {', '.join(keywords) if keywords else '없음'}
**본문 일부**: {content[:500]}...

**요구사항**:
1. 뉴스 내용과 직접 관련된 상품/카테고리 선정
   - 예: 베이글 가격 뉴스 → 베이글, 빵, 식품 관련
   - 예: 경제 정책 뉴스 → 경제 서적, 재테크 책
2. 각 상품에 대해 클릭을 유도하는 강렬하고 짧은 한 줄 타이틀 (15자 이내)
3. 실용적이고 구매 가능성이 높은 상품

**출력 형식** (JSON):
```json
[
  {{
    "category": "베이글",
    "hook_title": "지금 베이글 특가!"
  }},
  {{
    "category": "경제 도서",
    "hook_title": "경제 공부 필독서"
  }}
]
```

JSON만 출력하세요. 다른 설명은 넣지 마세요.
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # JSON 추출 (```json 태그 제거)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()

            import json
            recommendations = json.loads(result_text)

            # affiliate_link 추가
            for rec in recommendations:
                rec['affiliate_link'] = self.partner_link

            return recommendations[:max_items]

        except Exception as e:
            print(f"[ERROR] Failed to generate recommendations: {e}")
            return []

    def get_disclosure_text(self) -> str:
        """대가성 문구 반환"""
        return self.disclosure_text

    def get_disclosure_html(self, css_class: str = "coupang-disclaimer") -> str:
        """
        대가성 문구를 포함한 HTML 반환

        Args:
            css_class: CSS 클래스명 (기본값: "coupang-disclaimer")

        Returns:
            대가성 문구가 포함된 HTML 문자열
        """
        return f'<p class="{css_class}">{self.disclosure_text}</p>'

    def format_recommendation_html(self, recommendation: Dict) -> str:
        """
        추천 항목을 HTML로 포맷팅

        Args:
            recommendation: {'category': '', 'hook_title': '', 'affiliate_link': ''}

        Returns:
            HTML 문자열
        """
        category = recommendation.get('category', '추천 상품')
        hook_title = recommendation.get('hook_title', '확인하기')
        link = recommendation.get('affiliate_link', self.partner_link)

        html = f'''
<div class="coupang-recommendation">
    <p class="category">{category}</p>
    <a href="{link}" target="_blank" rel="noopener noreferrer">
        <strong>{hook_title}</strong> →
    </a>
</div>
        '''.strip()

        return html

    # === 레거시 메서드 (하위 호환성) ===

    def validate_partner_link(self, url: str) -> bool:
        """쿠팡 파트너스 링크 유효성 검증"""
        if not url:
            return False
        pattern = r'^https://link\.coupang\.com/(a|re)/[a-zA-Z0-9]+.*$'
        return bool(re.match(pattern, url))

    def add_affiliate_links(self, books: list) -> list:
        """
        도서 목록에 파트너스 링크 추가 (레거시)

        Note: 새 코드에서는 analyze_and_recommend() 사용 권장
        """
        result = []
        for book in books:
            book_copy = book.copy()
            book_copy['affiliate_link'] = self.partner_link
            result.append(book_copy)
        return result


if __name__ == '__main__':
    # 테스트
    partners = CoupangPartners()

    # 테스트 기사
    test_article = {
        'title': '베이글 가격 인플레이션, 3개에 44% 올라',
        'content': '최근 베이커리 업계에서 베이글 가격이 급등하면서 소비자들의 부담이 커지고 있다. 원재료 가격 상승과 인건비 인상이 주요 원인으로 지목된다.',
        'keywords': ['베이글', '인플레이션', '물가', '가격인상']
    }

    print("=" * 70)
    print("Coupang Partners AI Recommendation Test")
    print("=" * 70)
    print(f"\n뉴스 제목: {test_article['title']}")
    print(f"키워드: {', '.join(test_article['keywords'])}")

    print("\n" + "=" * 70)
    print("AI 추천 생성 중...")
    print("=" * 70)

    recommendations = partners.analyze_and_recommend(test_article, max_items=3)

    if recommendations:
        print(f"\n[OK] {len(recommendations)}개 추천 생성 완료:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. 카테고리: {rec.get('category', 'N/A')}")
            print(f"   후킹 타이틀: {rec.get('hook_title', 'N/A')}")
            print(f"   제휴 링크: {rec.get('affiliate_link', 'N/A')}\n")

        print("=" * 70)
        print("대가성 문구:")
        print(partners.get_disclosure_text())
        print("=" * 70)
    else:
        print("\n[FAIL] 추천 생성 실패")

# -*- coding: utf-8 -*-
"""
DALL-E 기반 이미지 카드 생성기

뉴스 기사를 시각적인 이미지 카드로 변환
"""

import os
from openai import OpenAI
from typing import List, Dict
from utils.config import Config


class ImageCardGenerator:
    """DALL-E를 사용한 뉴스 이미지 카드 생성"""

    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: OpenAI API 키 (선택사항, 환경변수에서 자동 로드)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in .env file")

        self.client = OpenAI(api_key=self.api_key)

    def generate_main_card(
        self,
        title: str,
        keywords: List[str],
        style: str = "modern economic news card"
    ) -> str:
        """
        메인 카드 생성 (제목 + 키워드)

        Args:
            title: 뉴스 제목
            keywords: 핵심 키워드 리스트
            style: 이미지 스타일

        Returns:
            생성된 이미지 URL
        """
        keyword_text = ", ".join(keywords[:3])  # 상위 3개만

        prompt = f"""
Create a modern, minimalist Korean economic news card with the following elements:

TITLE (in Korean, bold, large font):
{title}

KEYWORDS (in Korean, hashtag style):
#{keyword_text.replace(', ', ' #')}

DESIGN STYLE:
- Clean, professional layout similar to modern fintech apps
- Vibrant gradient background (blue to green or yellow to orange)
- Clear typography with high contrast
- Icon or simple graphic related to the news topic (economy, stocks, trade)
- Modern, Instagram story or LinkedIn post style
- 1024x1024 square format
- Minimal text, maximum visual impact

MOOD: Professional, trustworthy, energetic
        """.strip()

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url

    def generate_content_card(
        self,
        title: str,
        content: str,
        card_number: int = 1,
        total_cards: int = 4
    ) -> str:
        """
        콘텐츠 카드 생성 (서브 카드)

        Args:
            title: 카드 제목 (예: "현재 상황", "투자 영향")
            content: 카드 내용
            card_number: 카드 번호
            total_cards: 전체 카드 수

        Returns:
            생성된 이미지 URL
        """
        # 내용이 너무 길면 요약
        if len(content) > 200:
            content = content[:200] + "..."

        prompt = f"""
Create a Korean economic news content card (slide {card_number}/{total_cards}):

SECTION TITLE (in Korean, medium font):
{title}

CONTENT (in Korean, readable font, 3-4 lines):
{content}

DESIGN STYLE:
- Clean, professional layout like a presentation slide
- Soft gradient background (pastel colors)
- Card number indicator in corner ({card_number}/{total_cards})
- Clear hierarchy: title larger than content
- Modern, minimalist design
- 1024x1024 square format
- Easy to read on mobile

MOOD: Informative, professional, approachable
        """.strip()

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url

    def generate_full_card_set(
        self,
        article_data: dict
    ) -> Dict[str, str]:
        """
        전체 카드 세트 생성

        Args:
            article_data: 분석된 기사 데이터

        Returns:
            카드 타입별 이미지 URL 딕셔너리
        """
        cards = {}

        # 1. 메인 카드
        print("\n[1/5] 메인 카드 생성 중...")
        cards['main'] = self.generate_main_card(
            title=article_data.get('title', ''),
            keywords=article_data.get('keywords', [])
        )

        # 2-5. 콘텐츠 카드들
        content_sections = self._extract_content_sections(article_data)

        for i, (section_title, section_content) in enumerate(content_sections, 1):
            print(f"\n[{i+1}/5] '{section_title}' 카드 생성 중...")
            cards[f'card_{i}'] = self.generate_content_card(
                title=section_title,
                content=section_content,
                card_number=i,
                total_cards=len(content_sections)
            )

        return cards

    def _extract_content_sections(self, article_data: dict) -> List[tuple]:
        """
        기사 데이터에서 카드용 섹션 추출

        Returns:
            [(섹션 제목, 섹션 내용), ...]
        """
        sections = []

        # 투자 분석 파싱
        expert_opinion = article_data.get('expert_opinion', '')

        if expert_opinion:
            # 간단한 파싱: 숫자나 키워드로 섹션 분리
            parts = expert_opinion.split('\n\n')

            # 1. 현재 상황 + 과거 사례 (첫 2개 문단)
            if len(parts) >= 2:
                sections.append(("현재 상황 & 과거 사례", '\n\n'.join(parts[:2])))

            # 2. 투자 영향 분석
            if len(parts) >= 3:
                sections.append(("투자 영향 분석", parts[2] if len(parts) > 2 else ''))

            # 3. 시장 관점
            if len(parts) >= 4:
                sections.append(("시장 관점", parts[3] if len(parts) > 3 else ''))

        # 4. 쿠팡 파트너스 추천
        coupang_recs = article_data.get('coupang_recommendations', [])
        if coupang_recs:
            rec = coupang_recs[0]
            coupang_text = f"{rec.get('title', '')}\n\n{rec.get('partner_link', '')}"
            sections.append(("쿠팡 파트너스 추천", coupang_text))

        return sections

    def download_image(self, url: str, save_path: str) -> str:
        """
        이미지 다운로드

        Args:
            url: 이미지 URL
            save_path: 저장 경로

        Returns:
            저장된 파일 경로
        """
        import requests

        response = requests.get(url)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            f.write(response.content)

        return save_path


if __name__ == '__main__':
    # 테스트
    generator = ImageCardGenerator()

    test_data = {
        'title': '美 고율 관세에 포스코·현대제철 4000억원 폭탄',
        'keywords': ['관세', '철강', '무역', '미국', 'EU'],
        'expert_opinion': '''1. 현재 상황: 우리나라 대표 철강 업체인 포스코와 현대제철이 미국에 수출하는 철강 제품에 대해 관세가 올라, 올해 2분기 영업이익에 타격을 주는 상황입니다.

2. 과거 사례: 과거에도 미국은 자국 산업 보호를 위해 특정 국가의 제품에 대해 관세를 인상한 적이 있습니다.

3. 투자 영향 분석: 포스코와 현대제철 같은 철강 업체 주식은 단기적으로 하락 압력을 받을 수 있습니다.

4. 시장 관점: 시장은 이미 미국 측의 관세 인상을 철강 업계에 부정적인 요인으로 주목하고 있습니다.''',
        'coupang_recommendations': [
            {
                'title': '[철강 공구 세트] 가정용 필수품',
                'partner_link': 'https://link.coupang.com/a/cVz6PI'
            }
        ]
    }

    print("=" * 70)
    print("Image Card Generator Test")
    print("=" * 70)

    cards = generator.generate_full_card_set(test_data)

    print("\n" + "=" * 70)
    print("생성된 카드 URL:")
    print("=" * 70)
    for card_name, url in cards.items():
        print(f"{card_name}: {url}")

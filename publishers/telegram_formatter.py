# -*- coding: utf-8 -*-
from typing import List


class TelegramFormatter:
    """
    텔레그램 메시지 포맷터 (Markdown V2 형식)

    포함 내용:
    1. 제목 + 출처 + 날짜
    2. 요약
    3. 키워드
    4. 전문가 분석
    5. 쿠팡 파트너스 추천 (AI 생성)
    6. 대가성 문구
    7. HTML 링크 (선택)
    """

    def format_title_message(self, article_data: dict) -> str:
        """
        타이틀 메시지 포맷팅 (첫 번째 메시지)

        Returns:
            금일의 뉴스! (날짜)
        """
        date = article_data.get('date', '')
        if date:
            return f"📰 금일의 뉴스! ({date})"
        else:
            return "📰 금일의 뉴스!"

    def format_article(self, article_data: dict, include_html_link: bool = False) -> List[str]:
        """
        기사 데이터를 텔레그램 메시지로 포맷팅 (단순 텍스트 형식)

        Args:
            article_data: 기사 데이터 (모든 분석 결과 포함)
            include_html_link: HTML 링크 포함 여부

        Returns:
            텔레그램 메시지 리스트 (각 메시지는 4096자 이하)
        """
        sections = []

        # 1. 제목
        title = article_data.get('title', '')
        if title:
            sections.append(f"{title}")

        # 2. 요약
        summary = article_data.get('summary', '')
        if summary:
            sections.append(f"\n📌 요약\n{summary}")

        # 3. 키워드
        keywords = article_data.get('keywords', [])
        if keywords:
            keyword_text = ', '.join(f"#{kw}" for kw in keywords)
            sections.append(f"\n🏷️ 키워드\n{keyword_text}")

        # 4. 쉬운 설명
        expert_opinion = article_data.get('expert_opinion', '')
        if not expert_opinion:
            expert_opinion = article_data.get('easy_explanation', '')

        if expert_opinion:
            sections.append(f"\n💡 쉬운 설명\n{expert_opinion}")

        # 5. 쿠팡 파트너스 추천 (1개만)
        coupang_recs = article_data.get('coupang_recommendations', [])
        if coupang_recs:
            sections.append(self._format_coupang_recommendations(coupang_recs[:1]))  # 첫 번째만

        # 6. 대가성 문구
        disclosure = article_data.get('coupang_disclosure', '')
        if disclosure:
            sections.append(f"\n💳 {disclosure}")

        # 메시지를 4096자 제한에 맞춰 분할
        full_text = "\n\n".join(sections)
        return self.split_long_message(full_text, max_length=4000)

    def _format_header(self, article_data: dict) -> str:
        """헤더 포맷팅"""
        title = article_data.get('title', '제목 없음')
        date = article_data.get('date', '')

        header = f"📰 *{title}*"
        if date:
            header += f"\n📅 {date}"

        return header

    def _format_coupang_recommendations(self, recommendations: list) -> str:
        """쿠팡 파트너스 추천 포맷팅 (단순 텍스트, 1개만)"""
        if not recommendations:
            return ""

        rec = recommendations[0]  # 첫 번째만 사용
        category = rec.get('category', '상품')
        hook_title = rec.get('hook_title', '확인하기')
        link = rec.get('affiliate_link', '')

        msg = f"\n🛒 쿠팡 파트너스 추천\n"
        msg += f"{category}: {hook_title}\n"
        if link:
            msg += f"{link}"

        return msg

    def _format_books(self, books: list) -> str:
        """
        도서 추천 포맷팅 (레거시 - 하위 호환성)

        Note: 새 코드에서는 _format_coupang_recommendations 사용
        """
        msg = "📚 *추천 도서*\n\n"

        for i, book in enumerate(books, 1):
            title = book.get('title', '')
            author = book.get('author', '')
            link = book.get('affiliate_link', book.get('coupang_url', ''))

            msg += f"{i}. *{title}*\n"
            if author:
                msg += f"   저자: {author}\n"
            if link:
                msg += f"   🔗 [구매하기]({link})\n"
            msg += "\n"

        return msg.strip()

    def split_long_message(self, text: str, max_length: int = 4000) -> List[str]:
        """
        긴 메시지를 여러 개로 분할

        Args:
            text: 원본 텍스트
            max_length: 메시지당 최대 길이 (기본 4000자)

        Returns:
            분할된 메시지 리스트
        """
        if len(text) <= max_length:
            return [text]

        messages = []
        lines = text.split('\n')
        current_msg = ""

        for line in lines:
            if len(current_msg) + len(line) + 1 > max_length:
                # 현재 메시지가 너무 길면 저장하고 새로 시작
                messages.append(current_msg.strip())
                current_msg = line + "\n"
            else:
                current_msg += line + "\n"

        # 마지막 메시지 추가
        if current_msg.strip():
            messages.append(current_msg.strip())

        return messages

    def escape_markdown_v2(self, text: str) -> str:
        """
        Markdown V2 특수 문자 이스케이프

        Note: 현재는 사용하지 않지만 향후 Markdown V2로 전환 시 필요
        """
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text


if __name__ == '__main__':
    # 테스트
    formatter = TelegramFormatter()

    test_article = {
        'title': '현대중공업 창업자 정주영 현대그룹 명예회장 별세 23주기',
        'source': '파이낸셜',
        'date': '2025년 10월 09일',
        'summary': '정주영 현대그룹 명예회장이 별세한 지 23주기를 맞았습니다. 그는 한국 경제 발전에 큰 기여를 한 전설적인 기업인으로 기억됩니다.',
        'keywords': ['정주영', '현대그룹', '현대중공업', '경영 리더십'],
        'expert_opinion': '정주영 회장님은 우리나라에서 아무것도 없는 상태에서 회사를 세계 1위로 키운 유일한 경영자입니다.',
        'coupang_recommendations': [
            {
                'category': '경영/리더 도서',
                'hook_title': 'CEO 필독! 경영 인사이트',
                'affiliate_link': 'https://link.coupang.com/a/cVz6PI'
            },
            {
                'category': '건강식품',
                'hook_title': '회장님도 건강 챙겨',
                'affiliate_link': 'https://link.coupang.com/a/cVz6PI'
            }
        ],
        'coupang_disclosure': '이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
    }

    messages = formatter.format_article(test_article)

    print("=" * 70)
    print(f"Generated {len(messages)} messages:")
    print("=" * 70)

    for i, msg in enumerate(messages, 1):
        print(f"\n[Message {i}]")
        print("-" * 70)
        print(msg)
        print("-" * 70)
        print(f"Length: {len(msg)} chars")

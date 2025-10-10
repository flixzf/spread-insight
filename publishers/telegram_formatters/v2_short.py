# -*- coding: utf-8 -*-
"""
텔레그램 포맷터 v2 - Short Format (핵심 3줄)

버전: v2.0
상태: Experimental
특징:
  - 타이틀 → 이미지 → 텍스트 순서
  - 마크다운 없음 (순수 텍스트)
  - 핵심 3줄로 압축 (10초 안에 읽힘)
  - 쿠팡 파트너스 1개만
  - 3초 딜레이
"""
from typing import List


class TelegramFormatterV2:
    """
    텔레그램 메시지 포맷터 v2 - 핵심 3줄

    포함 내용:
    1. 타이틀 (금일의 뉴스!)
    2. 이미지 (별도 전송)
    3. 핵심 3줄 요약
    4. 쿠팡 파트너스 추천 (1개)
    5. 대가성 문구
    """

    def format_title_message(self, article_data: dict) -> str:
        """
        타이틀 메시지 포맷팅 (첫 번째 메시지)

        Returns:
            금일의 뉴스! (날짜)
        """
        date = article_data.get('date', '')
        if date:
            return f"금일의 뉴스! ({date})"
        else:
            return "금일의 뉴스!"

    def format_article(self, article_data: dict, include_html_link: bool = False) -> List[str]:
        """
        기사 데이터를 텔레그램 메시지로 포맷팅 (핵심 3줄 형식)

        Args:
            article_data: 기사 데이터 (모든 분석 결과 포함)
            include_html_link: HTML 링크 포함 여부

        Returns:
            텔레그램 메시지 리스트
        """
        sections = []

        # 1. 제목
        title = article_data.get('title', '')
        if title:
            sections.append(f"{title}")

        # 2. 핵심 3줄
        three_lines = self._extract_three_key_lines(article_data)
        if three_lines:
            sections.append(f"\n[핵심 3줄]\n\n{three_lines}")

        # 3. 쿠팡 파트너스 추천 (1개만)
        coupang_recs = article_data.get('coupang_recommendations', [])
        if coupang_recs:
            sections.append(self._format_coupang_recommendations(coupang_recs[:1]))

        # 4. 대가성 문구
        disclosure = article_data.get('coupang_disclosure', '')
        if disclosure:
            sections.append(f"\n{disclosure}")

        # 메시지를 4096자 제한에 맞춰 분할
        full_text = "\n\n".join(sections)
        return self.split_long_message(full_text, max_length=4000)

    def _extract_three_key_lines(self, article_data: dict) -> str:
        """
        Gemini가 이미 Q&A 형식으로 생성한 핵심 3줄을 그대로 반환

        Gemini 프롬프트가 직접 다음 형식으로 출력:
        Q. 무슨 일이야?
        A. ...

        Q. 내 투자엔 어떤 영향?
        A. ... + 과거 사례

        Q. 뭘 주목해야 해?
        A. ... (경제 흐름, 관련주 등락)
        """
        # Gemini가 생성한 easy_explanation을 그대로 사용
        explanation = article_data.get('easy_explanation', '') or article_data.get('expert_opinion', '')

        if not explanation:
            # 설명이 없으면 기본 포맷 반환
            summary = article_data.get('summary', '')
            return (
                f"Q. 무슨 일이야?\n"
                f"A. {summary}\n\n"
                f"Q. 내 투자엔 어떤 영향?\n"
                f"A. 추가 분석 필요\n\n"
                f"Q. 뭘 주목해야 해?\n"
                f"A. 관련 뉴스 지속 모니터링"
            )

        # Gemini 출력 정리 (앞뒤 공백, 불필요한 마크다운 제거)
        explanation = explanation.strip()

        # 마크다운 제거 (**, ##, ### 등)
        import re
        explanation = re.sub(r'\*\*(.+?)\*\*', r'\1', explanation)  # **bold** 제거
        explanation = re.sub(r'#{1,6}\s+', '', explanation)  # ## 제목 제거

        return explanation

    def _parse_explanation_sections(self, explanation: str) -> dict:
        """
        쉬운 설명을 섹션별로 파싱

        Returns:
            {
                'current': 현재 상황,
                'past': 과거 사례,
                'investment': 투자 영향,
                'market': 시장 관점
            }
        """
        sections = {
            'current': '',
            'past': '',
            'investment': '',
            'market': ''
        }

        # 섹션 구분 키워드
        current_markers = ['현재 상황', '한 마디로', '쉽게 말하면']
        past_markers = ['과거 사례', '이전에도', '역사를 보면']
        investment_markers = ['투자 영향', '내 돈', '투자자 입장']
        market_markers = ['시장 관점', '전문가들은', '시장에서 주목']

        lines = explanation.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 섹션 헤더 감지
            if any(marker in line for marker in current_markers):
                current_section = 'current'
                continue
            elif any(marker in line for marker in past_markers):
                current_section = 'past'
                continue
            elif any(marker in line for marker in investment_markers):
                current_section = 'investment'
                continue
            elif any(marker in line for marker in market_markers):
                current_section = 'market'
                continue

            # 현재 섹션에 내용 추가
            if current_section:
                if sections[current_section]:
                    sections[current_section] += ' ' + line
                else:
                    sections[current_section] = line

        return sections

    def _format_coupang_recommendations(self, recommendations: list) -> str:
        """쿠팡 파트너스 추천 포맷팅 (단순 텍스트, 1개만)"""
        if not recommendations:
            return ""

        rec = recommendations[0]
        category = rec.get('category', '상품')
        hook_title = rec.get('hook_title', '확인하기')
        link = rec.get('affiliate_link', '')

        msg = f"\n[쿠팡 파트너스 추천]\n"
        msg += f"{category}: {hook_title}\n"
        if link:
            msg += f"{link}"

        return msg

    def split_long_message(self, text: str, max_length: int = 4000) -> List[str]:
        """
        긴 메시지를 여러 개로 분할

        Args:
            text: 원본 텍스트
            max_length: 메시지당 최대 길이

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
                messages.append(current_msg.strip())
                current_msg = line + "\n"
            else:
                current_msg += line + "\n"

        if current_msg.strip():
            messages.append(current_msg.strip())

        return messages

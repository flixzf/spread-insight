# -*- coding: utf-8 -*-
"""
AI 기반 뉴스 선정 시스템

하드코딩된 키워드/점수 대신 LLM이 직접 뉴스의 중요도를 판단
"""

import os
import google.generativeai as genai
from models.news_article import NewsArticle
from typing import List, Optional


class AINewsSelector:
    """LLM 기반 뉴스 자동 선정"""

    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: Gemini API 키 (선택사항, 환경변수에서 자동 로드)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def select_best_news_from_metadata(
        self,
        metadata_list: List[dict],
        verbose: bool = True
    ) -> Optional[str]:
        """
        메타데이터(제목+요약)만으로 최고의 뉴스를 선정 - 빠른 선택용

        Args:
            metadata_list: [{'url': ..., 'title': ..., 'summary': ...}, ...]
            verbose: 상세 정보 출력 여부

        Returns:
            선정된 뉴스 URL (또는 None)
        """
        if not metadata_list:
            return None

        if len(metadata_list) == 1:
            return metadata_list[0]['url']

        # 뉴스 목록을 프롬프트용으로 포맷팅
        news_list = ""
        for i, meta in enumerate(metadata_list, 1):
            news_list += f"{i}. 제목: {meta['title']}\n"
            if meta.get('summary'):
                news_list += f"   요약: {meta['summary']}\n"
            news_list += "\n"

        prompt = f"""
당신은 경제 뉴스 편집장입니다.
다음 {len(metadata_list)}개 뉴스 중에서 **경제적으로 가장 중요하고 독자에게 유용한 뉴스 1개**를 선정해주세요.

**선정 기준**:
1. **경제적 영향력**: 금리, 환율, 관세, 무역, 증시 등 실질적 경제 이슈
2. **시의성**: 최근 발생한 중요한 경제 이벤트
3. **실용성**: 독자의 재테크/투자/소비에 도움이 되는 정보
4. **학습 가치**: 경제 현상을 이해하는 데 도움

**제외 기준**:
- 부고, 인사 이동, 수상 등 경제와 무관한 뉴스
- 지엽적이고 특정 기업/인물에만 관련된 뉴스
- 광고성 또는 홍보성 기사

뉴스 목록:
{news_list}

**답변 형식**:
선정 번호: [번호]
선정 이유: [50자 이내로 간단히]

예시:
선정 번호: 3
선정 이유: 달러 환율 급등은 수출입 기업과 개인 투자자 모두에게 직접적 영향을 미치는 중요한 경제 지표입니다.
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # 선정 번호 추출 (출력 전에 먼저 추출)
            selected_number = self._extract_selected_number(result_text)

            if verbose:
                try:
                    print("\n[AI 선정 결과]")
                    print("-" * 70)
                    print(result_text)
                    print("-" * 70)
                except UnicodeEncodeError:
                    # Windows 콘솔 인코딩 문제 - 무시하고 계속 진행
                    print("\n[AI 선정 결과] (콘솔 인코딩 문제로 일부 출력 생략)")

            if selected_number and 1 <= selected_number <= len(metadata_list):
                selected_url = metadata_list[selected_number - 1]['url']

                if verbose:
                    try:
                        print(f"\n✅ 선정: [{selected_number}] {metadata_list[selected_number - 1]['title']}")
                    except UnicodeEncodeError:
                        print(f"\n선정: [{selected_number}]")

                return selected_url
            else:
                print(f"[WARNING] AI가 유효한 번호를 선정하지 못했습니다. 첫 번째 뉴스를 반환합니다.")
                return metadata_list[0]['url']

        except Exception as e:
            try:
                print(f"[ERROR] AI 선정 실패: {e}")
            except:
                print("[ERROR] AI 선정 실패")
            print("[FALLBACK] 첫 번째 뉴스를 반환합니다.")
            return metadata_list[0]['url']

    def select_best_news(
        self,
        articles: List[NewsArticle],
        verbose: bool = True
    ) -> Optional[NewsArticle]:
        """
        여러 뉴스 중 경제적으로 가장 중요한 뉴스 1개를 AI가 선정

        Args:
            articles: 후보 뉴스 리스트
            verbose: 상세 정보 출력 여부

        Returns:
            선정된 뉴스 (또는 None)
        """
        if not articles:
            return None

        if len(articles) == 1:
            return articles[0]

        # 뉴스 목록을 프롬프트용으로 포맷팅
        news_list = ""
        for i, article in enumerate(articles, 1):
            news_list += f"""
{i}. 제목: {article.title}
   출처: {article.source}
   날짜: {article.published_at.strftime('%Y-%m-%d %H:%M')}
   본문 미리보기: {article.content[:300]}...
"""

        prompt = f"""
당신은 경제 뉴스 편집장입니다.
다음 {len(articles)}개 뉴스 중에서 **경제적으로 가장 중요하고 독자에게 유용한 뉴스 1개**를 선정해주세요.

**선정 기준**:
1. **경제적 영향력**: 금리, 환율, 관세, 무역, 증시 등 실질적 경제 이슈
2. **시의성**: 최근 발생한 중요한 경제 이벤트
3. **실용성**: 독자의 재테크/투자/소비에 도움이 되는 정보
4. **학습 가치**: 경제 현상을 이해하는 데 도움

**제외 기준**:
- 부고, 인사 이동, 수상 등 경제와 무관한 뉴스
- 지엽적이고 특정 기업/인물에만 관련된 뉴스
- 광고성 또는 홍보성 기사

뉴스 목록:
{news_list}

**답변 형식**:
선정 번호: [번호]
선정 이유: [50자 이내로 간단히]

예시:
선정 번호: 3
선정 이유: 달러 환율 급등은 수출입 기업과 개인 투자자 모두에게 직접적 영향을 미치는 중요한 경제 지표입니다.
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            if verbose:
                print("\n[AI 선정 결과]")
                print("-" * 70)
                print(result_text)
                print("-" * 70)

            # 선정 번호 추출
            selected_number = self._extract_selected_number(result_text)

            if selected_number and 1 <= selected_number <= len(articles):
                selected_article = articles[selected_number - 1]

                if verbose:
                    print(f"\n✅ 선정: [{selected_number}] {selected_article.title}")

                return selected_article
            else:
                print(f"[WARNING] AI가 유효한 번호를 선정하지 못했습니다. 첫 번째 뉴스를 반환합니다.")
                return articles[0]

        except Exception as e:
            print(f"[ERROR] AI 선정 실패: {e}")
            print("[FALLBACK] 첫 번째 뉴스를 반환합니다.")
            return articles[0]

    def _extract_selected_number(self, response_text: str) -> Optional[int]:
        """
        AI 응답에서 선정 번호 추출

        Args:
            response_text: AI 응답 텍스트

        Returns:
            선정 번호 (또는 None)
        """
        import re

        # "선정 번호: 3" 형태 찾기
        match = re.search(r'선정\s*번호\s*[:：]\s*(\d+)', response_text)
        if match:
            return int(match.group(1))

        # "번호: 3" 형태 찾기
        match = re.search(r'번호\s*[:：]\s*(\d+)', response_text)
        if match:
            return int(match.group(1))

        # 숫자만 있는 경우
        match = re.search(r'^(\d+)', response_text)
        if match:
            return int(match.group(1))

        return None

    def rank_news(
        self,
        articles: List[NewsArticle],
        top_n: int = 3,
        verbose: bool = True
    ) -> List[NewsArticle]:
        """
        여러 뉴스를 중요도 순으로 랭킹

        Args:
            articles: 후보 뉴스 리스트
            top_n: 반환할 상위 뉴스 개수
            verbose: 상세 정보 출력 여부

        Returns:
            랭킹된 뉴스 리스트 (상위 N개)
        """
        if not articles:
            return []

        if len(articles) <= top_n:
            return articles

        # 뉴스 목록을 프롬프트용으로 포맷팅
        news_list = ""
        for i, article in enumerate(articles, 1):
            news_list += f"""
{i}. 제목: {article.title}
   본문: {article.content[:200]}...
"""

        prompt = f"""
다음 {len(articles)}개 경제 뉴스를 중요도 순으로 랭킹해주세요.

뉴스 목록:
{news_list}

**랭킹 기준**: 경제적 영향력, 시의성, 독자 유용성

**답변 형식** (번호만 쉼표로 구분):
3, 1, 5, 2, 4

(예: 3번 뉴스가 가장 중요, 1번이 두 번째, ...)
        """.strip()

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            if verbose:
                print("\n[AI 랭킹 결과]")
                print(result_text)

            # 번호 추출 (예: "3, 1, 5, 2, 4")
            import re
            numbers = re.findall(r'\d+', result_text)
            ranked_indices = [int(n) - 1 for n in numbers if 1 <= int(n) <= len(articles)]

            # 랭킹된 순서대로 뉴스 반환
            ranked_articles = [articles[i] for i in ranked_indices if i < len(articles)]

            # 누락된 뉴스 추가 (랭킹에 없었던 것들)
            for i, article in enumerate(articles):
                if i not in ranked_indices:
                    ranked_articles.append(article)

            return ranked_articles[:top_n]

        except Exception as e:
            print(f"[ERROR] AI 랭킹 실패: {e}")
            return articles[:top_n]


if __name__ == '__main__':
    # 테스트
    selector = AINewsSelector()

    # 더미 뉴스 생성
    from datetime import datetime

    test_articles = [
        NewsArticle(
            url="https://example.com/1",
            title="'비철금속 거목' 최창걸 고려아연 명예회장 별세",
            content="최창걸 고려아연 명예회장이 지난 6일 숙환으로 별세했다. 84세. 비철금속 제련업의 불모지였던 한국에서...",
            published_at=datetime.now(),
            source="서울경제"
        ),
        NewsArticle(
            url="https://example.com/2",
            title="[단독] 환율 급등, 연준 긴축에 원·달러 1400원 돌파 전망",
            content="미국 연방준비제도(Fed·연준)가 금리 인상을 지속하면서 원·달러 환율이 1400원을 돌파할 것이라는 전망이 나왔다...",
            published_at=datetime.now(),
            source="한국경제"
        ),
        NewsArticle(
            url="https://example.com/3",
            title="삼성전자, 신규 임원 50명 선임",
            content="삼성전자가 올해 신규 임원 50명을 선임했다고 발표했다. 이는 작년보다 10명 늘어난 규모다...",
            published_at=datetime.now(),
            source="매일경제"
        )
    ]

    print("=" * 70)
    print("AI News Selector Test")
    print("=" * 70)

    selected = selector.select_best_news(test_articles, verbose=True)

    print("\n" + "=" * 70)
    print(f"최종 선정: {selected.title}")
    print("=" * 70)

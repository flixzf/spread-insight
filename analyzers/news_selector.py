"""
뉴스 선정 로직
CONTENT_STRATEGY.md의 선정 기준을 구현
"""

from datetime import datetime
from models.news_article import NewsArticle
import re


class NewsSelector:
    """뉴스 자동 선정 시스템"""

    # 우선순위 키워드 (CONTENT_STRATEGY.md 기준) - 실질적 경제 뉴스
    PRIORITY_KEYWORDS = [
        # 금융/통화 (최우선)
        "금리", "환율", "달러", "원화", "연준", "Fed", "한국은행", "기준금리",
        "통화정책", "양적완화", "긴축",
        # 무역/관세 (최우선)
        "관세", "무역", "수출", "수입", "무역수지", "통상",
        # 부동산
        "부동산", "아파트", "전세", "집값", "대출", "주택담보대출", "LTV", "DTI",
        # 물가/세금
        "물가", "인플레이션", "CPI", "소비자물가", "생산자물가", "세금", "세제", "감세", "증세",
        # 투자/증시
        "주식", "코스피", "다우", "나스닥", "S&P", "채권", "국채", "회사채",
        # 정책 (경제 정책만)
        "경기부양", "재정", "예산", "경제정책", "법안", "규제완화", "개정",
        # 산업/경기
        "GDP", "경제성장률", "실업률", "고용", "경기", "경기침체", "불황",
        # 국제경제
        "중국", "일본", "미국 경제", "유럽", "OPEC", "유가"
    ]

    # 제외 키워드 (부고, 인사 등 비경제 뉴스)
    EXCLUDE_KEYWORDS = [
        "별세", "타계", "사망", "부고", "영면", "별세",
        "인사", "임명", "취임", "퇴임", "영전",
        "수상", "시상", "포상", "훈장",
        "결혼", "이혼", "열애",
        "사고", "사건", "범죄", "구속"
    ]

    # 신뢰도 높은 언론사
    TRUSTED_SOURCES = [
        "한국경제", "매일경제", "조선일보", "중앙일보",
        "한겨레", "경향신문", "서울경제", "뉴시스"
    ]

    def calculate_score(self, article: NewsArticle) -> float:
        """
        뉴스 점수 계산 (0~100)

        배점:
        - 키워드 매칭: 40점
        - 시의성: 20점
        - 신뢰도: 20점
        - 본문 길이: 10점
        - 통계 포함: 10점
        - 제외 키워드 페널티: -50점
        """
        score = 0

        # 0. 제외 키워드 체크 (즉시 탈락)
        for exclude_kw in self.EXCLUDE_KEYWORDS:
            if exclude_kw in article.title or exclude_kw in article.content:
                return -50  # 부고/인사 등은 즉시 낮은 점수

        # 1. 키워드 매칭 (40점)
        title_keywords = sum(1 for kw in self.PRIORITY_KEYWORDS if kw in article.title)
        content_keywords = sum(1 for kw in self.PRIORITY_KEYWORDS if kw in article.content)

        # 제목에 키워드 있으면 가중치 높임
        keyword_score = (title_keywords * 10) + (content_keywords * 2)
        score += min(40, keyword_score)

        # 2. 시의성 (20점) - 최근 기사일수록 높은 점수
        hours_old = (datetime.now() - article.published_at).total_seconds() / 3600
        if hours_old < 6:
            score += 20
        elif hours_old < 24:
            score += 15
        elif hours_old < 48:
            score += 10
        elif hours_old < 72:
            score += 5

        # 3. 신뢰도 (20점) - 주요 언론사
        if any(src in article.source for src in self.TRUSTED_SOURCES):
            score += 20

        # 4. 본문 길이 (10점) - 너무 짧거나 길지 않은 것
        content_length = len(article.content)
        if 500 <= content_length <= 3000:
            score += 10
        elif 300 <= content_length < 500 or 3000 < content_length <= 4000:
            score += 7
        elif 200 <= content_length < 300 or 4000 < content_length <= 5000:
            score += 5

        # 5. 숫자/통계 포함 여부 (10점) - 데이터 기반 뉴스
        # "3.5%", "10조원", "5년" 등의 패턴 찾기
        numbers = re.findall(r'\d+\.?\d*%', article.content)
        currency = re.findall(r'\d+조|\d+억', article.content)

        data_count = len(numbers) + len(currency)
        if data_count >= 5:
            score += 10
        elif data_count >= 3:
            score += 7
        elif data_count >= 1:
            score += 5

        return round(score, 2)

    def select_top_news(
        self,
        articles: list[NewsArticle],
        top_n: int = 1,
        verbose: bool = True
    ) -> list[NewsArticle]:
        """
        상위 N개 뉴스 선정

        Args:
            articles: 후보 기사 리스트
            top_n: 선정할 기사 수
            verbose: 상세 정보 출력 여부

        Returns:
            선정된 기사 리스트
        """
        if not articles:
            return []

        # 점수 계산
        scored = []
        for article in articles:
            score = self.calculate_score(article)
            scored.append((article, score))

        # 점수 내림차순 정렬
        scored.sort(key=lambda x: x[1], reverse=True)

        if verbose:
            print(f"\n[뉴스 선정] 총 {len(articles)}개 기사 분석 완료")
            print("=" * 70)
            print(f"{'순위':<5} {'점수':<8} {'제목':<40} {'날짜'}")
            print("=" * 70)

            for i, (article, score) in enumerate(scored[:10], 1):
                # 특수 공백 문자 제거 (cp949 호환성)
                title = article.title.replace('\xa0', ' ').replace('\u3000', ' ')
                title = title[:37] + "..." if len(title) > 40 else title
                date_str = article.published_at.strftime('%m/%d %H:%M')
                print(f"{i:<5} {score:<8.1f} {title:<40} {date_str}")

            print("=" * 70)

            if top_n <= len(scored):
                selected = scored[0][0]
                selected_score = scored[0][1]
                print(f"\n[선정] {selected.title}")
                print(f"점수: {selected_score}점")
                print(f"선정 이유:")
                self._explain_score(selected, selected_score)

        # 상위 N개 반환
        return [article for article, score in scored[:top_n]]

    def _explain_score(self, article: NewsArticle, score: float):
        """점수 산출 근거 설명"""

        # 키워드 체크
        keywords_found = [kw for kw in self.PRIORITY_KEYWORDS if kw in article.title or kw in article.content]
        if keywords_found:
            print(f"  [+] 우선순위 키워드 포함: {', '.join(keywords_found[:5])}")

        # 시의성
        hours_old = (datetime.now() - article.published_at).total_seconds() / 3600
        if hours_old < 24:
            print(f"  [+] 최근 뉴스 ({int(hours_old)}시간 전)")

        # 신뢰도
        if any(src in article.source for src in self.TRUSTED_SOURCES):
            print(f"  [+] 신뢰할 수 있는 언론사")

        # 본문 길이
        content_length = len(article.content)
        print(f"  [+] 적절한 본문 길이 ({content_length}자)")

        # 통계 포함
        numbers = re.findall(r'\d+\.?\d*%', article.content)
        currency = re.findall(r'\d+조|\d+억', article.content)
        data_count = len(numbers) + len(currency)
        if data_count > 0:
            print(f"  [+] 데이터 기반 ({data_count}개 통계/수치 포함)")

    def filter_by_criteria(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        """
        CONTENT_STRATEGY.md의 필수 기준 필터링

        기준:
        - 영향력: 우선순위 키워드 최소 1개 포함
        - 실천 가능성: 본문 길이 200자 이상
        - 학습 가치: 통계/숫자 포함
        """
        filtered = []

        for article in articles:
            # 영향력: 키워드 체크
            has_keyword = any(kw in article.title or kw in article.content
                            for kw in self.PRIORITY_KEYWORDS)

            # 실천 가능성: 본문 길이
            has_enough_content = len(article.content) >= 200

            # 학습 가치: 숫자/통계 포함
            numbers = re.findall(r'\d+\.?\d*%|\d+조|\d+억', article.content)
            has_data = len(numbers) >= 1

            # 모든 기준 통과
            if has_keyword and has_enough_content and has_data:
                filtered.append(article)

        return filtered

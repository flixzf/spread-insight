"""
경제 용어 추출 및 설명 생성
CONTENT_STRATEGY.md의 "5️⃣ 어떤 용어를 쉽게 전달할 것인가?" 구현
"""

import json
import os
from models.news_article import NewsArticle
from analyzers.gemini_analyzer import GeminiAnalyzer


class TerminologyExtractor:
    """경제 용어 추출 및 설명 시스템"""

    def __init__(self, db_path: str = './data/terminology_db.json'):
        """
        Args:
            db_path: 용어 데이터베이스 JSON 파일 경로
        """
        self.db_path = db_path
        self.term_database = self._load_database()
        self.gemini = GeminiAnalyzer()

    def _load_database(self) -> dict:
        """용어 데이터베이스 로드"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"용어 데이터베이스를 찾을 수 없습니다: {self.db_path}")

        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_terms(self, article: NewsArticle, max_terms: int = 1) -> list[dict]:
        """
        기사에서 중요 용어 추출

        Args:
            article: 뉴스 기사 객체
            max_terms: 추출할 용어 수

        Returns:
            용어 정보 리스트 [{'term': '용어', 'tier': 1, 'count': 3}, ...]
        """
        found_terms = []

        # 데이터베이스에 등록된 용어 찾기
        for term, info in self.term_database.items():
            # 제목과 본문에서 용어 검색
            title_count = article.title.count(term)
            content_count = article.content.count(term)
            total_count = title_count + content_count

            if total_count > 0:
                found_terms.append({
                    'term': term,
                    'tier': info['tier'],
                    'category': info['category'],
                    'count': total_count,
                    'in_title': title_count > 0
                })

        # 정렬 우선순위:
        # 1. Tier 낮을수록 (1 > 2 > 3) - 중요도 높음
        # 2. 제목에 있는 용어 우선
        # 3. 출현 빈도 높을수록
        found_terms.sort(key=lambda x: (x['tier'], not x['in_title'], -x['count']))

        return found_terms[:max_terms]

    def generate_explanation(self, term: str) -> dict:
        """
        용어 쉬운 설명 생성

        Args:
            term: 설명할 용어

        Returns:
            용어 설명 딕셔너리
        """
        # 데이터베이스에 있는 용어인지 확인
        if term in self.term_database:
            info = self.term_database[term]
            return {
                'term': term,
                'tier': info['tier'],
                'category': info['category'],
                'definition': info['simple_def'],
                'example': info['example'],
                'why_important': info['why_important']
            }

        # 데이터베이스에 없으면 Gemini에게 요청
        return self._generate_with_gemini(term)

    def _generate_with_gemini(self, term: str) -> dict:
        """Gemini로 새로운 용어 설명 생성"""

        prompt = f"""
다음 경제 용어를 초등학생도 이해할 수 있게 설명해주세요:

용어: {term}

답변 형식 (각 항목을 구분하여 작성):

1. 한 줄 정의 (20자 이내):
[여기에 작성]

2. 구체적 예시 (일상생활 비유):
[여기에 작성]

3. 왜 중요한가? (1문장):
[여기에 작성]
        """.strip()

        try:
            response = self.gemini.model.generate_content(
                prompt,
                safety_settings=self.gemini.safety_settings
            )

            text = response.text.strip()

            # 파싱 (간단하게)
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            return {
                'term': term,
                'tier': 3,  # 새로운 용어는 tier 3로
                'category': '기타',
                'definition': lines[0] if len(lines) > 0 else '정의 없음',
                'example': lines[1] if len(lines) > 1 else '예시 없음',
                'why_important': lines[2] if len(lines) > 2 else '중요도 설명 없음'
            }

        except Exception as e:
            raise Exception(f"용어 설명 생성 실패: {e}")

    def format_explanation(self, term_info: dict) -> str:
        """
        용어 설명을 CONTENT_STRATEGY.md 형식으로 포맷팅

        Args:
            term_info: generate_explanation()의 결과

        Returns:
            포맷팅된 설명 텍스트
        """
        template = f"""
[용어] 알아두면 좋은 용어

**"{term_info['term']}"**
{term_info['definition']}

[쉽게] 쉽게 말하면?
{term_info['example']}

[중요] 왜 중요할까요?
{term_info['why_important']}
        """.strip()

        return template

    def extract_and_explain(self, article: NewsArticle, max_terms: int = 1) -> list[dict]:
        """
        기사에서 용어를 추출하고 설명까지 생성 (원스톱)

        Args:
            article: 뉴스 기사 객체
            max_terms: 설명할 용어 수

        Returns:
            설명이 포함된 용어 정보 리스트
        """
        # 용어 추출
        found_terms = self.extract_terms(article, max_terms)

        if not found_terms:
            print("[!] 기사에서 등록된 용어를 찾을 수 없습니다.")
            return []

        # 각 용어에 대해 설명 생성
        results = []
        for term_data in found_terms:
            term = term_data['term']
            explanation = self.generate_explanation(term)
            formatted = self.format_explanation(explanation)

            results.append({
                **explanation,
                'count': term_data['count'],
                'formatted': formatted
            })

        return results


if __name__ == '__main__':
    # 간단한 테스트
    print("용어 추출 시스템 테스트...")

    try:
        extractor = TerminologyExtractor()
        print(f"[OK] 용어 데이터베이스 로드 완료: {len(extractor.term_database)}개 용어")

        # 테스트 용어 설명
        test_term = "기준금리"
        explanation = extractor.generate_explanation(test_term)
        formatted = extractor.format_explanation(explanation)

        print(f"\n테스트 용어: {test_term}")
        print("=" * 60)
        print(formatted)

    except Exception as e:
        print(f"[ERROR] {e}")

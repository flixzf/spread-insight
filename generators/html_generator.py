"""
HTML 생성기
CONTENT_STRATEGY.md의 7섹션 구조로 HTML 페이지 생성

쿠팡 파트너스 준수사항:
- 제휴 링크 사용 시 대가성 문구 포함 필수
- 공정거래위원회 가이드라인 준수
"""

import json
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from urllib.parse import quote


class HTMLGenerator:
    def __init__(self, template_dir: str = './templates'):
        """Jinja2 환경 초기화"""
        self.template_dir = Path(template_dir)

        # Jinja2 환경 설정
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )

        # 커스텀 필터 등록
        self.env.filters['urlencode'] = lambda x: quote(str(x))

        self.template = self.env.get_template('news_template.html')

    def generate_from_json(self, json_path: str, output_path: str) -> None:
        """JSON 파일에서 HTML 생성"""
        with open(json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)

        self.generate_from_article(article_data, output_path)
        print(f"[OK] HTML 생성 완료: {output_path}")

    def generate_from_article(self, article_data: dict, output_path: str) -> None:
        """딕셔너리에서 직접 HTML 생성"""
        # 템플릿에 전달할 데이터 준비
        template_data = self._prepare_template_data(article_data)

        # HTML 렌더링
        html_content = self.template.render(article=template_data)

        # 파일 저장
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _prepare_template_data(self, article_data: dict) -> dict:
        """
        템플릿에 전달할 데이터 준비

        쿠팡 파트너스 준수사항:
        - recommended_books에 affiliate_link가 포함되어야 함
        - 템플릿에서 대가성 문구를 자동으로 표시
        """
        prepared = article_data.copy()

        # 1. 날짜 포맷팅
        if isinstance(article_data.get('published_at'), str):
            try:
                dt = datetime.fromisoformat(article_data['published_at'])
                prepared['published_at'] = dt.strftime('%Y년 %m월 %d일 %H:%M')
            except (ValueError, TypeError):
                prepared['published_at'] = article_data.get('published_at', '')

        # 2. 키워드 기본값
        if 'keywords' not in prepared or not prepared['keywords']:
            prepared['keywords'] = []

        # 3. 용어 설명 기본값
        if 'terminology' not in prepared or not prepared['terminology']:
            prepared['terminology'] = {}

        # 4. 요약 기본값
        if 'summary' not in prepared or not prepared['summary']:
            prepared['summary'] = prepared.get('content', '')[:300] + '...'

        # 5. 쉬운 설명 기본값
        if 'easy_explanation' not in prepared or not prepared['easy_explanation']:
            prepared['easy_explanation'] = '준비중입니다.'

        # 6. 쿠팡 파트너스 링크 검증
        # recommended_books가 있는 경우 affiliate_link 확인
        if 'recommended_books' in prepared and prepared['recommended_books']:
            for book in prepared['recommended_books']:
                if 'affiliate_link' not in book or not book['affiliate_link']:
                    print(f"[WARNING] 도서 '{book.get('title', 'Unknown')}'에 affiliate_link가 없습니다.")

        return prepared


if __name__ == '__main__':
    # 간단한 테스트
    generator = HTMLGenerator()

    test_article = {
        'url': 'https://example.com',
        'title': '테스트 기사',
        'content': '테스트 내용',
        'published_at': '2025-10-09T13:24:08',
        'source': '테스트',
        'keywords': ['키워드1', '키워드2'],
        'summary': '테스트 요약입니다.',
        'easy_explanation': '쉽게 설명하면 이렇습니다.',
        'terminology': {
            '테스트용어': {
                'tier': 1,
                'category': '금융',
                'definition': '테스트 정의',
                'example': '테스트 예시',
                'why_important': '테스트 중요성'
            }
        }
    }

    generator.generate_from_article(test_article, './output/test.html')
    print("[테스트] HTML 생성 완료")

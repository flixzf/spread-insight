"""
Gemini API 연동 및 요약 테스트

Step 2.1: Gemini API를 사용하여 선정된 기사를 요약합니다.
"""

from analyzers.gemini_analyzer import GeminiAnalyzer
from models.news_article import NewsArticle
import os


if __name__ == '__main__':
    print("=" * 70)
    print("Spread Insight - Gemini API 연동 및 요약 테스트")
    print("=" * 70)

    # ===== 1단계: API 연결 테스트 =====
    print("\n[1단계] API 연결 테스트...")

    try:
        analyzer = GeminiAnalyzer()

        if analyzer.test_connection():
            print("[OK] API 연결 성공!\n")
        else:
            print("[ERROR] API 연결 실패!")
            print("다음을 확인하세요:")
            print("1. .env 파일에 GEMINI_API_KEY가 설정되어 있는지")
            print("2. API 키가 유효한지 (https://makersuite.google.com/app/apikey)")
            exit(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        print("\n해결 방법:")
        print("1. https://makersuite.google.com/app/apikey 에서 API 키 발급")
        print("2. .env 파일에 GEMINI_API_KEY=발급받은_키 추가")
        exit(1)

    # ===== 2단계: 저장된 기사 로드 =====
    print("[2단계] 저장된 기사 로드 중...")

    article_path = './data/raw/selected_article.json'

    if not os.path.exists(article_path):
        print(f"[ERROR] {article_path} 파일이 없습니다.")
        print("먼저 test_scraper.py를 실행하여 기사를 선정하세요.")
        exit(1)

    try:
        article = NewsArticle.load_from_json(article_path)
        print(f"[OK] 기사 로드 완료\n")

    except Exception as e:
        print(f"[ERROR] 기사 로드 실패: {e}")
        exit(1)

    # ===== 3단계: 원본 기사 정보 출력 =====
    print("=" * 70)
    print("원본 기사")
    print("=" * 70)
    print(f"제목: {article.title}")
    print(f"출처: {article.source}")
    print(f"날짜: {article.published_at.strftime('%Y년 %m월 %d일 %H:%M')}")
    print(f"본문 길이: {len(article.content)}자")
    print(f"\n본문 미리보기:")
    print("-" * 70)
    print(article.content[:500])
    print("...")
    print("-" * 70)

    # ===== 4단계: 요약 생성 =====
    print("\n[3단계] 요약 생성 중...")
    print("=" * 70)

    try:
        summary = analyzer.summarize(article, num_sentences=3)
        print("\n[OK] 요약 생성 성공!\n")
        print("요약 (3문장):")
        print("-" * 70)
        print(summary)
        print("-" * 70)

        # 기사 객체에 저장
        article.summary = summary

    except Exception as e:
        print(f"[ERROR] 요약 생성 실패: {e}")
        exit(1)

    # ===== 5단계: 쉬운 설명 생성 =====
    print("\n[4단계] 쉬운 설명 생성 중...")
    print("=" * 70)

    try:
        easy_explanation = analyzer.explain_simple(article)
        print("\n[OK] 쉬운 설명 생성 성공!\n")
        print("쉬운 설명:")
        print("-" * 70)
        print(easy_explanation)
        print("-" * 70)

        # 기사 객체에 저장
        article.easy_explanation = easy_explanation

    except Exception as e:
        print(f"[ERROR] 쉬운 설명 생성 실패: {e}")
        exit(1)

    # ===== 6단계: 키워드 추출 =====
    print("\n[5단계] 키워드 추출 중...")
    print("=" * 70)

    try:
        keywords = analyzer.extract_keywords(article, max_keywords=5)
        print("\n[OK] 키워드 추출 성공!\n")
        print("핵심 키워드:")
        print("-" * 70)
        for i, keyword in enumerate(keywords, 1):
            print(f"  {i}. {keyword}")
        print("-" * 70)

        # 기사 객체에 저장
        article.keywords = keywords

    except Exception as e:
        print(f"[ERROR] 키워드 추출 실패: {e}")
        exit(1)

    # ===== 7단계: 결과 저장 =====
    print("\n[6단계] 분석 결과 저장 중...")

    try:
        output_path = './data/processed/analyzed_article.json'
        os.makedirs('./data/processed', exist_ok=True)

        article.save_to_json(output_path)
        print(f"[OK] 저장 완료: {output_path}")

    except Exception as e:
        print(f"[ERROR] 저장 실패: {e}")
        exit(1)

    # ===== 완료 =====
    print("\n" + "=" * 70)
    print("작업 완료!")
    print("=" * 70)
    print("\n분석 요약:")
    print(f"  - 제목: {article.title[:50]}...")
    print(f"  - 요약: {len(summary)}자")
    print(f"  - 쉬운 설명: {len(easy_explanation)}자")
    print(f"  - 키워드: {len(keywords)}개")
    print(f"  - 저장 위치: {output_path}")
    print("\n다음 단계: Phase 2.2 - 용어 추출 및 설명")

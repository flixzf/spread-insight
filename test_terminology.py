"""
용어 추출 및 설명 테스트

Step 2.2: 기사에서 경제 용어를 자동으로 추출하고 쉬운 설명을 생성합니다.
"""

from analyzers.terminology_extractor import TerminologyExtractor
from models.news_article import NewsArticle
import os


if __name__ == '__main__':
    print("=" * 70)
    print("Spread Insight - 용어 추출 및 설명 테스트")
    print("=" * 70)

    # ===== 1단계: 용어 추출 시스템 초기화 =====
    print("\n[1단계] 용어 추출 시스템 초기화...")

    try:
        extractor = TerminologyExtractor()
        print(f"[OK] 용어 데이터베이스 로드 완료: {len(extractor.term_database)}개 용어\n")

    except Exception as e:
        print(f"[ERROR] 초기화 실패: {e}")
        exit(1)

    # ===== 2단계: 분석된 기사 로드 =====
    print("[2단계] 분석된 기사 로드 중...")

    article_path = './data/processed/analyzed_article.json'

    if not os.path.exists(article_path):
        print(f"[ERROR] {article_path} 파일이 없습니다.")
        print("먼저 test_gemini.py를 실행하세요.")
        exit(1)

    try:
        article = NewsArticle.load_from_json(article_path)
        print(f"[OK] 기사 로드 완료\n")

    except Exception as e:
        print(f"[ERROR] 기사 로드 실패: {e}")
        exit(1)

    # ===== 3단계: 기사 정보 출력 =====
    print("=" * 70)
    print("분석 대상 기사")
    print("=" * 70)
    print(f"제목: {article.title}")
    print(f"출처: {article.source}")
    print(f"날짜: {article.published_at.strftime('%Y년 %m월 %d일')}")
    print(f"본문 길이: {len(article.content)}자")
    print("-" * 70)

    # ===== 4단계: 용어 추출 =====
    print("\n[3단계] 용어 추출 중...")

    try:
        found_terms = extractor.extract_terms(article, max_terms=5)

        if not found_terms:
            print("[!] 기사에서 등록된 경제 용어를 찾을 수 없습니다.")
            exit(1)

        print(f"[OK] {len(found_terms)}개 용어 발견\n")

        print("발견된 용어:")
        print("-" * 70)
        for i, term_data in enumerate(found_terms, 1):
            print(f"  {i}. {term_data['term']} "
                  f"(Tier {term_data['tier']}, "
                  f"{term_data['category']}, "
                  f"출현 {term_data['count']}회"
                  f"{', 제목 포함' if term_data['in_title'] else ''})")
        print("-" * 70)

    except Exception as e:
        print(f"[ERROR] 용어 추출 실패: {e}")
        exit(1)

    # ===== 5단계: 최우선 용어 선정 =====
    print("\n[4단계] 설명할 용어 선정...")

    selected_term = found_terms[0]['term']
    print(f"[OK] 선정된 용어: '{selected_term}'\n")

    # ===== 6단계: 용어 설명 생성 =====
    print("[5단계] 용어 설명 생성 중...")
    print("=" * 70)

    try:
        explanation = extractor.generate_explanation(selected_term)
        formatted = extractor.format_explanation(explanation)

        print("\n[OK] 설명 생성 완료!\n")
        print(formatted)
        print("\n" + "=" * 70)

        # 기사 객체에 저장
        if not article.terminology:
            article.terminology = {}

        article.terminology[selected_term] = {
            'definition': explanation['definition'],
            'example': explanation['example'],
            'why_important': explanation['why_important'],
            'tier': explanation['tier'],
            'category': explanation['category']
        }

    except Exception as e:
        print(f"[ERROR] 설명 생성 실패: {e}")
        exit(1)

    # ===== 7단계: 다른 용어들도 간단히 표시 =====
    if len(found_terms) > 1:
        print("\n[참고] 다른 용어들:")
        print("-" * 70)
        for term_data in found_terms[1:4]:  # 최대 3개만
            term = term_data['term']
            if term in extractor.term_database:
                info = extractor.term_database[term]
                print(f"\n• {term}")
                print(f"  정의: {info['simple_def']}")
        print("-" * 70)

    # ===== 8단계: 결과 저장 =====
    print("\n[6단계] 용어 설명 추가하여 저장 중...")

    try:
        output_path = './data/processed/article_with_terminology.json'
        article.save_to_json(output_path)
        print(f"[OK] 저장 완료: {output_path}")

    except Exception as e:
        print(f"[ERROR] 저장 실패: {e}")
        exit(1)

    # ===== 완료 =====
    print("\n" + "=" * 70)
    print("작업 완료!")
    print("=" * 70)
    print("\n최종 결과:")
    print(f"  - 제목: {article.title[:50]}...")
    print(f"  - 발견된 용어: {len(found_terms)}개")
    print(f"  - 설명한 용어: {selected_term}")
    print(f"  - 저장 위치: {output_path}")
    print("\n다음 단계: Phase 2.3 - 과거 데이터 수집")

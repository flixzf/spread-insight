"""
뉴스 스크래핑 테스트 (CONTENT_STRATEGY.md 반영)

단순히 첫 번째 기사를 가져오는 것이 아닌,
선정 기준(영향력, 실천 가능성, 학습 가치, 시의성)에 따라
가장 좋은 기사 1개를 선정합니다.
"""

from scrapers.naver_scraper import NaverScraper
from analyzers.ai_news_selector import AINewsSelector  # AI 기반 선정으로 변경
import time


if __name__ == '__main__':
    print("=" * 70)
    print("Spread Insight - 뉴스 자동 선정 및 스크래핑")
    print("=" * 70)

    scraper = NaverScraper()
    selector = AINewsSelector()  # AI 기반 선정기

    # ===== 1단계: 메타데이터 빠르게 수집 (30개) =====
    print("\n[1단계] 경제 섹션에서 기사 메타데이터(제목+요약) 빠르게 수집 중...")
    try:
        metadata_list = scraper.get_article_metadata(limit=30)  # 30개 메타데이터만 (빠름!)
        print(f"[OK] {len(metadata_list)}개 기사 메타데이터 수집 완료")
        for i, meta in enumerate(metadata_list[:5], 1):
            print(f"  {i}. {meta['title'][:50]}...")
        if len(metadata_list) > 5:
            print(f"  ... 외 {len(metadata_list) - 5}개")
    except Exception as e:
        print(f"[ERROR] 메타데이터 수집 실패: {e}")
        exit(1)

    if not metadata_list:
        print("[ERROR] 수집된 기사가 없습니다.")
        exit(1)

    # ===== 2단계: AI가 메타데이터만으로 최고의 뉴스 선정 =====
    print(f"\n[2단계] AI가 메타데이터를 분석하여 경제적으로 가장 중요한 뉴스 선정 중...")
    print("-" * 70)

    selected_url = selector.select_best_news_from_metadata(metadata_list, verbose=True)

    if not selected_url:
        print("[ERROR] AI가 뉴스를 선정하지 못했습니다.")
        exit(1)

    # ===== 3단계: 선정된 뉴스 1개만 본문 스크래핑 =====
    print(f"\n[3단계] 선정된 뉴스 본문 스크래핑 중...")
    try:
        selected_article = scraper.scrape_article(selected_url)
        print(f"[OK] 본문 수집 완료")
    except Exception as e:
        print(f"[ERROR] 본문 스크래핑 실패: {e}")
        exit(1)

    # ===== 4단계: 최종 결과 출력 및 저장 =====

    print("\n" + "=" * 70)
    print("최종 선정 기사")
    print("=" * 70)
    print(f"\n제목: {selected_article.title}")
    print(f"출처: {selected_article.source}")
    print(f"날짜: {selected_article.published_at.strftime('%Y년 %m월 %d일 %H:%M')}")
    print(f"본문 길이: {len(selected_article.content)}자")
    print(f"\n본문 미리보기:")
    print("-" * 70)
    print(selected_article.content[:400])
    print("...")
    print("-" * 70)

    # JSON 저장
    try:
        selected_article.save_to_json('./data/raw/selected_article.json')
        print(f"\n[저장완료] ./data/raw/selected_article.json")
    except Exception as e:
        print(f"[ERROR] 저장 실패: {e}")

    print("\n" + "=" * 70)
    print("작업 완료!")
    print("=" * 70)

# -*- coding: utf-8 -*-
"""
전체 아티클 생성 (쿠팡 파트너스 추천 포함)
"""
import json
from publishers.coupang_partners import CoupangPartners


def main():
    print("=" * 70)
    print("Full Article Generation with Coupang Recommendations")
    print("=" * 70)

    # 1. 분석된 기사 로드
    input_path = './data/processed/analyzed_article.json'

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        print(f"\n[OK] Article loaded")
        print(f"제목: {article_data.get('title', 'N/A')[:50]}...")
        print(f"키워드: {', '.join(article_data.get('keywords', [])[:5])}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_path}")
        return

    # 2. 쿠팡 파트너스 추천 생성
    print("\n[Step 1] Coupang Partners Recommendations")
    print("-" * 70)

    partners = CoupangPartners()
    print(f"파트너스 링크: {partners.partner_link}")
    print("\nGemini로 추천 생성 중...")

    recommendations = partners.analyze_and_recommend(article_data, max_items=1)

    if recommendations:
        print(f"\n[OK] {len(recommendations)}개 추천 생성:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. [{rec['category']}] {rec['hook_title']}")

        article_data['coupang_recommendations'] = recommendations
    else:
        print("[WARNING] 쿠팡 추천 생성 실패, 건너뜀")
        article_data['coupang_recommendations'] = []

    # 3. 대가성 문구 추가
    article_data['coupang_disclosure'] = partners.get_disclosure_text()

    # 4. 저장
    output_path = './data/processed/article_with_coupang.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Saved to: {output_path}")

    # 5. 요약 출력
    print("\n" + "=" * 70)
    print("Article Summary")
    print("=" * 70)
    print(f"제목: {article_data['title']}")
    print(f"요약: {article_data.get('summary', 'N/A')[:100]}...")
    print(f"키워드: {', '.join(article_data.get('keywords', []))}")
    print(f"\n쿠팡 추천 {len(recommendations)}개:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. [{rec['category']}] {rec['hook_title']}")
    print(f"\n대가성 문구: {article_data['coupang_disclosure']}")
    print("=" * 70)


if __name__ == '__main__':
    main()

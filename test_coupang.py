# -*- coding: utf-8 -*-
"""
쿠팡 파트너스 AI 추천 테스트

새로운 방식:
1. 뉴스 내용 분석 → Gemini로 관련 상품/카테고리 선정
2. Gemini로 후킹 가능한 강렬한 한 줄 타이틀 생성
3. 단일 파트너스 링크 적용 (https://link.coupang.com/a/cVz6PI)
4. 준수사항 문구 포함
"""
import json
from publishers.coupang_partners import CoupangPartners


def main():
    print("=" * 70)
    print("Spread Insight - Coupang Partners AI Test")
    print("=" * 70)

    json_path = './data/processed/article_with_terminology.json'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        print(f"\n[OK] Article loaded")
        print(f"제목: {article_data.get('title', 'N/A')}")
        print(f"키워드: {', '.join(article_data.get('keywords', [])[:5])}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_path}")
        return

    print("\n[Step 1] AI 기반 상품 추천 생성")
    print("-" * 70)
    partners = CoupangPartners()
    print(f"파트너스 링크: {partners.partner_link}")
    print(f"대가성 문구: {partners.get_disclosure_text()}")

    print("\nGemini로 추천 생성 중...")
    recommendations = partners.analyze_and_recommend(article_data, max_items=3)

    if not recommendations:
        print("[ERROR] 추천 생성 실패")
        return

    print(f"\n[OK] {len(recommendations)}개 추천 생성 완료:")
    print("-" * 70)
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.get('category', 'N/A')}")
        print(f"   후킹 타이틀: \"{rec.get('hook_title', 'N/A')}\"")
        print(f"   제휴 링크: {rec.get('affiliate_link', 'N/A')}")

    print("\n[Step 2] HTML 포맷팅 예시")
    print("-" * 70)
    for rec in recommendations[:1]:  # 첫 번째만 HTML 예시 출력
        html = partners.format_recommendation_html(rec)
        print(html)

    print("\n[Step 3] 기사 데이터에 추가")
    print("-" * 70)
    article_data['coupang_recommendations'] = recommendations

    output_path = './data/processed/article_with_coupang.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved to: {output_path}")

    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print("\n추천 요약:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. [{rec['category']}] {rec['hook_title']}")
    print(f"\n대가성 문구: {partners.get_disclosure_text()}")
    print("=" * 70)


if __name__ == '__main__':
    main()

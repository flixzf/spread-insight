# -*- coding: utf-8 -*-
"""
쿠팡 파트너스 준수사항 테스트

이 스크립트는 다음을 검증합니다:
1. 제휴 링크 생성이 올바른지
2. 대가성 문구가 포함되는지
3. HTML 출력이 준수사항을 만족하는지
"""

from publishers.coupang_partners import CoupangPartners


def test_disclosure_text():
    """대가성 문구 테스트"""
    print("=" * 70)
    print("Test 1: 대가성 문구 확인")
    print("=" * 70)

    partners = CoupangPartners()

    # 기본 대가성 문구 확인
    disclosure = partners.get_disclosure_text()
    print(f"\n[대가성 문구]\n{disclosure}")

    # 필수 키워드 포함 여부 확인
    required_keywords = ["쿠팡 파트너스", "수수료"]
    all_present = all(keyword in disclosure for keyword in required_keywords)

    if all_present:
        print("\n[PASS] 필수 키워드가 모두 포함되어 있습니다.")
    else:
        print("\n[FAIL] 필수 키워드가 누락되었습니다.")

    return all_present


def test_disclosure_html():
    """대가성 문구 HTML 테스트"""
    print("\n" + "=" * 70)
    print("Test 2: 대가성 문구 HTML 출력")
    print("=" * 70)

    partners = CoupangPartners()
    html = partners.get_disclosure_html()

    print(f"\n[HTML 출력]\n{html}")

    # HTML 태그 확인
    has_p_tag = html.startswith('<p') and html.endswith('</p>')
    has_class = 'class=' in html

    if has_p_tag and has_class:
        print("\n[PASS] HTML 형식이 올바릅니다.")
    else:
        print("\n[FAIL] HTML 형식에 문제가 있습니다.")

    return has_p_tag and has_class


def test_affiliate_link_with_disclosure():
    """제휴 링크와 대가성 문구 통합 테스트"""
    print("\n" + "=" * 70)
    print("Test 3: 제휴 링크 + 대가성 문구 통합")
    print("=" * 70)

    partners = CoupangPartners(partner_id="test_partner")

    # 테스트 도서 데이터
    test_book = {
        'title': '파이썬 프로그래밍 입문',
        'author': '홍길동',
        'coupang_url': 'https://www.coupang.com/vp/products/123456789',
        'affiliate_link': ''
    }

    # 1. 제휴 링크 생성
    test_book['affiliate_link'] = partners.generate_link(
        test_book['coupang_url'],
        subid="test_article"
    )

    print(f"\n[도서 정보]")
    print(f"제목: {test_book['title']}")
    print(f"원본 URL: {test_book['coupang_url']}")
    print(f"제휴 링크: {test_book['affiliate_link']}")

    # 2. HTML 포맷팅 (대가성 문구 포함)
    html_with_disclosure = partners.format_book_link_html(test_book, include_disclosure=True)

    print(f"\n[HTML 출력 (대가성 문구 포함)]")
    print(html_with_disclosure)

    # 3. HTML 포맷팅 (대가성 문구 없음)
    html_without_disclosure = partners.format_book_link_html(test_book, include_disclosure=False)

    print(f"\n[HTML 출력 (대가성 문구 없음)]")
    print(html_without_disclosure)

    # 검증
    has_link = 'link.coupang.com' in test_book['affiliate_link']
    has_partner_tag = 'lptag=test_partner' in test_book['affiliate_link']
    has_disclosure_in_html = '쿠팡 파트너스' in html_with_disclosure
    no_disclosure_when_disabled = '쿠팡 파트너스' not in html_without_disclosure

    all_pass = has_link and has_partner_tag and has_disclosure_in_html and no_disclosure_when_disabled

    if all_pass:
        print("\n[PASS] 제휴 링크와 대가성 문구가 올바르게 생성되었습니다.")
    else:
        print("\n[FAIL] 일부 검증에 실패했습니다.")
        if not has_link:
            print("  - 제휴 링크 형식 오류")
        if not has_partner_tag:
            print("  - 파트너 태그 누락")
        if not has_disclosure_in_html:
            print("  - 대가성 문구 누락")
        if not no_disclosure_when_disabled:
            print("  - 대가성 문구 제거 실패")

    return all_pass


def test_multiple_books():
    """여러 도서 처리 테스트"""
    print("\n" + "=" * 70)
    print("Test 4: 여러 도서 제휴 링크 생성")
    print("=" * 70)

    partners = CoupangPartners(partner_id="test_partner")

    test_books = [
        {
            'title': '경제학 원론',
            'author': '김경제',
            'coupang_url': 'https://www.coupang.com/vp/products/111111111',
        },
        {
            'title': '투자의 기술',
            'author': '박투자',
            'coupang_url': 'https://www.coupang.com/vp/products/222222222',
        }
    ]

    # 제휴 링크 추가
    books_with_links = partners.add_affiliate_to_books(test_books, subid="multi_test")

    print(f"\n[처리 결과]")
    all_have_links = True
    for book in books_with_links:
        print(f"\n제목: {book['title']}")
        print(f"제휴 링크: {book['affiliate_link']}")

        if 'link.coupang.com' not in book['affiliate_link']:
            all_have_links = False

    if all_have_links:
        print("\n[PASS] 모든 도서에 제휴 링크가 생성되었습니다.")
    else:
        print("\n[FAIL] 일부 도서의 제휴 링크 생성에 실패했습니다.")

    return all_have_links


def main():
    """모든 테스트 실행"""
    print("\n")
    print("=" * 70)
    print("       쿠팡 파트너스 준수사항 테스트")
    print("=" * 70)

    results = []

    # 각 테스트 실행
    results.append(("대가성 문구 확인", test_disclosure_text()))
    results.append(("대가성 문구 HTML", test_disclosure_html()))
    results.append(("제휴 링크 + 대가성 문구", test_affiliate_link_with_disclosure()))
    results.append(("여러 도서 처리", test_multiple_books()))

    # 결과 요약
    print("\n" + "=" * 70)
    print("테스트 결과 요약")
    print("=" * 70)

    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 70)
    if all_passed:
        print("[SUCCESS] 모든 테스트를 통과했습니다!")
        print("\n쿠팡 파트너스 준수사항이 올바르게 구현되었습니다:")
        print("- 제휴 링크 생성")
        print("- 대가성 문구 포함")
        print("- HTML 출력 형식")
    else:
        print("[WARNING] 일부 테스트가 실패했습니다. 위의 결과를 확인하세요.")
    print("=" * 70)


if __name__ == '__main__':
    main()

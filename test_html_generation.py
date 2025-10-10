"""
HTML 생성 테스트
article_with_terminology.json을 읽어 HTML 페이지 생성
"""

from generators.html_generator import HTMLGenerator
import json


if __name__ == '__main__':
    print("=" * 70)
    print("Spread Insight - HTML 생성 테스트")
    print("=" * 70)

    # HTML 생성기 초기화
    generator = HTMLGenerator(template_dir='./templates')

    # 테스트할 JSON 파일 경로
    json_path = './data/processed/article_with_coupang.json'
    output_path = './output/article_latest.html'

    try:
        # JSON 읽기
        print(f"\n[1단계] JSON 파일 읽기: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        print(f"[OK] 제목: {article_data.get('title', 'N/A')}")

        # HTML 생성
        print(f"\n[2단계] HTML 생성 중...")
        generator.generate_from_article(article_data, output_path)

        print(f"\n[3단계] 생성 완료!")
        print(f"[+] 출력 파일: {output_path}")
        print(f"[+] 브라우저에서 열어보세요!")

        # 간단한 통계
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"\n[통계]")
        print(f"  - HTML 크기: {len(html_content):,}자")
        print(f"  - 키워드 수: {len(article_data.get('keywords', []))}개")
        print(f"  - 용어 설명 수: {len(article_data.get('terminology', {}))}개")

    except FileNotFoundError:
        print(f"[ERROR] 파일을 찾을 수 없습니다: {json_path}")
        print("[!] test_terminology.py를 먼저 실행하세요.")
        exit(1)
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    print("\n" + "=" * 70)
    print("작업 완료!")
    print("=" * 70)

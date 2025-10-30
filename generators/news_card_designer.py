# -*- coding: utf-8 -*-
"""
뉴스 카드 디자이너 (Pillow 기반)

배경 이미지 + 텍스트 오버레이로 Instagram/LinkedIn 스타일 카드 생성
"""

import os
import platform
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from typing import List, Tuple, Optional


class NewsCardDesigner:
    """Pillow 기반 뉴스 카드 생성"""

    def __init__(self, output_dir: str = "./data/cards"):
        """
        Args:
            output_dir: 카드 이미지 저장 경로
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 카드 크기 (Instagram 정사각형)
        self.card_size = (1080, 1080)

        # 폰트 설정 (OS별 자동 감지)
        self.font_paths = self._get_font_paths()

    def _get_font_paths(self) -> dict:
        """
        OS별 한글 폰트 경로 자동 감지

        Returns:
            폰트 경로 딕셔너리 {'bold': path, 'regular': path}
        """
        system = platform.system()

        if system == 'Windows':
            return {
                'bold': 'C:/Windows/Fonts/malgunbd.ttf',
                'regular': 'C:/Windows/Fonts/malgun.ttf'
            }
        elif system == 'Linux':
            # Ubuntu/Debian 계열 (Railway 서버)
            # Nanum 폰트는 대부분의 Linux에 기본 설치되어 있음
            return {
                'bold': '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
                'regular': '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
            }
        elif system == 'Darwin':  # macOS
            return {
                'bold': '/System/Library/Fonts/AppleSDGothicNeo.ttc',
                'regular': '/System/Library/Fonts/AppleSDGothicNeo.ttc'
            }
        else:
            # 알 수 없는 OS - 빈 경로 반환 (기본 폰트 사용)
            return {
                'bold': '',
                'regular': ''
            }

    def get_background_image(self, keyword: str = "economy") -> Image.Image:
        """
        Unsplash에서 배경 이미지 가져오기

        Args:
            keyword: 검색 키워드

        Returns:
            PIL Image 객체
        """
        # Unsplash Source API (무료, API 키 불필요)
        url = f"https://source.unsplash.com/1080x1080/?{keyword},business,finance"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            return img.resize(self.card_size)
        except Exception as e:
            print(f"[WARNING] Unsplash 이미지 로드 실패: {e}")
            # 폴백: 단색 그라디언트 배경
            return self._create_gradient_background()

    def _create_gradient_background(
        self,
        color1: Tuple[int, int, int] = (67, 198, 172),  # 청록색
        color2: Tuple[int, int, int] = (248, 255, 174)   # 연노랑
    ) -> Image.Image:
        """
        그라디언트 배경 생성

        Returns:
            PIL Image 객체
        """
        base = Image.new('RGB', self.card_size, color1)
        top = Image.new('RGB', self.card_size, color2)

        # 그라디언트 마스크
        mask = Image.new('L', self.card_size)
        mask_draw = ImageDraw.Draw(mask)
        for y in range(self.card_size[1]):
            alpha = int(255 * (y / self.card_size[1]))
            mask_draw.rectangle([(0, y), (self.card_size[0], y + 1)], fill=alpha)

        base.paste(top, (0, 0), mask)
        return base

    def add_dark_overlay(self, img: Image.Image, opacity: int = 128) -> Image.Image:
        """
        이미지에 어두운 오버레이 추가 (텍스트 가독성 향상)

        Args:
            img: 원본 이미지
            opacity: 투명도 (0-255)

        Returns:
            오버레이가 추가된 이미지
        """
        overlay = Image.new('RGBA', img.size, (0, 0, 0, opacity))
        img = img.convert('RGBA')
        return Image.alpha_composite(img, overlay)

    def create_main_card(
        self,
        title: str,
        keywords: List[str],
        bg_keyword: str = "economy"
    ) -> str:
        """
        메인 카드 생성

        Args:
            title: 뉴스 제목
            keywords: 키워드 리스트
            bg_keyword: 배경 이미지 검색어

        Returns:
            저장된 카드 이미지 경로
        """
        # 배경 이미지
        bg = self.get_background_image(bg_keyword)

        # 어두운 오버레이 (가독성)
        bg = self.add_dark_overlay(bg, opacity=140)

        # 텍스트 추가
        draw = ImageDraw.Draw(bg)

        # 제목 폰트 (크고 굵게)
        try:
            title_font = ImageFont.truetype(self.font_paths['bold'], 72)
        except (IOError, OSError):
            title_font = ImageFont.load_default()

        # 키워드 폰트 (작고 가볍게)
        try:
            keyword_font = ImageFont.truetype(self.font_paths['regular'], 36)
        except (IOError, OSError):
            keyword_font = ImageFont.load_default()

        # 제목 그리기 (여러 줄 지원)
        title_lines = self._wrap_text(title, title_font, max_width=900)
        y_offset = 300

        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.card_size[0] - text_width) // 2
            draw.text((x, y_offset), line, fill='white', font=title_font)
            y_offset += 90

        # 키워드 그리기
        y_offset += 60
        keyword_text = " ".join([f"#{kw}" for kw in keywords[:3]])
        bbox = draw.textbbox((0, 0), keyword_text, font=keyword_font)
        text_width = bbox[2] - bbox[0]
        x = (self.card_size[0] - text_width) // 2
        draw.text((x, y_offset), keyword_text, fill='#FFD700', font=keyword_font)

        # 저장
        output_path = os.path.join(self.output_dir, "card_main.png")
        bg = bg.convert('RGB')
        bg.save(output_path, quality=95)

        return output_path

    def create_content_card(
        self,
        title: str,
        content: str,
        card_number: int = 1,
        total_cards: int = 4,
        bg_color: Tuple[int, int, int] = (67, 198, 172)
    ) -> str:
        """
        콘텐츠 카드 생성

        Args:
            title: 섹션 제목
            content: 섹션 내용
            card_number: 카드 번호
            total_cards: 전체 카드 수
            bg_color: 배경색

        Returns:
            저장된 카드 이미지 경로
        """
        # 그라디언트 배경
        bg = self._create_gradient_background(color1=bg_color, color2=(255, 255, 255))

        draw = ImageDraw.Draw(bg)

        # 폰트
        try:
            title_font = ImageFont.truetype(self.font_paths['bold'], 56)
            content_font = ImageFont.truetype(self.font_paths['regular'], 36)
            number_font = ImageFont.truetype(self.font_paths['bold'], 32)
        except (IOError, OSError):
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # 카드 번호 (우측 상단)
        number_text = f"{card_number}/{total_cards}"
        draw.text((920, 60), number_text, fill='white', font=number_font)

        # 제목
        y_offset = 200
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.card_size[0] - text_width) // 2
        draw.text((x, y_offset), title, fill='#333333', font=title_font)

        # 구분선
        y_offset += 100
        line_width = 400
        x_start = (self.card_size[0] - line_width) // 2
        draw.rectangle(
            [(x_start, y_offset), (x_start + line_width, y_offset + 4)],
            fill='#666666'
        )

        # 내용 (여러 줄)
        y_offset += 60
        content_lines = self._wrap_text(content, content_font, max_width=900)

        for line in content_lines[:8]:  # 최대 8줄
            bbox = draw.textbbox((0, 0), line, font=content_font)
            text_width = bbox[2] - bbox[0]
            x = (self.card_size[0] - text_width) // 2
            draw.text((x, y_offset), line, fill='#555555', font=content_font)
            y_offset += 50

        # 저장
        output_path = os.path.join(self.output_dir, f"card_{card_number}.png")
        bg.save(output_path, quality=95)

        return output_path

    def _wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int
    ) -> List[str]:
        """
        텍스트를 최대 너비에 맞춰 여러 줄로 나누기

        Returns:
            줄 리스트
        """
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

    def generate_full_card_set(self, article_data: dict) -> List[str]:
        """
        전체 카드 세트 생성

        Args:
            article_data: 분석된 기사 데이터

        Returns:
            생성된 카드 이미지 경로 리스트
        """
        card_paths = []

        # 1. 메인 카드
        print("\n[1/5] 메인 카드 생성 중...")
        main_card = self.create_main_card(
            title=article_data.get('title', ''),
            keywords=article_data.get('keywords', []),
            bg_keyword=article_data.get('keywords', ['economy'])[0]
        )
        card_paths.append(main_card)

        # 2-5. 콘텐츠 카드
        sections = self._extract_content_sections(article_data)
        colors = [
            (67, 198, 172),   # 청록
            (255, 183, 77),   # 오렌지
            (129, 212, 250),  # 하늘색
            (174, 213, 129)   # 연두색
        ]

        for i, (section_title, section_content) in enumerate(sections, 1):
            print(f"\n[{i+1}/5] '{section_title}' 카드 생성 중...")
            card_path = self.create_content_card(
                title=section_title,
                content=section_content,
                card_number=i,
                total_cards=len(sections),
                bg_color=colors[i-1] if i <= len(colors) else (200, 200, 200)
            )
            card_paths.append(card_path)

        return card_paths

    def _extract_content_sections(self, article_data: dict) -> List[Tuple[str, str]]:
        """기사 데이터에서 카드용 섹션 추출"""
        sections = []

        # expert_opinion 또는 easy_explanation 필드에서 가져오기
        analysis = article_data.get('expert_opinion') or article_data.get('easy_explanation', '')

        if analysis:
            # 단락별로 분리 (번호로 시작하는 섹션)
            parts = [p.strip() for p in analysis.split('\n\n') if p.strip()]

            # 각 섹션 제목 추출 또는 기본 제목 사용
            for i, part in enumerate(parts):
                # "1. 현재 상황:" 같은 패턴에서 제목 추출
                if part.startswith(f"{i+1}."):
                    # 첫 줄에서 제목 추출
                    lines = part.split('\n', 1)
                    first_line = lines[0]
                    # "1. 현재 상황:" -> "현재 상황"
                    if ':' in first_line:
                        title = first_line.split(':', 1)[0].split('.', 1)[1].strip()
                    else:
                        title = first_line.split('.', 1)[1].strip()
                    content = lines[1] if len(lines) > 1 else part
                else:
                    # 기본 제목
                    default_titles = ["현재 상황", "투자 영향", "시장 관점", "분석"]
                    title = default_titles[i] if i < len(default_titles) else f"분석 {i+1}"
                    content = part

                sections.append((title, content))

        # 쿠팡 파트너스 추천
        coupang_recs = article_data.get('coupang_recommendations', [])
        if coupang_recs:
            rec = coupang_recs[0]
            coupang_text = rec.get('hook_title', '') or rec.get('title', '')
            sections.append(("쿠팡 추천", coupang_text))

        return sections


if __name__ == '__main__':
    # 테스트
    designer = NewsCardDesigner()

    test_data = {
        'title': '美 고율 관세에 포스코·현대제철 4000억원 폭탄',
        'keywords': ['관세', '철강', '무역'],
        'expert_opinion': '''1. 현재 상황: 우리나라 대표 철강 업체인 포스코와 현대제철이 미국에 수출하는 철강 제품에 대해 관세가 올라 타격을 받고 있습니다.

2. 과거 사례: 과거에도 미국은 자국 산업 보호를 위해 특정 국가 제품에 관세를 인상한 적이 있습니다.

3. 투자 영향 분석: 포스코와 현대제철 같은 철강 업체 주식은 단기적으로 하락 압력을 받을 수 있습니다.''',
        'coupang_recommendations': [
            {'title': '철강 공구 세트 - 가정용 필수품'}
        ]
    }

    print("=" * 70)
    print("News Card Designer Test")
    print("=" * 70)

    cards = designer.generate_full_card_set(test_data)

    print("\n" + "=" * 70)
    print("생성된 카드:")
    print("=" * 70)
    for card_path in cards:
        print(f"✅ {card_path}")

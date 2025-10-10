# -*- coding: utf-8 -*-
"""
간단한 타이틀 카드 생성기 (Pillow + DALL-E)

제목 + 키워드만 담은 타이틀 이미지 1장만 생성
배경은 DALL-E로 생성
"""

import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import List
from openai import OpenAI
from utils.config import Config


class SimpleCardGenerator:
    """타이틀 카드만 생성하는 간단한 생성기"""

    def __init__(self, output_dir: str = "./data/cards"):
        """
        Args:
            output_dir: 카드 이미지 저장 경로
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 카드 크기 (Instagram 정사각형)
        self.card_size = (1080, 1080)

        # 폰트 설정
        self.font_paths = {
            'bold': 'C:/Windows/Fonts/malgunbd.ttf',
            'regular': 'C:/Windows/Fonts/malgun.ttf'
        }

        # OpenAI 클라이언트
        self.openai_client = None
        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def _generate_dalle_background(self, title: str, keywords: List[str]) -> Image.Image:
        """
        DALL-E로 배경 이미지 생성

        Args:
            title: 뉴스 제목
            keywords: 뉴스 키워드 리스트

        Returns:
            PIL Image 객체
        """
        if not self.openai_client:
            print("[Warning] OpenAI API key not set, using gradient background")
            return self._create_gradient_background()

        try:
            # 제목 + 키워드 기반 프롬프트 생성
            # 키워드를 구체적인 비주얼 요소로 변환
            keyword_text = ", ".join(keywords[:3])

            prompt = f"""Photorealistic image of business professionals in a modern corporate office discussing {keyword_text}.
Scene: executives analyzing economic data on large monitors, financial charts and graphs visible in background.
Setting: sleek modern office with glass walls, contemporary furniture, professional lighting.
People: diverse business team in professional attire, engaged in serious discussion.
Camera: professional photography, shallow depth of field, cinematic lighting, high quality corporate photography.
Style: realistic, professional stock photo aesthetic, vibrant but natural colors.
Important: NO TEXT or LETTERS visible anywhere in the image."""

            print(f"   DALL-E 프롬프트: {prompt[:100]}...")

            # DALL-E 이미지 생성
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # 이미지 다운로드
            image_url = response.data[0].url
            print(f"   [OK] DALL-E 이미지 생성 완료")

            image_response = requests.get(image_url)
            image_response.raise_for_status()

            img = Image.open(BytesIO(image_response.content))

            # 1080x1080으로 리사이즈
            img = img.resize(self.card_size, Image.Resampling.LANCZOS)

            return img

        except Exception as e:
            print(f"   [Warning] DALL-E 생성 실패: {e}")
            print("   그라데이션 배경 사용")
            return self._create_gradient_background()

    def _create_gradient_background(self) -> Image.Image:
        """그라데이션 배경 생성 (파란색 -> 보라색) - Fallback"""
        img = Image.new('RGB', self.card_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 그라데이션 색상
        color_start = (59, 130, 246)   # 파란색
        color_end = (147, 51, 234)     # 보라색

        for y in range(self.card_size[1]):
            ratio = y / self.card_size[1]
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)

            draw.rectangle([(0, y), (self.card_size[0], y + 1)], fill=(r, g, b))

        return img

    def create_title_card(self, title: str, keywords: List[str]) -> str:
        """
        타이틀 카드 생성

        Args:
            title: 뉴스 제목
            keywords: 키워드 리스트

        Returns:
            생성된 이미지 파일 경로
        """
        # 배경 이미지 (DALL-E)
        print("   배경 이미지 생성 중...")
        img = self._generate_dalle_background(title, keywords)

        # RGBA로 변환 (투명도 작업용)
        img = img.convert('RGBA')

        # 폰트 로드
        try:
            title_font = ImageFont.truetype(self.font_paths['bold'], 60)
            keyword_font = ImageFont.truetype(self.font_paths['regular'], 32)
        except:
            title_font = ImageFont.load_default()
            keyword_font = ImageFont.load_default()

        # 텍스트 영역 (중앙 정렬)
        padding = 80
        text_area_width = self.card_size[0] - (padding * 2)

        # 임시 draw로 제목 크기 계산
        temp_draw = ImageDraw.Draw(img)
        title_lines = self._wrap_text(title, title_font, text_area_width, temp_draw)

        # 제목 영역 크기 계산
        title_height = len(title_lines) * 80 + 40  # 각 줄 높이 + 여유
        title_y_start = 280
        title_y_end = title_y_start + title_height

        # 제목 배경 박스 (반투명 검은색)
        title_bg = Image.new('RGBA', self.card_size, (0, 0, 0, 0))
        title_bg_draw = ImageDraw.Draw(title_bg)
        title_bg_draw.rounded_rectangle(
            [60, title_y_start, self.card_size[0] - 60, title_y_end],
            radius=20,
            fill=(0, 0, 0, 180)  # 반투명 검은색
        )
        img = Image.alpha_composite(img, title_bg)

        # 이제 텍스트 그리기
        draw = ImageDraw.Draw(img)

        # 제목 그리기 (중앙)
        y_offset = 300
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.card_size[0] - text_width) // 2

            # 실제 텍스트 (흰색)
            draw.text((x, y_offset), line, font=title_font, fill=(255, 255, 255))

            y_offset += 80

        # 키워드 태그 그리기 (중앙 정렬, 반투명 배경)
        img = self._draw_centered_tags(img, keywords[:5], keyword_font)

        # RGB로 변환 후 저장
        img = img.convert('RGB')
        output_path = os.path.join(self.output_dir, "title_card.png")
        img.save(output_path, quality=95)

        return output_path

    def _draw_centered_tags(self, img: Image.Image, keywords: List[str], font: ImageFont.FreeTypeFont) -> Image.Image:
        """키워드 태그를 중앙 정렬로 그리기 (반투명 배경 포함)"""
        y_offset = 780
        tag_spacing = 20

        # 임시 draw로 크기 계산
        temp_draw = ImageDraw.Draw(img)

        # 전체 태그 너비 계산
        total_width = 0
        tag_widths = []
        for keyword in keywords:
            tag_text = f"#{keyword}"
            bbox = temp_draw.textbbox((0, 0), tag_text, font=font)
            width = bbox[2] - bbox[0]
            tag_widths.append(width)
            total_width += width

        total_width += tag_spacing * (len(keywords) - 1)

        # 태그 영역 배경 박스 (반투명 검은색)
        tag_height = 50
        tag_bg = Image.new('RGBA', self.card_size, (0, 0, 0, 0))
        tag_bg_draw = ImageDraw.Draw(tag_bg)
        tag_bg_draw.rounded_rectangle(
            [(self.card_size[0] - total_width) // 2 - 20, y_offset - 10,
             (self.card_size[0] + total_width) // 2 + 20, y_offset + tag_height],
            radius=15,
            fill=(0, 0, 0, 180)  # 반투명 검은색
        )
        img = Image.alpha_composite(img, tag_bg)

        # 태그 텍스트 그리기
        draw = ImageDraw.Draw(img)
        x_offset = (self.card_size[0] - total_width) // 2

        for i, keyword in enumerate(keywords):
            tag_text = f"#{keyword}"

            # 실제 텍스트 (흰색)
            draw.text((x_offset, y_offset), tag_text, font=font, fill=(255, 255, 255))

            x_offset += tag_widths[i] + tag_spacing

        return img

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """텍스트 자동 줄바꿈"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            bbox = draw.textbbox((0, 0), test_line, font=font)
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


if __name__ == "__main__":
    # 테스트
    generator = SimpleCardGenerator()

    test_title = "미국 금리 인하 전망, 국내 증시에 미치는 영향은?"
    test_keywords = ["금리인하", "미국경제", "증시전망", "투자전략"]

    card_path = generator.create_title_card(test_title, test_keywords)
    print(f"타이틀 카드 생성: {card_path}")

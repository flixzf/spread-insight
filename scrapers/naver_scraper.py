import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper
from models.news_article import NewsArticle


class NaverScraper(BaseScraper):
    """네이버 뉴스 스크래퍼"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape_article(self, url: str) -> NewsArticle:
        """네이버 뉴스 기사 상세 정보 추출"""
        try:
            # 페이지 요청
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            # HTML 파싱 (html.parser 사용)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 제목 추출
            title_elem = soup.select_one('#title_area span, #articleTitle, h2.media_end_head_headline')
            if not title_elem:
                raise ValueError("제목을 찾을 수 없습니다.")
            title = title_elem.get_text(strip=True)

            # 본문 추출
            content_elem = soup.select('#dic_area, #articeBody, #newsct_article')
            if not content_elem:
                raise ValueError("본문을 찾을 수 없습니다.")

            # 본문 내 모든 텍스트 추출 (광고 제거)
            paragraphs = []
            for elem in content_elem:
                # script, style 태그 제거
                for tag in elem.find_all(['script', 'style', 'iframe']):
                    tag.decompose()

                # 텍스트 추출
                text = elem.get_text(separator='\n', strip=True)
                if text:
                    paragraphs.append(text)

            content = '\n\n'.join(paragraphs)

            if not content or len(content) < 50:
                raise ValueError("본문 내용이 너무 짧습니다.")

            # 날짜 추출
            date_elem = soup.select_one('.media_end_head_info_datestamp_time, .author_info em, span.t11')
            if date_elem:
                date_str = date_elem.get('data-date-time') or date_elem.get_text(strip=True)

                # 여러 날짜 포맷 시도
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y.%m.%d. %H:%M', '%Y.%m.%d %H:%M']:
                    try:
                        published_at = datetime.strptime(date_str.replace('오전', '').replace('오후', '').strip(), fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # ISO 포맷 시도
                    try:
                        published_at = datetime.fromisoformat(date_str)
                    except (ValueError, TypeError):
                        published_at = datetime.now()  # 파싱 실패 시 현재 시간
            else:
                published_at = datetime.now()

            return NewsArticle(
                url=url,
                title=title,
                content=content,
                published_at=published_at,
                source='네이버'
            )

        except requests.RequestException as e:
            raise Exception(f"네트워크 오류: {e}")
        except Exception as e:
            raise Exception(f"파싱 오류: {e}")

    def get_article_metadata(self, category_url: str = 'https://news.naver.com/section/101', limit: int = 30) -> list[dict]:
        """네이버 경제 섹션에서 기사 메타데이터(제목+요약+URL)만 빠르게 추출 - AI 선택용"""
        try:
            response = requests.get(category_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            articles_metadata = []

            # 섹션별 기사 리스트 추출
            for item in soup.select('.sa_item, .sa_item_inner'):
                # 제목과 링크
                title_elem = item.select_one('.sa_text_title, .sa_text_strong')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                url = title_elem.get('href', '')

                if not url or 'news.naver.com' not in url:
                    continue

                # 요약 (lede)
                summary_elem = item.select_one('.sa_text_lede')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""

                articles_metadata.append({
                    'url': url,
                    'title': title,
                    'summary': summary
                })

                if len(articles_metadata) >= limit:
                    break

            return articles_metadata

        except Exception as e:
            raise Exception(f"메타데이터 수집 오류: {e}")

    def get_article_list(self, category_url: str = 'https://news.naver.com/section/101', limit: int = 10) -> list[str]:
        """네이버 경제 섹션에서 기사 URL 리스트 추출"""
        try:
            response = requests.get(category_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 기사 링크 추출 (네이버 뉴스 구조에 따라 선택자 조정 필요)
            article_links = []

            # 방법 1: sa_text 클래스 (데스크톱)
            for link in soup.select('.sa_text_title'):
                href = link.get('href')
                if href and href.startswith('http') and 'news.naver.com' in href:
                    article_links.append(href)

            # 방법 2: 리스트 형식
            for link in soup.select('a.news_tit'):
                href = link.get('href')
                if href and href.startswith('http'):
                    article_links.append(href)

            # 중복 제거
            article_links = list(dict.fromkeys(article_links))

            return article_links[:limit]

        except Exception as e:
            raise Exception(f"목록 수집 오류: {e}")

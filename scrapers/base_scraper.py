from abc import ABC, abstractmethod
from models.news_article import NewsArticle


class BaseScraper(ABC):
    """모든 스크래퍼의 추상 클래스"""

    @abstractmethod
    def scrape_article(self, url: str) -> NewsArticle:
        """단일 기사 스크래핑"""
        pass

    @abstractmethod
    def get_article_list(self, category_url: str, limit: int = 10) -> list[str]:
        """기사 URL 리스트 수집"""
        pass

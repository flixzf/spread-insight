from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class NewsArticle:
    """뉴스 기사 데이터 모델"""
    url: str
    title: str
    content: str
    published_at: datetime
    source: str
    keywords: Optional[list[str]] = None
    summary: Optional[str] = None
    easy_explanation: Optional[str] = None
    terminology: Optional[dict[str, str]] = None

    def to_dict(self) -> dict:
        """datetime을 ISO 포맷 문자열로 변환"""
        data = asdict(self)
        data['published_at'] = self.published_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'NewsArticle':
        """딕셔너리에서 객체 복원"""
        data['published_at'] = datetime.fromisoformat(data['published_at'])
        return cls(**data)

    def save_to_json(self, filepath: str):
        """JSON 파일로 저장"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str) -> 'NewsArticle':
        """JSON 파일에서 로드"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __str__(self):
        return f"[{self.source}] {self.title} ({self.published_at.strftime('%Y-%m-%d')})"

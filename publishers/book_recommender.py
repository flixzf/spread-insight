# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import List, Dict


class BookRecommender:
    def __init__(self, books_db_path: str = './data/recommended_books.json'):
        self.books_db_path = Path(books_db_path)
        self.books_db = self._load_books()

    def _load_books(self) -> Dict:
        try:
            with open(self.books_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[WARNING] Books DB not found: {self.books_db_path}")
            return {}

    def recommend(self, article_data: dict, max_books: int = 2) -> List[Dict]:
        keywords = article_data.get('keywords', [])
        title = article_data.get('title', '')
        content = article_data.get('content', '')
        
        all_text = f"{title} {' '.join(keywords)} {content}".lower()
        
        scored_books = []
        
        for category, books in self.books_db.items():
            for book in books:
                score = self._calculate_score(book, all_text, keywords)
                if score > 0:
                    book_copy = book.copy()
                    book_copy['score'] = score
                    book_copy['category'] = category
                    scored_books.append(book_copy)
        
        scored_books.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_books[:max_books]

    def _calculate_score(self, book: Dict, text: str, keywords: List[str]) -> int:
        score = 0
        book_keywords = book.get('keywords', [])
        
        for kw in book_keywords:
            kw_lower = kw.lower()
            if kw_lower in text:
                score += 10
            
            for article_kw in keywords:
                if kw_lower in article_kw.lower() or article_kw.lower() in kw_lower:
                    score += 20
        
        return score


if __name__ == '__main__':
    recommender = BookRecommender()
    
    test_article = {
        'title': 'Bread inflation',
        'keywords': ['inflation', 'price', 'CPI'],
        'content': 'Consumer price index rising...'
    }
    
    books = recommender.recommend(test_article, max_books=2)
    
    print(f"Recommended {len(books)} books:")
    for book in books:
        print(f"  - {book['title']} (score: {book['score']})")

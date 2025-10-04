from typing import List, Dict, Any
import httpx
from fastapi import HTTPException
from src.config import settings

class GoogleSearchService:
    def __init__(self):
        # Використовуємо наданий API ключ напряму
        self.api_key = "a99dd6ed78f093b7f484ba4c3f754d39513ddc8b371b5c6f15430c4171a87278"
        self.base_url = "https://serpapi.com/search.json"

    async def search_preply_reputation(self) -> List[Dict[Any, Any]]:
        """
        Виконує пошук інформації про репутацію Preply
        
        Returns:
            List[Dict]: Список результатів пошуку
        """
        params = {
            'api_key': self.api_key,
            'q': "Preply reviews reputation problems issues",
            'num': 10,  # Кількість результатів
            'engine': 'google'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            search_results = []
            
            # Збираємо органічні результати
            if 'organic_results' in data:
                for item in data['organic_results']:
                    result = {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google_search'
                    }
                    search_results.append(result)
            
            # Додаємо результати з featured snippets якщо є
            if 'answer_box' in data:
                answer = data['answer_box']
                result = {
                    'title': answer.get('title', ''),
                    'content': answer.get('snippet', ''),
                    'source': 'answer_box'
                }
                search_results.append(result)
            
            return search_results

    async def get_page_content(self, url: str) -> str:
        """
        Отримує контент сторінки за URL
        
        Args:
            url: URL сторінки
            
        Returns:
            str: Текстовий контент сторінки
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
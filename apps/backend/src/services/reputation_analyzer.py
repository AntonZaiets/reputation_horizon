from typing import Dict, List, Any
from src.services.openai_service import OpenAIService

class ReputationAnalyzer:
    def __init__(self):
        self.openai_service = OpenAIService()

    async def analyze_preply_reputation(self, search_results: List[Dict[Any, Any]]) -> Dict[str, Any]:
        """
        Аналізує репутацію Preply на основі результатів пошуку
        
        Args:
            search_results: Результати пошуку з Google
            
        Returns:
            Dict: Результат аналізу репутації
        """
        # Підготовка контексту для OpenAI
        context = "Analyze Preply's reputation based on the following search results:\n\n"
        
        for result in search_results:
            if result['source'] == 'answer_box':
                context += f"Featured Answer:\n{result['content']}\n\n"
            else:
                context += f"Title: {result['title']}\n"
                context += f"Snippet: {result['snippet']}\n\n"

        # New concise, structured API prompt for OpenAI
        prompt = f"""Analyze the reputation of Preply based on the provided sources. Return a concise JSON response in English with:\n\n1. Overall reputation score (X/10) with single-sentence rationale\n2. Top 2-3 key strengths with impact level (High/Medium/Low)\n3. Top 2-3 critical issues with severity (High/Medium/Low) and brief explanation why it's critical\n4. Risk assessment: overall business impact, 2-3 main risks with likelihood and consequence\n5. 2-3 priority actions with urgency and expected impact\n6. Total number of data sources used (integer only)\n\nFormat strictly as:\njson{{\n  \"overall_score\": {{\n    \"rating\": \"X/10\",\n    \"brief_reason\": \"...\"\n  }},\n  \"key_strengths\": [ ... ],\n  \"critical_issues\": [ ... ],\n  \"risk_assessment\": {{ ... }},\n  \"priority_actions\": [ ... ],\n  \"data_sources\": N\n}}\n\nAll output must be in English only. Do not include explanations, only the JSON object. Keep total response under 500 words.\n\nSources:\n{context}\n"""

        # Отримання відповіді від OpenAI
        response = await self.openai_service.get_completion(prompt)

        # Парсинг та структурування відповіді
        return {
            "company": "Preply",
            "analysis": response,
            "source": "openai_analysis",
            "raw_data": search_results,
            "analysis_timestamp": "utc_timestamp"
        }
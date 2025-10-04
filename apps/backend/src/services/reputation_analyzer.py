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

        # Промпт для аналізу репутації
        prompt = f"""Based on the provided information, analyze Preply's reputation and identify potential issues. 
        Please provide a detailed analysis in the following format:

        1. Overall Reputation Score (1-10)
        2. Main Strengths:
           - List key positive aspects
        3. Main Issues:
           - List identified problems or concerns
        4. Risk Assessment:
           - Evaluate severity of identified issues
           - Assess potential impact on business
        5. Recommendations:
           - Suggest specific improvements
           - Propose solutions for identified issues

        Context:
        {context}

        Please be objective and thorough in your analysis, considering both positive and negative aspects.
        """

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
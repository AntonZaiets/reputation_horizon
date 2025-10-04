from fastapi import APIRouter, HTTPException
from src.services.google_search import GoogleSearchService
from src.services.reputation_analyzer import ReputationAnalyzer
from typing import Dict, Any

router = APIRouter(prefix="/api/reputation", tags=["reputation"])
google_search = GoogleSearchService()
reputation_analyzer = ReputationAnalyzer()

@router.get("/analyze/preply")
async def analyze_preply_reputation() -> Dict[str, Any]:
    """
    Аналізує репутацію Preply на основі результатів пошуку Google та аналізу OpenAI
    
    Returns:
        Dict: Результат аналізу репутації
    """
    try:
        # Отримуємо результати пошуку
        search_results = await google_search.search_preply_reputation()
        
        if not search_results:
            raise HTTPException(
                status_code=404,
                detail="No search results found for Preply"
            )
        
        # Аналізуємо репутацію
        analysis = await reputation_analyzer.analyze_preply_reputation(search_results)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing reputation: {str(e)}"
        )
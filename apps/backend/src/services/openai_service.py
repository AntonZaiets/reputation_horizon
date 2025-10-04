"""OpenAI service for reputation analysis."""

import json
import logging
from typing import List, Dict, Any

import openai
from openai import AsyncOpenAI

from src.config import settings
from src.models import (
    AppReview, 
    SentimentAnalysis, 
    IntentClassification, 
    TopicExtraction,
    ReputationInsight,
    ReputationScore,
    PriorityIssue
)

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API interactions for reputation analysis."""

    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set in environment")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def analyze_review(self, review: AppReview) -> ReputationInsight:
        """
        Analyze a single review using OpenAI.
        
        Args:
            review: The review to analyze
            
        Returns:
            ReputationInsight with AI analysis
        """
        if not self.client:
            return self._get_mock_insight(review)

        try:
            # Prepare the review text for analysis
            review_text = f"Rating: {review.rating}/5\n"
            if review.title:
                review_text += f"Title: {review.title}\n"
            review_text += f"Content: {review.content}\n"
            review_text += f"Source: {review.source}\n"
            if review.app_version:
                review_text += f"App Version: {review.app_version}"

            # Create the analysis prompt
            prompt = self._create_analysis_prompt(review_text)
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert reputation analyst specializing in app reviews. Analyze reviews in Ukrainian and English."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )

            # Parse the response
            analysis_data = json.loads(response.choices[0].message.content)
            
            return ReputationInsight(
                review_id=review.id,
                sentiment=SentimentAnalysis(**analysis_data["sentiment"]),
                intent=IntentClassification(**analysis_data["intent"]),
                topics=TopicExtraction(**analysis_data["topics"]),
                priority_score=analysis_data["priority_score"],
                recommended_action=analysis_data["recommended_action"]
            )

        except Exception as e:
            logger.error(f"Error analyzing review {review.id}: {e}")
            return self._get_mock_insight(review)

    async def analyze_reputation_batch(self, reviews: List[AppReview]) -> Dict[str, Any]:
        """
        Analyze a batch of reviews and generate overall reputation insights.
        
        Args:
            reviews: List of reviews to analyze
            
        Returns:
            Dictionary with reputation analysis results
        """
        if not self.client or not reviews:
            return self._get_mock_batch_analysis(reviews)

        try:
            # Analyze individual reviews
            insights = []
            for review in reviews:
                insight = await self.analyze_review(review)
                insights.append(insight)

            # Generate overall reputation analysis
            reputation_analysis = await self._generate_reputation_analysis(reviews, insights)
            
            return {
                "insights": insights,
                "reputation_score": reputation_analysis["reputation_score"],
                "priority_issues": reputation_analysis["priority_issues"]
            }

        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            return self._get_mock_batch_analysis(reviews)

    def _create_analysis_prompt(self, review_text: str) -> str:
        """Create the prompt for review analysis."""
        return f"""
Проаналізуй цей відгук про мобільний додаток для вивчення мов (Preply) та надай детальний аналіз у JSON форматі.

Відгук:
{review_text}

Надай аналіз у наступному JSON форматі:
{{
    "sentiment": {{
        "sentiment": "positive|negative|neutral",
        "confidence": 0.0-1.0,
        "emotional_tone": "happy|frustrated|satisfied|disappointed|excited|angry|grateful|confused",
        "intensity": "low|medium|high"
    }},
    "intent": {{
        "primary_intent": "praise|complaint|question|suggestion|bug_report|feature_request",
        "secondary_intents": ["intent1", "intent2"],
        "urgency": "low|medium|high|critical",
        "action_required": true|false
    }},
    "topics": {{
        "main_topics": ["topic1", "topic2"],
        "subtopics": ["subtopic1", "subtopic2"],
        "keywords": ["keyword1", "keyword2"],
        "categories": ["ui_ux|performance|features|support|pricing|content|teachers|lessons|technical"]
    }},
    "priority_score": 0.0-10.0,
    "recommended_action": "none|respond|investigate|escalate"
}}

Критерії оцінки:
- priority_score: 0-2 (не потребує уваги), 3-5 (низький пріоритет), 6-7 (середній), 8-10 (високий/критичний)
- action_required: true якщо відгук потребує реакції команди
- urgency: critical для серйозних проблем, high для важливих, medium для звичайних, low для мінорних
- categories: вибери відповідні категорії з наданого списку

Аналізуй українською та англійською мовами.
"""

    async def _generate_reputation_analysis(self, reviews: List[AppReview], insights: List[ReputationInsight]) -> Dict[str, Any]:
        """Generate overall reputation analysis."""
        try:
            # Prepare summary data
            total_reviews = len(reviews)
            sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
            all_topics = []
            all_issues = []
            all_positive_aspects = []
            
            for insight in insights:
                sentiment_counts[insight.sentiment.sentiment] += 1
                all_topics.extend(insight.topics.main_topics)
                all_topics.extend(insight.topics.subtopics)
                
                if insight.intent.primary_intent in ["complaint", "bug_report"]:
                    all_issues.extend(insight.topics.main_topics)
                elif insight.intent.primary_intent == "praise":
                    all_positive_aspects.extend(insight.topics.main_topics)

            # Calculate overall score
            positive_ratio = sentiment_counts["positive"] / total_reviews if total_reviews > 0 else 0
            overall_score = (positive_ratio * 8) + 2  # Scale to 2-10 range

            # Generate topics summary
            topic_frequency = {}
            for topic in all_topics:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1

            top_issues = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            top_issues_list = [issue[0] for issue in top_issues]

            # Generate priority issues
            priority_issues = self._generate_priority_issues(insights, topic_frequency)

            reputation_score = ReputationScore(
                overall_score=round(overall_score, 1),
                sentiment_distribution=sentiment_counts,
                top_issues=top_issues_list,
                positive_aspects=list(set(all_positive_aspects))[:5],
                improvement_areas=list(set(all_issues))[:5],
                trend="stable"  # Could be enhanced with historical data
            )

            return {
                "reputation_score": reputation_score,
                "priority_issues": priority_issues
            }

        except Exception as e:
            logger.error(f"Error generating reputation analysis: {e}")
            return self._get_mock_reputation_analysis()

    def _generate_priority_issues(self, insights: List[ReputationInsight], topic_frequency: Dict[str, int]) -> List[PriorityIssue]:
        """Generate priority issues from insights."""
        priority_issues = []
        
        # Group insights by high priority
        high_priority_insights = [i for i in insights if i.priority_score >= 7]
        
        # Count issues by frequency and severity
        issue_counts = {}
        for insight in high_priority_insights:
            for topic in insight.topics.main_topics:
                if topic not in issue_counts:
                    issue_counts[topic] = {
                        "count": 0,
                        "severity": "medium",
                        "affected_users": 0,
                        "insights": []
                    }
                issue_counts[topic]["count"] += 1
                issue_counts[topic]["affected_users"] += 1
                issue_counts[topic]["insights"].append(insight)
                
                # Determine severity based on priority score
                if insight.priority_score >= 9:
                    issue_counts[topic]["severity"] = "critical"
                elif insight.priority_score >= 8:
                    issue_counts[topic]["severity"] = "high"

        # Convert to PriorityIssue objects
        for topic, data in issue_counts.items():
            if data["count"] >= 2:  # Only include issues mentioned multiple times
                priority_issues.append(PriorityIssue(
                    issue=topic,
                    frequency=data["count"],
                    severity=data["severity"],
                    affected_users=data["affected_users"],
                    recommended_response=self._get_recommended_response(topic, data["severity"]),
                    department=self._get_department(topic)
                ))

        # Sort by frequency and severity
        priority_issues.sort(key=lambda x: (x.frequency, x.severity == "critical"), reverse=True)
        return priority_issues[:5]  # Top 5 issues

    def _get_recommended_response(self, topic: str, severity: str) -> str:
        """Get recommended response strategy for an issue."""
        if "bug" in topic.lower() or "crash" in topic.lower():
            return "Immediate technical investigation and hotfix"
        elif "performance" in topic.lower() or "slow" in topic.lower():
            return "Performance optimization and user communication"
        elif "support" in topic.lower() or "help" in topic.lower():
            return "Improve support response time and documentation"
        elif "ui" in topic.lower() or "interface" in topic.lower():
            return "UX review and interface improvements"
        else:
            return "Investigate and develop improvement plan"

    def _get_department(self, topic: str) -> str:
        """Determine which department should handle the issue."""
        if any(word in topic.lower() for word in ["bug", "crash", "error", "technical", "performance"]):
            return "engineering"
        elif any(word in topic.lower() for word in ["ui", "interface", "design", "ux"]):
            return "product"
        elif any(word in topic.lower() for word in ["support", "help", "service"]):
            return "support"
        elif any(word in topic.lower() for word in ["price", "cost", "subscription"]):
            return "pr"
        else:
            return "product"

    def _get_mock_insight(self, review: AppReview) -> ReputationInsight:
        """Generate mock insight for testing."""
        return ReputationInsight(
            review_id=review.id,
            sentiment=SentimentAnalysis(
                sentiment="positive" if review.rating >= 4 else "negative",
                confidence=0.8,
                emotional_tone="happy" if review.rating >= 4 else "frustrated",
                intensity="medium"
            ),
            intent=IntentClassification(
                primary_intent="praise" if review.rating >= 4 else "complaint",
                secondary_intents=[],
                urgency="low",
                action_required=review.rating <= 2
            ),
            topics=TopicExtraction(
                main_topics=["app_quality"],
                subtopics=[],
                keywords=["app", "good" if review.rating >= 4 else "bad"],
                categories=["features"]
            ),
            priority_score=2.0 if review.rating >= 4 else 6.0,
            recommended_action="none" if review.rating >= 4 else "investigate"
        )

    def _get_mock_batch_analysis(self, reviews: List[AppReview]) -> Dict[str, Any]:
        """Generate mock batch analysis for testing."""
        insights = [self._get_mock_insight(review) for review in reviews]
        
        return {
            "insights": insights,
            "reputation_score": ReputationScore(
                overall_score=7.5,
                sentiment_distribution={"positive": 15, "negative": 3, "neutral": 2},
                top_issues=["app_performance", "user_interface", "customer_support"],
                positive_aspects=["easy_to_use", "good_teachers", "helpful_content"],
                improvement_areas=["loading_speed", "bug_fixes", "feature_requests"],
                trend="stable"
            ),
            "priority_issues": [
                PriorityIssue(
                    issue="App loading speed",
                    frequency=5,
                    severity="high",
                    affected_users=5,
                    recommended_response="Performance optimization",
                    department="engineering"
                )
            ]
        }

    def _get_mock_reputation_analysis(self) -> Dict[str, Any]:
        """Generate mock reputation analysis."""
        return {
            "reputation_score": ReputationScore(
                overall_score=7.0,
                sentiment_distribution={"positive": 10, "negative": 2, "neutral": 1},
                top_issues=["performance", "ui"],
                positive_aspects=["usability"],
                improvement_areas=["speed"],
                trend="stable"
            ),
            "priority_issues": []
        }

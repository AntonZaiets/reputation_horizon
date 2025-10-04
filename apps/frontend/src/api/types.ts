import { Review, Stats } from '../types'

// Базові типи для API відповідей
export interface BaseApiResponse {
  fetched_at: string
  time_range_hours: number
}

// Типи для API відповідей (як повертає бекенд)
export interface ApiReview {
  id: string
  author: string
  content: string
  rating: number
  date: string
  source: 'google' | 'apple'
  helpful_count?: number
  app_version?: string
}

export interface ApiStats {
  total_reviews: number
  average_rating: number
  rating_distribution: Record<string, number>
  google_reviews: number
  apple_reviews: number
}

// Типи для відгуків (API формат)
export interface ReviewsApiResponse extends BaseApiResponse {
  reviews: ApiReview[]
  stats: ApiStats
}

// Типи для аналізу репутації
export interface ReputationInsight {
  review_id: string
  sentiment: {
    sentiment: 'positive' | 'negative' | 'neutral'
    confidence: number
    emotional_tone: string
    intensity: 'low' | 'medium' | 'high'
  }
  intent: {
    primary_intent: 'praise' | 'complaint' | 'question' | 'suggestion' | 'bug_report' | 'feature_request'
    secondary_intents: string[]
    urgency: 'low' | 'medium' | 'high' | 'critical'
    action_required: boolean
  }
  topics: {
    main_topics: string[]
    subtopics: string[]
    keywords: string[]
    categories: string[]
  }
  priority_score: number
  recommended_action: 'none' | 'respond' | 'investigate' | 'escalate'
}

export interface ReputationScore {
  overall_score: number
  sentiment_distribution: {
    positive: number
    negative: number
    neutral: number
  }
  top_issues: string[]
  positive_aspects: string[]
  improvement_areas: string[]
  trend: 'improving' | 'declining' | 'stable'
}

export interface PriorityIssue {
  issue: string
  frequency: number
  severity: 'low' | 'medium' | 'high' | 'critical'
  affected_users: number
  recommended_response: string
  department: 'product' | 'support' | 'pr' | 'engineering'
}

export interface ReputationAnalysisApiResponse extends BaseApiResponse {
  reviews: ApiReview[]
  insights: ReputationInsight[]
  reputation_score: ReputationScore
  priority_issues: PriorityIssue[]
  stats: ApiStats
  analyzed_at: string
}

// Типи для здоров'я API
export interface HealthApiResponse {
  status: string
  message: string
  llm_provider: string
}

// Типи для параметрів запитів
export interface ReviewsParams {
  hours?: number
  country?: string
  limit?: number
}

export interface ReputationAnalysisParams {
  hours?: number
  max_reviews?: number
}

// Типи для помилок API
export interface ApiError {
  message: string
  code: string
  details?: any
}

// Типи для стану завантаження
export interface LoadingState {
  isLoading: boolean
  error: ApiError | null
}

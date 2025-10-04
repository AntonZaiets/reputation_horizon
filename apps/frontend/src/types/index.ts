// Основні типи для додатку
export interface Review {
  id: string
  userName: string
  rating: number
  text: string
  date: Date
  source: 'google' | 'apple' | 'trustpilot'
  version?: string
  thumbsUp?: number
  platform?: string
}

export interface Stats {
  totalReviews: number
  avgRating: number
  googlePlayReviews: number
  appStoreReviews: number
  trustpilotReviews: number
  positiveReviews: number
  negativeReviews: number
}

// Типи для фільтрації та сортування
export type FilterType = 'all' | 'google' | 'apple' | 'trustpilot'
export type SortType = 'date' | 'rating'

// Типи для API відповідей
export interface ApiReview {
  id: string
  author: string
  rating: number
  title?: string
  content: string
  date: string
  source: string
  helpful_count?: number
  app_version?: string
}

export interface ApiStats {
  total_reviews: number
  average_rating: number
  google_reviews: number
  apple_reviews: number
  rating_distribution: Record<string, number>
}

export interface ApiResponse {
  reviews: ApiReview[]
  stats: ApiStats
  fetched_at: string
  time_range_hours: number
}

// Типи для обробки помилок
export interface AppError {
  message: string
  code?: string
  details?: any
}

// Типи для стану завантаження
export interface LoadingState {
  isLoading: boolean
  error: AppError | null
}

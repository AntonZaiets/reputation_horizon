import { useState, useEffect, useCallback } from 'react'
import { Review, Stats, LoadingState, FilterType, SortType } from '../types'
import { mapApiResponseToReviews, handleApiError } from '../utils'
import { DEFAULT_SETTINGS, MESSAGES } from '../constants'
import { api } from '../api'
import { ReviewsApiResponse } from '../api/types'

interface UseReviewsReturn {
  reviews: Review[]
  filteredReviews: Review[]
  stats: Stats
  loadingState: LoadingState
  filter: FilterType
  sortBy: SortType
  setFilter: (filter: FilterType) => void
  setSortBy: (sortBy: SortType) => void
  loadReviews: () => Promise<void>
  refreshReviews: () => Promise<void>
}

export const useReviews = (): UseReviewsReturn => {
  const [reviews, setReviews] = useState<Review[]>([])
  const [filteredReviews, setFilteredReviews] = useState<Review[]>([])
  const [stats, setStats] = useState<Stats>({
    totalReviews: 0,
    avgRating: 0,
      googlePlayReviews: 0,
      appStoreReviews: 0,
      trustpilotReviews: 0,
      positiveReviews: 0,
      negativeReviews: 0,
  })
  const [loadingState, setLoadingState] = useState<LoadingState>({
    isLoading: false,
    error: null
  })
  const [filter, setFilter] = useState<FilterType>('all')
  const [sortBy, setSortBy] = useState<SortType>('date')

  const loadReviews = useCallback(async () => {
    setLoadingState({ isLoading: true, error: null })
    
    try {
      const data = await api.reviews.getReviews(DEFAULT_SETTINGS.HOURS, 20) as ReviewsApiResponse
      
      // Мапимо відгуки
      const reviewsWithDates = mapApiResponseToReviews(data)
      setReviews(reviewsWithDates)
      
      // Мапимо статистику
      setStats({
        totalReviews: data.stats?.total_reviews || 0,
        avgRating: data.stats?.average_rating || 0,
        googlePlayReviews: data.stats?.google_reviews || 0,
        appStoreReviews: data.stats?.apple_reviews || 0,
        trustpilotReviews: data.stats?.trustpilot_reviews || 0,
        positiveReviews: (data.stats?.rating_distribution?.['5'] || 0) + 
                        (data.stats?.rating_distribution?.['4'] || 0),
        negativeReviews: (data.stats?.rating_distribution?.['1'] || 0) + 
                        (data.stats?.rating_distribution?.['2'] || 0),
      })

      console.log(`✅ Завантажено ${data.stats?.total_reviews || 0} реальних відгуків про Preply`)
      
    } catch (error) {
      const errorMessage = handleApiError(error)
      console.error('❌ Помилка завантаження відгуків:', error)
      
      setLoadingState({ 
        isLoading: false, 
        error: { 
          message: MESSAGES.ERROR_LOADING,
          code: 'LOAD_REVIEWS_ERROR',
          details: errorMessage
        }
      })
    } finally {
      setLoadingState(prev => ({ ...prev, isLoading: false }))
    }
  }, [])

  const refreshReviews = useCallback(async () => {
    await loadReviews()
  }, [loadReviews])

  // Фільтрація та сортування
  useEffect(() => {
    let filtered = [...reviews]

    // Застосовуємо фільтр
    if (filter !== 'all') {
      filtered = filtered.filter(review => review.source === filter)
    }

    // Застосовуємо сортування
    if (sortBy === 'date') {
      filtered.sort((a, b) => b.date.getTime() - a.date.getTime())
    } else if (sortBy === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating)
    }

    setFilteredReviews(filtered)
  }, [filter, sortBy, reviews])

  // Завантаження при ініціалізації
  useEffect(() => {
    loadReviews()
  }, [loadReviews])

  return {
    reviews,
    filteredReviews,
    stats,
    loadingState,
    filter,
    sortBy,
    setFilter,
    setSortBy,
    loadReviews,
    refreshReviews
  }
}

import { useState, useCallback } from 'react'
import { api } from '../api'
import { AppError } from '../types'

// Хук для роботи з API запитами
export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<AppError | null>(null)

  const executeRequest = useCallback(async <T>(
    requestFn: () => Promise<T>
  ): Promise<T | null> => {
    setLoading(true)
    setError(null)

    try {
      const result = await requestFn()
      return result
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      setError({
        message: errorMessage,
        code: 'API_ERROR',
        details: err
      })
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    loading,
    error,
    executeRequest,
    clearError
  }
}

// Хук для роботи з відгуками
export const useReviewsApi = () => {
  const { loading, error, executeRequest, clearError } = useApi()

  const getReviews = useCallback(async (hours: number = 24) => {
    return executeRequest(() => api.reviews.getReviews(hours))
  }, [executeRequest])

  const getGoogleReviews = useCallback(async (hours: number = 24) => {
    return executeRequest(() => api.reviews.getGoogleReviews(hours))
  }, [executeRequest])

  const getAppleReviews = useCallback(async (hours: number = 24) => {
    return executeRequest(() => api.reviews.getAppleReviews(hours))
  }, [executeRequest])

  return {
    loading,
    error,
    getReviews,
    getGoogleReviews,
    getAppleReviews,
    clearError
  }
}

// Хук для роботи з аналізом репутації
export const useReputationApi = () => {
  const { loading, error, executeRequest, clearError } = useApi()

  const analyzeReputation = useCallback(async (hours: number = 24, maxReviews: number = 50) => {
    return executeRequest(() => api.reputation.analyzeReputation(hours, maxReviews))
  }, [executeRequest])

  const getReputationSummary = useCallback(async (hours: number = 24) => {
    return executeRequest(() => api.reputation.getReputationSummary(hours))
  }, [executeRequest])

  return {
    loading,
    error,
    analyzeReputation,
    getReputationSummary,
    clearError
  }
}

// Хук для перевірки здоров'я API
export const useHealthApi = () => {
  const { loading, error, executeRequest, clearError } = useApi()

  const checkHealth = useCallback(async () => {
    return executeRequest(() => api.health.checkHealth())
  }, [executeRequest])

  return {
    loading,
    error,
    checkHealth,
    clearError
  }
}

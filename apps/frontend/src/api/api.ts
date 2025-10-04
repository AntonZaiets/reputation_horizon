import { API_BASE_URL, API_ENDPOINTS } from '../constants'
import { 
  ReviewsApiResponse, 
  ReputationAnalysisApiResponse, 
  HealthApiResponse,
  ReviewsParams,
  ReputationAnalysisParams
} from './types'

// Базовий клас для API запитів
class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, defaultOptions)
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // GET запит
  async get<T>(endpoint: string, params?: Record<string, string | number | boolean>): Promise<T> {
    let url = endpoint
    
    if (params) {
      const searchParams = new URLSearchParams()
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, String(value))
        }
      })
      url += `?${searchParams.toString()}`
    }

    return this.request<T>(url, { method: 'GET' })
  }

  // POST запит
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // PUT запит
  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // DELETE запит
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

// Створюємо екземпляр API клієнта
const apiClient = new ApiClient(API_BASE_URL)

// API функції для різних ендпоінтів
export const reviewsApi = {
  // Отримати відгуки
  getReviews: async (hours: number = 24, max_trustpilot_pages: number = 20): Promise<ReviewsApiResponse> => {
    return apiClient.get<ReviewsApiResponse>(API_ENDPOINTS.REVIEWS, { hours, max_trustpilot_pages })
  },

  // Отримати відгуки з Google Play
  getGoogleReviews: async (hours: number = 24): Promise<ReviewsApiResponse> => {
    return apiClient.get<ReviewsApiResponse>(`${API_ENDPOINTS.REVIEWS}/google`, { hours })
  },

  // Отримати відгуки з App Store
  getAppleReviews: async (hours: number = 24): Promise<ReviewsApiResponse> => {
    return apiClient.get<ReviewsApiResponse>(`${API_ENDPOINTS.REVIEWS}/apple`, { hours })
  },

  // Отримати відгуки з Trustpilot
  getTrustpilotReviews: async (hours: number = 24, max_pages: number = 20): Promise<ReviewsApiResponse> => {
    return apiClient.get<ReviewsApiResponse>(`${API_ENDPOINTS.REVIEWS}/trustpilot`, { hours, max_pages })
  },
}

export const reputationApi = {
  // Аналіз репутації
  analyzeReputation: async (
    hours: number = 24,
    maxReviews: number = 50
  ): Promise<ReputationAnalysisApiResponse> => {
    return apiClient.get<ReputationAnalysisApiResponse>(
      API_ENDPOINTS.REPUTATION_ANALYSIS,
      { hours, max_reviews: maxReviews }
    )
  },

  // Отримати резюме репутації
  getReputationSummary: async (hours: number = 24): Promise<any> => {
    return apiClient.get<any>(API_ENDPOINTS.REPUTATION_SUMMARY, { hours })
  },
}

export const healthApi = {
  // Перевірка здоров'я API
  checkHealth: async (): Promise<HealthApiResponse> => {
    return apiClient.get<HealthApiResponse>(API_ENDPOINTS.HEALTH)
  },
}

// Експортуємо основний API клієнт для випадків, коли потрібен більш гнучкий доступ
export { apiClient }

// Експортуємо всі API функції разом для зручності
export const api = {
  reviews: reviewsApi,
  reputation: reputationApi,
  health: healthApi,
}

export default api

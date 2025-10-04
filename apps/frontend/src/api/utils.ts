// Утиліти для роботи з API

/**
 * Перевіряє, чи є помилка в відповіді API
 */
export const isApiError = (response: any): response is { error: string; detail: string } => {
  return response && (response.error || response.detail)
}

/**
 * Обробляє помилки API і повертає зрозуміле повідомлення
 */
export const handleApiError = (error: any): string => {
  if (error instanceof Error) {
    return error.message
  }
  
  if (typeof error === 'string') {
    return error
  }
  
  if (error?.response?.data?.detail) {
    return error.response.data.detail
  }
  
  if (error?.response?.data?.error) {
    return error.response.data.error
  }
  
  if (error?.response?.status) {
    return `HTTP ${error.response.status}: ${error.response.statusText || 'Unknown error'}`
  }
  
  return 'Невідома помилка API'
}

/**
 * Створює URL з параметрами
 */
export const buildApiUrl = (baseUrl: string, endpoint: string, params?: Record<string, any>): string => {
  let url = `${baseUrl}${endpoint}`
  
  if (params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value))
      }
    })
    url += `?${searchParams.toString()}`
  }
  
  return url
}

/**
 * Перевіряє, чи є відповідь успішною
 */
export const isSuccessResponse = (status: number): boolean => {
  return status >= 200 && status < 300
}

/**
 * Затримка для демонстрації завантаження
 */
export const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Повторює запит з експоненційною затримкою
 */
export const retryRequest = async <T>(
  requestFn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> => {
  let lastError: any
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await requestFn()
    } catch (error) {
      lastError = error
      
      if (attempt === maxRetries) {
        throw error
      }
      
      const delayMs = baseDelay * Math.pow(2, attempt)
      await delay(delayMs)
    }
  }
  
  throw lastError
}

/**
 * Кешування результатів API запитів
 */
export class ApiCache {
  private cache = new Map<string, { data: any; timestamp: number; ttl: number }>()
  
  set(key: string, data: any, ttl: number = 5 * 60 * 1000): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    })
  }
  
  get(key: string): any | null {
    const item = this.cache.get(key)
    
    if (!item) {
      return null
    }
    
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key)
      return null
    }
    
    return item.data
  }
  
  clear(): void {
    this.cache.clear()
  }
  
  delete(key: string): boolean {
    return this.cache.delete(key)
  }
}

// Глобальний кеш для API
export const apiCache = new ApiCache()

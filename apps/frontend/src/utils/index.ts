import { Review, ApiReview, ApiResponse, FilterType, SortType } from '../types'

// Форматування дати
export const formatDate = (date: Date): string => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))

  if (hours < 1) {
    return `${minutes} хв тому`
  } else if (hours < 24) {
    return `${hours} год тому`
  }
  return date.toLocaleDateString('uk-UA')
}

// Мапінг API відповіді на внутрішній формат
export const mapApiResponseToReviews = (data: { reviews: any[] }): Review[] => {
  return data.reviews.map((review: any) => ({
    id: review.id,
    userName: review.author || 'Anonymous',
    text: review.content || review.text || '',
    thumbsUp: review.helpful_count || review.thumbsUp,
    version: review.app_version || review.version,
    platform: review.source === 'google' ? 'Google Play' : 
              review.source === 'apple' ? 'App Store' : review.source,
    rating: review.rating,
    source: review.source as 'google' | 'apple',
    date: new Date(review.date)
  }))
}

// Фільтрація відгуків
export const filterReviews = (reviews: Review[], filter: FilterType): Review[] => {
  if (filter === 'all') return reviews
  return reviews.filter(review => review.source === filter)
}

// Сортування відгуків
export const sortReviews = (reviews: Review[], sortBy: SortType): Review[] => {
  const sorted = [...reviews]
  
  if (sortBy === 'date') {
    return sorted.sort((a, b) => b.date.getTime() - a.date.getTime())
  } else if (sortBy === 'rating') {
    return sorted.sort((a, b) => b.rating - a.rating)
  }
  
  return sorted
}

// Валідація відгуку
export const validateReview = (review: any): boolean => {
  return !!(
    review &&
    review.id &&
    review.rating >= 1 &&
    review.rating <= 5 &&
    review.text &&
    review.date
  )
}

// Отримання класу рейтингу
export const getRatingClass = (rating: number): string => {
  if (rating >= 4) return 'positive'
  if (rating <= 2) return 'negative'
  return 'neutral'
}

// Рендеринг зірок
export const renderStars = (rating: number) => {
  return Array.from({ length: 5 }, (_, i) => ({
    key: i,
    className: `star ${i < rating ? 'filled' : ''}`,
    content: '⭐'
  }))
}

// Обробка помилок API
export const handleApiError = (error: any): string => {
  if (error instanceof Error) {
    return error.message
  }
  
  if (typeof error === 'string') {
    return error
  }
  
  return 'Сталася невідома помилка'
}

// Дебаунс функція
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// Форматування числа
export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

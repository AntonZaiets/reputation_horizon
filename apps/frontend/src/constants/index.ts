// API константи
export const API_BASE_URL = 'http://localhost:8000'
export const API_ENDPOINTS = {
  REVIEWS: '/api/reviews',
  REPUTATION_ANALYSIS: '/api/reputation/analyze',
  REPUTATION_SUMMARY: '/api/reputation/summary',
  HEALTH: '/api/health'
} as const

// Налаштування за замовчуванням
export const DEFAULT_SETTINGS = {
  HOURS: 168, // 7 днів (168 годин) - максимальний ліміт бекенду
  MAX_REVIEWS: 100, // Бекенд має ліміт 100 для аналізу
  ANALYSIS_MAX_REVIEWS: 50
} as const

// Кольори для різних станів
export const COLORS = {
  PRIMARY: '#667eea',
  SECONDARY: '#764ba2',
  SUCCESS: '#10b981',
  WARNING: '#f59e0b',
  ERROR: '#ef4444',
  INFO: '#3b82f6'
} as const

// Розміри для спінерів
export const SPINNER_SIZES = {
  SMALL: 24,
  MEDIUM: 40,
  LARGE: 60
} as const

// Тривалість анімацій
export const ANIMATION_DURATION = {
  FAST: 200,
  NORMAL: 300,
  SLOW: 500
} as const

// Messages
export const MESSAGES = {
  LOADING_REVIEWS: 'Loading reviews...',
  LOADING_ANALYSIS: 'Analyzing reputation...',
  NO_REVIEWS: 'No reviews found for the selected filters',
  ERROR_LOADING: 'Failed to load data',
  ERROR_BACKEND: 'Make sure the backend is running on http://localhost:8000'
} as const

# API Module

Цей модуль містить всю логіку для роботи з API запитами.

## Структура

```
src/api/
├── index.ts          # Головний експорт модуля
├── api.ts            # Основний API клієнт та функції
├── types.ts          # TypeScript типи для API
├── utils.ts          # Утиліти для роботи з API
└── README.md         # Документація
```

## Використання

### Базове використання

```typescript
import { api } from '../api'

// Отримати відгуки
const reviews = await api.reviews.getReviews(24)

// Аналіз репутації
const analysis = await api.reputation.analyzeReputation(168, 50)

// Перевірка здоров'я
const health = await api.health.checkHealth()
```

### Використання з хуками

```typescript
import { useReviewsApi, useReputationApi } from '../hooks/useApi'

function MyComponent() {
  const { loading, error, getReviews } = useReviewsApi()
  const { analyzeReputation } = useReputationApi()

  const handleLoadReviews = async () => {
    const reviews = await getReviews(24)
    if (reviews) {
      console.log('Reviews loaded:', reviews)
    }
  }

  return (
    <div>
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
      <button onClick={handleLoadReviews}>Load Reviews</button>
    </div>
  )
}
```

### Пряме використання API клієнта

```typescript
import { apiClient } from '../api'

// GET запит
const data = await apiClient.get('/api/custom-endpoint', { param: 'value' })

// POST запит
const result = await apiClient.post('/api/custom-endpoint', { data: 'value' })
```

## Типи

Всі типи експортуються з `types.ts`:

```typescript
import { 
  ReviewsApiResponse, 
  ReputationAnalysisApiResponse,
  HealthApiResponse 
} from '../api'
```

## Утиліти

```typescript
import { 
  handleApiError, 
  buildApiUrl, 
  retryRequest,
  apiCache 
} from '../api'

// Обробка помилок
try {
  const data = await api.reviews.getReviews(24)
} catch (error) {
  const errorMessage = handleApiError(error)
  console.error(errorMessage)
}

// Кешування
const cachedData = apiCache.get('reviews-24h')
if (!cachedData) {
  const data = await api.reviews.getReviews(24)
  apiCache.set('reviews-24h', data, 5 * 60 * 1000) // 5 хвилин
}
```

## Переваги

1. **Централізована логіка** - всі API запити в одному місці
2. **Типізація** - повна підтримка TypeScript
3. **Обробка помилок** - уніфікована обробка помилок
4. **Кешування** - вбудований кеш для оптимізації
5. **Повторні спроби** - автоматичні повторні спроби при помилках
6. **Хуки** - зручні React хуки для використання в компонентах

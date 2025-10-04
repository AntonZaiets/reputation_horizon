import { useState, useEffect } from 'react'
import './App.css'
import ReviewCard from './components/ReviewCard'
import StatsCard from './components/StatsCard'
import FilterBar from './components/FilterBar'
import Header from './components/Header'

export interface Review {
  id: string
  userName: string
  rating: number
  text: string
  date: Date
  source: 'google' | 'apple'
  version?: string
  thumbsUp?: number
}

export interface Stats {
  totalReviews: number
  avgRating: number
  googlePlayReviews: number
  appStoreReviews: number
  positiveReviews: number
  negativeReviews: number
}

function App() {
  const [reviews, setReviews] = useState<Review[]>([])
  const [filteredReviews, setFilteredReviews] = useState<Review[]>([])
  const [stats, setStats] = useState<Stats>({
    totalReviews: 0,
    avgRating: 0,
    googlePlayReviews: 0,
    appStoreReviews: 0,
    positiveReviews: 0,
    negativeReviews: 0,
  })
  const [loading, setLoading] = useState(false)
  const [filter, setFilter] = useState<'all' | 'google' | 'apple'>('all')
  const [sortBy, setSortBy] = useState<'date' | 'rating'>('date')

  // Load real reviews from API
  const loadReviews = async () => {
    setLoading(true)
    try {
      // Отримуємо відгуки за останні 168 годин (7 днів) для більшої кількості даних
      const response = await fetch('http://localhost:8000/api/reviews?hours=168&country=us&limit=200')
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      
      // Конвертуємо дати з ISO string в Date об'єкти та мапимо поля
      const reviewsWithDates = data.reviews.map((review: any) => ({
        ...review,
        userName: review.author || 'Anonymous', // Мапимо author -> userName
        text: review.content || review.text || '', // Мапимо content -> text
        thumbsUp: review.helpful_count || review.thumbsUp, // Мапимо helpful_count -> thumbsUp
        version: review.app_version || review.version, // Мапимо app_version -> version
        platform: review.source === 'google' ? 'Google Play' : review.source === 'apple' ? 'App Store' : review.source, // Мапимо source -> platform
        date: new Date(review.date)
      }))

      setReviews(reviewsWithDates)
      setFilteredReviews(reviewsWithDates)
      
      // Мапимо статистику з API формату на frontend формат
      setStats({
        totalReviews: data.stats?.total_reviews || 0,
        avgRating: data.stats?.average_rating || 0,
        googlePlayReviews: data.stats?.google_reviews || 0,
        appStoreReviews: data.stats?.apple_reviews || 0,
        positiveReviews: data.stats?.rating_distribution?.['5'] + data.stats?.rating_distribution?.['4'] || 0,
        negativeReviews: data.stats?.rating_distribution?.['1'] + data.stats?.rating_distribution?.['2'] || 0,
      })

      console.log(`✅ Завантажено ${data.stats?.total_reviews || data.stats?.totalReviews || 0} реальних відгуків про Preply`)
      
    } catch (error) {
      console.error('❌ Помилка завантаження відгуків:', error)
      console.log('💡 Переконайтесь, що backend запущений: cd apps/backend && python main.py')
      
      // Показуємо помилку користувачу
      alert('Не вдалося завантажити відгуки. Переконайтесь, що backend запущений на http://localhost:8000')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReviews()
  }, [])

  useEffect(() => {
    let filtered = [...reviews]

    // Apply filter
    if (filter !== 'all') {
      filtered = filtered.filter(review => review.source === filter)
    }

    // Apply sort
    if (sortBy === 'date') {
      filtered.sort((a, b) => b.date.getTime() - a.date.getTime())
    } else if (sortBy === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating)
    }

    setFilteredReviews(filtered)
  }, [filter, sortBy, reviews])

  const handleRefresh = () => {
    loadReviews()
  }

  return (
    <div className="app">
      <Header onRefresh={handleRefresh} loading={loading} />
      
      <div className="container">
        <StatsCard stats={stats} />
        
        <FilterBar
          filter={filter}
          setFilter={setFilter}
          sortBy={sortBy}
          setSortBy={setSortBy}
        />

        <div className="reviews-section">
          <h2 className="section-title">
            Відгуки за останні 24 години
            <span className="review-count">{filteredReviews.length}</span>
          </h2>

          {loading ? (
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Завантаження відгуків...</p>
            </div>
          ) : filteredReviews.length === 0 ? (
            <div className="no-reviews">
              <p>Відгуків не знайдено за вказаними фільтрами</p>
            </div>
          ) : (
            <div className="reviews-grid">
              {filteredReviews.map(review => (
                <ReviewCard key={review.id} review={review} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

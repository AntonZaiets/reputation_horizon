import React, { useState } from 'react'
import './App.css'
import ReviewCard from './components/ReviewCard'
import StatsCard from './components/StatsCard'
import FilterBar from './components/FilterBar'
import Header from './components/Header'
import ReputationAnalysis from './components/ReputationAnalysis'
import { GoogleReputationAnalysis } from './components/GoogleReputationAnalysis'
import { ErrorBoundary } from './components/ErrorBoundary'
import { Notification } from './components/Notification'
import { LoadingSpinner } from './components/LoadingSpinner'
import { useReviews } from './hooks/useReviews'
import { MESSAGES } from './constants'

function App() {
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [showGoogleAnalysis, setShowGoogleAnalysis] = useState(false)
  const [notificationError, setNotificationError] = useState<any>(null)
  const [googleAnalysisData, setGoogleAnalysisData] = useState<any>(null)
  const [googleAnalysisLoading, setGoogleAnalysisLoading] = useState(false)
  const [googleAnalysisError, setGoogleAnalysisError] = useState<string | null>(null)
  
  const {
    filteredReviews,
    stats,
    loadingState,
    filter,
    sortBy,
    setFilter,
    setSortBy,
    refreshReviews
  } = useReviews()

  // Обробка помилок
  React.useEffect(() => {
    if (loadingState.error) {
      setNotificationError(loadingState.error)
    }
  }, [loadingState.error])

  // Автоматично запускаємо Google аналіз при відкритті сайту
  React.useEffect(() => {
    const runGoogleAnalysis = async () => {
      setGoogleAnalysisLoading(true)
      setGoogleAnalysisError(null)
      setGoogleAnalysisData(null)

      try {
        const response = await fetch('http://localhost:8000/api/reputation/analyze/preply')
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        setGoogleAnalysisData(data)
        // Автоматично відкриваємо аналіз після завершення
        setShowGoogleAnalysis(true)
      } catch (err) {
        setGoogleAnalysisError(err instanceof Error ? err.message : 'Failed to analyze reputation')
      } finally {
        setGoogleAnalysisLoading(false)
      }
    }

    runGoogleAnalysis()
  }, [])

  const handleAnalysisComplete = (data: any) => {
    console.log('Reputation analysis completed:', data)
  }

  return (
    <ErrorBoundary>
      <div className="app">
        <Notification 
          error={notificationError} 
          onClose={() => setNotificationError(null)} 
        />
        
        <Header 
          onRefresh={refreshReviews} 
          loading={loadingState.isLoading} 
        />
        
        <div className="container">
          <StatsCard stats={stats} />
          
          <div className="analysis-toggle">
            <button 
              className={`toggle-button ${showAnalysis ? 'active' : ''}`}
              onClick={() => setShowAnalysis(!showAnalysis)}
            >
              {showAnalysis ? '📊 Приховати аналіз' : '🤖 Показати AI аналіз репутації'}
            </button>
            <button 
              className={`toggle-button ${showGoogleAnalysis ? 'active' : ''}`}
              onClick={() => setShowGoogleAnalysis(!showGoogleAnalysis)}
            >
              {showGoogleAnalysis ? '🔍 Приховати Google аналіз' : 
               googleAnalysisLoading ? '⏳ Аналіз виконується...' :
               '🔍 Google аналіз репутації'}
            </button>
          </div>

          {showAnalysis && (
            <ReputationAnalysis onAnalysisComplete={handleAnalysisComplete} />
          )}

          {showGoogleAnalysis && (
            <GoogleReputationAnalysis 
              onClose={() => setShowGoogleAnalysis(false)}
              data={googleAnalysisData}
              loading={googleAnalysisLoading}
              error={googleAnalysisError}
            />
          )}
          
          <FilterBar
            filter={filter}
            setFilter={setFilter}
            sortBy={sortBy}
            setSortBy={setSortBy}
          />

          <div className="reviews-section">
            <h2 className="section-title">
              Відгуки за останні 7 днів
              <span className="review-count">{filteredReviews.length}</span>
            </h2>

            {loadingState.isLoading ? (
              <LoadingSpinner 
                message={MESSAGES.LOADING_REVIEWS} 
                size="large"
              />
            ) : filteredReviews.length === 0 ? (
              <div className="no-reviews">
                <p>{MESSAGES.NO_REVIEWS}</p>
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
    </ErrorBoundary>
  )
}

export default App

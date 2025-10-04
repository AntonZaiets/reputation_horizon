import React, { useState, Suspense, lazy } from 'react'
import './App.css'
import ReviewCard from './components/ReviewCard'
import StatsCard from './components/StatsCard'
import FilterBar from './components/FilterBar'
import Header from './components/Header'
import { ErrorBoundary } from './components/ErrorBoundary'
import { Notification } from './components/Notification'
import { LoadingSpinner } from './components/LoadingSpinner'
import { useReviews } from './hooks/useReviews'
import { MESSAGES } from './constants'

// Lazy load heavy components
const ReputationAnalysis = lazy(() => import('./components/ReputationAnalysis'))
const GoogleReputationAnalysis = lazy(() => import('./components/GoogleReputationAnalysis').then(module => ({ default: module.GoogleReputationAnalysis })))

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

  // Error handling
  React.useEffect(() => {
    if (loadingState.error) {
      setNotificationError(loadingState.error)
    }
  }, [loadingState.error])

  // Automatically run Google analysis when opening the site
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
        // Automatically open analysis after completion
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
        
        <main className="container" role="main">
          <section aria-labelledby="stats-heading">
            <h2 id="stats-heading" className="sr-only">Reviews Statistics</h2>
            <StatsCard stats={stats} />
          </section>
          
          <section className="analysis-toggle" aria-labelledby="analysis-heading">
            <h2 id="analysis-heading" className="sr-only">Reputation Analysis</h2>
            <button 
              className={`toggle-button ${showAnalysis ? 'active' : ''}`}
              onClick={() => setShowAnalysis(!showAnalysis)}
              aria-pressed={showAnalysis}
              aria-expanded={showAnalysis}
              aria-controls="ai-analysis-section"
            >
              <span aria-hidden="true">🤖</span>
              {showAnalysis ? 'Hide Analysis' : 'Show AI Reputation Analysis'}
            </button>
            <button 
              className={`toggle-button ${showGoogleAnalysis ? 'active' : ''}`}
              onClick={() => setShowGoogleAnalysis(!showGoogleAnalysis)}
              aria-pressed={showGoogleAnalysis}
              aria-expanded={showGoogleAnalysis}
              aria-controls="google-analysis-section"
              disabled={googleAnalysisLoading}
            >
              <span aria-hidden="true">🔍</span>
              {showGoogleAnalysis ? 'Hide Google Analysis' : 
               googleAnalysisLoading ? 'Analysis in progress...' :
               'Google Reputation Analysis'}
            </button>
          </section>

          {showAnalysis && (
            <section id="ai-analysis-section" aria-labelledby="ai-analysis-heading">
              <h2 id="ai-analysis-heading" className="sr-only">AI Reputation Analysis</h2>
              <Suspense fallback={
                <div className="loading-container">
                  <LoadingSpinner message="Loading AI analysis..." size="large" />
                </div>
              }>
                <ReputationAnalysis onAnalysisComplete={handleAnalysisComplete} />
              </Suspense>
            </section>
          )}

          {showGoogleAnalysis && (
            <section id="google-analysis-section" aria-labelledby="google-analysis-heading">
              <h2 id="google-analysis-heading" className="sr-only">Google Reputation Analysis</h2>
              <Suspense fallback={
                <div className="loading-container">
                  <LoadingSpinner message="Loading Google analysis..." size="large" />
                </div>
              }>
                <GoogleReputationAnalysis 
                  onClose={() => setShowGoogleAnalysis(false)}
                  data={googleAnalysisData}
                  loading={googleAnalysisLoading}
                  error={googleAnalysisError}
                />
              </Suspense>
            </section>
          )}
          
          <FilterBar
            filter={filter}
            setFilter={setFilter}
            sortBy={sortBy}
            setSortBy={setSortBy}
          />

          <section className="reviews-section" aria-labelledby="reviews-heading">
            <h2 id="reviews-heading" className="section-title">
              Reviews from the last 7 days
              <span className="review-count" aria-label={`Number of reviews: ${filteredReviews.length}`}>
                {filteredReviews.length}
              </span>
            </h2>

            {loadingState.isLoading ? (
              <div role="status" aria-live="polite">
                <LoadingSpinner 
                  message={MESSAGES.LOADING_REVIEWS} 
                  size="large"
                />
              </div>
            ) : filteredReviews.length === 0 ? (
              <div className="no-reviews" role="status" aria-live="polite">
                <p>{MESSAGES.NO_REVIEWS}</p>
              </div>
            ) : (
              <div className="reviews-grid" role="list" aria-label="Reviews list">
                {filteredReviews.map(review => (
                  <ReviewCard key={review.id} review={review} />
                ))}
              </div>
            )}
          </section>
        </main>
      </div>
    </ErrorBoundary>
  )
}

export default App

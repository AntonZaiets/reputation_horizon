import React, { memo } from 'react'
import { Stats } from '../types'

interface StatsCardProps {
  stats: Stats
}

const StatsCard = memo(function StatsCard({ stats }: StatsCardProps) {
  const totalSocialReviews = stats.googlePlayReviews + stats.appStoreReviews + stats.trustpilotReviews
  const sentimentPercentage = stats.totalReviews > 0 ? Math.round((stats.positiveReviews / stats.totalReviews) * 100) : 0
  
  return (
    <div className="stats-container">
      {/* Total Statistics */}
      <div className="stat-card primary">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <div className="stat-value">{stats.totalReviews}</div>
          <div className="stat-label">Total Reviews</div>
          <div className="stat-subtitle">All time</div>
        </div>
      </div>

      {/* Rating */}
      <div className="stat-card rating">
        <div className="stat-icon">⭐</div>
        <div className="stat-content">
          <div className="stat-value">{stats.avgRating}</div>
          <div className="stat-label">Average Rating</div>
          <div className="stat-subtitle">out of 5.0</div>
        </div>
      </div>

      {/* Social Platforms */}
      <div className="stat-card social">
        <div className="stat-icon">🌐</div>
        <div className="stat-content">
          <div className="stat-value">{totalSocialReviews}</div>
          <div className="stat-label">Social Platforms</div>
          <div className="stat-subtitle">
            Google: {stats.googlePlayReviews} • Apple: {stats.appStoreReviews} • Trustpilot: {stats.trustpilotReviews}
          </div>
        </div>
      </div>

      {/* Sentiment */}
      <div className="stat-card sentiment">
        <div className="stat-icon">😊</div>
        <div className="stat-content">
          <div className="stat-value">{sentimentPercentage}%</div>
          <div className="stat-label">Positivity</div>
          <div className="stat-subtitle">
            👍 {stats.positiveReviews} • 👎 {stats.negativeReviews}
          </div>
        </div>
      </div>
    </div>
  )
})

export default StatsCard


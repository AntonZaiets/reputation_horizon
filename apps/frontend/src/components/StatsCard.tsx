import React from 'react'
import { Stats } from '../App'

interface StatsCardProps {
  stats: Stats
}

export default function StatsCard({ stats }: StatsCardProps) {
  return (
    <div className="stats-container">
      <div className="stat-card primary">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <div className="stat-value">{stats.totalReviews}</div>
          <div className="stat-label">Всього відгуків</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">⭐</div>
        <div className="stat-content">
          <div className="stat-value">{stats.avgRating}</div>
          <div className="stat-label">Середній рейтинг</div>
        </div>
      </div>

      <div className="stat-card google">
        <div className="stat-icon">🤖</div>
        <div className="stat-content">
          <div className="stat-value">{stats.googlePlayReviews}</div>
          <div className="stat-label">Google Play</div>
        </div>
      </div>

      <div className="stat-card apple">
        <div className="stat-icon">🍎</div>
        <div className="stat-content">
          <div className="stat-value">{stats.appStoreReviews}</div>
          <div className="stat-label">App Store</div>
        </div>
      </div>

      <div className="stat-card positive">
        <div className="stat-icon">👍</div>
        <div className="stat-content">
          <div className="stat-value">{stats.positiveReviews}</div>
          <div className="stat-label">Позитивні</div>
        </div>
      </div>

      <div className="stat-card negative">
        <div className="stat-icon">👎</div>
        <div className="stat-content">
          <div className="stat-value">{stats.negativeReviews}</div>
          <div className="stat-label">Негативні</div>
        </div>
      </div>
    </div>
  )
}


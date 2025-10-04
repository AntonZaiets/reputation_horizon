import React, { memo } from 'react'
import { Review } from '../types'
import { formatDate, renderStars, getRatingClass } from '../utils'

interface ReviewCardProps {
  review: Review
}

const ReviewCard = memo(function ReviewCard({ review }: ReviewCardProps) {
  const getSourceName = () => {
    if (review.platform === 'Google Play' || review.source === 'google') return 'Google Play'
    if (review.platform === 'App Store' || review.source === 'apple') return 'App Store'
    return 'Trustpilot'
  }

  const getSourceIcon = () => {
    if (review.platform === 'Google Play' || review.source === 'google') return '🤖'
    if (review.platform === 'App Store' || review.source === 'apple') return '🍎'
    return '⭐'
  }

  const handleTranslate = () => {
    const text = encodeURIComponent(review.text)
    const translateUrl = `https://translate.google.com/?sl=auto&tl=en&text=${text}`
    window.open(translateUrl, '_blank', 'noopener,noreferrer')
  }

  return (
    <article className={`review-card ${review.source}`} role="article" aria-labelledby={`review-${review.id}`}>
      <header className="review-header">
        <div className="review-user">
          <div className="user-info">
            <h3 className="user-name" id={`review-${review.id}`}>
              {review.userName || 'Anonymous'}
            </h3>
            <div className="review-meta">
              <time className="review-date" dateTime={review.date}>
                {formatDate(review.date)}
              </time>
              {review.version && (
                <>
                  <span className="separator" aria-hidden="true">•</span>
                  <span className="review-version">v{review.version}</span>
                </>
              )}
            </div>
          </div>
        </div>
        <div 
          className={`source-badge ${review.source || review.platform?.toLowerCase().replace(' ', '')}`}
          aria-label={`Джерело: ${getSourceName()}`}
        >
          <span className="source-icon" aria-hidden="true">{getSourceIcon()}</span>
          <span className="source-text">{getSourceName()}</span>
        </div>
      </header>

      <div className={`review-rating ${getRatingClass(review.rating)}`} role="img" aria-label={`Рейтинг: ${review.rating} з 5 зірок`}>
        <div className="stars" aria-hidden="true">
          {renderStars(review.rating).map(star => (
            <span key={star.key} className={star.className}>
              {star.content}
            </span>
          ))}
        </div>
        <span className="rating-number">{review.rating}/5</span>
      </div>

      <div className="review-text">
        {review.text}
      </div>

      <div className="review-actions">
        <button 
          className="translate-button"
          onClick={handleTranslate}
          aria-label="Translate to English"
          title="Translate to English"
        >
          <span className="translate-icon" aria-hidden="true">🌐</span>
          Translate
        </button>
      </div>

      {review.thumbsUp !== undefined && (
        <footer className="review-footer">
          <div className="thumbs-up">
            <span className="thumbs-icon" aria-hidden="true">👍</span>
            <span className="thumbs-count">
              {review.thumbsUp} {review.thumbsUp === 1 ? 'людина знайшла' : 'людей знайшли'} це корисним
            </span>
          </div>
        </footer>
      )}
    </article>
  )
})

export default ReviewCard


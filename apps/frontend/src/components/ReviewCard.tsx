import React from 'react'
import { Review } from '../types'
import { formatDate, renderStars, getRatingClass } from '../utils'

interface ReviewCardProps {
  review: Review
}

export default function ReviewCard({ review }: ReviewCardProps) {

  return (
    <div className={`review-card ${review.source}`}>
      <div className="review-header">
        <div className="review-user">
          <div className="user-avatar">
            {(review.userName || 'A').charAt(0).toUpperCase()}
          </div>
          <div className="user-info">
            <div className="user-name">{review.userName || 'Anonymous'}</div>
            <div className="review-meta">
              <span className="review-date">{formatDate(review.date)}</span>
              {review.version && (
                <>
                  <span className="separator">•</span>
                  <span className="review-version">v{review.version}</span>
                </>
              )}
            </div>
          </div>
        </div>
        <div className={`source-badge ${review.source || review.platform?.toLowerCase().replace(' ', '')}`}>
          {review.platform === 'Google Play' || review.source === 'google' ? (
            <>
              <span className="source-icon">🤖</span>
              <span className="source-text">Google Play</span>
            </>
          ) : (
            <>
              <span className="source-icon">🍎</span>
              <span className="source-text">App Store</span>
            </>
          )}
        </div>
      </div>

      <div className={`review-rating ${getRatingClass(review.rating)}`}>
        <div className="stars">
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

      {review.thumbsUp !== undefined && (
        <div className="review-footer">
          <div className="thumbs-up">
            <span className="thumbs-icon">👍</span>
            <span className="thumbs-count">{review.thumbsUp} людей знайшли це корисним</span>
          </div>
        </div>
      )}
    </div>
  )
}


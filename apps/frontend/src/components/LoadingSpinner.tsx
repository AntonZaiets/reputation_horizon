import React from 'react'
import { MESSAGES } from '../constants'

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large'
  message?: string
  className?: string
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  message = MESSAGES.LOADING_REVIEWS,
  className = ''
}) => {
  const sizeClasses = {
    small: 'spinner-small',
    medium: 'spinner-medium',
    large: 'spinner-large'
  }

  return (
    <div className={`loading-container ${className}`}>
      <div className={`spinner ${sizeClasses[size]}`}></div>
      {message && <p className="loading-message">{message}</p>}
    </div>
  )
}

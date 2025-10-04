import React, { useEffect, useState } from 'react'
import { AppError } from '../types'

interface NotificationProps {
  error: AppError | null
  onClose: () => void
  autoClose?: boolean
  duration?: number
}

export const Notification: React.FC<NotificationProps> = ({
  error,
  onClose,
  autoClose = true,
  duration = 5000
}) => {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    if (error) {
      setIsVisible(true)
      
      if (autoClose) {
        const timer = setTimeout(() => {
          setIsVisible(false)
          setTimeout(onClose, 300) // Затримка для анімації
        }, duration)
        
        return () => clearTimeout(timer)
      }
    } else {
      setIsVisible(false)
    }
  }, [error, autoClose, duration, onClose])

  if (!error || !isVisible) return null

  return (
    <div className={`notification ${isVisible ? 'show' : 'hide'}`}>
      <div className="notification-content error">
        <div className="notification-icon">⚠️</div>
        <div className="notification-text">
          <h4>Помилка</h4>
          <p>{error.message}</p>
          {error.code && (
            <small>Код помилки: {error.code}</small>
          )}
        </div>
        <button 
          className="notification-close"
          onClick={() => {
            setIsVisible(false)
            setTimeout(onClose, 300)
          }}
        >
          ✕
        </button>
      </div>
    </div>
  )
}

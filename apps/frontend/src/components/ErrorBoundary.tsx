import React, { Component, ErrorInfo, ReactNode } from 'react'
import { AppError } from '../types'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: AppError | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error: {
        message: error.message,
        code: 'COMPONENT_ERROR',
        details: error.stack
      }
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="error-boundary">
          <div className="error-content">
            <h2>🚨 Щось пішло не так</h2>
            <p>Вибачте, сталася неочікувана помилка.</p>
            {this.state.error && (
              <details className="error-details">
                <summary>Деталі помилки</summary>
                <pre>{this.state.error.message}</pre>
              </details>
            )}
            <button 
              className="retry-button"
              onClick={() => this.setState({ hasError: false, error: null })}
            >
              Спробувати знову
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

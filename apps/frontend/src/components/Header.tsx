import React from 'react'

interface HeaderProps {
  onRefresh: () => void
  loading: boolean
}

export default function Header({ onRefresh, loading }: HeaderProps) {
  return (
    <header className="header" role="banner">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <img 
              src="/logo.png" 
              alt="Reputation Horizon Logo" 
              className="logo-icon"
            />
            <div className="logo-text">
              <h1>Reputation Horizon</h1>
              <p className="subtitle">Preply Reviews Monitoring</p>
            </div>
          </div>
        </div>
        <div className="header-right">
          <button 
            className={`refresh-button ${loading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={loading}
            aria-label={loading ? 'Updating data...' : 'Refresh data'}
            aria-describedby="refresh-description"
          >
            <span className="refresh-icon" aria-hidden="true">🔄</span>
            <span id="refresh-description" className="sr-only">
              {loading ? 'Updating reviews in progress' : 'Click to refresh the reviews list'}
            </span>
            {loading ? 'Updating...' : 'Refresh'}
          </button>
        </div>
      </div>
    </header>
  )
}


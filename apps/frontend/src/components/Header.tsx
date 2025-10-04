import React from 'react'

interface HeaderProps {
  onRefresh: () => void
  loading: boolean
}

export default function Header({ onRefresh, loading }: HeaderProps) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <div className="logo-icon">🎓</div>
            <div className="logo-text">
              <h1>Reputation Horizon</h1>
              <p className="subtitle">Моніторинг відгуків Preply</p>
            </div>
          </div>
        </div>
        <div className="header-right">
          <button 
            className={`refresh-button ${loading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={loading}
          >
            <span className="refresh-icon">🔄</span>
            {loading ? 'Оновлення...' : 'Оновити'}
          </button>
        </div>
      </div>
    </header>
  )
}


import React from 'react'

interface FilterBarProps {
  filter: 'all' | 'google' | 'apple'
  setFilter: (filter: 'all' | 'google' | 'apple') => void
  sortBy: 'date' | 'rating'
  setSortBy: (sortBy: 'date' | 'rating') => void
}

export default function FilterBar({ filter, setFilter, sortBy, setSortBy }: FilterBarProps) {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label>Джерело:</label>
        <div className="button-group">
          <button
            className={`filter-button ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Всі
          </button>
          <button
            className={`filter-button ${filter === 'google' ? 'active google' : ''}`}
            onClick={() => setFilter('google')}
          >
            <span>🤖</span> Google Play
          </button>
          <button
            className={`filter-button ${filter === 'apple' ? 'active apple' : ''}`}
            onClick={() => setFilter('apple')}
          >
            <span>🍎</span> App Store
          </button>
        </div>
      </div>

      <div className="filter-group">
        <label>Сортування:</label>
        <div className="button-group">
          <button
            className={`filter-button ${sortBy === 'date' ? 'active' : ''}`}
            onClick={() => setSortBy('date')}
          >
            📅 За датою
          </button>
          <button
            className={`filter-button ${sortBy === 'rating' ? 'active' : ''}`}
            onClick={() => setSortBy('rating')}
          >
            ⭐ За рейтингом
          </button>
        </div>
      </div>
    </div>
  )
}


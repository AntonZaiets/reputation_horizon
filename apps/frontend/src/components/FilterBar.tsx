import React from 'react'
import { FilterType, SortType } from '../types'

interface FilterBarProps {
  filter: FilterType
  setFilter: (filter: FilterType) => void
  sortBy: SortType
  setSortBy: (sortBy: SortType) => void
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


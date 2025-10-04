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
    <div className="filter-bar" role="toolbar" aria-label="Review filters and sorting">
      <fieldset className="filter-group">
        <legend className="filter-legend">Source:</legend>
        <div className="button-group" role="radiogroup" aria-label="Select review source">
          <button
            className={`filter-button ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
            aria-pressed={filter === 'all'}
            aria-label="Show all reviews"
          >
            <span aria-hidden="true">📊</span> All
          </button>
          <button
            className={`filter-button ${filter === 'google' ? 'active google' : ''}`}
            onClick={() => setFilter('google')}
            aria-pressed={filter === 'google'}
            aria-label="Show Google Play reviews"
          >
            <span aria-hidden="true">🤖</span> Google Play
          </button>
          <button
            className={`filter-button ${filter === 'apple' ? 'active apple' : ''}`}
            onClick={() => setFilter('apple')}
            aria-pressed={filter === 'apple'}
            aria-label="Show App Store reviews"
          >
            <span aria-hidden="true">🍎</span> App Store
          </button>
          <button
            className={`filter-button ${filter === 'trustpilot' ? 'active trustpilot' : ''}`}
            onClick={() => setFilter('trustpilot')}
            aria-pressed={filter === 'trustpilot'}
            aria-label="Show Trustpilot reviews"
          >
            <span aria-hidden="true">⭐</span> Trustpilot
          </button>
        </div>
      </fieldset>

      <fieldset className="filter-group">
        <legend className="filter-legend">Sort by:</legend>
        <div className="button-group" role="radiogroup" aria-label="Select sorting method">
          <button
            className={`filter-button ${sortBy === 'date' ? 'active' : ''}`}
            onClick={() => setSortBy('date')}
            aria-pressed={sortBy === 'date'}
            aria-label="Sort by date"
          >
            <span aria-hidden="true">📅</span> By Date
          </button>
          <button
            className={`filter-button ${sortBy === 'rating' ? 'active' : ''}`}
            onClick={() => setSortBy('rating')}
            aria-pressed={sortBy === 'rating'}
            aria-label="Sort by rating"
          >
            <span aria-hidden="true">⭐</span> By Rating
          </button>
        </div>
      </fieldset>
    </div>
  )
}


import React, { useState, useEffect } from 'react'
import './ReputationAnalysis.css'

export interface ReputationInsight {
  review_id: string
  sentiment: {
    sentiment: 'positive' | 'negative' | 'neutral'
    confidence: number
    emotional_tone: string
    intensity: 'low' | 'medium' | 'high'
  }
  intent: {
    primary_intent: 'praise' | 'complaint' | 'question' | 'suggestion' | 'bug_report' | 'feature_request'
    secondary_intents: string[]
    urgency: 'low' | 'medium' | 'high' | 'critical'
    action_required: boolean
  }
  topics: {
    main_topics: string[]
    subtopics: string[]
    keywords: string[]
    categories: string[]
  }
  priority_score: number
  recommended_action: 'none' | 'respond' | 'investigate' | 'escalate'
}

export interface ReputationScore {
  overall_score: number
  sentiment_distribution: {
    positive: number
    negative: number
    neutral: number
  }
  top_issues: string[]
  positive_aspects: string[]
  improvement_areas: string[]
  trend: 'improving' | 'declining' | 'stable'
}

export interface PriorityIssue {
  issue: string
  frequency: number
  severity: 'low' | 'medium' | 'high' | 'critical'
  affected_users: number
  recommended_response: string
  department: 'product' | 'support' | 'pr' | 'engineering'
}

export interface ReputationAnalysisData {
  reviews: any[]
  insights: ReputationInsight[]
  reputation_score: ReputationScore
  priority_issues: PriorityIssue[]
  stats: any
  analyzed_at: string
  time_range_hours: number
}

interface ReputationAnalysisProps {
  onAnalysisComplete?: (data: ReputationAnalysisData) => void
}

const ReputationAnalysis: React.FC<ReputationAnalysisProps> = ({ onAnalysisComplete }) => {
  const [analysisData, setAnalysisData] = useState<ReputationAnalysisData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'insights' | 'issues'>('overview')

  const loadAnalysis = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/reputation/analyze?hours=168&max_reviews=50')
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      setAnalysisData(data)
      onAnalysisComplete?.(data)
      
      console.log('✅ Reputation analysis loaded successfully')
    } catch (err) {
      console.error('❌ Error loading reputation analysis:', err)
      setError('Не вдалося завантажити аналіз репутації. Переконайтесь, що backend запущений.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAnalysis()
  }, [])

  const getScoreColor = (score: number) => {
    if (score >= 8) return '#10b981' // green
    if (score >= 6) return '#f59e0b' // yellow
    return '#ef4444' // red
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return '#dc2626'
      case 'high': return '#ea580c'
      case 'medium': return '#d97706'
      case 'low': return '#16a34a'
      default: return '#6b7280'
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '#10b981'
      case 'negative': return '#ef4444'
      case 'neutral': return '#6b7280'
      default: return '#6b7280'
    }
  }

  if (loading) {
    return (
      <div className="reputation-analysis">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Аналіз репутації...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="reputation-analysis">
        <div className="error-container">
          <p>❌ {error}</p>
          <button onClick={loadAnalysis} className="retry-button">
            Спробувати знову
          </button>
        </div>
      </div>
    )
  }

  if (!analysisData) {
    return (
      <div className="reputation-analysis">
        <p>Немає даних для аналізу</p>
      </div>
    )
  }

  return (
    <div className="reputation-analysis">
      <div className="analysis-header">
        <h2>🤖 AI Аналіз Репутації</h2>
        <div className="analysis-meta">
          <span>Проаналізовано {analysisData.insights.length} відгуків</span>
          <span>•</span>
          <span>За {analysisData.time_range_hours} годин</span>
          <button onClick={loadAnalysis} className="refresh-button">
            🔄 Оновити
          </button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Огляд
        </button>
        <button 
          className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          🔍 Детальний аналіз
        </button>
        <button 
          className={`tab ${activeTab === 'issues' ? 'active' : ''}`}
          onClick={() => setActiveTab('issues')}
        >
          ⚠️ Пріоритетні проблеми
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="overview-tab">
          <div className="score-card">
            <h3>Загальна оцінка репутації</h3>
            <div className="score-display">
              <div 
                className="score-circle"
                style={{ borderColor: getScoreColor(analysisData.reputation_score.overall_score) }}
              >
                {analysisData.reputation_score.overall_score.toFixed(1)}
              </div>
              <div className="score-details">
                <p>Тренд: <span className={`trend ${analysisData.reputation_score.trend}`}>
                  {analysisData.reputation_score.trend === 'improving' ? '📈 Покращується' :
                   analysisData.reputation_score.trend === 'declining' ? '📉 Погіршується' : '➡️ Стабільний'}
                </span></p>
              </div>
            </div>
          </div>

          <div className="sentiment-distribution">
            <h3>Розподіл тональності</h3>
            <div className="sentiment-bars">
              <div className="sentiment-bar">
                <span className="sentiment-label positive">Позитивні</span>
                <div className="bar-container">
                  <div 
                    className="bar positive"
                    style={{ width: `${(analysisData.reputation_score.sentiment_distribution.positive / analysisData.insights.length) * 100}%` }}
                  ></div>
                </div>
                <span className="sentiment-count">{analysisData.reputation_score.sentiment_distribution.positive}</span>
              </div>
              <div className="sentiment-bar">
                <span className="sentiment-label neutral">Нейтральні</span>
                <div className="bar-container">
                  <div 
                    className="bar neutral"
                    style={{ width: `${(analysisData.reputation_score.sentiment_distribution.neutral / analysisData.insights.length) * 100}%` }}
                  ></div>
                </div>
                <span className="sentiment-count">{analysisData.reputation_score.sentiment_distribution.neutral}</span>
              </div>
              <div className="sentiment-bar">
                <span className="sentiment-label negative">Негативні</span>
                <div className="bar-container">
                  <div 
                    className="bar negative"
                    style={{ width: `${(analysisData.reputation_score.sentiment_distribution.negative / analysisData.insights.length) * 100}%` }}
                  ></div>
                </div>
                <span className="sentiment-count">{analysisData.reputation_score.sentiment_distribution.negative}</span>
              </div>
            </div>
          </div>

          <div className="top-issues">
            <h3>Топ проблеми</h3>
            <ul>
              {analysisData.reputation_score.top_issues.map((issue, index) => (
                <li key={index} className="issue-item">
                  <span className="issue-rank">#{index + 1}</span>
                  <span className="issue-text">{issue}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="positive-aspects">
            <h3>Позитивні аспекти</h3>
            <div className="aspects-grid">
              {analysisData.reputation_score.positive_aspects.map((aspect, index) => (
                <div key={index} className="aspect-tag positive">
                  ✅ {aspect}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'insights' && (
        <div className="insights-tab">
          <h3>Детальний аналіз відгуків</h3>
          <div className="insights-grid">
            {analysisData.insights.map((insight, index) => (
              <div key={insight.review_id} className="insight-card">
                <div className="insight-header">
                  <span className="review-id">Відгук #{index + 1}</span>
                  <span 
                    className="priority-badge"
                    style={{ backgroundColor: getScoreColor(insight.priority_score) }}
                  >
                    Пріоритет: {insight.priority_score.toFixed(1)}
                  </span>
                </div>
                
                <div className="insight-content">
                  <div className="sentiment-info">
                    <span 
                      className="sentiment-badge"
                      style={{ backgroundColor: getSentimentColor(insight.sentiment.sentiment) }}
                    >
                      {insight.sentiment.sentiment === 'positive' ? '😊 Позитивний' :
                       insight.sentiment.sentiment === 'negative' ? '😞 Негативний' : '😐 Нейтральний'}
                    </span>
                    <span className="confidence">Впевненість: {(insight.sentiment.confidence * 100).toFixed(0)}%</span>
                  </div>
                  
                  <div className="intent-info">
                    <strong>Намір:</strong> {insight.intent.primary_intent}
                    {insight.intent.action_required && (
                      <span className="action-required">⚠️ Потребує дії</span>
                    )}
                  </div>
                  
                  <div className="topics-info">
                    <strong>Теми:</strong> {insight.topics.main_topics.join(', ')}
                  </div>
                  
                  <div className="recommended-action">
                    <strong>Рекомендована дія:</strong> {insight.recommended_action}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'issues' && (
        <div className="issues-tab">
          <h3>Пріоритетні проблеми</h3>
          {analysisData.priority_issues.length === 0 ? (
            <p className="no-issues">🎉 Немає критичних проблем!</p>
          ) : (
            <div className="issues-list">
              {analysisData.priority_issues.map((issue, index) => (
                <div key={index} className="priority-issue-card">
                  <div className="issue-header">
                    <h4>{issue.issue}</h4>
                    <span 
                      className="severity-badge"
                      style={{ backgroundColor: getSeverityColor(issue.severity) }}
                    >
                      {issue.severity === 'critical' ? '🚨 Критична' :
                       issue.severity === 'high' ? '⚠️ Висока' :
                       issue.severity === 'medium' ? '⚡ Середня' : 'ℹ️ Низька'}
                    </span>
                  </div>
                  
                  <div className="issue-stats">
                    <div className="stat">
                      <span className="stat-label">Частота:</span>
                      <span className="stat-value">{issue.frequency} разів</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Зачеплені користувачі:</span>
                      <span className="stat-value">{issue.affected_users}</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Відділ:</span>
                      <span className="stat-value">{issue.department}</span>
                    </div>
                  </div>
                  
                  <div className="issue-recommendation">
                    <strong>Рекомендована реакція:</strong>
                    <p>{issue.recommended_response}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ReputationAnalysis

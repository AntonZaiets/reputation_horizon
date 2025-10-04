import React, { useState } from 'react';
import './GoogleReputationAnalysis.css';

interface GoogleReputationAnalysisProps {
  onClose?: () => void;
  data?: AnalysisResult | null;
  loading?: boolean;
  error?: string | null;
}

interface AnalysisResult {
  company: string;
  analysis: string;
  source: string;
  raw_data: Array<{
    title: string;
    link: string;
    snippet: string;
    source: string;
  }>;
}

interface JSONAnalysisData {
  overall_score: {
    rating: string;
    brief_reason: string;
  };
  key_strengths: Array<{
    name?: string;
    strength?: string;
    impact: string;
    explanation?: string;
  }>;
  critical_issues: Array<{
    issue: string;
    severity: string;
    explanation?: string;
    why_critical?: string;
  }>;
  risk_assessment: {
    overall_business_impact: string;
    main_risks: Array<{
      name?: string;
      risk?: string;
      likelihood: string;
      consequence: string;
    }>;
  };
  priority_actions: Array<{
    action: string;
    urgency: string;
    expected_impact: string;
  }>;
  data_sources: number;
}

const JSONAnalysis: React.FC<{ data: JSONAnalysisData }> = ({ data }) => {
  // Перевіряємо, чи дані існують
  if (!data) {
    return <div className="error-message">No analysis data available</div>;
  }
  const getSeverityColor = (severity: string | undefined) => {
    if (!severity) return '#6b7280';
    switch (severity.toLowerCase()) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getUrgencyColor = (urgency: string | undefined) => {
    if (!urgency) return '#6b7280';
    switch (urgency.toLowerCase()) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className="json-analysis">
      {/* Overall Score */}
      <div className="score-section">
        <div className="score-card">
          <div className="score-rating">{data.overall_score?.rating || 'N/A'}</div>
          <p className="score-reason">{data.overall_score?.brief_reason || 'No rating available'}</p>
        </div>
      </div>

      {/* Key Strengths */}
      <div className="strengths-section">
        <h3>✅ Key Strengths</h3>
        <div className="strengths-grid">
          {data.key_strengths?.map((strength, index) => (
            <div key={index} className="strength-card">
              <h4>{strength.name || strength.strength}</h4>
              <div className="impact-badge" style={{ backgroundColor: getSeverityColor(strength.impact) }}>
                {strength.impact} impact
              </div>
              {strength.explanation && <p>{strength.explanation}</p>}
            </div>
          )) || []}
        </div>
      </div>

      {/* Critical Issues */}
      <div className="issues-section">
        <h3>⚠️ Critical Issues</h3>
        <div className="issues-grid">
          {data.critical_issues?.map((issue, index) => (
            <div key={index} className="issue-card">
              <div className="issue-header">
                <h4>{issue.issue}</h4>
                <div className="severity-badge" style={{ backgroundColor: getSeverityColor(issue.severity) }}>
                  {issue.severity} severity
                </div>
              </div>
              {(issue.explanation || issue.why_critical) && (
                <p className="issue-explanation">{issue.explanation || issue.why_critical}</p>
              )}
            </div>
          )) || []}
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="risks-section">
        <h3>🎯 Risk Assessment</h3>
        <div className="risk-overview">
          <p className="risk-impact">{data.risk_assessment?.overall_business_impact}</p>
        </div>
        <div className="risks-grid">
          {data.risk_assessment?.main_risks?.map((risk, index) => (
            <div key={index} className="risk-card">
              <h4>{risk.name || risk.risk}</h4>
              <div className="risk-metrics">
                <span className="likelihood">Likelihood: {risk.likelihood}</span>
                <span className="consequence">Consequence: {risk.consequence}</span>
              </div>
            </div>
          )) || []}
        </div>
      </div>

      {/* Priority Actions */}
      <div className="actions-section">
        <h3>🚀 Priority Actions</h3>
        <div className="actions-grid">
          {data.priority_actions?.map((action, index) => (
            <div key={index} className="action-card">
              <h4>{action.action}</h4>
              <div className="action-metrics">
                <div className="urgency-badge" style={{ backgroundColor: getUrgencyColor(action.urgency) }}>
                  {action.urgency} urgency
                </div>
                <div className="impact-badge" style={{ backgroundColor: getSeverityColor(action.expected_impact) }}>
                  {action.expected_impact} impact
                </div>
              </div>
            </div>
          )) || []}
        </div>
      </div>

      {/* Data Sources */}
      <div className="sources-info">
        <p className="sources-count">📑 Analyzed {data.data_sources || 0} data sources</p>
      </div>
    </div>
  );
};

export const GoogleReputationAnalysis: React.FC<GoogleReputationAnalysisProps> = ({ 
  onClose, 
  data, 
  loading, 
  error 
}) => {
  // Автоматично показуємо результати, якщо дані є
  const showResults = !!data && !loading;

  // Використовуємо дані з пропсів
  const result = data;
  const isLoading = loading || false;
  const errorMessage = error;

  const formatAnalysis = (analysis: string) => {
    try {
      // Спробуємо парсити як JSON
      const jsonMatch = analysis.match(/json\s*(\{[\s\S]*\})/);
      if (jsonMatch) {
        const jsonStr = jsonMatch[1];
        const parsedData = JSON.parse(jsonStr);
        return <JSONAnalysis data={parsedData} />;
      }
    } catch (error) {
      console.log('Не вдалося парсити JSON, використовуємо текстовий формат');
    }

    // Якщо не JSON, використовуємо старий формат
    const sections = analysis.split(/\n\n+/);
    return sections.map((section, index) => (
      <div key={index} className="analysis-section">
        {section.split('\n').map((line, lineIndex) => {
          // Заголовки секцій
          if (line.match(/^\d+\./)) {
            return <h3 key={lineIndex} className="section-title">{line}</h3>;
          }
          // Підзаголовки з тире
          if (line.startsWith('- ') && line.includes(':')) {
            return <h4 key={lineIndex} className="subsection-title">{line}</h4>;
          }
          // Пункти списку
          if (line.startsWith('  - ') || line.startsWith('- ')) {
            return <li key={lineIndex} className="list-item">{line.replace(/^[\s-]+/, '')}</li>;
          }
          // Звичайний текст
          return line ? <p key={lineIndex} className="text-line">{line}</p> : null;
        })}
      </div>
    ));
  };

  return (
    <div className="google-reputation-container">
      {isLoading && (
        <div className="intro-section">
          <p className="intro-text">
            This tool uses Google Search API to find information about Preply's reputation 
            and OpenAI for deep analysis of the found data.
          </p>
          <div className="analyze-btn" style={{ cursor: 'default' }}>
            <span className="spinner"></span>
            Analyzing...
          </div>
        </div>
      )}

      {errorMessage && (
        <div className="error-message">
          <h3>❌ Error</h3>
          <p>{errorMessage}</p>
        </div>
      )}

      {showResults && result && (
        <div className="results-container">
          <div className="analysis-content">
            {formatAnalysis(result.analysis)}
          </div>

          <div className="raw-data-section">
            <h3>📑 Data Sources ({result.raw_data.length})</h3>
            <div className="sources-grid">
              {result.raw_data.map((item, index) => (
                <div key={index} className="source-card">
                  <h4 className="source-title">{item.title}</h4>
                  <p className="source-snippet">{item.snippet}</p>
                  <a 
                    href={item.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="source-link"
                  >
                    View Source →
                  </a>
                </div>
              ))}
            </div>
          </div>

          <button 
            className="new-analysis-btn"
            onClick={() => {
              // Можна додати логіку для нового аналізу
            }}
          >
            Hide Results
          </button>
        </div>
      )}
    </div>
  );
};

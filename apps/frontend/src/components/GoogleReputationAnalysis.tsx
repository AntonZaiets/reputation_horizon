import React, { useState } from 'react';
import './GoogleReputationAnalysis.css';

interface GoogleReputationAnalysisProps {
  onClose?: () => void;
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

export const GoogleReputationAnalysis: React.FC<GoogleReputationAnalysisProps> = ({ onClose }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const analyzeReputation = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/reputation/analyze/preply');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не вдалося виконати аналіз');
    } finally {
      setLoading(false);
    }
  };

  const formatAnalysis = (analysis: string) => {
    // Розбиваємо на секції
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
      <div className="header">
        <h2>🔍 Аналіз репутації через Google Search</h2>
        {onClose && (
          <button className="close-btn" onClick={onClose}>✕</button>
        )}
      </div>

      {!result && (
        <div className="intro-section">
          <p className="intro-text">
            Цей інструмент використовує Google Search API для пошуку інформації про репутацію Preply 
            та OpenAI для глибокого аналізу знайдених даних.
          </p>
          <button 
            className="analyze-btn"
            onClick={analyzeReputation}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Аналізую...
              </>
            ) : (
              <>
                <span className="icon">🔍</span>
                Запустити аналіз репутації
              </>
            )}
          </button>
        </div>
      )}

      {error && (
        <div className="error-message">
          <h3>❌ Помилка</h3>
          <p>{error}</p>
          <button onClick={analyzeReputation} className="retry-btn">
            Спробувати знову
          </button>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="company-info">
            <h2>📊 Компанія: {result.company}</h2>
            <span className="source-badge">{result.source}</span>
          </div>

          <div className="analysis-content">
            {formatAnalysis(result.analysis)}
          </div>

          <div className="raw-data-section">
            <h3>📑 Джерела даних ({result.raw_data.length})</h3>
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
                    Переглянути джерело →
                  </a>
                </div>
              ))}
            </div>
          </div>

          <button 
            className="new-analysis-btn"
            onClick={() => {
              setResult(null);
              setError(null);
            }}
          >
            Новий аналіз
          </button>
        </div>
      )}
    </div>
  );
};

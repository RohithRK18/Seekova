import { FileText, ExternalLink, Sparkles } from "lucide-react";
import { useState } from "react";

function SearchResult({ result, activeMode }) {
  const relevance = Math.round(result.score * 100);
  const [showInsight, setShowInsight] = useState(false);

  return (
    <article className="result-card">
      <div className="result-icon">
        <FileText size={20} />
      </div>

      <div className="result-body">
        <div className="result-meta">
          <span className="file-badge">{result.file_type}</span>
          <span className="score-badge">Cosine Similarity: {result.score}</span>
        </div>

        <h2>{result.title}</h2>

        <p>
          {result.content}
          {result.content.length >= 500 ? "..." : ""}
        </p>

        <div className="result-actions">
          <button
            className="insight-btn"
            onClick={() => setShowInsight(!showInsight)}
          >
            <Sparkles size={14} />
            {showInsight ? "Hide Insight" : "Seekova Insight"}
          </button>
        </div>

        {showInsight && (
          <div className="insight-panel">
            <div className="insight-header">
              <Sparkles size={16} className="insight-sparkle" />
              <span>SEEKOVA INSIGHT</span>
            </div>
            <p>
              This document <strong>"{result.title}"</strong> achieved a{" "}
              <strong>{relevance}% match score</strong> under the{" "}
              <strong>{activeMode.toUpperCase()}</strong> mode using TF-IDF term
              weighting and n-gram cosine vector alignment.
            </p>
            <div className="insight-metrics">
              <div>
                <span className="metric-label">Document ID</span>
                <span className="metric-val">{result.id.slice(0, 8)}...</span>
              </div>
              <div>
                <span className="metric-label">Relevance Index</span>
                <span className="metric-val">{relevance} / 100</span>
              </div>
              <div>
                <span className="metric-label">Engine Mode</span>
                <span className="metric-val">{activeMode}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="relevance">
        <div
          className="relevance-circle"
          style={{ "--score": `${relevance}%` }}
        >
          {relevance}%
        </div>
      </div>
    </article>
  );
}

export default SearchResult;

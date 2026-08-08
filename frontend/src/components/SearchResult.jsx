import { FileText, Sparkles, Copy, Check } from "lucide-react";
import { useState } from "react";

function SearchResult({ result, activeMode, query }) {
  const relevance = Math.round(result.score * 100);
  const [showInsight, setShowInsight] = useState(false);
  const [copied, setCopied] = useState(false);

  function copySnippet() {
    navigator.clipboard.writeText(`${result.title}\n\n${result.content}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const STOP_TERMS = new Set([
    "what", "where", "who", "when", "how", "is", "are", "the", "a", "an", "in", "on",
    "of", "to", "for", "and", "or", "me", "tell", "explain", "about", "this", "that", "with"
  ]);

  // Highlight query keywords in text strictly on word boundaries
  function renderHighlighted(text) {
    if (!query || !query.trim()) return text;
    const terms = query
      .trim()
      .split(/\s+/)
      .map((t) => t.toLowerCase().replace(/[^a-z0-9]/g, ""))
      .filter((t) => t.length > 1 && !STOP_TERMS.has(t))
      .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));

    if (terms.length === 0) return text;

    const regex = new RegExp(`\\b(${terms.join("|")})\\b`, "gi");
    const parts = text.split(regex);

    return parts.map((part, i) =>
      terms.some((term) => term.toLowerCase() === part.toLowerCase()) ? (
        <mark key={i} className="highlight-term">
          {part}
        </mark>
      ) : (
        part
      )
    );
  }

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

        <h2>{renderHighlighted(result.title)}</h2>

        <p>
          {renderHighlighted(result.content)}
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

          <button className="copy-snippet-btn" onClick={copySnippet} title="Copy Snippet">
            {copied ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
            <span>{copied ? "Copied" : "Copy"}</span>
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

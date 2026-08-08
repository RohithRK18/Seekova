import React from "react";
import {
  FileText,
  ExternalLink,
  Shield,
  BookOpen,
  Sparkles,
  Copy,
  Check
} from "lucide-react";
import { useState } from "react";

function SourceCard({ result, activeMode, query, citationNumber }) {
  const relevance = Math.round(result.score * 100);
  const [copied, setCopied] = useState(false);

  function copySnippet() {
    navigator.clipboard.writeText(`${result.title}\n\n${result.content}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <article className="seekova-source-card">
      <div className="card-top-bar">
        <div className="source-citation-badge">
          <span>[{citationNumber}]</span>
        </div>
        <div className="source-file-type">
          <FileText size={13} />
          <span>{result.file_type || ".md"}</span>
        </div>
        <div className="relevance-pill">
          <Shield size={12} />
          <span>{relevance}% Relevance</span>
        </div>
      </div>

      <h3 className="source-card-title">{result.title}</h3>

      <p className="source-card-excerpt">
        {result.content.slice(0, 240)}
        {result.content.length > 240 ? "..." : ""}
      </p>

      <div className="source-card-footer">
        <span className="cosine-score">Cosine Score: {result.score}</span>
        <button
          className="copy-card-btn"
          onClick={copySnippet}
          title="Copy Document Excerpt"
        >
          {copied ? (
            <>
              <Check size={12} color="#10b981" />
              <span>Copied</span>
            </>
          ) : (
            <>
              <Copy size={12} />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
    </article>
  );
}

export default SourceCard;

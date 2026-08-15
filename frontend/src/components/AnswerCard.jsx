import React, { useState } from "react";
import { Sparkles, ShieldCheck, Copy, Check, RotateCw, Bookmark, Share2, Layers, BookOpen, Clock, Tag } from "lucide-react";
import WhyThisAnswer from "./WhyThisAnswer";
import { MindMapRenderer, TimelineRenderer } from "./VisualizationRenderers";

function AnswerCard({ query, answer, activeMode, topDoc, onRegenerate, onSelectSearch }) {
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);
  const [showWhy, setShowWhy] = useState(false);
  const [viewLevel, setViewLevel] = useState("standard"); // "simple" | "standard" | "deep"

  if (!answer) return null;

  function copyAnswer() {
    if (!answer.text) return;
    const currentText = viewLevel === "simple" && answer.explain_simply
      ? answer.explain_simply
      : viewLevel === "deep" && answer.deep_dive
      ? answer.deep_dive
      : answer.text;

    const textToCopy = `✦ SECONDLYBRAIN ANSWER: ${query}\n\n${currentText}\n\nKey Insights:\n` +
      (answer.key_takeaways || []).map(t => `• ${t}`).join("\n");
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function saveInsight() {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  }

  function shareInsight() {
    if (navigator.share) {
      navigator.share({
        title: `SECONDLYBRAIN: ${query}`,
        text: answer.text?.slice(0, 150) + "...",
        url: window.location.href,
      }).catch(() => {});
    } else {
      copyAnswer();
    }
  }

  // Render markdown text cleanly
  function renderFormattedText(rawText) {
    if (!rawText) return null;
    const lines = rawText.split("\n");
    let inCodeBlock = false;
    let codeContent = [];
    let codeLanguage = "";
    let inTable = false;
    let tableRows = [];

    const elements = [];

    lines.forEach((line, idx) => {
      // Code block detection
      if (line.trim().startsWith("```")) {
        if (inCodeBlock) {
          // Close code block
          elements.push(
            <div key={`code-${idx}`} className="secondlybrain-code-wrapper">
              <div className="code-header">
                <span className="code-lang">{codeLanguage || "code"}</span>
                <button
                  className="copy-code-btn"
                  onClick={() => navigator.clipboard.writeText(codeContent.join("\n"))}
                >
                  <Copy size={12} />
                  <span>Copy Code</span>
                </button>
              </div>
              <pre className="code-content">
                <code>{codeContent.join("\n")}</code>
              </pre>
            </div>
          );
          inCodeBlock = false;
          codeContent = [];
          codeLanguage = "";
        } else {
          inCodeBlock = true;
          codeLanguage = line.trim().replace("```", "");
        }
        return;
      }

      if (inCodeBlock) {
        codeContent.push(line);
        return;
      }

      // Markdown Table detection
      if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
        inTable = true;
        tableRows.push(line.trim());
        return;
      } else if (inTable) {
        // Render completed table
        const parsedHeaders = tableRows[0].split("|").filter(c => c.trim().length > 0).map(c => c.trim());
        const contentRows = tableRows.slice(2).map(r => r.split("|").filter(c => c.trim().length > 0).map(c => c.trim()));

        elements.push(
          <div key={`table-${idx}`} className="table-responsive-wrapper">
            <table className="secondlybrain-markdown-table">
              <thead>
                <tr>
                  {parsedHeaders.map((h, i) => (
                    <th key={i}>{h.replace(/\*\*/g, '')}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {contentRows.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((cell, cIdx) => (
                      <td key={cIdx}>{cell.replace(/\*\*/g, '')}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        inTable = false;
        tableRows = [];
      }

      // Helper to format inline bold text **word**
      const parseInlineStyles = (txt) => {
        const parts = txt.split(/(\*\*.*?\*\*)/g);
        return parts.map((part, i) => {
          if (part.startsWith("**") && part.endsWith("**")) {
            return <strong key={i} style={{ color: "#ffffff", fontWeight: 700 }}>{part.slice(2, -2)}</strong>;
          }
          return part;
        });
      };

      // Headers
      if (line.startsWith("# ")) {
        elements.push(<h1 key={idx} className="answer-section-h1" style={{ fontSize: "22px", fontWeight: 800, color: "#ffffff", margin: "16px 0 10px 0" }}>{parseInlineStyles(line.replace("# ", ""))}</h1>);
      } else if (line.startsWith("## ")) {
        elements.push(<h2 key={idx} className="answer-section-h2">{parseInlineStyles(line.replace("## ", ""))}</h2>);
      } else if (line.startsWith("### ")) {
        elements.push(<h3 key={idx} className="answer-section-h3">{parseInlineStyles(line.replace("### ", ""))}</h3>);
      } else if (line.startsWith("- ") || line.startsWith("* ")) {
        elements.push(
          <li key={idx} className="answer-bullet-item">
            <span className="bullet-dot">•</span>
            <span>{parseInlineStyles(line.replace(/^[-*]\s+/, ""))}</span>
          </li>
        );
      } else if (line.trim().length > 0) {
        elements.push(<p key={idx} className="answer-paragraph-text">{parseInlineStyles(line)}</p>);
      }
    });

    return elements;
  }

  const activeText = viewLevel === "simple" && answer.explain_simply
    ? answer.explain_simply
    : viewLevel === "deep" && answer.deep_dive
    ? answer.deep_dive
    : answer.text;

  return (
    <div className="secondlybrain-answer-card-v2">
      {/* Top Card Navigation & Domain Metadata */}
      <div className="answer-card-header-bar">
        <div className="brand-identity-tag">
          <Sparkles size={16} className="orb-sparkle-icon" />
          <span className="card-brand-name">SECONDLYBRAIN ANSWER</span>
        </div>

        <div className="answer-card-controls">
          {/* Level Toggle: [Simple] [Standard] [Deep Dive] */}
          <div className="level-toggle-group">
            <button
              className={`toggle-btn ${viewLevel === "simple" ? "active" : ""}`}
              onClick={() => setViewLevel("simple")}
              title="Explain simply for beginners"
            >
              Simple
            </button>
            <button
              className={`toggle-btn ${viewLevel === "standard" ? "active" : ""}`}
              onClick={() => setViewLevel("standard")}
            >
              Standard
            </button>
            <button
              className={`toggle-btn ${viewLevel === "deep" ? "active" : ""}`}
              onClick={() => setViewLevel("deep")}
              title="Deep technical perspective"
            >
              Deep Dive
            </button>
          </div>

          <button className="icon-action-btn" onClick={copyAnswer} title="Copy formatted answer">
            {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
          </button>

          <button className="icon-action-btn" onClick={saveInsight} title="Save to Knowledge Base">
            {saved ? <Check size={14} color="#10b981" /> : <Bookmark size={14} />}
          </button>

          <button className="icon-action-btn" onClick={shareInsight} title="Share Answer">
            <Share2 size={14} />
          </button>

          {onRegenerate && (
            <button className="icon-action-btn" onClick={onRegenerate} title="Regenerate Answer">
              <RotateCw size={14} />
            </button>
          )}
        </div>
      </div>

      {/* Metadata Row */}
      <div className="answer-query-heading-box">
        <div className="metadata-pills-row">
          <span className="reading-time-pill">
            <Clock size={12} />
            {answer.reading_time || "~2 min read"}
          </span>

          <span className="confidence-pill">
            <ShieldCheck size={12} />
            Confidence · {answer.confidence || "High"}
          </span>
        </div>
      </div>

      {/* Answer Body with Rich Markdown & Code Blocks */}
      <div className="answer-card-content-body">
        {renderFormattedText(activeText)}

        {/* Dynamic Visualization Rendering (MindMap / Timeline) */}
        {answer.visualization && answer.visualization.type === "mindmap" && (
          <MindMapRenderer data={answer.visualization} />
        )}

        {answer.visualization && answer.visualization.type === "timeline" && (
          <TimelineRenderer data={answer.visualization} />
        )}

        {/* Key Takeaways Box */}
        {answer.key_takeaways && answer.key_takeaways.length > 0 && (
          <div className="secondlybrain-takeaways-box">
            <div className="takeaways-header">
              <Layers size={15} />
              <span>KEY INSIGHTS & TAKEAWAYS</span>
            </div>
            <ul className="takeaways-grid-list">
              {answer.key_takeaways.map((takeaway, tIdx) => (
                <li key={tIdx} className="takeaway-card-item">
                  <span className="bullet-num">{tIdx + 1}</span>
                  <span>{takeaway}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Sources Footer Summary */}
        {answer.sources && answer.sources.length > 0 && (
          <div className="card-sources-meta-footer">
            <span>Sources used ({answer.sources.length})</span>
            {answer.is_current_info && (
              <span className="live-update-badge">• Updated real-time information</span>
            )}
          </div>
        )}
      </div>

      {/* Follow-up Questions ("Continue Exploring") */}
      {answer.follow_up_questions && answer.follow_up_questions.length > 0 && (
        <div className="secondlybrain-followups-footer">
          <span className="followup-title">Continue exploring</span>
          <div className="followup-pills-container">
            {answer.follow_up_questions.map((fq, fIdx) => (
              <button
                key={fIdx}
                className="followup-pill-btn"
                onClick={() => onSelectSearch && onSelectSearch(fq)}
              >
                <span>{fq}</span>
                <span className="arrow">→</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnswerCard;

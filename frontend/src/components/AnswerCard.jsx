import React, { useState } from "react";
import { Sparkles, ShieldCheck, Copy, Check, Info } from "lucide-react";
import WhyThisAnswer from "./WhyThisAnswer";

function AnswerCard({ query, answer, activeMode, topDoc }) {
  const [copied, setCopied] = useState(false);
  const [showWhy, setShowWhy] = useState(false);

  if (!answer) return null;

  function copyAnswer() {
    if (!answer.text) return;
    const textToCopy = `${answer.text}\n\nKey Takeaways:\n` +
      (answer.key_takeaways || []).map(t => `• ${t}`).join("\n");
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="seekova-answer-card">
      <div className="answer-header">
        <div className="answer-title-group">
          <div className="sparkle-badge">
            <Sparkles size={16} />
          </div>
          <div>
            <h2 className="answer-heading">SecondlyBrain Synthesized Answer</h2>
            <span className="answer-subtext">Direct answer computed from corpus TF-IDF alignment</span>
          </div>
        </div>

        <div className="answer-meta-badges">
          <div className={`mode-badge mode-${activeMode}`}>
            <span>{activeMode.toUpperCase()} MODE</span>
          </div>
          <div className="confidence-badge">
            <ShieldCheck size={14} />
            <span>{answer.confidence || 95}% Confidence</span>
          </div>
          <button
            className="why-btn"
            onClick={() => setShowWhy(!showWhy)}
            title="Why this answer?"
          >
            <Info size={13} />
            <span>{showWhy ? "Hide Why" : "Why this answer?"}</span>
          </button>
          <button className="copy-answer-btn" onClick={copyAnswer} title="Copy Answer">
            {copied ? (
              <>
                <Check size={13} color="#10b981" />
                <span style={{ color: "#10b981" }}>Copied!</span>
              </>
            ) : (
              <>
                <Copy size={13} />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="answer-body">
        <p className="answer-text">{answer.text}</p>

        {answer.key_takeaways && answer.key_takeaways.length > 0 && (
          <div className="takeaways-section">
            <h4 className="takeaways-title">Key Insights & Corpus Takeaways</h4>
            <ul className="takeaways-list">
              {answer.key_takeaways.map((item, idx) => (
                <li key={idx}>
                  <span className="takeaway-bullet">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {showWhy && <WhyThisAnswer query={query} answer={answer} topDoc={topDoc} />}
      </div>
    </div>
  );
}

export default AnswerCard;

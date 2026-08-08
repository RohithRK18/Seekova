import { Sparkles, Check, Copy, ShieldCheck, Zap, BookOpen, Compass } from "lucide-react";
import { useState } from "react";

function AnswerCard({ query, answer, activeMode }) {
  const [copied, setCopied] = useState(false);

  if (!answer) return null;

  function copyAnswer() {
    if (!answer.text) return;
    const textToCopy = `${answer.text}\n\nKey Takeaways:\n` + 
      (answer.key_takeaways || []).map(t => `• ${t}`).join("\n");
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const modeIcons = {
    deep: <Sparkles size={16} className="mode-icon deep" />,
    fast: <Zap size={16} className="mode-icon fast" />,
    creative: <Compass size={16} className="mode-icon creative" />,
    academic: <BookOpen size={16} className="mode-icon academic" />
  };

  return (
    <div className="answer-card">
      <div className="answer-card-header">
        <div className="answer-title-group">
          <div className="sparkle-badge">
            <Sparkles size={18} />
          </div>
          <div>
            <h2 className="answer-heading">AI Synthesized Answer</h2>
            <span className="answer-subtext">Direct answer computed from corpus TF-IDF alignment</span>
          </div>
        </div>

        <div className="answer-meta-badges">
          <div className={`mode-badge mode-${activeMode}`}>
            {modeIcons[activeMode] || <Sparkles size={14} />}
            <span>{activeMode.toUpperCase()} MODE</span>
          </div>
          <div className="confidence-badge">
            <ShieldCheck size={14} />
            <span>{answer.confidence || 95}% Confidence</span>
          </div>
          <button className="copy-answer-btn" onClick={copyAnswer} title="Copy Answer">
            {copied ? (
              <>
                <Check size={14} color="#10b981" />
                <span style={{ color: "#10b981" }}>Copied!</span>
              </>
            ) : (
              <>
                <Copy size={14} />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="answer-card-body">
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
      </div>
    </div>
  );
}

export default AnswerCard;

import React from "react";
import { HelpCircle, ArrowRight } from "lucide-react";

function RelatedQuestions({ query, onSelectSearch }) {
  if (!query) return null;

  const cleanQ = query.replace(/[?._!]/g, "").trim();

  const questions = [
    `What are the core fundamentals of ${cleanQ}?`,
    `How does ${cleanQ} compare to classical alternatives?`,
    `What are the real-world applications of ${cleanQ}?`,
    `What are the key technical challenges in ${cleanQ}?`
  ];

  return (
    <div className="related-questions-card">
      <div className="related-header">
        <HelpCircle size={15} className="related-icon" />
        <span>CONTINUE EXPLORING & RELATED QUESTIONS</span>
      </div>

      <div className="related-grid">
        {questions.map((q, idx) => (
          <button
            key={idx}
            className="related-question-pill"
            onClick={() => onSelectSearch(q)}
          >
            <span>{q}</span>
            <ArrowRight size={13} className="pill-arrow" />
          </button>
        ))}
      </div>
    </div>
  );
}

export default RelatedQuestions;

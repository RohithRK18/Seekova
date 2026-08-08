import React from "react";
import { GitBranch, ChevronRight, Search } from "lucide-react";

function SearchJourney({ query, onSelectSearch }) {
  if (!query) return null;

  const journeySteps = [
    { label: query, type: "current" },
    { label: `What is the core definition of ${query.slice(0, 20)}?`, type: "node" },
    { label: `Key architecture & structural breakdown of ${query.slice(0, 18)}`, type: "node" },
    { label: `Real-world applications & technical implementation of ${query.slice(0, 18)}`, type: "node" }
  ];

  return (
    <div className="search-journey-panel">
      <div className="journey-header">
        <GitBranch size={15} className="journey-icon" />
        <span>SEARCH JOURNEY & EXPLORATION PATH</span>
      </div>
      <div className="journey-timeline">
        {journeySteps.map((step, idx) => (
          <div key={idx} className={`journey-step ${step.type}`}>
            <div className="step-node-dot" />
            <button
              className="step-button"
              onClick={() => onSelectSearch(step.label)}
            >
              <span>{step.label}</span>
              <ChevronRight size={13} className="step-arrow" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchJourney;

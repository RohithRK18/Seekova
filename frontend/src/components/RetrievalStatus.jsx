import React from "react";
import { Cpu, Search, Sparkles, CheckCircle2 } from "lucide-react";
import { SecondlyBrainOrb } from "./SecondlyBrainLogo";

function RetrievalStatus({ statusStage, statusMessage }) {
  const stages = [
    { id: "understanding", label: "Understanding question" },
    { id: "retrieving", label: "Searching knowledge base & sources" },
    { id: "synthesizing", label: "Analyzing context" },
    { id: "chunk", label: "Generating structured answer" }
  ];

  const currentIdx = stages.findIndex(s => s.id === statusStage);

  return (
    <div className="secondlybrain-retrieval-status-card">
      <div className="status-header-row">
        <SecondlyBrainOrb state="searching" size={40} />
        <div className="status-text-group">
          <span className="status-eyebrow">SECONDLYBRAIN REASONING PIPELINE</span>
          <h3 className="status-main-message">{statusMessage || "Processing query..."}</h3>
        </div>
      </div>

      <div className="status-pipeline-steps">
        {stages.map((stage, idx) => {
          const isDone = currentIdx > idx;
          const isCurrent = statusStage === stage.id || (statusStage === "complete" && idx === stages.length - 1);

          return (
            <div
              key={stage.id}
              className={`pipeline-step-pill ${isDone ? "done" : isCurrent ? "active" : "pending"}`}
            >
              {isDone ? (
                <CheckCircle2 size={13} className="step-check" />
              ) : isCurrent ? (
                <Sparkles size={13} className="step-sparkle animate-spin" />
              ) : (
                <span className="step-num">{idx + 1}</span>
              )}
              <span>{stage.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default RetrievalStatus;

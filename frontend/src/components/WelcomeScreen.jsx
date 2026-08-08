import React from "react";
import {
  Sparkles,
  Search,
  Compass,
  Cpu,
  Eye,
  FileText,
  Mic,
  UploadCloud,
  ArrowRight
} from "lucide-react";
import SeekovaLogo, { SeekovaOrb } from "./SeekovaLogo";

function WelcomeScreen({ onSearch, onTriggerUpload, setActiveMode }) {
  const quickPrompts = [
    {
      title: "Quantum Computing & Qubits",
      desc: "Explore superposition & quantum algorithms",
      mode: "deep"
    },
    {
      title: "Generative AI vs Agentic AI",
      desc: "Compare direct LLMs with autonomous tools",
      mode: "research"
    },
    {
      title: "Data Structures & Big-O",
      desc: "Inspect array memory and sorting complexity",
      mode: "deep"
    },
    {
      title: "Madurai History & Culture",
      desc: "2,500+ years of Pandya history and architecture",
      mode: "deep"
    }
  ];

  return (
    <div className="seekova-welcome-hero">
      <div className="welcome-orb-backdrop">
        <SeekovaOrb state="idle" size={140} />
      </div>

      <div className="hero-eyebrow">
        <span className="dot" />
        <span>INTELLIGENT KNOWLEDGE RETRIEVAL</span>
      </div>

      <h1 className="hero-title">
        SEARCH BEYOND <br />
        <span className="hero-gradient-text">KEYWORDS.</span>
      </h1>

      <p className="hero-subtitle">
        Search, understand, and connect information with Seekova — powered by TF-IDF n-gram vector alignment, document ingestion, and voice recognition.
      </p>

      <div className="hero-prompt-grid">
        {quickPrompts.map((prompt, idx) => (
          <div
            key={idx}
            className="prompt-card"
            onClick={() => {
              setActiveMode(prompt.mode);
              onSearch(prompt.title);
            }}
          >
            <div className="prompt-card-header">
              <span className="prompt-title">{prompt.title}</span>
              <ArrowRight size={14} className="prompt-arrow" />
            </div>
            <span className="prompt-desc">{prompt.desc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default WelcomeScreen;

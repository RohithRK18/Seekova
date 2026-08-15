import React from "react";
import {
  Sparkles,
  ArrowRight,
  Cpu,
  History as HistoryIcon,
  Atom,
  Globe,
  Code2,
  TrendingUp,
  BookOpen
} from "lucide-react";
import { SecondlyBrainOrb } from "./SecondlyBrainLogo";

function WelcomeScreen({ onSearch, onTriggerUpload, setActiveMode }) {
  const categoryPrompts = [
    {
      category: "Technology",
      icon: Cpu,
      query: "How does Apache Kafka partition replication and offset management work?",
      subtitle: "Event streaming & distributed logs"
    },
    {
      category: "Software",
      icon: Code2,
      query: "Explain Java NullPointerException causes and how to prevent it with Optionals.",
      subtitle: "Code solutions & error fixes"
    },
    {
      category: "Science",
      icon: Atom,
      query: "How does Photosynthesis convert light and CO2 into Glucose?",
      subtitle: "Biochemical reactions & Calvin cycle"
    },
    {
      category: "History",
      icon: HistoryIcon,
      query: "Explain the history of the Roman Empire, its rise and collapse.",
      subtitle: "Timeline & imperial governance"
    },
    {
      category: "Geography",
      icon: Globe,
      query: "Why does India have a monsoon climate and how do the Himalayas affect it?",
      subtitle: "Atmospheric geography & climate"
    },
    {
      category: "Culture",
      icon: BookOpen,
      query: "What is the cultural and historical significance of Diwali?",
      subtitle: "Traditions & festival heritage"
    },
    {
      category: "Business",
      icon: TrendingUp,
      query: "Kafka vs RabbitMQ for real-time analytics platform?",
      subtitle: "Architecture comparison matrix"
    },
    {
      category: "General Knowledge",
      icon: Sparkles,
      query: "Why is the sky blue and how does Rayleigh scattering work?",
      subtitle: "Physics & light dispersion"
    }
  ];

  return (
    <div className="secondlybrain-welcome-hero-v2">
      <div className="welcome-orb-backdrop">
        <SecondlyBrainOrb state="idle" size={130} />
      </div>

      <div className="hero-eyebrow">
        <span className="dot animate-pulse" />
        <span>SECONDLYBRAIN UNIVERSAL AI ANSWER ENGINE</span>
      </div>

      <h1 className="hero-title">
        Ask Anything. <br />
        <span className="hero-gradient-text">Understand Everything.</span>
      </h1>

      <p className="hero-subtitle">
        Your intelligent research assistant for Technology, Software, Science, History, Culture, Geography, and Business.
      </p>

      {/* Domain Category Grid */}
      <div className="hero-category-grid">
        {categoryPrompts.map((item, idx) => {
          const IconComp = item.icon;
          return (
            <div
              key={idx}
              className="prompt-category-card"
              onClick={() => {
                setActiveMode("deep");
                onSearch(item.query);
              }}
            >
              <div className="category-card-top">
                <div className="category-icon-wrapper">
                  <IconComp size={16} />
                </div>
                <span className="category-badge-text">{item.category}</span>
                <ArrowRight size={14} className="prompt-arrow-icon" />
              </div>
              <h3 className="category-query-text">"{item.query}"</h3>
              <span className="category-subtitle-text">{item.subtitle}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WelcomeScreen;

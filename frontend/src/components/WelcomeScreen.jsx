import { Sparkles, FileSearch, Mic, Zap, UploadCloud } from "lucide-react";

function WelcomeScreen({ onSearch, onTriggerUpload }) {
  return (
    <div className="welcome">
      <div className="welcome-logo-wrapper">
        <img src="/logo.png" alt="Seekova" className="welcome-logo-img" />
      </div>

      <span className="welcome-label">INTELLIGENT KNOWLEDGE RETRIEVAL</span>

      <h1>
        Search beyond <br />
        <span>keywords.</span>
      </h1>

      <p>
        Meet Seekova — a powerful search engine powered by TF-IDF relevance
        vectorization, document ingestion, and intelligent speech processing.
      </p>

      <div className="feature-grid">
        <button
          onClick={() =>
            onSearch("Machine learning patterns and neural networks")
          }
        >
          <FileSearch size={24} />
          <strong>Deep Search</strong>
          <span>TF-IDF n-gram vector matching</span>
        </button>

        <button onClick={() => onSearch("Data structures and search index")}>
          <Mic size={24} />
          <strong>Voice Query</strong>
          <span>Search naturally with Web Speech API</span>
        </button>

        <button onClick={onTriggerUpload}>
          <UploadCloud size={24} />
          <strong>Instant Ingestion</strong>
          <span>Upload PDF, DOCX, TXT, or MD files</span>
        </button>
      </div>
    </div>
  );
}

export default WelcomeScreen;

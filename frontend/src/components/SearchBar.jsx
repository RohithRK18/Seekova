import React, { useRef, useState, useEffect } from "react";
import {
  Plus,
  Mic,
  Search,
  X,
  FileText,
  Sparkles,
  Zap,
  Compass,
  Cpu,
  Eye,
  FileCode,
  Image as ImageIcon,
  Link2,
  Send,
  CornerDownLeft,
  Globe,
  Video,
  Code2,
  BookOpen,
  Share2,
  ExternalLink
} from "lucide-react";
import { SecondlyBrainOrb } from "./SecondlyBrainLogo";

const API_URL = import.meta.env.VITE_API_URL || (window.location.hostname === "localhost" ? "http://localhost:8000" : "");

const PLATFORMS = [
  { id: "all", name: "All Platforms", icon: Globe, prefix: "" },
  { id: "google", name: "Google", icon: Search, prefix: "g: " },
  { id: "youtube", name: "YouTube", icon: Video, prefix: "yt: " },
  { id: "github", name: "GitHub", icon: Code2, prefix: "gh: " },
  { id: "reddit", name: "Reddit", icon: Share2, prefix: "r/ " },
  { id: "wikipedia", name: "Wikipedia", icon: BookOpen, prefix: "wiki: " },
  { id: "arxiv", name: "ArXiv", icon: FileText, prefix: "arxiv: " },
];

function SearchBar({
  query,
  setQuery,
  onSearch,
  uploadedFiles,
  setUploadedFiles,
  activeMode,
  setActiveMode
}) {
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);
  const [listening, setListening] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [plusMenuOpen, setPlusMenuOpen] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState("all");

  const modes = [
    { id: "quick", label: "QUICK", icon: Zap },
    { id: "deep", label: "DEEP", icon: Compass },
    { id: "research", label: "RESEARCH", icon: Cpu },
    { id: "vision", label: "VISION", icon: Eye },
    { id: "docs", label: "DOCUMENTS", icon: FileText },
    { id: "voice", label: "VOICE", icon: Mic }
  ];

  // Auto-resize textarea on typing
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [query]);

  function startVoiceSearch() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      let currentTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        currentTranscript += event.results[i][0].transcript;
      }
      setQuery(currentTranscript);
      if (event.results[0].isFinal) {
        onSearch(currentTranscript);
      }
    };

    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognition.start();
  }

  async function uploadFiles(event) {
    const files = Array.from(event.target.files);
    if (!files.length) return;

    setUploading(true);
    setPlusMenuOpen(false);

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(`${API_URL}/api/upload`, {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        if (data.success) {
          setUploadedFiles((previous) => [...previous, data.document]);
        } else {
          alert(`Failed to parse ${file.name}: ${data.detail || 'Error'}`);
        }
      } catch (error) {
        console.error("Upload error:", error);
      }
    }

    setUploading(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function removeFile(id) {
    setUploadedFiles((files) => files.filter((file) => file.id !== id));
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSearch(query);
    }
  }

  function handlePlatformClick(plat) {
    setSelectedPlatform(plat.id);
    if (!plat.prefix) return;
    // Check if query already has a prefix, replace or prepending
    const cleanQuery = query.replace(/^(g:|yt:|gh:|r\/|wiki:|arxiv:)\s*/i, "");
    setQuery(plat.prefix + cleanQuery);
    if (textareaRef.current) textareaRef.current.focus();
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSearch(query);
  }

  return (
    <div className="secondlybrain-search-command-center">
      {/* Mode Selector Pills */}
      <div className="mode-selector-pills">
        {modes.map((mode) => {
          const Icon = mode.icon;
          const isSelected = activeMode === mode.id;
          return (
            <button
              key={mode.id}
              type="button"
              className={`mode-pill ${isSelected ? "selected" : ""}`}
              onClick={() => setActiveMode(mode.id)}
            >
              <Icon size={13} />
              <span>{mode.label}</span>
              {isSelected && <span className="pill-active-glow" />}
            </button>
          );
        })}
      </div>

      {/* Multi-Platform Quick Target Bar (Mobile & Desktop Friendly) */}
      <div className="platform-target-bar">
        <span className="platform-target-label">Target Platform:</span>
        <div className="platform-pills">
          {PLATFORMS.map((plat) => {
            const Icon = plat.icon;
            const isSelected = selectedPlatform === plat.id;
            return (
              <button
                key={plat.id}
                type="button"
                className={`platform-pill ${isSelected ? "active" : ""}`}
                onClick={() => handlePlatformClick(plat)}
                title={`Target ${plat.name}`}
              >
                <Icon size={12} />
                <span>{plat.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Uploaded File Previews */}
      {uploadedFiles.length > 0 && (
        <div className="command-file-previews">
          {uploadedFiles.map((file) => (
            <div className="preview-chip" key={file.id}>
              <FileText size={14} className="chip-icon" />
              <span className="chip-name">{file.name}</span>
              <button
                type="button"
                className="chip-remove"
                onClick={() => removeFile(file.id)}
              >
                <X size={13} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Main Command Box */}
      <form className="command-box-form" onSubmit={handleSubmit}>
        <input
          ref={fileInputRef}
          type="file"
          hidden
          multiple
          accept=".pdf,.docx,.txt,.md"
          onChange={uploadFiles}
        />

        {/* Floating Action + Button */}
        <div className="plus-action-wrapper">
          <button
            type="button"
            className={`plus-action-btn ${plusMenuOpen ? "active" : ""}`}
            onClick={() => setPlusMenuOpen(!plusMenuOpen)}
            title="Add Resources & Ingestion"
            disabled={uploading}
          >
            {uploading ? (
              <div className="spinner-mini" />
            ) : (
              <Plus size={20} className={plusMenuOpen ? "rotate-45" : ""} />
            )}
          </button>

          {/* Plus Action Floating Drawer Menu */}
          {plusMenuOpen && (
            <div className="plus-floating-menu">
              <button
                type="button"
                onClick={() => fileInputRef.current.click()}
              >
                <FileText size={15} color="#818cf8" />
                <span>Upload PDF Document</span>
              </button>
              <button
                type="button"
                onClick={() => fileInputRef.current.click()}
              >
                <FileCode size={15} color="#38bdf8" />
                <span>Upload DOCX / TXT / MD</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setActiveMode("vision");
                  setPlusMenuOpen(false);
                }}
              >
                <ImageIcon size={15} color="#c084fc" />
                <span>Vision Search (Image Analysis)</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  startVoiceSearch();
                  setPlusMenuOpen(false);
                }}
              >
                <Mic size={15} color="#f472b6" />
                <span>Voice Query Mode</span>
              </button>
            </div>
          )}
        </div>

        {/* Auto-resizing Textarea */}
        <textarea
          ref={textareaRef}
          className="command-textarea"
          placeholder="Ask SecondlyBrain anything..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />

        {/* Right Command Actions */}
        <div className="command-actions-right">
          <button
            type="button"
            className={`voice-mic-btn ${listening ? "listening" : ""}`}
            onClick={startVoiceSearch}
            title="Voice Search"
          >
            <Mic size={18} />
            {listening && <span className="mic-pulse" />}
          </button>

          <button
            type="submit"
            className="submit-search-btn"
            disabled={!query.trim() && uploadedFiles.length === 0}
            title="Execute Search (Enter)"
          >
            <Send size={16} />
          </button>
        </div>
      </form>

      {/* Keyboard Shortcut & Search Hint Bar */}
      <div className="command-bottom-hints">
        <span className="hint-item">
          <CornerDownLeft size={12} /> Press <strong>Enter</strong> to search
        </span>
        <span className="hint-item">
          <strong>Shift + Enter</strong> for line break
        </span>
        <span className="hint-item">
          <SecondlyBrainOrb size={14} state={listening ? "listening" : "idle"} /> TF-IDF Semantic Ingestion Active
        </span>
      </div>
    </div>
  );
}

export default SearchBar;

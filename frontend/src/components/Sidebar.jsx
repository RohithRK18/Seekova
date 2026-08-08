import {
  Plus,
  Search,
  Trash2,
  SlidersHorizontal,
  Sparkles,
  Database
} from "lucide-react";

function Sidebar({
  history,
  onNewSearch,
  onSelectSearch,
  activeMode,
  setActiveMode,
  onClearHistory
}) {
  const modes = [
    { id: "quick", label: "⚡ Quick", desc: "Fast token match" },
    { id: "deep", label: "📚 Deep", desc: "TF-IDF + Cosine" },
    { id: "docs", label: "📄 Documents", desc: "PDF & DOCX focus" },
    { id: "voice", label: "🎙️ Voice", desc: "Speech mode" }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="mini-logo">S</div>
        <span className="sidebar-title">Seekova</span>
      </div>

      <button className="new-search" onClick={onNewSearch}>
        <Plus size={18} />
        New Search
      </button>

      <div className="mode-selector">
        <div className="section-label">SEARCH MODE</div>
        <div className="mode-grid">
          {modes.map((mode) => (
            <button
              key={mode.id}
              className={`mode-badge ${activeMode === mode.id ? "active" : ""}`}
              onClick={() => setActiveMode(mode.id)}
              title={mode.desc}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      <div className="history-header">
        <span className="section-label">SEARCH HISTORY</span>
        {history.length > 0 && (
          <button className="clear-history-btn" onClick={onClearHistory} title="Clear history">
            <Trash2 size={13} />
          </button>
        )}
      </div>

      <div className="history">
        {history.length === 0 ? (
          <div className="empty-history">
            <Search size={16} />
            <span>No previous searches</span>
          </div>
        ) : (
          history.map((item, index) => (
            <button
              key={index}
              className="history-item"
              onClick={() => onSelectSearch(item)}
            >
              <Search size={14} />
              <span>{item}</span>
            </button>
          ))
        )}
      </div>

      <div className="sidebar-footer">
        <div className="engine-status">
          <span className="status-dot"></span>
          <span>TF-IDF Engine Active</span>
        </div>
        <div className="version">Seekova v1.0 • Intelligent Search</div>
      </div>
    </aside>
  );
}

export default Sidebar;

import React, { useEffect } from "react";
import {
  Search,
  Cpu,
  Eye,
  FileText,
  Mic,
  Bookmark,
  History,
  Sliders,
  X,
  Plus
} from "lucide-react";

function CommandPalette({
  isOpen,
  onClose,
  onNewSearch,
  onSelectMode,
  onSelectSearch,
  history,
  onTriggerUpload
}) {
  useEffect(() => {
    function handleKeyDown(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          // Open handled by parent or toggle
        }
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    {
      label: "Start New Search",
      icon: Plus,
      action: () => {
        onNewSearch();
        onClose();
      }
    },
    {
      label: "Deep Research Mode",
      icon: Cpu,
      action: () => {
        onSelectMode("research");
        onClose();
      }
    },
    {
      label: "Vision Search (Image Analysis)",
      icon: Eye,
      action: () => {
        onSelectMode("vision");
        onClose();
      }
    },
    {
      label: "Upload Document (PDF / DOCX)",
      icon: FileText,
      action: () => {
        onTriggerUpload();
        onClose();
      }
    },
    {
      label: "Voice Query Search",
      icon: Mic,
      action: () => {
        onSelectMode("voice");
        onClose();
      }
    }
  ];

  return (
    <div className="command-palette-overlay" onClick={onClose}>
      <div
        className="command-palette-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="palette-search-header">
          <Search size={18} className="palette-icon" />
          <input
            type="text"
            className="palette-input"
            placeholder="Type a command or search..."
            autoFocus
          />
          <button className="palette-close-btn" onClick={onClose}>
            <X size={16} />
          </button>
        </div>

        <div className="palette-body">
          <div className="palette-section-label">COMMAND ACTIONS</div>
          <div className="palette-actions-list">
            {actions.map((act, idx) => {
              const Icon = act.icon;
              return (
                <button
                  key={idx}
                  className="palette-action-item"
                  onClick={act.action}
                >
                  <Icon size={16} className="item-icon" />
                  <span>{act.label}</span>
                </button>
              );
            })}
          </div>

          {history.length > 0 && (
            <>
              <div className="palette-section-label">RECENT SEARCHES</div>
              <div className="palette-history-list">
                {history.slice(0, 5).map((item, idx) => (
                  <button
                    key={idx}
                    className="palette-history-item"
                    onClick={() => {
                      onSelectSearch(item);
                      onClose();
                    }}
                  >
                    <History size={14} className="item-icon" />
                    <span>{item}</span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>

        <div className="palette-footer">
          <span>Use <strong>Esc</strong> to exit</span>
          <span>Seekova Command Palette</span>
        </div>
      </div>
    </div>
  );
}

export default CommandPalette;

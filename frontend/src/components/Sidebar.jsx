import React from "react";
import {
  Search,
  Sparkles,
  Eye,
  FileText,
  Mic,
  Bookmark,
  FolderKanban,
  Library,
  Settings,
  Keyboard,
  Cpu,
  Plus,
  Compass,
  History,
  X,
  PanelLeftClose,
  PanelLeft
} from "lucide-react";
import SecondlyBrainLogo from "./SecondlyBrainLogo";

function Sidebar({
  history,
  onNewSearch,
  onSelectSearch,
  activeMode,
  setActiveMode,
  onClearHistory,
  collapsed,
  setCollapsed,
  activeTab,
  setActiveTab,
  onOpenCommandPalette
}) {
  const modes = [
    { id: "quick", label: "Quick", icon: Sparkles, desc: "Fast keyword search" },
    { id: "deep", label: "Deep", icon: Compass, desc: "TF-IDF + Vector ranking" },
    { id: "research", label: "Research", icon: Cpu, desc: "Multi-source research" },
    { id: "vision", label: "Vision", icon: Eye, desc: "Image analysis search" },
    { id: "docs", label: "Documents", icon: FileText, desc: "Ingested doc search" },
    { id: "voice", label: "Voice", icon: Mic, desc: "Live speech query" }
  ];

  return (
    <aside className={`secondlybrain-sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* Sidebar Header */}
      <div className="sidebar-top">
        <div className="sidebar-brand" onClick={onNewSearch}>
          {collapsed ? (
            <SecondlyBrainLogo variant="compact" size="medium" />
          ) : (
            <SecondlyBrainLogo variant="full" size="medium" />
          )}
        </div>
        <button
          className="collapse-toggle-btn"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          {collapsed ? <PanelLeft size={18} /> : <PanelLeftClose size={18} />}
        </button>
      </div>

      {/* New Search Action */}
      <button className="sidebar-new-search-btn" onClick={onNewSearch}>
        <Plus size={18} />
        {!collapsed && <span>New Search</span>}
      </button>

      {/* Navigation Workspace Modes */}
      <div className="sidebar-section">
        {!collapsed && <span className="section-title">SEARCH MODES</span>}
        <div className="sidebar-nav-list">
          {modes.map((mode) => {
            const Icon = mode.icon;
            const isActive = activeMode === mode.id;
            return (
              <button
                key={mode.id}
                className={`nav-item ${isActive ? "active" : ""}`}
                onClick={() => setActiveMode(mode.id)}
                title={mode.desc}
              >
                <Icon size={17} className="nav-icon" />
                {!collapsed && (
                  <div className="nav-label-group">
                    <span className="nav-title">{mode.label}</span>
                  </div>
                )}
                {!collapsed && isActive && <div className="active-pill" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Recent Searches */}
      <div className="sidebar-section history-section">
        {!collapsed && (
          <div className="section-header">
            <span className="section-title">RECENT SEARCHES</span>
            {history.length > 0 && (
              <button
                className="clear-btn"
                onClick={onClearHistory}
                title="Clear Search History"
              >
                Clear
              </button>
            )}
          </div>
        )}
        <div className="history-scroll-list">
          {history.length === 0 ? (
            !collapsed && (
              <div className="empty-history-text">
                <History size={14} />
                <span>No recent searches</span>
              </div>
            )
          ) : (
            history.map((item, idx) => (
              <button
                key={idx}
                className="history-nav-item"
                onClick={() => onSelectSearch(item)}
                title={item}
              >
                <Search size={14} className="history-icon" />
                {!collapsed && <span className="history-text">{item}</span>}
              </button>
            ))
          )}
        </div>
      </div>

      {/* Saved Collections */}
      {!collapsed && (
        <div className="sidebar-section collections-section">
          <span className="section-title">COLLECTIONS</span>
          <div className="collection-item">
            <Bookmark size={15} color="#818cf8" />
            <span>Saved Insights</span>
          </div>
          <div className="collection-item">
            <FolderKanban size={15} color="#c084fc" />
            <span>Research Projects</span>
          </div>
          <div className="collection-item">
            <Library size={15} color="#38bdf8" />
            <span>Knowledge Base</span>
          </div>
        </div>
      )}

      {/* Sidebar Bottom Engine Footer */}
      <div className="sidebar-footer">
        <div className="engine-active-indicator" title="TF-IDF Engine Active">
          <span className="pulse-dot" />
          {!collapsed && <span className="engine-name">TF-IDF Engine Active</span>}
        </div>
        {!collapsed && (
          <div className="footer-actions">
            <button
              className="footer-icon-btn"
              onClick={onOpenCommandPalette}
              title="Keyboard Shortcuts (Ctrl+K)"
            >
              <Keyboard size={15} />
            </button>
            <button className="footer-icon-btn" title="Engine Settings">
              <Settings size={15} />
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}

export default Sidebar;

import React from "react";
import { Command, Sliders, Moon, User, Sparkles } from "lucide-react";
import SeekovaLogo from "./SeekovaLogo";

function TopNavigation({
  activeMode,
  onNewSearch,
  onOpenCommandPalette,
  onToggleSidebar,
  mobileSidebarOpen
}) {
  return (
    <header className="seekova-topbar">
      <div className="topbar-left">
        <div className="mobile-brand" onClick={onNewSearch}>
          <SeekovaLogo variant="full" size="small" />
        </div>

        <div className="workspace-badge">
          <Sparkles size={13} className="sparkle-icon" />
          <span className="badge-mode-label">Mode: {activeMode.toUpperCase()}</span>
        </div>
      </div>

      <div className="topbar-right">
        <button
          className="keyboard-shortcut-btn"
          onClick={onOpenCommandPalette}
          title="Open Command Palette (Ctrl+K)"
        >
          <Command size={13} />
          <span>Ctrl K</span>
        </button>

        <button className="topbar-action-btn" title="System Settings">
          <Sliders size={16} />
        </button>

        <div className="user-profile-avatar" title="Seekova User">
          <User size={15} />
        </div>
      </div>
    </header>
  );
}

export default TopNavigation;

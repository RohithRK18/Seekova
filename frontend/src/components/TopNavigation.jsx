import React, { useState } from "react";
import { Command, Sliders, User, Sparkles, LogOut, Bookmark, Layers, Settings, LogIn } from "lucide-react";
import SecondlyBrainLogo from "./SecondlyBrainLogo";

function TopNavigation({
  activeMode,
  onNewSearch,
  onOpenCommandPalette,
  onToggleSidebar,
  currentUser,
  onOpenAuth,
  onLogout
}) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header className="secondlybrain-topbar">
      <div className="topbar-left">
        <div className="mobile-brand" onClick={onNewSearch}>
          <SecondlyBrainLogo variant="full" size="small" />
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

        {/* User Account Avatar & Dropdown */}
        <div className="user-profile-wrapper" style={{ position: "relative" }}>
          {currentUser ? (
            <div
              className="user-profile-avatar"
              onClick={() => setDropdownOpen(!dropdownOpen)}
              title={currentUser.name}
              style={{ cursor: "pointer" }}
            >
              <span>{currentUser.name.charAt(0).toUpperCase()}</span>
            </div>
          ) : (
            <button
              className="topbar-action-btn"
              onClick={() => onOpenAuth("login")}
              title="Sign In / Register"
              style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 12px", background: "rgba(99, 102, 241, 0.15)", border: "1px solid rgba(99,102,241,0.3)", borderRadius: "20px", color: "#38bdf8", fontWeight: 600, fontSize: 12 }}
            >
              <LogIn size={14} />
              <span>Sign In</span>
            </button>
          )}

          {dropdownOpen && currentUser && (
            <div className="user-menu-dropdown" onClick={() => setDropdownOpen(false)}>
              <div className="menu-user-info">
                <span className="menu-user-name">{currentUser.name}</span>
                <span className="menu-user-email">{currentUser.email}</span>
              </div>
              <button className="user-menu-item">
                <Bookmark size={14} />
                <span>Saved Insights</span>
              </button>
              <button className="user-menu-item">
                <Layers size={14} />
                <span>Research Projects</span>
              </button>
              <button className="user-menu-item">
                <Settings size={14} />
                <span>Account Settings</span>
              </button>
              <button className="user-menu-item logout" onClick={onLogout}>
                <LogOut size={14} />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default TopNavigation;

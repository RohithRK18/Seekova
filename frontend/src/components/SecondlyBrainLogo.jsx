import React from "react";

export function SecondlyBrainOrb({ state = "idle", size = 48, className = "" }) {
  // states: idle, listening, searching, processing, complete
  return (
    <div
      className={`secondlybrain-orb-container state-${state} ${className}`}
      style={{ width: `${size}px`, height: `${size}px` }}
    >
      <svg
        viewBox="0 0 100 100"
        className="secondlybrain-orb-svg"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="sbBrainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#a855f7" />
            <stop offset="50%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#38bdf8" />
          </linearGradient>
          <linearGradient id="sbRightNodeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#38bdf8" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
          <radialGradient id="sbGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#a855f7" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#38bdf8" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Glowing Aura Ring */}
        <circle cx="50" cy="50" r="46" fill="url(#sbGlow)" opacity="0.3" className="orb-aura" />

        {/* Outer Circular Tech Arc */}
        <path
          d="M 50 6 A 44 44 0 0 1 94 50 A 44 44 0 0 1 50 94"
          fill="none"
          stroke="#38bdf8"
          strokeWidth="3.5"
          strokeLinecap="round"
          className="ring-1"
        />
        <path
          d="M 50 94 A 44 44 0 0 1 6 50 A 44 44 0 0 1 50 6"
          fill="none"
          stroke="#a855f7"
          strokeWidth="3.5"
          strokeLinecap="round"
          className="ring-2"
        />

        {/* Left Organic Brain Lobe Path */}
        <path
          d="M 46 22 C 34 22 24 28 24 38 C 24 44 28 48 24 54 C 20 60 22 72 32 76 C 38 78 44 74 46 78 Z"
          fill="none"
          stroke="url(#sbBrainGrad)"
          strokeWidth="3.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M 34 34 C 30 38 32 46 38 46 M 30 52 C 36 54 34 66 42 66"
          fill="none"
          stroke="url(#sbBrainGrad)"
          strokeWidth="2.5"
          strokeLinecap="round"
        />

        {/* Right Digital Neural Network Nodes & Links */}
        <g stroke="url(#sbRightNodeGrad)" strokeWidth="2.2">
          <line x1="54" y1="26" x2="68" y2="34" />
          <line x1="68" y1="34" x2="82" y2="30" />
          <line x1="54" y1="50" x2="68" y2="34" />
          <line x1="54" y1="50" x2="74" y2="52" />
          <line x1="74" y1="52" x2="84" y2="44" />
          <line x1="54" y1="74" x2="70" y2="68" />
          <line x1="70" y1="68" x2="82" y2="70" />
          <line x1="74" y1="52" x2="70" y2="68" />
          <line x1="68" y1="34" x2="74" y2="52" />
        </g>

        {/* Neural Node Points */}
        <circle cx="54" cy="26" r="3.5" fill="#38bdf8" />
        <circle cx="68" cy="34" r="4" fill="#a855f7" />
        <circle cx="82" cy="30" r="3.5" fill="#38bdf8" />
        <circle cx="54" cy="50" r="4" fill="#38bdf8" />
        <circle cx="74" cy="52" r="4.5" fill="#ffffff" />
        <circle cx="84" cy="44" r="3.5" fill="#a855f7" />
        <circle cx="54" cy="74" r="3.5" fill="#38bdf8" />
        <circle cx="70" cy="68" r="4" fill="#a855f7" />
        <circle cx="82" cy="70" r="3.5" fill="#38bdf8" />
      </svg>
    </div>
  );
}

export function SecondlyBrainLogo({ variant = "full", size = "medium", className = "" }) {
  const orbSizes = { small: 26, medium: 36, large: 48 };
  const currentOrbSize = orbSizes[size] || 36;

  if (variant === "compact" || variant === "symbol") {
    return (
      <div className={`secondlybrain-logo compact ${className}`}>
        <SecondlyBrainOrb size={currentOrbSize} />
      </div>
    );
  }

  return (
    <div className={`secondlybrain-logo full ${size} ${className}`}>
      <SecondlyBrainOrb size={currentOrbSize} className="logo-orb" />
      <div className="logo-text-group">
        <span className="logo-main-text">
          SECONDLY<span className="logo-highlight">BRAIN</span>
        </span>
        {size !== "small" && (
          <span className="logo-tagline">YOUR INTELLIGENT SECOND BRAIN</span>
        )}
      </div>
    </div>
  );
}

export default SecondlyBrainLogo;

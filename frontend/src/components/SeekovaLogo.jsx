import React from "react";

export function SeekovaOrb({ state = "idle", size = 48, className = "" }) {
  // states: idle, listening, searching, processing, complete
  return (
    <div
      className={`seekova-orb-container state-${state} ${className}`}
      style={{ width: `${size}px`, height: `${size}px` }}
    >
      <svg
        viewBox="0 0 100 100"
        className="seekova-orb-svg"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <radialGradient id="orbCoreGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#a78bfa" stopOpacity="1" />
            <stop offset="45%" stopColor="#6366f1" stopOpacity="0.9" />
            <stop offset="85%" stopColor="#3b82f6" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="orbRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#60a5fa" />
            <stop offset="50%" stopColor="#c084fc" />
            <stop offset="100%" stopColor="#38bdf8" />
          </linearGradient>
          <filter id="orbGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Outer Pulsing Aura */}
        <circle
          cx="50"
          cy="50"
          r="42"
          className="orb-aura"
          fill="url(#orbCoreGrad)"
          opacity="0.35"
        />

        {/* Orbital Ring 1 */}
        <ellipse
          cx="50"
          cy="50"
          rx="36"
          ry="14"
          className="orb-ring ring-1"
          fill="none"
          stroke="url(#orbRingGrad)"
          strokeWidth="1.8"
          strokeDasharray="4 3 12 4"
        />

        {/* Orbital Ring 2 (Crossed) */}
        <ellipse
          cx="50"
          cy="50"
          rx="36"
          ry="14"
          className="orb-ring ring-2"
          fill="none"
          stroke="url(#orbRingGrad)"
          strokeWidth="1.4"
          strokeDasharray="8 4 4 4"
          transform="rotate(60 50 50)"
        />

        {/* Core Glowing Sphere */}
        <circle
          cx="50"
          cy="50"
          r="18"
          fill="url(#orbCoreGrad)"
          filter="url(#orbGlow)"
          className="orb-core"
        />

        {/* Central Intelligence Node */}
        <circle cx="50" cy="50" r="6" fill="#ffffff" opacity="0.95" />
        <circle cx="50" cy="50" r="2.5" fill="#38bdf8" />
      </svg>
    </div>
  );
}

export function SeekovaLogo({ variant = "full", size = "medium", className = "" }) {
  // size: small, medium, large
  const orbSizes = { small: 24, medium: 32, large: 44 };
  const currentOrbSize = orbSizes[size] || 32;

  if (variant === "compact" || variant === "symbol") {
    return (
      <div className={`seekova-logo compact ${className}`}>
        <SeekovaOrb size={currentOrbSize} />
      </div>
    );
  }

  return (
    <div className={`seekova-logo full ${size} ${className}`}>
      <span className="logo-text">
        SEEK
        <span className="logo-o-wrapper">
          <SeekovaOrb size={currentOrbSize} className="logo-inline-orb" />
        </span>
        VA
      </span>
    </div>
  );
}

export default SeekovaLogo;

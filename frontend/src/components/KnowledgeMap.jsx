import React, { useState } from "react";
import { Network, Maximize2, ZoomIn, ZoomOut, Compass } from "lucide-react";

function KnowledgeMap({ query, results, onSelectNode }) {
  const [zoom, setZoom] = useState(1);

  if (!query) return null;

  const nodes = [
    { id: "root", label: query, type: "root", x: 180, y: 110 },
    { id: "sub1", label: "Core Concepts", type: "branch", x: 70, y: 40 },
    { id: "sub2", label: "Architecture & Rules", type: "branch", x: 290, y: 40 },
    { id: "sub3", label: "Algorithms & Logic", type: "branch", x: 70, y: 180 },
    { id: "sub4", label: "Applications", type: "branch", x: 290, y: 180 }
  ];

  return (
    <div className="knowledge-map-card">
      <div className="map-header">
        <div className="map-title-group">
          <Network size={16} className="map-icon" />
          <span>KNOWLEDGE MAP GRAPH</span>
        </div>
        <div className="map-controls">
          <button onClick={() => setZoom(Math.min(zoom + 0.15, 1.4))} title="Zoom In">
            <ZoomIn size={14} />
          </button>
          <button onClick={() => setZoom(Math.max(zoom - 0.15, 0.7))} title="Zoom Out">
            <ZoomOut size={14} />
          </button>
        </div>
      </div>

      <div className="map-svg-container" style={{ transform: `scale(${zoom})` }}>
        <svg viewBox="0 0 360 220" className="knowledge-svg">
          {/* Connector Lines */}
          <line x1="180" y1="110" x2="70" y2="40" stroke="#4f46e5" strokeWidth="1.5" strokeDasharray="3 3" />
          <line x1="180" y1="110" x2="290" y2="40" stroke="#818cf8" strokeWidth="1.5" strokeDasharray="3 3" />
          <line x1="180" y1="110" x2="70" y2="180" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="3 3" />
          <line x1="180" y1="110" x2="290" y2="180" stroke="#c084fc" strokeWidth="1.5" strokeDasharray="3 3" />

          {/* Interactive Nodes */}
          {nodes.map((node) => (
            <g
              key={node.id}
              className={`graph-node ${node.type}`}
              transform={`translate(${node.x}, ${node.y})`}
              onClick={() => onSelectNode(`${query} ${node.label}`)}
            >
              <circle
                r={node.type === "root" ? 22 : 16}
                fill={node.type === "root" ? "#6366f1" : "#1e1b4b"}
                stroke={node.type === "root" ? "#c084fc" : "#60a5fa"}
                strokeWidth="2"
              />
              <text
                textAnchor="middle"
                dy="4"
                fontSize={node.type === "root" ? "10" : "8"}
                fill="#ffffff"
                fontWeight="600"
              >
                {node.label.length > 12 ? `${node.label.slice(0, 10)}..` : node.label}
              </text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
}

export default KnowledgeMap;

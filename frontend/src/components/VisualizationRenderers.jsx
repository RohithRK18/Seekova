import React from "react";
import { GitFork, Clock, Layers, Sparkles } from "lucide-react";

export function MindMapRenderer({ data }) {
  if (!data || !data.nodes) return null;

  const rootNode = data.nodes.find(n => n.type === "root") || data.nodes[0];
  const mainBranches = data.nodes.filter(n => n.parent === rootNode.id);

  return (
    <div className="secondlybrain-mindmap-container">
      <div className="visualization-header">
        <GitFork size={16} className="viz-icon" />
        <span>INTERACTIVE MIND MAP</span>
      </div>

      <div className="mindmap-canvas">
        {/* Root Node */}
        <div className="mindmap-root-node">
          <Sparkles size={14} />
          <span>{rootNode.label}</span>
        </div>

        {/* Main Branches Grid */}
        <div className="mindmap-branches-grid">
          {mainBranches.map((branch) => {
            const subNodes = data.nodes.filter(n => n.parent === branch.id);
            return (
              <div key={branch.id} className="mindmap-branch-card">
                <div className="branch-header-pill">
                  <span>{branch.label}</span>
                </div>
                <div className="branch-children-list">
                  {subNodes.map((child) => (
                    <div key={child.id} className="branch-child-item">
                      <span className="child-dot">•</span>
                      <span>{child.label}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function TimelineRenderer({ data }) {
  if (!data || !data.events) return null;

  return (
    <div className="secondlybrain-timeline-container">
      <div className="visualization-header">
        <Clock size={16} className="viz-icon" />
        <span>HISTORICAL TIMELINE CHRONOLOGY</span>
      </div>

      <div className="timeline-events-list">
        {data.events.map((event, idx) => (
          <div key={idx} className="timeline-event-card">
            <div className="timeline-year-badge">{event.year}</div>
            <div className="timeline-content-box">
              <h4 className="timeline-event-title">{event.title}</h4>
              <p className="timeline-event-desc">{event.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

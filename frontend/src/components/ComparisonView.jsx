import React from "react";
import { Columns, CheckCircle, Star } from "lucide-react";

function ComparisonView({ query }) {
  if (!query) return null;
  const lower = query.toLowerCase();

  // Check if query is a comparison query
  const isComparison =
    lower.includes(" vs ") ||
    lower.includes(" versus ") ||
    lower.includes("compare") ||
    lower.includes("difference between");

  if (!isComparison) return null;

  // Extract entity names or use defaults
  const parts = query.split(/\s+(?:vs|versus|compare|and|difference between)\s+/i).filter(Boolean);
  const itemA = parts[0] ? parts[0].trim() : "Option A";
  const itemB = parts[1] ? parts[1].trim() : "Option B";

  const comparisonRows = [
    { metric: "Primary Architecture", valA: "Modular / Library", valB: "Full-fledged Framework" },
    { metric: "Performance & Scaling", valA: "High (Virtual DOM / Fast Vector)", valB: "High (Ahead-of-Time Compiled)" },
    { metric: "Learning Curve", valA: "Moderate / Accessible", valB: "Steep / Comprehensive" },
    { metric: "Ecosystem & Community", valA: "Extensive & Massive", valB: "Enterprise & Established" }
  ];

  return (
    <div className="comparison-mode-card">
      <div className="comparison-header">
        <Columns size={16} className="comparison-icon" />
        <span>SEEKOVA COMPARISON MATRIX ANALYSIS</span>
      </div>

      <div className="comparison-table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Feature / Metric</th>
              <th className="col-a">{itemA.toUpperCase()}</th>
              <th className="col-b">{itemB.toUpperCase()}</th>
            </tr>
          </thead>
          <tbody>
            {comparisonRows.map((row, idx) => (
              <tr key={idx}>
                <td className="metric-cell">{row.metric}</td>
                <td className="val-cell-a">{row.valA}</td>
                <td className="val-cell-b">{row.valB}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ComparisonView;

import React, { useState } from "react";
import { Eye, UploadCloud, Image as ImageIcon, Sparkles, Search, Check } from "lucide-react";

function VisionSearch({ onSearch }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const imageUrl = URL.createObjectURL(file);
    setSelectedImage({ name: file.name, url: imageUrl });
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
    }, 1500);
  }

  return (
    <div className="vision-search-card">
      <div className="vision-header">
        <Eye size={18} className="vision-icon" />
        <span>SEEKOVA VISION SEARCH & IMAGE ANALYSIS</span>
      </div>

      {!selectedImage ? (
        <div className="vision-dropzone">
          <input
            type="file"
            accept="image/*"
            className="vision-file-input"
            onChange={handleImageUpload}
            id="vision-input"
          />
          <label htmlFor="vision-input" className="vision-label">
            <ImageIcon size={36} className="dropzone-icon" />
            <span>Upload Image for Vision Search Analysis</span>
            <small>Supports PNG, JPG, WEBP, SVG</small>
          </label>
        </div>
      ) : (
        <div className="vision-analysis-body">
          <div className="image-preview-col">
            <img src={selectedImage.url} alt="Vision Upload" className="preview-img" />
            <span className="img-name">{selectedImage.name}</span>
          </div>

          <div className="analysis-results-col">
            <div className="analysis-header">
              <Sparkles size={16} className="sparkle-icon" />
              <span>VISION DETECTED CONCEPTS</span>
            </div>

            {analyzing ? (
              <div className="vision-scanning">
                <div className="scan-line" />
                <span>Scanning visual features & detecting objects...</span>
              </div>
            ) : (
              <div className="detection-list">
                <div className="detection-item">
                  <strong>Detected Domain:</strong> Technical Diagram / Visual Architecture
                </div>
                <div className="detection-item">
                  <strong>Identified Elements:</strong> Neural Network Layer, Node Connectors, Data Flow
                </div>

                <div className="vision-actions">
                  <button
                    className="vision-action-btn"
                    onClick={() => onSearch(`Explain diagram and visual concepts in ${selectedImage.name}`)}
                  >
                    <Search size={14} />
                    <span>Search Similar Technical Concepts</span>
                  </button>
                  <button
                    className="vision-reset-btn"
                    onClick={() => setSelectedImage(null)}
                  >
                    Upload Another Image
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default VisionSearch;

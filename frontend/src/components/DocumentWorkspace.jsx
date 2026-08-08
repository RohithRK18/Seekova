import React, { useState } from "react";
import {
  FileText,
  UploadCloud,
  FileCode,
  FileSpreadsheet,
  CheckCircle,
  Sparkles,
  Search,
  BookOpen
} from "lucide-react";

function DocumentWorkspace({ uploadedFiles, onTriggerUpload, onSearch }) {
  if (!uploadedFiles || uploadedFiles.length === 0) {
    return (
      <div className="document-workspace-empty">
        <UploadCloud size={40} className="empty-upload-icon" />
        <h3>Document Intelligence Workspace</h3>
        <p>
          Upload PDF, DOCX, TXT, or MD documents to ingest custom knowledge into SecondlyBrain's TF-IDF vector ranking engine.
        </p>
        <button className="workspace-upload-btn" onClick={onTriggerUpload}>
          <UploadCloud size={16} />
          <span>Upload Document</span>
        </button>
      </div>
    );
  }

  return (
    <div className="document-workspace-card">
      <div className="workspace-header">
        <div className="workspace-title">
          <FileText size={18} className="title-icon" />
          <span>DOCUMENT INTELLIGENCE ({uploadedFiles.length} INDEXED)</span>
        </div>
        <button className="add-doc-btn" onClick={onTriggerUpload}>
          <UploadCloud size={14} />
          <span>Add More</span>
        </button>
      </div>

      <div className="file-grid">
        {uploadedFiles.map((file) => (
          <div key={file.id} className="file-card">
            <div className="file-card-top">
              <FileCode size={20} color="#818cf8" />
              <span className="file-type-badge">{file.type || ".txt"}</span>
            </div>
            <h4 className="file-name">{file.name}</h4>
            <span className="file-info">{file.characters || 1200} characters indexed</span>

            <div className="file-actions">
              <button
                className="action-pill"
                onClick={() => onSearch(`Summarize ${file.name}`)}
              >
                <Sparkles size={12} />
                <span>Summarize</span>
              </button>
              <button
                className="action-pill"
                onClick={() => onSearch(`Extract key points from ${file.name}`)}
              >
                <BookOpen size={12} />
                <span>Extract</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DocumentWorkspace;

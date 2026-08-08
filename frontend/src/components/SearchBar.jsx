import {
  Plus,
  Mic,
  Search,
  X,
  FileText,
  Sparkles,
  Zap,
  BookOpen
} from "lucide-react";
import { useRef, useState } from "react";

const API_URL = "http://localhost:8000";

function SearchBar({
  query,
  setQuery,
  onSearch,
  uploadedFiles,
  setUploadedFiles,
  activeMode
}) {
  const fileInputRef = useRef(null);
  const [listening, setListening] = useState(false);
  const [uploading, setUploading] = useState(false);

  function startVoiceSearch() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      onSearch(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Voice recognition error:", event.error);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  }

  async function uploadFiles(event) {
    const files = Array.from(event.target.files);
    if (!files.length) return;

    setUploading(true);

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(`${API_URL}/api/upload`, {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        if (data.success) {
          setUploadedFiles((previous) => [...previous, data.document]);
        } else {
          alert(`Failed to parse ${file.name}: ${data.detail || 'Error'}`);
        }
      } catch (error) {
        console.error("Upload error:", error);
      }
    }

    setUploading(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function removeFile(id) {
    setUploadedFiles((files) => files.filter((file) => file.id !== id));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(query);
  }

  return (
    <div className="search-wrapper">
      {uploadedFiles.length > 0 && (
        <div className="file-preview">
          {uploadedFiles.map((file) => (
            <div className="uploaded-file" key={file.id}>
              <FileText size={15} />
              <span>{file.name}</span>
              <button onClick={() => removeFile(file.id)}>
                <X size={14} />
              </button>
            </div>
          ))}
        </div>
      )}

      <form className="search-box" onSubmit={handleSubmit}>
        <input
          ref={fileInputRef}
          type="file"
          hidden
          multiple
          accept=".pdf,.docx,.txt,.md"
          onChange={uploadFiles}
        />

        <button
          type="button"
          className="icon-button"
          onClick={() => fileInputRef.current.click()}
          title="Upload Documents (PDF, DOCX, TXT, MD)"
          disabled={uploading}
        >
          {uploading ? <div className="spinner-mini" /> : <Plus size={21} />}
        </button>

        <input
          type="text"
          placeholder={`Ask Seekova anything [Mode: ${activeMode.toUpperCase()}]...`}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />

        <button
          type="button"
          className={`voice-button ${listening ? "active" : ""}`}
          onClick={startVoiceSearch}
          title="Voice Search"
        >
          <Mic size={20} />
        </button>

        <button type="submit" className="search-button" title="Execute Search">
          <Search size={19} />
        </button>
      </form>

      <div className="search-hint">
        <span>
          <Plus size={12} /> Upload (PDF/DOCX/TXT/MD)
        </span>
        <span>
          <Mic size={12} /> Web Speech API
        </span>
        <span>
          <Sparkles size={12} /> TF-IDF Semantic Ranking Engine
        </span>
      </div>
    </div>
  );
}

export default SearchBar;

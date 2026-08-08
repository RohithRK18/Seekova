import { useEffect, useState } from "react";
import { Menu, X, AlertTriangle, RefreshCw } from "lucide-react";
import Sidebar from "./components/Sidebar";
import SearchBar from "./components/SearchBar";
import SearchResult from "./components/SearchResult";
import WelcomeScreen from "./components/WelcomeScreen";
import AnswerCard from "./components/AnswerCard";
import "./index.css";

const API_URL = import.meta.env.VITE_API_URL || (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" ? "http://localhost:8000" : "");

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchError, setSearchError] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [activeMode, setActiveMode] = useState("deep");
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const response = await fetch(`${API_URL}/api/history`);
      const data = await response.json();
      setHistory(data.history || []);
    } catch (error) {
      console.error("Failed to load history:", error);
    }
  }

  async function clearHistory() {
    try {
      await fetch(`${API_URL}/api/history`, { method: "DELETE" });
      setHistory([]);
    } catch (error) {
      console.error("Failed to clear history:", error);
    }
  }

  async function performSearch(searchQuery = query) {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setHasSearched(true);
    setSearchError(null);
    setQuery(searchQuery);

    try {
      const response = await fetch(`${API_URL}/api/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: searchQuery,
          limit: 10,
          mode: activeMode
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();
      setResults(data.results || []);
      setAnswer(data.answer || null);

      // Save to history asynchronously
      fetch(`${API_URL}/api/history`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: searchQuery
        })
      })
        .then(() => loadHistory())
        .catch(() => {});
    } catch (error) {
      console.error("Search error:", error);
      setSearchError(error.message || "Failed to fetch search results from Seekova engine.");
    } finally {
      setLoading(false);
    }
  }

  function newSearch() {
    setQuery("");
    setResults([]);
    setAnswer(null);
    setHasSearched(false);
    setSearchError(null);
    setUploadedFiles([]);
  }

  return (
    <div className={`app ${mobileSidebarOpen ? "sidebar-open" : ""}`}>
      {mobileSidebarOpen && (
        <div
          className="mobile-overlay"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      <Sidebar
        history={history}
        onNewSearch={newSearch}
        onSelectSearch={(q) => {
          performSearch(q);
          setMobileSidebarOpen(false);
        }}
        activeMode={activeMode}
        setActiveMode={setActiveMode}
        onClearHistory={clearHistory}
      />

      <main className="main">
        <header className="topbar">
          <button
            className="mobile-menu-toggle"
            onClick={() => setMobileSidebarOpen(!mobileSidebarOpen)}
            title="Toggle Menu"
          >
            {mobileSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          <div className="brand" onClick={newSearch} style={{ cursor: "pointer" }}>
            <div className="brand-logo">S</div>
            <span>Seekova</span>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            <span className="status-text">Mode: {activeMode.toUpperCase()}</span>
          </div>
        </header>

        <section className="content">
          {!hasSearched ? (
            <WelcomeScreen
              onSearch={performSearch}
              onTriggerUpload={() => {
                const input = document.querySelector('input[type="file"]');
                if (input) input.click();
              }}
            />
          ) : (
            <>
              <div className="results-header">
                <div>
                  <span className="eyebrow">SEEKOVA INTELLIGENT SEARCH</span>
                  <h1>Results for "{query}"</h1>
                </div>
                <div className="result-count">
                  {results.length} matched {results.length === 1 ? "document" : "documents"}
                </div>
              </div>

              {loading ? (
                <div className="loader">
                  <div className="loader-ring"></div>
                  <p>Seekova is computing TF-IDF similarity vectors & synthesizing answer...</p>
                </div>
              ) : searchError ? (
                <div className="error-container">
                  <AlertTriangle size={32} className="error-icon" />
                  <h3>Search Request Failed</h3>
                  <p>{searchError}</p>
                  <button className="retry-btn" onClick={() => performSearch(query)}>
                    <RefreshCw size={16} />
                    <span>Try Again</span>
                  </button>
                </div>
              ) : (
                <div className="results-container">
                  {/* AI Synthesized Answer Box */}
                  {answer && (
                    <AnswerCard query={query} answer={answer} activeMode={activeMode} />
                  )}

                  {/* Document Results List */}
                  <div className="results">
                    {results.length === 0 ? (
                      <div className="no-results">
                        <h3>No matching documents found</h3>
                        <p>
                          Try uploading documents (PDF, DOCX, TXT, MD) using the + button below or try different search keywords.
                        </p>
                      </div>
                    ) : (
                      results.map((result) => (
                        <SearchResult
                          key={result.id}
                          result={result}
                          activeMode={activeMode}
                          query={query}
                        />
                      ))
                    )}
                  </div>
                </div>
              )}
            </>
          )}

          <SearchBar
            query={query}
            setQuery={setQuery}
            onSearch={performSearch}
            uploadedFiles={uploadedFiles}
            setUploadedFiles={setUploadedFiles}
            activeMode={activeMode}
          />
        </section>
      </main>
    </div>
  );
}

export default App;

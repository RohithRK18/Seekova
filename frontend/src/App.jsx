import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import SearchBar from "./components/SearchBar";
import SearchResult from "./components/SearchResult";
import WelcomeScreen from "./components/WelcomeScreen";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [activeMode, setActiveMode] = useState("deep");

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
    setQuery(searchQuery);

    try {
      const response = await fetch(`${API_URL}/api/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: searchQuery,
          limit: 10
        })
      });

      const data = await response.json();
      setResults(data.results || []);

      await fetch(`${API_URL}/api/history`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: searchQuery
        })
      });

      loadHistory();
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      setLoading(false);
    }
  }

  function newSearch() {
    setQuery("");
    setResults([]);
    setUploadedFiles([]);
  }

  return (
    <div className="app">
      <Sidebar
        history={history}
        onNewSearch={newSearch}
        onSelectSearch={performSearch}
        activeMode={activeMode}
        setActiveMode={setActiveMode}
        onClearHistory={clearHistory}
      />

      <main className="main">
        <header className="topbar">
          <div className="brand">
            <div className="brand-logo">S</div>
            <span>Seekova</span>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            <span>Search Intelligence Mode: {activeMode.toUpperCase()}</span>
          </div>
        </header>

        <section className="content">
          {results.length === 0 && !loading ? (
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
                  {results.length} matched documents
                </div>
              </div>

              {loading ? (
                <div className="loader">
                  <div className="loader-ring"></div>
                  <p>Seekova is computing TF-IDF similarity vectors...</p>
                </div>
              ) : (
                <div className="results">
                  {results.length === 0 ? (
                    <div className="no-results">
                      <h3>No relevant documents found</h3>
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
                      />
                    ))
                  )}
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

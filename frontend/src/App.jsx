import { useEffect, useState } from "react";
import { AlertTriangle, RefreshCw, Layers } from "lucide-react";
import Sidebar from "./components/Sidebar";
import TopNavigation from "./components/TopNavigation";
import SearchBar from "./components/SearchBar";
import SearchResult from "./components/SearchResult";
import WelcomeScreen from "./components/WelcomeScreen";
import AnswerCard from "./components/AnswerCard";
import SourceCard from "./components/SourceCard";
import SearchJourney from "./components/SearchJourney";
import KnowledgeMap from "./components/KnowledgeMap";
import ComparisonView from "./components/ComparisonView";
import RelatedQuestions from "./components/RelatedQuestions";
import DocumentWorkspace from "./components/DocumentWorkspace";
import VisionSearch from "./components/VisionSearch";
import VoiceSearch from "./components/VoiceSearch";
import CommandPalette from "./components/CommandPalette";
import { SeekovaOrb } from "./components/SeekovaLogo";
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
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

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
    if (!searchQuery.trim() && uploadedFiles.length === 0) return;

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
          mode: activeMode,
          custom_documents: uploadedFiles.map((file) => ({
            id: file.id,
            title: file.name,
            content: file.content || file.name,
            file_type: file.type || ".txt"
          }))
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

  function triggerFileUpload() {
    const input = document.querySelector('input[type="file"]');
    if (input) input.click();
  }

  return (
    <div className={`seekova-app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""}`}>
      {/* Mobile Drawer Overlay */}
      {mobileSidebarOpen && (
        <div
          className="mobile-overlay"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      {/* Left Sidebar */}
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
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        onOpenCommandPalette={() => setCommandPaletteOpen(true)}
      />

      {/* Main App Layout Area */}
      <div className="seekova-main-wrapper">
        <TopNavigation
          activeMode={activeMode}
          onNewSearch={newSearch}
          onOpenCommandPalette={() => setCommandPaletteOpen(true)}
          onToggleSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
          mobileSidebarOpen={mobileSidebarOpen}
        />

        <main className="seekova-content-area">
          {!hasSearched ? (
            /* Home Mode Views */
            activeMode === "docs" ? (
              <DocumentWorkspace
                uploadedFiles={uploadedFiles}
                onTriggerUpload={triggerFileUpload}
                onSearch={performSearch}
              />
            ) : activeMode === "vision" ? (
              <VisionSearch onSearch={performSearch} />
            ) : activeMode === "voice" ? (
              <VoiceSearch onSearch={performSearch} setQuery={setQuery} />
            ) : (
              <WelcomeScreen
                onSearch={performSearch}
                onTriggerUpload={triggerFileUpload}
                setActiveMode={setActiveMode}
              />
            )
          ) : (
            /* Search Results Dashboard - 3 Column Layout */
            <div className="seekova-results-layout">
              {/* Center Main Column: Answer & In-depth Analysis */}
              <div className="center-results-column">
                <div className="results-header-bar">
                  <div className="header-title-group">
                    <span className="eyebrow-tag">SEEKOVA INTELLIGENT SEARCH</span>
                    <h1 className="query-heading">Results for "{query}"</h1>
                  </div>
                  <div className="result-stats">
                    {results.length} grounded document matches
                  </div>
                </div>

                {loading ? (
                  <div className="seekova-loader-box">
                    <SeekovaOrb state="searching" size={64} />
                    <p className="loader-text">
                      Seekova is computing TF-IDF similarity vectors & synthesizing answer...
                    </p>
                  </div>
                ) : searchError ? (
                  <div className="seekova-error-card">
                    <AlertTriangle size={32} className="error-icon" />
                    <h3>Search Engine Request Failed</h3>
                    <p>{searchError}</p>
                    <button
                      className="retry-btn"
                      onClick={() => performSearch(query)}
                    >
                      <RefreshCw size={16} />
                      <span>Retry Search</span>
                    </button>
                  </div>
                ) : (
                  <>
                    {/* AI Answer Synthesis Card */}
                    {answer && (
                      <AnswerCard
                        query={query}
                        answer={answer}
                        activeMode={activeMode}
                        topDoc={results[0]}
                      />
                    )}

                    {/* Comparison Matrix (if vs query) */}
                    <ComparisonView query={query} />

                    {/* Interactive Knowledge Map */}
                    <KnowledgeMap
                      query={query}
                      results={results}
                      onSelectNode={performSearch}
                    />

                    {/* Search Journey Timeline */}
                    <SearchJourney
                      query={query}
                      onSelectSearch={performSearch}
                    />

                    {/* Document Results List */}
                    <div className="document-results-list">
                      <div className="list-title">
                        <Layers size={16} />
                        <span>INDEXED GROUNDED DOCUMENTS ({results.length})</span>
                      </div>

                      {results.length === 0 ? (
                        <div className="no-results-card">
                          <h3>No matching documents found in index</h3>
                          <p>
                            Try uploading documents (PDF, DOCX, TXT, MD) using the + button on the search bar or try different keywords.
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

                    {/* Related Questions Bottom Section */}
                    <RelatedQuestions
                      query={query}
                      onSelectSearch={performSearch}
                    />
                  </>
                )}
              </div>

              {/* Right Panel: Grounded Source Cards */}
              <div className="right-sources-column">
                <div className="sources-column-header">
                  <h3>GROUNDED SOURCES ({results.length})</h3>
                </div>

                <div className="sources-cards-scroll">
                  {results.length === 0 ? (
                    <div className="empty-sources-notice">
                      <span>No direct source documents match query.</span>
                    </div>
                  ) : (
                    results.map((res, index) => (
                      <SourceCard
                        key={res.id}
                        result={res}
                        activeMode={activeMode}
                        query={query}
                        citationNumber={index + 1}
                      />
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Sticky Bottom Search Command Center */}
          <SearchBar
            query={query}
            setQuery={setQuery}
            onSearch={performSearch}
            uploadedFiles={uploadedFiles}
            setUploadedFiles={setUploadedFiles}
            activeMode={activeMode}
            setActiveMode={setActiveMode}
          />
        </main>
      </div>

      {/* Command Palette Modal (Ctrl + K) */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
        onNewSearch={newSearch}
        onSelectMode={(m) => {
          setActiveMode(m);
          setCommandPaletteOpen(false);
        }}
        onSelectSearch={(q) => {
          performSearch(q);
          setCommandPaletteOpen(false);
        }}
        history={history}
        onTriggerUpload={triggerFileUpload}
      />
    </div>
  );
}

export default App;

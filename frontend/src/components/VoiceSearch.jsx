import React, { useState } from "react";
import { Mic, Volume2, Search, X, Check, Radio } from "lucide-react";
import { SecondlyBrainOrb } from "./SecondlyBrainLogo";

function VoiceSearch({ onSearch, setQuery }) {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");

  function startListening() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;

    recognition.onstart = () => setListening(true);

    recognition.onresult = (e) => {
      let current = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        current += e.results[i][0].transcript;
      }
      setTranscript(current);
      setQuery(current);
    };

    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognition.start();
  }

  return (
    <div className="voice-search-card">
      <div className="voice-orb-wrapper">
        <SecondlyBrainOrb state={listening ? "listening" : "idle"} size={110} />
      </div>

      <h3 className="voice-title">
        {listening ? "Listening to your voice..." : "Tap Microphone to Speak"}
      </h3>

      <div className="transcript-box">
        {transcript ? (
          <p className="transcript-text">"{transcript}"</p>
        ) : (
          <p className="transcript-placeholder">
            Speak naturally (e.g. "What is quantum computing?")
          </p>
        )}
      </div>

      <div className="voice-controls">
        <button
          className={`mic-trigger-btn ${listening ? "listening" : ""}`}
          onClick={startListening}
        >
          <Mic size={24} />
        </button>

        {transcript && (
          <button
            className="execute-voice-btn"
            onClick={() => onSearch(transcript)}
          >
            <Search size={16} />
            <span>Search Query</span>
          </button>
        )}
      </div>
    </div>
  );
}

export default VoiceSearch;

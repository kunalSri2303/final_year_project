import React, { useState, useEffect } from 'react';
import EmotionInput from './components/EmotionInput';
import EmotionDisplay from './components/EmotionDisplay';
import SongList from './components/SongList';
import HistoryPanel from './components/HistoryPanel';

const API_BASE = "http://localhost:8000/api";

function App() {
  const [emotionData, setEmotionData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState("english");

  const handleDetectFace = async (base64Image) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Detect
      const res = await fetch(`${API_BASE}/detect-emotion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image, language })
      });
      if (!res.ok) throw new Error("Failed to detect face emotion");
      const data = await res.json();
      setEmotionData(data);
      
      // 2. Recommend
      await fetchRecommendations(data.emotion);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDetectText = async (text) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/text-emotion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language })
      });
      if (!res.ok) throw new Error("Failed to detect text emotion");
      const data = await res.json();
      setEmotionData(data);
      
      await fetchRecommendations(data.emotion);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async (emotion) => {
    try {
      const res = await fetch(`${API_BASE}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emotion, limit: 10, language })
      });
      if (!res.ok) throw new Error("Failed to fetch recommendations");
      const data = await res.json();
      setRecommendations(data.tracks);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Moodify</h1>
        <p>Emotion-Based Music Recommender</p>
      </header>

      {error && <div className="auth-warning">{error}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        <EmotionInput 
          onDetectFace={handleDetectFace} 
          onDetectText={handleDetectText} 
          disabled={loading} 
          language={language}
          setLanguage={setLanguage}
        />
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {loading ? (
              <div className="glass-card loader-container">
                <div className="spinner"></div>
                <p>Analyzing your mood...</p>
              </div>
            ) : emotionData ? (
              <EmotionDisplay data={emotionData} />
            ) : (
                <div className="glass-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', minHeight: '200px' }}>
                    <p style={{ color: 'var(--text-muted)' }}>Input your mood using the camera or text to see results here.</p>
                </div>
            )}
        </div>
      </div>

      {recommendations && (
        <SongList 
            emotion={emotionData?.emotion} 
            tracks={recommendations} 
        />
      )}

      <HistoryPanel apiBase={API_BASE} />
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import WebcamCapture from './WebcamCapture';

function EmotionInput({ onDetectFace, onDetectText, disabled, language, setLanguage }) {
  const [activeTab, setActiveTab] = useState('camera');
  const [textInput, setTextInput] = useState('');

  const handleSubmitText = () => {
    if (!textInput.trim()) return;
    onDetectText(textInput);
  };

  return (
    <div className="glass-card input-section">
      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'camera' ? 'active' : ''}`}
          onClick={() => setActiveTab('camera')}
        >
          Camera
        </button>
        <button 
          className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          Text Input
        </button>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ marginRight: '0.5rem', color: 'var(--text-muted)' }}>Music Language:</label>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          style={{ background: 'var(--bg-color)', color: 'var(--text-color)', border: '1px solid var(--border-color)', padding: '0.5rem', borderRadius: '8px', cursor: 'pointer' }}
          disabled={disabled}
        >
          <option value="english">English</option>
          <option value="hindi">Hindi / Bollywood</option>
          <option value="spanish">Spanish / Latin</option>
          <option value="korean">Korean / K-Pop</option>
          <option value="japanese">Japanese / J-Pop</option>
        </select>
      </div>

      {activeTab === 'camera' ? (
        <WebcamCapture onCapture={onDetectFace} disabled={disabled} />
      ) : (
        <div className="text-input-container">
          <textarea 
            placeholder="How are you feeling today?" 
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button 
            className="btn" 
            onClick={handleSubmitText} 
            disabled={disabled || !textInput.trim()}
          >
            Detect Emotion
          </button>
        </div>
      )}
    </div>
  );
}

export default EmotionInput;

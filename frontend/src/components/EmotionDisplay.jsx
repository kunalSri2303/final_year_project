import React from 'react';

const EMOTION_EMOJIS = {
  happy: '😄', joy: '😄',
  sad: '😢', sadness: '😢',
  angry: '😠', anger: '😠',
  fear: '😨',
  surprise: '😲',
  disgust: '🤢',
  neutral: '😐',
  love: '🥰'
};

const EMOTION_COLORS = {
  happy: '#f59e0b', joy: '#f59e0b',
  sad: '#3b82f6', sadness: '#3b82f6',
  angry: '#ef4444', anger: '#ef4444',
  fear: '#8b5cf6',
  surprise: '#ec4899',
  disgust: '#10b981',
  neutral: '#94a3b8',
  love: '#f43f5e'
};

function EmotionDisplay({ data }) {
  if (!data) return null;

  const key = data.emotion.toLowerCase();
  const emoji = EMOTION_EMOJIS[key] || '😐';
  const color = EMOTION_COLORS[key] || 'var(--accent-primary)';
  const confText = Math.round(data.confidence * 100);

  return (
    <div className="glass-card emotion-display">
      <div className="emotion-emoji">{emoji}</div>
      <div className="emotion-text" style={{ color }}>{data.emotion}</div>
      
      <div style={{ width: '100%', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
          Confidence: {confText}%
        </p>
        <div className="confidence-bar-container">
          <div 
            className="confidence-bar" 
            style={{ width: `${confText}%`, backgroundColor: color }}
          ></div>
        </div>
      </div>
    </div>
  );
}

export default EmotionDisplay;

import React, { useState, useEffect } from 'react';

function HistoryPanel({ apiBase }) {
  const [history, setHistory] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${apiBase}/history`);
      const data = await res.json();
      setHistory(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="glass-card history-section">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => setIsOpen(!isOpen)}>
        <h3>📚 Interaction History</h3>
        <span>{isOpen ? '▲' : '▼'}</span>
      </div>

      {isOpen && (
        <div style={{ marginTop: '1rem' }}>
          {history.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No history yet.</p>
          ) : (
            history.map((item) => (
              <div key={item.id} className="history-item">
                <div>
                  <strong>{item.emotion}</strong>
                  <div className="history-metadata">
                    {new Date(item.timestamp).toLocaleString()}
                  </div>
                </div>
                <div>{item.tracks?.length || 0} tracks</div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default HistoryPanel;

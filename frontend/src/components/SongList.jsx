import React from 'react';

function SongList({ emotion, tracks }) {
  if (!tracks || tracks.length === 0) return null;

  return (
    <div className="glass-card" style={{ marginTop: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <h2 style={{ margin: 0 }}>Recommended for {emotion}</h2>
        <a 
          href={`https://open.spotify.com/search/${emotion}%20mood/playlists`} 
          target="_blank" 
          rel="noreferrer" 
          className="btn"
          style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '8px' }}
        >
          <svg style={{ width: '20px', height: '20px' }} viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.84.241 1.2zM20.16 9.6C16.32 7.32 9.6 7.14 5.64 8.4c-.6.181-1.32-.12-1.5-.72-.18-.6.12-1.32.72-1.5 4.56-1.44 12.06-1.2 16.56 1.44.6.36.78 1.08.42 1.62-.24.599-.9.779-1.68.36z"></path>
          </svg>
          Open Automated Playlist ↗
        </a>
      </div>
      
      <div className="song-grid">
        {tracks.map((track, i) => (
          <div key={track.id + i} className="glass-card song-card">
            {track.album_art ? (
                <img src={track.album_art} alt={track.album} className="song-art" />
            ) : (
                <div className="song-art" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    🎵 No Art
                </div>
            )}
            <div className="song-info">
              <span className="song-title" title={track.name}>{track.name}</span>
              <span className="song-artist" title={track.artist}>{track.artist}</span>
            </div>
            
            {track.preview_url && (
              <audio controls className="audio-preview">
                <source src={track.preview_url} type="audio/mpeg" />
                Browser does not support audio.
              </audio>
            )}
            
            <a 
              href={track.spotify_url} 
              target="_blank" 
              rel="noreferrer" 
              className="play-link"
            >
              Open in Spotify ↗
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SongList;

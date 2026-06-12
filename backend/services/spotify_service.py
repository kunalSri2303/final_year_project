import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import settings
from models.schemas import TrackInfo
import random

sp = None

if settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET:
    auth_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("Spotify Client Initialized")
else:
    print("WARNING: Spotify credentials not found. Using mock data.")

def get_mock_tracks(seed_genres, limit, language="english") -> list:
    """Mock fallback when Spotify credentials aren't provided"""
    genre = seed_genres[0] if seed_genres else "pop"
    lang_prefix = f" [{language.capitalize()}]" if language and language.lower() != "english" else ""
    search_query = f"{genre} {language}".strip().replace(" ", "%20")
    
    mock_tracks = [
        TrackInfo(
            id=f"track_{genre}_1",
            name=f"{genre.capitalize()}{lang_prefix} Anthem",
            artist="Mock Artist A",
            album="Mock Album",
            preview_url=None,
            spotify_url=f"https://open.spotify.com/search/{search_query}%20track",
            album_art="https://placehold.co/400x400/1DB954/FFFFFF?text=Mock+Track+1"
        ),
        TrackInfo(
            id=f"track_{genre}_2",
            name=f"Vibing {genre}{lang_prefix}",
            artist="Mock Artist B",
            album="Mock Album 2",
            preview_url=None,
            spotify_url=f"https://open.spotify.com/search/{search_query}%20vibes",
            album_art="https://placehold.co/400x400/1DB954/FFFFFF?text=Mock+Track+2"
        ),
        TrackInfo(
            id=f"track_{genre}_3",
            name=f"Classic {genre}{lang_prefix} Track",
            artist="Mock Artist C",
            album="Mock Album 3",
            preview_url=None,
            spotify_url=f"https://open.spotify.com/search/{search_query}%20classic",
            album_art="https://placehold.co/400x400/1DB954/FFFFFF?text=Mock+Track+3"
        )
    ]
    
    # Return requested limit or available tracks
    return mock_tracks[:limit]

def get_recommendations(seed_genres: list, target_valence: float, target_energy: float, limit: int = 10, language: str = "english") -> list:
    if not sp:
        return get_mock_tracks(seed_genres, limit, language)
        
    try:
        results = sp.recommendations(
            seed_genres=seed_genres[:min(len(seed_genres), 5)], # max 5 seeds
            target_valence=target_valence,
            target_energy=target_energy,
            limit=limit
        )
        
        tracks = []
        for track in results['tracks']:
            album_art = ""
            if track['album']['images']:
                album_art = track['album']['images'][0]['url']
                
            artists = ", ".join([artist['name'] for artist in track['artists']])
            
            tracks.append(TrackInfo(
                id=track['id'],
                name=track['name'],
                artist=artists,
                album=track['album']['name'],
                preview_url=track['preview_url'],
                spotify_url=track['external_urls'].get("spotify", ""),
                album_art=album_art
            ))
            
        return tracks
    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        return get_mock_tracks(seed_genres, limit, language)

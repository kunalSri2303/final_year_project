from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class EmotionRequest(BaseModel):
    image: Optional[str] = None # Base64 encoded image
    language: str = "english"
    
class TextEmotionRequest(BaseModel):
    text: str
    language: str = "english"

class EmotionResult(BaseModel):
    emotion: str
    confidence: float
    source: str # 'face' or 'text'
    all_emotions: Dict[str, float]

class RecommendRequest(BaseModel):
    emotion: str
    limit: int = 10
    language: str = "english"

class TrackInfo(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    preview_url: Optional[str]
    spotify_url: str
    album_art: str

class RecommendResponse(BaseModel):
    emotion: str
    tracks: List[TrackInfo]
    mood_params: Dict[str, Any] # e.g. valence, energy, seed genres used

class HistoryResponse(BaseModel):
    id: int
    emotion: str
    timestamp: str
    tracks: List[TrackInfo]

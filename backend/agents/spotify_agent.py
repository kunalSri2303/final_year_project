from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from services.spotify_service import get_recommendations
from models.schemas import TrackInfo

class SpotifyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SpotifyAgent")

    async def _process(self, params: Dict[str, Any], limit: int = 10) -> List[TrackInfo]:
        tracks = get_recommendations(
            seed_genres=params.get("seed_genres", ["pop"]),
            target_valence=params.get("target_valence", 0.5),
            target_energy=params.get("target_energy", 0.5),
            limit=limit,
            language=params.get("language", "english")
        )
        return tracks

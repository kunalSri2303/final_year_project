from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RecommendationAgent")
        
        # Mappings of emotion to Spotify audio features and genre seeds
        self.emotion_map = {
            "happy": {"target_energy": 0.8, "target_valence": 0.9, "seed_genres": ["pop", "dance", "happy"]},
            "sad": {"target_energy": 0.2, "target_valence": 0.2, "seed_genres": ["acoustic", "piano", "sad"]},
            "angry": {"target_energy": 0.9, "target_valence": 0.2, "seed_genres": ["rock", "metal", "hard-rock"]},
            "fear": {"target_energy": 0.4, "target_valence": 0.3, "seed_genres": ["ambient", "classical", "chill"]},
            "surprise": {"target_energy": 0.7, "target_valence": 0.6, "seed_genres": ["electronic", "indie-pop", "synth-pop"]},
            "disgust": {"target_energy": 0.6, "target_valence": 0.3, "seed_genres": ["alternative", "grunge"]},
            "neutral": {"target_energy": 0.5, "target_valence": 0.5, "seed_genres": ["pop", "chill", "indie"]},
            # Common text pipeline outputs map to the above
            "joy": {"target_energy": 0.8, "target_valence": 0.9, "seed_genres": ["pop", "dance", "happy"]},
            "love": {"target_energy": 0.6, "target_valence": 0.8, "seed_genres": ["romance", "r-n-b", "pop"]},
            "sadness": {"target_energy": 0.2, "target_valence": 0.2, "seed_genres": ["acoustic", "piano", "sad"]},
            "anger": {"target_energy": 0.9, "target_valence": 0.2, "seed_genres": ["rock", "metal", "hard-rock"]}
        }

    async def _process(self, emotion: str, language: str = "english") -> Dict[str, Any]:
        emotion_key = emotion.lower()
        if emotion_key in self.emotion_map:
            params = self.emotion_map[emotion_key].copy()
            params["language"] = language
            return params
        else:
            # Fallback for unmapped emotions
            params = self.emotion_map["neutral"].copy()
            params["language"] = language
            return params

from agents.emotion_agent import EmotionDetectionAgent
from agents.recommendation_agent import RecommendationAgent
from agents.spotify_agent import SpotifyAgent
from models.schemas import EmotionResult, RecommendResponse

class OrchestratorAgent:
    def __init__(self):
        self.emotion_agent = EmotionDetectionAgent()
        self.recommendation_agent = RecommendationAgent()
        self.spotify_agent = SpotifyAgent()

    async def process_emotion_input(self, source: str, data: str, limit: int = 10, language: str = "english") -> RecommendResponse:
        # Step 1: Detect Emotion
        emotion_result: EmotionResult = await self.emotion_agent.execute(source=source, data=data)
        
        # Step 2: Extract Recommendation Parameters
        mood_params = await self.recommendation_agent.execute(emotion=emotion_result.emotion, language=language)
        
        # Step 3: Fetch Spotify Tracks
        tracks = await self.spotify_agent.execute(params=mood_params, limit=limit)
        
        # Step 4: Construct Response
        return RecommendResponse(
            emotion=emotion_result.emotion,
            tracks=tracks,
            mood_params=mood_params
        )
        
    async def process_emotion_only(self, emotion: str, limit: int = 10, language: str = "english") -> RecommendResponse:
        # Step 1: Skip detection, use provided emotion
        mood_params = await self.recommendation_agent.execute(emotion=emotion, language=language)
        
        # Step 2: Fetch Spotify Tracks
        tracks = await self.spotify_agent.execute(params=mood_params, limit=limit)
        
        return RecommendResponse(
            emotion=emotion,
            tracks=tracks,
            mood_params=mood_params
        )

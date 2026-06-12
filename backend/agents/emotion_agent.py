from typing import Optional, Dict
from models.schemas import EmotionResult
from agents.base_agent import BaseAgent
from services.face_service import analyze_face
from services.text_service import analyze_text

class EmotionDetectionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="EmotionDetectionAgent")

    async def _process(self, source: str, data: str) -> EmotionResult:
        if source == "face":
            return await self._detect_face(data)
        elif source == "text":
            return await self._detect_text(data)
        else:
            raise ValueError(f"Unknown source: {source}")

    async def _detect_face(self, base64_image: str) -> EmotionResult:
        result = analyze_face(base64_image)
        return EmotionResult(
            emotion=result["emotion"],
            confidence=result["confidence"],
            source="face",
            all_emotions=result["all_emotions"]
        )

    async def _detect_text(self, text: str) -> EmotionResult:
        result = analyze_text(text)
        return EmotionResult(
            emotion=result["emotion"],
            confidence=result["confidence"],
            source="text",
            all_emotions=result["all_emotions"]
        )

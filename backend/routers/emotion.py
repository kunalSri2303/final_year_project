from fastapi import APIRouter, HTTPException, Depends
from models.schemas import EmotionRequest, TextEmotionRequest, EmotionResult
from agents.orchestrator import OrchestratorAgent

router = APIRouter()

# Initialize the orchestrator globally for the router to avoid recreating models
orchestrator = OrchestratorAgent()

@router.post("/detect-emotion", response_model=EmotionResult)
async def detect_face_emotion(request: EmotionRequest):
    if not request.image:
        raise HTTPException(status_code=400, detail="Image is required")
        
    try:
        # Step 1: Detect Emotion via Orchestrator's Emotion Agent
        result = await orchestrator.emotion_agent.execute(source="face", data=request.image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-emotion", response_model=EmotionResult)
async def detect_text_emotion(request: TextEmotionRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
        
    try:
        # Step 1: Detect Emotion via Orchestrator's Emotion Agent
        result = await orchestrator.emotion_agent.execute(source="text", data=request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

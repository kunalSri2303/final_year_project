from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from models.schemas import RecommendRequest, RecommendResponse, HistoryResponse, TrackInfo
from models.database import get_db, InteractionHistory, RecommendedTrack
from agents.orchestrator import OrchestratorAgent
import json

router = APIRouter()

# Global orchestrator
orchestrator = OrchestratorAgent()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()


@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendation(request: RecommendRequest, db: Session = Depends(get_db)):
    try:
        response = await orchestrator.process_emotion_only(emotion=request.emotion, limit=request.limit, language=request.language)
        
        # Save to DB
        new_interaction = InteractionHistory(
            emotion=response.emotion,
            confidence=1.0, # Not provided when jumping straight to recommend
            source="manual"
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        
        for track in response.tracks:
            new_track = RecommendedTrack(
                interaction_id=new_interaction.id,
                track_id=track.id,
                name=track.name,
                artist=track.artist,
                album=track.album,
                preview_url=track.preview_url,
                spotify_url=track.spotify_url,
                album_art=track.album_art
            )
            db.add(new_track)
        db.commit()
        
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[HistoryResponse])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    interactions = db.query(InteractionHistory).order_by(InteractionHistory.timestamp.desc()).limit(limit).all()
    
    result = []
    for interaction in interactions:
        tracks = []
        for track in interaction.recommendations:
            tracks.append(TrackInfo(
                id=track.track_id,
                name=track.name,
                artist=track.artist,
                album=track.album,
                preview_url=track.preview_url,
                spotify_url=track.spotify_url,
                album_art=track.album_art
            ))
            
        result.append(HistoryResponse(
            id=interaction.id,
            emotion=interaction.emotion,
            timestamp=interaction.timestamp.isoformat(),
            tracks=tracks
        ))
        
    return result

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            source = payload.get("type")
            content = payload.get("data")
            limit = payload.get("limit", 10)
            
            if not source or not content:
                await manager.send_personal_message({"error": "Invalid payload format."}, websocket)
                continue
                
            language = payload.get("language", "english")
            # Process Full Flow (Detection + Recommendation)
            response = await orchestrator.process_emotion_input(source=source, data=content, limit=limit, language=language)
            
            # Save to history implicitly
            new_interaction = InteractionHistory(
                emotion=response.emotion,
                confidence=0.0, # Approximate, available in full flow but ignored for brevity in DB
                source=source,
                input_data=content if source == "text" else None # Don't store large image
            )
            db.add(new_interaction)
            db.commit()
            db.refresh(new_interaction)
            
            for track in response.tracks:
                new_track = RecommendedTrack(
                    interaction_id=new_interaction.id,
                    track_id=track.id,
                    name=track.name,
                    artist=track.artist,
                    album=track.album,
                    preview_url=track.preview_url,
                    spotify_url=track.spotify_url,
                    album_art=track.album_art
                )
                db.add(new_track)
            db.commit()
            
            # Send result back
            await manager.send_personal_message(response.model_dump(), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WS Error: {e}")
        await manager.send_personal_message({"error": str(e)}, websocket)
        manager.disconnect(websocket)

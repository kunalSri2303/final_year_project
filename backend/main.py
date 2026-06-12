from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import emotion, recommend
from models.database import init_db
from config import settings
import json

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# this is cahage

@app.on_event("startup")
async def startup_event():
    init_db()
    # Initialize ML models implicitly by importing services below if needed
    print("Database Initialized")

app.include_router(emotion.router, prefix="/api", tags=["emotion"])
app.include_router(recommend.router, prefix="/api", tags=["recommend"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

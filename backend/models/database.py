from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import settings
import json

#sqlalchemy is used in previous backend for database connectivity.
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class InteractionHistory(Base):
    __tablename__ = "interaction_history"

    id = Column(Integer, primary_key=True, index=True)
    emotion = Column(String, index=True)
    confidence = Column(Float)
    source = Column(String)  # face or text
    input_data = Column(Text, nullable=True) # Could be text used, or omited for image due to size
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    recommendations = relationship("RecommendedTrack", back_populates="interaction")

class RecommendedTrack(Base):
    __tablename__ = "recommended_tracks"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interaction_history.id"))
    track_id = Column(String)
    name = Column(String)
    artist = Column(String)
    album = Column(String)
    preview_url = Column(String, nullable=True)
    spotify_url = Column(String)
    album_art = Column(String)
    
    interaction = relationship("InteractionHistory", back_populates="recommendations")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

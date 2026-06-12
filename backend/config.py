from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Emotion-Based Music Recommender"
    DATABASE_URL: str = "sqlite:///./recommender.db"
    
    # Spotify Credentials (Optional, mock will be used if empty)
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""
    
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()

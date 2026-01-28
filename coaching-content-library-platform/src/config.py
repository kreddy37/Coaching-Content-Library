"""Application settings using pydantic-settings."""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    youtube_api_key: str
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "goalie-drill-aggregator/1.0"

    # Phase 2: Discord Bot and API
    discord_bot_token: str = ""
    api_base_url: str = "http://localhost:8000"

    database_path: str = "data/content.db"
    
    youtube_discover_terms: list[str] = Field(default=[
        "goalie drills",
        "hockey goalie training",
        "goaltender practice",
        "nhl goalie drills",
        "hockey goalie coaching"
    ])
    
    reddit_subreddits: list[str] = Field(default=[
        "hockeygoalies",
        "hockeyplayers"
    ])
    
    instagram_hashtags: list[str] = Field(default=[
        "goalies",
        "goalie",
        "goaliecoaches",
        "goaliedrills",
        "goalieskating",
        "goaliedevelopment",
        "hockeygoalie",
        "goalietraining"
    ])
    
    tiktok_hashtags: list[str] = Field(default=[
        "goalies",
        "goalie",
        "goaliecoaches",
        "goaliedrills",
        "goalieskating",
        "goaliedevelopment",
        "hockeygoalie",
        "goalietraining"
    ])
    
    prefetch_multiplier: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

class ContentSource(str, Enum):
    YOUTUBE = "YouTube"
    REDDIT = "Reddit"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    ARTICLE = "Article"
    
class ContentType(str, Enum):
    VIDEO = "Video"
    POST = "Post"
    ARTICLE = "Article"
    IMAGE = "Image"

class Difficulty(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    
class ContentItem(BaseModel):
    """
    Unified model for all content sources.
    
    Design decision: One model with optional source-specific fields
    vs. inheritance hierarchy. We chose flat + optional because:
    1. Simpler serialization to/from database
    2. Easier to query across sources
    3. Source-specific fields are metadata, not behavior
    """
    # Universal fields (all sources have these)
    id: str                          # Source-specific ID (e.g., YouTube video ID)
    source: ContentSource
    content_type: ContentType
    title: str
    url: str
    description: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    thumbnail_url: Optional[str] = None
    
    # Engagement metrics (optional, not all sources provide)
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    
    # Source-specific metadata stored as dict
    # This avoids explosion of optional fields while preserving data
    source_metadata: dict = Field(default_factory=dict)
    
    # User-added data (for Phase 2)
    tags: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
    saved_at: Optional[datetime] = None
    collection_id: Optional[str] = None

    # Drill-specific metadata (Phase 2)
    drill_tags: list[str] = Field(default_factory=list)  # e.g., ["butterfly", "lateral-movement", "warmup"]
    drill_description: Optional[str] = None  # Custom drill description (separate from auto-fetched description)
    difficulty: Optional[Difficulty] = None   # Beginner, Intermediate, Advanced (PascalCase)
    equipment: Optional[str] = None    # e.g., "pucks, cones"
    age_group: Optional[str] = None    # e.g., "bantam", "12-14"
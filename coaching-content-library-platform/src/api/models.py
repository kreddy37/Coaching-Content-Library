"""Pydantic models for API requests and responses."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from ..models.content import ContentSource, ContentType


class ContentItemResponse(BaseModel):
    """Response model for content items."""

    id: str
    source: ContentSource
    content_type: ContentType
    title: str
    url: str
    description: Optional[str] = None
    author: Optional[str] = None
    thumbnail_url: Optional[str] = None
    published_at: Optional[datetime] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None

    # Phase 2: Drill-specific metadata
    drill_tags: list[str] = []
    drill_description: Optional[str] = None
    difficulty: Optional[str] = None
    equipment: Optional[str] = None
    age_group: Optional[str] = None

    source_metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class SaveContentRequest(BaseModel):
    """Request model for saving content from URL.

    Note: For Instagram and TikTok, title and description are recommended
    since these platforms don't provide automatic metadata fetching.
    """

    url: str = Field(..., description="URL of the content to save")
    source: ContentSource = Field(..., description="Content source platform")

    # Optional basic metadata (recommended for Instagram/TikTok)
    title: Optional[str] = Field(None, description="Content title (recommended for Instagram/TikTok)")
    description: Optional[str] = Field(None, description="Content description (recommended for Instagram/TikTok)")
    author: Optional[str] = Field(None, description="Content author/creator")

    # Optional drill-specific metadata
    drill_tags: Optional[list[str]] = Field(None, description="Drill tags (e.g., ['butterfly', 'lateral-movement', 'warmup'])")
    drill_description: Optional[str] = Field(None, description="Custom drill description")
    difficulty: Optional[str] = Field(None, description="Difficulty level (beginner, intermediate, advanced)")
    equipment: Optional[str] = Field(None, description="Required equipment (e.g., 'pucks, cones')")
    age_group: Optional[str] = Field(None, description="Target age group (e.g., 'bantam', '12-14')")


class UpdateMetadataRequest(BaseModel):
    """Request model for updating content metadata."""

    drill_tags: Optional[list[str]] = Field(None, description="Drill tags")
    drill_description: Optional[str] = Field(None, description="Custom drill description")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    equipment: Optional[str] = Field(None, description="Required equipment")
    age_group: Optional[str] = Field(None, description="Target age group")


class SearchContentRequest(BaseModel):
    """Request model for searching content."""

    query: Optional[str] = Field(None, description="Search query text")
    source: Optional[ContentSource] = Field(None, description="Filter by content source")
    content_type: Optional[ContentType] = Field(None, description="Filter by content type")
    difficulty: Optional[str] = Field(None, description="Filter by difficulty level")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results")


class ContentListResponse(BaseModel):
    """Response model for content lists."""

    items: list[ContentItemResponse]
    total: int

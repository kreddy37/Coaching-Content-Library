"""API routes for content management."""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from ..storage.sqlite import SQLiteRepository
from ..models.content import ContentSource, ContentType
from ..config import settings
from ..ingestors.youtube import YouTubeIngestor
from ..ingestors.reddit import RedditIngestor
from ..ingestors.instagram import InstagramIngestor
from ..ingestors.tiktok import TikTokIngestor
from .models import (
    SaveContentRequest,
    UpdateMetadataRequest,
    ContentItemResponse,
    ContentListResponse,
)

router = APIRouter(tags=["content"])

# Initialize repository
repository = SQLiteRepository()

# Initialize ingestors with credentials from settings
ingestors = {
    ContentSource.YOUTUBE: YouTubeIngestor(api_key=settings.youtube_api_key),
    ContentSource.REDDIT: RedditIngestor(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    ),
    ContentSource.INSTAGRAM: InstagramIngestor(),
    ContentSource.TIKTOK: TikTokIngestor(),
}


@router.post("/content", response_model=ContentItemResponse, status_code=201)
async def save_content(request: SaveContentRequest):
    """Save content from URL.

    Fetches content metadata from the source platform and saves to the database.
    Optionally accepts metadata overrides for drill-specific fields.
    """
    # Get appropriate ingestor
    ingestor = ingestors.get(request.source)
    if not ingestor:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported content source: {request.source}"
        )

    # Fetch content from URL
    content = ingestor.from_url(request.url)
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch content from URL: {request.url}"
        )

    # Apply basic metadata overrides if provided (especially useful for Instagram/TikTok)
    if request.title is not None:
        content.title = request.title
    if request.description is not None:
        content.description = request.description
    if request.author is not None:
        content.author = request.author

    # Apply drill-specific metadata overrides if provided
    if request.drill_tags is not None:
        content.drill_tags = request.drill_tags
    if request.drill_description is not None:
        content.drill_description = request.drill_description
    if request.difficulty is not None:
        content.difficulty = request.difficulty
    if request.equipment is not None:
        content.equipment = request.equipment
    if request.age_group is not None:
        content.age_group = request.age_group

    # Save to database
    repository.save(content)

    return ContentItemResponse.model_validate(content)


@router.get("/content", response_model=ContentListResponse)
async def list_content(
    query: Optional[str] = Query(None, description="Search query"),
    source: Optional[ContentSource] = Query(None, description="Filter by source"),
    content_type: Optional[ContentType] = Query(None, description="Filter by type"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
):
    """List and search content.

    Supports filtering by various criteria and full-text search.
    """
    # Build search criteria
    criteria = {}
    if source:
        criteria["source"] = source
    if content_type:
        criteria["content_type"] = content_type
    if difficulty:
        criteria["difficulty"] = difficulty

    # Search repository
    if query:
        results = repository.search(query, criteria=criteria, limit=limit)
    else:
        # Get all with filters
        results = repository.search("", criteria=criteria, limit=limit)

    return ContentListResponse(
        items=[ContentItemResponse.model_validate(item) for item in results],
        total=len(results)
    )


@router.get("/content/{content_id}", response_model=ContentItemResponse)
async def get_content(content_id: str):
    """Get a specific content item by ID."""
    content = repository.get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Content not found: {content_id}"
        )

    return ContentItemResponse.model_validate(content)


@router.put("/content/{content_id}/metadata", response_model=ContentItemResponse)
async def update_metadata(content_id: str, request: UpdateMetadataRequest):
    """Update drill-specific metadata for a content item.

    Only updates fields that are explicitly provided (non-null).
    """
    # Get existing content
    content = repository.get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Content not found: {content_id}"
        )

    # Update metadata fields (only if provided)
    if request.drill_tags is not None:
        content.drill_tags = request.drill_tags
    if request.drill_description is not None:
        content.drill_description = request.drill_description
    if request.difficulty is not None:
        content.difficulty = request.difficulty
    if request.equipment is not None:
        content.equipment = request.equipment
    if request.age_group is not None:
        content.age_group = request.age_group

    # Save updated content
    repository.save(content)

    return ContentItemResponse.model_validate(content)


@router.delete("/content/{content_id}", status_code=204)
async def delete_content(content_id: str):
    """Delete a content item."""
    content = repository.get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Content not found: {content_id}"
        )

    # Delete using source and ID from the retrieved content
    repository.delete(content.source, content.id)
    return JSONResponse(status_code=204, content=None)

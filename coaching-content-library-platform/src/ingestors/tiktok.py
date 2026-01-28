"""TikTok content ingestor.

Creates minimal ContentItem from TikTok URLs.
Metadata should be provided by the user when saving.
"""
import logging
import re
from typing import Optional

from ..models.content import ContentItem, ContentSource, ContentType
from .base import BaseIngestor

logger = logging.getLogger(__name__)


class TikTokIngestor(BaseIngestor):
    """Ingestor for TikTok videos.

    Creates minimal ContentItem objects with URL and ID only.
    Provide title, description, and metadata when saving content.
    """

    def __init__(self):
        """Initialize TikTok ingestor.

        No authentication required for oEmbed API.
        """
        pass

    @property
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        return ContentSource.TIKTOK

    def search(self, query: str, max_results: int = 10, **kwargs) -> list[ContentItem]:
        """TikTok search not supported via oEmbed.

        Args:
            query: Search terms (not used)
            max_results: Maximum number of results (not used)
            **kwargs: Additional parameters (not used)

        Raises:
            NotImplementedError: TikTok search not available
        """
        raise NotImplementedError(
            "TikTok search not supported — use from_url to save content you find"
        )

    def get_recent(self, max_results: int = 10) -> list[ContentItem]:
        """TikTok discovery not supported via oEmbed.

        Args:
            max_results: Maximum number of results (not used)

        Raises:
            NotImplementedError: TikTok discovery not available
        """
        raise NotImplementedError(
            "TikTok discover not supported — use from_url to save content you find"
        )

    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Fetch a specific TikTok video by its ID.

        Note: TikTok URLs require both username and video ID.
        This method attempts common URL patterns but may not work
        for all videos. Use from_url() with the full URL when possible.

        Args:
            content_id: TikTok video ID

        Returns:
            ContentItem if found, None otherwise
        """
        # TikTok URLs require username, which we don't have from just the ID
        # Try a generic pattern, but this may not always work
        # Better to use from_url() with the full URL
        logger.warning(
            "TikTok get_by_id() has limited support. "
            "Use from_url() with the full TikTok URL for best results."
        )

        # Try constructing a URL (this is a best-effort attempt)
        # Common pattern: https://www.tiktok.com/@username/video/{id}
        # Without username, we can't construct a proper URL
        # Return None and log a warning
        logger.error(
            f"Cannot fetch TikTok video by ID alone: {content_id}. "
            "TikTok requires the full URL including username."
        )
        return None

    def from_url(self, url: str) -> Optional[ContentItem]:
        """Extract video ID from TikTok URL and create minimal ContentItem.

        Note: This method creates a minimal ContentItem with just the URL and ID.
        You should provide title, description, and other metadata via the API when saving.

        Args:
            url: TikTok video URL (e.g., "https://www.tiktok.com/@user/video/123")

        Returns:
            ContentItem with URL and ID, None if URL is invalid
        """
        # Extract video ID from URL
        video_id = self._extract_video_id(url)
        if not video_id:
            logger.warning(f"Could not extract video ID from URL: {url}")
            return None

        # Return minimal ContentItem - user will provide metadata
        return ContentItem(
            id=video_id,
            source=ContentSource.TIKTOK,
            content_type=ContentType.VIDEO,
            title="TikTok Video",
            url=url,
            description=None,
            author=None,
            thumbnail_url=None,
            published_at=None,
            view_count=None,
            like_count=None,
            comment_count=None,
            source_metadata={
                "note": "Provide title, description, and other metadata when saving"
            },
        )

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from TikTok URL.

        Args:
            url: TikTok URL

        Returns:
            Video ID if found, None otherwise
        """
        # Match patterns like:
        # https://www.tiktok.com/@username/video/1234567890
        # https://tiktok.com/@user/video/123
        # https://vm.tiktok.com/ZMabcdef/ (short URL)

        # Standard URL pattern
        match = re.search(r'tiktok\.com/@[\w.-]+/video/(\d+)', url)
        if match:
            return match.group(1)

        # Short URL pattern (vm.tiktok.com)
        # These don't have numeric IDs in the URL, use the short code as ID
        match = re.search(r'vm\.tiktok\.com/([A-Za-z0-9]+)', url)
        if match:
            return match.group(1)

        return None

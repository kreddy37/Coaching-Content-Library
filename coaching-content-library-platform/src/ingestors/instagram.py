"""Instagram content ingestor.

Creates minimal ContentItem from Instagram URLs.
Metadata should be provided by the user when saving.
"""
import logging
import re
from typing import Optional

from ..models.content import ContentItem, ContentSource, ContentType
from .base import BaseIngestor

logger = logging.getLogger(__name__)


class InstagramIngestor(BaseIngestor):
    """Ingestor for Instagram posts and reels.

    Note: Instagram's public oEmbed API is deprecated. This ingestor
    creates minimal ContentItem objects with URL and ID only.
    Provide title, description, and metadata when saving content.
    """

    def __init__(self):
        """Initialize Instagram ingestor.

        No authentication required for oEmbed API.
        """
        pass

    @property
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        return ContentSource.INSTAGRAM

    def search(self, query: str, max_results: int = 10, **kwargs) -> list[ContentItem]:
        """Instagram search not supported via oEmbed.

        Args:
            query: Search terms (not used)
            max_results: Maximum number of results (not used)
            **kwargs: Additional parameters (not used)

        Raises:
            NotImplementedError: Instagram search not available
        """
        raise NotImplementedError(
            "Instagram search not supported — use from_url to save content you find"
        )

    def get_recent(self, max_results: int = 10) -> list[ContentItem]:
        """Instagram discovery not supported via oEmbed.

        Args:
            max_results: Maximum number of results (not used)

        Raises:
            NotImplementedError: Instagram discovery not available
        """
        raise NotImplementedError(
            "Instagram discover not supported — use from_url to save content you find"
        )

    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Fetch a specific Instagram post by its shortcode.

        Args:
            content_id: Instagram post shortcode (e.g., "ABC123xyz")

        Returns:
            ContentItem if found, None otherwise
        """
        # Construct Instagram URL from shortcode
        url = f"https://www.instagram.com/p/{content_id}/"
        return self.from_url(url)

    def from_url(self, url: str) -> Optional[ContentItem]:
        """Extract shortcode from Instagram URL and create minimal ContentItem.

        Note: Instagram's oEmbed API is deprecated. This method creates a minimal
        ContentItem with just the URL and ID. You should provide title, description,
        and other metadata via the API when saving.

        Args:
            url: Instagram post URL (e.g., "https://www.instagram.com/p/ABC123xyz/")

        Returns:
            ContentItem with URL and ID, None if URL is invalid
        """
        # Extract shortcode from URL
        shortcode = self._extract_shortcode(url)
        if not shortcode:
            logger.warning(f"Could not extract shortcode from URL: {url}")
            return None

        # Determine content type from URL
        content_type = self._determine_content_type(url)

        # Return minimal ContentItem - user will provide metadata
        return ContentItem(
            id=shortcode,
            source=ContentSource.INSTAGRAM,
            content_type=content_type,
            title="Instagram " + ("Reel" if content_type == ContentType.VIDEO else "Post"),
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

    def _extract_shortcode(self, url: str) -> Optional[str]:
        """Extract shortcode from Instagram URL.

        Args:
            url: Instagram URL

        Returns:
            Shortcode if found, None otherwise
        """
        # Match patterns like:
        # https://www.instagram.com/p/SHORTCODE/
        # https://www.instagram.com/reel/SHORTCODE/
        # https://instagram.com/p/SHORTCODE/
        match = re.search(r'instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)', url)
        if match:
            return match.group(1)
        return None

    def _determine_content_type(self, url: str) -> ContentType:
        """Determine content type based on URL.

        Args:
            url: Instagram URL

        Returns:
            ContentType.VIDEO if /reel/, otherwise ContentType.IMAGE
        """
        if '/reel/' in url.lower():
            return ContentType.VIDEO
        return ContentType.IMAGE

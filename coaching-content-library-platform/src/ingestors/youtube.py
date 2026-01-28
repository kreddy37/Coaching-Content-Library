"""YouTube content ingestor."""
import logging
import re
from typing import Optional
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models.content import ContentItem, ContentSource, ContentType
from ..config import settings
from .base import BaseIngestor

logger = logging.getLogger(__name__)


class YouTubeIngestor(BaseIngestor):
    """Ingestor for YouTube videos using the YouTube Data API v3."""

    def __init__(self, api_key: str):
        """Initialize YouTube ingestor.

        Args:
            api_key: YouTube Data API v3 key
        """
        self.api_key = api_key
        self._youtube = None

    @property
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        return ContentSource.YOUTUBE

    @property
    def youtube(self):
        """Lazy-load the YouTube API client."""
        if self._youtube is None:
            self._youtube = build('youtube', 'v3', developerKey=self.api_key)
        return self._youtube

    def search(
        self,
        query: str,
        max_results: int = 10,
        **kwargs
    ) -> list[ContentItem]:
        """Search for YouTube videos matching the query.

        Args:
            query: Search terms (e.g., "butterfly drill goalie")
            max_results: Maximum number of results to return
            **kwargs: Additional YouTube-specific parameters (e.g., order, publishedAfter)

        Returns:
            List of ContentItem objects
        """
        try:
            # Step 1: Search for videos
            search_response = self.youtube.search().list(
                part="snippet",
                type="video",
                q=query,
                maxResults=max_results,
                **kwargs
            ).execute()

            # Extract video IDs
            video_ids = [
                item['id']['videoId']
                for item in search_response.get('items', [])
                if item['id']['kind'] == 'youtube#video'
            ]

            if not video_ids:
                return []

            # Step 2: Get detailed video information including statistics
            videos_response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=','.join(video_ids)
            ).execute()

            # Step 3: Map to ContentItem objects
            content_items = []
            for video in videos_response.get('items', []):
                try:
                    content_item = self._map_to_content_item(video)
                    content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping video {video.get('id')}: {e}")
                    continue

            return content_items

        except HttpError as e:
            logger.error(f"YouTube API error during search: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during YouTube search: {e}")
            return []

    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Fetch a specific YouTube video by its video ID.

        Args:
            content_id: YouTube video ID

        Returns:
            ContentItem if found, None otherwise
        """
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=content_id
            ).execute()

            items = response.get('items', [])
            if not items:
                logger.warning(f"No video found with ID: {content_id}")
                return None

            return self._map_to_content_item(items[0])

        except HttpError as e:
            logger.error(f"YouTube API error fetching video {content_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching video {content_id}: {e}")
            return None

    def from_url(self, url: str) -> Optional[ContentItem]:
        """Fetch a YouTube video from its URL.

        Args:
            url: YouTube video URL (watch, shorts, or youtu.be format)

        Returns:
            ContentItem if found, None otherwise
        """
        video_id = self._extract_video_id(url)
        if not video_id:
            logger.warning(f"Could not extract video ID from URL: {url}")
            return None

        return self.get_by_id(video_id)

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL.

        Supports formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtube.com/shorts/VIDEO_ID
        - https://youtu.be/VIDEO_ID

        Args:
            url: YouTube URL

        Returns:
            Video ID if found, None otherwise
        """
        # Standard watch URL: youtube.com/watch?v=VIDEO_ID
        match = re.search(r'[?&]v=([A-Za-z0-9_-]{11})', url)
        if match:
            return match.group(1)

        # Shorts URL: youtube.com/shorts/VIDEO_ID
        match = re.search(r'youtube\.com/shorts/([A-Za-z0-9_-]{11})', url)
        if match:
            return match.group(1)

        # Short URL: youtu.be/VIDEO_ID
        match = re.search(r'youtu\.be/([A-Za-z0-9_-]{11})', url)
        if match:
            return match.group(1)

        return None

    def get_recent(self, max_results: int = 10) -> list[ContentItem]:
        """Get recent videos for configured discover terms.

        Searches for recent uploads across all terms in settings.youtube_discover_terms,
        deduplicates by video ID, and returns up to max_results items.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of ContentItem objects, ordered by publish date (most recent first)
        """
        try:
            all_video_ids = {}  # Use dict to preserve order and deduplicate

            # Calculate results per term to fetch enough before deduplication
            # Use a multiplier to account for duplicates across terms
            results_per_term = max(5, max_results // len(settings.youtube_discover_terms) + 2)

            for term in settings.youtube_discover_terms:
                try:
                    # Search with order="date" to get recent uploads
                    search_response = self.youtube.search().list(
                        part="snippet",
                        type="video",
                        q=term,
                        maxResults=results_per_term,
                        order="date"
                    ).execute()

                    # Collect video IDs (dict preserves insertion order in Python 3.7+)
                    for item in search_response.get('items', []):
                        if item['id']['kind'] == 'youtube#video':
                            video_id = item['id']['videoId']
                            # Only add if not already seen
                            if video_id not in all_video_ids:
                                all_video_ids[video_id] = True

                    # Stop early if we have enough unique videos
                    if len(all_video_ids) >= max_results:
                        break

                except HttpError as e:
                    logger.error(f"YouTube API error searching term '{term}': {e}")
                    continue
                except Exception as e:
                    logger.error(f"Unexpected error searching term '{term}': {e}")
                    continue

            if not all_video_ids:
                logger.warning("No recent videos found across all discover terms")
                return []

            # Limit to max_results
            video_ids_list = list(all_video_ids.keys())[:max_results]

            # Get detailed video information
            videos_response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=','.join(video_ids_list)
            ).execute()

            # Map to ContentItem objects
            content_items = []
            for video in videos_response.get('items', []):
                try:
                    content_item = self._map_to_content_item(video)
                    content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping video {video.get('id')}: {e}")
                    continue

            # Sort by published date (most recent first)
            content_items.sort(
                key=lambda x: x.published_at if x.published_at else datetime.min,
                reverse=True
            )

            logger.info(f"Retrieved {len(content_items)} recent videos from {len(settings.youtube_discover_terms)} discover terms")
            return content_items

        except Exception as e:
            logger.error(f"Unexpected error in get_recent: {e}")
            return []

    def _map_to_content_item(self, video: dict) -> ContentItem:
        """Map a YouTube video response to a ContentItem.

        Args:
            video: YouTube video resource from API response

        Returns:
            ContentItem object
        """
        video_id = video['id']
        snippet = video.get('snippet', {})
        statistics = video.get('statistics', {})
        content_details = video.get('contentDetails', {})

        # Parse published date
        published_at = None
        if 'publishedAt' in snippet:
            try:
                published_at = datetime.fromisoformat(
                    snippet['publishedAt'].replace('Z', '+00:00')
                )
            except Exception as e:
                logger.warning(f"Failed to parse publishedAt: {e}")

        # Get thumbnail URL (prefer high quality)
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = None
        for quality in ['high', 'medium', 'default']:
            if quality in thumbnails:
                thumbnail_url = thumbnails[quality]['url']
                break

        # Build source_metadata with YouTube-specific fields
        source_metadata = {
            'channel_id': snippet.get('channelId'),
            'channel_title': snippet.get('channelTitle'),
            'duration': content_details.get('duration'),
            'category_id': snippet.get('categoryId'),
        }

        return ContentItem(
            id=video_id,
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title=snippet.get('title', ''),
            url=f"https://www.youtube.com/watch?v={video_id}",
            description=snippet.get('description'),
            author=snippet.get('channelTitle'),
            published_at=published_at,
            thumbnail_url=thumbnail_url,
            view_count=int(statistics.get('viewCount', 0)) if statistics.get('viewCount') else None,
            like_count=int(statistics.get('likeCount', 0)) if statistics.get('likeCount') else None,
            comment_count=int(statistics.get('commentCount', 0)) if statistics.get('commentCount') else None,
            source_metadata=source_metadata,
        )

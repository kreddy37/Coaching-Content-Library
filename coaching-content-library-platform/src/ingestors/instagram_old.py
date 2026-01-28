"""Instagram content ingestor."""
import logging
import time
import re
from typing import Optional
from datetime import datetime
from instaloader import Instaloader, Hashtag, Post
from instaloader.exceptions import QueryReturnedNotFoundException, ConnectionException

from ..models.content import ContentItem, ContentSource, ContentType
from ..config import settings
from .base import BaseIngestor

logger = logging.getLogger(__name__)


class InstagramIngestor(BaseIngestor):
    """Ingestor for Instagram posts using Instaloader."""

    def __init__(self, username: str = "", password: str = ""):
        """Initialize Instagram ingestor.

        Instaloader is configured to not download any files - we only extract metadata.

        Args:
            username: Instagram username for login (optional)
            password: Instagram password for login (optional)
        """
        self.username = username
        self.password = password
        self._loader = None
        self._logged_in = False

    @property
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        return ContentSource.INSTAGRAM

    @property
    def loader(self):
        """Lazy-load the Instaloader client and login if credentials provided."""
        if self._loader is None:
            self._loader = Instaloader(
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                quiet=True,
            )

            # Login if credentials are provided
            if self.username and self.password and not self._logged_in:
                try:
                    logger.info(f"Logging in to Instagram as {self.username}...")
                    self._loader.login(self.username, self.password)
                    self._logged_in = True
                    logger.info("Successfully logged in to Instagram")
                except Exception as e:
                    logger.error(f"Failed to login to Instagram: {e}")
                    logger.warning("Continuing without login - some features may not work")

        return self._loader

    def get_recent(self, max_results: int = 10) -> list[ContentItem]:
        """Get recent posts from configured Instagram hashtags.

        Fetches recent posts from hashtags in settings.instagram_hashtags,
        deduplicates by shortcode, and returns up to max_results items.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of ContentItem objects, ordered by publish date (most recent first)
        """
        try:
            all_posts = {}  # Use dict to deduplicate by shortcode

            # Calculate results per hashtag to fetch enough before deduplication
            results_per_hashtag = max(5, max_results // len(settings.instagram_hashtags) + 2)

            for hashtag_name in settings.instagram_hashtags:
                try:
                    hashtag = Hashtag.from_name(self.loader.context, hashtag_name)

                    # Fetch recent posts
                    count = 0
                    for post in hashtag.get_posts():
                        if post.shortcode not in all_posts:
                            all_posts[post.shortcode] = post
                            count += 1

                        # Stop after fetching enough from this hashtag
                        if count >= results_per_hashtag:
                            break

                    # Stop early if we have enough unique posts
                    if len(all_posts) >= max_results:
                        break

                    # Rate limiting between hashtag fetches
                    if hashtag_name != settings.instagram_hashtags[-1]:
                        time.sleep(1)

                except QueryReturnedNotFoundException:
                    logger.warning(f"Hashtag not found: #{hashtag_name}")
                    continue
                except ConnectionException as e:
                    logger.error(f"Connection error fetching hashtag #{hashtag_name}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Error fetching hashtag #{hashtag_name}: {e}")
                    continue

            if not all_posts:
                logger.warning("No recent posts found across all hashtags")
                return []

            # Limit to max_results
            posts_list = list(all_posts.values())[:max_results]

            # Map to ContentItem objects
            content_items = []
            for post in posts_list:
                try:
                    content_item = self._post_to_content_item(post)
                    content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping post {post.shortcode}: {e}")
                    continue

            # Sort by published date (most recent first)
            content_items.sort(
                key=lambda x: x.published_at if x.published_at else datetime.min,
                reverse=True
            )

            logger.info(f"Retrieved {len(content_items)} recent posts from {len(settings.instagram_hashtags)} hashtags")
            return content_items

        except Exception as e:
            logger.error(f"Unexpected error in get_recent: {e}")
            return []

    def search(
        self,
        query: str,
        max_results: int = 10,
        **kwargs
    ) -> list[ContentItem]:
        """Search for Instagram posts by fetching from hashtags and filtering by caption.

        Note: Instagram doesn't have a direct search API. This implementation fetches
        posts from configured hashtags and filters them by caption matching.

        Args:
            query: Search terms to match in post captions
            max_results: Maximum number of results to return
            **kwargs: Additional parameters (ignored)

        Returns:
            List of ContentItem objects matching the search query
        """
        try:
            matching_posts = {}  # Deduplicate by shortcode

            # Fetch more posts than needed to account for filtering
            fetch_multiplier = settings.prefetch_multiplier
            posts_to_fetch = max_results * fetch_multiplier

            for hashtag_name in settings.instagram_hashtags:
                try:
                    hashtag = Hashtag.from_name(self.loader.context, hashtag_name)

                    count = 0
                    for post in hashtag.get_posts():
                        # Check if caption matches query
                        if self._caption_matches(post.caption, query):
                            if post.shortcode not in matching_posts:
                                matching_posts[post.shortcode] = post

                        count += 1

                        # Stop after checking enough posts
                        if count >= posts_to_fetch:
                            break

                    # Stop early if we have enough matching posts
                    if len(matching_posts) >= max_results:
                        break

                    # Rate limiting between hashtag fetches
                    if hashtag_name != settings.instagram_hashtags[-1]:
                        time.sleep(1)

                except QueryReturnedNotFoundException:
                    logger.warning(f"Hashtag not found: #{hashtag_name}")
                    continue
                except ConnectionException as e:
                    logger.error(f"Connection error searching hashtag #{hashtag_name}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Error searching hashtag #{hashtag_name}: {e}")
                    continue

            if not matching_posts:
                logger.info(f"No posts found matching query: {query}")
                return []

            # Limit to max_results
            posts_list = list(matching_posts.values())[:max_results]

            # Map to ContentItem objects
            content_items = []
            for post in posts_list:
                try:
                    content_item = self._post_to_content_item(post)
                    content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping post {post.shortcode}: {e}")
                    continue

            logger.info(f"Found {len(content_items)} posts matching query: {query}")
            return content_items

        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []

    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Fetch a specific Instagram post by its shortcode.

        Args:
            content_id: Instagram post shortcode (e.g., "ABC123xyz")

        Returns:
            ContentItem if found, None otherwise
        """
        try:
            post = Post.from_shortcode(self.loader.context, content_id)
            return self._post_to_content_item(post)

        except QueryReturnedNotFoundException:
            logger.warning(f"Post not found with shortcode: {content_id}")
            return None
        except ConnectionException as e:
            logger.error(f"Connection error fetching post {content_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching post {content_id}: {e}")
            return None

    def from_url(self, url: str) -> Optional[ContentItem]:
        """Extract shortcode from Instagram URL and fetch the post.

        Args:
            url: Instagram post URL (e.g., "https://www.instagram.com/p/ABC123xyz/")

        Returns:
            ContentItem if found, None otherwise
        """
        try:
            # Extract shortcode from URL using regex
            # Matches patterns like: instagram.com/p/SHORTCODE/ or instagram.com/reel/SHORTCODE/
            match = re.search(r'instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)', url)
            if not match:
                logger.warning(f"Could not extract shortcode from URL: {url}")
                return None

            shortcode = match.group(1)
            return self.get_by_id(shortcode)

        except Exception as e:
            logger.error(f"Error extracting shortcode from URL {url}: {e}")
            return None

    def _post_to_content_item(self, post: Post) -> ContentItem:
        """Map an Instaloader Post to a ContentItem.

        Args:
            post: Instaloader Post object

        Returns:
            ContentItem object
        """
        # Determine content type
        if post.is_video:
            content_type = ContentType.VIDEO
        elif post.typename == 'GraphSidecar':
            # Carousel posts could contain multiple images/videos
            content_type = ContentType.POST
        else:
            content_type = ContentType.IMAGE

        # Get the appropriate URL (video URL for videos, otherwise image URL)
        media_url = post.video_url if post.is_video else post.url

        # Build source_metadata with Instagram-specific fields
        source_metadata = {
            'shortcode': post.shortcode,
            'typename': post.typename,
            'is_video': post.is_video,
            'mediacount': getattr(post, 'mediacount', 1),
            'caption_hashtags': getattr(post, 'caption_hashtags', []),
            'caption_mentions': getattr(post, 'caption_mentions', []),
        }

        # Add location if available
        if hasattr(post, 'location') and post.location:
            source_metadata['location'] = post.location.name

        # Add video duration if available
        if post.is_video and hasattr(post, 'video_duration'):
            source_metadata['video_duration'] = post.video_duration

        return ContentItem(
            id=post.shortcode,
            source=ContentSource.INSTAGRAM,
            content_type=content_type,
            title=f"Post by @{post.owner_username}",
            url=f"https://www.instagram.com/p/{post.shortcode}/",
            description=post.caption,
            author=post.owner_username,
            published_at=post.date_utc if hasattr(post, 'date_utc') else None,
            thumbnail_url=post.url,  # Use the image URL as thumbnail
            view_count=getattr(post, 'video_view_count', None) if post.is_video else None,
            like_count=post.likes if hasattr(post, 'likes') else None,
            comment_count=post.comments if hasattr(post, 'comments') else None,
            source_metadata=source_metadata,
        )

    def _caption_matches(self, caption: Optional[str], query: str) -> bool:
        """Check if a caption matches the search query.

        Performs case-insensitive word matching - all query words must appear in caption.

        Args:
            caption: Post caption text (may be None)
            query: Search query string

        Returns:
            True if all query words are found in caption, False otherwise
        """
        if not caption:
            return False

        # Convert both to lowercase for case-insensitive matching
        caption_lower = caption.lower()
        query_lower = query.lower()

        # Split query into words
        query_words = query_lower.split()

        # Check if all query words are present in caption
        return all(word in caption_lower for word in query_words)

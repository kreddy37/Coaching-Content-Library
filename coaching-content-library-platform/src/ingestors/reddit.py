"""Reddit content ingestor."""
import logging
import re
from typing import Optional
from datetime import datetime
import praw
from prawcore.exceptions import NotFound, Forbidden

from ..models.content import ContentItem, ContentSource, ContentType
from ..config import settings
from .base import BaseIngestor

logger = logging.getLogger(__name__)


class RedditIngestor(BaseIngestor):
    """Ingestor for Reddit posts using PRAW."""

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """Initialize Reddit ingestor.

        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self._reddit = None

    @property
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        return ContentSource.REDDIT

    @property
    def reddit(self):
        """Lazy-load the Reddit API client."""
        if self._reddit is None:
            self._reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )
        return self._reddit

    def search(
        self,
        query: str,
        max_results: int = 10,
        subreddits: Optional[list[str]] = None,
        sort: str = "relevance",
        time_filter: str = "all",
        **kwargs
    ) -> list[ContentItem]:
        """Search for Reddit posts matching the query.

        Args:
            query: Search terms (e.g., "goalie drills")
            max_results: Maximum number of results to return
            subreddits: Optional list of subreddit names to search within
            sort: Sort order - "relevance", "hot", "new", "top" (default: "relevance")
            time_filter: Time filter - "all", "day", "week", "month", "year" (default: "all")
            **kwargs: Additional Reddit-specific parameters

        Returns:
            List of ContentItem objects
        """
        try:
            # Determine which subreddit(s) to search
            if subreddits:
                # Join multiple subreddits with '+'
                subreddit_str = '+'.join(subreddits)
            else:
                subreddit_str = "all"

            subreddit = self.reddit.subreddit(subreddit_str)

            # Perform the search
            search_results = subreddit.search(
                query=query,
                sort=sort,
                time_filter=time_filter,
                limit=max_results,
                **kwargs
            )

            # Map results to ContentItem objects
            content_items = []
            for submission in search_results:
                try:
                    content_item = self._map_to_content_item(submission)
                    if content_item:  # Only add if not deleted/removed
                        content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping submission {submission.id}: {e}")
                    continue

            return content_items

        except Exception as e:
            logger.error(f"Reddit API error during search: {e}")
            return []

    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Fetch a specific Reddit post by its submission ID.

        Args:
            content_id: Reddit submission ID (e.g., "abc123")

        Returns:
            ContentItem if found and accessible, None otherwise
        """
        try:
            submission = self.reddit.submission(id=content_id)
            # Access an attribute to trigger the fetch
            _ = submission.title
            return self._map_to_content_item(submission)

        except NotFound:
            logger.warning(f"Submission not found with ID: {content_id}")
            return None
        except Forbidden:
            logger.warning(f"Access forbidden to submission: {content_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching submission {content_id}: {e}")
            return None

    def from_url(self, url: str) -> Optional[ContentItem]:
        """Fetch a Reddit post from its URL.

        Args:
            url: Reddit post URL

        Returns:
            ContentItem if found, None otherwise
        """
        submission_id = self._extract_submission_id(url)
        if not submission_id:
            logger.warning(f"Could not extract submission ID from URL: {url}")
            return None

        return self.get_by_id(submission_id)

    def _extract_submission_id(self, url: str) -> Optional[str]:
        """Extract submission ID from Reddit URL.

        Supports format:
        - https://www.reddit.com/r/SUBREDDIT/comments/SUBMISSION_ID/...

        Args:
            url: Reddit URL

        Returns:
            Submission ID if found, None otherwise
        """
        # Reddit URL pattern: reddit.com/r/subreddit/comments/ID/...
        match = re.search(r'reddit\.com/r/\w+/comments/([A-Za-z0-9]+)', url)
        if match:
            return match.group(1)

        return None

    def get_recent(self, max_results: int = 10, sort: str = "hot") -> list[ContentItem]:
        """Get recent posts from configured subreddits.

        Fetches hot or new posts from subreddits in settings.reddit_subreddits.

        Args:
            max_results: Maximum number of results to return
            sort: Sorting method - "hot" (default) or "new"

        Returns:
            List of ContentItem objects
        """
        try:
            # Join configured subreddits with '+'
            if not settings.reddit_subreddits:
                logger.warning("No subreddits configured in settings.reddit_subreddits")
                return []

            subreddit_str = '+'.join(settings.reddit_subreddits)
            subreddit = self.reddit.subreddit(subreddit_str)

            # Fetch posts based on sort method
            if sort == "new":
                submissions = subreddit.new(limit=max_results)
            else:  # Default to "hot"
                submissions = subreddit.hot(limit=max_results)

            # Map submissions to ContentItem objects
            content_items = []
            for submission in submissions:
                try:
                    content_item = self._map_to_content_item(submission)
                    if content_item:  # Only add if not deleted/removed
                        content_items.append(content_item)
                except Exception as e:
                    logger.error(f"Error mapping submission {submission.id}: {e}")
                    continue

            logger.info(f"Retrieved {len(content_items)} {sort} posts from {len(settings.reddit_subreddits)} subreddits")
            return content_items

        except Exception as e:
            logger.error(f"Reddit API error in get_recent: {e}")
            return []

    def _map_to_content_item(self, submission) -> Optional[ContentItem]:
        """Map a Reddit submission to a ContentItem.

        Args:
            submission: PRAW Submission object

        Returns:
            ContentItem object, or None if the post is deleted/removed
        """
        # Check if post is deleted or removed
        if submission.removed_by_category is not None or submission.author is None:
            logger.debug(f"Skipping deleted/removed submission: {submission.id}")
            return None

        # Determine content type based on URL
        content_type = self._determine_content_type(submission)

        # Parse published date
        published_at = None
        if hasattr(submission, 'created_utc'):
            published_at = datetime.fromtimestamp(submission.created_utc)

        # Get description - use selftext for text posts, otherwise use title
        description = None
        if submission.is_self and submission.selftext:
            description = submission.selftext
        elif hasattr(submission, 'selftext') and submission.selftext:
            description = submission.selftext

        # Get thumbnail URL
        thumbnail_url = None
        if hasattr(submission, 'thumbnail') and submission.thumbnail not in ['self', 'default', 'nsfw', 'spoiler']:
            thumbnail_url = submission.thumbnail
        elif hasattr(submission, 'preview') and submission.preview:
            # Try to get better quality thumbnail from preview
            try:
                images = submission.preview.get('images', [])
                if images:
                    thumbnail_url = images[0]['source']['url']
            except (KeyError, IndexError, AttributeError):
                pass

        # Build source_metadata with Reddit-specific fields
        source_metadata = {
            'subreddit': str(submission.subreddit),
            'upvote_ratio': getattr(submission, 'upvote_ratio', None),
            'flair': submission.link_flair_text,
            'is_video': getattr(submission, 'is_video', False),
            'is_self': submission.is_self,
            'permalink': f"https://reddit.com{submission.permalink}",
        }

        return ContentItem(
            id=submission.id,
            source=ContentSource.REDDIT,
            content_type=content_type,
            title=submission.title,
            url=submission.url,
            description=description,
            author=str(submission.author) if submission.author else None,
            published_at=published_at,
            thumbnail_url=thumbnail_url,
            view_count=None,  # Reddit doesn't provide view counts via API
            like_count=submission.score,
            comment_count=submission.num_comments,
            source_metadata=source_metadata,
        )

    def _determine_content_type(self, submission) -> ContentType:
        """Determine the content type based on the submission URL and properties.

        Args:
            submission: PRAW Submission object

        Returns:
            ContentType enum value
        """
        url = submission.url.lower()

        # Check if it's a video
        if getattr(submission, 'is_video', False):
            return ContentType.VIDEO

        # Check for YouTube links
        if 'youtube.com' in url or 'youtu.be' in url:
            return ContentType.VIDEO

        # Check for Reddit video
        if 'v.redd.it' in url:
            return ContentType.VIDEO

        # Check for image domains
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
        image_domains = ('i.redd.it', 'i.imgur.com', 'imgur.com')

        if any(domain in url for domain in image_domains) or url.endswith(image_extensions):
            return ContentType.IMAGE

        # Default to POST for self posts and other content
        return ContentType.POST

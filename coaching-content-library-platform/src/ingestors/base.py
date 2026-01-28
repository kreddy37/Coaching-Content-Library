from abc import ABC, abstractmethod
from typing import Optional
from ..models.content import ContentItem, ContentSource

class BaseIngestor(ABC):
    """
    Abstract base class for all content ingestors.
    
    Each ingestor is responsible for:
    1. Authenticating with its source API
    2. Searching for content based on a query
    3. Transforming source-specific data into ContentItem
    """
    
    @property
    @abstractmethod
    def source(self) -> ContentSource:
        """Return the ContentSource enum for this ingestor."""
        pass
    
    @abstractmethod
    def search(
        self, 
        query: str, 
        max_results: int = 10,
        **kwargs
    ) -> list[ContentItem]:
        """
        Search for content matching the query.
        
        Args:
            query: Search terms (e.g., "butterfly drill goalie")
            max_results: Maximum number of results to return
            **kwargs: Source-specific parameters (e.g., subreddit, date range)
        
        Returns:
            List of ContentItem objects
        """
        pass
    
    @abstractmethod
    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        """
        Fetch a specific piece of content by its source ID.
        Useful for refreshing saved content.
        """
        pass
    
    @abstractmethod
    def get_recent(
        self, 
        max_results: int = 10,
        **kwargs
    ) -> list[ContentItem]:
        """
        Get recent content for discover mode (no keyword filtering).
        - YouTube: Recent videos from discover search terms
        - Reddit: Hot/new posts from configured subreddits
        - Instagram/TikTok: Recent posts from configured hashtags
        """
        pass
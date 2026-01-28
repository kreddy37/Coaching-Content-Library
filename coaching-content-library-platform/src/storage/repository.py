from abc import ABC, abstractmethod
from typing import Optional
from ..models.content import ContentItem, ContentSource

class ContentRepository(ABC):
    """
    Abstract repository for content persistence.
    Implementations: SQLiteRepository (now), PostgresRepository (later)
    """
    
    @abstractmethod
    def save(self, item: ContentItem) -> None:
        """Save or update a content item."""
        pass
    
    @abstractmethod
    def get_by_id(self, source: ContentSource, content_id: str) -> Optional[ContentItem]:
        """Retrieve a saved content item."""
        pass
    
    @abstractmethod
    def search_saved(
        self, 
        query: Optional[str] = None,
        source: Optional[ContentSource] = None,
        tags: Optional[list[str]] = None,
        collection_id: Optional[str] = None
    ) -> list[ContentItem]:
        """Search through saved content with filters."""
        pass
    
    @abstractmethod
    def delete(self, source: ContentSource, content_id: str) -> bool:
        """Delete a saved content item. Returns True if found and deleted."""
        pass
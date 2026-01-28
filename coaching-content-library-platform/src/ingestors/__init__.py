"""Content ingestors for various platforms."""
from .base import BaseIngestor
from .youtube import YouTubeIngestor
from .reddit import RedditIngestor
from .instagram import InstagramIngestor

__all__ = ["BaseIngestor", "YouTubeIngestor", "RedditIngestor", "InstagramIngestor"]

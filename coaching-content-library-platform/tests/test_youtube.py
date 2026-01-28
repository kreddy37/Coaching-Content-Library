"""Tests for YouTube ingestor."""
import pytest
from src.ingestors.youtube import YouTubeIngestor


def test_youtube_ingestor_initialization():
    """Test that YouTubeIngestor can be initialized."""
    ingestor = YouTubeIngestor(api_key="test_key")
    assert ingestor.api_key == "test_key"


def test_youtube_fetch_content():
    """Test fetching content from YouTube."""
    ingestor = YouTubeIngestor(api_key="test_key")
    results = ingestor.search("goalie drills", max_results=5)
    assert isinstance(results, list)

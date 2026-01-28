"""Tests for Reddit ingestor."""
import pytest
from src.ingestors.reddit import RedditIngestor


def test_reddit_ingestor_initialization():
    """Test that RedditIngestor can be initialized."""
    ingestor = RedditIngestor(
        client_id="test_id",
        client_secret="test_secret",
        user_agent="test_agent"
    )
    assert ingestor.client_id == "test_id"
    assert ingestor.client_secret == "test_secret"
    assert ingestor.user_agent == "test_agent"


def test_reddit_fetch_content():
    """Test fetching content from Reddit."""
    ingestor = RedditIngestor(
        client_id="test_id",
        client_secret="test_secret",
        user_agent="test_agent"
    )
    results = ingestor.fetch_content("hockeygoalies", max_results=5)
    assert isinstance(results, list)

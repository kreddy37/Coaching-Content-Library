"""Tests for TikTok oEmbed ingestor."""
import pytest
from unittest.mock import patch, Mock
import httpx

from src.ingestors.tiktok import TikTokIngestor
from src.models.content import ContentSource, ContentType


class TestTikTokIngestor:
    """Test TikTok oEmbed ingestor."""

    @pytest.fixture
    def ingestor(self):
        """Create TikTok ingestor instance."""
        return TikTokIngestor()

    def test_source_property(self, ingestor):
        """Test that source property returns TIKTOK."""
        assert ingestor.source == ContentSource.TIKTOK

    def test_search_raises_not_implemented(self, ingestor):
        """Test that search() raises NotImplementedError."""
        with pytest.raises(NotImplementedError) as exc_info:
            ingestor.search("goalie drills")

        assert "use from_url" in str(exc_info.value).lower()

    def test_get_recent_raises_not_implemented(self, ingestor):
        """Test that get_recent() raises NotImplementedError."""
        with pytest.raises(NotImplementedError) as exc_info:
            ingestor.get_recent()

        assert "use from_url" in str(exc_info.value).lower()

    def test_extract_video_id_from_standard_url(self, ingestor):
        """Test extracting video ID from standard URL."""
        url = "https://www.tiktok.com/@username/video/1234567890"
        video_id = ingestor._extract_video_id(url)
        assert video_id == "1234567890"

    def test_extract_video_id_without_www(self, ingestor):
        """Test extracting video ID from URL without www."""
        url = "https://tiktok.com/@user/video/9876543210"
        video_id = ingestor._extract_video_id(url)
        assert video_id == "9876543210"

    def test_extract_video_id_from_short_url(self, ingestor):
        """Test extracting video ID from short URL."""
        url = "https://vm.tiktok.com/ZMabcdef123/"
        video_id = ingestor._extract_video_id(url)
        assert video_id == "ZMabcdef123"

    def test_extract_video_id_from_short_url_without_trailing_slash(self, ingestor):
        """Test extracting video ID from short URL without trailing slash."""
        url = "https://vm.tiktok.com/ABC123xyz"
        video_id = ingestor._extract_video_id(url)
        assert video_id == "ABC123xyz"

    def test_extract_video_id_invalid_url(self, ingestor):
        """Test extracting video ID from invalid URL returns None."""
        url = "https://example.com/something"
        video_id = ingestor._extract_video_id(url)
        assert video_id is None

    @patch('httpx.get')
    def test_from_url_success(self, mock_get, ingestor):
        """Test successful oEmbed fetch and mapping."""
        # Mock oEmbed response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Amazing goalie drill #goalies #hockey',
            'author_name': 'goaliecoach',
            'author_url': 'https://www.tiktok.com/@goaliecoach',
            'thumbnail_url': 'https://tiktok.com/thumbnail.jpg',
            'provider_name': 'TikTok',
            'html': '<blockquote>...</blockquote>',
            'author_unique_id': 'goaliecoach123'
        }
        mock_get.return_value = mock_response

        url = "https://www.tiktok.com/@goaliecoach/video/1234567890"
        result = ingestor.from_url(url)

        assert result is not None
        assert result.id == "1234567890"
        assert result.source == ContentSource.TIKTOK
        assert result.content_type == ContentType.VIDEO
        assert result.title == 'Amazing goalie drill #goalies #hockey'
        assert result.description == 'Amazing goalie drill #goalies #hockey'
        assert result.author == 'goaliecoach'
        assert result.thumbnail_url == 'https://tiktok.com/thumbnail.jpg'
        assert result.url == url
        assert result.source_metadata['provider_name'] == 'TikTok'
        assert result.source_metadata['author_url'] == 'https://www.tiktok.com/@goaliecoach'
        assert result.source_metadata['html'] == '<blockquote>...</blockquote>'
        assert result.source_metadata['author_unique_id'] == 'goaliecoach123'

    @patch('httpx.get')
    def test_from_url_truncates_long_title(self, mock_get, ingestor):
        """Test that long titles are truncated to 100 chars."""
        long_title = "A" * 150  # 150 character title

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': long_title,
            'author_name': 'user'
        }
        mock_get.return_value = mock_response

        url = "https://www.tiktok.com/@user/video/123456"
        result = ingestor.from_url(url)

        assert result is not None
        assert len(result.title) == 100  # Truncated
        assert result.description == long_title  # Full title in description

    @patch('httpx.get')
    def test_from_url_short_url(self, mock_get, ingestor):
        """Test successful fetch from short URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test TikTok',
            'author_name': 'user'
        }
        mock_get.return_value = mock_response

        url = "https://vm.tiktok.com/ZMabcdef/"
        result = ingestor.from_url(url)

        assert result is not None
        assert result.id == "ZMabcdef"
        assert result.content_type == ContentType.VIDEO

    @patch('httpx.get')
    def test_from_url_all_content_is_video(self, mock_get, ingestor):
        """Test that all TikTok content is classified as VIDEO."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test Video',
            'author_name': 'user'
        }
        mock_get.return_value = mock_response

        url = "https://www.tiktok.com/@user/video/123"
        result = ingestor.from_url(url)

        assert result is not None
        assert result.content_type == ContentType.VIDEO

    @patch('httpx.get')
    def test_from_url_404_returns_none(self, mock_get, ingestor):
        """Test that 404 response returns None."""
        mock_get.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=Mock(),
            response=Mock(status_code=404)
        )

        url = "https://www.tiktok.com/@user/video/NOTFOUND"
        result = ingestor.from_url(url)

        assert result is None

    @patch('httpx.get')
    def test_from_url_timeout_returns_none(self, mock_get, ingestor):
        """Test that timeout returns None."""
        mock_get.side_effect = httpx.TimeoutException("Request timed out")

        url = "https://www.tiktok.com/@user/video/TIMEOUT"
        result = ingestor.from_url(url)

        assert result is None

    @patch('httpx.get')
    def test_from_url_request_error_returns_none(self, mock_get, ingestor):
        """Test that request error returns None."""
        mock_get.side_effect = httpx.RequestError("Connection failed")

        url = "https://www.tiktok.com/@user/video/ERROR"
        result = ingestor.from_url(url)

        assert result is None

    def test_from_url_invalid_url_returns_none(self, ingestor):
        """Test that invalid URL returns None (no video ID)."""
        url = "https://example.com/nottiktok"
        result = ingestor.from_url(url)

        assert result is None

    def test_get_by_id_returns_none(self, ingestor):
        """Test that get_by_id returns None with warning."""
        # TikTok requires username in URL, so get_by_id cannot work
        result = ingestor.get_by_id("1234567890")

        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

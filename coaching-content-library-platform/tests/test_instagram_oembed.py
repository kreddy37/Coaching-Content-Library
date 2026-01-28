"""Tests for Instagram oEmbed ingestor."""
import pytest
from unittest.mock import patch, Mock
import httpx

from src.ingestors.instagram import InstagramIngestor
from src.models.content import ContentSource, ContentType


class TestInstagramIngestor:
    """Test Instagram oEmbed ingestor."""

    @pytest.fixture
    def ingestor(self):
        """Create Instagram ingestor instance."""
        return InstagramIngestor()

    def test_source_property(self, ingestor):
        """Test that source property returns INSTAGRAM."""
        assert ingestor.source == ContentSource.INSTAGRAM

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

    def test_extract_shortcode_from_post_url(self, ingestor):
        """Test extracting shortcode from /p/ URL."""
        url = "https://www.instagram.com/p/ABC123xyz/"
        shortcode = ingestor._extract_shortcode(url)
        assert shortcode == "ABC123xyz"

    def test_extract_shortcode_from_reel_url(self, ingestor):
        """Test extracting shortcode from /reel/ URL."""
        url = "https://www.instagram.com/reel/XYZ789abc/"
        shortcode = ingestor._extract_shortcode(url)
        assert shortcode == "XYZ789abc"

    def test_extract_shortcode_without_www(self, ingestor):
        """Test extracting shortcode from URL without www."""
        url = "https://instagram.com/p/TEST123/"
        shortcode = ingestor._extract_shortcode(url)
        assert shortcode == "TEST123"

    def test_extract_shortcode_invalid_url(self, ingestor):
        """Test extracting shortcode from invalid URL returns None."""
        url = "https://example.com/something"
        shortcode = ingestor._extract_shortcode(url)
        assert shortcode is None

    def test_determine_content_type_post(self, ingestor):
        """Test content type for regular post URL."""
        url = "https://www.instagram.com/p/ABC123/"
        content_type = ingestor._determine_content_type(url)
        assert content_type == ContentType.IMAGE

    def test_determine_content_type_reel(self, ingestor):
        """Test content type for reel URL."""
        url = "https://www.instagram.com/reel/XYZ789/"
        content_type = ingestor._determine_content_type(url)
        assert content_type == ContentType.VIDEO

    @patch('httpx.get')
    def test_from_url_success(self, mock_get, ingestor):
        """Test successful oEmbed fetch and mapping."""
        # Mock oEmbed response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Amazing goalie save drill by @coach',
            'author_name': 'coach',
            'author_url': 'https://www.instagram.com/coach/',
            'thumbnail_url': 'https://instagram.com/image.jpg',
            'provider_name': 'Instagram',
            'html': '<blockquote>...</blockquote>'
        }
        mock_get.return_value = mock_response

        url = "https://www.instagram.com/p/ABC123xyz/"
        result = ingestor.from_url(url)

        assert result is not None
        assert result.id == "ABC123xyz"
        assert result.source == ContentSource.INSTAGRAM
        assert result.content_type == ContentType.IMAGE
        assert result.title == 'Amazing goalie save drill by @coach'
        assert result.description == 'Amazing goalie save drill by @coach'
        assert result.author == 'coach'
        assert result.thumbnail_url == 'https://instagram.com/image.jpg'
        assert result.url == url
        assert result.source_metadata['provider_name'] == 'Instagram'
        assert result.source_metadata['author_url'] == 'https://www.instagram.com/coach/'
        assert result.source_metadata['html'] == '<blockquote>...</blockquote>'

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

        url = "https://www.instagram.com/p/TEST123/"
        result = ingestor.from_url(url)

        assert result is not None
        assert len(result.title) == 100  # Truncated
        assert result.description == long_title  # Full title in description

    @patch('httpx.get')
    def test_from_url_reel_is_video(self, mock_get, ingestor):
        """Test that reel URLs are classified as VIDEO."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test Reel',
            'author_name': 'user'
        }
        mock_get.return_value = mock_response

        url = "https://www.instagram.com/reel/ABC123xyz/"
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

        url = "https://www.instagram.com/p/NOTFOUND/"
        result = ingestor.from_url(url)

        assert result is None

    @patch('httpx.get')
    def test_from_url_timeout_returns_none(self, mock_get, ingestor):
        """Test that timeout returns None."""
        mock_get.side_effect = httpx.TimeoutException("Request timed out")

        url = "https://www.instagram.com/p/TIMEOUT/"
        result = ingestor.from_url(url)

        assert result is None

    @patch('httpx.get')
    def test_from_url_request_error_returns_none(self, mock_get, ingestor):
        """Test that request error returns None."""
        mock_get.side_effect = httpx.RequestError("Connection failed")

        url = "https://www.instagram.com/p/ERROR/"
        result = ingestor.from_url(url)

        assert result is None

    def test_from_url_invalid_url_returns_none(self, ingestor):
        """Test that invalid URL returns None (no shortcode)."""
        url = "https://example.com/notinstagram"
        result = ingestor.from_url(url)

        assert result is None

    @patch('httpx.get')
    def test_get_by_id_constructs_url_and_calls_from_url(self, mock_get, ingestor):
        """Test that get_by_id constructs URL and delegates to from_url."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test Post',
            'author_name': 'user'
        }
        mock_get.return_value = mock_response

        shortcode = "ABC123xyz"
        result = ingestor.get_by_id(shortcode)

        assert result is not None
        assert result.id == shortcode
        # Verify the correct URL was constructed
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert f"url=https://www.instagram.com/p/{shortcode}/" in call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

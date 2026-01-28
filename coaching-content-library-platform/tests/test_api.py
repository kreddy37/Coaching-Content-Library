"""Tests for FastAPI backend."""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from src.api.main import app
from src.models.content import ContentItem, ContentSource, ContentType


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test health check returns 200."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestSaveContent:
    """Test POST /api/v1/content endpoint."""

    @patch('src.api.routes.repository')
    @patch('src.api.routes.ingestors')
    def test_save_content_success(self, mock_ingestors, mock_repo):
        """Test successful content save."""
        # Mock ingestor
        mock_ingestor = Mock()
        mock_content = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Video",
            url="https://youtube.com/watch?v=test123",
            description="Test description",
            author="Test Author",
        )
        mock_ingestor.from_url.return_value = mock_content
        mock_ingestors.get.return_value = mock_ingestor

        # Mock repository
        mock_repo.save.return_value = None

        client = TestClient(app)
        response = client.post(
            "/api/v1/content",
            json={
                "url": "https://youtube.com/watch?v=test123",
                "source": "YouTube"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "test123"
        assert data["source"] == "YouTube"
        assert data["title"] == "Test Video"

        # Verify ingestor and repo were called
        mock_ingestor.from_url.assert_called_once_with("https://youtube.com/watch?v=test123")
        mock_repo.save.assert_called_once()

    @patch('src.api.routes.repository')
    @patch('src.api.routes.ingestors')
    def test_save_content_with_metadata(self, mock_ingestors, mock_repo):
        """Test saving content with metadata overrides."""
        mock_ingestor = Mock()
        mock_content = ContentItem(
            id="test456",
            source=ContentSource.INSTAGRAM,
            content_type=ContentType.IMAGE,
            title="Test Post",
            url="https://instagram.com/p/test456",
        )
        mock_ingestor.from_url.return_value = mock_content
        mock_ingestors.get.return_value = mock_ingestor

        client = TestClient(app)
        response = client.post(
            "/api/v1/content",
            json={
                "url": "https://instagram.com/p/test456",
                "source": "Instagram",
                "drill_tags": ["butterfly", "push"],
                "drill_description": "Practice butterfly push technique",
                "difficulty": "intermediate",
                "equipment": "pucks, cones",
                "age_group": "bantam"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert "butterfly" in data["drill_tags"]
        assert "push" in data["drill_tags"]
        assert data["drill_description"] == "Practice butterfly push technique"
        assert data["difficulty"] == "intermediate"
        assert data["equipment"] == "pucks, cones"
        assert data["age_group"] == "bantam"

    @patch('src.api.routes.ingestors')
    def test_save_content_unsupported_source(self, mock_ingestors):
        """Test error when source is unsupported."""
        mock_ingestors.get.return_value = None

        client = TestClient(app)
        response = client.post(
            "/api/v1/content",
            json={
                "url": "https://example.com/test",
                "source": "YouTube"  # Will be None from mock
            }
        )

        assert response.status_code == 400
        assert "Unsupported content source" in response.json()["detail"]

    @patch('src.api.routes.repository')
    @patch('src.api.routes.ingestors')
    def test_save_content_not_found(self, mock_ingestors, mock_repo):
        """Test error when content cannot be fetched."""
        mock_ingestor = Mock()
        mock_ingestor.from_url.return_value = None  # Content not found
        mock_ingestors.get.return_value = mock_ingestor

        client = TestClient(app)
        response = client.post(
            "/api/v1/content",
            json={
                "url": "https://youtube.com/watch?v=notfound",
                "source": "YouTube"
            }
        )

        assert response.status_code == 404
        assert "Could not fetch content" in response.json()["detail"]


class TestListContent:
    """Test GET /api/v1/content endpoint."""

    @patch('src.api.routes.repository')
    def test_list_content_empty(self, mock_repo):
        """Test listing content when database is empty."""
        mock_repo.search.return_value = []

        client = TestClient(app)
        response = client.get("/api/v1/content")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    @patch('src.api.routes.repository')
    def test_list_content_with_results(self, mock_repo):
        """Test listing content with results."""
        mock_items = [
            ContentItem(
                id="item1",
                source=ContentSource.YOUTUBE,
                content_type=ContentType.VIDEO,
                title="Video 1",
                url="https://youtube.com/1",
            ),
            ContentItem(
                id="item2",
                source=ContentSource.REDDIT,
                content_type=ContentType.POST,
                title="Post 1",
                url="https://reddit.com/1",
            ),
        ]
        mock_repo.search.return_value = mock_items

        client = TestClient(app)
        response = client.get("/api/v1/content")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2
        assert data["items"][0]["id"] == "item1"
        assert data["items"][1]["id"] == "item2"

    @patch('src.api.routes.repository')
    def test_list_content_with_filters(self, mock_repo):
        """Test listing content with filters."""
        mock_repo.search.return_value = []

        client = TestClient(app)
        response = client.get(
            "/api/v1/content",
            params={
                "source": "YouTube",
                "content_type": "Video",
                "difficulty": "intermediate",
                "limit": 20
            }
        )

        assert response.status_code == 200
        # Verify repository was called with correct criteria
        mock_repo.search.assert_called_once()
        call_args = mock_repo.search.call_args
        assert call_args[1]["criteria"]["source"] == ContentSource.YOUTUBE
        assert call_args[1]["criteria"]["content_type"] == ContentType.VIDEO
        assert call_args[1]["criteria"]["difficulty"] == "intermediate"
        assert call_args[1]["limit"] == 20

    @patch('src.api.routes.repository')
    def test_list_content_with_query(self, mock_repo):
        """Test searching content with query."""
        mock_repo.search.return_value = []

        client = TestClient(app)
        response = client.get(
            "/api/v1/content",
            params={"query": "butterfly push"}
        )

        assert response.status_code == 200
        # Verify repository was called with query
        mock_repo.search.assert_called_once()
        call_args = mock_repo.search.call_args
        assert call_args[0][0] == "butterfly push"


class TestGetContent:
    """Test GET /api/v1/content/{id} endpoint."""

    @patch('src.api.routes.repository')
    def test_get_content_success(self, mock_repo):
        """Test getting existing content."""
        mock_item = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Video",
            url="https://youtube.com/test",
        )
        mock_repo.get.return_value = mock_item

        client = TestClient(app)
        response = client.get("/api/v1/content/test123")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test123"
        assert data["title"] == "Test Video"

    @patch('src.api.routes.repository')
    def test_get_content_not_found(self, mock_repo):
        """Test getting non-existent content."""
        mock_repo.get.return_value = None

        client = TestClient(app)
        response = client.get("/api/v1/content/notfound")

        assert response.status_code == 404
        assert "Content not found" in response.json()["detail"]


class TestUpdateMetadata:
    """Test PUT /api/v1/content/{id}/metadata endpoint."""

    @patch('src.api.routes.repository')
    def test_update_metadata_success(self, mock_repo):
        """Test updating metadata."""
        mock_item = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Video",
            url="https://youtube.com/test",
        )
        mock_repo.get.return_value = mock_item
        mock_repo.save.return_value = None

        client = TestClient(app)
        response = client.put(
            "/api/v1/content/test123/metadata",
            json={
                "drill_tags": ["butterfly", "lateral"],
                "drill_description": "Advanced butterfly drill",
                "difficulty": "advanced",
                "equipment": "pucks"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "butterfly" in data["drill_tags"]
        assert "lateral" in data["drill_tags"]
        assert data["drill_description"] == "Advanced butterfly drill"
        assert data["difficulty"] == "advanced"
        assert data["equipment"] == "pucks"

        # Verify save was called
        mock_repo.save.assert_called_once()

    @patch('src.api.routes.repository')
    def test_update_metadata_partial(self, mock_repo):
        """Test updating only some metadata fields."""
        mock_item = ContentItem(
            id="test456",
            source=ContentSource.INSTAGRAM,
            content_type=ContentType.IMAGE,
            title="Test Post",
            url="https://instagram.com/test",
            difficulty="beginner",  # Existing value
        )
        mock_repo.get.return_value = mock_item

        client = TestClient(app)
        response = client.put(
            "/api/v1/content/test456/metadata",
            json={
                "skill_focus": "skating"  # Only update this field
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["skill_focus"] == "skating"
        assert data["difficulty"] == "beginner"  # Unchanged

    @patch('src.api.routes.repository')
    def test_update_metadata_not_found(self, mock_repo):
        """Test updating metadata for non-existent content."""
        mock_repo.get.return_value = None

        client = TestClient(app)
        response = client.put(
            "/api/v1/content/notfound/metadata",
            json={"difficulty": "advanced"}
        )

        assert response.status_code == 404
        assert "Content not found" in response.json()["detail"]


class TestDeleteContent:
    """Test DELETE /api/v1/content/{id} endpoint."""

    @patch('src.api.routes.repository')
    def test_delete_content_success(self, mock_repo):
        """Test deleting existing content."""
        mock_item = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Video",
            url="https://youtube.com/test",
        )
        mock_repo.get.return_value = mock_item
        mock_repo.delete.return_value = None

        client = TestClient(app)
        response = client.delete("/api/v1/content/test123")

        assert response.status_code == 204
        mock_repo.delete.assert_called_once_with(ContentSource.YOUTUBE, "test123")

    @patch('src.api.routes.repository')
    def test_delete_content_not_found(self, mock_repo):
        """Test deleting non-existent content."""
        mock_repo.get.return_value = None

        client = TestClient(app)
        response = client.delete("/api/v1/content/notfound")

        assert response.status_code == 404
        assert "Content not found" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

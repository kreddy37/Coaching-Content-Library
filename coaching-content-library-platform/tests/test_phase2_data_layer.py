"""Tests for Phase 2 data layer changes (ContentItem model + SQLite repository)."""
import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timezone

from src.models.content import ContentItem, ContentSource, ContentType
from src.storage.sqlite import SQLiteRepository


class TestPhase2ContentItem:
    """Test Phase 2 fields on ContentItem model."""

    def test_content_item_with_phase2_fields(self):
        """Test that ContentItem accepts and stores Phase 2 fields."""
        item = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Butterfly Push Drill",
            url="https://youtube.com/watch?v=test123",
            skill_focus="butterfly push, lateral movement",
            difficulty="intermediate",
            equipment="pucks, cones",
            age_group="bantam",
            drill_type="warmup"
        )

        assert item.skill_focus == "butterfly push, lateral movement"
        assert item.difficulty == "intermediate"
        assert item.equipment == "pucks, cones"
        assert item.age_group == "bantam"
        assert item.drill_type == "warmup"

    def test_content_item_phase2_fields_optional(self):
        """Test that Phase 2 fields are optional (default to None)."""
        item = ContentItem(
            id="test123",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Video",
            url="https://youtube.com/watch?v=test123"
        )

        assert item.skill_focus is None
        assert item.difficulty is None
        assert item.equipment is None
        assert item.age_group is None
        assert item.drill_type is None


class TestPhase2SQLiteRepository:
    """Test Phase 2 SQLite repository changes."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        temp_file.close()
        yield temp_file.name
        Path(temp_file.name).unlink()

    def test_save_and_retrieve_with_phase2_fields(self, temp_db):
        """Test saving and retrieving content with Phase 2 fields."""
        repo = SQLiteRepository(temp_db)

        # Create item with Phase 2 fields
        item = ContentItem(
            id="drill001",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Glove Save Drill",
            url="https://youtube.com/watch?v=drill001",
            skill_focus="glove positioning, quick recovery",
            difficulty="advanced",
            equipment="pucks",
            age_group="16-18",
            drill_type="main",
            tags=["glove", "recovery"],
            notes="Focus on hand speed"
        )

        # Save item
        repo.save(item)

        # Retrieve item
        retrieved = repo.get_by_id(ContentSource.YOUTUBE, "drill001")

        assert retrieved is not None
        assert retrieved.skill_focus == "glove positioning, quick recovery"
        assert retrieved.difficulty == "advanced"
        assert retrieved.equipment == "pucks"
        assert retrieved.age_group == "16-18"
        assert retrieved.drill_type == "main"
        assert retrieved.notes == "Focus on hand speed"
        assert retrieved.tags == ["glove", "recovery"]

    def test_save_without_phase2_fields(self, temp_db):
        """Test saving content without Phase 2 fields (None values)."""
        repo = SQLiteRepository(temp_db)

        item = ContentItem(
            id="drill002",
            source=ContentSource.REDDIT,
            content_type=ContentType.POST,
            title="Interesting drill discussion",
            url="https://reddit.com/r/hockeygoalies/drill002"
        )

        # Save item
        repo.save(item)

        # Retrieve item
        retrieved = repo.get_by_id(ContentSource.REDDIT, "drill002")

        assert retrieved is not None
        assert retrieved.skill_focus is None
        assert retrieved.difficulty is None
        assert retrieved.equipment is None
        assert retrieved.age_group is None
        assert retrieved.drill_type is None

    def test_migration_from_phase1_schema(self, temp_db):
        """Test that migration adds Phase 2 columns to existing Phase 1 database."""
        # Create a Phase 1 schema manually (without Phase 2 fields)
        with sqlite3.connect(temp_db) as conn:
            conn.execute("""
                CREATE TABLE content (
                    source TEXT NOT NULL,
                    id TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT,
                    author TEXT,
                    published_at TEXT,
                    fetched_at TEXT NOT NULL,
                    thumbnail_url TEXT,
                    view_count INTEGER,
                    like_count INTEGER,
                    comment_count INTEGER,
                    source_metadata TEXT,
                    tags TEXT,
                    notes TEXT,
                    saved_at TEXT,
                    collection_id TEXT,
                    PRIMARY KEY (source, id)
                )
            """)

            # Insert Phase 1 data
            conn.execute("""
                INSERT INTO content (
                    source, id, content_type, title, url, fetched_at,
                    source_metadata, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "YouTube",
                "old_video",
                "Video",
                "Old Phase 1 Video",
                "https://youtube.com/watch?v=old",
                datetime.now(timezone.utc).isoformat(),
                "{}",
                "[]"
            ))
            conn.commit()

        # Now initialize the repository - should trigger migration
        repo = SQLiteRepository(temp_db)

        # Verify columns were added
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.execute("PRAGMA table_info(content)")
            columns = {row[1] for row in cursor.fetchall()}

            assert 'skill_focus' in columns
            assert 'difficulty' in columns
            assert 'equipment' in columns
            assert 'age_group' in columns
            assert 'drill_type' in columns

        # Verify old data still retrievable
        old_item = repo.get_by_id(ContentSource.YOUTUBE, "old_video")
        assert old_item is not None
        assert old_item.title == "Old Phase 1 Video"
        assert old_item.skill_focus is None  # New fields should be None for old data

        # Verify we can save new data with Phase 2 fields
        new_item = ContentItem(
            id="new_video",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="New Phase 2 Video",
            url="https://youtube.com/watch?v=new",
            skill_focus="butterfly",
            difficulty="beginner"
        )
        repo.save(new_item)

        retrieved_new = repo.get_by_id(ContentSource.YOUTUBE, "new_video")
        assert retrieved_new.skill_focus == "butterfly"
        assert retrieved_new.difficulty == "beginner"

    def test_update_existing_item_with_phase2_fields(self, temp_db):
        """Test updating an existing item to add Phase 2 metadata."""
        repo = SQLiteRepository(temp_db)

        # Save initial item without Phase 2 fields
        item = ContentItem(
            id="drill003",
            source=ContentSource.YOUTUBE,
            content_type=ContentType.VIDEO,
            title="Test Drill",
            url="https://youtube.com/watch?v=drill003"
        )
        repo.save(item)

        # Update with Phase 2 fields
        item.skill_focus = "skating, edges"
        item.difficulty = "intermediate"
        item.equipment = "cones"
        repo.save(item)

        # Retrieve and verify
        retrieved = repo.get_by_id(ContentSource.YOUTUBE, "drill003")
        assert retrieved.skill_focus == "skating, edges"
        assert retrieved.difficulty == "intermediate"
        assert retrieved.equipment == "cones"

    def test_search_results_include_phase2_fields(self, temp_db):
        """Test that search results include Phase 2 fields."""
        repo = SQLiteRepository(temp_db)

        # Save items with Phase 2 data
        for i in range(3):
            item = ContentItem(
                id=f"drill{i}",
                source=ContentSource.YOUTUBE,
                content_type=ContentType.VIDEO,
                title=f"Drill {i}",
                url=f"https://youtube.com/watch?v=drill{i}",
                difficulty=["beginner", "intermediate", "advanced"][i],
                skill_focus="test skill"
            )
            repo.save(item)

        # Search and verify Phase 2 fields present
        results = repo.search_saved()
        assert len(results) == 3

        for result in results:
            assert result.difficulty in ["beginner", "intermediate", "advanced"]
            assert result.skill_focus == "test skill"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

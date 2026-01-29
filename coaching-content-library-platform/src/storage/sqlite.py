"""SQLite implementation of ContentRepository."""
import sqlite3
import json
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from ..models.content import ContentItem, ContentSource, ContentType, Difficulty
from .repository import ContentRepository

logger = logging.getLogger(__name__)


class SQLiteRepository(ContentRepository):
    """SQLite-based content repository."""

    def __init__(self, db_path: str = "data/content.db"):
        """Initialize SQLite repository.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_db()
        self._ensure_schema()  # Run migrations for Phase 2 fields

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS content (
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
            conn.commit()

    def _ensure_schema(self):
        """Ensure database schema includes all Phase 2 fields.

        Adds missing columns to existing databases (migration).
        """
        with sqlite3.connect(self.db_path) as conn:
            # Check existing columns
            cursor = conn.execute("PRAGMA table_info(content)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Define Phase 2 columns
            phase2_columns = {
                'drill_tags': 'TEXT',  # JSON array of tags
                'drill_description': 'TEXT',  # Custom drill description
                'difficulty': 'TEXT',
                'equipment': 'TEXT',
                'age_group': 'TEXT',
                # Legacy columns (deprecated but kept for backward compatibility):
                'skill_focus': 'TEXT',
                'drill_type': 'TEXT'
            }

            # Add missing columns
            for col_name, col_type in phase2_columns.items():
                if col_name not in existing_columns:
                    logger.info(f"Adding column '{col_name}' to content table")
                    conn.execute(f"ALTER TABLE content ADD COLUMN {col_name} {col_type}")

            conn.commit()

    def save(self, item: ContentItem) -> None:
        """Save or update a content item.

        Args:
            item: ContentItem to save
        """
        # Set saved_at if not already set
        if item.saved_at is None:
            item.saved_at = datetime.now(timezone.utc)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO content (
                    source, id, content_type, title, url, description, author,
                    published_at, fetched_at, thumbnail_url, view_count,
                    like_count, comment_count, source_metadata, tags, notes,
                    saved_at, collection_id, drill_tags, drill_description, difficulty,
                    equipment, age_group
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.source.value,
                item.id,
                item.content_type.value,
                item.title,
                item.url,
                item.description,
                item.author,
                item.published_at.isoformat() if item.published_at else None,
                item.fetched_at.isoformat(),
                item.thumbnail_url,
                item.view_count,
                item.like_count,
                item.comment_count,
                json.dumps(item.source_metadata),
                json.dumps(item.tags),
                item.notes,
                item.saved_at.isoformat() if item.saved_at else None,
                item.collection_id,
                json.dumps(item.drill_tags),
                item.drill_description,
                item.difficulty.value if item.difficulty else None,
                item.equipment,
                item.age_group,
            ))
            conn.commit()

    def get_by_id(self, source: ContentSource, content_id: str) -> Optional[ContentItem]:
        """Retrieve a saved content item.

        Args:
            source: ContentSource enum value
            content_id: Source-specific ID

        Returns:
            ContentItem if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM content WHERE source = ? AND id = ?",
                (source.value, content_id)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_content_item(row)

    def search_saved(
        self,
        query: Optional[str] = None,
        source: Optional[ContentSource] = None,
        tags: Optional[list[str]] = None,
        collection_id: Optional[str] = None
    ) -> list[ContentItem]:
        """Search through saved content with filters.

        Args:
            query: Search in title and description (case-insensitive)
            source: Filter by ContentSource
            tags: Filter items containing any of the provided tags
            collection_id: Exact match on collection_id

        Returns:
            List of matching ContentItem objects
        """
        sql = "SELECT * FROM content WHERE 1=1"
        params = []

        # Add query filter (search in title and description)
        if query:
            sql += " AND (title LIKE ? OR description LIKE ?)"
            search_term = f"%{query}%"
            params.extend([search_term, search_term])

        # Add source filter
        if source:
            sql += " AND source = ?"
            params.append(source.value)

        # Add collection_id filter
        if collection_id:
            sql += " AND collection_id = ?"
            params.append(collection_id)

        # Add tags filter
        if tags:
            # Use json_each to search within the tags JSON array
            # We need to find items that have ANY of the provided tags
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("json_each.value = ?")
                params.append(tag)

            tags_sql = " OR ".join(tag_conditions)
            sql += f" AND EXISTS (SELECT 1 FROM json_each(content.tags) WHERE {tags_sql})"

        sql += " ORDER BY saved_at DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()

            return [self._row_to_content_item(row) for row in rows]

    def delete(self, source: ContentSource, content_id: str) -> bool:
        """Delete a saved content item.

        Args:
            source: ContentSource enum value
            content_id: Source-specific ID

        Returns:
            True if found and deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM content WHERE source = ? AND id = ?",
                (source.value, content_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    # Convenience methods for API (Phase 2)

    def get(self, content_id: str) -> Optional[ContentItem]:
        """Get content by ID only (searches across all sources).

        Args:
            content_id: Content ID (just the ID, not including source)

        Returns:
            ContentItem if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM content WHERE id = ? LIMIT 1",
                (content_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_content_item(row)

    def search(
        self,
        query: str = "",
        criteria: Optional[dict] = None,
        limit: int = 10
    ) -> list[ContentItem]:
        """Search content with flexible criteria.

        Args:
            query: Text search in title and description
            criteria: Dict with optional filters (source, content_type, difficulty, skill_focus, etc.)
            limit: Maximum number of results

        Returns:
            List of matching ContentItem objects
        """
        sql = "SELECT * FROM content WHERE 1=1"
        params = []

        # Add text search
        if query:
            sql += " AND (title LIKE ? OR description LIKE ?)"
            search_term = f"%{query}%"
            params.extend([search_term, search_term])

        # Add criteria filters
        if criteria:
            if "source" in criteria:
                sql += " AND source = ?"
                params.append(criteria["source"].value)

            if "content_type" in criteria:
                sql += " AND content_type = ?"
                params.append(criteria["content_type"].value)

            if "difficulty" in criteria:
                # Case-insensitive comparison to handle legacy lowercase data
                sql += " AND LOWER(difficulty) = LOWER(?)"
                params.append(criteria["difficulty"].value if hasattr(criteria["difficulty"], 'value') else criteria["difficulty"])

            if "equipment" in criteria:
                sql += " AND equipment LIKE ?"
                params.append(f"%{criteria['equipment']}%")

            if "age_group" in criteria:
                sql += " AND age_group = ?"
                params.append(criteria["age_group"])

        sql += " ORDER BY saved_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()

            return [self._row_to_content_item(row) for row in rows]

    def _row_to_content_item(self, row: sqlite3.Row) -> ContentItem:
        """Convert a database row to a ContentItem.

        Args:
            row: SQLite row object

        Returns:
            ContentItem object
        """
        # Parse JSON fields
        source_metadata = json.loads(row['source_metadata']) if row['source_metadata'] else {}
        tags = json.loads(row['tags']) if row['tags'] else []

        # Parse datetime fields
        published_at = None
        if row['published_at']:
            try:
                published_at = datetime.fromisoformat(row['published_at'])
            except ValueError as e:
                logger.warning(f"Failed to parse published_at: {e}")

        fetched_at = datetime.fromisoformat(row['fetched_at'])

        saved_at = None
        if row['saved_at']:
            try:
                saved_at = datetime.fromisoformat(row['saved_at'])
            except ValueError as e:
                logger.warning(f"Failed to parse saved_at: {e}")

        # Get Phase 2 fields (with migration compatibility)
        row_keys = row.keys()

        # Parse drill_tags from JSON
        drill_tags = []
        if 'drill_tags' in row_keys and row['drill_tags']:
            try:
                drill_tags = json.loads(row['drill_tags'])
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Failed to parse drill_tags for {row['id']}")

        drill_description = row['drill_description'] if 'drill_description' in row_keys else None

        # Normalize difficulty to PascalCase enum value (handles legacy lowercase data)
        difficulty_raw = row['difficulty'] if 'difficulty' in row_keys else None
        difficulty = None
        if difficulty_raw:
            difficulty_map = {
                'beginner': Difficulty.BEGINNER,
                'intermediate': Difficulty.INTERMEDIATE,
                'advanced': Difficulty.ADVANCED,
            }
            difficulty = difficulty_map.get(difficulty_raw.lower())

        equipment = row['equipment'] if 'equipment' in row_keys else None
        age_group = row['age_group'] if 'age_group' in row_keys else None

        return ContentItem(
            id=row['id'],
            source=ContentSource(row['source']),
            content_type=ContentType(row['content_type']),
            title=row['title'],
            url=row['url'],
            description=row['description'],
            author=row['author'],
            published_at=published_at,
            fetched_at=fetched_at,
            thumbnail_url=row['thumbnail_url'],
            view_count=row['view_count'],
            like_count=row['like_count'],
            comment_count=row['comment_count'],
            source_metadata=source_metadata,
            tags=tags,
            notes=row['notes'],
            saved_at=saved_at,
            collection_id=row['collection_id'],
            drill_tags=drill_tags,
            drill_description=drill_description,
            difficulty=difficulty,
            equipment=equipment,
            age_group=age_group,
        )

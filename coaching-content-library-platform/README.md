# Goalie Drill Library

A comprehensive content aggregation system for hockey goalie coaches to discover, organize, and share drill ideas from YouTube, Reddit, Instagram, and TikTok.

## Features

### Phase 1: Core Infrastructure ✅
- Fetch goalie drill videos from YouTube
- Aggregate goalie-related posts from Reddit
- Store content in a local SQLite database with automatic migrations
- Tag and categorize content for easy searching

### Phase 2: Backend API, oEmbed Ingestors, Discord Bot ✅
- **REST API**: FastAPI backend with full CRUD operations
- **Instagram Support**: Fetch posts and reels via oEmbed API (no authentication required)
- **TikTok Support**: Fetch videos via oEmbed API (no authentication required)
- **Discord Bot**: Interactive bot for automatic URL detection and content saving
- **Drill Metadata**: Track skill focus, difficulty, equipment, age group, and drill type

### Phase 3+: AI Features (Planned)
- Semantic search with vector embeddings
- Automatic drill tagging using LLM
- Practice plan generation
- Video transcription and analysis

## Installation

1. Clone the repository

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys in `.env`:
   ```env
   # Required for YouTube
   YOUTUBE_API_KEY=your_youtube_api_key_here

   # Required for Reddit
   REDDIT_CLIENT_ID=your_reddit_client_id_here
   REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
   REDDIT_USER_AGENT=goalie-drill-aggregator/1.0

   # Required for Discord Bot (Phase 2)
   DISCORD_BOT_TOKEN=your_discord_bot_token_here

   # Optional: API base URL (defaults to http://localhost:8000)
   API_BASE_URL=http://localhost:8000
   ```

## Usage

### Option 1: CLI (Phase 1)

Search for content from the command line:

```bash
# Search YouTube for goalie drills
python -m src.main search "goalie drills" --source youtube --max-results 5

# Search Reddit
python -m src.main search "butterfly push" --source reddit --max-results 10

# Get recent content from YouTube
python -m src.main discover --source youtube
```

### Option 2: REST API (Phase 2)

#### Start the API Server

```bash
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```

Access API documentation at: http://localhost:8000/docs

#### API Endpoints

**Save Content from URL**
```bash
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "source": "YouTube",
    "skill_focus": "butterfly push",
    "difficulty": "intermediate",
    "equipment": "pucks, cones",
    "age_group": "bantam",
    "drill_type": "main"
  }'
```

**List All Content**
```bash
curl http://localhost:8000/api/v1/content
```

**Search and Filter Content**
```bash
curl "http://localhost:8000/api/v1/content?query=butterfly&difficulty=intermediate&limit=10"
```

**Get Specific Content**
```bash
curl http://localhost:8000/api/v1/content/{content_id}
```

**Update Content Metadata**
```bash
curl -X PUT http://localhost:8000/api/v1/content/{content_id}/metadata \
  -H "Content-Type: application/json" \
  -d '{
    "skill_focus": "lateral movement",
    "difficulty": "advanced"
  }'
```

**Delete Content**
```bash
curl -X DELETE http://localhost:8000/api/v1/content/{content_id}
```

### Option 3: Discord Bot (Phase 2)

#### Setup Discord Bot

1. Create a Discord application at https://discord.com/developers/applications
2. Create a bot and copy the bot token
3. Add the bot token to your `.env` file as `DISCORD_BOT_TOKEN`
4. Invite the bot to your Discord server with the following permissions:
   - Read Messages/View Channels
   - Send Messages
   - Use Slash Commands
   - Read Message History

#### Start the Discord Bot

```bash
source venv/bin/activate
python -m src.bot.main
```

#### Using the Bot

1. **Automatic URL Detection**: Simply paste a YouTube, Reddit, Instagram, or TikTok URL in any channel
2. **Interactive Prompts**: The bot will detect the URL and offer to save it with buttons
3. **Metadata Collection**: Click "Save to Library" to open a form where you can add:
   - Skill Focus (e.g., "butterfly push, lateral movement")
   - Difficulty Level (beginner, intermediate, advanced)
   - Required Equipment (e.g., "pucks, cones")
   - Age Group (e.g., "bantam", "12-14")
   - Drill Type (warmup, main, game)
4. **Confirmation**: The bot will confirm when content is saved successfully

**Example Workflow:**
```
User: Check out this drill! https://www.youtube.com/watch?v=example

Bot: 🔵 Content URL Detected
     Found a YouTube link!
     URL: https://www.youtube.com/watch?v=example

     Would you like to save this to your library?
     [Save to Library] [Ignore]

User: *clicks Save to Library*

Bot: *Opens modal form*

User: *Fills in:*
     Skill Focus: butterfly push
     Difficulty: intermediate
     Equipment: pucks

Bot: ✅ Content Saved
     Title: Amazing Butterfly Drill
     Source: YouTube
     Author: Coach Smith
     Skill Focus: butterfly push
     Difficulty: intermediate
```

## Project Structure

```
coaching-drill-aggregator/
├── src/
│   ├── api/                    # FastAPI backend (Phase 2)
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models.py          # Request/response models
│   │   └── routes.py          # API endpoints
│   ├── bot/                   # Discord bot (Phase 2)
│   │   ├── __init__.py
│   │   └── main.py           # Discord bot implementation
│   ├── ingestors/             # Platform-specific content fetchers
│   │   ├── base.py           # Base ingestor interface
│   │   ├── youtube.py        # YouTube API integration
│   │   ├── reddit.py         # Reddit PRAW integration
│   │   ├── instagram.py      # Instagram oEmbed (Phase 2)
│   │   └── tiktok.py         # TikTok oEmbed (Phase 2)
│   ├── models/                # Data models
│   │   └── content.py        # ContentItem model with Phase 2 metadata
│   ├── storage/               # Data persistence layer
│   │   ├── base.py           # Repository interface
│   │   └── sqlite.py         # SQLite implementation with migrations
│   ├── config.py              # Configuration management
│   └── main.py                # CLI entry point
├── tests/                     # Unit tests (57 tests, all passing ✅)
│   ├── test_api.py           # API endpoint tests
│   ├── test_instagram_oembed.py
│   ├── test_tiktok_oembed.py
│   ├── test_phase2_data_layer.py
│   └── ...
├── data/                      # Database storage (created automatically)
│   └── content.db            # SQLite database
├── .env                       # API keys and secrets (not committed)
├── .env.example              # Example environment file
├── requirements.txt           # Python dependencies
├── CLAUDE.md                 # Project documentation and development guide
└── README.md                 # This file
```

## Supported Platforms

| Platform | Search | Get Recent | From URL | Authentication |
|----------|--------|------------|----------|----------------|
| YouTube  | ✅     | ✅         | ✅       | API Key        |
| Reddit   | ✅     | ✅         | ✅       | OAuth Credentials |
| Instagram | ❌    | ❌         | ✅       | None (oEmbed)  |
| TikTok   | ❌     | ❌         | ✅       | None (oEmbed)  |

**Note**: Instagram and TikTok use oEmbed API, which only supports fetching content from URLs (no search/discovery).

## Content Metadata Fields

Each content item can include the following drill-specific metadata:

- **Skill Focus**: What skills the drill targets (e.g., "butterfly push, lateral movement")
- **Difficulty**: Skill level (beginner, intermediate, advanced)
- **Equipment**: Required equipment (e.g., "pucks, cones, net")
- **Age Group**: Target age range (e.g., "bantam", "12-14", "peewee")
- **Drill Type**: Category (warmup, main, game)

These fields can be set when saving content via the API or Discord bot, and updated later.

## Development

### Running Tests

All tests (57 total):
```bash
pytest tests/ -v
```

Specific test suites:
```bash
# Data layer tests
pytest tests/test_phase2_data_layer.py -v

# Instagram oEmbed tests
pytest tests/test_instagram_oembed.py -v

# TikTok oEmbed tests
pytest tests/test_tiktok_oembed.py -v

# API tests
pytest tests/test_api.py -v
```

### Running in Development Mode

**Terminal 1: API Server**
```bash
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```

**Terminal 2: Discord Bot**
```bash
source venv/bin/activate
python -m src.bot.main
```

**Terminal 3: Test API**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"2.0.0"}
```

### Database Migrations

The SQLite database automatically migrates when new Phase 2 fields are added. The migration logic:
1. Checks existing schema using `PRAGMA table_info()`
2. Adds missing columns using `ALTER TABLE`
3. Runs automatically on app startup
4. Is idempotent (safe to run multiple times)

Existing Phase 1 data is preserved during migration.

## Architecture

The system follows a layered architecture:

1. **Data Layer**: Pydantic models and SQLite repository pattern
2. **Ingestor Layer**: Platform-specific adapters implementing `BaseIngestor`
3. **API Layer**: FastAPI REST endpoints for CRUD operations
4. **Bot Layer**: Discord integration for user interaction

Data flows from:
- **CLI** → Ingestor → Repository → Database
- **API** → Ingestor → Repository → Database → API Response
- **Discord Bot** → API → Ingestor → Repository → Database → Discord Response

## Configuration

All configuration is managed through `src/config.py` using Pydantic settings. Configuration can be set via:

1. Environment variables (`.env` file)
2. Default values in `Settings` class

See `.env.example` for all available configuration options.

## Troubleshooting

### Discord Bot Issues

**Bot doesn't respond to messages:**
- Ensure `message_content` intent is enabled in Discord Developer Portal
- Check that bot has "Read Messages" permission in the channel
- Verify `DISCORD_BOT_TOKEN` is correct in `.env`

**API connection failed:**
- Ensure the FastAPI server is running at `API_BASE_URL`
- Check firewall settings if running on different machines
- Verify no authentication is blocking requests

### API Issues

**404 on content fetch:**
- Verify the URL is valid and publicly accessible
- Check that the platform is supported (YouTube, Reddit, Instagram, TikTok)
- Instagram/TikTok private accounts won't work with oEmbed

**422 Validation Error:**
- Ensure `source` field uses correct enum values: "YouTube", "Reddit", "Instagram", "TikTok"
- Check that required fields are provided in request body

## License

MIT

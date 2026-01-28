# Coaching Content Library

Coaching Content Library is an AI-powered content management system designed for hockey goalie coaches. It solves the critical retrieval problem for drills and content saved from social media platforms like YouTube, Instagram, TikTok, and Reddit. The system transforms scattered, hard-to-find content into a structured, searchable, and intelligent library, turning lesson planning from a time-consuming hunt into a fast, focused design session.

## Features

- **Multi-Platform Content Ingestion**: Capture drills and content from YouTube, Reddit, Instagram, and TikTok using a dedicated Discord Bot.
- **Rich Metadata Management**: Go beyond simple bookmarks by adding rich metadata like skill focus, difficulty level, age group, and equipment requirements.
- **Responsive Web Interface**: Browse your entire collection in a modern, responsive web app featuring a visual grid of drill cards.
- **AI-Powered Semantic Search**: Find drills using natural coaching language (e.g., "drills for getting back up quickly") instead of just keyword matching.
- **AI-Driven Recommendations**: Discover new approaches with the "Similar Drills" feature, which suggests related content based on a combination of tags and semantic similarity.
- **AI Auto-Tagging**: Augment your own tags with AI-generated suggestions to improve discoverability.

## Technology Stack

### Backend (`coaching-content-library-platform`)
- **Framework**: Python 3.12 with FastAPI
- **ORM**: SQLAlchemy 2.0+ with Pydantic 2.0+ for data validation
- **Database**: SQLite for primary metadata storage
- **Discord Bot**: discord.py
- **Platform Ingestors**: Google API Client (YouTube), PRAW (Reddit)

### Frontend (`coaching-content-library-web`)
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with a custom hockey-themed design system
- **UI Components**: shadcn/ui (Radix UI primitives)
- **State Management**: TanStack Query for server state
- **Routing**: React Router

### AI & MLOps
- **Vector Database**: ChromaDB for storing and searching vector embeddings.
- **AI Services**:
  - **OpenAI `text-embedding-3-small`**: For generating vector embeddings for semantic search.
  - **OpenAI `gpt-4o-mini`**: For AI-powered auto-tagging.

## Project Structure

This monorepo is organized into two main packages:

-   `./coaching-content-library-platform/`: The Python backend, which includes the FastAPI server, Discord bot, and content ingestors.
-   `./coaching-content-library-web/`: The React frontend application.
-   `./_bmad/`: Contains development artifacts and workflows for the BMAD (Bot-Me-And-Dall-E) development process. This directory is part of the project's tooling and can generally be ignored during normal development.

## Getting Started

### Prerequisites

-   Python 3.12+
-   Node.js 18+ and npm
-   Git

### 1. Backend Setup

First, set up the Python backend server and Discord bot.

```bash
# Navigate to the backend directory
cd coaching-content-library-platform

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate
# On Windows, use: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file for your API keys
cp .env.example .env
```

Now, open the newly created `.env` file and add your API keys for the required services (YouTube, Reddit, Discord, and OpenAI).

### 2. Frontend Setup

Next, set up the React frontend.

```bash
# Navigate to the frontend directory from the project root
cd coaching-content-library-web

# Install Node.js dependencies
npm install
```

## Running the Application

To run the full application, you need to run the backend and frontend servers in separate terminal windows.

### Terminal 1: Run the Backend API

```bash
# In the coaching-content-library-platform directory
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`.

### Terminal 2: Run the Frontend Application

```bash
# In the coaching-content-library-web directory
npm run dev
```
The web app will be available at `http://localhost:5173` (or another port if 5173 is busy). The Vite dev server is configured to proxy API requests from `/api` to the backend at `http://localhost:8000`.

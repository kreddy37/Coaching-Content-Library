---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - '_bmad-output/planning-artifacts/product-brief-Coaching-content-library-2026-01-07.md'
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/ux-design-specification.md'
  - '_bmad-output/project-context.md'
workflowType: 'architecture'
project_name: 'Coaching-content-library'
user_name: 'Kohl'
date: '2026-01-23'
lastStep: 8
status: 'complete'
completedAt: '2026-01-24'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

The project has **50 functional requirements** organized into 6 capability areas:

1. **Content Capture & Ingestion (FR1-FR9):** Discord bot-based URL submission with guided metadata collection for YouTube, TikTok, Instagram, Reddit sources. The Discord bot is already functional and deployed.

2. **Content Management (FR10-FR15):** Full CRUD operations on drill metadata including viewing, editing, deleting drills, and managing tags with timestamp tracking.

3. **Content Discovery & Search (FR16-FR25):** Dual search approach - semantic search using vector embeddings for natural language queries, plus advanced filtering by tags, difficulty, age group, equipment with real-time application.

4. **AI-Enhanced Organization (FR26-FR33):** Three AI features requiring careful integration:
   - LLM-powered auto-tagging that augments (never replaces) user tags with rate limiting (1 per 5 min)
   - Tag-based similarity calculation using Jaccard similarity
   - Semantic similarity using vector embeddings with cosine similarity
   - Combined recommendation engine blending both approaches

5. **Content Viewing & Browsing (FR34-FR41):** Responsive drill library grid with drill cards, expandable detail sheets, thumbnail display, and mobile/tablet/desktop support.

6. **Metadata Management (FR42-FR50):** Structured data model with specific field types - arrays for tags, enums for difficulty/age_group/source, free text for descriptions/equipment, timestamps for tracking.

**Architectural Implications:**
- Backend must support vector embeddings storage and querying (separate from main data)
- AI service integration requires rate limiting, cost management, and graceful failure handling
- Frontend needs real-time filtering with <500ms response
- Existing Discord bot → SQLite database → web UI workflow must be preserved

**Non-Functional Requirements:**

**Performance (NFR1-NFR5):**
- Page load <3s, semantic search <2s, filter <500ms, instant detail view
- Progressive image loading with lazy loading strategy
- Requires caching strategy and optimized API design

**Integration (NFR6-NFR21):**
- 4 external platform APIs (YouTube, Reddit have good APIs; Instagram/TikTok limited)
- 2 AI service integrations (embeddings API, LLM API) with rate limiting
- Discord bot integration maintaining existing workflow
- Graceful degradation when external services fail

**Reliability (NFR22-NFR30):**
- Live deployment for portfolio presentation (no downtime during job search)
- Database backups for curated drill library
- Backend contract integrity (PascalCase enums, snake_case fields) enforced throughout
- User data never overwritten by AI operations

**Security (NFR31-NFR36):**
- Basic security best practices (env vars for credentials, input validation, HTTPS)
- No sensitive user data or compliance requirements
- Private drill library (no public sharing in MVP)

**Scale & Complexity:**

- **Primary domain:** Full-stack web application (React 19.2.0 SPA + FastAPI 0.104.0+ backend)
- **Complexity level:** Medium
  - Sophisticated: AI integration with 3 features, dual database strategy, platform integrations
  - Straightforward: Single-user tool, no multi-tenancy, no complex authorization, personal use scale
- **Estimated architectural components:**
  - Frontend: 7 custom components (DrillCard, DrillGrid, DrillDetail, FilterBar, SearchHero, TagManager, AddDrillModal)
  - Backend: 4 platform ingestors (YouTube, Reddit, Instagram, TikTok), content repository, vector embeddings service, LLM tagging service, recommendation engine
  - Data: SQLite main database, vector database (ChromaDB or FAISS), API client layer
  - Integration: Discord bot (already complete), 6 external APIs (platforms + AI services)

### Technical Constraints & Dependencies

**Existing Infrastructure:**
- Discord bot already functional and deployed (discord.py 2.3.0+)
- Backend SQLite database with ContentItem model already established
- Backend contract defined and enforced:
  - **PascalCase enum values:** `'YouTube'`, `'TikTok'`, `'Instagram'`, `'Reddit'`
  - **snake_case field names:** `drill_tags`, `drill_description`, `content_type`, `published_at`
  - Frontend must match backend exactly - no camelCase conversion

**Technology Stack Constraints:**
- **Frontend:** React 19.2.0, TypeScript 5.9.3, Vite 7.2.4, TanStack Query 5.90.16, Tailwind CSS 4.1.18
- **Backend:** Python 3.12, FastAPI 0.104.0+, SQLAlchemy 2.0+, Pydantic 2.0+
- **Database:** SQLite for main data (already chosen for simplicity), separate vector DB for embeddings
- **Deployment:** Static frontend hosting, backend with SQLite support, public URL required for portfolio

**External Dependencies:**
- Platform APIs: YouTube (good), Reddit (good via PRAW), Instagram (limited), TikTok (limited)
- AI Services: Vector embeddings API (OpenAI or Sentence Transformers), LLM API (GPT-4o-mini or Claude-3-haiku)
- Rate limits and costs must be managed

**Project Context Rules:**
58 critical implementation rules documented in project-context.md including:
- Backend contract enforcement patterns
- Import/export conventions (@/ alias required)
- TanStack Query patterns (query keys, invalidation)
- Repository patterns (check existence before delete)
- Test organization (pytest with @patch decorators)

### Cross-Cutting Concerns Identified

**Backend Contract Enforcement:**
- Enum casing and field naming must be validated throughout the stack
- TypeScript types must match backend exactly (no transformation layer)
- API integration layer must preserve backend contracts
- Testing must verify contract compliance

**AI Service Integration Patterns:**
- Rate limiting strategy (1 LLM call per 5 min, embedding batching)
- Cost management and monitoring
- Graceful degradation when AI services fail
- Error handling that doesn't block core functionality
- Caching strategy for embeddings and LLM responses

**Performance Optimization:**
- TanStack Query caching configuration
- Image lazy loading and progressive enhancement
- Debounced search input (300ms from UX spec)
- Real-time filter application (<500ms target)
- Code splitting and route-based chunks

**Error Handling & Resilience:**
- Platform API failures and rate limits
- AI service unavailability
- Fallback metadata for Instagram/TikTok
- Network errors and timeout handling
- User-friendly error messages

**Data Flow & State Management:**
- Discord bot → SQLite → FastAPI → React SPA
- Server state via TanStack Query
- UI state via React hooks
- Vector embeddings lifecycle (create on save, store in vector DB, query for search/recommendations)

**Testing Strategy:**
- Backend: pytest with mocks for repository/ingestors/external APIs
- Integration tests using TestClient
- Frontend: Expected Vitest/React Testing Library (not yet implemented)
- Contract testing to ensure frontend/backend alignment

**Development Workflow:**
- Frontend dev server (port 3000) proxies /api to backend (port 8000)
- .env files for credentials (not committed)
- BMAD workflows for planning and implementation tracking

## Starter Template Evaluation

### Primary Technology Domain

**Full-stack web application** with:
- **Frontend:** React SPA (to be scaffolded)
- **Backend:** FastAPI + Python (already complete and functional)

### Technical Stack Status

**Backend Infrastructure: ✅ COMPLETE**
- FastAPI 0.104.0+ backend with SQLite database operational
- Discord bot deployed and capturing drills successfully
- Platform ingestors (YouTube, Reddit, Instagram, TikTok) implemented
- ContentItem model and repository pattern established
- API endpoints functional and tested

**Frontend Infrastructure: 🔨 TO BE BUILT**
- React 19.2.0 + TypeScript 5.9.3 SPA to be scaffolded
- Exact technology stack specified in project-context.md
- Backend contract already defined - frontend must match

### Starter Options Considered

**Option 1: Create React App (CRA)**
- ❌ **Rejected:** Deprecated and no longer recommended by React team
- ❌ Uses outdated build tooling (Webpack)
- ❌ Slower development server and build times

**Option 2: Next.js**
- ❌ **Rejected:** Overkill for this use case
- Backend already exists (FastAPI) - don't need Next.js API routes
- SEO not required (NFR: personal tool, no search engine discoverability needed)
- Server-side rendering unnecessary - client-side SPA is sufficient
- Adds complexity without benefit for single-user portfolio project

**Option 3: Vite + React (Official Vite Scaffolding)**
- ✅ **SELECTED:** Aligns perfectly with project requirements
- Fast development server with HMR (Hot Module Replacement)
- Optimized production builds
- Official React + TypeScript template available
- Lightweight and simple - matches "pragmatic over perfect" philosophy
- Vite 7.2.4 already specified in project-context.md

### Selected Starter: Vite + React Official Template

**Rationale for Selection:**

1. **Backend Already Complete:** Don't need full-stack framework - just frontend scaffolding
2. **Version Alignment:** Vite 7.2.4 specified in project-context.md
3. **Development Speed:** Instant server start, fast HMR for rapid iteration
4. **Simplicity:** Minimal boilerplate, easy to understand and extend
5. **Production Ready:** Optimized builds with code splitting and tree shaking
6. **TypeScript First:** Official TypeScript template with proper configuration
7. **Portfolio Quality:** Modern tooling demonstrates current best practices

**Initialization Command:**

```bash
# Navigate to project root
cd coaching-content-library-platform

# Create frontend using Vite official template
npm create vite@7.2.4 frontend -- --template react-ts

# Navigate into frontend directory
cd frontend

# Install base dependencies
npm install

# Add project-specific dependencies (per project-context.md requirements)
npm install @tanstack/react-query@5.90.16 react-router-dom@7.11.0 axios@1.13.2

# Add Tailwind CSS 4.1.18
npm install -D tailwindcss@4.1.18 postcss@8.5.6 autoprefixer

# Add shadcn/ui dependencies (Radix UI primitives)
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
npm install @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-label

# Add Lucide React icons
npm install lucide-react@0.562.0

# Add utility libraries
npm install clsx tailwind-merge class-variance-authority

# Add development dependencies
npm install -D @types/node
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- TypeScript 5.9.3 with strict mode enabled
- React 19.2.0 with automatic JSX runtime
- Module resolution: "bundler" (Vite-specific)
- ESLint 9.39.1 with typescript-eslint 8.46.4
- Path alias: `@/*` → `./src/*` (configured in tsconfig and vite.config)

**Styling Solution:**
- Tailwind CSS 4.1.18 (v4 API - different from v3!)
- PostCSS 8.5.6 for processing
- Custom theme: `hockey-blue` (#1e3a5f), `ice-blue` (#38bdf8)
- Source colors: YouTube (red-600), Reddit (orange-500), Instagram (pink-500), TikTok (black)
- Difficulty colors: beginner (green-500), intermediate (amber-500), advanced (red-500)
- shadcn/ui component library for accessible Radix UI primitives

**Build Tooling:**
- Vite 7.2.4 for development and production builds
- Development server on port 3000 with HMR
- API proxy configuration: `/api` → `http://localhost:8000` (FastAPI backend)
- Code splitting and tree shaking automatic
- Production build outputs to `dist/`

**Testing Framework:**
- Vitest (Vite's test runner) for unit tests
- React Testing Library for component tests
- Expected pattern: `src/**/*.test.tsx` or `src/**/*.spec.tsx`
- TanStack Query testing utilities for hook tests

**Code Organization:**
- `src/components/ui/` - shadcn/ui components ONLY
- `src/components/{feature}/` - Feature components (drills, search, planner, layout)
- `src/lib/` - Utilities, types, API client
- `src/hooks/` - Custom React hooks (useContentList, useContentItem, useCreateContent)
- `src/pages/` - Route pages
- `src/App.tsx` - Root component with router
- `src/main.tsx` - Entry point

**Development Experience:**
- Hot module replacement (HMR) for instant updates
- TypeScript strict mode with enhanced linting
- ESLint flat config with React hooks and React refresh rules
- Vite dev server runs on port 3000
- Backend integration via proxy during development

**State Management:**
- TanStack Query 5.90.16 for server state (API data, caching, mutations)
- React hooks for UI state (useState, useReducer)
- Query keys pattern: `['content', params]` or `['content', source, id]`
- Automatic query invalidation after mutations

**Routing:**
- React Router DOM 7.11.0
- Routes defined in `App.tsx` with layout wrapper using `<Outlet />`
- Client-side routing (no SSR needed)
- Pages in `src/pages/` directory

**Backend Integration:**
- Axios 1.13.2 HTTP client
- API client in `src/lib/api.ts`
- Backend contract enforcement: PascalCase enums, snake_case fields
- TypeScript types matching backend exactly (no camelCase conversion)

**Critical Setup Requirements:**

1. **Configure Vite Proxy** (vite.config.ts):
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
```

2. **Initialize Tailwind Config** with custom theme colors

3. **Set up shadcn/ui** components directory structure

4. **Create TypeScript types** matching backend contract exactly

5. **Configure TanStack Query** provider in App.tsx

**Note:** Frontend project initialization using Vite should be **Story 1.1: Frontend Project Setup** in Epic 1. This establishes the foundation before any feature development begins.

### Architectural Constraints from Existing Backend

**Backend Contract (MUST MATCH):**
- Enum values: `'YouTube'`, `'TikTok'`, `'Instagram'`, `'Reddit'` (PascalCase)
- Field names: `drill_tags`, `drill_description`, `content_type`, `published_at` (snake_case)
- Frontend types MUST NOT transform to camelCase
- Use `| null` for nullable fields (backend returns null, not undefined)

**API Integration Pattern:**
- All API calls go through Axios client
- TanStack Query wraps all data fetching
- Query invalidation after mutations for cache consistency
- Error handling preserves backend error messages

**Data Flow:**
Discord bot → SQLite → FastAPI `/api/v1/*` → Axios → TanStack Query → React components

## Core Architectural Decisions

### Decision Summary

**Critical Decisions Made:**
All decisions required for implementation are now complete. No blocking architectural choices remain.

**Decision Categories:**
1. AI Services Integration (ChromaDB, OpenAI embeddings & LLM)
2. Deployment & Infrastructure (Vercel + self-hosted hybrid)
3. API Design Standards (structured errors, rate limiting, versioning)

### AI Services Integration

**Vector Database: ChromaDB**
- **Decision:** Use ChromaDB for vector storage and similarity search
- **Version:** Latest stable (to be verified at implementation)
- **Rationale:**
  - Lightweight with SQLite backend (aligns with existing database choice)
  - Simple Python API with good documentation
  - Sufficient performance for personal-use scale (hundreds of drills)
  - Built-in persistence with minimal configuration
- **Affects:**
  - FR17-FR18 (semantic search implementation)
  - FR31-FR33 (recommendation engine similarity calculations)
  - Backend architecture (separate vector storage from main SQLite DB)
- **Implementation Note:** Initialize ChromaDB collection on first run, persist to disk alongside SQLite database

**Embeddings API: OpenAI text-embedding-3-small**
- **Decision:** Use OpenAI embeddings API for vector generation
- **Model:** text-embedding-3-small (1536 dimensions)
- **Rationale:**
  - High-quality semantic embeddings for accurate search
  - Demonstrates AI API integration for portfolio presentation
  - Negligible cost at personal-use scale (~$0.0001 for 50 drills)
  - Industry-standard solution with excellent documentation
- **Affects:**
  - FR17-FR18 (semantic search quality)
  - FR31 (semantic similarity calculations for recommendations)
  - NFR13 (embedding API integration)
  - NFR15 (API cost management - minimal costs)
- **Cost Management:**
  - Batch embedding generation where possible
  - Cache embeddings in ChromaDB (never regenerate unless content changes)
  - Estimated cost: <$0.01 for MVP with 50 drills

**LLM API: OpenAI GPT-4o-mini**
- **Decision:** Use GPT-4o-mini for auto-tagging drill content
- **Model:** gpt-4o-mini
- **Rationale:**
  - Cost-efficient (~$0.150 per 1M input tokens, ~$0.600 per 1M output tokens)
  - Fast response times suitable for interactive features
  - Good at structured output generation (tag arrays)
  - Single API provider with embeddings (simplified key management)
- **Affects:**
  - FR26-FR29 (AI-powered auto-tagging)
  - NFR12 (LLM integration with rate limiting)
  - NFR15 (API cost management)
- **Rate Limiting:** Max 1 call per 5 minutes (in-memory tracking)
- **Cost Management:**
  - Rate limiting prevents cost runaway
  - Estimated cost: ~$0.002 for 50 drills
  - Graceful failure - manual tagging always available

**AI Services Architecture:**
```
Drill Save Event
  ↓
Generate Embeddings (OpenAI) → Store in ChromaDB
  ↓
Auto-Tag (GPT-4o-mini, rate limited) → Augment drill_tags
  ↓
Save to SQLite (main database)

Search Query
  ↓
Generate Query Embedding (OpenAI)
  ↓
Query ChromaDB for Similar Vectors
  ↓
Return Matching Drills from SQLite

Recommendation Request
  ↓
Calculate Tag Similarity (Jaccard) + Semantic Similarity (ChromaDB)
  ↓
Combine Scores & Return Top N Drills
```

### Deployment & Infrastructure

**Frontend Hosting: Vercel**
- **Decision:** Deploy React SPA to Vercel
- **Rationale:**
  - Zero-config Vite deployment with automatic builds
  - Automatic HTTPS with free SSL certificates
  - Git-based deployments (push to main = automatic deploy)
  - Generous free tier perfect for portfolio projects
  - Professional URL for portfolio presentation
  - Industry standard for modern React applications
- **Affects:**
  - NFR22 (public URL accessibility for portfolio)
  - NFR33 (HTTPS enforcement)
  - Deployment workflow and CI/CD
- **Configuration:**
  - Build command: `npm run build`
  - Output directory: `dist`
  - Environment variable: `VITE_API_URL` pointing to backend dynamic DNS domain

**Backend Hosting: Self-Hosted on Proxmox**
- **Decision:** Host FastAPI backend on existing Proxmox server with dynamic DNS
- **Rationale:**
  - Leverages existing always-on infrastructure
  - Zero monthly hosting costs
  - Full control over SQLite database and Discord bot integration
  - Direct access to drill library data for backups
  - Not actively interviewing - local hosting acceptable
- **Affects:**
  - NFR22 (backend API accessibility)
  - NFR23 (availability during demos)
  - NFR24 (database backups - easier with local control)
  - Deployment workflow
- **Configuration:**
  - Dynamic DNS for stable public hostname
  - Reverse proxy (Caddy) for HTTPS
  - Environment variables for API keys
  - Discord bot runs on same server (already operational)

**Reverse Proxy: Caddy**
- **Decision:** Use Caddy for reverse proxy and automatic HTTPS
- **Rationale:**
  - Automatic Let's Encrypt SSL certificate management
  - Simple configuration (Caddyfile)
  - Built-in HTTPS redirects
  - Perfect for FastAPI backend exposure
- **Affects:**
  - NFR33 (HTTPS enforcement)
  - Backend public accessibility
  - SSL certificate management
- **Configuration:**
  ```
  your-domain.com {
      reverse_proxy localhost:8000
  }
  ```

**Hybrid Architecture:**
```
User Browser
  ↓ HTTPS
Vercel (Frontend - React SPA)
  ↓ HTTPS API Calls
Caddy Reverse Proxy (Proxmox)
  ↓
FastAPI Backend (localhost:8000)
  ↓
SQLite DB + ChromaDB ← Discord Bot (same machine)
```

**CORS Configuration:**
- FastAPI must allow origin: `https://yourusername.vercel.app` (or custom domain)
- Configured in FastAPI middleware

### API Design & Standards

**Error Response Format: Structured Errors**
- **Decision:** Use structured error response format across all API endpoints
- **Format:**
  ```json
  {
    "error": {
      "code": "ERROR_CODE_CONSTANT",
      "message": "Human-readable error description",
      "details": {}  // Optional additional context
    }
  }
  ```
- **Rationale:**
  - Better frontend error handling and user messaging
  - Clearer debugging with error codes
  - Demonstrates API design best practices for portfolio
  - Allows error categorization and logging
- **Affects:**
  - All FastAPI endpoints error handling
  - Frontend error handling logic
  - NFR20 (clear error messages to users)
- **Error Code Examples:**
  - `CONTENT_NOT_FOUND` (404)
  - `INVALID_SOURCE_PLATFORM` (400)
  - `RATE_LIMIT_EXCEEDED` (429)
  - `EXTERNAL_API_FAILURE` (503)

**Rate Limiting: Application-Level In-Memory**
- **Decision:** Implement rate limiting using in-memory timestamp tracking
- **Strategy:**
  - Track last LLM call timestamp in Python dictionary/variable
  - Check elapsed time before making new auto-tag requests
  - Limit: 1 LLM call per 5 minutes (FR28)
- **Rationale:**
  - Simple implementation without external dependencies
  - Adequate for single-user, low-frequency limit
  - Timestamp reset on server restart acceptable for personal use
  - Can upgrade to database-backed later if needed
- **Affects:**
  - FR28 (auto-tagging rate limit)
  - NFR12 (LLM API rate limiting)
  - NFR15 (API cost management)
- **Implementation:**
  ```python
  last_llm_call: Optional[datetime] = None
  MIN_INTERVAL = timedelta(minutes=5)

  def can_call_llm() -> bool:
      if last_llm_call is None:
          return True
      return datetime.now() - last_llm_call >= MIN_INTERVAL
  ```

**API Versioning: /api/v1/ Prefix**
- **Decision:** Maintain `/api/v1/` prefix for all API endpoints
- **Rationale:**
  - Already established in existing backend
  - Allows future breaking changes via `/api/v2/` if needed
  - Industry best practice for API versioning
- **Affects:** All API endpoint paths
- **Examples:**
  - `GET /api/v1/content`
  - `POST /api/v1/content`
  - `GET /api/v1/content/{id}/similar`

### Decision Impact Analysis

**Implementation Sequence:**

**Phase 1: Foundation (Epic 1)**
1. Frontend scaffold with Vite (Story 1.1)
2. Tailwind + shadcn/ui setup (Story 1.2)
3. TanStack Query configuration (Story 1.4)
4. API client with structured error handling (Story 1.4)

**Phase 2: AI Services Setup (Epics 5, 6, 7)**
5. ChromaDB initialization and persistence
6. OpenAI API integration (embeddings + LLM)
7. Rate limiting implementation for LLM calls
8. Vector embedding generation pipeline

**Phase 3: Deployment (Post-Implementation)**
9. Vercel frontend deployment configuration
10. Caddy reverse proxy setup on Proxmox
11. CORS configuration for hybrid architecture
12. Environment variable management

**Cross-Component Dependencies:**

**ChromaDB ↔ OpenAI Embeddings:**
- Embeddings must be generated via OpenAI before storing in ChromaDB
- ChromaDB queries return vector IDs that map to SQLite drill records

**Rate Limiting ↔ LLM Auto-Tagging:**
- Auto-tagging feature checks rate limiter before calling GPT-4o-mini
- Failed rate limit check skips auto-tagging gracefully (user tags still saved)

**Frontend (Vercel) ↔ Backend (Proxmox):**
- CORS configuration must allow Vercel domain
- Frontend environment variable must point to dynamic DNS backend URL
- HTTPS required on both sides for security

**Structured Errors ↔ Frontend Error Handling:**
- Frontend can categorize errors by code for user-friendly messages
- Error details can be logged for debugging without exposing to user

**AI Services ↔ Graceful Degradation:**
- If OpenAI API fails, semantic search falls back to tag-based filtering
- If auto-tagging fails, user-provided tags still saved successfully
- Core functionality (browse, filter, CRUD) works without AI services

### Deferred Decisions (Post-MVP)

**Not Critical for MVP Implementation:**
- Database migration strategy (simple SQLite schema, migrations can wait)
- Monitoring and logging infrastructure (local access sufficient for personal use)
- CI/CD pipeline automation (manual deploys acceptable initially)
- Performance optimization beyond requirements (NFR targets are conservative)
- Backup automation (manual backups acceptable for MVP)

**Can Be Added Later:**
- Redis for rate limiting (in-memory adequate for single user)
- Database connection pooling (SQLite doesn't benefit from pooling)
- Advanced caching strategies (TanStack Query handles caching)
- Load balancing (single-user application)

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 7 additional pattern areas beyond the 58 rules in project-context.md

These patterns prevent AI agents from making incompatible implementation choices that would cause integration conflicts.

### Naming Patterns

**Component Naming (from project-context.md):**
- Component files: PascalCase (`DrillCard.tsx`, `SearchHero.tsx`)
- Component functions: PascalCase export (`export function DrillCard`)
- Props interfaces: PascalCase with `Props` suffix (`DrillCardProps`)
- **Pattern:** Always export props interfaces separately for type reusability

**API Naming (from project-context.md):**
- Endpoints: `/api/v1/` prefix, plural resources (`/api/v1/content`)
- Field names: snake_case (`drill_tags`, `drill_description`, `content_type`)
- Enum values: PascalCase (`'YouTube'`, `'TikTok'`, `'Instagram'`, `'Reddit'`)
- Query parameters: snake_case (`?difficulty=beginner&age_group=bantam`)

**File & Directory Naming (from project-context.md):**
- Components: PascalCase files (`DrillCard.tsx`)
- Utilities/hooks: camelCase files (`useContent.ts`, `utils.ts`)
- Directories: lowercase, feature-based (`drills/`, `search/`, `layout/`)
- Test files: `*.test.tsx` or `*.spec.tsx` pattern

**Backend Naming (from project-context.md):**
- All files: snake_case (`content.py`, `test_api.py`)
- Directories: lowercase (`api/`, `ingestors/`, `models/`)
- Python classes: PascalCase (`ContentItem`, `BaseIngestor`)
- Functions/methods: snake_case (`get_content`, `from_url`)

### Structure Patterns

**Frontend Project Organization (from project-context.md + new patterns):**
```
src/
├── components/
│   ├── ui/              # shadcn/ui components ONLY
│   ├── drills/          # Drill-related feature components
│   ├── search/          # Search feature components
│   ├── layout/          # Layout components (Header, Footer)
│   └── planner/         # Planner feature components
├── hooks/               # Custom React hooks (useContentList, useContentItem)
├── lib/
│   ├── api.ts          # Axios API client
│   ├── types.ts        # TypeScript interfaces matching backend
│   ├── utils.ts        # Utility functions (cn helper)
│   └── config.ts       # ✅ NEW: Centralized environment variable config
├── pages/               # Route pages (Library.tsx, Planner.tsx)
├── routes.tsx          # ✅ NEW: Centralized route configuration
├── App.tsx             # Root component with QueryClientProvider
└── main.tsx            # Entry point
```

**Backend Project Organization (from project-context.md):**
```
src/
├── api/                # FastAPI routes and API models
├── ingestors/          # Platform-specific content fetchers
├── models/             # Domain models (ContentItem, enums)
├── storage/            # Database repository layer
├── services/           # ✅ NEW: AI services (ChromaDB, OpenAI)
└── bot/                # Discord bot (separate concern)

tests/                  # Mirror src/ structure
chroma_data/            # ✅ NEW: ChromaDB persistence directory
```

**Test Organization (from project-context.md):**
- Backend: `tests/` directory mirroring `src/` structure
- Test files: `test_*.py` pattern
- Test classes: `TestCamelCase` grouping
- Frontend: `src/**/*.test.tsx` co-located with components

### Format Patterns

**API Response Formats (from decisions):**

**Success Response:**
```json
{
  "data": [...],
  "total": 10
}
```

**Error Response (structured):**
```json
{
  "error": {
    "code": "CONTENT_NOT_FOUND",
    "message": "Content not found",
    "details": {}
  }
}
```

**Data Exchange Formats (from project-context.md):**
- Field naming: snake_case (`drill_tags`, `published_at`)
- Enum values: PascalCase strings (`'YouTube'`, `'Beginner'`)
- Dates: ISO 8601 strings (`"2026-01-23T10:30:00Z"`)
- Nullables: Use `null` (not `undefined`)
- Booleans: `true`/`false` (not 1/0)

### Component Patterns

**React Component Structure:**

**✅ REQUIRED PATTERN:**
```typescript
// 1. Imports
import { useState } from 'react';
import type { ContentItem } from '@/lib/types';

// 2. Props interface (ALWAYS export separately)
export interface DrillCardProps {
  drill: ContentItem;
  onClick: () => void;
}

// 3. Component export
export function DrillCard({ drill, onClick }: DrillCardProps) {
  // 4. Hooks first
  const [isHovered, setIsHovered] = useState(false);

  // 5. Handlers next
  const handleClick = () => { ... };

  // 6. Render
  return <div>...</div>;
}
```

**❌ ANTI-PATTERN:**
```typescript
// Don't: Inline props without exported interface
export function DrillCard(props: { drill: ContentItem }) { ... }

// Don't: Default exports
export default function DrillCard() { ... }
```

**Form State Management:**

**✅ REQUIRED PATTERN (Form Object State):**
```typescript
function AddDrillModal() {
  const [formData, setFormData] = useState({
    url: '',
    drill_description: '',
    drill_tags: [],
    difficulty: 'beginner',
    age_group: 'bantam'
  });

  const handleSubmit = () => {
    createDrill.mutate(formData); // Direct pass to API
  };
}
```

**❌ ANTI-PATTERN:**
```typescript
// Don't: Individual state for each field (harder to manage)
const [url, setUrl] = useState('');
const [description, setDescription] = useState('');
const [tags, setTags] = useState([]);
```

### State Management Patterns

**TanStack Query Configuration (from project-context.md + new patterns):**

**Global QueryClient Setup (App.tsx):**
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      onError: (error) => {
        // ✅ NEW: Global error handling
        console.error('Query error:', error);
        toast.error('Failed to load data');
      }
    },
    mutations: {
      onError: (error) => {
        console.error('Mutation error:', error);
        toast.error('Operation failed');
      }
    }
  }
});
```

**Query Key Patterns (from project-context.md):**
- List queries: `['content']` or `['content', filters]`
- Detail queries: `['content', source, id]`
- Related queries: `['content', id, 'similar']`

**Query Invalidation (from project-context.md):**
```typescript
useMutation({
  mutationFn: (data) => contentApi.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['content'] });
  }
});
```

### Environment Configuration Patterns

**Centralized Config Object:**

**✅ REQUIRED PATTERN (`src/lib/config.ts`):**
```typescript
function getEnvVar(key: string, defaultValue?: string): string {
  const value = import.meta.env[key] || defaultValue;
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

export const config = {
  apiUrl: getEnvVar('VITE_API_URL', 'http://localhost:8000'),
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD
} as const;
```

**Usage:**
```typescript
import { config } from '@/lib/config';

const response = await axios.get(`${config.apiUrl}/api/v1/content`);
```

**❌ ANTI-PATTERN:**
```typescript
// Don't: Direct import.meta.env access everywhere
const url = import.meta.env.VITE_API_URL; // No validation, no defaults
```

### Routing Patterns

**Route Configuration:**

**✅ REQUIRED PATTERN (`src/routes.tsx`):**
```typescript
import { RouteObject } from 'react-router-dom';
import { Library } from '@/pages/Library';
import { Planner } from '@/pages/Planner';
import { Layout } from '@/components/layout/Layout';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Library /> },
      { path: 'planner', element: <Planner /> }
    ]
  }
];
```

**Usage in App.tsx:**
```typescript
import { useRoutes } from 'react-router-dom';
import { routes } from './routes';

function App() {
  const element = useRoutes(routes);
  return element;
}
```

### AI Services Integration Patterns

**ChromaDB Collection Management:**

**✅ REQUIRED PATTERN (Backend initialization):**
```python
# src/services/vector_service.py
import chromadb
from chromadb.config import Settings

COLLECTION_NAME = "coaching_drills"
CHROMA_PERSIST_DIR = "./chroma_data"

def initialize_chroma_client():
    client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Drill content embeddings"}
    )

    return client, collection

# Initialize on app startup (main.py)
chroma_client, drill_collection = initialize_chroma_client()
```

**Collection ID Mapping:**
- ChromaDB vector IDs map to SQLite drill primary keys
- Use drill ID as ChromaDB document ID for easy lookup

**OpenAI API Call Patterns:**

**✅ REQUIRED PATTERN (with retry and timeout):**
```python
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

EMBEDDING_TIMEOUT = 30  # seconds
LLM_TIMEOUT = 60  # seconds

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_embedding(text: str) -> list[float]:
    try:
        response = await openai.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            timeout=EMBEDDING_TIMEOUT
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        # Graceful degradation: continue without embeddings
        return None

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_tags(description: str) -> list[str]:
    try:
        response = await openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Generate tags: {description}"}],
            timeout=LLM_TIMEOUT
        )
        # Parse tags from response
        return parse_tags(response)
    except Exception as e:
        logger.error(f"LLM tagging failed: {e}")
        # Graceful degradation: return empty tags (user tags still saved)
        return []
```

**Rate Limiting Pattern (LLM calls):**
```python
from datetime import datetime, timedelta

last_llm_call: Optional[datetime] = None
MIN_INTERVAL = timedelta(minutes=5)

def can_call_llm() -> bool:
    global last_llm_call
    if last_llm_call is None:
        return True
    return datetime.now() - last_llm_call >= MIN_INTERVAL

def record_llm_call():
    global last_llm_call
    last_llm_call = datetime.now()
```

### Error Handling Patterns

**Structured Error Responses (from decisions):**

**✅ REQUIRED PATTERN (FastAPI):**
```python
from fastapi import HTTPException
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: dict[str, any]

def raise_structured_error(code: str, message: str, status_code: int, details: dict = None):
    raise HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": code,
                "message": message,
                "details": details or {}
            }
        }
    )

# Usage
if not content:
    raise_structured_error(
        code="CONTENT_NOT_FOUND",
        message=f"Content {content_id} not found",
        status_code=404
    )
```

**Frontend Error Handling:**
```typescript
// Global error handler in QueryClient (already configured)
// Component-level override when needed:
const { data, error } = useQuery({
  queryKey: ['content', id],
  queryFn: () => contentApi.get(id),
  onError: (err) => {
    // Custom error handling for this specific query
    toast.error(`Failed to load drill: ${err.message}`);
  }
});
```

### Testing Patterns (from project-context.md)

**Backend Testing:**
```python
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

class TestContentAPI:
    @patch('src.api.routes.repository')
    def test_get_content_list(self, mock_repo):
        mock_repo.get_all.return_value = [mock_content_item]

        client = TestClient(app)
        response = client.get('/api/v1/content')

        assert response.status_code == 200
        mock_repo.get_all.assert_called_once()
```

**Frontend Testing (expected pattern):**
```typescript
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DrillCard } from './DrillCard';

test('renders drill card', () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <DrillCard drill={mockDrill} onClick={() => {}} />
    </QueryClientProvider>
  );

  expect(screen.getByText(mockDrill.title)).toBeInTheDocument();
});
```

### Enforcement Guidelines

**All AI Agents MUST:**

1. **Follow Backend Contract:**
   - Use PascalCase for enum values (`'YouTube'`, not `'youtube'`)
   - Use snake_case for field names (`drill_tags`, not `drillTags`)
   - Never transform between camelCase and snake_case

2. **Use Path Aliases:**
   - Import from `@/lib/types`, never `../../lib/types`
   - Configure TypeScript and Vite with `@/*` → `./src/*` alias

3. **Export Props Interfaces:**
   - Every component exports its props interface separately
   - Pattern: `export interface ComponentNameProps { ... }`

4. **Use Centralized Config:**
   - Access env vars through `src/lib/config.ts`
   - Never use `import.meta.env` directly in components

5. **Define Routes Centrally:**
   - All routes in `src/routes.tsx`
   - Never inline routes in App.tsx or other components

6. **Handle Errors Consistently:**
   - Backend: Use structured error responses with code/message/details
   - Frontend: Rely on global QueryClient error handler, override locally when needed

7. **Manage ChromaDB Properly:**
   - Single collection: `"coaching_drills"`
   - Persist to `./chroma_data/` directory
   - Initialize on app startup, not on first use

8. **Integrate OpenAI Safely:**
   - Always use retry with exponential backoff (3 attempts)
   - Set timeouts: 30s (embeddings), 60s (LLM)
   - Graceful degradation on failure (log error, continue without AI)

9. **Respect Rate Limits:**
   - Check `can_call_llm()` before LLM API calls
   - Max 1 LLM call per 5 minutes
   - Record timestamp after successful call

10. **Invalidate Queries:**
    - After mutations, invalidate related queries
    - Pattern: `queryClient.invalidateQueries({ queryKey: ['content'] })`

### Pattern Verification

**How to Verify Patterns Are Followed:**

1. **Code Review Checklist:**
   - ✅ All imports use `@/` alias
   - ✅ Backend fields use snake_case
   - ✅ Enum values use PascalCase
   - ✅ Components export props interfaces
   - ✅ Env vars accessed through config
   - ✅ Routes defined in routes.tsx

2. **Type Safety Checks:**
   - TypeScript strict mode catches contract violations
   - Backend Pydantic models enforce field naming
   - Test failures indicate pattern violations

3. **Runtime Validation:**
   - Config file validates env vars at startup
   - ChromaDB collection name consistent across calls
   - Rate limiter enforces LLM call frequency

**Pattern Violation Documentation:**
- Document violations in implementation readiness report
- Track technical debt if patterns bypassed for pragmatic reasons
- Update patterns if better approach discovered during implementation

### Pattern Examples

**Good Examples:**

✅ **Component with exported props interface:**
```typescript
export interface DrillCardProps {
  drill: ContentItem;
  onClick: () => void;
}

export function DrillCard({ drill, onClick }: DrillCardProps) {
  return <div onClick={onClick}>{drill.title}</div>;
}
```

✅ **Form with object state matching API:**
```typescript
const [formData, setFormData] = useState({
  url: '',
  drill_description: '',
  drill_tags: []
});

createDrill.mutate(formData); // Direct pass
```

✅ **Query with invalidation:**
```typescript
const createDrill = useMutation({
  mutationFn: (data) => contentApi.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['content'] });
  }
});
```

✅ **Centralized env var access:**
```typescript
import { config } from '@/lib/config';
const apiUrl = config.apiUrl;
```

✅ **Structured error response:**
```python
raise_structured_error(
  code="RATE_LIMIT_EXCEEDED",
  message="LLM call rate limit exceeded (max 1 per 5 minutes)",
  status_code=429
)
```

**Anti-Patterns:**

❌ **Inline props without export:**
```typescript
function DrillCard(props: { drill: ContentItem }) { ... }
```

❌ **Individual field state:**
```typescript
const [url, setUrl] = useState('');
const [description, setDescription] = useState('');
```

❌ **Direct env var access:**
```typescript
const url = import.meta.env.VITE_API_URL;
```

❌ **Routes inline in App.tsx:**
```typescript
<Routes>
  <Route path="/" element={<Library />} />
</Routes>
```

❌ **Backend field name transformation:**
```typescript
// Don't transform snake_case to camelCase
const drillTags = data.drill_tags; // Just use drill_tags directly
```

❌ **Missing query invalidation:**
```typescript
// Mutation without invalidation = stale data
createDrill.mutate(data); // Missing onSuccess invalidation
```

## Project Structure & Boundaries

### Complete Directory Structure

**Frontend Structure (coaching-content-library-platform/frontend/):**

```
frontend/
├── public/                         # Static assets
│   └── vite.svg                   # Vite logo (default)
├── src/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components ONLY
│   │   │   ├── button.tsx         # Story 1.2 - shadcn Button
│   │   │   ├── card.tsx           # Story 1.2 - shadcn Card
│   │   │   ├── dialog.tsx         # Story 1.2 - shadcn Dialog
│   │   │   ├── input.tsx          # Story 1.2 - shadcn Input
│   │   │   ├── label.tsx          # Story 1.2 - shadcn Label
│   │   │   ├── select.tsx         # Story 1.2 - shadcn Select
│   │   │   ├── badge.tsx          # Story 1.2 - shadcn Badge
│   │   │   ├── toast.tsx          # Story 1.2 - shadcn Toast
│   │   │   └── toaster.tsx        # Story 1.2 - Toast container
│   │   ├── drills/                # Drill feature components
│   │   │   ├── DrillCard.tsx      # Story 2.1 - Individual drill card
│   │   │   ├── DrillGrid.tsx      # Story 2.2 - Responsive grid layout
│   │   │   └── DrillDetail.tsx    # Story 3.1 - Expandable detail sheet
│   │   ├── search/                # Search feature components
│   │   │   ├── SearchHero.tsx     # Story 5.1 - Search input UI
│   │   │   └── FilterBar.tsx      # Story 4.1 - Filter controls
│   │   ├── layout/                # Layout components
│   │   │   ├── Layout.tsx         # Story 1.3 - Root layout with Outlet
│   │   │   ├── Header.tsx         # Story 1.3 - Navigation header
│   │   │   └── Footer.tsx         # Story 1.3 - Optional footer
│   │   └── planner/               # Planner feature components
│   │       └── PlannerView.tsx    # Story 8.3 - Planner UI
│   ├── hooks/                     # Custom React hooks
│   │   ├── useContentList.ts      # Story 2.2 - List drill data fetching
│   │   ├── useContentItem.ts      # Story 3.1 - Single drill fetching
│   │   ├── useCreateContent.ts    # Story 8.2 - Create drill mutation
│   │   ├── useUpdateContent.ts    # Story 3.2 - Update drill mutation
│   │   ├── useDeleteContent.ts    # Story 3.3 - Delete drill mutation
│   │   ├── useSemanticSearch.ts   # Story 5.2 - Semantic search query
│   │   ├── useSimilarDrills.ts    # Story 6.1 - Similar drills query
│   │   └── useAutoTag.ts          # Story 7.2 - Auto-tag mutation
│   ├── lib/
│   │   ├── api.ts                 # Story 1.4 - Axios client setup
│   │   ├── types.ts               # Story 1.5 - Backend contract types
│   │   ├── utils.ts               # Story 1.2 - cn() helper
│   │   └── config.ts              # Story 1.1 - Env config
│   ├── pages/                     # Route pages
│   │   ├── Library.tsx            # Story 2.1 - Main library page
│   │   └── Planner.tsx            # Story 8.3 - Planner page
│   ├── routes.tsx                 # Story 1.3 - Route configuration
│   ├── App.tsx                    # Story 1.4 - Root with QueryClientProvider
│   └── main.tsx                   # Story 1.1 - Vite entry point
├── .env.development               # Story 1.1 - Local dev config
├── .env.production                # Post-implementation - Vercel config
├── .gitignore                     # Story 1.1 - Git ignore rules
├── index.html                     # Story 1.1 - Vite HTML template
├── package.json                   # Story 1.1 - Dependencies
├── tsconfig.json                  # Story 1.1 - TypeScript config
├── tsconfig.node.json             # Story 1.1 - Node TS config
├── vite.config.ts                 # Story 1.1 - Vite configuration
├── tailwind.config.js             # Story 1.2 - Tailwind config
├── postcss.config.js              # Story 1.2 - PostCSS config
├── eslint.config.js               # Story 1.1 - ESLint flat config
└── README.md                      # Story 1.1 - Project documentation
```

**Backend Structure (coaching-content-library-platform/backend/):**

```
backend/
├── src/
│   ├── api/                       # FastAPI routes
│   │   ├── __init__.py
│   │   ├── routes.py              # ✅ EXISTING - Main API routes
│   │   └── models.py              # ✅ EXISTING - API request/response models
│   ├── ingestors/                 # Platform fetchers
│   │   ├── __init__.py
│   │   ├── base.py                # ✅ EXISTING - BaseIngestor
│   │   ├── youtube.py             # ✅ EXISTING - YouTube API
│   │   ├── reddit.py              # ✅ EXISTING - Reddit API (PRAW)
│   │   ├── instagram.py           # ✅ EXISTING - Instagram fallback
│   │   └── tiktok.py              # ✅ EXISTING - TikTok fallback
│   ├── models/                    # Domain models
│   │   ├── __init__.py
│   │   ├── content.py             # ✅ EXISTING - ContentItem model
│   │   └── enums.py               # ✅ EXISTING - Source/Difficulty/AgeGroup
│   ├── storage/                   # Repository layer
│   │   ├── __init__.py
│   │   └── repository.py          # ✅ EXISTING - ContentRepository
│   ├── services/                  # 🔨 NEW - AI services
│   │   ├── __init__.py            # Story 5.2 - Service exports
│   │   ├── vector_service.py      # Story 5.2 - ChromaDB operations
│   │   ├── embedding_service.py   # Story 5.2 - OpenAI embeddings
│   │   ├── tagging_service.py     # Story 7.1 - OpenAI LLM tagging
│   │   └── recommendation_service.py  # Story 6.1 - Combined similarity
│   ├── bot/                       # Discord bot
│   │   ├── __init__.py
│   │   ├── bot.py                 # ✅ EXISTING - Discord bot main
│   │   └── commands.py            # ✅ EXISTING - Discord commands
│   └── main.py                    # ✅ EXISTING - FastAPI app entry
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_api.py                # ✅ EXISTING - API route tests
│   ├── test_ingestors.py          # ✅ EXISTING - Ingestor tests
│   ├── test_repository.py         # ✅ EXISTING - Repository tests
│   ├── test_vector_service.py     # Story 5.3 - Vector service tests
│   ├── test_embedding_service.py  # Story 5.3 - Embedding tests
│   ├── test_tagging_service.py    # Story 7.3 - Tagging tests
│   └── test_recommendation_service.py  # Story 6.2 - Recommendation tests
├── chroma_data/                   # 🔨 NEW - ChromaDB persistence
│   └── .gitkeep                   # Story 5.2 - Ensure dir tracked
├── .env                           # ✅ EXISTING - API keys
├── .gitignore                     # ✅ EXISTING - Git ignore
├── requirements.txt               # ✅ EXISTING + Story 5.2 - Add ChromaDB, OpenAI
├── pytest.ini                     # ✅ EXISTING - Pytest config
└── README.md                      # ✅ EXISTING - Backend docs
```

**Project Root Structure:**

```
coaching-content-library-platform/
├── frontend/                      # React SPA (see above)
├── backend/                       # FastAPI + Discord bot (see above)
├── _bmad/                         # ✅ EXISTING - BMAD workflows
├── _bmad-output/                  # ✅ EXISTING - Planning artifacts
│   ├── planning-artifacts/
│   │   ├── architecture.md        # ✅ THIS DOCUMENT
│   │   ├── prd.md                 # ✅ EXISTING
│   │   ├── epics.md               # ✅ EXISTING
│   │   ├── ux-design-specification.md  # ✅ EXISTING
│   │   └── product-brief-*.md     # ✅ EXISTING
│   └── implementation-artifacts/  # 🔨 For story tracking
├── docs/                          # ✅ EXISTING - Project knowledge
│   └── project-context.md         # ✅ EXISTING - 58 implementation rules
├── .git/                          # ✅ EXISTING - Git repository
└── README.md                      # ✅ EXISTING - Root project docs
```

### Epic → File Mapping

**Epic 1: Project Foundation & Core Infrastructure**
- **Files Created:**
  - `frontend/package.json` - Dependencies (Story 1.1)
  - `frontend/vite.config.ts` - Vite config with proxy (Story 1.1)
  - `frontend/tailwind.config.js` - Tailwind theme (Story 1.2)
  - `frontend/src/lib/config.ts` - Env config (Story 1.1)
  - `frontend/src/lib/utils.ts` - cn() helper (Story 1.2)
  - `frontend/src/components/ui/*.tsx` - shadcn components (Story 1.2)
  - `frontend/src/routes.tsx` - Route definitions (Story 1.3)
  - `frontend/src/App.tsx` - QueryClientProvider setup (Story 1.4)
  - `frontend/src/lib/api.ts` - Axios client (Story 1.4)
  - `frontend/src/lib/types.ts` - Backend contract types (Story 1.5)
- **Related NFRs:** NFR1 (page load <3s), NFR22 (deployment), NFR33 (HTTPS)

**Epic 2: Drill Library Browsing & Display**
- **Files Created:**
  - `frontend/src/components/drills/DrillCard.tsx` - Individual drill card (Story 2.1)
  - `frontend/src/components/drills/DrillGrid.tsx` - Responsive grid (Story 2.2)
  - `frontend/src/hooks/useContentList.ts` - List data fetching (Story 2.2)
  - `frontend/src/pages/Library.tsx` - Main library page (Story 2.1)
- **Related FRs:** FR34-FR38 (library grid, drill cards, thumbnails, mobile support)
- **Related NFRs:** NFR1 (page load), NFR4 (progressive loading)
- **Backend Integration:** `GET /api/v1/content` (existing)

**Epic 3: Drill Detail View & Management**
- **Files Created:**
  - `frontend/src/components/drills/DrillDetail.tsx` - Detail sheet (Story 3.1)
  - `frontend/src/hooks/useContentItem.ts` - Single drill fetching (Story 3.1)
  - `frontend/src/hooks/useUpdateContent.ts` - Update mutation (Story 3.2)
  - `frontend/src/hooks/useDeleteContent.ts` - Delete mutation (Story 3.3)
- **Related FRs:** FR10-FR15 (view, edit, delete, tag management)
- **Related NFRs:** NFR2 (instant detail view)
- **Backend Integration:**
  - `GET /api/v1/content/{id}` (existing)
  - `PUT /api/v1/content/{id}` (existing)
  - `DELETE /api/v1/content/{id}` (existing)

**Epic 4: Advanced Filtering System**
- **Files Created:**
  - `frontend/src/components/search/FilterBar.tsx` - Filter UI (Story 4.1)
  - Enhanced `frontend/src/hooks/useContentList.ts` - Add filter params (Story 4.2)
- **Related FRs:** FR20-FR25 (filter by tags, difficulty, age group, equipment)
- **Related NFRs:** NFR3 (filter <500ms)
- **Backend Integration:** `GET /api/v1/content?tags=...&difficulty=...` (existing)

**Epic 5: Semantic Search**
- **Files Created:**
  - `frontend/src/components/search/SearchHero.tsx` - Search UI (Story 5.1)
  - `frontend/src/hooks/useSemanticSearch.ts` - Search query hook (Story 5.1)
  - `backend/src/services/vector_service.py` - ChromaDB operations (Story 5.2)
  - `backend/src/services/embedding_service.py` - OpenAI embeddings (Story 5.2)
  - `backend/tests/test_vector_service.py` - Vector tests (Story 5.3)
  - `backend/tests/test_embedding_service.py` - Embedding tests (Story 5.3)
  - Enhanced `backend/src/api/routes.py` - Add `/api/v1/search` endpoint (Story 5.2)
- **Related FRs:** FR17-FR18 (semantic search)
- **Related NFRs:** NFR2 (search <2s), NFR13 (embedding API)
- **Backend Integration:** `POST /api/v1/search` (new endpoint)
- **External Dependencies:** OpenAI embeddings API, ChromaDB

**Epic 6: Similar Drill Recommendations**
- **Files Created:**
  - `frontend/src/hooks/useSimilarDrills.ts` - Similar drills query (Story 6.1)
  - `backend/src/services/recommendation_service.py` - Combined similarity (Story 6.1)
  - `backend/tests/test_recommendation_service.py` - Recommendation tests (Story 6.2)
  - Enhanced `backend/src/api/routes.py` - Add `/api/v1/content/{id}/similar` (Story 6.1)
- **Related FRs:** FR31-FR33 (tag similarity, semantic similarity, recommendations)
- **Related NFRs:** NFR5 (instant recommendations)
- **Backend Integration:** `GET /api/v1/content/{id}/similar` (new endpoint)
- **Dependencies:** ChromaDB vectors, tag-based Jaccard similarity

**Epic 7: AI-Powered Auto-Tagging**
- **Files Created:**
  - `frontend/src/hooks/useAutoTag.ts` - Auto-tag mutation (Story 7.2)
  - `backend/src/services/tagging_service.py` - OpenAI LLM tagging (Story 7.1)
  - `backend/tests/test_tagging_service.py` - Tagging tests (Story 7.3)
  - Enhanced `backend/src/api/routes.py` - Add `/api/v1/content/{id}/auto-tag` (Story 7.1)
- **Related FRs:** FR26-FR29 (auto-tagging, rate limiting, augmentation)
- **Related NFRs:** NFR12 (LLM integration), NFR15 (cost management)
- **Backend Integration:** `POST /api/v1/content/{id}/auto-tag` (new endpoint)
- **External Dependencies:** OpenAI GPT-4o-mini API
- **Rate Limiting:** 1 call per 5 minutes (in-memory tracking)

**Epic 8: Web-Based Drill Capture**
- **Files Created:**
  - `frontend/src/components/drills/AddDrillModal.tsx` - Add drill form (Story 8.2)
  - `frontend/src/hooks/useCreateContent.ts` - Create mutation (Story 8.2)
  - `frontend/src/pages/Planner.tsx` - Planner page (Story 8.3)
  - `frontend/src/components/planner/PlannerView.tsx` - Planner UI (Story 8.3)
- **Related FRs:** FR1-FR9 (URL submission, metadata collection, platform support)
- **Related NFRs:** NFR6-NFR11 (platform API integration)
- **Backend Integration:** `POST /api/v1/content` (existing endpoint)

### Architectural Boundaries

**API Boundary (Backend ↔ Frontend):**

**Contract:**
- **Protocol:** REST over HTTPS
- **Base URL:** `https://your-domain.com/api/v1` (production), `http://localhost:8000/api/v1` (dev)
- **Content-Type:** `application/json`
- **Field Naming:** snake_case (`drill_tags`, `drill_description`)
- **Enum Values:** PascalCase (`'YouTube'`, `'Beginner'`)
- **Nullables:** Use `null` (not `undefined`)

**Endpoints:**
- `GET /api/v1/content` - List drills with optional filters
- `GET /api/v1/content/{id}` - Get single drill
- `POST /api/v1/content` - Create new drill
- `PUT /api/v1/content/{id}` - Update drill
- `DELETE /api/v1/content/{id}` - Delete drill
- `POST /api/v1/search` - Semantic search (NEW)
- `GET /api/v1/content/{id}/similar` - Similar drills (NEW)
- `POST /api/v1/content/{id}/auto-tag` - Trigger auto-tagging (NEW)

**Error Format:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

**CORS Policy:**
- Allowed origin: `https://yourusername.vercel.app` (or custom domain)
- Allowed methods: GET, POST, PUT, DELETE
- Allowed headers: Content-Type, Authorization
- Configured in FastAPI middleware

**Component Boundary (React Components):**

**Communication Pattern:**
- **Parent → Child:** Props (typed interfaces)
- **Child → Parent:** Callback functions via props
- **Server State:** TanStack Query hooks (useContentList, useContentItem)
- **UI State:** React hooks (useState, useReducer)

**Props Interface Rule:**
- Every component MUST export its props interface separately
- Pattern: `export interface ComponentNameProps { ... }`
- Enables type reusability and better autocomplete

**Component Hierarchy:**
```
App (QueryClientProvider)
└── Layout (Header + Outlet + Footer)
    ├── Library Page
    │   ├── SearchHero (search input)
    │   ├── FilterBar (filter controls)
    │   └── DrillGrid
    │       └── DrillCard (repeats)
    │           └── DrillDetail (dialog)
    └── Planner Page
        └── PlannerView
            └── AddDrillModal (dialog)
```

**Service Boundary (Backend Services):**

**Service Responsibilities:**

**Vector Service (`vector_service.py`):**
- ChromaDB client initialization and persistence
- Collection management (`"coaching_drills"` collection)
- Vector storage (add, update, delete embeddings)
- Vector similarity queries (cosine similarity)
- Maps ChromaDB IDs to SQLite drill IDs

**Embedding Service (`embedding_service.py`):**
- OpenAI API integration for embeddings
- text-embedding-3-small model (1536 dimensions)
- Retry logic with exponential backoff (3 attempts)
- Timeout: 30 seconds
- Graceful degradation on failure

**Tagging Service (`tagging_service.py`):**
- OpenAI API integration for LLM tagging
- GPT-4o-mini model
- Rate limiting enforcement (1 call per 5 minutes)
- Retry logic with exponential backoff (3 attempts)
- Timeout: 60 seconds
- Graceful degradation on failure
- Never overwrites user-provided tags (augments only)

**Recommendation Service (`recommendation_service.py`):**
- Combines tag-based similarity (Jaccard) and semantic similarity (vector cosine)
- Weighted scoring algorithm
- Returns top N similar drills with scores
- Depends on Vector Service for semantic similarity

**Service Dependencies:**
```
API Routes
  ↓
Recommendation Service → Vector Service → ChromaDB
  ↓                       ↓
Tagging Service         Embedding Service → OpenAI API
  ↓
Repository → SQLite
```

**Data Boundary (Persistence Layer):**

**SQLite Database (Main Data):**
- **Location:** `backend/drill_library.db` (existing)
- **Schema:** ContentItem model with drill metadata
- **Fields:** id (PK), source, url, title, drill_description, drill_tags, difficulty, age_group, equipment, thumbnail_url, published_at, created_at, updated_at
- **Access:** ContentRepository only (no direct SQL in routes)
- **Transactions:** Managed by SQLAlchemy sessions

**ChromaDB (Vector Data):**
- **Location:** `backend/chroma_data/` directory
- **Collection:** Single collection `"coaching_drills"`
- **Schema:** Vector embeddings (1536 dimensions) with metadata
- **Document IDs:** Map to SQLite drill primary keys (string conversion)
- **Access:** Vector Service only
- **Persistence:** Automatic on disk write
- **Initialization:** On app startup (get_or_create_collection)

**Data Flow:**
```
Discord Bot → SQLite (via Repository)
                ↓
Web UI → FastAPI → Repository → SQLite
                ↓                 ↓
          Embedding Service   (read drill)
                ↓
          Vector Service → ChromaDB
                ↓
          (store embeddings)
```

**State Management Boundary (Frontend):**

**Server State (TanStack Query):**
- Managed by QueryClient with 5-minute stale time
- Query keys: `['content']`, `['content', id]`, `['content', id, 'similar']`
- Automatic cache invalidation after mutations
- Retry: 1 attempt for queries
- Global error handling with component-level override

**UI State (React Hooks):**
- Form input values
- Modal open/closed states
- Hover/focus states
- Filter selection (client-side only until applied)
- Search input (debounced before query)

**URL State (React Router):**
- Current route (/, /planner)
- No query params for state (use TanStack Query instead)

### Integration Points

**Integration Point 1: Discord Bot → SQLite**
- **Status:** ✅ EXISTING AND OPERATIONAL
- **Flow:** Discord command → Ingestor (YouTube/Reddit/Instagram/TikTok) → Repository → SQLite
- **Contract:** ContentItem model with snake_case fields, PascalCase enums
- **Error Handling:** Discord bot sends error messages to user in Discord channel
- **Impact:** Web UI reads drills created by Discord bot immediately (same database)

**Integration Point 2: Frontend → Backend API**
- **Status:** 🔨 TO BE IMPLEMENTED (API exists, frontend connects in Epic 1)
- **Flow:** React component → TanStack Query hook → Axios → FastAPI endpoint → Repository → SQLite
- **Protocol:** REST over HTTPS (Vercel → Caddy → FastAPI)
- **Error Handling:** Structured error responses, global QueryClient handler, user-friendly toasts
- **CORS:** FastAPI allows Vercel origin
- **Environment:** `VITE_API_URL` env var in frontend config

**Integration Point 3: Backend → OpenAI API (Embeddings)**
- **Status:** 🔨 TO BE IMPLEMENTED (Epic 5)
- **Flow:** Drill save event → Embedding Service → OpenAI API → Vector Service → ChromaDB
- **Model:** text-embedding-3-small (1536 dimensions)
- **Rate Limiting:** None required (embeddings API has generous limits)
- **Cost Management:** Cache embeddings in ChromaDB, never regenerate
- **Error Handling:** Retry 3x with exponential backoff, graceful degradation (log error, continue without embeddings)
- **API Key:** `OPENAI_API_KEY` env var in backend

**Integration Point 4: Backend → OpenAI API (LLM)**
- **Status:** 🔨 TO BE IMPLEMENTED (Epic 7)
- **Flow:** User triggers auto-tag → Tagging Service checks rate limit → OpenAI API → Augment drill_tags
- **Model:** GPT-4o-mini
- **Rate Limiting:** 1 call per 5 minutes (in-memory timestamp tracking)
- **Cost Management:** Rate limiting prevents runaway costs
- **Error Handling:** Retry 3x with exponential backoff, graceful degradation (user tags still saved)
- **API Key:** `OPENAI_API_KEY` env var in backend

**Integration Point 5: Backend → ChromaDB**
- **Status:** 🔨 TO BE IMPLEMENTED (Epic 5)
- **Flow:** Embedding generated → Vector Service → ChromaDB collection → Persist to disk
- **Collection:** Single collection `"coaching_drills"`
- **Persistence:** `./chroma_data/` directory
- **Initialization:** On app startup (get_or_create_collection)
- **Query:** Semantic search → Generate query embedding → ChromaDB similarity search → Return drill IDs → Fetch from SQLite
- **Error Handling:** ChromaDB failures logged, semantic search unavailable (fallback to tag filtering)

**Integration Point 6: Vercel (Frontend) → Proxmox (Backend)**
- **Status:** 🔨 TO BE CONFIGURED (Post-implementation)
- **Flow:** User browser → Vercel CDN (React SPA) → User action → Axios request → Caddy (Proxmox) → FastAPI
- **HTTPS:** Both sides (Vercel automatic, Caddy Let's Encrypt)
- **Domain:** Dynamic DNS pointing to Proxmox public IP
- **CORS:** FastAPI allows Vercel domain origin
- **Environment:** Frontend `VITE_API_URL` points to Proxmox dynamic DNS domain
- **Deployment:**
  - Frontend: Git push → Vercel automatic deploy
  - Backend: Manual deploy on Proxmox (systemd service or similar)

**Integration Point 7: FastAPI → SQLite + ChromaDB (Dual Database)**
- **Status:** 🔨 PARTIAL (SQLite exists, ChromaDB to be added in Epic 5)
- **Flow:**
  - **Write:** Drill created → Save to SQLite → Generate embedding → Save to ChromaDB
  - **Read:** Search query → Query ChromaDB for IDs → Fetch drills from SQLite by IDs
  - **Delete:** Drill deleted → Delete from SQLite → Delete from ChromaDB
- **Consistency:** Application-level consistency (no distributed transactions)
- **Error Handling:** If ChromaDB write fails, log error but commit to SQLite (core data preserved)

### File Responsibility Matrix

**Frontend Files:**

| File | Epic | Stories | Responsibilities |
|------|------|---------|------------------|
| `src/lib/config.ts` | 1 | 1.1 | Centralized env var config, validation |
| `src/lib/types.ts` | 1 | 1.5 | Backend contract TypeScript types |
| `src/lib/api.ts` | 1 | 1.4 | Axios client, request/response interceptors |
| `src/lib/utils.ts` | 1 | 1.2 | cn() helper, utility functions |
| `src/routes.tsx` | 1 | 1.3 | Centralized route configuration |
| `src/App.tsx` | 1 | 1.4 | QueryClientProvider, router setup |
| `src/components/ui/*.tsx` | 1 | 1.2 | shadcn/ui components (Button, Card, Dialog, etc.) |
| `src/components/drills/DrillCard.tsx` | 2 | 2.1 | Individual drill card display, thumbnail, metadata |
| `src/components/drills/DrillGrid.tsx` | 2 | 2.2 | Responsive grid layout, loading states |
| `src/components/drills/DrillDetail.tsx` | 3 | 3.1 | Expandable detail sheet, full metadata display |
| `src/components/search/SearchHero.tsx` | 5 | 5.1 | Search input, debouncing, query submission |
| `src/components/search/FilterBar.tsx` | 4 | 4.1 | Filter controls, tag/difficulty/age group selection |
| `src/components/planner/PlannerView.tsx` | 8 | 8.3 | Planner page layout, drill capture UI |
| `src/hooks/useContentList.ts` | 2, 4 | 2.2, 4.2 | List drill fetching, filtering, TanStack Query |
| `src/hooks/useContentItem.ts` | 3 | 3.1 | Single drill fetching, TanStack Query |
| `src/hooks/useCreateContent.ts` | 8 | 8.2 | Create drill mutation, cache invalidation |
| `src/hooks/useUpdateContent.ts` | 3 | 3.2 | Update drill mutation, cache invalidation |
| `src/hooks/useDeleteContent.ts` | 3 | 3.3 | Delete drill mutation, cache invalidation |
| `src/hooks/useSemanticSearch.ts` | 5 | 5.1 | Semantic search query, TanStack Query |
| `src/hooks/useSimilarDrills.ts` | 6 | 6.1 | Similar drills query, TanStack Query |
| `src/hooks/useAutoTag.ts` | 7 | 7.2 | Auto-tag mutation, rate limit handling |
| `src/pages/Library.tsx` | 2 | 2.1 | Main library page, composition of grid/search/filter |
| `src/pages/Planner.tsx` | 8 | 8.3 | Planner page, composition of planner view |

**Backend Files:**

| File | Epic | Stories | Responsibilities |
|------|------|---------|------------------|
| `src/services/vector_service.py` | 5 | 5.2 | ChromaDB client, collection management, vector CRUD |
| `src/services/embedding_service.py` | 5 | 5.2 | OpenAI embeddings API, retry logic, timeouts |
| `src/services/tagging_service.py` | 7 | 7.1 | OpenAI LLM API, rate limiting, tag generation |
| `src/services/recommendation_service.py` | 6 | 6.1 | Combined similarity scoring, ranking algorithm |
| `src/api/routes.py` | 5, 6, 7 | 5.2, 6.1, 7.1 | Add new endpoints: /search, /similar, /auto-tag |
| `tests/test_vector_service.py` | 5 | 5.3 | Unit tests for vector service with mocked ChromaDB |
| `tests/test_embedding_service.py` | 5 | 5.3 | Unit tests for embedding service with mocked OpenAI |
| `tests/test_tagging_service.py` | 7 | 7.3 | Unit tests for tagging service, rate limit validation |
| `tests/test_recommendation_service.py` | 6 | 6.2 | Unit tests for recommendation service, scoring validation |
| `requirements.txt` | 5 | 5.2 | Add: chromadb, openai, tenacity |

**Existing Files (No Changes Required):**
- `src/bot/bot.py` - Discord bot (continues to operate independently)
- `src/ingestors/*.py` - Platform ingestors (used by Discord bot and web UI)
- `src/models/content.py` - ContentItem model (no changes)
- `src/storage/repository.py` - Repository (minimal changes for AI service integration)

### Cross-Epic Dependencies

**Dependency Graph:**

```
Epic 1 (Foundation)
  ↓ (BLOCKS ALL OTHER EPICS)
Epic 2 (Library Browsing) ←┐
  ↓                         │
Epic 3 (Detail View)        │
  ↓                         │
Epic 4 (Filtering) ─────────┘
  ↓ (parallel)
  ├─→ Epic 5 (Semantic Search) → Epic 6 (Recommendations)
  │                                    ↓
  └─→ Epic 7 (Auto-Tagging) ──────────┘
                                       ↓
                                Epic 8 (Web Capture)
```

**Critical Path:**
1. **Epic 1** must be completed first (foundation for all frontend work)
2. **Epic 2** depends on Epic 1 (needs QueryClient, API client, types)
3. **Epic 3** depends on Epic 2 (needs DrillCard for detail trigger)
4. **Epic 4** can proceed after Epic 2 (parallel with Epic 3)
5. **Epic 5** depends on Epic 1 (needs API client, config) - can be parallel with Epics 2-4
6. **Epic 6** depends on Epic 5 (needs vector service and embeddings)
7. **Epic 7** depends on Epic 1 (needs API client) - can be parallel with Epics 2-6
8. **Epic 8** can proceed after Epic 1 (needs form components, API client) - parallel with Epics 2-7

**Recommended Implementation Order:**
1. Epic 1 (Foundation) - **REQUIRED FIRST**
2. Epic 2 (Library Browsing) + Epic 5 Story 5.2 (Backend AI services setup) - **PARALLEL**
3. Epic 3 (Detail View) + Epic 5 Story 5.1 (Frontend search UI) - **PARALLEL**
4. Epic 4 (Filtering) + Epic 6 (Recommendations) - **PARALLEL**
5. Epic 7 (Auto-Tagging) + Epic 8 (Web Capture) - **PARALLEL**

### Architecture Validation Checklist

**Completeness Check:**
- ✅ All 8 epics mapped to specific files
- ✅ All 50 FRs covered by file responsibilities
- ✅ All 36 NFRs addressed in boundaries and integration points
- ✅ Frontend directory structure complete
- ✅ Backend directory structure complete
- ✅ All new endpoints documented
- ✅ All external dependencies identified (OpenAI, ChromaDB)
- ✅ All integration points documented (6 total)

**Consistency Check:**
- ✅ Backend contract preserved (snake_case fields, PascalCase enums)
- ✅ All 58 rules from project-context.md incorporated
- ✅ 7 additional patterns defined and mapped to files
- ✅ Path alias (@/) used consistently
- ✅ Props interfaces exported for all components
- ✅ Centralized config pattern enforced
- ✅ Routes defined centrally in routes.tsx
- ✅ Error handling consistent (structured errors)

**Implementation Readiness:**
- ✅ No blocking architectural decisions remain
- ✅ All technology choices finalized (Vite, ChromaDB, OpenAI, Vercel, Caddy)
- ✅ Deployment strategy clear (hybrid Vercel + Proxmox)
- ✅ Development workflow defined (proxy, env vars, testing)
- ✅ Epic dependencies documented (critical path identified)
- ✅ File responsibilities unambiguous (no overlap or gaps)
- ✅ Integration points explicit (protocols, error handling, CORS)

**AI Agent Alignment:**
- ✅ All patterns documented for preventing conflicts
- ✅ File structure explicit (no ambiguous directory placement)
- ✅ Backend contract rules repeated throughout document
- ✅ Testing patterns defined for all new services
- ✅ Error handling patterns consistent across stack

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**

All technology choices work together without conflicts:
- React 19.2.0 + Vite 7.2.4: Official compatibility, modern tooling
- TypeScript 5.9.3: Compatible with all libraries (React 19, TanStack Query 5.90.16, Axios 1.13.2)
- FastAPI + SQLite + ChromaDB: Python-native stack, no version conflicts
- OpenAI API: Single provider for embeddings + LLM simplifies key management
- Vercel + Proxmox: Hybrid architecture with clear separation (static frontend, dynamic backend)
- Caddy reverse proxy: Automatic HTTPS, simple configuration

**Pattern Consistency:**

Implementation patterns fully support architectural decisions:
- Backend contract enforcement (PascalCase enums, snake_case fields) maintained across all layers
- Structured error responses consistent from FastAPI through TanStack Query global handler
- Component pattern (exported props interfaces) enforced for all React components
- Centralized configuration (backend .env, frontend config.ts) aligns with deployment strategy
- AI service patterns (retry + timeout + graceful degradation) consistent across OpenAI calls
- Query invalidation pattern ensures cache consistency after mutations

**Structure Alignment:**

Project structure fully enables architectural decisions:
- Feature-based frontend directories (drills/, search/, planner/) align with epic organization
- Backend service layer added cleanly without disrupting existing ingestors/repository patterns
- All 7 integration points properly structured with explicit protocols
- 5 architectural boundaries (API, Component, Service, Data, State) clearly defined and non-overlapping
- Dual database strategy (SQLite + ChromaDB) supported by file structure (chroma_data/ directory)

### Requirements Coverage Validation ✅

**Epic Coverage:**

All 8 epics have complete architectural support:
- **Epic 1 (Foundation):** 15 files for Vite setup, Tailwind, shadcn/ui, QueryClient, API client, types
- **Epic 2 (Library Browsing):** 4 files for DrillCard, DrillGrid, useContentList, Library page
- **Epic 3 (Detail View):** 4 files for DrillDetail, useContentItem, update/delete hooks
- **Epic 4 (Filtering):** 2 files for FilterBar, enhanced useContentList with filter params
- **Epic 5 (Semantic Search):** 6 files for SearchHero, vector/embedding services, tests, /search endpoint
- **Epic 6 (Recommendations):** 3 files for useSimilarDrills, recommendation_service, /similar endpoint
- **Epic 7 (Auto-Tagging):** 3 files for useAutoTag, tagging_service with rate limiting, /auto-tag endpoint
- **Epic 8 (Web Capture):** 4 files for AddDrillModal, useCreateContent, Planner page

Cross-epic dependencies documented with critical path and parallelization opportunities.

**Functional Requirements Coverage (50 FRs):**

All functional requirements architecturally supported:
- **FR1-FR9 (Content Capture):** Existing Discord bot + new web UI (Epic 8) with platform ingestors
- **FR10-FR15 (Management):** Epic 3 provides detail view with edit/delete mutations, query invalidation
- **FR16-FR25 (Discovery):** Epic 4 filtering (tags, difficulty, age_group) + Epic 5 semantic search
- **FR26-FR33 (AI Organization):** Epic 7 auto-tagging with rate limiting + Epic 6 combined recommendations
- **FR34-FR41 (Viewing):** Epic 2 library browsing with responsive grid, drill cards, lazy loading
- **FR42-FR50 (Metadata):** Backend contract enforces structured fields, enums, timestamps

**Non-Functional Requirements Coverage (36 NFRs):**

All non-functional requirements addressed:
- **NFR1-NFR5 (Performance):** TanStack Query caching (5 min stale time), lazy loading, 300ms debouncing, <3s page load, <2s search, <500ms filter
- **NFR6-NFR21 (Integration):** 4 platform ingestors (YouTube, Reddit, Instagram, TikTok) existing, OpenAI API with retry/timeout/graceful degradation, Discord bot operational
- **NFR22-NFR30 (Reliability):** Vercel + Proxmox deployment for portfolio presentation, backend contract enforcement via TypeScript strict mode, dual database with application-level consistency
- **NFR31-NFR36 (Security):** HTTPS enforced (Vercel automatic, Caddy Let's Encrypt), env vars for API keys, CORS policy allows only Vercel domain, input validation in FastAPI

### Implementation Readiness Validation ✅

**Decision Completeness:**

All critical architectural decisions documented with full context:
- ✅ 9 core decisions made (vector DB, embeddings API, LLM API, frontend hosting, backend hosting, reverse proxy, error format, rate limiting, API versioning)
- ✅ All decisions include rationale, affects analysis, and implementation notes
- ✅ Technology versions specified: React 19.2.0, Vite 7.2.4, TypeScript 5.9.3, TanStack Query 5.90.16, FastAPI 0.104.0+, Python 3.12
- ✅ External dependencies identified: OpenAI API (embeddings + LLM), ChromaDB, platform APIs (YouTube, Reddit, Instagram, TikTok)
- ✅ Cost management documented: OpenAI estimated <$0.01 for MVP with 50 drills
- ✅ Code examples provided for all major patterns (13+ examples in Implementation Patterns section)

**Structure Completeness:**

Project structure fully specified with no ambiguity:
- ✅ Complete directory tree: Frontend 30+ files, backend 10+ new files
- ✅ All files explicitly listed (no placeholder "etc." or "additional files")
- ✅ Epic → File mapping: Every file mapped to specific epic and story
- ✅ File responsibility matrix: 29 files with epic/story/responsibility assignments
- ✅ Existing files marked: Clear distinction between ✅ EXISTING and 🔨 NEW files
- ✅ Integration points explicit: 7 integration points with protocols, error handling, CORS policy
- ✅ Boundaries well-defined: 5 boundary types (API, Component, Service, Data, State) with clear communication rules

**Pattern Completeness:**

Implementation patterns comprehensive enough to prevent AI agent conflicts:
- ✅ 58 existing rules from project-context.md fully incorporated
- ✅ 7 new patterns defined for conflict-prone areas: Component structure (exported props), Form state (form object), TanStack Query (global error handler), Env config (centralized), Routes (routes.tsx file), ChromaDB (single collection), OpenAI (retry + timeout)
- ✅ Backend contract enforcement throughout: PascalCase enums (`'YouTube'`), snake_case fields (`drill_tags`)
- ✅ Good/Bad examples: 6 good examples + 6 anti-patterns documented
- ✅ Enforcement guidelines: 10 must-follow rules for all AI agents
- ✅ Pattern verification: Code review checklist, type safety checks, runtime validation

### Gap Analysis Results

**Critical Gaps:** ✅ None identified

All blocking architectural decisions have been made:
- Technology stack fully specified with versions
- Deployment strategy clear (Vercel + Proxmox)
- AI services integrated (ChromaDB, OpenAI embeddings, OpenAI LLM)
- Error handling patterns consistent
- Backend contract enforced throughout

**Important Gaps:** ✅ None identified

All epics have clear implementation paths:
- Every epic mapped to specific files
- All integration points documented
- All external dependencies identified
- Cross-epic dependencies with critical path defined

**Nice-to-Have Enhancements (Post-MVP):**

These are explicitly deferred and documented in "Deferred Decisions" section:
- Database migration strategy (simple SQLite schema, migrations can wait)
- CI/CD pipeline automation (manual deploys acceptable initially)
- Monitoring/logging infrastructure (local access sufficient for personal use)
- Redis for distributed rate limiting (in-memory adequate for single user)
- Database connection pooling (SQLite doesn't benefit from pooling)

### Validation Issues Addressed

**No Critical Issues Found**

The architecture is coherent, complete, and ready for implementation.

**Minor Documentation Enhancements (Non-blocking):**

1. **OpenAI API Key Management:**
   - Current: Documents .env for credentials
   - Enhancement: Could emphasize key rotation for production use
   - Impact: None for MVP (personal use, private repo)
   - Status: Acceptable as-is

2. **ChromaDB Backup Strategy:**
   - Current: SQLite backups documented
   - Enhancement: Consider documenting chroma_data/ directory backup alongside SQLite
   - Impact: Low (vectors can be regenerated from SQLite data)
   - Status: Can be added during implementation

3. **Vercel Deployment Instructions:**
   - Current: Build command and output directory specified
   - Enhancement: Could add explicit Vercel project setup steps in implementation handoff
   - Impact: None (Vercel auto-detects Vite projects)
   - Status: Can be added in implementation artifacts

**Resolution:** These are documentation improvements that don't block implementation. They can be addressed during implementation or post-MVP as needed.

### Architecture Completeness Checklist

**✅ Requirements Analysis**

- [x] Project context thoroughly analyzed (50 FRs, 36 NFRs, 8 epics)
- [x] Scale and complexity assessed (Medium complexity, full-stack web app, AI integration)
- [x] Technical constraints identified (Existing Discord bot, backend contract, technology stack)
- [x] Cross-cutting concerns mapped (Backend contract enforcement, AI service integration, performance optimization, error handling, data flow, testing strategy)

**✅ Architectural Decisions**

- [x] Critical decisions documented with versions (9 core decisions with rationale)
- [x] Technology stack fully specified (React 19.2.0, Vite 7.2.4, TypeScript 5.9.3, TanStack Query 5.90.16, FastAPI 0.104.0+, Python 3.12, ChromaDB, OpenAI)
- [x] Integration patterns defined (7 integration points with protocols)
- [x] Performance considerations addressed (Caching, lazy loading, debouncing, timeouts)

**✅ Implementation Patterns**

- [x] Naming conventions established (Backend contract PascalCase/snake_case, component PascalCase, files camelCase)
- [x] Structure patterns defined (Feature-based directories, service layer, component hierarchy)
- [x] Communication patterns specified (Props, callbacks, TanStack Query, structured errors)
- [x] Process patterns documented (Error handling, retry logic, rate limiting, query invalidation)

**✅ Project Structure**

- [x] Complete directory structure defined (Frontend 30+ files, backend 10+ new files)
- [x] Component boundaries established (API, Component, Service, Data, State)
- [x] Integration points mapped (7 integration points with detailed specifications)
- [x] Requirements to structure mapping complete (Epic → File mapping, File Responsibility Matrix)

### Architecture Readiness Assessment

**Overall Status:** ✅ READY FOR IMPLEMENTATION

**Confidence Level:** HIGH

Based on validation results:
- All 8 epics have complete architectural support
- All 50 FRs and 36 NFRs architecturally covered
- No critical gaps or blocking issues identified
- 65 implementation patterns (58 existing + 7 new) prevent AI agent conflicts
- Complete project structure with explicit file mappings
- All technology decisions made with versions specified
- Integration points fully documented with protocols

**Key Strengths:**

1. **Backend Already Operational:** Discord bot + SQLite + ingestors already functional, reducing implementation risk
2. **Clear Separation of Concerns:** Feature-based organization (drills/, search/, planner/) aligns with epic structure
3. **Backend Contract Enforcement:** PascalCase enums + snake_case fields maintained throughout all layers prevents type mismatches
4. **Dual Database Strategy:** SQLite for structured data + ChromaDB for vectors with clear separation and application-level consistency
5. **Hybrid Deployment:** Vercel (frontend) + Proxmox (backend) leverages existing infrastructure while maintaining professional portfolio URL
6. **AI Services Integration:** OpenAI single provider for embeddings + LLM with retry + timeout + graceful degradation
7. **Comprehensive Patterns:** 65 total patterns (58 existing + 7 new) with good/bad examples prevent AI agent conflicts
8. **Complete File Mapping:** Every epic mapped to specific files with responsibilities, no ambiguity

**Areas for Future Enhancement:**

1. **CI/CD Automation:** Currently manual deploys, could add GitHub Actions for Vercel + Proxmox automated deployment
2. **Monitoring/Observability:** Could add structured logging, error tracking (Sentry), performance monitoring (Vercel Analytics)
3. **Database Migrations:** Could add Alembic for SQLAlchemy schema migrations as complexity grows
4. **Rate Limiting Evolution:** Could upgrade from in-memory to Redis-backed for distributed rate limiting if needed
5. **Testing Infrastructure:** Frontend testing framework (Vitest + React Testing Library) specified but not yet implemented
6. **Performance Optimization:** Could add more aggressive caching strategies (service worker, edge caching) if NFR targets aren't met

These enhancements are non-critical and can be addressed post-MVP based on actual usage patterns and performance metrics.

### Implementation Handoff

**AI Agent Guidelines:**

1. **Follow Architectural Decisions Exactly:**
   - Use specified versions: React 19.2.0, Vite 7.2.4, TypeScript 5.9.3, TanStack Query 5.90.16
   - Implement patterns as documented (no improvisation)
   - Respect backend contract (PascalCase enums, snake_case fields)
   - Use centralized config (src/lib/config.ts) for all env vars

2. **Use Implementation Patterns Consistently:**
   - Export props interfaces for all components (`export interface ComponentNameProps`)
   - Use form object state matching API payload structure
   - Apply global QueryClient error handling with component-level override
   - Define routes in routes.tsx, never inline
   - Use path alias (@/) for all imports

3. **Respect Project Structure:**
   - Place components in feature directories (drills/, search/, planner/)
   - shadcn/ui components ONLY in components/ui/
   - Backend services in services/ (vector_service, embedding_service, tagging_service, recommendation_service)
   - Tests mirror src/ structure

4. **Respect Boundaries:**
   - API calls only through Axios client in lib/api.ts
   - Server state only through TanStack Query hooks
   - ChromaDB access only through vector_service.py
   - OpenAI API calls only through embedding_service.py and tagging_service.py

5. **Refer to This Document:**
   - For all architectural questions, consult this document first
   - Follow code examples in Implementation Patterns section
   - Use File Responsibility Matrix to understand file purposes
   - Check Integration Points for cross-system communication protocols

**First Implementation Priority:**

Epic 1, Story 1.1: Frontend Project Setup using Vite

**Command Sequence:**
```bash
# Navigate to project root
cd coaching-content-library-platform

# Create frontend using Vite official template
npm create vite@7.2.4 frontend -- --template react-ts

# Navigate into frontend directory
cd frontend

# Install base dependencies
npm install

# Add project-specific dependencies
npm install @tanstack/react-query@5.90.16 react-router-dom@7.11.0 axios@1.13.2

# Add Tailwind CSS 4.1.18
npm install -D tailwindcss@4.1.18 postcss@8.5.6 autoprefixer

# Add shadcn/ui dependencies
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
npm install @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-label

# Add Lucide React icons
npm install lucide-react@0.562.0

# Add utility libraries
npm install clsx tailwind-merge class-variance-authority

# Add development dependencies
npm install -D @types/node
```

After setup, proceed with Story 1.2 (Tailwind configuration), then Story 1.3 (routing), Story 1.4 (QueryClient setup), and Story 1.5 (TypeScript types).

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED ✅
**Total Steps Completed:** 8
**Date Completed:** 2026-01-24
**Document Location:** `_bmad-output/planning-artifacts/architecture.md`

### Final Architecture Deliverables

**📋 Complete Architecture Document**

- All architectural decisions documented with specific versions
- Implementation patterns ensuring AI agent consistency
- Complete project structure with all files and directories
- Requirements to architecture mapping
- Validation confirming coherence and completeness

**🏗️ Implementation Ready Foundation**

- **9 architectural decisions made:** Vector DB (ChromaDB), Embeddings API (OpenAI text-embedding-3-small), LLM API (GPT-4o-mini), Frontend hosting (Vercel), Backend hosting (Proxmox), Reverse proxy (Caddy), Error format (structured), Rate limiting (in-memory), API versioning (/api/v1/)
- **65 implementation patterns defined:** 58 existing rules from project-context.md + 7 new patterns for conflict prevention
- **8 architectural components specified:** 8 epics mapped to 40+ files across frontend and backend
- **86 requirements fully supported:** 50 functional requirements + 36 non-functional requirements

**📚 AI Agent Implementation Guide**

- Technology stack with verified versions (React 19.2.0, Vite 7.2.4, TypeScript 5.9.3, TanStack Query 5.90.16, FastAPI 0.104.0+, Python 3.12, ChromaDB, OpenAI)
- Consistency rules that prevent implementation conflicts (backend contract, exported props, centralized config, routes.tsx, error handling)
- Project structure with clear boundaries (API, Component, Service, Data, State)
- Integration patterns and communication standards (7 integration points documented)

### Implementation Handoff

**For AI Agents:**
This architecture document is your complete guide for implementing Coaching-content-library. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:**
Epic 1, Story 1.1: Frontend Project Setup using Vite

**Command Sequence:**
```bash
cd coaching-content-library-platform
npm create vite@7.2.4 frontend -- --template react-ts
cd frontend
npm install
npm install @tanstack/react-query@5.90.16 react-router-dom@7.11.0 axios@1.13.2
npm install -D tailwindcss@4.1.18 postcss@8.5.6 autoprefixer
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
npm install @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-label
npm install lucide-react@0.562.0
npm install clsx tailwind-merge class-variance-authority
npm install -D @types/node
```

**Development Sequence:**

1. Initialize project using documented starter template (Epic 1, Story 1.1)
2. Set up development environment per architecture (Tailwind, shadcn/ui, QueryClient)
3. Implement core architectural foundations (API client, types, config, routes)
4. Build features following established patterns (Epics 2-8)
5. Maintain consistency with documented rules (65 patterns)

### Quality Assurance Checklist

**✅ Architecture Coherence**

- [x] All decisions work together without conflicts
- [x] Technology choices are compatible (verified React 19 + Vite 7.2.4, FastAPI + ChromaDB + OpenAI)
- [x] Patterns support the architectural decisions
- [x] Structure aligns with all choices

**✅ Requirements Coverage**

- [x] All functional requirements are supported (50 FRs across 6 categories)
- [x] All non-functional requirements are addressed (36 NFRs across 4 categories)
- [x] Cross-cutting concerns are handled (backend contract, AI integration, performance, error handling)
- [x] Integration points are defined (7 integration points with protocols)

**✅ Implementation Readiness**

- [x] Decisions are specific and actionable (versions specified, rationale provided)
- [x] Patterns prevent agent conflicts (65 patterns with good/bad examples)
- [x] Structure is complete and unambiguous (every file explicitly mapped)
- [x] Examples are provided for clarity (13+ code examples in patterns section)

### Project Success Factors

**🎯 Clear Decision Framework**
Every technology choice was made collaboratively with clear rationale, ensuring all stakeholders understand the architectural direction. Hybrid deployment (Vercel + Proxmox) leverages existing infrastructure while maintaining professional portfolio presentation.

**🔧 Consistency Guarantee**
Implementation patterns and rules ensure that multiple AI agents will produce compatible, consistent code that works together seamlessly. Backend contract (PascalCase enums, snake_case fields) enforced throughout all layers prevents type mismatches.

**📋 Complete Coverage**
All project requirements are architecturally supported, with clear mapping from business needs to technical implementation. Epic → File → Responsibility matrix eliminates ambiguity.

**🏗️ Solid Foundation**
The chosen starter template (Vite + React official) and architectural patterns provide a production-ready foundation following current best practices. Backend already operational (Discord bot + SQLite + ingestors) reduces implementation risk.

---

**Architecture Status:** ✅ READY FOR IMPLEMENTATION

**Next Phase:** Begin implementation using the architectural decisions and patterns documented herein.

**Document Maintenance:** Update this architecture when major technical decisions are made during implementation.


---
stepsCompleted: [1, 2, 3]
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/project-context.md'
  - '_bmad-output/planning-artifacts/ux-design-specification.md'
---

# Coaching-content-library - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Coaching-content-library, decomposing the requirements from the PRD, UX Design, and Architecture (project-context.md) into implementable stories.

## Requirements Inventory

### Functional Requirements

**Content Capture & Ingestion:**
- FR1: Coaches can submit drill URLs via Discord bot for automatic capture
- FR2: System can ingest content from YouTube, TikTok, Instagram, and Reddit sources
- FR3: System can extract available metadata from URL sources (title, author, thumbnail, view counts)
- FR4: Coaches can provide drill description during capture via Discord bot
- FR5: Coaches can specify drill tags during capture via Discord bot
- FR6: Coaches can specify difficulty level during capture (beginner, intermediate, advanced)
- FR7: Coaches can specify age group during capture (mite, squirt, peewee, bantam, midget, junior, adult)
- FR8: Coaches can specify equipment requirements during capture
- FR9: System can store captured drills with all metadata in persistent storage

**Content Management:**
- FR10: Coaches can view full drill details including all metadata
- FR11: Coaches can edit drill metadata after capture (description, tags, difficulty, age group, equipment)
- FR12: Coaches can delete drills from their library
- FR13: Coaches can add tags to existing drills
- FR14: Coaches can remove tags from existing drills
- FR15: System can track when each drill was captured (saved_at timestamp)

**Content Discovery & Search:**
- FR16: Coaches can search drill library using natural language queries
- FR17: System can perform semantic search across drill descriptions and tags
- FR18: System can return contextually relevant search results based on query meaning (not just keyword matching)
- FR19: Coaches can filter drill library by tags
- FR20: Coaches can filter drill library by difficulty level
- FR21: Coaches can filter drill library by age group
- FR22: Coaches can filter drill library by equipment requirements
- FR23: Coaches can combine multiple filters simultaneously
- FR24: Coaches can identify group drills using special "group drill" tag filter
- FR25: System can apply filters in real-time with responsive feedback

**AI-Enhanced Organization:**
- FR26: System can analyze drill content and automatically suggest relevant tags
- FR27: System can augment user-provided tags with AI-generated tags (never replacing user tags)
- FR28: System can trigger auto-tagging on drill save with rate limiting (max 1 per 5 minutes)
- FR29: Coaches can review and accept/reject auto-generated tags
- FR30: System can calculate similarity between drills based on tag overlap
- FR31: System can calculate semantic similarity between drills based on description embeddings
- FR32: System can recommend similar drills when viewing drill details
- FR33: System can combine tag similarity and semantic similarity for recommendations

**Content Viewing & Browsing:**
- FR34: Coaches can view drill library as a grid of drill cards
- FR35: System can display drill thumbnails in library grid
- FR36: System can display drill title, author, source, and key metadata on drill cards
- FR37: Coaches can navigate to original drill URL
- FR38: Coaches can view drill details in expandable sheet/modal interface
- FR39: System can display all drill metadata in detail view (title, author, source, description, tags, difficulty, age group, equipment, statistics)
- FR40: System can display similar drill recommendations in drill detail view
- FR41: Coaches can access the library on mobile, tablet, and desktop devices with responsive layout

**Metadata Management:**
- FR42: System can store drill descriptions as free text
- FR43: System can store drill tags as an array of strings
- FR44: System can store difficulty level as enumerated value (beginner, intermediate, advanced)
- FR45: System can store age group as enumerated value (mite, squirt, peewee, bantam, midget, junior, adult)
- FR46: System can store equipment requirements as free text
- FR47: System can store source platform as enumerated value (YouTube, TikTok, Instagram, Reddit)
- FR48: System can store drill statistics from source platform (view count, like count, comment count)
- FR49: System can track when each drill was published on source platform (published_at)
- FR50: System can track when each drill was fetched into the system (fetched_at)

### NonFunctional Requirements

**Performance:**
- NFR1: Initial page load completes within 3 seconds on broadband connection
- NFR2: Semantic search returns results within 2 seconds for typical queries
- NFR3: Filter application completes within 500ms (real-time feel)
- NFR4: Drill detail view opens instantly via client-side navigation
- NFR5: Images and thumbnails load progressively with lazy loading

**Integration:**
- NFR6: System can reliably integrate with YouTube API for metadata extraction
- NFR7: System can reliably integrate with TikTok for content ingestion (limited auto-fetch)
- NFR8: System can reliably integrate with Instagram for content ingestion (limited auto-fetch)
- NFR9: System can reliably integrate with Reddit API (PRAW) for metadata extraction
- NFR10: System gracefully handles API failures or rate limits from platform providers
- NFR11: System accepts user-provided metadata when platform auto-fetch fails (fallback for Instagram/TikTok)
- NFR12: System integrates with LLM API for auto-tagging with rate limiting (max 1 request per 5 minutes)
- NFR13: System integrates with embedding API for semantic search and similarity calculations
- NFR14: System handles AI API failures gracefully without blocking core functionality
- NFR15: System manages AI API costs through rate limiting and efficient request patterns
- NFR16: System maintains reliable connection between Discord bot and backend database
- NFR17: Drills captured via Discord bot appear in web UI on next page load/refresh (real-time sync not required)
- NFR18: Discord bot → database → web UI workflow functions reliably end-to-end
- NFR19: All external API calls include timeout handling
- NFR20: Failed integrations provide clear error messages to coaches
- NFR21: System logs integration failures for debugging and monitoring

**Reliability:**
- NFR22: Live deployment maintains public URL accessibility for portfolio presentation
- NFR23: System remains available during employer demo periods (no planned downtime during job search)
- NFR24: Database backups prevent data loss of curated drill library
- NFR25: All three core AI features (semantic search, auto-tagging, recommendations) function reliably and consistently
- NFR26: Discord bot capture workflow functions without data loss
- NFR27: Filtering and search operations return consistent results across sessions
- NFR28: Drill metadata is stored persistently and reliably (SQLite database integrity)
- NFR29: User-provided tags and descriptions are never lost or overwritten by AI operations
- NFR30: Backend contract integrity maintained (PascalCase enums, snake_case fields) throughout system

**Security:**
- NFR31: API credentials stored securely in environment variables (never hardcoded or committed)
- NFR32: Backend validates all user input to prevent injection attacks
- NFR33: HTTPS enforced for all production traffic
- NFR34: No logging or exposure of API keys or sensitive credentials
- NFR35: Drill library data is private to the coach (no public sharing in MVP)
- NFR36: Discord bot authentication prevents unauthorized access

### Additional Requirements

**Architecture Requirements (from project-context.md):**

**Technology Stack:**
- React 19.2.0 with TypeScript 5.9.3 (~patch updates only)
- Vite 7.2.4 (build tool, dev server on port 3000)
- TanStack Query 5.90.16 (server state management)
- React Router DOM 7.11.0 (routing)
- Tailwind CSS 4.1.18 with PostCSS 8.5.6 (v4 API, different from v3)
- Axios 1.13.2 (HTTP client)
- Radix UI components (shadcn/ui primitives)
- Lucide React 0.562.0 (icons)
- ESLint 9.39.1 with typescript-eslint 8.46.4
- Python 3.12 with FastAPI 0.104.0+
- Uvicorn 0.24.0+ (ASGI server)
- Pydantic 2.0+ with pydantic-settings 2.0+
- SQLAlchemy 2.0+ (database ORM)
- HTTPX 0.26.0+ (async HTTP client)

**Critical Backend Contract:**
- Backend enums use PascalCase: 'YouTube' | 'Reddit' | 'Instagram' | 'TikTok' (NOT lowercase!)
- Backend API uses snake_case field names: drill_tags, drill_description, content_type, published_at
- Frontend types MUST match backend exactly - DO NOT rename to camelCase
- Use `| null` for nullable fields (backend returns null, not undefined)
- **CRITICAL:** drill_tags is the active tagging system (NOT drill_type which is antiquated)

**Critical Field Names (MUST MATCH BACKEND):**
- ✅ drill_tags - ❌ NOT "tags" or "drill_type"
- ✅ drill_description - ❌ NOT "notes" or "description"
- ✅ content_type - ❌ NOT "contentType"
- ✅ 'YouTube' (PascalCase) - ❌ NOT 'youtube'

**Frontend Configuration Requirements:**
- TypeScript strict mode ENABLED with additional linting: noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch, verbatimModuleSyntax
- Module resolution: "bundler" (Vite-specific)
- JSX: "react-jsx" (automatic React import)
- ALWAYS use `@/` path alias for local imports - NEVER use relative paths like `../../`
- Use explicit type imports: `import type { ContentItem } from '@/lib/types'`
- Named exports preferred over default exports

**Backend Patterns:**
- Use absolute imports from src package root: `from ..models.content import ContentItem`
- Use `Field(default_factory=...)` for mutable defaults (lists, dicts)
- Enum values MUST be PascalCase strings: "YouTube", "Video", "Reddit"
- Use `Optional[type]` for nullable fields
- Routes use `async def` handlers
- Use `HTTPException` with proper status codes (404, 400, 201, etc.)

**React Hooks Usage:**
- Use TanStack Query hooks for all server state: useQuery, useMutation
- Custom hooks pattern: useContentList, useContentItem, useCreateContent
- Query keys: ['content', params] or ['content', source, id]
- Invalidate after mutations: queryClient.invalidateQueries({ queryKey: ['content'] })

**Component Structure:**
- shadcn/ui components in src/components/ui/
- Feature components by domain: src/components/drills/, src/components/search/
- Export named functions: `export function DrillCard({ ... }) { ... }`

**UX Design Requirements (from ux-design-specification.md):**

**Responsive Design:**
- Mobile (<768px): 1-column drill grid, collapsible filters, full-screen detail sheets
- Tablet (768-1024px): 2-column drill grid, accessible filters, drawer detail view
- Desktop (>1024px): 3-4 column drill grid, persistent filters, side panel detail view

**Hockey-Themed Design System:**
- Primary color: Deep blue (#1e3a5f - hockey-blue)
- Accent color: Ice blue (#38bdf8 - ice-blue)
- Source colors: YouTube (red-600), Reddit (orange-500), Instagram (pink-500), TikTok (black)
- Difficulty colors: beginner (green-500), intermediate (amber-500), advanced (red-500)
- Typography: Poppins (display), Inter (body)
- Spacing: 4px base unit, 8px vertical rhythm

**Component Requirements:**
- SearchHero: Prominent semantic search bar with search-first mental model
- DrillCard: Thumbnail-first visual hierarchy with progressive disclosure (thumbnail/placeholder, title, source icon, difficulty badge, 1-2 key tags)
- DrillDetail: Expandable sheet/modal with comprehensive metadata, similar drills, edit/delete actions
- FilterBar: Combinable filters for Source, Difficulty, Tags (NOT drill_type) with real-time application
- AddDrillModal: URL submission with guided metadata collection (if adding via web UI)
- TagManager: Visual distinction between user-provided tags and AI-generated tags with easy removal
- EmptyState: Clear messaging for empty library or no search results

**Critical UX Patterns:**
- Progressive disclosure: Minimal cards → comprehensive details on click
- Search-first mental model: Semantic search as primary entry point
- Coach expertise first: User tags sacred and displayed first, AI augments second
- Real-time feedback: Filters apply in <500ms, search returns in <2s
- Mobile-first: Touch-optimized interactions, thumb-friendly targets

**Accessibility Requirements:**
- Semantic HTML elements where natural
- Keyboard navigation for interactive elements
- Sufficient color contrast for readability (hockey theme uses dark blue + light blue)
- Alt text on images where present
- WCAG compliance not required for MVP, but basic accessibility practices

**Instagram/TikTok Thumbnail Constraint:**
- YouTube/Reddit: Display actual thumbnails extracted via APIs
- Instagram: Pink/purple gradient background with Instagram icon
- TikTok: Black background with cyan TikTok icon
- Maintain consistent card structure across all sources for fast scanning

**Filter System (CRITICAL CORRECTION):**
- **Correct Filters:** Source, Difficulty, Tags (drill_tags)
- **drill_type is ANTIQUATED** - replaced by tag system
- Tags filter uses drill_tags field (user-provided + AI-augmented tags)
- Multi-select tag filtering capability

### FR Coverage Map

**Epic 1: Project Foundation & Core Infrastructure**
- FR9: System can store captured drills with all metadata in persistent storage
- FR47: System can store source platform as enumerated value (YouTube, TikTok, Instagram, Reddit)

**Epic 2: Drill Library Browsing & Display**
- FR34: Coaches can view drill library as a grid of drill cards
- FR35: System can display drill thumbnails in library grid
- FR36: System can display drill title, author, source, and key metadata on drill cards
- FR41: Coaches can access the library on mobile, tablet, and desktop devices with responsive layout
- FR42: System can store drill descriptions as free text
- FR43: System can store drill tags as an array of strings
- FR44: System can store difficulty level as enumerated value (beginner, intermediate, advanced)
- FR45: System can store age group as enumerated value (mite, squirt, peewee, bantam, midget, junior, adult)
- FR46: System can store equipment requirements as free text
- FR48: System can store drill statistics from source platform (view count, like count, comment count)
- FR49: System can track when each drill was published on source platform (published_at)
- FR50: System can track when each drill was fetched into the system (fetched_at)

**Epic 3: Drill Detail View & Management**
- FR10: Coaches can view full drill details including all metadata
- FR11: Coaches can edit drill metadata after capture (description, tags, difficulty, age group, equipment)
- FR12: Coaches can delete drills from their library
- FR13: Coaches can add tags to existing drills
- FR14: Coaches can remove tags from existing drills
- FR15: System can track when each drill was captured (saved_at timestamp)
- FR37: Coaches can navigate to original drill URL
- FR38: Coaches can view drill details in expandable sheet/modal interface
- FR39: System can display all drill metadata in detail view (title, author, source, description, tags, difficulty, age group, equipment, statistics)

**Epic 4: Advanced Filtering System**
- FR19: Coaches can filter drill library by tags
- FR20: Coaches can filter drill library by difficulty level
- FR21: Coaches can filter drill library by age group
- FR22: Coaches can filter drill library by equipment requirements
- FR23: Coaches can combine multiple filters simultaneously
- FR24: Coaches can identify group drills using special "group drill" tag filter
- FR25: System can apply filters in real-time with responsive feedback

**Epic 5: Semantic Search**
- FR16: Coaches can search drill library using natural language queries
- FR17: System can perform semantic search across drill descriptions and tags
- FR18: System can return contextually relevant search results based on query meaning (not just keyword matching)

**Epic 6: Similar Drill Recommendations**
- FR30: System can calculate similarity between drills based on tag overlap
- FR31: System can calculate semantic similarity between drills based on description embeddings
- FR32: System can recommend similar drills when viewing drill details
- FR33: System can combine tag similarity and semantic similarity for recommendations
- FR40: System can display similar drill recommendations in drill detail view

**Epic 7: AI-Powered Auto-Tagging**
- FR26: System can analyze drill content and automatically suggest relevant tags
- FR27: System can augment user-provided tags with AI-generated tags (never replacing user tags)
- FR28: System can trigger auto-tagging on drill save with rate limiting (max 1 per 5 minutes)
- FR29: Coaches can review and accept/reject auto-generated tags

**Epic 8: Web-Based Drill Capture**
- FR1: Coaches can submit drill URLs via Discord bot for automatic capture
- FR2: System can ingest content from YouTube, TikTok, Instagram, and Reddit sources
- FR3: System can extract available metadata from URL sources (title, author, thumbnail, view counts)
- FR4: Coaches can provide drill description during capture via Discord bot
- FR5: Coaches can specify drill tags during capture via Discord bot
- FR6: Coaches can specify difficulty level during capture (beginner, intermediate, advanced)
- FR7: Coaches can specify age group during capture (mite, squirt, peewee, bantam, midget, junior, adult)
- FR8: Coaches can specify equipment requirements during capture

## Epic List

### Epic 1: Project Foundation & Core Infrastructure
Development environment is set up with React + TypeScript frontend, FastAPI backend, and database configured. Users can access a working homepage with hockey-themed branding.

**FRs covered:** FR9, FR47

**Implementation Notes:**
- React 19.2.0 + TypeScript 5.9.3 + Vite 7.2.4 scaffolding
- FastAPI backend with SQLAlchemy + SQLite database
- Hockey-themed design system (hockey-blue #1e3a5f, ice-blue #38bdf8)
- Backend contract enforcement (PascalCase enums, snake_case fields)
- Path aliases (@/) and TypeScript strict mode
- Basic routing and layout structure
- shadcn/ui component library setup

### Epic 2: Drill Library Browsing & Display
Coaches can view all saved drills in a responsive grid with visual drill cards showing thumbnails (or source-specific placeholders), titles, sources, and key metadata. The Discord bot → database → web UI workflow is complete.

**FRs covered:** FR34, FR35, FR36, FR41, FR42, FR43, FR44, FR45, FR46, FR48, FR49, FR50

**Implementation Notes:**
- DrillCard component with thumbnail-first design
- Responsive grid layout (1 column mobile → 2 tablet → 3-4 desktop)
- Instagram/TikTok placeholder solution (brand-colored backgrounds with icons)
- Source icons with brand colors (YouTube red, Reddit orange, Instagram pink, TikTok black)
- Difficulty badges (beginner green, intermediate amber, advanced red)
- TanStack Query integration for data fetching
- EmptyState component for empty library

**NFRs:** NFR1 (page load <3s), NFR4 (instant navigation), NFR5 (progressive image loading)

### Epic 3: Drill Detail View & Management
Coaches can click any drill to view comprehensive details in an expandable sheet/modal, edit all metadata (description, tags, difficulty, age group, equipment), delete drills, and navigate to original source URLs.

**FRs covered:** FR10, FR11, FR12, FR13, FR14, FR15, FR37, FR38, FR39

**Implementation Notes:**
- DrillDetail component as Sheet (shadcn/ui)
- Full metadata display with organized sections
- TagManager component for add/remove tags
- Edit mode for metadata updates
- Delete confirmation dialog
- "Open Original" link to source URL
- Visual distinction between user tags and AI tags (prepared for Epic 7)

**NFRs:** NFR4 (instant detail view), NFR28 (persistent metadata storage), NFR29 (user data never overwritten)

### Epic 4: Advanced Filtering System
Coaches can filter the drill library by source, difficulty, tags (drill_tags), age group, and equipment. Filters are combinable, apply in real-time (<500ms), and work seamlessly on mobile and desktop.

**FRs covered:** FR19, FR20, FR21, FR22, FR23, FR24, FR25

**Implementation Notes:**
- FilterBar component with dropdown selects
- **CRITICAL:** Filters are Source, Difficulty, Tags (drill_tags) - NOT drill_type
- Multi-select tag filtering
- Real-time filter application with TanStack Query
- Clear filters button
- Active filter state visibility
- Mobile: collapsible filter panel
- Desktop: persistent filter sidebar

**NFRs:** NFR3 (filter <500ms), NFR27 (consistent results)

### Epic 5: Semantic Search
Coaches can search the drill library using natural language queries like "drills for getting back up quickly" and receive contextually relevant results based on meaning, not just keyword matching. Search returns results within 2 seconds.

**FRs covered:** FR16, FR17, FR18

**Implementation Notes:**
- SearchHero component with prominent search bar
- Vector embeddings integration (OpenAI or Sentence Transformers)
- Vector database setup (ChromaDB or FAISS)
- Semantic similarity search across drill_description and drill_tags
- Search-first mental model in UI design
- Debounced search input (300ms)

**NFRs:** NFR2 (search <2s), NFR13 (embedding API integration), NFR14 (graceful AI API failures), NFR15 (API cost management)

### Epic 6: Similar Drill Recommendations
When viewing drill details, coaches see "Similar Drills" recommendations based on tag overlap and semantic similarity of descriptions. This helps discover related approaches and drill variety.

**FRs covered:** FR30, FR31, FR32, FR33, FR40

**Implementation Notes:**
- Recommendation engine combining tag similarity + semantic similarity
- Display in DrillDetail component
- "Drills Like This" natural language framing
- Click to navigate to recommended drill
- Builds on vector embeddings from Epic 5

**NFRs:** NFR25 (reliable AI features), NFR27 (consistent results)

### Epic 7: AI-Powered Auto-Tagging
When drills are saved (via Discord bot), the system automatically analyzes content and suggests relevant tags that augment (never replace) user-provided tags. Coaches can review, accept, or remove AI-generated tags.

**FRs covered:** FR26, FR27, FR28, FR29

**Implementation Notes:**
- LLM API integration for content analysis
- Rate limiting (max 1 per 5 minutes)
- Tag augmentation model (adds to drill_tags, never replaces)
- Visual distinction between user tags and AI tags
- Easy AI tag removal (X button)
- Triggers on drill save (Discord bot workflow)

**NFRs:** NFR12 (LLM API integration with rate limit), NFR14 (graceful AI failures), NFR15 (cost management), NFR29 (user tags never overwritten)

### Epic 8: Web-Based Drill Capture
Coaches can add drills directly from the web UI by pasting URLs, in addition to using the Discord bot. The system extracts metadata and provides guided metadata collection forms.

**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8

**Implementation Notes:**
- AddDrillModal component with URL input
- URL validation for supported platforms (YouTube, TikTok, Instagram, Reddit)
- Metadata extraction where available
- Guided forms for description, tags, difficulty, age group, equipment
- Fallback for Instagram/TikTok limited auto-fetch

**NFRs:** NFR6-NFR11 (platform API integration), NFR16-NFR18 (Discord bot integration maintained)

---

## Epic 1: Project Foundation & Core Infrastructure

**Epic Goal:** Development environment is set up with React + TypeScript frontend, FastAPI backend, and database configured. Users can access a working homepage with hockey-themed branding.

**FRs Covered:** FR9, FR47

**Backend Status:** ✅ COMPLETE (FastAPI, SQLAlchemy, ContentItem model, API endpoints, ingestors)

**Frontend Implementation:**

### Story 1.1: Frontend Project Setup

As a developer,
I want a fully configured React + TypeScript + Vite project,
So that I can start building frontend features with proper tooling and type safety.

**Acceptance Criteria:**

**Given** the coaching-content-library-web directory
**When** I run the project setup
**Then** the following are configured:
**And** package.json exists with React 19.2.0, TypeScript 5.9.3, Vite 7.2.4
**And** TanStack Query 5.90.16 for server state management
**And** React Router DOM 7.11.0 for routing
**And** Axios 1.13.2 for HTTP client
**And** Lucide React 0.562.0 for icons
**And** TypeScript strict mode is enabled with noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch
**And** Module resolution is set to "bundler" (Vite-specific)
**And** JSX is set to "react-jsx" (automatic React import)
**And** Path alias @/* maps to ./src/*
**And** ESLint 9.39.1 with typescript-eslint 8.46.4 is configured
**And** Vite dev server runs on port 3000
**And** Vite proxy configured: /api → http://localhost:8000

**Given** the TypeScript configuration
**When** importing local modules
**Then** developers must use @/ path alias (NEVER relative paths like ../../)
**And** use explicit type imports: import type { ContentItem } from '@/lib/types'
**And** named exports are preferred over default exports

### Story 1.2: Tailwind CSS & Design System

As a developer,
I want Tailwind CSS 4 configured with hockey-themed colors and shadcn/ui components,
So that I can build consistent, branded UI following the design system.

**Acceptance Criteria:**

**Given** the frontend project
**When** I configure Tailwind CSS 4
**Then** Tailwind CSS 4.1.18 with PostCSS 8.5.6 is installed (v4 API, different from v3)
**And** Custom theme colors are defined:
  - hockey-blue: #1e3a5f (primary deep blue)
  - ice-blue: #38bdf8 (accent light blue)
**And** Source badge colors are configured:
  - YouTube: red-600
  - Reddit: orange-500
  - Instagram: pink-500
  - TikTok: black
**And** Difficulty badge colors are configured:
  - beginner: green-500
  - intermediate: amber-500
  - advanced: red-500
**And** Base spacing uses 4px base unit with 8px vertical rhythm
**And** Typography fonts are configured: Poppins (display), Inter (body)

**Given** shadcn/ui setup
**When** I install base components
**Then** Radix UI primitives are installed
**And** src/components/ui/ directory is created
**And** Base shadcn/ui components are available (Button, Card, Sheet, Dialog, Select)

### Story 1.3: Router & Layout Structure

As a developer,
I want React Router and a main layout component,
So that I can structure the app with navigation and consistent page layout.

**Acceptance Criteria:**

**Given** React Router DOM 7.11.0 installed
**When** I configure routing
**Then** a router is set up with the following routes:
  - / (home page)
  - /library (drill library - future)
  - /drill/:id (drill detail - future)
**And** BrowserRouter wraps the application
**And** Route components use proper React Router v7 patterns

**Given** the layout structure
**When** I create the main layout component
**Then** src/components/layout/MainLayout.tsx exists
**And** MainLayout includes:
  - Hockey-themed header with branding
  - Navigation bar with links (Home, Library)
  - Main content area with proper spacing
  - Responsive design (mobile-first)
**And** Header uses hockey-blue background (#1e3a5f)
**And** Branding includes "Coaching Content Library" title
**And** Navigation is accessible via keyboard
**And** Layout is mobile-responsive (collapses nav on mobile)

### Story 1.4: API Integration Setup

As a developer,
I want Axios and TanStack Query configured,
So that I can make type-safe API calls to the backend with proper state management.

**Acceptance Criteria:**

**Given** Axios 1.13.2 installed
**When** I configure the HTTP client
**Then** src/lib/api.ts exports a configured Axios instance
**And** Base URL is set to /api/v1 (proxied to http://localhost:8000)
**And** Default headers include Content-Type: application/json
**And** Response interceptors handle common errors (404, 500)

**Given** TanStack Query 5.90.16 installed
**When** I configure query client
**Then** QueryClientProvider wraps the app
**And** Default query options are set (staleTime, refetchOnWindowFocus)
**And** Query cache is configured

**Given** TypeScript types for backend contract
**When** I create src/lib/types.ts
**Then** ContentItem interface matches backend exactly:
  - Uses snake_case field names (drill_tags, drill_description, content_type)
  - Enums use PascalCase: 'YouTube' | 'Reddit' | 'Instagram' | 'TikTok'
  - Nullable fields use | null (not undefined)
**And** Type definitions include:
  - ContentItem (full drill object)
  - ContentSource enum
  - ContentType enum
  - API request/response types

**Given** custom hooks scaffolding
**When** I create src/hooks/ directory
**Then** Base structure exists for future hooks:
  - useContentList (future - Epic 2)
  - useContentItem (future - Epic 3)
  - useCreateContent (future - Epic 8)

### Story 1.5: Homepage with Empty State

As a coach,
I want to see a branded homepage with clear messaging,
So that I understand what the app does and can navigate to features.

**Acceptance Criteria:**

**Given** the home route (/)
**When** I navigate to the homepage
**Then** src/pages/Home.tsx renders successfully
**And** Page displays "Coaching Content Library" heading with hockey-blue color
**And** Hero section explains the app purpose: "Organize and discover hockey goalie drills from YouTube, Reddit, Instagram, and TikTok"
**And** Empty state message displays: "Your drill library is empty. Start by adding drills via the Discord bot or web interface."
**And** CTA button links to /library (placeholder for Epic 2)

**Given** the homepage layout
**When** I view on different devices
**Then** layout is responsive:
  - Mobile (<768px): Single column, full-width hero
  - Tablet (768-1024px): Centered content with padding
  - Desktop (>1024px): Centered content with max-width

**Given** hockey-themed branding
**When** I view the homepage
**Then** visual design uses:
  - hockey-blue (#1e3a5f) for headers and primary elements
  - ice-blue (#38bdf8) for accents and CTAs
  - Clean, modern layout with sufficient whitespace
  - Hockey-related iconography (optional: puck, net, goalie silhouette)

---

## Epic 2: Drill Library Browsing & Display

**Epic Goal:** Coaches can view all saved drills in a responsive grid with visual drill cards showing thumbnails (or source-specific placeholders), titles, sources, and key metadata.

**FRs Covered:** FR34, FR35, FR36, FR41, FR42, FR43, FR44, FR45, FR46, FR48, FR49, FR50
**NFRs:** NFR1 (page load <3s), NFR4 (instant navigation), NFR5 (progressive image loading)

### Story 2.1: Drill Library Page & Data Fetching

As a coach,
I want to view all my saved drills in a library page,
So that I can browse and access my drill collection.

**Acceptance Criteria:**

**Given** React Router is configured
**When** I create the library route
**Then** /library route is registered
**And** src/pages/Library.tsx component exists
**And** Library page is accessible from navigation

**Given** the Library page
**When** I implement data fetching
**Then** src/hooks/useContentList.ts custom hook exists
**And** useContentList uses TanStack Query's useQuery
**And** Hook calls GET /api/v1/content endpoint
**And** Query key is ['content'] for base list
**And** Hook returns { data, isLoading, isError, error }

**Given** TanStack Query integration
**When** data is fetching
**Then** Loading skeleton displays (3-4 card placeholders with shimmer animation)
**And** Loading state uses Suspense pattern or conditional rendering

**Given** API call fails
**When** error occurs
**Then** Error message displays: "Failed to load drills. Please try again."
**And** Retry button is available
**And** Error uses toast notification or inline alert

**Given** successful data fetch
**When** drills are returned
**Then** Library page maps over data.items array
**And** Each drill is passed to DrillCard component
**And** Drills display in grid layout (Story 2.3)

**Given** zero drills in database
**When** API returns empty array
**Then** EmptyState component displays (Story 2.5)

### Story 2.2: DrillCard Component

As a coach,
I want to see visual drill cards with thumbnails and key information,
So that I can quickly scan and identify drills at a glance.

**Acceptance Criteria:**

**Given** the DrillCard component
**When** I create src/components/drills/DrillCard.tsx
**Then** Component accepts ContentItem as prop
**And** Component uses shadcn/ui Card primitive
**And** Card has hover effect (slight elevation/scale)
**And** Card is clickable (future: opens drill detail)

**Given** thumbnail display
**When** drill has thumbnail_url (YouTube, Reddit)
**Then** <img> element displays thumbnail
**And** Image has alt text with drill title
**And** Image uses object-cover for consistent aspect ratio
**And** Image has loading="lazy" for progressive loading (NFR5)
**And** Aspect ratio is 16:9 for video thumbnails

**Given** Instagram source without thumbnail
**When** source is Instagram
**Then** Placeholder displays with:
  - Pink/purple gradient background (from pink-400 to purple-500)
  - Instagram icon (Lucide Instagram) centered in white
  - Same 16:9 aspect ratio as thumbnails

**Given** TikTok source without thumbnail
**When** source is TikTok
**Then** Placeholder displays with:
  - Black background (#000000)
  - Cyan TikTok-style musical note icon centered
  - Same 16:9 aspect ratio as thumbnails

**Given** card metadata display
**When** card renders
**Then** Following are visible below thumbnail:
  - Drill title (truncated to 2 lines with ellipsis)
  - Author name (if available, truncated to 1 line)
  - SourceBadge component showing source (Story 2.4)
  - DifficultyBadge component if difficulty exists (Story 2.4)
  - 1-2 drill_tags displayed as small chips (progressive disclosure)

**Given** card layout
**When** content is displayed
**Then** Layout follows UX spec:
  - Thumbnail at top (thumbnail-first visual hierarchy)
  - Title in hockey-blue color, bold, 16px font
  - Author in gray-600, 14px font
  - Badges and tags in flex row with gap-2
  - Proper padding (p-4) and spacing between elements

### Story 2.3: Responsive Grid Layout

As a coach,
I want the drill library to adapt to my device screen size,
So that I can browse drills comfortably on mobile, tablet, or desktop.

**Acceptance Criteria:**

**Given** Library page with drill cards
**When** I implement grid container
**Then** Container uses CSS Grid or Tailwind grid classes
**And** Grid has proper gap spacing (gap-4 or gap-6)

**Given** mobile viewport (<768px)
**When** I view library on mobile
**Then** Grid displays 1 column
**And** Cards are full-width minus container padding
**And** Touch targets are 48px minimum for accessibility

**Given** tablet viewport (768-1024px)
**When** I view library on tablet
**Then** Grid displays 2 columns
**And** Cards maintain proper aspect ratio
**And** Gap between cards is consistent

**Given** desktop viewport (>1024px)
**When** I view library on desktop
**Then** Grid displays 3-4 columns based on container width
**And** Max container width prevents cards from becoming too wide
**And** Grid is centered with margin auto

**Given** responsive breakpoints
**When** resizing browser window
**Then** Grid smoothly transitions between column counts
**And** No horizontal scroll appears at any breakpoint
**And** Performance remains smooth (no jank during resize)

### Story 2.4: Source Icons & Difficulty Badges

As a coach,
I want to see visual badges for source platforms and difficulty levels,
So that I can quickly identify drill characteristics without reading text.

**Acceptance Criteria:**

**Given** SourceBadge component
**When** I create src/components/drills/SourceBadge.tsx
**Then** Component accepts source: ContentSource prop
**And** Component renders small badge with source icon and label

**Given** YouTube source
**When** source is 'YouTube'
**Then** Badge displays with:
  - YouTube icon (Lucide Video)
  - Red-600 background color
  - White text "YouTube"
  - Rounded corners (rounded-full or rounded-md)

**Given** Reddit source
**When** source is 'Reddit'
**Then** Badge displays with:
  - Reddit icon (Lucide MessageSquare or custom)
  - Orange-500 background color
  - White text "Reddit"

**Given** Instagram source
**When** source is 'Instagram'
**Then** Badge displays with:
  - Instagram icon (Lucide Instagram)
  - Pink-500 background color
  - White text "Instagram"

**Given** TikTok source
**When** source is 'TikTok'
**Then** Badge displays with:
  - TikTok icon (Lucide Music or custom)
  - Black background (#000000)
  - White text "TikTok"

**Given** DifficultyBadge component
**When** I create src/components/drills/DifficultyBadge.tsx
**Then** Component accepts difficulty: string | null prop
**And** Component returns null if difficulty is null

**Given** beginner difficulty
**When** difficulty is "beginner"
**Then** Badge displays with:
  - Green-500 background
  - White text "Beginner"
  - Small size (text-xs, px-2, py-1)

**Given** intermediate difficulty
**When** difficulty is "intermediate"
**Then** Badge displays with:
  - Amber-500 background
  - White text "Intermediate"

**Given** advanced difficulty
**When** difficulty is "advanced"
**Then** Badge displays with:
  - Red-500 background
  - White text "Advanced"

### Story 2.5: Empty State Component

As a coach,
I want to see a helpful message when my drill library is empty,
So that I understand what to do next and don't think the app is broken.

**Acceptance Criteria:**

**Given** EmptyState component
**When** I create src/components/ui/EmptyState.tsx
**Then** Component accepts props: title, message, actionLabel?, onAction?
**And** Component is reusable for different empty scenarios

**Given** empty drill library
**When** no drills exist in database
**Then** EmptyState displays:
  - Icon (Lucide FolderOpen or similar) in ice-blue color
  - Title: "No Drills Yet"
  - Message: "Your drill library is empty. Start by capturing drills via Discord bot or web interface."
  - CTA button: "Add Drill" (future: opens capture modal)

**Given** empty search/filter results (future)
**When** filters return zero results
**Then** EmptyState displays:
  - Icon (Lucide SearchX)
  - Title: "No Drills Found"
  - Message: "Try adjusting your filters or search query."
  - CTA button: "Clear Filters"

**Given** EmptyState layout
**When** component renders
**Then** Content is centered vertically and horizontally
**And** Icon is large (w-16 h-16 or larger)
**And** Text uses proper hierarchy (title bold, message gray-600)
**And** Adequate spacing between elements (gap-4)
**And** Component is responsive and works at all breakpoints

---

## Epic 3: Drill Detail View & Management

**Epic Goal:** Coaches can click any drill to view comprehensive details in an expandable sheet/modal, edit all metadata, delete drills, and navigate to original source URLs.

**FRs Covered:** FR10, FR11, FR12, FR13, FR14, FR15, FR37, FR38, FR39
**NFRs:** NFR4 (instant detail view), NFR28 (persistent metadata storage), NFR29 (user data never overwritten)

### Story 3.1: DrillDetail Sheet Component

As a coach,
I want to click a drill card to see full details in an expandable view,
So that I can review all drill information without leaving the library page.

**Acceptance Criteria:**

**Given** DrillCard component
**When** I add click handler
**Then** onClick opens DrillDetail sheet/modal
**And** Drill ID is passed to DrillDetail component
**And** Navigation is instant (NFR4 - client-side)

**Given** DrillDetail component
**When** I create src/components/drills/DrillDetail.tsx
**Then** Component uses shadcn/ui Sheet component
**And** Component accepts drillId prop
**And** Component fetches drill data using useContentItem hook

**Given** useContentItem hook
**When** I create src/hooks/useContentItem.ts
**Then** Hook uses TanStack Query useQuery
**And** Hook calls GET /api/v1/content/{id}
**And** Query key is ['content', drillId]
**And** Hook returns { data, isLoading, isError, error, refetch }

**Given** Sheet on mobile (<768px)
**When** DrillDetail opens on mobile
**Then** Sheet takes full screen
**And** Header has close button (X) in top-right
**And** Content is scrollable
**And** Sheet slides up from bottom with animation

**Given** Sheet on desktop (>1024px)
**When** DrillDetail opens on desktop
**Then** Sheet appears as side panel from right
**And** Width is 40-50% of viewport (max 600px)
**And** Overlay darkens background
**And** Clicking overlay closes sheet
**And** Escape key closes sheet

**Given** loading state
**When** drill data is fetching
**Then** Skeleton loader displays in sheet
**And** Skeleton matches layout structure

**Given** error state
**When** drill fetch fails
**Then** Error message displays in sheet
**And** Retry button is available
**And** Close button remains accessible

### Story 3.2: Comprehensive Metadata Display

As a coach,
I want to see all drill information in organized sections,
So that I can quickly find specific details about the drill.

**Acceptance Criteria:**

**Given** DrillDetail with loaded drill data
**When** I organize the layout
**Then** Content is divided into clear sections:
  1. Header (title, source badge, difficulty badge)
  2. Media (thumbnail or placeholder)
  3. Overview (drill_description or description, author)
  4. Drill Details (drill_tags, difficulty, age_group, equipment)
  5. Metadata (source URL, published_at, saved_at)
  6. Statistics (view_count, like_count, comment_count if available)

**Given** Header section
**When** displaying drill header
**Then** Shows:
  - Title in large, bold font (text-xl or text-2xl)
  - SourceBadge component (Story 2.4)
  - DifficultyBadge component if difficulty exists (Story 2.4)
  - Action buttons row (Edit, Delete, Open Original)

**Given** Media section
**When** drill has thumbnail_url
**Then** Displays thumbnail image with 16:9 aspect ratio
**And** Image is clickable to view full-size (optional enhancement)

**Given** Instagram/TikTok without thumbnail
**When** displaying placeholder
**Then** Shows same placeholder as DrillCard (Story 2.2)
**And** Placeholder is larger to fit detail view

**Given** Overview section
**When** displaying descriptions
**Then** Prioritizes drill_description if it exists (user-provided)
**And** Falls back to description (auto-fetched) if drill_description is null
**And** Displays author with label "By: {author}"
**And** Shows "No description available" if both are null

**Given** Drill Details section
**When** displaying drill metadata
**Then** Shows each field with label:
  - Tags: (displays all drill_tags - Story 3.4)
  - Difficulty: {difficulty} (if exists)
  - Age Group: {age_group} (if exists)
  - Equipment: {equipment} (if exists)
**And** Missing fields show "Not specified" or hide label

**Given** Metadata section
**When** displaying source info
**Then** Shows:
  - Source URL as clickable link: "Open Original" button
  - Published: {formatted_date} (if published_at exists)
  - Saved: {formatted_date} (saved_at timestamp - FR15)
**And** Dates are formatted as "Jan 15, 2026" or similar human-readable format

**Given** Statistics section
**When** drill has engagement metrics
**Then** Shows:
  - Views: {view_count} (if available)
  - Likes: {like_count} (if available)
  - Comments: {comment_count} (if available)
**And** Section is hidden if all stats are null
**And** Numbers are formatted with commas (e.g., "1,234")

### Story 3.3: Edit Mode for Metadata

As a coach,
I want to edit drill metadata after capture,
So that I can update descriptions, difficulty, age group, and equipment as needed.

**Acceptance Criteria:**

**Given** DrillDetail in view mode
**When** I click Edit button
**Then** Component switches to edit mode
**And** Editable fields become form inputs
**And** Edit button changes to Save and Cancel buttons

**Given** edit mode
**When** displaying editable fields
**Then** Following fields are editable:
  - drill_description (textarea, multiline)
  - difficulty (select dropdown: beginner, intermediate, advanced)
  - age_group (select dropdown: mite, squirt, peewee, bantam, midget, junior, adult)
  - equipment (text input)
**And** drill_tags are managed by TagManager component (Story 3.4)
**And** Non-editable fields remain display-only (title, author, source, stats)

**Given** drill_description textarea
**When** editing description
**Then** Textarea has minimum 4 rows
**And** Textarea auto-expands with content
**And** Character count displays if there's a limit
**And** Placeholder text: "Add custom drill description..."

**Given** difficulty select
**When** selecting difficulty
**Then** Options are: None, Beginner, Intermediate, Advanced
**And** "None" clears the difficulty field
**And** Current value is pre-selected

**Given** age_group select
**When** selecting age group
**Then** Options are: None, Mite, Squirt, Peewee, Bantam, Midget, Junior, Adult
**And** "None" clears the age_group field
**And** Current value is pre-selected

**Given** equipment input
**When** editing equipment
**Then** Text input allows free-form text
**And** Placeholder text: "e.g., pucks, cones, nets"
**And** Current value is pre-filled

**Given** Save button clicked
**When** user saves changes
**Then** useUpdateDrillMetadata hook is called
**And** PUT /api/v1/content/{id}/metadata is called
**And** Request includes only changed fields (drill_description, difficulty, age_group, equipment)
**And** Optimistic update shows changes immediately
**And** Success toast notification displays: "Drill updated"
**And** Edit mode switches back to view mode

**Given** useUpdateDrillMetadata hook
**When** I create src/hooks/useUpdateDrillMetadata.ts
**Then** Hook uses TanStack Query useMutation
**And** On success, invalidates ['content'] and ['content', drillId] queries
**And** On error, reverts optimistic update
**And** Error toast displays: "Failed to update drill"

**Given** Cancel button clicked
**When** user cancels editing
**Then** Form inputs revert to original values
**And** No API call is made
**And** Edit mode switches back to view mode

**Given** form validation
**When** saving changes
**Then** drill_description has max length (e.g., 2000 chars) if specified
**And** Validation errors display inline below fields
**And** Save button is disabled if validation fails

### Story 3.4: TagManager Component

As a coach,
I want to add and remove tags from drills,
So that I can organize my drills with custom labels.

**Acceptance Criteria:**

**Given** TagManager component
**When** I create src/components/drills/TagManager.tsx
**Then** Component accepts props: tags (string[]), onAddTag, onRemoveTag
**And** Component displays all tags as chips with remove buttons
**And** Component includes input field to add new tags

**Given** tag display
**When** rendering existing tags
**Then** Each tag displays as a chip/badge
**And** Each chip has small X button on the right (Lucide X icon)
**And** Chips have subtle background (gray-100 or blue-50)
**And** Chips have rounded corners (rounded-full)
**And** Chips use small font (text-sm)
**And** Tags wrap to multiple lines if needed (flex-wrap)

**Given** user tags vs AI tags (preparation for Epic 7)
**When** rendering tags
**Then** All tags initially render with same style (user tags)
**And** Component structure allows future distinction (e.g., data-source attribute)
**And** Future AI tags will have different visual style (lighter background, italic text)

**Given** remove tag interaction
**When** I click X button on a tag
**Then** onRemoveTag callback is called with tag value
**And** Tag is immediately removed from display (optimistic update)
**And** PUT /api/v1/content/{id}/metadata is called with updated drill_tags array
**And** On success, query cache is invalidated

**Given** add tag input
**When** displaying input field
**Then** Input has placeholder: "Add tag..."
**And** Input is small (text-sm, py-1, px-2)
**And** Input is positioned after existing tags

**Given** adding a new tag
**When** I type in input and press Enter
**Then** onAddTag callback is called with new tag value
**And** Tag is added to display immediately (optimistic update)
**And** Input field clears
**And** PUT /api/v1/content/{id}/metadata is called with updated drill_tags array
**And** On success, query cache is invalidated

**Given** tag validation
**When** adding a tag
**Then** Duplicate tags are prevented (case-insensitive check)
**And** Empty tags are prevented
**And** Tags are trimmed of whitespace
**And** Maximum tag length is enforced (e.g., 50 chars)
**And** Validation error displays briefly if invalid

**Given** TagManager in DrillDetail
**When** viewing Drill Details section
**Then** TagManager displays in editable mode at all times
**And** Tags can be added/removed without entering full Edit mode
**And** Changes persist immediately via API mutations

### Story 3.5: Delete Drill Confirmation

As a coach,
I want to delete drills from my library with confirmation,
So that I can remove drills I no longer need while preventing accidental deletion.

**Acceptance Criteria:**

**Given** DrillDetail component
**When** displaying action buttons
**Then** Delete button is visible in header or footer
**And** Delete button has destructive styling (red text or red background)
**And** Delete button icon is Trash2 (Lucide)

**Given** Delete button clicked
**When** user clicks Delete
**Then** Confirmation dialog opens (shadcn/ui AlertDialog)
**And** Dialog does not close DrillDetail sheet

**Given** confirmation dialog
**When** dialog displays
**Then** Dialog shows:
  - Title: "Delete Drill?"
  - Message: "Are you sure you want to delete '{drill.title}'? This action cannot be undone."
  - Cancel button (default focus)
  - Delete button (destructive red styling)

**Given** Cancel button clicked
**When** user cancels deletion
**Then** Dialog closes
**And** No API call is made
**And** DrillDetail remains open

**Given** Delete button clicked in dialog
**When** user confirms deletion
**Then** useDeleteDrill hook is called with drillId
**And** DELETE /api/v1/content/{id} is called
**And** Dialog closes
**And** DrillDetail sheet closes
**And** Deleted drill is removed from library grid immediately (optimistic update)
**And** Success toast displays: "Drill deleted"

**Given** useDeleteDrill hook
**When** I create src/hooks/useDeleteDrill.ts
**Then** Hook uses TanStack Query useMutation
**And** On success, invalidates ['content'] query to refresh list
**And** On error, reverts optimistic update
**And** Error toast displays: "Failed to delete drill"

**Given** deletion in progress
**When** API call is processing
**Then** Delete button shows loading state (spinner icon)
**And** Dialog buttons are disabled during deletion
**And** User cannot interact with dialog until complete or error

**Given** navigation after deletion
**When** drill is successfully deleted
**Then** User returns to library page
**And** Deleted drill no longer appears in grid
**And** Grid re-flows to fill the gap
**And** Focus management returns to library (accessibility)

---

## Epic 4: Advanced Filtering System

**Epic Goal:** Coaches can filter the drill library by source, difficulty, tags, age group, and equipment. Filters are combinable, apply in real-time, and work seamlessly on mobile and desktop.

**FRs Covered:** FR19, FR20, FR21, FR22, FR23, FR24, FR25
**NFRs:** NFR3 (filter <500ms), NFR27 (consistent results)

### Story 4.1: FilterBar Component & State Management

As a coach,
I want to see a filter bar with all available filter options,
So that I can easily narrow down my drill library.

**Acceptance Criteria:**

**Given** Library page
**When** I create FilterBar component
**Then** src/components/search/FilterBar.tsx exists
**And** FilterBar is positioned above the drill grid
**And** FilterBar contains filter controls (dropdowns, inputs)

**Given** filter state management
**When** implementing state
**Then** useState or useReducer manages filter state object:
  - selectedSources: string[] (ContentSource values)
  - selectedDifficulty: string | null
  - selectedTags: string[]
  - selectedAgeGroup: string | null
  - equipmentQuery: string
**And** State updates trigger useContentList re-fetch
**And** Filter state persists during session (optional: URL params)

**Given** mobile layout (<768px)
**When** viewing FilterBar on mobile
**Then** FilterBar is collapsible with toggle button
**And** Toggle button shows "Filters" with active filter count badge
**And** When expanded, filter panel slides in from top or side
**And** Panel overlays drill grid (modal-like behavior)
**And** Close button dismisses filter panel

**Given** desktop layout (>1024px)
**When** viewing FilterBar on desktop
**Then** FilterBar is persistent sidebar on left (250-300px width)
**And** Sidebar is always visible (not collapsible)
**And** Drill grid adjusts width to accommodate sidebar
**And** Sidebar has subtle border or background separation

**Given** tablet layout (768-1024px)
**When** viewing FilterBar on tablet
**Then** FilterBar appears as horizontal bar above grid
**And** Filters display in row with wrapping
**And** Dropdowns open downward without overlapping grid

**Given** active filter visibility
**When** filters are applied
**Then** Active filter count displays in badge (e.g., "Filters (3)")
**And** Each active filter shows visual indicator (checkmark, highlight)
**And** "Clear All" button appears when any filter is active

### Story 4.2: Source & Difficulty Filters

As a coach,
I want to filter drills by source platform and difficulty level,
So that I can focus on specific content types.

**Acceptance Criteria:**

**Given** Source filter
**When** I create source filter dropdown
**Then** Filter uses shadcn/ui Select or Checkbox group
**And** Filter allows multi-select (FR23 - combine filters)
**And** Options are: YouTube, Reddit, Instagram, TikTok
**And** Each option shows source icon and label
**And** Selected sources display checkmarks

**Given** no source filters selected
**When** viewing drill library
**Then** All sources are shown (default: all inclusive)

**Given** one or more sources selected
**When** I select sources
**Then** selectedSources array updates immediately
**And** useContentList hook filters by source parameter
**And** GET /api/v1/content?source={source} is called
**And** Only drills from selected sources appear in grid
**And** Filter applies in <500ms (NFR3)

**Given** Difficulty filter
**When** I create difficulty filter dropdown
**Then** Filter uses shadcn/ui Select component
**And** Filter allows single-select (one difficulty at a time)
**And** Options are: All, Beginner, Intermediate, Advanced
**And** "All" clears difficulty filter

**Given** difficulty selected
**When** I select a difficulty
**Then** selectedDifficulty updates immediately
**And** useContentList filters by difficulty parameter
**And** GET /api/v1/content?difficulty={difficulty} is called
**And** Only drills with matching difficulty appear
**And** Drills without difficulty (null) are excluded
**And** Filter applies in <500ms (NFR3)

**Given** combining source and difficulty filters (FR23)
**When** both filters are active
**Then** Query combines filters: GET /api/v1/content?source={source}&difficulty={difficulty}
**And** Results show drills matching ALL active filters (AND logic)
**And** Grid updates immediately with combined results

### Story 4.3: Tags Filter (Multi-Select)

As a coach,
I want to filter drills by tags including the special "group drill" tag,
So that I can find drills with specific characteristics or themes.

**Acceptance Criteria:**

**Given** Tags filter
**When** I create tags filter component
**Then** Filter displays list of all unique tags from existing drills
**And** Each tag is a checkbox option
**And** Tags are sorted alphabetically
**And** Tag list is scrollable if many tags exist (max-height)

**Given** tag frequency counts
**When** displaying tag options
**Then** Each tag shows count of drills with that tag: "butterfly (12)"
**And** Counts update when other filters are applied
**And** Tags with zero drills (after filtering) are grayed out or hidden

**Given** special "group drill" tag (FR24)
**When** "group drill" tag exists
**Then** Tag is labeled clearly: "group drill" or "Group Drill"
**And** Tag is easily identifiable (same as other tags, no special styling needed)
**And** Filtering by "group drill" works identically to other tags

**Given** selecting tags
**When** I check one or more tags
**Then** selectedTags array updates immediately
**And** useContentList filters by tags parameter
**And** GET /api/v1/content with tags query is called
**And** Only drills containing ANY selected tag appear (OR logic within tags)
**And** Filter applies in <500ms (NFR3)

**Given** combining tags with other filters (FR23)
**When** multiple filter types are active
**Then** Results show drills matching:
  - Selected sources (if any) AND
  - Selected difficulty (if any) AND
  - Any selected tag (OR within tags, AND with other filters)
**And** Backend search query handles multiple criteria correctly

**Given** search input for tags (optional enhancement)
**When** many tags exist
**Then** Search input filters tag list
**And** Typing narrows visible tag options
**And** Search is case-insensitive

### Story 4.4: Age Group & Equipment Filters

As a coach,
I want to filter drills by age group and equipment requirements,
So that I can find drills appropriate for my team and available resources.

**Acceptance Criteria:**

**Given** Age Group filter
**When** I create age group filter dropdown
**Then** Filter uses shadcn/ui Select component
**And** Filter allows single-select
**And** Options are: All, Mite, Squirt, Peewee, Bantam, Midget, Junior, Adult
**And** "All" clears age group filter

**Given** age group selected
**When** I select an age group
**Then** selectedAgeGroup updates immediately
**And** useContentList filters by age_group parameter
**And** GET /api/v1/content?age_group={age_group} is called
**And** Only drills with matching age_group appear
**And** Drills without age_group (null) are excluded
**And** Filter applies in <500ms (NFR3)

**Given** Equipment filter
**When** I create equipment filter input
**Then** Filter is a text input field
**And** Input has placeholder: "Search equipment..."
**And** Input has debounce delay (300ms) to avoid excessive requests

**Given** equipment search
**When** I type in equipment field
**Then** equipmentQuery updates after debounce
**And** useContentList filters by equipment parameter
**And** GET /api/v1/content?equipment={query} is called
**And** Backend performs partial match on equipment field (LIKE query)
**And** Drills with matching equipment text appear
**And** Search is case-insensitive

**Given** equipment suggestions (optional enhancement)
**When** displaying equipment filter
**Then** Dropdown shows common equipment from existing drills
**And** Clicking suggestion populates input
**And** Examples: "pucks", "cones", "nets", "sticks"

**Given** clearing individual filters
**When** I want to clear a specific filter
**Then** Each filter has clear button (X icon) when active
**And** Clicking X clears that filter only
**And** Other filters remain active
**And** Grid updates immediately

### Story 4.5: Filter Application & Clear Functionality

As a coach,
I want filters to apply instantly and see which filters are active,
So that I can quickly explore my drill library and reset when needed.

**Acceptance Criteria:**

**Given** useContentList hook updates
**When** I modify src/hooks/useContentList.ts
**Then** Hook accepts filterParams object parameter
**And** filterParams includes: sources, difficulty, tags, ageGroup, equipment
**And** Hook constructs query string from filterParams
**And** Query key includes filterParams for proper caching: ['content', filterParams]

**Given** filter application performance (NFR3)
**When** any filter changes
**Then** Results update in <500ms
**And** No unnecessary API calls are made (debouncing for text inputs)
**And** TanStack Query caching prevents duplicate requests
**And** Loading state is minimal or not noticeable

**Given** combining all filter types (FR23)
**When** multiple filters are active across all types
**Then** Query combines all parameters:
  - GET /api/v1/content?source=YouTube&source=Reddit&difficulty=beginner&tags=butterfly&tags=lateral&age_group=bantam&equipment=pucks
**And** Backend correctly handles multiple parameters
**And** Results match ALL criteria (AND logic between filter types)
**And** Results are consistent across sessions (NFR27)

**Given** "Clear All Filters" button
**When** I create clear all functionality
**Then** Button displays when any filter is active
**And** Button is prominently placed (top of FilterBar)
**And** Button label: "Clear All Filters" or "Clear (3)" with count

**Given** clicking "Clear All Filters"
**When** button is clicked
**Then** All filter state resets to defaults:
  - selectedSources = []
  - selectedDifficulty = null
  - selectedTags = []
  - selectedAgeGroup = null
  - equipmentQuery = ""
**And** All visual indicators clear (checkboxes unchecked, dropdowns reset)
**And** useContentList fetches unfiltered results
**And** Full drill library displays

**Given** active filter count badge
**When** filters are applied
**Then** Badge shows count of active filter categories (not individual selections)
**And** Example: Source + Difficulty + 3 Tags = "Filters (3)"
**And** Badge updates immediately as filters change
**And** Badge is visually distinct (colored background, e.g., ice-blue)

**Given** URL state sync (optional enhancement)
**When** filters are applied
**Then** URL updates with filter parameters
**And** Example: /library?source=YouTube&difficulty=beginner
**And** Sharing URL preserves filters
**And** Refreshing page maintains filter state

**Given** empty results after filtering
**When** filters produce zero results
**Then** EmptyState component displays (Story 2.5)
**And** Message: "No drills found matching your filters"
**And** "Clear Filters" action in EmptyState
**And** Active filter summary displays above EmptyState

**Given** filter state consistency (NFR27)
**When** applying same filters multiple times
**Then** Results are identical each time
**And** Order is consistent (e.g., by saved_at DESC)
**And** No random variations in results

---

## Epic 5: Semantic Search

**Epic Goal:** Coaches can search the drill library using natural language queries and receive contextually relevant results based on meaning, not just keyword matching.

**FRs Covered:** FR16, FR17, FR18
**NFRs:** NFR2 (search <2s), NFR13 (embedding API integration), NFR14 (graceful AI API failures), NFR15 (API cost management)

### Story 5.1: SearchHero Component & UI

As a coach,
I want a prominent search bar that understands natural language,
So that I can find drills by describing what I'm looking for in my own words.

**Acceptance Criteria:**

**Given** Library page
**When** I create SearchHero component
**Then** src/components/search/SearchHero.tsx exists
**And** SearchHero is positioned prominently at top of library page
**And** Component follows search-first mental model from UX spec

**Given** search input field
**When** rendering the search bar
**Then** Input is large and visually prominent (text-lg, py-3, px-4)
**And** Placeholder text: "Search drills... e.g., 'quick recovery drills' or 'lateral movement'"
**And** Search icon (Lucide Search) displays on left side of input
**And** Input has rounded corners and subtle border
**And** Input uses hockey-blue focus ring on focus

**Given** search input interaction
**When** I type in search field
**Then** Input is debounced with 300ms delay
**And** No API call is made until typing pauses
**And** Debounce prevents excessive requests during typing

**Given** search submission
**When** I press Enter key or click search button
**Then** Search query is submitted immediately (bypasses debounce)
**And** useSemanticSearch hook is called with query
**And** Loading state displays

**Given** loading state
**When** search is in progress
**Then** Loading spinner displays inside search input (right side)
**And** Input remains enabled (can type to refine)
**And** Loading indicator is subtle (small spinner)

**Given** active search query
**When** search has been performed
**Then** Clear button (X icon) appears on right side of input
**And** Clicking X clears the search query
**And** Clearing search resets to full drill library
**And** Input refocuses after clearing

**Given** empty search input
**When** input is empty
**Then** Full drill library displays (no filtering)
**And** Search button is disabled or hidden
**And** Placeholder text is visible

**Given** mobile layout
**When** viewing SearchHero on mobile
**Then** Search bar takes full width
**And** Input size adjusts for mobile (slightly smaller padding)
**And** Touch target for clear button is 44x44px minimum

### Story 5.2: Vector Embeddings Backend Setup

As a developer,
I want drill content embedded as vectors,
So that I can perform semantic similarity searches.

**Acceptance Criteria:**

**Given** embedding provider choice
**When** selecting embedding solution
**Then** Choose between:
  - OpenAI Embeddings API (text-embedding-3-small) - paid, high quality
  - Sentence Transformers (all-MiniLM-L6-v2) - free, local, good quality
**And** Document choice in project-context.md or config
**And** Install required dependencies (openai SDK or sentence-transformers)

**Given** database schema update
**When** I modify SQLite schema
**Then** Add embedding column to content table:
  - ALTER TABLE content ADD COLUMN embedding BLOB
**And** BLOB stores serialized vector (pickle or JSON)
**And** Migration runs automatically on app start (_ensure_schema)

**Given** embedding generation function
**When** I create src/embeddings/generator.py
**Then** Function generate_embedding(text: str) -> list[float] exists
**And** Function combines drill_description and drill_tags into single text
**And** Example combined text: "{drill_description}. Tags: {tag1}, {tag2}"
**And** Function calls embedding API or model
**And** Function returns vector (e.g., 384-dimensional for MiniLM)

**Given** OpenAI embeddings choice
**When** using OpenAI
**Then** Use text-embedding-3-small model (cost-efficient)
**And** API key stored in settings.openai_api_key
**And** Handle API errors gracefully (NFR14)
**And** Implement retry logic with exponential backoff

**Given** Sentence Transformers choice
**When** using local embeddings
**Then** Model is downloaded on first run (~80MB)
**And** Model is cached for subsequent uses
**And** Inference runs on CPU (fast enough for single queries)

**Given** embedding on save
**When** drill is saved via POST /api/v1/content
**Then** After saving drill, generate_embedding is called
**And** Embedding is calculated for drill_description + drill_tags
**And** Embedding is stored in embedding column
**And** If embedding fails, drill is still saved (graceful degradation - NFR14)

**Given** background job for existing drills
**When** I create embedding backfill script
**Then** Script iterates all drills without embeddings
**And** Generates embeddings for each drill
**And** Updates database with embeddings
**And** Script can be run via CLI: python -m src.embeddings.backfill
**And** Script includes rate limiting to avoid API limits (NFR15)

**Given** cost management (NFR15)
**When** using OpenAI embeddings
**Then** Rate limit: max 100 embeddings per minute
**And** Log embedding API calls for cost tracking
**And** Use caching: don't re-embed unchanged content
**And** Estimated cost: ~$0.00002 per drill (negligible)

### Story 5.3: Semantic Search Backend Implementation

As a developer,
I want a semantic search endpoint that finds similar drills,
So that coaches can search using natural language.

**Acceptance Criteria:**

**Given** vector database choice
**When** selecting vector search solution
**Then** Choose between:
  - ChromaDB (simple, persistent, good for small-medium datasets)
  - FAISS (Meta, high performance, in-memory or persistent)
  - SQLite with cosine similarity (simple, no extra dependencies)
**And** For MVP, SQLite cosine similarity is sufficient
**And** Install required dependencies if needed

**Given** semantic search endpoint
**When** I create POST /api/v1/content/search route
**Then** Endpoint accepts SearchRequest body:
  - query: str (natural language search query)
  - limit: int = 10 (max results)
**And** Endpoint is separate from GET /api/v1/content (filtering)
**And** Endpoint uses async def handler

**Given** search query processing
**When** search request is received
**Then** Generate embedding for query using generate_embedding(query)
**And** If embedding fails, fall back to keyword search (NFR14)
**And** Embedding generation completes in <500ms

**Given** similarity calculation (SQLite approach)
**When** computing semantic similarity
**Then** Calculate cosine similarity between query embedding and all drill embeddings
**And** Cosine similarity formula: dot(A, B) / (norm(A) * norm(B))
**And** Query: SELECT *, cosine_similarity(embedding, ?) as score FROM content ORDER BY score DESC LIMIT ?
**And** Return drills ranked by similarity score (0-1 range)

**Given** ChromaDB approach (alternative)
**When** using ChromaDB
**Then** Create ChromaDB collection on app startup
**And** Index all drill embeddings in collection
**And** Use collection.query(query_embeddings=..., n_results=limit)
**And** ChromaDB handles similarity search automatically

**Given** search across drill_description and drill_tags (FR17)
**When** embeddings are generated
**Then** Combined text includes both fields
**And** Semantic search considers both description content and tags
**And** Results reflect matches in either field

**Given** contextually relevant results (FR18)
**When** processing search query
**Then** Results are ranked by semantic meaning, not keyword matching
**And** Example: "quick recovery" matches "fast rebound drills" even without exact words
**And** Example: "lateral movement" matches "side-to-side skating"
**And** Minimum similarity threshold: 0.3 (configurable)

**Given** search performance (NFR2)
**When** search endpoint is called
**Then** Total response time is <2 seconds:
  - Embedding generation: <500ms
  - Similarity search: <1000ms
  - Result formatting: <500ms
**And** Response includes timing metadata for monitoring

**Given** search response format
**When** returning results
**Then** Response is SearchResponse:
  - items: list[ContentItemResponse]
  - total: int
  - query_time_ms: int (optional, for monitoring)
**And** Items are ordered by relevance (similarity score DESC)
**And** Items match ContentItemResponse schema from Epic 2

### Story 5.4: Search Results Display & Integration

As a coach,
I want to see relevant search results instantly,
So that I can quickly find the drills I'm looking for.

**Acceptance Criteria:**

**Given** useSemanticSearch hook
**When** I create src/hooks/useSemanticSearch.ts
**Then** Hook uses TanStack Query useMutation (POST request)
**And** Hook accepts query: string parameter
**And** Hook calls POST /api/v1/content/search
**And** Hook returns { mutate, data, isLoading, isError, error }

**Given** SearchHero integration
**When** search query is submitted
**Then** useSemanticSearch.mutate({ query }) is called
**And** Loading state displays in search bar
**And** Drill grid shows loading skeletons

**Given** search results display
**When** search completes successfully
**Then** Drill grid displays search results
**And** Results use same DrillCard components (Story 2.2)
**And** Grid layout remains responsive (Story 2.3)
**And** Search results replace filtered results (search takes precedence over filters)

**Given** relevance indicators (optional enhancement)
**When** displaying search results
**Then** Each card optionally shows similarity score (e.g., "95% match")
**And** Visual indicator is subtle (small badge, gray text)
**And** High relevance (>0.7) could have stronger visual cue

**Given** search result ordering
**When** results are displayed
**Then** Drills are ordered by semantic similarity score (highest first)
**And** Most relevant drills appear at top
**And** Order is consistent for same query (NFR27)

**Given** empty search results
**When** search finds no matches (similarity < threshold)
**Then** EmptyState component displays (Story 2.5)
**And** Message: "No drills found for '{query}'"
**And** Suggestion: "Try different keywords or check spelling"
**And** Option to clear search and return to library

**Given** search error (NFR14)
**When** semantic search API fails
**Then** Error toast displays: "Search failed. Showing keyword results instead."
**And** System falls back to keyword search (GET /api/v1/content?query={query})
**And** User still sees some results (graceful degradation)
**And** Error is logged for debugging

**Given** combining search with filters
**When** both search and filters are active
**Then** Search takes precedence (filters are temporarily ignored)
**And** Message displays: "Showing search results. Clear search to use filters."
**And** Or, apply filters to search results (product decision)

**Given** clearing search
**When** user clears search query
**Then** Search results clear
**And** Library returns to previous state (filtered or full library)
**And** Filters re-apply if they were active

### Story 5.5: Error Handling & Cost Management

As a developer,
I want robust error handling and cost controls for AI features,
So that the system remains reliable and cost-efficient.

**Acceptance Criteria:**

**Given** embedding API failure (NFR14)
**When** generate_embedding() fails
**Then** Function logs error with details
**And** Function returns None or empty vector
**And** Caller handles None gracefully (skips embedding, continues operation)
**And** User-facing operations don't fail due to embedding errors

**Given** semantic search failure
**When** POST /api/v1/content/search fails
**Then** Frontend catches error
**And** Error toast displays: "Semantic search unavailable. Try again or use filters."
**And** Optionally falls back to keyword search automatically
**And** Error doesn't crash the application

**Given** rate limiting (NFR15)
**When** making embedding API calls
**Then** Implement rate limiter:
  - Max 100 requests per minute for OpenAI
  - No limit for local Sentence Transformers
**And** Rate limiter queues requests if limit exceeded
**And** Rate limiter prevents API errors from rate limits

**Given** embedding cost tracking (NFR15)
**When** using OpenAI embeddings
**Then** Log each embedding API call with:
  - Timestamp
  - Token count
  - Estimated cost ($0.00002 per embedding)
**And** Optional: Daily cost summary in logs
**And** Alert if daily cost exceeds threshold (e.g., $1.00)

**Given** caching embeddings
**When** drill content hasn't changed
**Then** Don't regenerate embedding (use existing)
**And** Only regenerate if drill_description or drill_tags change
**And** Check: if existing embedding is not None, skip generation

**Given** embedding generation timeout
**When** API call takes too long
**Then** Timeout after 5 seconds
**And** Log timeout error
**And** Return None to allow operation to continue
**And** User sees graceful degradation (drill saves without embedding)

**Given** monitoring and logging
**When** semantic search is used
**Then** Log key metrics:
  - Search query
  - Result count
  - Query time (total and breakdown)
  - Success/failure status
**And** Metrics enable performance tuning
**And** Logs help debug search quality issues

**Given** API key security
**When** using OpenAI API
**Then** API key stored in environment variable (settings.openai_api_key)
**And** API key never logged or exposed in responses
**And** .env file is in .gitignore (never committed)
**And** Documentation explains API key setup

---

## Epic 6: Similar Drill Recommendations

**Epic Goal:** When viewing drill details, coaches see "Similar Drills" recommendations based on tag overlap and semantic similarity, helping discover related approaches and drill variety.

**FRs Covered:** FR30, FR31, FR32, FR33, FR40
**NFRs:** NFR25 (reliable AI features), NFR27 (consistent results)

### Story 6.1: Similar Drills Backend Endpoint

As a developer,
I want a backend endpoint that finds similar drills,
So that coaches can discover related content when viewing drill details.

**Acceptance Criteria:**

**Given** similar drills endpoint
**When** I create GET /api/v1/content/{id}/similar route
**Then** Endpoint accepts path parameter: content_id
**And** Endpoint accepts query parameter: limit (default 5, max 20)
**And** Endpoint uses async def handler
**And** Endpoint returns SimilarDrillsResponse

**Given** SimilarDrillsResponse schema
**When** defining response model
**Then** Response includes:
  - items: list[ContentItemResponse] (similar drills)
  - total: int (count of similar drills found)
  - source_drill_id: str (the original drill ID)
**And** Each item includes similarity metadata (optional for debugging)

**Given** tag similarity calculation (FR30)
**When** computing tag overlap
**Then** Use Jaccard similarity: |A ∩ B| / |A ∪ B|
**And** A = source drill's drill_tags
**And** B = candidate drill's drill_tags
**And** Score ranges from 0 (no overlap) to 1 (identical tags)
**And** Handle empty tag arrays (return 0 similarity)

**Given** semantic similarity calculation (FR31)
**When** computing embedding similarity
**Then** Use cosine similarity between embeddings
**And** Source drill embedding vs candidate drill embedding
**And** Score ranges from 0 (opposite) to 1 (identical)
**And** Handle missing embeddings (return 0 or skip drill)

**Given** query execution
**When** finding similar drills
**Then** Fetch all drills except the source drill (exclude self)
**And** Calculate tag similarity for each drill
**And** Calculate semantic similarity for each drill (if embeddings exist)
**And** Combine similarities using formula from Story 6.2
**And** Sort by combined similarity score DESC
**And** Return top N drills (limit parameter)

**Given** no similar drills found
**When** all similarity scores are below threshold
**Then** Return empty items array
**And** total = 0
**And** Response is still successful (200 OK)

**Given** source drill has no tags or embedding
**When** source drill lacks similarity features
**Then** Return drills from same source platform as fallback
**And** Or return recently added drills
**And** Or return empty if no good recommendations

### Story 6.2: Recommendation Algorithm

As a developer,
I want a configurable recommendation algorithm,
So that I can balance tag-based and semantic-based similarity for optimal results.

**Acceptance Criteria:**

**Given** combined similarity formula (FR33)
**When** calculating final similarity score
**Then** Use weighted combination:
  - combined_score = (tag_weight * tag_similarity) + (semantic_weight * semantic_similarity)
**And** Default weights: tag_weight = 0.4, semantic_weight = 0.6
**And** Weights are configurable in settings
**And** Weights sum to 1.0 (tag_weight + semantic_weight = 1.0)

**Given** tag similarity weight
**When** tags overlap significantly
**Then** Drills with many shared tags rank higher
**And** Tag similarity contributes 40% to final score
**And** Example: 3 shared tags out of 5 = high tag similarity

**Given** semantic similarity weight
**When** descriptions are semantically similar
**Then** Drills with similar descriptions rank higher
**And** Semantic similarity contributes 60% to final score
**And** Example: "quick recovery" matches "fast rebound" semantically

**Given** minimum similarity threshold
**When** filtering candidates
**Then** Only return drills with combined_score >= threshold
**And** Default threshold: 0.3 (configurable in settings)
**And** Threshold prevents irrelevant recommendations
**And** Threshold ensures minimum quality bar

**Given** tie-breaking
**When** multiple drills have same similarity score
**Then** Secondary sort by saved_at DESC (newer drills first)
**And** Ensures consistent ordering (NFR27)
**And** Provides variety in recommendations

**Given** diversity in recommendations
**When** selecting top N drills
**Then** Optionally limit drills from same source (e.g., max 2 YouTube)
**And** Ensures variety across platforms
**And** Configurable: diversity_mode = true/false

**Given** algorithm configuration
**When** defining settings
**Then** Add to settings.py or config:
  - similarity_tag_weight: float = 0.4
  - similarity_semantic_weight: float = 0.6
  - similarity_threshold: float = 0.3
  - similarity_diversity_mode: bool = False
**And** Document algorithm in code comments
**And** Allow tuning based on user feedback

**Given** edge cases
**When** handling special scenarios
**Then** Source drill has no tags → rely 100% on semantic similarity
**And** Source drill has no embedding → rely 100% on tag similarity
**And** Source drill has neither → return popular drills or empty
**And** All calculations handle None/null values gracefully

### Story 6.3: Similar Drills Display in DrillDetail

As a coach,
I want to see similar drills when viewing drill details,
So that I can discover related drills and expand my practice ideas.

**Acceptance Criteria:**

**Given** DrillDetail component
**When** I add Similar Drills section
**Then** Section appears after main drill details
**And** Section has header: "Similar Drills" or "You might also like"
**And** Section is visually separated (border-top or spacing)

**Given** useSimilarDrills hook
**When** I create src/hooks/useSimilarDrills.ts
**Then** Hook uses TanStack Query useQuery
**And** Hook accepts drillId: string parameter
**And** Hook calls GET /api/v1/content/{id}/similar
**And** Query key: ['content', drillId, 'similar']
**And** Hook returns { data, isLoading, isError, error }

**Given** Similar Drills layout
**When** rendering recommendations
**Then** Display as horizontal scrollable row
**And** Use flex row with overflow-x-auto
**And** Show 2-3 cards visible at once (responsive)
**And** Smooth scroll behavior
**And** Scroll indicators (shadows on edges) if many drills

**Given** compact drill card
**When** I create SimilarDrillCard component
**Then** Card is smaller than main DrillCard (Story 2.2)
**And** Card shows:
  - Thumbnail or placeholder (smaller aspect ratio)
  - Title (truncated to 1-2 lines)
  - SourceBadge (small)
  - DifficultyBadge (small, if exists)
**And** Card is clickable
**And** Card has hover effect (elevation or border)

**Given** loading state
**When** similar drills are fetching
**Then** Show 3-4 skeleton card placeholders
**And** Skeletons match SimilarDrillCard dimensions
**And** Loading is non-blocking (main content already visible)

**Given** error state
**When** similar drills API fails
**Then** Show message: "Unable to load similar drills"
**And** Or hide Similar Drills section entirely
**And** Error doesn't affect main drill details display
**And** Error is logged for debugging

**Given** no similar drills found
**When** API returns empty array
**Then** Show message: "No similar drills found"
**And** Or hide Similar Drills section entirely
**And** Don't show empty scrollable area

**Given** mobile layout
**When** viewing on mobile (<768px)
**Then** Similar Drills section is full-width
**And** Cards are larger on mobile (easier to tap)
**And** Horizontal scroll is smooth with touch gestures
**And** Show 1-2 cards visible at once

**Given** desktop layout
**When** viewing on desktop (>1024px)
**Then** Similar Drills section fits within DrillDetail width
**And** Show 3-4 cards visible at once
**And** Mouse wheel scrolls horizontally (optional enhancement)

### Story 6.4: Navigation & Interaction

As a coach,
I want to click similar drills to view their details,
So that I can seamlessly explore related drills.

**Acceptance Criteria:**

**Given** SimilarDrillCard click
**When** I click a similar drill card
**Then** DrillDetail component updates to show clicked drill
**And** Similar drills re-fetch for new drill
**And** Smooth transition (no flash or loading flicker)
**And** Scroll position resets to top of DrillDetail

**Given** drill navigation state
**When** navigating between similar drills
**Then** Current drill ID updates
**And** URL updates to reflect current drill (optional): /library?drill={id}
**And** Browser back button navigates to previous drill
**And** Navigation history is tracked

**Given** deep linking
**When** using URL parameters
**Then** Opening /library?drill={id} opens DrillDetail automatically
**And** Sheet opens with correct drill data
**And** Similar drills load for that drill
**And** Shareable URLs work correctly

**Given** breadcrumb or back navigation (optional)
**When** viewing drill from similar drills
**Then** Option to return to original drill
**And** "Back to [Original Drill Title]" link (optional)
**And** Or use browser back button

**Given** infinite similar drill exploration
**When** user clicks similar drill, then another similar drill
**Then** User can navigate indefinitely through recommendations
**And** Each drill shows its own similar drills
**And** Navigation doesn't break or loop infinitely

**Given** closing DrillDetail
**When** user closes sheet after exploring similar drills
**Then** Sheet closes completely
**And** Returns to library grid
**And** No residual state from similar drill navigation

### Story 6.5: Performance & Caching

As a developer,
I want similar drill recommendations to be fast and efficient,
So that coaches experience smooth navigation without delays.

**Acceptance Criteria:**

**Given** similar drills caching
**When** fetching similar drills
**Then** TanStack Query caches results for 5 minutes
**And** Subsequent views of same drill use cached results
**And** Cache key includes drillId: ['content', drillId, 'similar']
**And** Cache invalidates when drill is updated or deleted

**Given** lazy loading similar drills
**When** DrillDetail opens
**Then** Main drill data loads first (priority)
**And** Similar drills load after main content (lower priority)
**And** Similar Drills section displays loading state initially
**And** User can interact with main content while similar drills load

**Given** similarity calculation performance
**When** backend calculates similarities
**Then** Total query time is <1 second for 100 drills
**And** Optimize with database indices if needed
**And** Consider pre-computing similarities for popular drills (future)

**Given** recommendation consistency (NFR27)
**When** viewing same drill multiple times
**Then** Similar drills are identical each time
**And** Order is stable and consistent
**And** No randomness in recommendations

**Given** drill with no similar matches
**When** source drill is very unique
**Then** Handle gracefully (empty state or hide section)
**And** Don't show error to user
**And** Log for analytics (helps identify content gaps)

**Given** batch similarity calculations (optimization)
**When** calculating similarities for many drills
**Then** Use vectorized operations if possible
**And** SQLite: calculate all similarities in single query
**And** Avoid N+1 query problems

**Given** cache invalidation
**When** drill metadata is updated
**Then** Invalidate similar drills cache for that drill
**And** Invalidate cache for drills that had it as recommendation
**And** Or use cache TTL to handle stale data (simpler)

**Given** monitoring
**When** similar drills feature is used
**Then** Log metrics:
  - Average similarity scores
  - Number of similar drills found per query
  - Click-through rate on recommendations
**And** Metrics inform algorithm tuning
**And** Track if feature provides value to users

---

## Epic 7: AI-Powered Auto-Tagging

**Epic Goal:** When drills are saved, the system automatically analyzes content and suggests relevant tags that augment (never replace) user-provided tags. Coaches can review, accept, or remove AI-generated tags.

**FRs Covered:** FR26, FR27, FR28, FR29
**NFRs:** NFR12 (LLM API integration with rate limit), NFR14 (graceful AI failures), NFR15 (cost management), NFR29 (user tags never overwritten)

### Story 7.1: LLM Integration & Tag Generation Backend

As a developer,
I want an LLM to analyze drill content and suggest relevant tags,
So that coaches benefit from automatic drill organization.

**Acceptance Criteria:**

**Given** LLM provider choice
**When** selecting LLM for auto-tagging
**Then** Choose between:
  - OpenAI GPT-4o-mini (cost-efficient, high quality)
  - Anthropic Claude Haiku (fast, cost-efficient)
  - Local LLM (Llama, Mistral - free but requires more resources)
**And** Document choice in project-context.md or config
**And** Install required SDK (openai, anthropic, or ollama)

**Given** tag generation function
**When** I create src/ai/auto_tagger.py
**Then** Function generate_tags(title: str, description: str) -> list[str] exists
**And** Function accepts drill title and description as input
**And** Function returns 3-5 relevant tags
**And** Function uses LLM API to analyze content

**Given** LLM prompt engineering
**When** crafting the prompt
**Then** Prompt instructs LLM to:
  - Analyze hockey goalie drill content
  - Extract 3-5 specific, relevant tags
  - Focus on: skills (butterfly, lateral movement), drill type (warmup, game situation), equipment needed
  - Return tags as JSON array or comma-separated list
  - Use lowercase, hyphenated format (e.g., "butterfly-push", "quick-recovery")
**And** Prompt includes few-shot examples for consistency
**And** Prompt emphasizes brevity and specificity

**Given** example prompt structure
**When** calling LLM
**Then** Prompt format:
```
Analyze this hockey goalie drill and suggest 3-5 relevant tags.

Title: {title}
Description: {description}

Tags should describe:
- Skills practiced (butterfly, lateral-movement, tracking)
- Drill type (warmup, game-situation, conditioning)
- Equipment needed (pucks, cones, nets)

Return only the tags as a comma-separated list. Be specific and concise.

Tags:
```
**And** LLM response is parsed into tag array

**Given** OpenAI implementation
**When** using OpenAI GPT-4o-mini
**Then** Use gpt-4o-mini model (cost-efficient: ~$0.0001 per drill)
**And** Set max_tokens to 50 (tags are short)
**And** Set temperature to 0.3 (consistent, less creative)
**And** API key stored in settings.openai_api_key

**Given** Anthropic Claude implementation
**When** using Claude Haiku
**Then** Use claude-3-haiku model (fast and cheap)
**And** Set max_tokens to 100
**And** API key stored in settings.anthropic_api_key

**Given** tag parsing
**When** LLM returns response
**Then** Parse response to extract tags
**And** Handle both JSON array and comma-separated formats
**And** Clean tags: strip whitespace, lowercase, validate format
**And** Deduplicate tags (case-insensitive)
**And** Limit to 5 tags maximum

**Given** error handling (NFR14)
**When** LLM API fails
**Then** Log error with details
**And** Return empty list (graceful degradation)
**And** Drill save operation continues without tags
**And** Error doesn't block user workflow

**Given** timeout handling
**When** LLM API is slow
**Then** Timeout after 10 seconds
**And** Return empty list on timeout
**And** Log timeout for monitoring

### Story 7.2: Rate Limiting & Cost Management

As a developer,
I want to rate limit auto-tagging requests,
So that API costs remain controlled and within budget.

**Acceptance Criteria:**

**Given** rate limiting requirement (FR28, NFR12)
**When** implementing rate limiter
**Then** Maximum 1 auto-tag request per 5 minutes globally
**And** Rate limit applies across all users (for MVP)
**And** Rate limiter uses in-memory store (Redis for production)

**Given** rate limiter implementation
**When** I create src/ai/rate_limiter.py
**Then** Class RateLimiter exists with methods:
  - is_allowed(key: str) -> bool
  - record_request(key: str) -> None
**And** Uses sliding window algorithm
**And** Key: "auto-tag" (global for MVP)
**And** Window: 5 minutes (300 seconds)

**Given** rate limit check
**When** drill is saved and triggers auto-tagging
**Then** Check if auto-tagging is allowed: rate_limiter.is_allowed("auto-tag")
**And** If allowed: proceed with generate_tags()
**And** If not allowed: skip auto-tagging, save drill without AI tags
**And** Log when rate limit is hit

**Given** rate limit exceeded
**When** max requests per window is reached
**Then** Skip auto-tagging for this drill
**And** Log: "Auto-tagging skipped due to rate limit"
**And** User notification (optional): "Auto-tags will be generated shortly"
**And** Drill saves successfully without AI tags

**Given** queue system (optional enhancement)
**When** rate limit is exceeded
**Then** Queue drill for later auto-tagging
**And** Background worker processes queue when rate limit resets
**And** Update drill with AI tags asynchronously

**Given** cost tracking (NFR15)
**When** auto-tagging is performed
**Then** Log each request:
  - Timestamp
  - Drill ID
  - Number of tags generated
  - Estimated cost (e.g., $0.0001 per request)
**And** Calculate daily/monthly totals
**And** Alert if costs exceed threshold (e.g., $5/month)

**Given** cost estimation
**When** using GPT-4o-mini
**Then** Estimated cost: ~$0.0001 per drill
**And** 1000 drills = ~$0.10
**And** At 1 request per 5 min = max 288 requests/day = ~$0.03/day
**And** Max monthly cost: ~$1.00 (well within budget)

**Given** rate limit configuration
**When** defining settings
**Then** Add to settings.py:
  - auto_tag_enabled: bool = True
  - auto_tag_rate_limit_seconds: int = 300 (5 minutes)
  - auto_tag_cost_alert_threshold: float = 5.0 (dollars per month)
**And** Allow disabling auto-tagging entirely if needed

### Story 7.3: Tag Augmentation (Never Replace User Tags)

As a developer,
I want AI tags to augment user tags, never replace them,
So that user expertise is always preserved and respected.

**Acceptance Criteria:**

**Given** tag augmentation model (FR27, NFR29)
**When** AI generates tags
**Then** AI tags are ADDED to existing drill_tags
**And** User-provided tags are NEVER removed or modified
**And** User tags take precedence in display order

**Given** tag metadata storage
**When** storing tags in database
**Then** drill_tags remains a simple string array (no complex structure)
**And** Tag source is tracked separately in tag_metadata JSON field:
  - tag_metadata: {"butterfly": "user", "quick-recovery": "ai", "lateral-movement": "user"}
**And** Metadata allows distinguishing user vs AI tags in UI

**Given** database schema update
**When** adding tag metadata support
**Then** Add tag_metadata column to content table:
  - ALTER TABLE content ADD COLUMN tag_metadata TEXT (JSON)
**And** Column stores JSON object mapping tag -> source
**And** Migration runs automatically on app start

**Given** drill save with user tags
**When** user saves drill via Discord bot with tags
**Then** User-provided tags are stored in drill_tags
**And** tag_metadata marks them as "user": {"butterfly": "user", "warmup": "user"}
**And** User tags are sacred (NFR29)

**Given** auto-tagging trigger (FR28)
**When** drill is saved via Discord bot
**Then** After drill is saved to database
**And** After rate limit check passes
**And** Call generate_tags(drill.title, drill.description)
**And** Merge AI tags with existing drill_tags
**And** Update tag_metadata for AI tags: {"quick-recovery": "ai"}

**Given** tag merging logic
**When** combining user and AI tags
**Then** Start with existing drill_tags (user tags)
**And** Add AI tags that don't already exist (case-insensitive check)
**And** Preserve user tag order (user tags first)
**And** Append AI tags after user tags
**And** Deduplicate (don't add AI tag if user already provided it)

**Given** example tag augmentation
**When** user provides tags: ["butterfly", "warmup"]
**And** AI suggests tags: ["quick-recovery", "butterfly", "lateral-movement"]
**Then** Final drill_tags: ["butterfly", "warmup", "quick-recovery", "lateral-movement"]
**And** tag_metadata: {"butterfly": "user", "warmup": "user", "quick-recovery": "ai", "lateral-movement": "ai"}
**And** "butterfly" not duplicated (user version kept)

**Given** updating drill with AI tags
**When** auto-tagging completes
**Then** UPDATE content SET drill_tags = ?, tag_metadata = ? WHERE id = ?
**And** Database transaction ensures atomic update
**And** Query invalidation triggers in frontend (TanStack Query)

**Given** user edits tags later
**When** user adds or removes tags via TagManager (Story 3.4)
**Then** All tags (user and AI) can be removed
**And** Newly added tags are marked as "user" in tag_metadata
**And** Removed AI tags are deleted from drill_tags and tag_metadata
**And** User has full control over final tag set

### Story 7.4: Visual Distinction for AI Tags in UI

As a coach,
I want to see which tags are AI-generated vs user-provided,
So that I can trust user expertise while benefiting from AI suggestions.

**Acceptance Criteria:**

**Given** TagManager component update
**When** displaying tags in Story 3.4 component
**Then** Fetch tag_metadata along with drill data
**And** Determine source for each tag: user or AI
**And** Render tags with different styles based on source

**Given** user tag styling
**When** rendering user-provided tags
**Then** Display with standard chip styling (from Story 3.4)
**And** Background: gray-100 or blue-50
**And** Text: gray-800, normal weight
**And** Border: none or subtle
**And** Position: displayed first in tag list

**Given** AI tag styling
**When** rendering AI-generated tags
**Then** Display with distinct but subtle styling:
  - Background: blue-50 or gray-50 (lighter than user tags)
  - Text: gray-600, italic font style
  - Small "AI" badge or icon (Sparkles icon from Lucide)
  - Border: dashed (optional, to distinguish further)
**And** Position: displayed after user tags

**Given** AI tag badge
**When** showing AI indicator
**Then** Small "AI" text badge OR Sparkles icon (⚡)
**And** Badge is subtle (8-10px text or small icon)
**And** Badge color: blue-500 or gray-500
**And** Badge appears before tag text: "⚡ quick-recovery"
**And** Or as small superscript: "quick-recovery ᴬᴵ"

**Given** tag ordering
**When** displaying all tags
**Then** User tags appear first (left side)
**And** AI tags appear after user tags
**And** Within each group, tags are sorted alphabetically (optional)
**And** Clear visual separation (user expertise first - UX principle)

**Given** tooltip explanation (optional)
**When** hovering over AI tag
**Then** Tooltip displays: "AI-suggested tag"
**And** Tooltip explains: "You can remove this if it's not relevant"
**And** Helps user understand AI tag functionality

**Given** DrillCard component (Story 2.2)
**When** showing tags on drill cards
**Then** Display 1-2 user tags first (if available)
**And** Optionally show 1 AI tag if space permits
**And** AI tags have subtle indicator (small sparkles icon)
**And** Progressive disclosure: full tag list in DrillDetail

**Given** accessibility
**When** using screen readers
**Then** AI tags have aria-label: "AI-suggested tag: {tag_name}"
**And** User tags have aria-label: "Tag: {tag_name}"
**And** Visual distinction is also conveyed via text

### Story 7.5: Accept/Reject AI Tags Functionality

As a coach,
I want to easily remove AI-generated tags that aren't relevant,
So that my drill library stays accurately organized.

**Acceptance Criteria:**

**Given** AI tag removal (FR29)
**When** viewing TagManager in DrillDetail
**Then** Each AI tag has X button (same as user tags from Story 3.4)
**And** Clicking X removes AI tag immediately
**And** Removal works identically to user tag removal
**And** No confirmation needed (quick action)

**Given** removing AI tag
**When** I click X on AI tag
**Then** Tag is removed from drill_tags array
**And** Tag is removed from tag_metadata
**And** PUT /api/v1/content/{id}/metadata is called
**And** Update is optimistic (immediate UI update)
**And** Query cache is invalidated

**Given** converting AI tag to user tag (implicit)
**When** user keeps AI tag (doesn't remove it)
**Then** Tag remains in drill_tags
**And** tag_metadata preserves source: "ai"
**And** Or optionally: after 30 days, AI tags convert to "user" (acceptance by inaction)
**And** Or: explicit "Accept All AI Tags" button

**Given** "Accept All AI Tags" button (optional enhancement)
**When** drill has AI tags
**Then** Button displays above tags: "Keep all AI suggestions"
**And** Clicking button marks all AI tags as "user" in tag_metadata
**And** Visual distinction is removed (all tags styled as user tags)
**And** Button disappears after acceptance

**Given** "Remove All AI Tags" button (optional enhancement)
**When** drill has multiple AI tags
**Then** Button displays: "Remove all AI suggestions"
**And** Clicking button removes all AI tags at once
**And** Confirmation dialog: "Remove all {count} AI-suggested tags?"
**And** Batch removal API call or multiple mutations

**Given** adding tags after auto-tagging
**When** user manually adds tags
**Then** Newly added tags are marked as "user" in tag_metadata
**And** New user tags appear in user tag section (before AI tags)
**And** TagManager continues to work as in Story 3.4

**Given** tag source persistence
**When** tag metadata is updated
**Then** Database stores tag source reliably (NFR28)
**And** Tag source survives drill edits
**And** Tag source is included in drill exports (future feature)

**Given** Discord bot integration
**When** drill is captured via Discord bot
**Then** User can provide initial tags via bot command
**And** User tags are marked as "user" immediately
**And** Auto-tagging runs after save (rate limit permitting)
**And** AI tags are added without user confirmation (augmentation model)
**And** User can review/remove AI tags in web UI later

**Given** notification of AI tags (optional)
**When** AI tags are added to drill
**Then** Optional: Discord bot sends message: "Added {count} AI-suggested tags to your drill"
**And** Or: web UI shows toast on next visit: "New AI tags suggested"
**And** Non-intrusive notification respects user attention

---

## Epic 8: Web-Based Drill Capture

**Epic Goal:** Coaches can add drills directly from the web UI by pasting URLs, in addition to using the Discord bot. The system extracts metadata and provides guided metadata collection forms.

**FRs Covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8
**NFRs:** NFR6-NFR11 (platform API integration), NFR16-NFR18 (Discord bot integration maintained)

### Story 8.1: AddDrillModal Component & UI

As a coach,
I want to add drills from the web interface by pasting URLs,
So that I can quickly capture drills without using Discord bot.

**Acceptance Criteria:**

**Given** Library page
**When** I add "Add Drill" button
**Then** Button is prominently displayed near search bar or top-right
**And** Button uses ice-blue background color (primary CTA)
**And** Button label: "Add Drill" or "+ Add Drill"
**And** Button icon: Plus or PlusCircle (Lucide)

**Given** "Add Drill" button click
**When** user clicks button
**Then** AddDrillModal opens
**And** Modal uses shadcn/ui Dialog component
**And** Modal is centered on screen
**And** Overlay darkens background
**And** Modal is responsive (full-screen on mobile)

**Given** AddDrillModal component
**When** I create src/components/drills/AddDrillModal.tsx
**Then** Component manages multi-step form state
**And** Step 1: URL input
**And** Step 2: Metadata extraction (loading)
**And** Step 3: Guided metadata form
**And** Component tracks current step

**Given** URL input field
**When** displaying Step 1
**Then** Large text input for URL
**And** Placeholder: "Paste drill URL (YouTube, Reddit, Instagram, TikTok)"
**And** Input has focus on modal open (auto-focus)
**And** Paste icon button for convenience (triggers navigator.clipboard)
**And** Help text: "Supported platforms: YouTube, Reddit, Instagram, TikTok"

**Given** URL input interaction
**When** user pastes or types URL
**Then** Input accepts full URLs
**And** Input shows character count if needed
**And** Input validates format on blur (not on every keystroke)
**And** Next button appears when URL is entered

**Given** modal footer
**When** displaying action buttons
**Then** Shows Cancel and Next/Submit buttons
**And** Cancel button closes modal without saving
**And** Next button proceeds to next step (Step 1 → Step 2)
**And** Submit button saves drill (Step 3)
**And** Buttons are disabled during loading states

**Given** mobile layout
**When** viewing on mobile
**Then** Modal takes full screen (100vh)
**And** URL input is large enough for mobile keyboards
**And** Touch-friendly button sizes (min 44px height)

### Story 8.2: URL Validation & Platform Detection

As a coach,
I want the system to validate my URL and detect the platform,
So that I know if the drill can be captured.

**Acceptance Criteria:**

**Given** URL validation
**When** user enters URL and clicks Next
**Then** Validate URL format (valid HTTP/HTTPS URL)
**And** Check URL matches supported platform patterns:
  - YouTube: youtube.com/watch, youtu.be/
  - Reddit: reddit.com/r/, redd.it/
  - Instagram: instagram.com/p/, instagram.com/reel/
  - TikTok: tiktok.com/@, vm.tiktok.com/
**And** Display validation error if URL is invalid

**Given** invalid URL format
**When** URL doesn't match any pattern
**Then** Error displays below input: "Please enter a valid URL from YouTube, Reddit, Instagram, or TikTok"
**And** Next button remains disabled
**And** Error is red text with warning icon
**And** User can correct URL and retry

**Given** valid URL entered
**When** URL matches supported platform
**Then** Platform is detected automatically
**And** Platform preview displays:
  - Platform name: "YouTube", "Reddit", etc.
  - Platform icon (SourceBadge from Story 2.4)
  - Confirmation: "✓ Valid YouTube URL"
**And** Next button becomes enabled

**Given** platform detection preview
**When** showing detected platform
**Then** Display near URL input (below or to the right)
**And** Use hockey-blue checkmark icon for valid
**And** Show platform badge with brand color
**And** Build user confidence before proceeding

**Given** unsupported platform
**When** URL is from different site (e.g., Facebook, Twitter)
**Then** Error displays: "This platform is not supported yet. Supported: YouTube, Reddit, Instagram, TikTok"
**And** Next button remains disabled
**And** Suggest using Discord bot as alternative (optional)

**Given** Next button clicked
**When** URL is valid and platform detected
**Then** Proceed to Step 2 (metadata extraction)
**And** URL is locked (display-only in subsequent steps)
**And** User can go back to edit URL if needed

### Story 8.3: Metadata Extraction & Auto-Population

As a coach,
I want the system to automatically fetch drill details from the URL,
So that I don't have to manually enter title, author, and description.

**Acceptance Criteria:**

**Given** Step 2: Metadata extraction
**When** user proceeds from URL input
**Then** Modal displays loading state
**And** Loading message: "Fetching drill details..."
**And** Loading spinner is visible
**And** Progress indicator (optional): "Extracting metadata from {platform}..."

**Given** useCreateDrill hook
**When** I create src/hooks/useCreateDrill.ts
**Then** Hook uses TanStack Query useMutation
**And** Hook calls POST /api/v1/content
**And** Request body includes:
  - url: string
  - source: ContentSource (detected platform)
  - Optional overrides: title, description, drill_tags, difficulty, age_group, equipment
**And** Hook returns { mutate, data, isLoading, isError, error }

**Given** metadata extraction API call
**When** POST /api/v1/content is called with URL
**Then** Backend ingestor fetches content from URL (Story 1.2 - backend already implemented)
**And** Extracts available metadata: title, author, description, thumbnail_url, published_at, view_count, etc.
**And** Returns ContentItem response
**And** Extraction completes in <5 seconds (most platforms are fast)

**Given** YouTube metadata extraction (FR3)
**When** URL is from YouTube
**Then** Extracts: title, author (channel name), description, thumbnail, view count, published date
**And** All fields auto-populate in form
**And** Extraction is reliable (YouTube API works well)

**Given** Reddit metadata extraction (FR3)
**When** URL is from Reddit
**Then** Extracts: title, author (username), description (post text), thumbnail (if image/video post)
**And** Auto-populated fields are editable in form

**Given** Instagram metadata extraction (FR3, NFR11)
**When** URL is from Instagram
**Then** Attempts extraction via oEmbed or scraping
**And** May only get partial metadata (title might be missing)
**And** Fallback: User provides title and description manually
**And** Placeholder displays (pink gradient) instead of thumbnail

**Given** TikTok metadata extraction (FR3, NFR11)
**When** URL is from TikTok
**Then** Attempts extraction via oEmbed
**And** May only get partial metadata
**And** Fallback: User provides title and description manually
**And** Placeholder displays (black with cyan icon) instead of thumbnail

**Given** successful metadata extraction
**When** backend returns drill data
**Then** Proceed to Step 3 (guided metadata form)
**And** Auto-populate form fields with extracted data
**And** Show preview: thumbnail, title, author
**And** User can edit all fields before saving

**Given** extraction error (NFR10, NFR14)
**When** API call fails or returns 404
**Then** Error message displays: "Could not fetch drill details. Please enter details manually."
**And** Proceed to Step 3 with empty form (manual entry)
**And** User can still save drill with manual metadata
**And** Error is logged for debugging

**Given** extraction timeout
**When** API takes too long (>10 seconds)
**Then** Show error: "Extraction timed out. Please try again or enter details manually."
**And** Provide Retry button
**And** Or proceed to manual entry

### Story 8.4: Guided Metadata Collection Forms

As a coach,
I want to provide drill-specific metadata like tags, difficulty, and age group,
So that my drill is properly organized in my library.

**Acceptance Criteria:**

**Given** Step 3: Metadata form
**When** displaying guided form
**Then** Form shows sections:
  1. Basic Info (title, description - from extraction)
  2. Drill Details (drill_description, drill_tags, difficulty, age_group, equipment)
**And** All fields are editable
**And** Form is scrollable if content is long

**Given** Basic Info section
**When** showing extracted metadata
**Then** Title field is pre-filled (editable)
**And** Description field is pre-filled (editable, textarea)
**And** Author is display-only (not editable)
**And** Thumbnail preview displays if available

**Given** Instagram/TikTok fallback (NFR11)
**When** extraction provided no title/description
**Then** Title field is empty with placeholder: "Enter drill title"
**And** Description field is empty with placeholder: "Describe this drill"
**And** Fields are required (validation)
**And** Help text: "Since {platform} doesn't allow automatic extraction, please provide details manually"

**Given** Drill Description field (FR4)
**When** coach provides custom description
**Then** Textarea for drill_description (separate from auto-fetched description)
**And** Placeholder: "Add your coaching notes about this drill..."
**And** Optional field (can be empty)
**And** Multi-line, min 3 rows

**Given** Tags field (FR5)
**When** entering tags
**Then** Tag input component (similar to TagManager Story 3.4)
**And** Enter tags one at a time, press Enter to add
**And** Placeholder: "Add tags... (e.g., butterfly, warmup)"
**And** Show added tags as removable chips
**And** Tag suggestions (optional): common tags from existing drills

**Given** Difficulty dropdown (FR6)
**When** selecting difficulty
**Then** Select dropdown with options:
  - None (default)
  - Beginner
  - Intermediate
  - Advanced
**And** Optional field
**And** Visual preview: show DifficultyBadge color

**Given** Age Group dropdown (FR7)
**When** selecting age group
**Then** Select dropdown with options:
  - None (default)
  - Mite
  - Squirt
  - Peewee
  - Bantam
  - Midget
  - Junior
  - Adult
**And** Optional field

**Given** Equipment field (FR8)
**When** entering equipment requirements
**Then** Text input for equipment
**And** Placeholder: "e.g., pucks, cones, nets"
**And** Optional field
**And** Suggestions (optional): pucks, cones, nets, sticks, goalie pads

**Given** form validation
**When** user attempts to submit
**Then** Required fields: title (if not extracted)
**And** Optional validation: tags max length, description max length
**And** Display validation errors inline below fields
**And** Disable Submit button if validation fails

**Given** form preview (optional enhancement)
**When** form is filled
**Then** Show mini preview card of how drill will appear
**And** Preview uses DrillCard component
**And** Builds confidence before saving

### Story 8.5: Success/Error Handling & Integration

As a coach,
I want to see confirmation when my drill is added,
So that I know it's saved and can continue capturing more drills.

**Acceptance Criteria:**

**Given** Submit button clicked
**When** user completes form and clicks Submit
**Then** useCreateDrill.mutate() is called
**And** POST /api/v1/content is sent with all metadata
**And** Loading state displays: spinner on Submit button
**And** Form inputs are disabled during submission

**Given** successful drill creation
**When** API returns 201 Created
**Then** Modal closes automatically
**And** Success toast notification: "Drill added to your library!"
**And** New drill appears in library grid immediately (optimistic update)
**And** Query cache invalidates: ['content']
**And** Grid scrolls to show new drill (optional)

**Given** optimistic update
**When** drill is submitted
**Then** Drill is added to grid before API response
**And** If API fails, drill is removed from grid
**And** TanStack Query handles rollback automatically

**Given** API error during submission
**When** POST /api/v1/content fails
**Then** Error toast displays: "Failed to add drill. Please try again."
**And** Modal remains open (don't lose form data)
**And** Submit button re-enables (user can retry)
**And** Error details logged for debugging

**Given** duplicate drill detection (optional)
**When** URL already exists in library
**Then** Backend returns 409 Conflict
**And** Error message: "This drill is already in your library"
**And** Optionally: offer to view existing drill
**And** User can cancel or force re-add

**Given** query cache invalidation
**When** drill is successfully added
**Then** Invalidate ['content'] query (library list)
**And** Refetch library data to include new drill
**And** Ensure consistent state across components

**Given** "Add Another" workflow (optional)
**When** drill is successfully added
**Then** Show "Add Another Drill" button in success toast
**And** Clicking reopens AddDrillModal with empty form
**And** Enables rapid drill capture workflow

**Given** integration with auto-tagging (Epic 7)
**When** drill is saved via web UI
**Then** Auto-tagging is triggered (if rate limit allows)
**And** AI tags are added asynchronously
**And** User sees AI tags appear after a few seconds (or on next load)
**And** Auto-tagging doesn't block drill save

**Given** integration with Discord bot (NFR16-NFR18)
**When** drill is captured via web UI
**Then** Drill is saved to same database as Discord bot
**And** Discord bot captures and web UI captures are equivalent
**And** Both workflows produce identical data structure
**And** Drills from both sources appear in unified library

**Given** mobile optimization
**When** using AddDrillModal on mobile
**Then** Keyboard doesn't obscure input fields
**And** Form scrolls to keep current field visible
**And** Modal is dismissable with swipe gesture (optional)
**And** Touch targets are large enough (44px minimum)

**Given** empty library onboarding
**When** library is empty (Story 2.5)
**Then** EmptyState includes "Add Drill" CTA button
**And** Clicking opens AddDrillModal
**And** First-time user can easily add their first drill
**And** Clear call-to-action for getting started

---

## 🎉 ALL EPICS COMPLETE!

**Total Epics:** 8
**Total Stories:** 40
**Total FRs Covered:** 50/50 (100%)
**Total NFRs Covered:** 36/36 (100%)

### Epic Summary:

1. ✅ **Epic 1: Project Foundation & Core Infrastructure** (5 stories - FR9, FR47)
2. ✅ **Epic 2: Drill Library Browsing & Display** (5 stories - FR34-36, FR41-46, FR48-50)
3. ✅ **Epic 3: Drill Detail View & Management** (5 stories - FR10-15, FR37-39)
4. ✅ **Epic 4: Advanced Filtering System** (5 stories - FR19-25)
5. ✅ **Epic 5: Semantic Search** (5 stories - FR16-18)
6. ✅ **Epic 6: Similar Drill Recommendations** (5 stories - FR30-33, FR40)
7. ✅ **Epic 7: AI-Powered Auto-Tagging** (5 stories - FR26-29)
8. ✅ **Epic 8: Web-Based Drill Capture** (5 stories - FR1-8)

### Ready for Implementation!

All requirements from your PRD, UX Design, and Architecture have been broken down into implementation-ready stories with comprehensive acceptance criteria. Each story is sized for a single dev agent execution and includes specific, testable criteria.

**Next Steps:**
1. Run Implementation Readiness Review (if needed)
2. Sprint Planning to organize stories into sprints
3. Begin implementation with Epic 1

---

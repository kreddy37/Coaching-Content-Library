---
project_name: 'Coaching-content-library'
user_name: 'Kohl'
date: '2026-01-24'
sections_completed: ['technology_stack', 'language_specific_rules', 'framework_specific_rules', 'testing_rules', 'code_quality_rules', 'workflow_rules', 'critical_rules']
status: 'complete'
rule_count: 108
optimized_for_llm: true
existing_patterns_found: 15
architecture_integration: true
last_updated: '2026-01-24'
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

### Frontend (React Web App)
- React 19.2.0 with TypeScript 5.9.3 (~patch updates only)
- Vite 7.2.4 (build tool, dev server on port 3000)
- TanStack Query 5.90.16 (server state management)
- React Router DOM 7.11.0 (routing)
- Tailwind CSS 4.1.18 with PostCSS 8.5.6 (v4 API, different from v3)
- Axios 1.13.2 (HTTP client)
- Radix UI components (shadcn/ui primitives)
- Lucide React 0.562.0 (icons)
- ESLint 9.39.1 with typescript-eslint 8.46.4

### Backend (Python Platform)
- Python 3.12 with FastAPI 0.104.0+
- Uvicorn 0.24.0+ (ASGI server)
- Pydantic 2.0+ with pydantic-settings 2.0+
- SQLAlchemy 2.0+ (database ORM)
- HTTPX 0.26.0+ (async HTTP client)
- google-api-python-client 2.0+ (YouTube API)
- praw 7.7.0+ (Reddit API)
- discord.py 2.3.0+ (Discord bot)
- Typer with [all] extras (CLI)

### AI Services
- ChromaDB (vector database for semantic search and embeddings storage)
- OpenAI API:
  - text-embedding-3-small (1536 dimensions for vector embeddings)
  - GPT-4o-mini (LLM for auto-tagging drill content)
- tenacity (Python retry library for resilient API calls with exponential backoff)

### Deployment & Infrastructure
- Vercel (frontend static hosting with automatic HTTPS and git-based deploys)
- Caddy (reverse proxy with automatic Let's Encrypt SSL for backend)
- Proxmox (self-hosted backend infrastructure with dynamic DNS)

### Configuration Notes
- Vite proxy: `/api` → `http://localhost:8000` (development)
- TypeScript strict mode with enhanced linting enabled
- Custom Tailwind theme: `hockey-blue` (#1e3a5f), `ice-blue` (#38bdf8)
- Path alias: `@/*` → `./src/*`
- ChromaDB persistence: `./chroma_data/` directory (backend)
- Frontend centralized config: `src/lib/config.ts` for environment variables
- Frontend routes: `src/routes.tsx` for centralized route configuration

---

## Critical Implementation Rules

### Language-Specific Rules

#### Frontend (TypeScript/React)

**Configuration Requirements:**
- TypeScript strict mode ENABLED with additional linting: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`
- Module resolution: `"bundler"` (Vite-specific)
- JSX: `"react-jsx"` (automatic React import)

**Import/Export Patterns:**
- ALWAYS use `@/` path alias for local imports - NEVER use relative paths like `../../`
- Use explicit type imports: `import type { ContentItem } from '@/lib/types'`
- Named exports preferred over default exports

**Environment Variables - Centralized Config Pattern:**
- NEVER use `import.meta.env` directly in components
- ALWAYS use centralized config from `src/lib/config.ts`:
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
- Import: `import { config } from '@/lib/config'`
- Use: `const apiUrl = config.apiUrl`

**CRITICAL BACKEND CONTRACT - Type System:**
- Backend enums use **PascalCase**: `'YouTube' | 'Reddit' | 'Instagram' | 'TikTok'` (NOT lowercase!)
- Backend API uses **snake_case** field names: `drill_tags`, `drill_description`, `content_type`, `published_at`
- Frontend types MUST match backend exactly - DO NOT rename to camelCase
- Use `| null` for nullable fields (backend returns null, not undefined)

**Critical Field Names (MUST MATCH BACKEND):**
- ✅ `drill_tags` - ❌ NOT "tags"
- ✅ `drill_description` - ❌ NOT "notes" or "description"
- ✅ `content_type` - ❌ NOT "contentType"
- ✅ `'YouTube'` (PascalCase) - ❌ NOT `'youtube'`

#### Backend (Python/FastAPI)

**Module Structure:**
- Use absolute imports from `src` package root: `from ..models.content import ContentItem`
- Directory structure: `src/ingestors/`, `src/models/`, `src/api/`

**Pydantic Models:**
- Use `Field(default_factory=...)` for mutable defaults (lists, dicts)
- Enum values MUST be PascalCase strings: `"YouTube"`, `"Video"`, `"Reddit"`
- Use `Optional[type]` for nullable fields
- Use `Config.from_attributes = True` for ORM compatibility

**FastAPI Patterns:**
- Routes use `async def` handlers
- Use `HTTPException` with proper status codes (404, 400, 201, etc.)
- Response models: `response_model=SomeResponse, status_code=201`
- Query parameters: `Query(None, description="...")` for optional filters

**Critical Enum Pattern:**
```python
class ContentSource(str, Enum):
    YOUTUBE = "YouTube"    # NOT "youtube"
    REDDIT = "Reddit"      # PascalCase required
```

**Repository Pattern:**
- Always check if content exists before operations
- Delete requires both source and ID: `repository.delete(content.source, content.id)`

**AI Services Integration (NEW):**

**ChromaDB Service Pattern:**
- Single collection name: `"coaching_drills"` (NEVER create multiple collections)
- Persistence directory: `./chroma_data/` (relative to backend root)
- Initialize on app startup: `get_or_create_collection()` pattern
- Document IDs MUST map to SQLite drill primary keys (string conversion)
- Use `PersistentClient` with path, NOT in-memory client

**OpenAI API Integration Pattern:**
- ALWAYS use `@retry` decorator with `tenacity`:
  - `stop=stop_after_attempt(3)` - exactly 3 retry attempts
  - `wait=wait_exponential(multiplier=1, min=2, max=10)` - exponential backoff
- ALWAYS set timeouts:
  - Embeddings: `timeout=30` seconds
  - LLM calls: `timeout=60` seconds
- ALWAYS implement graceful degradation:
  ```python
  try:
      result = await openai_call()
      return result
  except Exception as e:
      logger.error(f"OpenAI call failed: {e}")
      return None  # Allow operation to continue without AI
  ```

**Rate Limiting Pattern (LLM calls):**
- Global in-memory tracking: `last_llm_call: Optional[datetime] = None`
- Minimum interval: `timedelta(minutes=5)`
- Check before call: `if not can_call_llm(): raise HTTPException(429, ...)`
- Record after success: `last_llm_call = datetime.now()`
- NEVER bypass rate limiting - prevents cost runaway

**Service Layer Structure:**
- AI services in `src/services/` directory:
  - `vector_service.py` - ChromaDB operations ONLY
  - `embedding_service.py` - OpenAI embeddings ONLY
  - `tagging_service.py` - OpenAI LLM with rate limiting
  - `recommendation_service.py` - Combined similarity (tag + semantic)
- NEVER access ChromaDB directly from routes - always through vector_service
- NEVER call OpenAI API directly from routes - always through service layer

### Framework-Specific Rules

#### Frontend (React + TanStack Query)

**React Hooks Usage:**
- Use TanStack Query hooks for all server state: `useQuery`, `useMutation`
- Custom hooks pattern: `useContentList`, `useContentItem`, `useCreateContent`
- Query keys: `['content', params]` or `['content', source, id]`
- Invalidate after mutations: `queryClient.invalidateQueries({ queryKey: ['content'] })`

**Component Props Interface Pattern (REQUIRED - NEW):**
- ALWAYS export props interfaces separately:
  ```typescript
  export interface DrillCardProps {
    drill: ContentItem;
    onClick: () => void;
  }

  export function DrillCard({ drill, onClick }: DrillCardProps) {
    return <div onClick={onClick}>{drill.title}</div>;
  }
  ```
- NEVER use inline props without exported interface
- ❌ WRONG: `function DrillCard(props: { drill: ContentItem }) { ... }`
- This enables type reusability and better autocomplete

**Form State Pattern (REQUIRED - NEW):**
- Use form object state matching API payload structure:
  ```typescript
  const [formData, setFormData] = useState({
    url: '',
    drill_description: '',
    drill_tags: []
  });

  // Direct pass to API - no transformation needed
  createDrill.mutate(formData);
  ```
- NEVER use individual state for each field
- ❌ WRONG: `const [url, setUrl] = useState(''); const [description, setDescription] = useState('');`

**Component Structure:**
- shadcn/ui components in `src/components/ui/`
- Feature components by domain: `src/components/drills/`, `src/components/search/`
- Export named functions: `export function DrillCard({ ... }) { ... }`

**TanStack Query Patterns:**
- Enable conditionally: `enabled: !!source && !!id`
- Extract data in component: `const { data, isLoading, error } = useContentList()`
- Mutations return promises: `.then(res => res.data)`
- Always handle loading, error, and empty states

**TanStack Query Global Error Handling (NEW):**
- Configure global error handler in QueryClient setup (App.tsx):
  ```typescript
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes
        retry: 1,
        onError: (error) => {
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
- Component-level override when needed: `useQuery({ ..., onError: (err) => customHandler(err) })`

**Styling with Tailwind:**
- Custom theme colors: `hockey-blue`, `ice-blue`
- Use `cn()` from `@/lib/utils` for conditional classes
- Source colors: YouTube (red-600), Reddit (orange-500), Instagram (pink-500), TikTok (black)
- Difficulty colors: beginner (green-500), intermediate (amber-500), advanced (red-500)

**React Router (NEW PATTERN):**
- ALL routes in `src/routes.tsx` file - NEVER inline in App.tsx:
  ```typescript
  // src/routes.tsx
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

  // src/App.tsx
  function App() {
    const element = useRoutes(routes);
    return element;
  }
  ```
- ❌ WRONG: Inline routes in App.tsx with `<Routes><Route>` JSX
- Pages in `src/pages/` directory
- Layout uses `<Outlet />` for child routes

#### Backend (FastAPI + SQLAlchemy)

**API Route Organization:**
- Routes in `src/api/routes.py` with `APIRouter(tags=["content"])`
- Mount in main: `app.include_router(router, prefix="/api/v1")`

**New API Endpoints (AI Features):**
- `POST /api/v1/search` - Semantic search using vector embeddings
- `GET /api/v1/content/{id}/similar` - Similar drills (tag + semantic similarity)
- `POST /api/v1/content/{id}/auto-tag` - Trigger AI auto-tagging (rate limited)

**Structured Error Response Pattern (NEW):**
- ALWAYS use structured errors for consistency:
  ```python
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
  raise_structured_error(
      code="RATE_LIMIT_EXCEEDED",
      message="LLM call rate limit exceeded (max 1 per 5 minutes)",
      status_code=429
  )
  ```
- Error codes: `CONTENT_NOT_FOUND`, `INVALID_SOURCE_PLATFORM`, `RATE_LIMIT_EXCEEDED`, `EXTERNAL_API_FAILURE`

**Dependency Pattern:**
- Ingestors/repository initialized at module level
- Dictionary lookup: `ingestors.get(request.source)`

**Request/Response Flow:**
1. Validate with Pydantic model
2. Get ingestor/repository
3. Perform operation
4. Return response or raise HTTPException
5. Status codes: 200 (GET), 201 (POST), 204 (DELETE), 404, 400

**Ingestor Pattern:**
- Inherit from `BaseIngestor` with abstract `from_url()`
- Returns `ContentItem` or `None`
- Platform credentials passed to constructor

**Settings:**
- Use `pydantic-settings` with `.env` file
- Access: `settings.youtube_api_key`

### Testing Rules

#### Backend (Python/pytest)

**Test Organization:**
- Tests in `tests/` directory mirroring `src/` structure
- Test files: `test_*.py` pattern (e.g., `test_api.py`, `test_youtube.py`)
- Test classes: `TestCamelCase` grouping related tests
- Test methods: `test_snake_case_description` pattern
- Main block: `if __name__ == "__main__": pytest.main([__file__, "-v"])`

**Mock Usage:**
- Use `@patch` decorator for mocking: `@patch('src.api.routes.repository')`
- Mock pattern: Decorator creates parameter in reverse order: `def test(mock_repo, mock_ingestors)`
- Set return values: `mock_obj.method.return_value = result`
- Verify calls: `mock_obj.method.assert_called_once()` or `assert_called_once_with(args)`
- FastAPI testing: `TestClient(app)` for integration tests

**Test Coverage Requirements:**
- Test all HTTP methods per endpoint: GET, POST, PUT, DELETE
- Test success cases AND error cases (404, 400, 201, etc.)
- Test with filters, metadata overrides, partial updates
- Test edge cases: empty results, not found, unsupported sources
- Verify repository/service calls with correct parameters

**Integration vs Unit Test Boundaries:**
- Integration: Use `TestClient` for full API tests with mocked repository/ingestors
- Unit: Test ingestors individually (e.g., `test_youtube.py`)
- Mock at module boundaries (repository, ingestors, external APIs)
- Don't mock Pydantic models or internal logic

**AI Services Testing (NEW):**

**Vector Service Tests:**
- Mock ChromaDB client: `@patch('src.services.vector_service.chromadb')`
- Test collection initialization: Verify `get_or_create_collection()` called with `"coaching_drills"`
- Test vector operations: add, query, delete with proper document IDs
- Verify document IDs match SQLite drill primary keys (string conversion)
- Test persistence directory: Verify `./chroma_data/` path used

**Embedding Service Tests:**
- Mock OpenAI API: `@patch('src.services.embedding_service.openai')`
- Test retry behavior: Verify 3 attempts with exponential backoff on failure
- Test timeout configuration: Verify 30-second timeout set correctly
- Test graceful degradation: Verify returns `None` on API failure (not exception)
- Verify embedding dimensions: 1536 for text-embedding-3-small

**Tagging Service Tests:**
- Mock OpenAI API: `@patch('src.services.tagging_service.openai')`
- Test rate limiting:
  - Verify `can_call_llm()` checked before API call
  - Verify 429 error when rate limit exceeded (within 5 minutes)
  - Verify timestamp recorded after successful call
- Test retry behavior: Verify 3 attempts with exponential backoff
- Test timeout: Verify 60-second timeout for LLM calls
- Test graceful degradation: Verify returns empty list on failure (user tags preserved)
- Verify NEVER overwrites user-provided tags (augments only)

**Recommendation Service Tests:**
- Mock vector service and tag similarity calculations
- Test combined scoring: Verify tag-based + semantic similarity weighted properly
- Test ranking: Verify top N results returned in correct order
- Test edge cases: Empty results, single result, no semantic matches
- Verify calls to vector_service for semantic similarity

#### Frontend (React/TypeScript)

**Test Organization (when implemented):**
- Expected pattern: `src/**/*.test.tsx` or `src/**/*.spec.tsx`
- Use Vitest (Vite standard) or Jest for unit/component tests
- React Testing Library for component tests
- Test TanStack Query hooks with proper query client wrapper

### Code Quality & Style Rules

#### Frontend (TypeScript/React)

**ESLint Configuration:**
- Flat config with recommended rules: `@eslint/js`, `typescript-eslint`, `react-hooks`, `react-refresh`
- Files: `**/*.{ts,tsx}`
- Global ignore: `dist/`
- ECMAVersion: 2020, browser globals

**File Naming:**
- Components: PascalCase (e.g., `DrillCard.tsx`, `Header.tsx`)
- Utilities/hooks: camelCase (e.g., `utils.ts`, `useContent.ts`)
- Directories: lowercase, feature-based (e.g., `drills/`, `layout/`, `search/`)
- Pages: PascalCase (e.g., `Library.tsx`, `Planner.tsx`)

**Code Organization:**
- `src/components/ui/` - shadcn/ui components ONLY
- `src/components/{feature}/` - Feature components (drills, search, planner, layout)
- `src/lib/` - Utilities, types, API client
  - `config.ts` - REQUIRED centralized environment variable config (NEW)
  - `api.ts` - Axios client
  - `types.ts` - Backend contract types
  - `utils.ts` - cn() helper and utilities
- `src/hooks/` - Custom React hooks
- `src/pages/` - Route pages
- `src/routes.tsx` - REQUIRED centralized route configuration (NEW)

**Centralized Patterns (NEW):**
- ALL environment variables accessed through `src/lib/config.ts` - NEVER direct `import.meta.env`
- ALL routes defined in `src/routes.tsx` - NEVER inline in App.tsx
- ALL component props interfaces exported separately - enables type reusability

**Utilities:**
- Use `cn()` from `@/lib/utils` for className merging (clsx + tailwind-merge)

#### Backend (Python/FastAPI)

**File Naming:**
- All files: snake_case (e.g., `content.py`, `test_api.py`)
- Directories: lowercase (e.g., `api/`, `ingestors/`, `models/`)

**Code Organization:**
- `src/api/` - FastAPI routes and API models
- `src/ingestors/` - Platform-specific content fetchers
- `src/models/` - Domain models (ContentItem, enums)
- `src/storage/` - Database repository layer
- `src/services/` - AI services layer (NEW)
  - `vector_service.py` - ChromaDB operations ONLY
  - `embedding_service.py` - OpenAI embeddings ONLY
  - `tagging_service.py` - OpenAI LLM with rate limiting
  - `recommendation_service.py` - Combined similarity engine
- `src/bot/` - Discord bot (separate concern)

**Service Boundary Rules (NEW):**
- Each service has single responsibility - NEVER mix concerns
- API routes NEVER call ChromaDB directly - always through vector_service
- API routes NEVER call OpenAI API directly - always through service layer
- Services NEVER call repository directly - pass data through routes
- Services focus on AI operations, repository focuses on SQLite operations
- Services are stateless except for rate limiting (global in-memory state)

**Documentation:**
- Docstrings for classes, complex functions, and API routes
- TypeScript types provide self-documentation on frontend
- No comments required for obvious code

### Development Workflow Rules

**Git/Repository (when initialized):**
- Project not yet in git, but .gitignore patterns are configured
- Frontend ignores: `node_modules`, `dist`, `.env`, `.vscode`, logs
- Backend ignores: `__pycache__`, `venv/`, `.env`, `*.db`, `.pytest_cache/`, `.coverage`
- NEVER commit `.env` files or secrets

**Environment Variables:**
- Both projects require `.env` files (not committed)
- Frontend: `VITE_API_URL` for backend connection (default: http://localhost:8000)
- Backend API credentials:
  - `youtube_api_key`, `reddit_client_id`, `reddit_client_secret`, `reddit_user_agent`
  - `OPENAI_API_KEY` - NEW for AI services (embeddings + LLM)
- `.env` files must be created manually after cloning

**Deployment Configuration (NEW):**

**Frontend Deployment (Vercel):**
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_URL` (production: Proxmox dynamic DNS domain)
- Automatic HTTPS with Vercel SSL
- Git-based deploys: Push to main triggers automatic build

**Backend Deployment (Self-Hosted Proxmox):**
- Run: `uvicorn src.api.main:app --host 0.0.0.0 --port 8000`
- Caddy reverse proxy for automatic HTTPS (Let's Encrypt)
- Dynamic DNS pointing to Proxmox public IP
- CORS configuration: Allow Vercel domain origin only
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://yourusername.vercel.app"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

**Hybrid Architecture Data Flow:**
```
User Browser → Vercel (React SPA) → Axios (HTTPS) → Caddy (Proxmox) → FastAPI → SQLite + ChromaDB
```

**Running Applications:**

Frontend:
- Dev: `npm run dev` (Vite dev server on port 3000)
- Build: `npm run build` (TypeScript compile + Vite build)
- Lint: `npm run lint`
- Preview: `npm run preview`

Backend:
- Dev: `uvicorn src.api.main:app --reload` (port 8000)
- Test: `pytest` or `pytest -v`
- Coverage: `pytest --cov=src`

**Setup Requirements:**
- Frontend: `npm install` after cloning
- Backend: Create venv, `pip install -r requirements.txt`, create `.env` with credentials
- ChromaDB: `./chroma_data/` directory created automatically on first run (NEW)

**BMAD Workflow System:**
- BMAD workflows in `_bmad/` directory
- Workflow outputs in `_bmad-output/`
- Use BMAD commands for planning and implementation tracking

### Critical Don't-Miss Rules

**CRITICAL Backend Contract Issues:**

❌ **NEVER use lowercase enum values**
```typescript
// WRONG - will break API communication
source: 'youtube', contentType: 'video'

// CORRECT - must match backend exactly
source: 'YouTube', contentType: 'Video'
```

❌ **NEVER rename backend fields to camelCase**
```typescript
// WRONG - backend doesn't recognize these
{ tags, notes, contentType, publishedAt }

// CORRECT - exact backend field names
{ drill_tags, drill_description, content_type, published_at }
```

❌ **NEVER confuse drill_tags with tags**
- Backend has BOTH `tags` (deprecated/unused) and `drill_tags` (active field)
- Always use `drill_tags` for drill-specific tagging

**Repository Pattern Gotchas:**

❌ **NEVER delete without checking existence first**
```python
# WRONG - will fail if content doesn't exist
repository.delete(source, id)

# CORRECT - check first, then delete with both parameters
content = repository.get(content_id)
if not content:
    raise HTTPException(status_code=404, ...)
repository.delete(content.source, content.id)  # Requires both!
```

**Frontend API Integration Issues:**

❌ **NEVER forget query invalidation after mutations**
```typescript
// WRONG - stale data in UI
await contentApi.create(data);

// CORRECT - invalidate to refetch
useMutation({
  mutationFn: (data) => contentApi.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['content'] });
  }
});
```

❌ **NEVER use relative imports when @/ alias exists**
```typescript
// WRONG: import { Button } from '../../components/ui/button';
// CORRECT: import { Button } from '@/components/ui/button';
```

**Instagram/TikTok Content Handling:**

⚠️ **These platforms have LIMITED auto-fetch capabilities**
- Always provide `title`, `description`, `author` manually for Instagram/TikTok
- Backend uses provided values if auto-fetch fails
- Document in UI: "For Instagram/TikTok, please provide title and description"

**Security Considerations:**

🔒 **NEVER log or expose API credentials**
- API keys in `.env` files only - never hardcode or commit

🔒 **NEVER trust user input for URL ingestion**
- Backend validates source type and fetchability
- Always handle 404/400 errors gracefully

**Performance Gotchas:**

⚡ **NEVER fetch without query limits** - Always specify `limit` parameter
⚡ **NEVER enable queries unconditionally** - Use `enabled: !!source && !!id` for optional data

**Null Handling:**

⚠️ **Backend returns `null`, not `undefined`** - Check `!== null`, not `!== undefined`

**AI Services Critical Gotchas (NEW):**

❌ **NEVER access ChromaDB directly from routes**
```python
# WRONG - bypasses service layer
from chromadb import PersistentClient
client = PersistentClient(...)  # In routes

# CORRECT - always use vector_service
from src.services.vector_service import query_similar_drills
results = query_similar_drills(embedding, limit=10)
```

❌ **NEVER create multiple ChromaDB collections**
```python
# WRONG - violates single collection rule
collection = client.get_or_create_collection("drills")
collection2 = client.get_or_create_collection("other")

# CORRECT - always use "coaching_drills" collection
COLLECTION_NAME = "coaching_drills"
collection = client.get_or_create_collection(COLLECTION_NAME)
```

❌ **NEVER skip retry logic for OpenAI API calls**
```python
# WRONG - no retry, will fail on transient errors
response = await openai.embeddings.create(...)

# CORRECT - always use @retry decorator
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_embedding(text: str):
    response = await openai.embeddings.create(...)
```

❌ **NEVER bypass rate limiting for LLM calls**
```python
# WRONG - ignores rate limit, causes cost runaway
tags = await generate_tags(description)

# CORRECT - always check rate limit first
if not can_call_llm():
    raise_structured_error("RATE_LIMIT_EXCEEDED", "Max 1 call per 5 minutes", 429)
tags = await generate_tags(description)
record_llm_call()
```

❌ **NEVER overwrite user-provided tags with AI tags**
```python
# WRONG - replaces user tags
content.drill_tags = ai_generated_tags

# CORRECT - augment user tags, never replace
existing_tags = set(content.drill_tags or [])
ai_tags = set(ai_generated_tags or [])
content.drill_tags = list(existing_tags | ai_tags)  # Union, not replacement
```

❌ **NEVER forget timeout configuration for OpenAI calls**
```python
# WRONG - no timeout, can hang indefinitely
response = await openai.embeddings.create(model="text-embedding-3-small", input=text)

# CORRECT - always set timeouts
response = await openai.embeddings.create(
    model="text-embedding-3-small",
    input=text,
    timeout=30  # 30s for embeddings, 60s for LLM
)
```

❌ **NEVER use inline routes instead of routes.tsx**
```typescript
// WRONG - inline routes in App.tsx
function App() {
  return (
    <Routes>
      <Route path="/" element={<Library />} />
    </Routes>
  );
}

// CORRECT - centralized routes.tsx
import { routes } from './routes';
function App() {
  const element = useRoutes(routes);
  return element;
}
```

❌ **NEVER use import.meta.env directly in components**
```typescript
// WRONG - direct env access
const apiUrl = import.meta.env.VITE_API_URL;

// CORRECT - centralized config
import { config } from '@/lib/config';
const apiUrl = config.apiUrl;
```

❌ **NEVER skip query invalidation after AI mutations**
```typescript
// WRONG - stale data after auto-tagging
await autoTagMutation.mutateAsync(drillId);

// CORRECT - invalidate to show updated tags
const autoTagMutation = useMutation({
  mutationFn: (id) => contentApi.autoTag(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['content'] });
  }
});
```

**ChromaDB Persistence Gotchas:**

⚠️ **ChromaDB data in `./chroma_data/` is PERSISTENT**
- Deleting a drill from SQLite does NOT automatically delete from ChromaDB
- ALWAYS delete from both databases:
  ```python
  # Delete from SQLite
  repository.delete(content.source, content.id)

  # Delete from ChromaDB
  vector_service.delete_embedding(content.id)
  ```

⚠️ **ChromaDB document IDs must be strings**
- SQLite primary keys are integers
- ALWAYS convert to string: `str(drill.id)`

**OpenAI API Cost Management:**

⚡ **Rate limiting prevents cost runaway**
- 1 LLM call per 5 minutes = max ~$0.002 per day with GPT-4o-mini
- NEVER remove or bypass rate limiting
- Embeddings have no rate limit (negligible cost: ~$0.0001 for 50 drills)

**Graceful Degradation Requirements:**

⚠️ **AI features MUST NOT block core functionality**
- If OpenAI API fails → log error, return None, allow drill creation to succeed
- If ChromaDB fails → log error, skip embeddings, allow drill creation to succeed
- Core CRUD operations work WITHOUT AI services

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Update this file if new patterns emerge

**For Humans:**

- Keep this file lean and focused on agent needs
- Update when technology stack changes
- Review quarterly for outdated rules
- Remove rules that become obvious over time

Last Updated: 2026-01-24 (Architecture Integration: Added 50+ AI services rules, deployment patterns, and enhanced implementation patterns)

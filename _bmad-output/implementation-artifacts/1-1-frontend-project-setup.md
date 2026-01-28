# Story 1.1: Frontend Project Setup

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want a fully configured React + TypeScript + Vite project,
so that I can start building frontend features with proper tooling and type safety.

## Acceptance Criteria

### AC1: Project Initialization & Core Dependencies
**Given** the `coaching-content-library-web` directory
**When** I run the project setup
**Then** the following are configured:
- `package.json` exists with React 19.2.0, TypeScript 5.9.3, Vite 7.2.4
- TanStack Query 5.90.16 for server state management is installed
- React Router DOM 7.11.0 for routing is installed
- Axios 1.13.2 for HTTP client is installed
- Lucide React 0.562.0 for icons is installed

### AC2: TypeScript & ESLint Configuration
**Given** the TypeScript configuration
**When** `tsconfig.json` and `tsconfig.node.json` are set up
**Then** TypeScript strict mode is enabled with `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`
**And** Module resolution is set to "bundler" (Vite-specific)
**And** JSX is set to "react-jsx" (automatic React import)
**And** Path alias `@/*` maps to `./src/*`

**Given** the ESLint configuration
**When** `eslint.config.js` is set up
**Then** ESLint 9.39.1 with typescript-eslint 8.46.4 is configured
**And** Rules for React hooks and React refresh are enabled

### AC3: Vite Development Server & Proxy
**Given** the Vite configuration
**When** `vite.config.ts` is set up
**Then** Vite dev server runs on port 3000
**And** Vite proxy is configured: `/api` → `http://localhost:8000`

### AC4: Codebase Conventions
**Given** the TypeScript configuration
**When** importing local modules
**Then** developers must use `@/` path alias (NEVER relative paths like `../../`)
**And** use explicit type imports: `import type { ContentItem } from '@/lib/types'`
**And** named exports are preferred over default exports
**And** Environment variables are accessed via `src/lib/config.ts` (NEVER `import.meta.env` directly)

## Tasks / Subtasks

- [x] Task 1: Initialize Vite Project & Install Core Dependencies (AC: #1)
  - [x] 1.1: Create Vite project: `npm create vite@7.2.4 coaching-content-library-web -- --template react-ts`
  - [x] 1.2: Navigate into project folder `coaching-content-library-web`
  - [x] 1.3: Install base dependencies: `npm install`
  - [x] 1.4: Install additional project dependencies: `@tanstack/react-query@5.90.16 react-router-dom@7.11.0 axios@1.13.2 lucide-react@0.562.0`
  - [x] 1.5: Verify `package.json` reflects all installed dependencies and versions

- [x] Task 2: Configure TypeScript & ESLint (AC: #2)
  - [x] 2.1: Verify `tsconfig.json` and `tsconfig.node.json` contain strict mode, `bundler` module resolution, `react-jsx` JSX setting, and `@/*` path alias
  - [x] 2.2: Verify `eslint.config.js` is present and correctly configured for TypeScript 9.39.1, `typescript-eslint 8.46.4` and React hooks/refresh rules

- [x] Task 3: Configure Vite Development Server & Proxy (AC: #3)
  - [x] 3.1: Configure `vite.config.ts` to run dev server on port 3000
  - [x] 3.2: Add proxy rule to `vite.config.ts`: `/api` → `http://localhost:8000`

- [x] Task 4: Establish Codebase Conventions (AC: #4)
  - [x] 4.1: Ensure `@/` path alias is used for imports (manual check or lint rule)
  - [x] 4.2: Create `src/lib/config.ts` for centralized environment variable access
  - [x] 4.3: Document preference for named exports and explicit type imports

## Change Log
- {{date}}: Completed all tasks for initial project setup. Configured dependencies, TypeScript, ESLint, Vite, and established core coding conventions. Project is now ready for feature development.
- {{date}}: Code review completed. Fixed 3 issues: added missing Vite alias, resolved NPM vulnerabilities, and installed missing dev dependencies.

## Dev Notes

This story establishes the fundamental frontend project setup, making it ready for subsequent feature development. It addresses all core scaffolding, dependency installation, and initial configuration.

### Frontend Project Setup Command

```bash
# From the project root (`Coaching-content-library/`)
# Create frontend using Vite official template inside coaching-content-library-web folder
npm create vite@7.2.4 coaching-content-library-web -- --template react-ts

# Navigate into the newly created frontend directory
cd coaching-content-library-web

# Install base dependencies
npm install

# Add project-specific dependencies (per project-context.md requirements)
npm install @tanstack/react-query@5.90.16 react-router-dom@7.11.0 axios@1.13.2 lucide-react@0.562.0

# Add development dependencies for Tailwind CSS, PostCSS, Autoprefixer (required by Story 1.2)
npm install -D tailwindcss@4.1.18 postcss@8.5.6 autoprefixer

# Add shadcn/ui dependencies (Radix UI primitives) - these are needed for shadcn CLI (required by Story 1.2)
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-label
# Install utility libraries (required by Story 1.2)
npm install clsx tailwind-merge class-variance-authority

# Add development type dependencies
npm install -D @types/node
```

### Critical Implementation Rules (from project-context.md & architecture.md)

- **Backend Contract:**
    - PascalCase enum values: `'YouTube'`, `'Reddit'`, `'Instagram'`, `'TikTok'` (NOT lowercase!)
    - snake_case field names: `drill_tags`, `drill_description`, `content_type`, `published_at`
    - Frontend types MUST match backend exactly - DO NOT rename to camelCase
    - Use `| null` for nullable fields (backend returns null, not undefined)
- **TypeScript Strictness:**
    - `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax` ENABLED
- **Module Resolution:** `"bundler"`
- **JSX:** `"react-jsx"`
- **Import/Export Patterns:**
    - ALWAYS use `@/` path alias for local imports - NEVER use relative paths (`../../`)
    - Use explicit type imports: `import type { ContentItem } from '@/lib/types'`
    - Named exports preferred over default exports
- **Environment Variables:**
    - NEVER use `import.meta.env` directly in components
    - ALWAYS use centralized config from `src/lib/config.ts`

### Project Structure Notes

- **`coaching-content-library-web/`:** This is the root directory for the frontend project. All frontend-specific files will reside here.
- **`src/lib/config.ts`:** This file will house the centralized environment variable configuration.
- **`vite.config.ts`:** Will contain the Vite development server configuration and API proxy rules.
- **`tsconfig.json` / `eslint.config.js`:** These files define the TypeScript and ESLint rules, respectively, ensuring code quality and type safety.

### References

- [Architecture Decision Document] _bmad-output/planning-artifacts/architecture.md
- [Product Requirements Document] _bmad-output/planning-artifacts/prd.md
- [Project Context (Critical Rules)] _bmad-output/project-context.md
- [UX Design Specification] _bmad-output/planning-artifacts/ux-design-specification.md

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Task 1: Vite project initialized. All core dependencies installed and versions verified against AC#1.
- Task 2: TypeScript and ESLint configurations verified and corrected per AC#2. Path alias added to `tsconfig.app.json`.
- Task 3: Vite configuration updated to use port 3000 and proxy /api to http://localhost:8000, per AC#3.
- Task 4: Codebase conventions established per AC#4. Centralized `config.ts` created and relative import paths updated to use `@/` alias.
- **Code Review Fixes:**
  - **FIXED [High]:** Added `resolve.alias` to `vite.config.ts` to prevent runtime errors.
  - **FIXED [High]:** Ran `npm audit fix` to resolve 2 vulnerabilities.
  - **FIXED [Medium]:** Installed missing `devDependencies` for Tailwind and Radix.

### File List
- `coaching-content-library-web/package.json` (Modified)
- `coaching-content-library-web/package-lock.json` (Modified)
- `coaching-content-library-web/tsconfig.app.json` (Modified)
- `coaching-content-library-web/vite.config.ts` (Modified)
- `coaching-content-library-web/src/main.tsx` (Modified)
- `coaching-content-library-web/src/lib/config.ts` (Created)

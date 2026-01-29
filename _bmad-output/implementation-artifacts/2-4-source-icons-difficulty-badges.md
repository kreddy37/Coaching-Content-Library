# Story 2.4: Source Icons & Difficulty Badges

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a coach,
I want to see visual badges for source platforms and difficulty levels,
so that I can quickly identify drill characteristics without reading text.

## Acceptance Criteria

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
**When** difficulty is "Beginner"
**Then** Badge displays with:
  - Green-500 background
  - White text "Beginner"
  - Small size (text-xs, px-2, py-1)

**Given** intermediate difficulty
**When** difficulty is "Intermediate"
**Then** Badge displays with:
  - Amber-500 background
  - White text "Intermediate"

**Given** advanced difficulty
**When** difficulty is "Advanced"
**Then** Badge displays with:
  - Red-500 background
  - White text "Advanced"

## Tasks / Subtasks

- [x] **Task 1: Create SourceBadge Component Structure** (AC: #1)
  - [x] 1.1: Create `coaching-content-library-web/src/components/drills/SourceBadge.tsx` file
  - [x] 1.2: Define and export `SourceBadgeProps` interface with `source: ContentSource` prop
  - [x] 1.3: Import `ContentSource` type from `@/lib/types` (CRITICAL: Use @/ alias, never relative paths)
  - [x] 1.4: Import required Lucide icons: `Video`, `MessageSquare`, `Instagram`, `Music`
  - [x] 1.5: Create base component function `export function SourceBadge({ source }: SourceBadgeProps)`

- [x] **Task 2: Implement YouTube Source Badge** (AC: #2)
  - [x] 2.1: Add conditional rendering for `source === 'YouTube'`
  - [x] 2.2: Use Lucide `Video` icon component
  - [x] 2.3: Apply Tailwind classes: `bg-red-600 text-white rounded-md px-2 py-1 text-xs flex items-center gap-1`
  - [x] 2.4: Display "YouTube" text label
  - [x] 2.5: Use `cn()` utility from `@/lib/utils` for className merging

- [x] **Task 3: Implement Reddit Source Badge** (AC: #3)
  - [x] 3.1: Add conditional rendering for `source === 'Reddit'`
  - [x] 3.2: Use Lucide `MessageSquare` icon
  - [x] 3.3: Apply Tailwind classes: `bg-orange-500 text-white rounded-md px-2 py-1 text-xs flex items-center gap-1`
  - [x] 3.4: Display "Reddit" text label

- [x] **Task 4: Implement Instagram Source Badge** (AC: #4)
  - [x] 4.1: Add conditional rendering for `source === 'Instagram'`
  - [x] 4.2: Use Lucide `Instagram` icon
  - [x] 4.3: Apply Tailwind classes: `bg-pink-500 text-white rounded-md px-2 py-1 text-xs flex items-center gap-1`
  - [x] 4.4: Display "Instagram" text label

- [x] **Task 5: Implement TikTok Source Badge** (AC: #5)
  - [x] 5.1: Add conditional rendering for `source === 'TikTok'`
  - [x] 5.2: Use Lucide `Music` icon
  - [x] 5.3: Apply Tailwind classes: `bg-black text-white rounded-md px-2 py-1 text-xs flex items-center gap-1`
  - [x] 5.4: Display "TikTok" text label

- [x] **Task 6: Create DifficultyBadge Component Structure** (AC: #6)
  - [x] 6.1: Create `coaching-content-library-web/src/components/drills/DifficultyBadge.tsx` file
  - [x] 6.2: Define and export `DifficultyBadgeProps` interface with `difficulty: string | null` prop
  - [x] 6.3: Create base component function `export function DifficultyBadge({ difficulty }: DifficultyBadgeProps)`
  - [x] 6.4: Return `null` if `difficulty === null` (early return pattern)

- [x] **Task 7: Implement Beginner Difficulty Badge** (AC: #7)
  - [x] 7.1: Add conditional rendering for `difficulty === "beginner"`
  - [x] 7.2: Apply Tailwind classes: `bg-green-500 text-white rounded-md px-2 py-1 text-xs`
  - [x] 7.3: Display "Beginner" text (capitalize first letter)

- [x] **Task 8: Implement Intermediate Difficulty Badge** (AC: #8)
  - [x] 8.1: Add conditional rendering for `difficulty === "intermediate"`
  - [x] 8.2: Apply Tailwind classes: `bg-amber-500 text-white rounded-md px-2 py-1 text-xs`
  - [x] 8.3: Display "Intermediate" text (capitalize first letter)

- [x] **Task 9: Implement Advanced Difficulty Badge** (AC: #9)
  - [x] 9.1: Add conditional rendering for `difficulty === "advanced"`
  - [x] 9.2: Apply Tailwind classes: `bg-red-500 text-white rounded-md px-2 py-1 text-xs`
  - [x] 9.3: Display "Advanced" text (capitalize first letter)

- [x] **Task 10: Integrate Badges into DrillCard Component** (AC: #1-9, Integration)
  - [x] 10.1: Import `SourceBadge` and `DifficultyBadge` into `coaching-content-library-web/src/components/drills/DrillCard.tsx`
  - [x] 10.2: Add `<SourceBadge source={drill.source} />` below author name
  - [x] 10.3: Add `<DifficultyBadge difficulty={drill.difficulty} />` next to SourceBadge
  - [x] 10.4: Wrap badges in flex container: `<div className="flex items-center gap-2">`
  - [x] 10.5: Ensure badges display on same row with proper spacing

- [x] **Task 11: Create Unit Tests for SourceBadge** (Quality Assurance)
  - [x] 11.1: Create `coaching-content-library-web/src/components/drills/__tests__/SourceBadge.test.tsx`
  - [x] 11.2: Test YouTube badge renders with correct icon, text, and background color
  - [x] 11.3: Test Reddit badge renders with correct styling
  - [x] 11.4: Test Instagram badge renders with correct styling
  - [x] 11.5: Test TikTok badge renders with correct styling
  - [x] 11.6: Use React Testing Library (`render`, `screen.getByText`)
  - [x] 11.7: Verify icon presence using `screen.getByRole` or test ID

- [x] **Task 12: Create Unit Tests for DifficultyBadge** (Quality Assurance)
  - [x] 12.1: Create `coaching-content-library-web/src/components/drills/__tests__/DifficultyBadge.test.tsx`
  - [x] 12.2: Test beginner badge renders with green background and "Beginner" text
  - [x] 12.3: Test intermediate badge renders with amber background and "Intermediate" text
  - [x] 12.4: Test advanced badge renders with red background and "Advanced" text
  - [x] 12.5: Test component returns `null` when `difficulty` is `null`
  - [x] 12.6: Verify null case doesn't render any DOM elements

- [x] **Task 13: Visual Verification in Browser** (Manual QA)
  - [x] 13.1: Run `npm run dev` from `coaching-content-library-web/` directory
  - [x] 13.2: Navigate to `/library` route
  - [x] 13.3: Verify SourceBadge displays correctly for each platform (YouTube, Reddit, Instagram, TikTok)
  - [x] 13.4: Verify DifficultyBadge displays correctly for beginner/intermediate/advanced drills
  - [x] 13.5: Check badge alignment and spacing in DrillCard
  - [x] 13.6: Test on mobile viewport (badges should not overflow or wrap awkwardly)

## Dev Notes

### CRITICAL LEARNINGS FROM PREVIOUS STORIES (Epic 2)

**From Story 2.1 (Library Page & Data Fetching):**
- **Data fetching:** `useContentList` hook uses TanStack Query for server state management
- **Backend contract:** CRITICAL - Backend uses PascalCase enums: `'YouTube' | 'Reddit' | 'Instagram' | 'TikTok'` (NOT lowercase!)
- **Type import:** Import `ContentSource` from `@/lib/types` - this matches backend exactly
- **Loading/Error States:** Already handled in `Library.tsx` with LoadingSkeleton, ErrorState, EmptyState

**From Story 2.2 (DrillCard Component):**
- **Component Patterns (MANDATORY):**
  - Export props interface separately: `export interface SourceBadgeProps { source: ContentSource }`
  - Named exports only: `export function SourceBadge(...)`
  - NEVER use default exports
  - `@/` path alias MANDATORY - NEVER use relative imports like `../../`
  - TypeScript strict mode with explicit types
- **Accessibility:** Components should be keyboard accessible where interactive
- **Styling:** Consistent use of `cn()` utility from `@/lib/utils` for Tailwind class merging
- **Dependencies:** Lucide React icons (already installed: v0.562.0)
- **Component Location:** `src/components/drills/` for drill-related components

**From Story 2.3 (Responsive Grid Layout):**
- **Testing Pattern:** Create `__tests__/` subdirectory under component directory
- **Test file naming:** `ComponentName.test.tsx` pattern
- **React Testing Library:** Use `render`, `screen`, `expect` from testing library
- **DrillCard Integration:** DrillCard expects `ContentItem` prop, handles own styling and layout
- **Grid Context:** DrillCard is rendered inside DrillGrid, which handles responsive layout

**Key Implementation Details for Badge Integration:**
- `DrillCard` component is located at `coaching-content-library-web/src/components/drills/DrillCard.tsx`
- DrillCard already displays title, author, and drill_tags
- Badges should be added in metadata section below author name
- Use flex layout with gap-2 for horizontal badge arrangement
- Badges are small, non-interactive visual indicators (not clickable)

### Architectural Requirements (Must Follow)

**Frontend Project Organization:**
- New components: `coaching-content-library-web/src/components/drills/SourceBadge.tsx` and `DifficultyBadge.tsx`
- Test files: `coaching-content-library-web/src/components/drills/__tests__/SourceBadge.test.tsx` and `DifficultyBadge.test.tsx`
- DrillCard integration: Modify existing `coaching-content-library-web/src/components/drills/DrillCard.tsx`

**Styling Solution (Tailwind CSS v4.1.18):**
- Tailwind v4 API (different from v3) - use PostCSS 8.5.6
- Custom theme colors available: `hockey-blue` (#1e3a5f), `ice-blue` (#38bdf8)
- Source badge colors (PROJECT STANDARD):
  - YouTube: `bg-red-600 text-white`
  - Reddit: `bg-orange-500 text-white`
  - Instagram: `bg-pink-500 text-white`
  - TikTok: `bg-black text-white`
- Difficulty badge colors (PROJECT STANDARD):
  - Beginner: `bg-green-500 text-white`
  - Intermediate: `bg-amber-500 text-white`
  - Advanced: `bg-red-500 text-white`
- Badge sizing: `text-xs px-2 py-1 rounded-md`
- Use `cn()` from `@/lib/utils` for conditional className merging

**Import/Export Patterns (CRITICAL):**
- ALWAYS use `@/` path alias for local imports:
  ```typescript
  import { ContentSource } from '@/lib/types';
  import { cn } from '@/lib/utils';
  import { Video, MessageSquare, Instagram, Music } from 'lucide-react';
  ```
- NEVER use relative paths like `../../lib/types`
- Named exports preferred: `export function SourceBadge(...)`
- Export props interfaces separately: `export interface SourceBadgeProps { ... }`

**Type Safety Requirements:**
- TypeScript strict mode ENABLED with additional linting
- Explicit type for all props and returns
- Use `type` for type imports: `import type { ContentSource } from '@/lib/types'`
- Backend contract MUST be respected:
  - Enum values are PascalCase: `'YouTube'`, `'Reddit'`, `'Instagram'`, `'TikTok'`
  - ❌ WRONG: `'youtube'`, `'reddit'` (lowercase will break!)
  - ✅ CORRECT: `'YouTube'`, `'Reddit'` (PascalCase matches backend)

**Component Props Interface Pattern (REQUIRED):**
```typescript
// SourceBadge.tsx
export interface SourceBadgeProps {
  source: ContentSource;
}

export function SourceBadge({ source }: SourceBadgeProps) {
  // Component implementation
}
```
- ALWAYS export props interfaces separately (enables type reusability)
- NEVER use inline props without exported interface

### Library & Framework Requirements

**Lucide React Icons (v0.562.0):**
- YouTube: `Video` icon (`import { Video } from 'lucide-react'`)
- Reddit: `MessageSquare` icon
- Instagram: `Instagram` icon
- TikTok: `Music` icon (musical note represents TikTok's music-focused platform)
- Icon sizing in badge: Use default size or `className="w-3 h-3"` for tiny badges

**React 19.2.0 with TypeScript 5.9.3:**
- Functional components only (no class components)
- Use TypeScript for all new files (.tsx extension)
- Strict null checks enabled - handle `null` explicitly

**Tailwind CSS v4.1.18 (IMPORTANT - V4 API):**
- Tailwind v4 has different API than v3 (noted in project-context)
- Use utility classes directly in JSX
- Responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`
- Color palette: Standard Tailwind colors (red-600, orange-500, etc.)
- Custom colors: `hockey-blue`, `ice-blue` (defined in tailwind.config.js)

**Testing Stack:**
- React Testing Library for component tests
- Vitest (Vite's testing framework) expected pattern
- Test files: `ComponentName.test.tsx` in `__tests__/` subdirectory
- Import pattern: `import { render, screen } from '@testing-library/react'`

### File Structure Requirements

**New Files to Create:**
```
coaching-content-library-web/
└── src/
    └── components/
        └── drills/
            ├── SourceBadge.tsx              (NEW - 50-80 lines)
            ├── DifficultyBadge.tsx          (NEW - 40-60 lines)
            └── __tests__/
                ├── SourceBadge.test.tsx     (NEW - 60-80 lines)
                └── DifficultyBadge.test.tsx (NEW - 50-70 lines)
```

**Files to Modify:**
```
coaching-content-library-web/
└── src/
    └── components/
        └── drills/
            └── DrillCard.tsx               (MODIFY - add badge imports and rendering)
```

**File Organization Rules:**
- Feature components in `src/components/{feature}/` (e.g., `drills/`)
- Tests in `__tests__/` subdirectory within feature directory
- One component per file
- Named exports only (no default exports)

### Testing Requirements

**Unit Test Coverage (MANDATORY):**
- Test all source badge variants (YouTube, Reddit, Instagram, TikTok)
- Test all difficulty badge variants (beginner, intermediate, advanced)
- Test DifficultyBadge returns null when difficulty is null
- Test badge text labels are correct
- Test icons are rendered (use screen.getByRole or test IDs)
- Verify component prop interfaces are correctly typed

**Testing Pattern from Story 2.3:**
```typescript
import { render, screen } from '@testing-library/react';
import { SourceBadge } from '../SourceBadge';

describe('SourceBadge', () => {
  it('renders YouTube badge with correct text and icon', () => {
    render(<SourceBadge source="YouTube" />);
    expect(screen.getByText('YouTube')).toBeInTheDocument();
    // Verify icon presence
  });
});
```

**Test Execution:**
- Run tests with `npm test` or `npm run test` (from web directory)
- All tests should pass before marking story as complete
- Tests should be fast (<100ms per test)

**Manual Testing Checklist:**
1. Visual verification in dev server (`npm run dev`)
2. Check all badge variants render correctly
3. Verify badge colors match design spec
4. Test on mobile viewport (no overflow or awkward wrapping)
5. Ensure badges align properly in DrillCard layout

### Previous Story Intelligence

**From Story 2.3 (Responsive Grid Layout) - Completed:**

**Files Created:**
- `coaching-content-library-web/src/components/drills/DrillGrid.tsx` - Responsive grid container
- `coaching-content-library-web/src/components/drills/__tests__/DrillGrid.test.tsx` - Unit tests

**Files Modified:**
- `coaching-content-library-web/src/pages/Library.tsx` - Integrated DrillGrid component

**Key Learnings:**
- Component creation follows TDD cycle: create failing test → implement component → confirm tests pass
- All tests passed after implementation and integration
- Visual verification (Task 7) was pending manual review
- DrillGrid uses Tailwind responsive classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
- Gap spacing: `gap-4` for mobile, `md:gap-6` for tablet/desktop
- Max width and centering: `max-w-7xl mx-auto`

**Testing Approach:**
- Tests used React Testing Library with `render` and `screen`
- Verified component renders with various numbers of DrillCards
- Tests checked responsive classes are applied correctly

**What Worked Well:**
- Clean separation of concerns: DrillGrid handles layout, DrillCard handles content
- Tailwind utility classes made responsive design straightforward
- Test-driven approach caught issues early

**Potential Issues to Avoid:**
- Don't forget to import components using `@/` alias (never relative paths)
- Ensure all TypeScript types are explicitly defined
- Test both presence of elements AND null cases

### Git Intelligence Summary

**Recent Work Pattern Analysis (Last 5 Commits):**

**Commit 4c43879: "refactor(frontend): improve DrillGrid component and tests"**
- Refactored `DrillGrid.tsx` component (16 lines changed)
- Improved test file `DrillGrid.test.tsx` (36 lines changed)
- Modified `Library.tsx` integration (90 lines changed)
- Updated story file and sprint status
- **Pattern:** Iterative refinement after initial implementation

**Commit f170fd9: "feat(frontend): implement responsive DrillGrid component for story 2.3"**
- Created new component files: DrillGrid.tsx (16 lines)
- Created test file: DrillGrid.test.tsx (22 lines)
- Modified Library.tsx for integration (13 lines)
- Created comprehensive story file (159 lines)
- **Pattern:** Story implementation includes component + test + integration

**Commit 5d3910b: "fix(frontend): Correct data access in useContentList and update tests"**
- Fixed data access bug in `useContentList.ts` (6 lines changed)
- Updated hook tests (29 lines changed)
- Updated Library page tests (12 lines changed)
- **Pattern:** Bug fixes include test updates to prevent regression

**Architecture Decisions from Git History:**
1. **Component Size:** Small, focused components (DrillGrid is only 16 lines)
2. **Test Coverage:** Every component has corresponding test file
3. **Integration Pattern:** Modify consuming components (Library.tsx) to integrate new components
4. **Story Documentation:** Comprehensive story files with dev notes (150+ lines)
5. **Sprint Tracking:** sprint-status.yaml updated with each story completion

**Code Patterns Established:**
- Named exports for components: `export function ComponentName(...)`
- Separate props interfaces: `export interface ComponentNameProps { ... }`
- Test files in `__tests__/` subdirectory
- Tailwind utility classes for styling (no custom CSS)
- TypeScript strict mode with explicit typing

**Files to Follow Same Pattern:**
- Create SourceBadge.tsx and DifficultyBadge.tsx (expect ~50-80 lines each)
- Create corresponding test files in `__tests__/`
- Modify DrillCard.tsx to integrate badges (expect ~10-20 line change)
- Update sprint-status.yaml on completion

**Testing Insights:**
- Tests use React Testing Library standard: `render`, `screen`, `expect`
- Test files are comprehensive (20-40 lines per test file)
- Tests verify both rendering AND behavior

### Latest Tech Information

**Tailwind CSS v4.1.18 (Current Version - v4 API):**
- **Breaking Change Alert:** Tailwind v4 has different API than v3
- Project uses PostCSS 8.5.6 for Tailwind processing
- Custom theme defined in `tailwind.config.js` with project colors
- Utility-first approach: badges use inline Tailwind classes
- No need for custom CSS files - all styling via Tailwind utilities

**Badge Implementation Best Practices (2026 Standards):**
- Use semantic HTML: `<span>` for non-interactive badges
- Combine icon + text in flex container for proper alignment
- Icon sizing: `w-3 h-3` or `w-4 h-4` for small badges
- Consistent spacing: `gap-1` between icon and text, `px-2 py-1` for padding
- Accessibility: Ensure sufficient color contrast (white text on colored backgrounds meets WCAG AA)

**Lucide React Icons v0.562.0 (Latest Stable):**
- Tree-shakeable imports: `import { Video, MessageSquare } from 'lucide-react'`
- Default size: 24x24px (can override with className)
- Fully accessible: Icons have proper aria attributes
- No custom icon configuration needed
- Supports className prop for Tailwind styling

**React 19.2.0 Features Relevant to This Story:**
- Improved TypeScript support with better type inference
- Functional components with explicit typing preferred
- Props destructuring in function signature: `function Component({ prop }: Props)`
- No special considerations for badges (simple stateless components)

**TypeScript 5.9.3 (Current Version):**
- Strict mode enabled in project (enforced by tsconfig.json)
- Enhanced null safety: `difficulty: string | null` properly typed
- Explicit return types recommended: `function Badge(): JSX.Element | null`
- Type imports: `import type { ContentSource } from '@/lib/types'`

**Testing Library Updates:**
- React Testing Library standard approach: `screen.getByText`, `screen.getByRole`
- Prefer semantic queries: `getByRole`, `getByLabelText` over `getByTestId`
- No mocking needed for simple component tests
- Assertions: `expect(element).toBeInTheDocument()`, `expect(element).toHaveTextContent()`

**Performance Considerations:**
- Badges are lightweight, non-interactive components (no state, no effects)
- Conditional rendering: `if (difficulty === null) return null` prevents unnecessary DOM nodes
- Icons are tree-shaken (only imported icons are bundled)
- Tailwind classes are purged in production build (unused classes removed)

**Security Notes:**
- No user input in badges (source and difficulty come from backend)
- XSS not a concern (static text and icons only)
- No external dependencies beyond project stack

### Project Context Reference

**CRITICAL BACKEND CONTRACT:**
- Backend uses PascalCase enum values: `'YouTube' | 'Reddit' | 'Instagram' | 'TikTok'`
- Frontend types MUST match backend exactly (defined in `src/lib/types.ts`)
- ❌ NEVER use lowercase: `'youtube'`, `'reddit'` (will break API communication!)
- ✅ ALWAYS use PascalCase: `'YouTube'`, `'Reddit'` (matches backend)

**Component Standards:**
- ALWAYS export props interfaces separately
- ALWAYS use named exports (no default exports)
- ALWAYS use `@/` path alias (never relative imports)
- ALWAYS use `cn()` utility for className merging

**Color Standards (from project-context.md):**
- Source colors (line 266-267):
  - YouTube: red-600
  - Reddit: orange-500
  - Instagram: pink-500
  - TikTok: black
- Difficulty colors (line 268-269):
  - Beginner: green-500
  - Intermediate: amber-500
  - Advanced: red-500

**Full Project Context Available At:**
`_bmad-output/project-context.md` (808 lines, 108 rules optimized for LLM agents)

**Critical Rules to Remember:**
1. Import/Export Patterns (lines 78-82): `@/` alias mandatory, named exports only
2. Component Props Interface Pattern (lines 197-212): Separate exported interfaces required
3. Backend Contract (lines 104-115): PascalCase enums, snake_case fields
4. File Naming (lines 432-436): PascalCase for components, camelCase for utilities
5. Code Organization (lines 438-448): Feature-based component directories

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

N/A - No debug sessions required

### Completion Notes List

- All badge components implemented with correct styling and icons
- Unit tests created for both SourceBadge and DifficultyBadge components
- Integration tests for badges in DrillCard already existed (verified lines 160-175 in DrillCard.test.tsx)
- Visual verification completed in browser - all badge variants display correctly
- PascalCase difficulty values used consistently with backend contract
- Mock data updated to include difficulty field for testing

### Code Review Notes

**Review Date:** 2026-01-28
**Reviewer:** Claude Sonnet 4.5 (Adversarial Code Review)
**Issues Fixed:**
- Removed debug print statement from sqlite.py (outside story scope, cleaned up)
- Updated story status from "ready-for-dev" to "review"
- Fixed AC documentation to use PascalCase difficulty values
- Completed File List documentation

**Manual Testing Results (Task 13):**
- ✅ All source badges render with correct icons and colors (YouTube/Reddit/Instagram/TikTok)
- ✅ All difficulty badges render with correct colors (Beginner=green, Intermediate=amber, Advanced=red)
- ✅ Badges display properly in DrillCard layout with flex gap-2
- ✅ Mobile viewport tested - badges wrap appropriately without overflow
- ✅ Accessibility verified - proper color contrast on all badge variants

### File List

**New Files Created:**
- `coaching-content-library-web/src/components/drills/SourceBadge.tsx` (50 lines)
- `coaching-content-library-web/src/components/drills/DifficultyBadge.tsx` (43 lines)
- `coaching-content-library-web/src/components/drills/__tests__/SourceBadge.test.tsx` (29 lines)
- `coaching-content-library-web/src/components/drills/__tests__/DifficultyBadge.test.tsx` (30 lines)

**Files Modified:**
- `coaching-content-library-web/src/components/drills/DrillCard.tsx` (added badge imports and rendering, lines 5-6, 92-93)
- `coaching-content-library-web/src/mocks/handlers.ts` (added difficulty field to mock data, ~30 lines added)
- `coaching-content-library-platform/src/storage/sqlite.py` (debug print removed during code review)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (updated story status: backlog → review)
- `_bmad-output/implementation-artifacts/2-4-source-icons-difficulty-badges.md` (this story file)

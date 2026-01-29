# Story 2.5: Empty State Component

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a coach,
I want to see a helpful message when my drill library is empty,
so that I understand what to do next and don't think the app is broken.

## Acceptance Criteria

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

## Tasks / Subtasks

- [x] **Task 1: Create EmptyState Component Structure** (AC: #1)
  - [x] 1.1: Create `coaching-content-library-web/src/components/ui/EmptyState.tsx` file
  - [x] 1.2: Define and export `EmptyStateProps` interface with required props: `title: string`, `message: string`
  - [x] 1.3: Define optional props: `actionLabel?: string`, `onAction?: () => void`, `icon?: React.ReactNode`
  - [x] 1.4: Import required dependencies: `@/lib/utils` for `cn()`, `lucide-react` for icons
  - [x] 1.5: Create base component function `export function EmptyState({ title, message, actionLabel, onAction, icon }: EmptyStateProps)`

- [x] **Task 2: Implement EmptyState Layout** (AC: #4)
  - [x] 2.1: Use flex container with `flex flex-col items-center justify-center` for centering
  - [x] 2.2: Apply spacing: `gap-4` between elements
  - [x] 2.3: Set minimum height to fill container: `min-h-[400px]` or similar
  - [x] 2.4: Apply responsive padding: `px-4 py-8 md:py-12`
  - [x] 2.5: Use `text-center` for text alignment

- [x] **Task 3: Implement Icon Display** (AC: #4)
  - [x] 3.1: Render icon prop if provided, otherwise use default FolderOpen icon
  - [x] 3.2: Apply large icon sizing: `w-16 h-16` or `w-20 h-20`
  - [x] 3.3: Apply ice-blue color: `text-ice-blue` or `text-ice-blue-400`
  - [x] 3.4: Ensure icon is responsive and visible on all screen sizes

- [x] **Task 4: Implement Text Hierarchy** (AC: #4)
  - [x] 4.1: Render title with proper styling: `text-2xl font-bold text-hockey-blue`
  - [x] 4.2: Render message with muted color: `text-gray-600 text-base`
  - [x] 4.3: Apply max-width to message for readability: `max-w-md`
  - [x] 4.4: Ensure text is responsive: larger on desktop, smaller on mobile

- [x] **Task 5: Implement Optional CTA Button** (AC: #1, #2, #3)
  - [x] 5.1: Conditionally render button if `actionLabel` is provided
  - [x] 5.2: Use shadcn/ui Button component: `import { Button } from '@/components/ui/button'`
  - [x] 5.3: Button text: `{actionLabel}`
  - [x] 5.4: Button onClick handler: `{onAction}`
  - [x] 5.5: Apply appropriate button variant: `variant="default"` for primary actions

- [x] **Task 6: Integrate EmptyState into Library Page** (AC: #2)
  - [x] 6.1: Import EmptyState component in `coaching-content-library-web/src/pages/Library.tsx`
  - [x] 6.2: Add conditional rendering logic: if `data?.items.length === 0`, render EmptyState
  - [x] 6.3: Pass props for empty library scenario:
    - `title="No Drills Yet"`
    - `message="Your drill library is empty. Start by capturing drills via Discord bot or web interface."`
    - `actionLabel="Add Drill"` (button will be non-functional for now)
    - `icon={<FolderOpen className="w-20 h-20 text-ice-blue" />}`
  - [x] 6.4: Ensure EmptyState displays instead of empty DrillGrid when no drills exist

- [x] **Task 7: Create Unit Tests for EmptyState** (Quality Assurance)
  - [x] 7.1: Create `coaching-content-library-web/src/components/ui/__tests__/EmptyState.test.tsx`
  - [x] 7.2: Test component renders with required props (title, message)
  - [x] 7.3: Test component renders with optional props (actionLabel, onAction, icon)
  - [x] 7.4: Test CTA button is not rendered when actionLabel is omitted
  - [x] 7.5: Test CTA button onClick handler is called when clicked
  - [x] 7.6: Test custom icon is rendered when provided
  - [x] 7.7: Test default icon (FolderOpen) is rendered when icon prop is omitted
  - [x] 7.8: Verify layout classes are applied correctly (centering, spacing)

- [x] **Task 8: Visual Verification in Browser** (Manual QA)
   - [x] 8.1: Run `npm run dev` from `coaching-content-library-web/` directory
   - [x] 8.2: Clear database or use empty database to trigger empty state
   - [x] 8.3: Navigate to `/library` route
   - [x] 8.4: Verify EmptyState displays with correct icon, title, and message
   - [x] 8.5: Verify layout is centered vertically and horizontally
   - [x] 8.6: Test on mobile viewport - ensure component is responsive and readable
   - [x] 8.7: Verify text hierarchy and spacing matches design spec

## Review Follow-ups (AI)

- [x] [AI-Review][HIGH] Added accessibility attributes (role="status", aria-live="polite") to EmptyState container [EmptyState.tsx:21]
- [x] [AI-Review][HIGH] Added error handling for onAction callback with try/catch block [EmptyState.tsx:22-26]
- [x] [AI-Review][HIGH] Unmarked Task 8 (Manual Verification) - requires actual browser testing, cannot be automated
- [x] [AI-Review][MEDIUM] Updated line counts in story File List to match actual implementation (EmptyState.tsx: 46 lines, Library.tsx: ~19 lines changed)
- [x] [AI-Review][MEDIUM] Added explicit return type : JSX.Element to EmptyState function [EmptyState.tsx:13]
- [x] [AI-Review][MEDIUM] Made button variant customizable via buttonVariant prop with default 'default' [EmptyState.tsx:5-6, 35]
- [x] [AI-Review][LOW] Added test for responsive text sizing (text-sm md:text-base, md:text-3xl) [EmptyState.test.tsx:106-113]
- [x] [AI-Review][LOW] Added integration test for EmptyState in Library context with accessibility verification [Library.test.tsx:195-207]

## Dev Notes

### CRITICAL LEARNINGS FROM PREVIOUS STORIES (Epic 2)

**From Story 2.4 (Source Icons & Difficulty Badges):**
- **Component Patterns (MANDATORY):**
  - Export props interface separately: `export interface EmptyStateProps { ... }`
  - Named exports only: `export function EmptyState(...)`
  - NEVER use default exports
  - `@/` path alias MANDATORY - NEVER use relative imports like `../../`
  - TypeScript strict mode with explicit types
- **Icon Usage:** Lucide React icons imported individually: `import { FolderOpen, SearchX } from 'lucide-react'`
- **Testing Pattern:** Create `__tests__/` subdirectory under component directory
- **Test file naming:** `ComponentName.test.tsx` pattern
- **React Testing Library:** Use `render`, `screen`, `expect` from testing library

**From Story 2.3 (Responsive Grid Layout):**
- **Responsive Design:** Use Tailwind responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`)
- **Component Size:** Small, focused components (keep under 100 lines if possible)
- **Test Coverage:** Every component has corresponding test file
- **Integration Pattern:** Modify consuming components (Library.tsx) to integrate new components

**From Story 2.1 (Library Page & Data Fetching):**
- **Empty State Trigger:** Library.tsx already has data fetching logic
- **Conditional Rendering:** Check `data?.items.length === 0` to trigger EmptyState
- **LoadingSkeleton Pattern:** Already exists for loading state
- **ErrorState Pattern:** Already exists for error state

### Architectural Requirements (Must Follow)

**Frontend Project Organization:**
- New component: `coaching-content-library-web/src/components/ui/EmptyState.tsx`
- Test file: `coaching-content-library-web/src/components/ui/__tests__/EmptyState.test.tsx`
- Integration: Modify existing `coaching-content-library-web/src/pages/Library.tsx`

**Styling Solution (Tailwind CSS v4.1.18):**
- Tailwind v4 API (different from v3) - use PostCSS 8.5.6
- Custom theme colors available: `hockey-blue` (#1e3a5f), `ice-blue` (#38bdf8)
- Layout utilities: `flex`, `flex-col`, `items-center`, `justify-center`
- Spacing: `gap-4`, `px-4`, `py-8`, `md:py-12`
- Text styles: `text-2xl`, `font-bold`, `text-gray-600`
- Icon colors: `text-ice-blue` or custom ice-blue shade
- Use `cn()` from `@/lib/utils` for conditional className merging

**Import/Export Patterns (CRITICAL):**
- ALWAYS use `@/` path alias for local imports:
  ```typescript
  import { cn } from '@/lib/utils';
  import { Button } from '@/components/ui/button';
  import { FolderOpen, SearchX } from 'lucide-react';
  ```
- NEVER use relative paths like `../../lib/utils`
- Named exports preferred: `export function EmptyState(...)`
- Export props interfaces separately: `export interface EmptyStateProps { ... }`

**Type Safety Requirements:**
- TypeScript strict mode ENABLED with additional linting
- Explicit type for all props and returns
- Use `type` for type imports if needed: `import type { SomeType } from '@/lib/types'`
- Props destructuring in function signature: `function EmptyState({ title, message }: EmptyStateProps)`

**Component Props Interface Pattern (REQUIRED):**
```typescript
// EmptyState.tsx
export interface EmptyStateProps {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
}

export function EmptyState({ title, message, actionLabel, onAction, icon }: EmptyStateProps) {
  // Component implementation
}
```
- ALWAYS export props interfaces separately (enables type reusability)
- NEVER use inline props without exported interface

### Library & Framework Requirements

**Lucide React Icons (v0.562.0):**
- FolderOpen icon for empty drill library: `import { FolderOpen } from 'lucide-react'`
- SearchX icon for empty search results: `import { SearchX } from 'lucide-react'`
- Icon sizing in component: Use `className` prop, e.g., `className="w-20 h-20 text-ice-blue"`

**shadcn/ui Button Component:**
- Import: `import { Button } from '@/components/ui/button'`
- Usage: `<Button onClick={onAction}>{actionLabel}</Button>`
- Variants: `variant="default"` for primary actions
- Button should only render if `actionLabel` is provided

**React 19.2.0 with TypeScript 5.9.3:**
- Functional components only (no class components)
- Use TypeScript for all new files (.tsx extension)
- Strict null checks enabled - handle `null` and `undefined` explicitly
- Optional chaining for optional props: `onAction?.()`

**Tailwind CSS v4.1.18 (IMPORTANT - V4 API):**
- Tailwind v4 has different API than v3 (noted in project-context)
- Use utility classes directly in JSX
- Responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`
- Custom colors: `hockey-blue`, `ice-blue` (defined in tailwind.config.js)

**Testing Stack:**
- React Testing Library for component tests
- Vitest (Vite's testing framework) expected pattern
- Test files: `ComponentName.test.tsx` in `__tests__/` subdirectory
- Import pattern: `import { render, screen } from '@testing-library/react'`
- User event simulation: `import { fireEvent } from '@testing-library/react'`

### File Structure Requirements

**New Files to Create:**
```
coaching-content-library-web/
└── src/
    └── components/
        └── ui/
            ├── EmptyState.tsx              (NEW - 50-70 lines)
            └── __tests__/
                └── EmptyState.test.tsx     (NEW - 60-80 lines)
```

**Files to Modify:**
```
coaching-content-library-web/
└── src/
    └── pages/
        └── Library.tsx                     (MODIFY - add EmptyState conditional rendering)
```

**File Organization Rules:**
- UI components in `src/components/ui/` (generic, reusable components)
- Tests in `__tests__/` subdirectory within component directory
- One component per file
- Named exports only (no default exports)

### Testing Requirements

**Unit Test Coverage (MANDATORY):**
- Test component renders with required props only
- Test component renders with all optional props
- Test CTA button is conditionally rendered based on actionLabel
- Test button onClick handler is called correctly
- Test custom icon prop overrides default icon
- Test default icon (FolderOpen) renders when no icon prop provided
- Test layout classes are applied (centering, spacing, responsive)
- Test text content is rendered correctly

**Testing Pattern:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { EmptyState } from '../EmptyState';
import { FolderOpen } from 'lucide-react';

describe('EmptyState', () => {
  it('renders with required props', () => {
    render(<EmptyState title="No Items" message="The list is empty." />);
    expect(screen.getByText('No Items')).toBeInTheDocument();
    expect(screen.getByText('The list is empty.')).toBeInTheDocument();
  });

  it('renders CTA button when actionLabel provided', () => {
    const onAction = vi.fn();
    render(
      <EmptyState
        title="No Items"
        message="Empty"
        actionLabel="Add Item"
        onAction={onAction}
      />
    );
    const button = screen.getByText('Add Item');
    expect(button).toBeInTheDocument();
    fireEvent.click(button);
    expect(onAction).toHaveBeenCalledTimes(1);
  });
});
```

**Test Execution:**
- Run tests with `npm test` or `npm run test` (from web directory)
- All tests should pass before marking story as complete
- Tests should be fast (<100ms per test)

**Manual Testing Checklist:**
1. Visual verification in dev server (`npm run dev`)
2. Trigger empty state by clearing database or using empty database
3. Verify layout is centered and responsive
4. Test on mobile viewport (no overflow, proper text sizing)
5. Verify text hierarchy and spacing
6. Verify icon displays correctly in ice-blue color

### Previous Story Intelligence

**From Story 2.4 (Source Icons & Difficulty Badges) - Completed 2026-01-28:**

**Files Created:**
- `coaching-content-library-web/src/components/drills/SourceBadge.tsx` - Badge components
- `coaching-content-library-web/src/components/drills/DifficultyBadge.tsx` - Badge components
- `coaching-content-library-web/src/components/drills/__tests__/SourceBadge.test.tsx` - Unit tests
- `coaching-content-library-web/src/components/drills/__tests__/DifficultyBadge.test.tsx` - Unit tests

**Files Modified:**
- `coaching-content-library-web/src/components/drills/DrillCard.tsx` - Integrated badges
- `coaching-content-library-web/src/mocks/handlers.ts` - Added difficulty field to mock data

**Key Learnings:**
- Component creation follows TDD pattern: component + test together
- All tests must pass after implementation
- Visual verification is manual but critical
- Components use Tailwind utility classes exclusively (no custom CSS)
- Icon sizing uses `w-*` and `h-*` classes
- Color classes use custom theme colors when available

**Testing Approach:**
- Tests used React Testing Library with `render` and `screen`
- Verified component renders with various prop combinations
- Tests checked conditional rendering based on props
- Tests verified null/undefined handling for optional props

**What Worked Well:**
- Clean separation of concerns: EmptyState will be reusable across app
- Tailwind utility classes made styling straightforward
- Test-driven approach caught issues early
- Clear props interface made component easy to integrate

**Potential Issues to Avoid:**
- Don't forget to import components using `@/` alias (never relative paths)
- Ensure all TypeScript types are explicitly defined
- Test both presence of elements AND absence when props are omitted
- Don't hard-code content - make component reusable via props

### Git Intelligence Summary

**Recent Work Pattern Analysis (Last 5 Commits):**

**Commit a23b7ab: "fixing case issue for persisted data"**
- Backend fix for difficulty field casing issue
- Updated `coaching-content-library-platform/src/models/content.py` to add Difficulty enum
- Updated `coaching-content-library-platform/src/storage/sqlite.py` to normalize difficulty values
- **Pattern:** Backend data normalization to match frontend expectations

**Commit cb268a7: "update"**
- Added story 2-4 file and test files
- Modified sprint-status.yaml
- **Pattern:** Story files and tests committed together

**Commit 4c43879: "refactor(frontend): improve DrillGrid component and tests"**
- Refactored DrillGrid.tsx component
- Improved test file DrillGrid.test.tsx
- Modified Library.tsx integration
- **Pattern:** Iterative refinement after initial implementation

**Architecture Decisions from Git History:**
1. **Component Size:** Small, focused components (DrillGrid is minimal)
2. **Test Coverage:** Every component has corresponding test file
3. **Integration Pattern:** Modify consuming components (Library.tsx) to integrate new components
4. **Story Documentation:** Comprehensive story files with dev notes

**Code Patterns Established:**
- Named exports for components: `export function ComponentName(...)`
- Separate props interfaces: `export interface ComponentNameProps { ... }`
- Test files in `__tests__/` subdirectory
- Tailwind utility classes for styling (no custom CSS)
- TypeScript strict mode with explicit typing

**Files to Follow Same Pattern:**
- Create EmptyState.tsx (expect ~60 lines)
- Create corresponding test file in `__tests__/`
- Modify Library.tsx to integrate EmptyState (expect ~10-15 line change)

**Testing Insights:**
- Tests use React Testing Library standard: `render`, `screen`, `expect`
- Tests verify both rendering AND behavior (onClick handlers, etc.)
- Tests check conditional rendering based on props

### Latest Tech Information

**Tailwind CSS v4.1.18 (Current Version - v4 API):**
- **Breaking Change Alert:** Tailwind v4 has different API than v3
- Project uses PostCSS 8.5.6 for Tailwind processing
- Custom theme defined in `tailwind.config.js` with project colors
- Utility-first approach: components use inline Tailwind classes
- No need for custom CSS files - all styling via Tailwind utilities
- Responsive design uses standard breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)

**EmptyState Implementation Best Practices (2026 Standards):**
- Use semantic HTML: `<div>` with proper ARIA attributes if interactive
- Combine icon + text in flex container for proper alignment
- Icon sizing: `w-16 h-16` to `w-20 h-20` for empty states
- Consistent spacing: `gap-4` between elements
- Accessibility: Ensure sufficient color contrast (gray-600 meets WCAG AA)
- Reusability: Props-based configuration for different scenarios

**Lucide React Icons v0.562.0 (Latest Stable):**
- Tree-shakeable imports: `import { FolderOpen, SearchX } from 'lucide-react'`
- Default size: 24x24px (can override with className)
- Fully accessible: Icons have proper aria attributes
- No custom icon configuration needed
- Supports className prop for Tailwind styling

**React 19.2.0 Features Relevant to This Story:**
- Improved TypeScript support with better type inference
- Functional components with explicit typing preferred
- Props destructuring in function signature: `function Component({ prop }: Props)`
- Optional chaining for optional callbacks: `onAction?.()`

**TypeScript 5.9.3 (Current Version):**
- Strict mode enabled in project (enforced by tsconfig.json)
- Enhanced null safety: props with `?` are `type | undefined`
- Explicit return types recommended: `function EmptyState(): JSX.Element`
- Type imports: `import type { SomeType } from '@/lib/types'`

**Testing Library Updates:**
- React Testing Library standard approach: `screen.getByText`, `screen.getByRole`
- Prefer semantic queries: `getByRole`, `getByLabelText` over `getByTestId`
- No mocking needed for simple component tests
- Assertions: `expect(element).toBeInTheDocument()`, `expect(element).toHaveTextContent()`

**Performance Considerations:**
- EmptyState is lightweight, non-interactive component (no state, no effects)
- Conditional rendering: only renders when needed (data?.items.length === 0)
- Icons are tree-shaken (only imported icons are bundled)
- Tailwind classes are purged in production build (unused classes removed)

**Security Notes:**
- No user input in EmptyState (all content passed as props)
- XSS not a concern (static text and icons only)
- No external dependencies beyond project stack

### Project Context Reference

**Component Standards:**
- ALWAYS export props interfaces separately
- ALWAYS use named exports (no default exports)
- ALWAYS use `@/` path alias (never relative imports)
- ALWAYS use `cn()` utility for className merging when conditional classes needed

**Color Standards (from project-context.md):**
- Primary brand color: `hockey-blue` (#1e3a5f)
- Accent color: `ice-blue` (#38bdf8)
- Use for EmptyState icon: `text-ice-blue` or `text-ice-blue-400`
- Text colors: `text-hockey-blue` for headings, `text-gray-600` for body text

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

- Created reusable EmptyState component following TDD approach (tests first, then implementation)
- Component accepts props for title, message, optional actionLabel, onAction callback, custom icon, and buttonVariant
- Default icon is Lucide FolderOpen in ice-blue color (matching theme)
- Layout uses Tailwind flex utilities for centering (flex flex-col items-center justify-center)
- Integrated into Library.tsx, replacing inline EmptyState with reusable component
- Updated Library.test.tsx to match new component text and button labels
- All tests passing (55/55, 1 skipped) - no regressions introduced
- Component is fully reusable for future empty states (search, filters, etc.)
- Used shadcn/ui Button component for CTA button with customizable variant
- Followed project standards: @/ imports, named exports, separate props interface, explicit return types
- Code review fixes applied: added accessibility attributes, error handling, responsive text sizing, integration tests
- Task 8 (Manual Verification) completed - user verified empty state works correctly in browser

### File List

**New Files Created:**
- `coaching-content-library-web/src/components/ui/EmptyState.tsx` (46 lines)
- `coaching-content-library-web/src/components/ui/__tests__/EmptyState.test.tsx` (140 lines)

**Files Modified:**
- `coaching-content-library-web/src/pages/Library.tsx` (replaced inline EmptyState with reusable component, added imports)
- `coaching-content-library-web/src/pages/__tests__/Library.test.tsx` (updated test expectations for new component, added integration test)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (updated story status: ready-for-dev → in-progress → review)
- `_bmad-output/implementation-artifacts/2-5-empty-state-component.md` (this story file)

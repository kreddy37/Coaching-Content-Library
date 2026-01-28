# Story 2.3: Responsive Grid Layout

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a coach,
I want the drill library to adapt to my device screen size,
so that I can browse drills comfortably on mobile, tablet, or desktop.

## Acceptance Criteria

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

## Tasks / Subtasks

- [x] **Task 1: Create `DrillGrid` Component Structure**
  - [x] 1.1: Create `src/components/drills/DrillGrid.tsx` file.
  - [x] 1.2: Define `DrillGridProps` interface to accept `drills: ContentItem[]`.
  - [x] 1.3: Set up the base `div` with `grid` class.
  - [x] 1.4: Map over `drills` prop and render `DrillCard` for each. (AC: #1)

- [x] **Task 2: Implement Responsive Grid Layout (Mobile)**
  - [x] 2.1: Apply `grid-cols-1` for mobile viewport. (AC: #2)
  - [x] 2.2: Ensure `gap-4` for mobile. (AC: #1)
  - [x] 2.3: Add horizontal padding (`px-4`) to the main container of the grid.

- [x] **Task 3: Implement Responsive Grid Layout (Tablet)**
  - [x] 3.1: Apply `md:grid-cols-2` for tablet viewport. (AC: #3)
  - [x] 3.2: Ensure `md:gap-6` for tablet. (AC: #1)
  - [x] 3.3: Adjust horizontal padding (`md:px-6`).

- [x] **Task 4: Implement Responsive Grid Layout (Desktop)**
  - [x] 4.1: Apply `lg:grid-cols-3` and `xl:grid-cols-4` (for 3-4 columns) for desktop viewport. (AC: #4)
  - [x] 4.2: Ensure `lg:gap-6` for desktop. (AC: #1)
  - [x] 4.3: Set `max-w-7xl mx-auto` to center the grid with a max width. (AC: #4)

- [x] **Task 5: Integrate `DrillGrid` into `Library.tsx`**
  - [x] 5.1: Import `DrillGrid` into `src/pages/Library.tsx`.
  - [x] 5.2: Replace the existing `div` that renders `DrillCard`s with the `DrillGrid` component, passing the `drills` prop.

- [x] **Task 6: Create Unit Tests for `DrillGrid` Component**
  - [x] 6.1: Create `src/components/drills/__tests__/DrillGrid.test.tsx` with failing tests.
  - [x] 6.2: Test `DrillGrid` renders correctly with various numbers of `DrillCard`s.
  - [x] 6.3: Test responsive classes are applied using mocked window width (advanced, optional for JSDOM).

- [ ] **Task 7: Visual Verification**
  - [ ] 7.1: Run `npm run dev` and verify responsive behavior in browser dev tools.
  - [ ] 7.2: Check grid column counts on mobile, tablet, desktop.
  - [ ] 7.3: Verify gap spacing and centering.
  - [ ] 7.4: Ensure no horizontal scrolling or content overflow.

## Dev Notes

### CRITICAL LEARNINGS FROM PREVIOUS STORIES (Epic 2)

**From Story 2.1 (Library Page & Data Fetching):**
- **Data fetching:** `useContentList` hook, TanStack Query for server state.
- **Loading/Error States:** Implemented in `Library.tsx` (LoadingSkeleton, ErrorState, EmptyState).

**From Story 2.2 (DrillCard Component):**
- **Component Patterns:**
  - Exported props interface separately (`DrillCardProps`).
  - Named exports only.
  - `@/` path alias MANDATORY - no relative imports.
  - TypeScript strict mode with explicit types.
- **Accessibility:** `DrillCard` is keyboard accessible (`role="button"`, `tabIndex={0}`, `onKeyDown` handler).
- **Styling:** Consistent use of `cn()` utility for Tailwind classes.
- **Dependencies:** `shadcn/ui Card` primitive, `lucide-react` icons.

**Key Implementation Details from Story 2.2 Relevant to Grid:**
- `DrillCard` component expects `ContentItem` as a prop.
- `DrillCard` handles its own styling, including rounded corners, hover effects, and aspect ratio for thumbnails/placeholders. This means `DrillGrid` primarily manages the grid container.

### Architectural Requirements (Must Follow)

**Frontend Project Organization:**
- New component `DrillGrid.tsx` should reside in `src/components/drills/`.
- Corresponding test file in `src/components/drills/__tests__/`.

**Styling Solution:**
- Utilize Tailwind CSS for all grid-related styling (e.g., `grid`, `grid-cols-X`, `gap-X`).
- Refer to `tailwind.config.js` for custom theme colors (e.g., `hockey-blue`, `ice-blue`) and spacing scale.

**UX Design Specification Requirements (from ux-design-specification.md):**

**Grid System:**
- **Mobile (<768px):** 1 column, `gap-4` (16px), `px-4` (16px margins).
- **Tablet (768-1024px):** 2 columns, `md:gap-6` (24px), `md:px-6` (24px margins).
- **Desktop (>1024px):** 3-4 columns (`lg:grid-cols-3 xl:grid-cols-4`), `lg:gap-6` (24px), `max-w-7xl mx-auto` (centered, max width).

**Responsive Design:**
- Mobile-first approach is mandatory.
- Smooth transitions between breakpoints.
- No horizontal scroll at any breakpoint.

### Project Structure Notes

- A new `DrillGrid.tsx` component will be created in `coaching-content-library-web/src/components/drills/`.
- This component will be responsible for defining the responsive grid layout.
- `coaching-content-library-web/src/pages/Library.tsx` will be modified to use this new `DrillGrid` component.

### References

- **Epics File:** `_bmad-output/planning-artifacts/epics.md` - (Contains the full story and ACs)
- **Architecture Decisions:** `_bmad-output/planning-artifacts/architecture.md` - (Details on frontend project structure and styling)
- **UX Design Specification:** `_bmad-output/planning-artifacts/ux-design-specification.md` - (Precise grid system breakpoints, margins, and gaps)
- **Project Context:** `_bmad-output/project-context.md` - (General coding standards and patterns)
- **Tailwind CSS Grid Documentation:** https://tailwindcss.com/docs/grid-template-columns (for usage of `grid-cols-X`, `gap-*`, responsive prefixes)

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro

### Debug Log References
- Implementation followed TDD cycle: created failing test, implemented component, confirmed tests pass.
- All tests passed after implementation and integration into Library.tsx.

### Completion Notes List
- Created `DrillGrid.tsx` component with responsive grid classes.
- Integrated `DrillGrid` into `Library.tsx` page.
- Created passing unit test for `DrillGrid`.
- Tasks 1-6 are complete. Task 7 (Visual Verification) is pending manual review.

### File List
- `coaching-content-library-web/src/components/drills/DrillGrid.tsx` (NEW)
- `coaching-content-library-web/src/components/drills/__tests__/DrillGrid.test.tsx` (NEW)
- `coaching-content-library-web/src/pages/Library.tsx` (MODIFIED)

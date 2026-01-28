---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - '_bmad-output/project-context.md'
  - 'CLAUDE.md'
date: '2026-01-07'
author: 'Kohl'
---

# Product Brief: Coaching-content-library

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

**Coaching-content-library** is a personal AI-powered content management system built by a goalie coach to solve the broken retrieval problem in coaching content discovery. While social media platforms excel at surfacing valuable drill content, they fail catastrophically at helping coaches use that content later—saved posts become buried in mixed collections, and keyword search returns irrelevant results because it doesn't understand the nuances of position-specific coaching.

This project transforms Kohl's 5-year coaching practice by creating a curated library of drill content captured via Discord bot, enhanced with AI-powered features including automatic tagging, semantic search, and intelligent drill recommendations. Rather than winging lessons or repeatedly using the same drills because they're the ones he remembers, Kohl will have instant access to contextually relevant drills matched to specific skills and goalie development needs.

As an AI engineering portfolio piece, the project demonstrates practical integration of vector embeddings, LLM-powered content analysis, and agentic workflows in a full-stack application—showcasing not just technical capability, but the ability to identify real problems and architect AI solutions that create genuine value.

---

## Core Vision

### Problem Statement

Goalie coaches encounter valuable drill content passively through social media (TikTok, Instagram, YouTube), but current tools make that content effectively unusable when it's actually needed. The workflow breaks down at retrieval:

**Discovery works** → Algorithms surface great content
**Storage works** → Platform save features capture content
**Retrieval is broken** → Content buried in mixed collections, keyword search returns irrelevant results

When planning lessons, coaches either:
- Spend excessive time hunting through scattered collections across multiple apps
- Give up and wing it, using only drills they recently saw or can remember
- Miss opportunities to match drills precisely to goalie skill needs

### Problem Impact

For Kohl specifically (5-year private goalie coach):
- **Time waste:** Lesson brainstorming takes too long when he can't remember what each goalie needs or retrieve appropriate drills
- **Limited variety:** Reuses familiar drills instead of leveraging curated content
- **Missed opportunities:** Great drills seen on social media are effectively lost because retrieval friction is too high
- **Suboptimal matching:** Can't quickly find drills that match specific skills, age groups, or individual goalie development stages

The core frustration: "I know I saved a perfect drill for this, but finding it takes longer than just making something up."

### Why Existing Solutions Fall Short

**Social Media Save Features:**
- Content gets buried in mixed collections (drills mixed with personal saves)
- No drill-specific organization or tagging
- Keyword search doesn't understand coaching context (searches for "butterfly recovery drill" return irrelevant content or non-hockey results)

**Generic Save Tools (Notion, Pocket, etc.):**
- Require manual tagging and organization (too much friction)
- No video content understanding
- No coaching-specific intelligence

**ChatGPT/Generic AI:**
- Doesn't know which drills Kohl likes or trusts
- Can't distinguish drills that work from those that instill bad habits
- No persistent curated library
- Lacks integration with coaching workflow

**Coaching Platforms:**
- Don't integrate with social media content sources
- Still rely on keyword search, not semantic understanding
- Not built for goalie-specific coaching nuances

### Proposed Solution

**Coaching-content-library** creates a coach-curated, AI-enhanced drill library with intelligent retrieval that understands goalie coaching context.

**Core Workflow:**
1. **Low-friction capture:** See drill on social media → Copy URL → Paste to Discord bot → Provide context → Saved to library
2. **AI enhancement:** LLM automatically analyzes and tags drills (skills, difficulty, age group, drill type)
3. **Intelligent retrieval:** Semantic search finds drills by concept, not keywords ("show me drills for lateral tracking" → relevant results regardless of exact wording)
4. **Contextual discovery:** Similar drill recommendations when viewing any drill
5. **Future: Chat interface:** Natural language queries ("show me drills for building a lesson on butterfly mechanics for intermediate goalies") with multi-drill suggestions

**Technical Architecture:**
- **Frontend:** React + TypeScript web UI with hockey-themed design
- **Backend:** FastAPI + Python with platform-specific content ingestors (YouTube, TikTok, Instagram, Reddit)
- **AI Features:** Vector embeddings (semantic search), LLM-powered auto-tagging, recommendation engine
- **Capture:** Discord bot for URL submission with guided metadata capture
- **Future:** Agentic workflow for intelligent lesson planning suggestions

**MVP Scope (under 6 months):**
- Save and filter capabilities
- Auto-tagging of drill metadata
- Semantic search
- Similar drill suggestions
- Clean, hockey-themed UI

**Future Enhancements:**
- Chat interface for lesson planning inspiration
- Individual goalie tracking and progress monitoring
- Personalized drill recommendations per goalie

### Key Differentiators

**1. Coach-Curated Intelligence**
Unlike generic AI solutions, this library contains only drills Kohl has vetted based on 5 years of coaching experience. He knows what works, what instills bad habits, and what's appropriate for different skill levels.

**2. Position-Specific Context**
The AI understands goalie coaching nuances that generic search algorithms miss—the difference between butterfly recovery, lateral tracking, and post integration; age-appropriate progression; skill interdependencies.

**3. Workflow Integration**
Captures content at the moment of discovery (Discord bot) and surfaces it at the moment of need (lesson planning), eliminating the friction that makes social media saves unusable.

**4. AI Engineering Showcase**
Demonstrates practical integration of multiple AI capabilities in a real-world application:
- Vector embeddings for semantic understanding
- LLM-powered content analysis and tagging
- Recommendation systems
- Future: Agentic workflows for complex query handling

This is not "AI for AI's sake"—each feature solves a specific retrieval or organization problem that makes coaching more effective.

**5. Built by a Coach, for a Coach**
Solves a real problem the builder experiences daily, showcasing ability to identify genuine pain points and architect appropriate solutions—a critical skill for AI engineers building client-facing applications.

---

## Target Users

### Primary Users

#### Kohl - The Pragmatic Goalie Coach

**Background:**
Kohl is a 5-year private goalie coach with a technical background transitioning into AI engineering. He runs 2-3 coaching sessions per week, working with individual goalies or small groups (3-4 goalies). Each session requires 30-60 minutes of lesson planning, where he designs progressive drill sequences tailored to each goalie's skill development needs.

**Current Challenge:**
Kohl's lesson planning is constrained by what he can recall in the moment. Social media feeds him great drill content passively (TikTok, Instagram), but when planning time comes, that content is effectively lost—buried in mixed collections across multiple apps. His challenge isn't lack of coaching expertise; it's lack of efficient retrieval and variety at the moment of need.

**Specific Pain Points:**
- **Limited variety:** Reuses familiar drills because finding new ones takes longer than the planning time available
- **Drill validation overhead:** Spends significant time mentally validating whether a drill is practical and truly targets the intended skill
- **Group drill struggle:** Particularly challenged by keeping 3-4 goalies simultaneously engaged; group drills require different thinking than 1-on-1 sessions
- **Missing angles:** Wants to approach skills from multiple perspectives but brainstorming all angles takes too long
- **Confidence gap:** When reusing drills, wonders if there's a better option he's missing

**Goals:**
- Spend less time hunting and validating, more time on creative lesson design
- Access drill variety that expands beyond what he can recall
- Gain confidence that he's using the best available drill for each situation
- Find group-specific drills that keep multiple goalies engaged simultaneously
- Hit multiple angles/approaches to the same skill within a single lesson

**Tech Profile:**
Highly tech-comfortable and open to new tools. Values solutions that are thoughtfully designed for his specific workflow. Willing to invest setup time if the long-term payoff is clear.

**Success Looks Like:**
Opens the tool → describes what he needs (skill focus, goalie level, group vs. individual) → receives curated, validated drill options immediately → picks the right drill with confidence → moves on to designing the lesson structure. Planning time drops from 30-60 minutes to 15-30 minutes, with higher-quality, more varied lesson plans.

---

### Secondary Users

#### Sarah Chen - The AI Product Engineer (Employer Evaluator)

**Background:**
Sarah is a senior AI engineer at a 50-person SaaS company looking to enhance their product with AI capabilities. Her team is hiring an ML/AI engineer who can identify practical problems, architect appropriate solutions, and ship production-quality code—not just someone who can follow LLM tutorials.

**Evaluation Context:**
Sarah reviews portfolios and conducts technical interviews. She's seen countless "I built a chatbot" and "I fine-tuned a model" projects. What she's looking for is someone who can:
1. Identify a real problem (not a manufactured one)
2. Choose appropriate AI techniques (not over-engineering or hype-chasing)
3. Build clean, maintainable architecture
4. Ship something that actually works and creates value

**What She Evaluates:**
- **Problem-solution fit:** Does this solve a real problem the builder actually experiences?
- **Architecture decisions:** Why vector embeddings? Why this RAG approach? What trade-offs were considered?
- **Code quality:** Is this production-ready or a prototype hack? Clean abstractions? Error handling?
- **AI integration thoughtfulness:** Are AI features solving specific problems, or just "AI for AI's sake"?
- **Scope management:** Did they ship something complete, or is it half-finished across 10 features?

**Red Flags She Watches For:**
- "I used every trendy AI technique I could find"
- Code that works but would be unmaintainable in a team setting
- Over-scoped projects that are 30% done across everything
- Solutions looking for problems

**Green Flags She Looks For:**
- Clear problem statement with real user pain
- Appropriate tool selection with justification
- Clean architecture that someone else could extend
- Complete MVP with clear future roadmap
- Evidence of iteration and learning

**Evaluation Method:**
She'll ask for a live demo, dive into the codebase during technical discussions, and ask probing questions about design decisions. She wants to understand not just what was built, but *why* it was built that way and what was learned.

**Success Looks Like:**
After reviewing Coaching-content-library, Sarah thinks: "This person understands how to integrate AI practically into products. They can identify real problems, architect clean solutions, and ship complete features. They'd be a strong addition to our team."

---

### User Journeys

#### Primary User Journey: Kohl Planning a Lesson

**Discovery Phase:**
- Kohl passively encounters drill content on TikTok/Instagram throughout the week
- Sees valuable content → copies URL → pastes to Discord bot → provides brief context → content saved to library
- Library automatically analyzes and tags drills (AI-powered, zero manual work)

**Planning Phase (2x per week per goalie):**
1. **Context setting:** Opens planning session for specific goalie (e.g., "14U goalie, needs work on butterfly recovery")
2. **Initial search:** Uses semantic search: "drills for getting back up quickly after butterfly" → receives contextually relevant results (not keyword-dependent)
3. **Drill evaluation:** Clicks a promising drill → sees full details, auto-generated tags, similar drill suggestions
4. **Creative exploration:** "Similar drills" feature exposes related approaches he hadn't considered
5. **Group adaptation:** Filters for "group drills" when planning multi-goalie session
6. **Confidence check:** Before reusing a familiar drill, searches to confirm there's not a better option

**Success Moment:**
Planning time cut in half. More varied, creative lessons. Confidence that he's using the best available drill, not just the one he remembered.

**Future Journey (Chat Interface):**
Opens planner → types "I need drills for building a lesson on butterfly mechanics for intermediate goalies" → receives curated list of 5-8 drills organized by progression → picks combinations → moves to lesson structure design.

#### Secondary User Journey: Sarah Evaluating the Portfolio

**Discovery Phase:**
- Reviews Kohl's application and portfolio
- Sees Coaching-content-library listed as key project
- Clicks through to project showcase

**Initial Review:**
1. **Problem understanding:** Reads the problem statement, immediately recognizes it as a real problem (content discovery vs. retrieval breakdown)
2. **Solution appropriateness:** Sees AI techniques aligned with specific problems (semantic search for retrieval, LLM tagging for automation, not just "AI because trendy")
3. **Scope assessment:** Notes MVP is complete with clear future roadmap (not over-promised)

**Technical Deep Dive:**
1. **Live demo:** Kohl walks through the Discord bot workflow, semantic search, similar drill recommendations
2. **Architecture discussion:** Sarah asks about vector embedding approach, RAG architecture, why ChromaDB vs. other options
3. **Code review:** Looks at backend structure, frontend patterns, test coverage, error handling
4. **Trade-off exploration:** "Why Discord bot instead of browser extension?" (Answer: lower friction, faster to ship, fits personal workflow)

**Decision Criteria:**
- ✅ Real problem with clear user pain (Kohl himself)
- ✅ Appropriate AI technique selection (semantic search, auto-tagging, recommendations)
- ✅ Clean, maintainable code architecture
- ✅ Complete MVP showing follow-through
- ✅ Thoughtful trade-offs and scope management
- ✅ Evidence this will actually be used (not a throwaway project)

**Success Moment:**
Sarah thinks: "This person can ship AI features that create real value. They'd fit well on our team." Moves forward with interview process.

---

## Success Metrics

### User Success Metrics (Coaching Practice)

**Primary Success Indicators:**

1. **Adoption Velocity**
   - **Target:** 50 drills saved to library within first 90 days
   - **Measurement:** Drill count in database
   - **Success Signal:** Consistent weekly additions (averaging 4-5 drills/week) indicating the Discord bot workflow is frictionless enough for regular use
   - **Current Status:** Discord bot already functional (built and working in `coaching-content-library-platform/src/bot`)

2. **Planning Time Efficiency**
   - **Target:** Lesson planning time reduced to 15-30 minutes (from current 30-60 minutes)
   - **Measurement:** Self-reported time tracking during planning sessions
   - **Success Signal:** Spending less time hunting/validating, more time on creative lesson design

3. **Lesson Plan Coverage**
   - **Target:** Tool used for every lesson plan (2-3x per week)
   - **Measurement:** Search/retrieval activity logs aligned with coaching schedule
   - **Success Signal:** Tool becomes default planning workflow, not occasional supplement

**Quality Indicators (Qualitative):**

4. **Drill Variety & Entropy**
   - **Criteria:** High search result entropy while maintaining relevance to queries
   - **Measurement:** Subjective judgment during planning - "Am I seeing diverse options that all make sense?"
   - **Success Signal:** No longer defaulting to familiar drills; exploring new approaches confidently

5. **Goalie Application Success**
   - **Criteria:** Goalies applying lesson insights to practices and games
   - **Measurement:** Direct feedback from goalies and observable performance improvements
   - **Success Signal:** Evidence that better drill selection leads to better skill transfer

---

### Business Objectives (Portfolio & Career)

**Primary Objective: Resume-Ready AI Engineering Portfolio Piece**

1. **Technical Completeness**
   - **Criteria:** MVP demonstrates core AI capabilities
   - **Required Features:**
     - ✅ LLM-powered auto-tagging (working, accurate)
     - ✅ Semantic search (contextual understanding, not keyword matching)
     - ✅ Recommendation engine (similar drills based on content analysis)
   - **Success Signal:** All three AI features functional and demonstrable

2. **Production Deployment**
   - **Target:** Deployed and accessible via public URL
   - **Criteria:** Employers can access and explore independently
   - **Success Signal:** Link on resume → live, working application

3. **Code Quality & Architecture**
   - **Criteria:** Clean, maintainable codebase demonstrating software engineering best practices
   - **Measurement:** Clean abstractions, error handling, production-ready patterns
   - **Success Signal:** Code employer would feel comfortable extending in a team setting

4. **UI Polish**
   - **Criteria:** Professional, polished interface (not prototype-looking)
   - **Success Signal:** Hockey-themed design, responsive layout, smooth user experience

**Timeline Objective:**

5. **Speed to Market**
   - **Target:** MVP completed in 1-2 months (aggressive, achievable with full-time focus)
   - **Milestone Tracking:**
     - Week 1-2: Backend AI features (auto-tagging, embeddings, semantic search)
     - Week 3-4: Frontend build-out, integrate with existing Discord bot
     - Week 5-6: Recommendation engine, polish, deployment
     - Week 7-8: Buffer for unexpected challenges, final polish
   - **Success Signal:** Resume-ready link available for immediate job applications
   - **Advantage:** Discord bot capture workflow already complete, reducing development timeline

---

### Key Performance Indicators

**User Adoption KPIs:**
- **Library Growth:** 50+ drills within 90 days (17 drills/month average)
- **Weekly Usage:** Tool accessed 2-3x per week (aligned with coaching schedule)
- **Search Activity:** Average 3-5 searches per planning session

**Technical Performance KPIs:**
- **Auto-Tagging Accuracy:** Subjective validation - "Are the tags actually useful?"
- **Search Relevance:** Semantic search returns contextually appropriate results (not just keyword matches)
- **Recommendation Quality:** Similar drills feel genuinely related and useful

**Portfolio Impact KPIs:**
- **Deployment Status:** Live, accessible URL ✅
- **Interview Conversion:** Employers request live demo or technical deep dive after reviewing project
- **Code Review Feedback:** Positive assessment of architecture and code quality during technical interviews

**Leading Indicators (Early Success Signals):**
- **Completed:** Discord bot saves drills successfully ✅
- **First Month:** 15-20 drills saved, semantic search returning relevant results
- **Two Months:** MVP deployed, all core features working, resume updated with project link
- **Three Months:** 50 drills reached, tool integrated into regular coaching workflow

---

## MVP Scope

### Core Features

**1. Content Capture & Storage** ✅ (Already Complete)
- Discord bot integration for drill URL submission
- Metadata collection: `drill_tags`, `drill_description`, `difficulty`, `age_group`, `equipment`
- Support for YouTube, TikTok, Instagram, Reddit sources
- URL storage with automatic metadata extraction where available

**2. LLM-Powered Auto-Tagging**
- Automatic tag enhancement that augments user-provided `drill_tags`
- Triggers on save (max rate: 1 per 5 minutes)
- Analyzes drill description and content to suggest relevant tags
- Adds tags without replacing user-provided tags
- Quality threshold: subjectively validated by user as "relevant and useful"

**3. Semantic Search**
- Text-based semantic search (no video content analysis)
- Searches across `drill_description` and `drill_tags`
- Returns contextually relevant drills based on meaning, not just keywords
- Example: "butterfly recovery" finds relevant drills regardless of exact wording
- Quality threshold: results feel contextually appropriate to search intent

**4. Similar Drill Recommendations**
- Recommendation engine based on two factors:
  - Tag similarity (shared tags between drills)
  - Semantic similarity of drill descriptions
- Shown when viewing individual drill details
- Quality threshold: "interesting suggestions" that feel genuinely related

**5. Advanced Filtering**
- Filter library by:
  - Tags (including group drill tag)
  - Difficulty level
  - Age group
- Combinable filters for precise drill discovery
- Real-time filter application

**6. Group Drill Support**
- Special "group drill" tag to identify drills for 3-4 goalie sessions
- Filterable to find group-specific content quickly
- Addresses challenge of keeping multiple goalies engaged simultaneously

**7. Professional Web UI**
- Clean, hockey-themed design (primary: deep blue #1e3a5f, accent: ice blue #38bdf8)
- Responsive layout (mobile, tablet, desktop)
- Key views:
  - Library grid with drill cards
  - Drill detail view with full metadata
  - Search and filter interface
- Portfolio-ready polish for employer presentation

### Out of Scope for MVP

**Explicitly Excluded from Initial Release:**

1. **Chat Interface for Lesson Planning**
   - Natural language queries like "show me drills for butterfly mechanics"
   - Multi-drill suggestions for lesson building
   - Deferred to post-MVP as most complex feature

2. **Individual Goalie Tracking**
   - Per-goalie progress monitoring
   - Personalized drill recommendations per athlete
   - Historical tracking of what each goalie has worked on

3. **Practice Plan Export & Save**
   - Building and saving lesson plans within the app
   - Exporting plans to documents or other formats
   - Plan templates or structures

4. **Video Transcription**
   - Automatic transcription of YouTube videos
   - Speech-to-text analysis for richer semantic understanding
   - Future enhancement for more accurate tagging

5. **Semantic Clustering**
   - Automatic organization of drills into clusters
   - Visual grouping of similar content
   - Advanced library organization beyond tags/filters

6. **Visual/Video Content Analysis**
   - Computer vision analysis of drill videos
   - Automatic detection of drill mechanics from video
   - Visual similarity matching

**Rationale:** These features are valuable but not essential for solving the core retrieval problem. The MVP focuses on making saved content discoverable and useful, with AI features that enhance organization and search. More complex features (chat interface, video analysis, goalie tracking) build on this foundation once core value is proven.

### MVP Success Criteria

**Technical Completeness:**
- ✅ All three AI features functional and demonstrable:
  - LLM auto-tagging working with relevant, useful tags
  - Semantic search returning contextually appropriate results
  - Similar drill recommendations feeling genuinely related
- ✅ Discord bot capture workflow integrated with web UI
- ✅ Filtering system working across tags, difficulty, age_group
- ✅ Clean, responsive UI with professional polish

**Deployment & Accessibility:**
- ✅ Live deployment with public URL
- ✅ Accessible for employer review without setup
- ✅ Link-ready for resume and job applications

**User Adoption (Coaching Practice):**
- ✅ 50 drills saved within first 90 days (17/month average)
- ✅ Tool used for every lesson plan (2-3x per week)
- ✅ Planning time reduced to 15-30 minutes (from 30-60 minutes)
- ✅ Subjective validation: "Am I seeing diverse, relevant options?"

**Code Quality (Portfolio):**
- ✅ Clean, maintainable architecture demonstrating software engineering best practices
- ✅ Code employer would feel comfortable extending in a team setting
- ✅ Proper error handling, abstractions, and production-ready patterns

**Timeline:**
- ✅ MVP completed in 1-2 months
- ✅ Advantage: Discord bot already complete, reducing development timeline
- ✅ Full-time focus enables aggressive but achievable schedule

### Future Vision

**Post-MVP Evolution (2-6 months after launch):**

**Phase 2: Intelligent Lesson Planning**
- Chat interface for natural language drill queries
- Multi-drill suggestions organized by lesson progression
- Query examples:
  - "Show me drills for building a lesson on butterfly mechanics for intermediate goalies"
  - "Find group drills for lateral tracking, bantam level"
- Agentic workflow demonstrating complex AI orchestration

**Phase 3: Enhanced Content Understanding**
- Video transcription integration (Whisper API)
- Richer semantic search incorporating spoken content
- Automatic drill description generation from transcripts
- Improved auto-tagging accuracy with video content context

**Phase 4: Smart Organization**
- Semantic clustering to automatically group related drills
- Visual drill library with clustered organization
- Discovery of drill patterns and progressions
- "Drills like this" expanded to cluster-based navigation

**Phase 5: Personalized Coaching**
- Individual goalie tracking and progress monitoring
- Per-athlete drill history and recommendations
- Skill gap analysis and suggested focus areas
- Personalized lesson planning: "Show me drills for John Doe's next session"
- Multi-goalie session optimization

**Phase 6: Complete Lesson Builder**
- Practice plan creation and saving
- Drill sequencing and progression planning
- Plan templates for common lesson types
- Export to PDF, docs, or coaching platforms
- Session notes and post-lesson feedback capture

**Long-Term Vision (1-2 years):**
A comprehensive AI-powered coaching assistant that:
- Knows every drill you've curated and trusts
- Understands each goalie's development journey
- Suggests complete, personalized lesson plans with one query
- Learns from your preferences and coaching style
- Surfaces the right drill at the right time, every time

**Expansion Opportunities:**
- Community features: share drill collections with other coaches
- Mobile app for on-ice drill reference
- Integration with goalie training platforms
- Video upload for private drill library
- Analytics on drill effectiveness and goalie improvement correlation

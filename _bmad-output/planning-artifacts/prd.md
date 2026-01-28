---
stepsCompleted: [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
inputDocuments:
  - '_bmad-output/planning-artifacts/product-brief-Coaching-content-library-2026-01-07.md'
  - '_bmad-output/project-context.md'
workflowType: 'prd'
lastStep: 11
briefCount: 1
researchCount: 0
brainstormingCount: 0
projectDocsCount: 0
date: '2026-01-07'
author: 'Kohl'
project_name: 'Coaching-content-library'
status: 'complete'
---

# Product Requirements Document - Coaching-content-library

**Author:** Kohl
**Date:** 2026-01-07

## Executive Summary

**Coaching-content-library** is an AI-powered content management system that solves the critical retrieval problem in goalie coaching content discovery. While social media platforms (TikTok, Instagram, YouTube) excel at surfacing valuable drill content, they fail catastrophically at helping coaches use that content when it's actually needed—saved posts become buried in mixed collections, and keyword search returns irrelevant results because it doesn't understand position-specific coaching nuances.

This project transforms lesson planning for private goalie coaches by creating a curated library of drill content captured via Discord bot, enhanced with three core AI features: LLM-powered auto-tagging (augmenting user-provided `drill_tags`), semantic search (text-based contextual understanding across `drill_description` and `drill_tags`), and intelligent drill recommendations (based on tag similarity and semantic description similarity). The system reduces lesson planning time from 30-60 minutes to 15-30 minutes while increasing drill variety and confidence in drill selection.

The Discord bot capture workflow is already complete and working, providing a significant head start on the 1-2 month aggressive MVP timeline. The primary user is Kohl, a 5-year private goalie coach running 2-3 sessions per week with individual goalies or groups of 3-4. The secondary audience is AI engineering employers at 50-person SaaS companies evaluating portfolio projects for practical AI integration, clean architecture, and complete MVPs.

### What Makes This Special

**1. Coach-Curated Intelligence**
Unlike generic AI solutions, this library contains only drills vetted through 5 years of coaching experience. The coach knows what works, what instills bad habits, and what's appropriate for different skill levels—creating a trusted, personalized knowledge base.

**2. Position-Specific Context**
The AI understands goalie coaching nuances that generic search algorithms miss: the difference between butterfly recovery, lateral tracking, and post integration; age-appropriate progression; skill interdependencies. This specialized understanding makes retrieval dramatically more relevant.

**3. Workflow Integration**
Captures content at the moment of discovery (Discord bot) and surfaces it at the moment of need (lesson planning), eliminating the friction that makes social media saves unusable. The capture-to-retrieval loop is optimized for the coach's actual workflow.

**4. AI Engineering Showcase**
Demonstrates practical integration of multiple AI capabilities solving specific problems:
- Vector embeddings for semantic understanding (contextual search, not keyword matching)
- LLM-powered content analysis and tagging (automatic enhancement of user tags)
- Recommendation systems (similar drills based on content similarity)
- Future: Agentic workflows for complex query handling

This is not "AI for AI's sake"—each feature solves a specific retrieval or organization problem that makes coaching more effective.

**5. Built by a Coach, for a Coach**
Solves a real problem the builder experiences daily in coaching practice, showcasing the ability to identify genuine pain points and architect appropriate AI solutions—a critical skill for AI engineers building client-facing applications.

## Project Classification

**Technical Type:** Web App (SPA)
**Domain:** General (AI-enhanced productivity)
**Complexity:** Medium
**Project Context:** Greenfield - new project

**Technology Stack:**
- **Frontend:** React 19.2.0 + TypeScript 5.9.3, Vite 7.2.4, TanStack Query 5.90.16, Tailwind CSS 4.1.18
- **Backend:** Python 3.12, FastAPI 0.104.0+, SQLAlchemy 2.0+, Pydantic 2.0+
- **AI Integration:** Vector embeddings, LLM APIs for auto-tagging, semantic similarity algorithms
- **Data:** `drill_tags` (array), `drill_description` (string), `difficulty`, `age_group`, `equipment`
- **Capture:** Discord bot (already complete) using discord.py 2.3.0+

**Classification Rationale:**
This is a web application providing browser-based access to an AI-enhanced drill library with semantic search, filtering, and recommendation features. While technically sophisticated (vector embeddings, LLM integration, recommendation engine), it operates in a general domain without regulatory compliance requirements. The complexity rating of "medium" reflects the advanced AI features balanced against the straightforward coaching productivity use case.

**Key Technical Characteristics:**
- Single-page application with responsive design (mobile, tablet, desktop)
- Hockey-themed UI (primary: deep blue #1e3a5f, accent: ice blue #38bdf8)
- Backend contract critical: PascalCase enums (`'YouTube'`), snake_case fields (`drill_tags`, `drill_description`)
- Real-time semantic search across text content
- Portfolio-ready deployment with public URL access

## Success Criteria

### User Success

**Primary Success Indicator:**
The tool transforms lesson planning from a time-consuming, memory-constrained process into a fast, confident, variety-rich workflow. Success is achieved when Kohl consistently chooses this tool over "winging it" because retrieval is faster and more reliable than recall.

**Measurable User Outcomes:**

1. **Planning Time Efficiency**
   - **Target:** Lesson planning reduced to 15-30 minutes (from current 30-60 minutes)
   - **Measurement:** Self-reported time tracking during planning sessions
   - **Success Signal:** Spending less time hunting/validating, more time on creative lesson design

2. **Adoption Velocity**
   - **Target:** 50 drills saved to library within first 90 days
   - **Measurement:** Drill count in database
   - **Success Signal:** Consistent weekly additions (averaging 4-5 drills/week) indicating frictionless capture workflow

3. **Workflow Integration**
   - **Target:** Tool used for every lesson plan (2-3x per week)
   - **Measurement:** Search/retrieval activity logs aligned with coaching schedule
   - **Success Signal:** Tool becomes default planning workflow, not occasional supplement

4. **Drill Variety & Confidence**
   - **Criteria:** High search result entropy while maintaining relevance to queries
   - **Measurement:** Subjective judgment during planning - "Am I seeing diverse options that all make sense?"
   - **Success Signal:** No longer defaulting to familiar drills; exploring new approaches confidently

5. **Goalie Application Success**
   - **Criteria:** Goalies applying lesson insights to practices and games
   - **Measurement:** Direct feedback from goalies and observable performance improvements
   - **Success Signal:** Evidence that better drill selection leads to better skill transfer

**User Success Moment:**
"I know I saved a perfect drill for this" → finds it in 30 seconds → picks it with confidence → moves on to lesson structure design.

### Business Success

**Primary Objective: Resume-Ready AI Engineering Portfolio Piece**

This project serves dual purposes: solving a real coaching problem while demonstrating AI engineering capabilities to employers at 50-person SaaS companies looking to enhance products with AI.

**Measurable Business Outcomes:**

1. **Technical Completeness**
   - **Criteria:** MVP demonstrates all three core AI capabilities
   - **Required Features:**
     - ✅ LLM-powered auto-tagging (working, subjectively "useful")
     - ✅ Semantic search (contextually appropriate results, not keyword matching)
     - ✅ Recommendation engine (similar drills feel genuinely related)
   - **Success Signal:** All three AI features functional and demonstrable in live demo

2. **Production Deployment**
   - **Target:** Deployed and accessible via public URL
   - **Criteria:** Employers can access and explore independently
   - **Success Signal:** Link on resume → live, working application (no setup required)

3. **Code Quality & Architecture**
   - **Criteria:** Clean, maintainable codebase demonstrating software engineering best practices
   - **Measurement:** Clean abstractions, error handling, production-ready patterns
   - **Success Signal:** Code employer would feel comfortable extending in a team setting

4. **UI Polish**
   - **Criteria:** Professional, polished interface (not prototype-looking)
   - **Success Signal:** Hockey-themed design, responsive layout, smooth user experience

5. **Speed to Market**
   - **Target:** MVP completed in 1-2 months with full-time focus
   - **Advantage:** Discord bot already complete, reducing development timeline
   - **Success Signal:** Resume-ready link available for immediate job applications

**Business Success Moment:**
Employer reviews portfolio → clicks link → explores live app → thinks "This person can ship AI features that create real value" → requests technical interview.

### Technical Success

**Core AI Features Performance:**

1. **Auto-Tagging Quality**
   - **Threshold:** Subjectively validated as "relevant and useful"
   - **Trigger:** Automatic on save (max rate: 1 per 5 minutes)
   - **Behavior:** Augments user-provided `drill_tags` (never replaces)
   - **Success:** Tags consistently add value beyond what user provided

2. **Semantic Search Relevance**
   - **Threshold:** Results feel contextually appropriate to search intent
   - **Capability:** Text-based search across `drill_description` and `drill_tags`
   - **Example:** "butterfly recovery" finds relevant drills regardless of exact wording
   - **Success:** Semantic understanding beats keyword search consistently

3. **Recommendation Quality**
   - **Threshold:** "Interesting suggestions" that feel genuinely related
   - **Algorithm:** Tag similarity + semantic similarity of descriptions
   - **Context:** Shown when viewing individual drill details
   - **Success:** Recommendations expose drill approaches user hadn't considered

**System Performance:**

- **Backend Contract Integrity:** PascalCase enums (`'YouTube'`), snake_case fields (`drill_tags`, `drill_description`) enforced consistently
- **Responsive UI:** Clean performance on mobile, tablet, desktop
- **Data Integrity:** Discord bot → database → web UI workflow functions reliably
- **Deployment Stability:** Public URL accessible without downtime during demo periods

### Measurable Outcomes

**Leading Indicators (Early Success Signals):**

- **Month 0 (Complete):** Discord bot saves drills successfully ✅
- **Month 1:** 15-20 drills saved, semantic search returning relevant results
- **Month 2:** MVP deployed, all core features working, resume updated with project link
- **Month 3:** 50 drills reached, tool integrated into regular coaching workflow

**Key Performance Indicators:**

**User Adoption:**
- Library Growth: 50+ drills within 90 days (17 drills/month average)
- Weekly Usage: Tool accessed 2-3x per week (aligned with coaching schedule)
- Search Activity: Average 3-5 searches per planning session

**Technical Performance:**
- Auto-Tagging Accuracy: Subjective validation - "Are the tags actually useful?"
- Search Relevance: Semantic search returns contextually appropriate results
- Recommendation Quality: Similar drills feel genuinely related and useful

**Portfolio Impact:**
- Deployment Status: Live, accessible URL ✅
- Interview Conversion: Employers request live demo or technical deep dive after reviewing project
- Code Review Feedback: Positive assessment of architecture and code quality during technical interviews

## Product Scope

### MVP - Minimum Viable Product

**Timeline:** 1-2 months with full-time focus

**Core Features (Must Have):**

1. **Content Capture & Storage** ✅ (Already Complete)
   - Discord bot integration for drill URL submission
   - Metadata collection: `drill_tags`, `drill_description`, `difficulty`, `age_group`, `equipment`
   - Support for YouTube, TikTok, Instagram, Reddit sources
   - URL storage with automatic metadata extraction where available

2. **LLM-Powered Auto-Tagging**
   - Automatic tag enhancement that augments user-provided `drill_tags`
   - Triggers on save (max rate: 1 per 5 minutes)
   - Analyzes drill description and content to suggest relevant tags
   - Adds tags without replacing user-provided tags
   - Quality threshold: subjectively validated by user as "relevant and useful"

3. **Semantic Search**
   - Text-based semantic search (no video content analysis)
   - Searches across `drill_description` and `drill_tags`
   - Returns contextually relevant drills based on meaning, not just keywords
   - Example: "butterfly recovery" finds relevant drills regardless of exact wording
   - Quality threshold: results feel contextually appropriate to search intent

4. **Similar Drill Recommendations**
   - Recommendation engine based on two factors:
     - Tag similarity (shared tags between drills)
     - Semantic similarity of drill descriptions
   - Shown when viewing individual drill details
   - Quality threshold: "interesting suggestions" that feel genuinely related

5. **Advanced Filtering**
   - Filter library by:
     - Tags (including group drill tag)
     - Difficulty level
     - Age group
   - Combinable filters for precise drill discovery
   - Real-time filter application

6. **Group Drill Support**
   - Special "group drill" tag to identify drills for 3-4 goalie sessions
   - Filterable to find group-specific content quickly
   - Addresses challenge of keeping multiple goalies engaged simultaneously

7. **Professional Web UI**
   - Clean, hockey-themed design (primary: deep blue #1e3a5f, accent: ice blue #38bdf8)
   - Responsive layout (mobile, tablet, desktop)
   - Key views:
     - Library grid with drill cards
     - Drill detail view with full metadata
     - Search and filter interface
   - Portfolio-ready polish for employer presentation

**Explicitly Out of MVP Scope:**
- Chat interface for lesson planning
- Individual goalie tracking
- Practice plan export & save
- Video transcription
- Semantic clustering
- Visual/video content analysis

**MVP Success Criteria:**
- All three AI features functional and demonstrable
- Discord bot capture workflow integrated with web UI
- Filtering system working across tags, difficulty, age_group
- Clean, responsive UI with professional polish
- Live deployment with public URL
- Code quality demonstrating best practices

### Growth Features (Post-MVP) - Dream Version

**Timeline:** 2-6 months after MVP launch

This phase represents the dream version of the application—what makes it truly exceptional for coaching practice and compelling as a portfolio piece.

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

### Vision (Future) - Extended Blue Sky

**Timeline:** 1-2 years

**Phase 6: Complete Lesson Builder**
- Practice plan creation and saving
- Drill sequencing and progression planning
- Plan templates for common lesson types
- Export to PDF, docs, or coaching platforms
- Session notes and post-lesson feedback capture

**Long-Term Vision:**
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

## User Journeys

### Journey 1: Kohl - From Scrambling to Confident Lesson Planning

**The Problem:**
It's Tuesday evening, and Kohl has a lesson with a 14U goalie tomorrow who's struggling with butterfly recovery. He opens Instagram, scrolls through his saved posts looking for that perfect drill he saw last week. Five minutes pass. Ten minutes. The drill is buried somewhere in a collection mixed with personal posts, memes, and other hockey content. He tries searching "butterfly recovery" but gets results for actual butterflies, recovery drinks, and unrelated hockey content. Frustrated, he gives up and decides to just reuse the same drill he used last session. Again.

**Discovery & Capture:**
Two weeks earlier, Kohl was scrolling TikTok during his lunch break and saw an excellent butterfly recovery drill from a coach he respects. Instead of just saving it to TikTok's collection (where it would disappear), he copied the URL and pasted it into his Discord bot. The bot asked him a few quick questions: "What does this drill work on?" He typed: "butterfly recovery, getting back up quickly, post integration." The bot confirmed: "Saved! I'll analyze it and suggest similar drills when you need them." The whole process took 30 seconds.

**The Turning Point:**
Now it's Tuesday evening again, but this time Kohl opens his drill library web app. He types in the semantic search: "drills for getting back up quickly after butterfly." Within seconds, he sees 8 relevant results—not based on exact keyword matching, but contextual understanding. The drill from TikTok is there, along with variations he had forgotten about. He clicks on the TikTok drill. The detail view shows the auto-generated tags the LLM added: "explosive movement," "core engagement," "butterfly mechanics"—tags he wouldn't have thought to add himself, but that make perfect sense.

Below the drill details, he sees "Similar Drills" recommendations. One catches his eye—a YouTube drill that approaches butterfly recovery from a different angle, focusing on hand positioning during the push. This gives him an idea: he can build a progression, starting with the TikTok drill for the basic movement, then advancing to the YouTube drill for refinement.

**The New Reality:**
Fifteen minutes later, Kohl has a complete lesson plan with 3 drills that build on each other, each targeting butterfly recovery from a different angle. He's confident these are the right drills—not because they're the only ones he could remember, but because he evaluated several options and chose strategically. When his session starts tomorrow, he'll have variety, progression, and purpose. Most importantly, he spent those 15 minutes on creative lesson design, not hunting through scattered collections.

Three months later, Kohl has 62 drills in his library. He uses the tool for every lesson plan, and his planning sessions consistently take 20-25 minutes instead of 45-60. His goalies are progressing faster because he's matching drills more precisely to their development needs. And when he's tired of using the same warm-up, he filters by "warmup + beginner + butterfly" and discovers drills he saved months ago that are perfect for the moment.

**Journey Requirements Revealed:**
- Semantic search capability across drill descriptions and tags
- LLM auto-tagging that enhances user-provided tags
- Similar drill recommendations based on content similarity
- Filtering by tags, difficulty, and age group
- Drill detail view with full metadata
- Library grid with visual drill cards
- Integration with Discord bot capture workflow

### Journey 2: Sarah Chen - Evaluating a Real AI Engineer

**The Screening:**
Sarah Chen opens her email to find another batch of AI engineer applications. She's seen 47 candidates this quarter, and most portfolios look identical: a chatbot, a sentiment analyzer, maybe a RAG implementation following a tutorial. She clicks on Kohl's application. Under "Portfolio Projects," she sees: "Coaching-content-library - AI-powered content management solving retrieval problems in goalie coaching." Intrigued by the specificity, she clicks the link.

**First Impression:**
The live app loads immediately—no "please run npm install" instructions, no broken deployment. A clean hockey-themed interface appears with a library of drill cards. She notices the search bar: "Try semantic search: 'drills for lateral movement'" it suggests. She types "getting back to feet quickly" and watches results appear. The drills shown are clearly about recovery movements, even though none of the titles contain her exact words. "Okay," she thinks, "semantic search actually works."

She clicks on a drill. The detail page shows auto-generated tags alongside user-provided ones, similar drill recommendations, and filtering options. She tests the recommendations—they make sense. She tries the filters—they work smoothly. Three minutes into exploring, she's already thinking: "This person can ship working features."

**The Technical Deep Dive:**
Sarah schedules a technical interview. During the video call, she shares her screen showing Kohl's deployed app. "Walk me through your architecture decisions," she asks. Kohl explains: "I use vector embeddings for semantic search because keyword matching failed catastrophically for position-specific coaching terms. The LLM auto-tagging augments my manual tags rather than replacing them because I know which drills instill bad habits—the AI doesn't. Similar drill recommendations combine tag similarity with semantic similarity of descriptions because tags alone miss nuance."

She probes deeper: "Why Discord bot instead of browser extension?" Kohl responds: "Lower friction to ship, fits my actual workflow, and I use Discord daily anyway. The bot was quickest path to proving the capture workflow worked before building the full UI."

Sarah opens the GitHub repo. The code is clean—proper TypeScript types, TanStack Query for server state, clear component boundaries. The backend uses FastAPI with proper Pydantic models, error handling, and a repository pattern. The README shows the critical field names (`drill_tags`, `drill_description`) are documented. She sees test files with meaningful coverage. This isn't prototype code; it's production-ready architecture.

**The Decision:**
Sarah reviews her mental checklist:
- ✅ Real problem the builder actually experiences (not manufactured)
- ✅ Appropriate AI technique selection (semantic search for retrieval, LLM for tagging, not hype-chasing)
- ✅ Clean, maintainable architecture (could onboard a team member to extend this)
- ✅ Complete MVP showing follow-through (not 30% done across 10 features)
- ✅ Thoughtful trade-offs (Discord bot over browser extension—pragmatic choice)
- ✅ Evidence this will actually be used (solving personal coaching problem)

She messages the hiring manager: "Move Kohl to final round. This is exactly the kind of practical AI engineering we need—someone who can identify real problems, architect appropriate solutions, and ship complete features. The fact that it's solving his own coaching problem shows he understands how to build user-centered AI products, not just follow LLM tutorials."

**The Outcome:**
Two weeks later, Kohl receives an offer. During the negotiation call, the CTO mentions: "Your drill library project stood out because it showed you understand the difference between 'using AI' and 'solving problems with AI.' That's what we're looking for."

**Journey Requirements Revealed:**
- Live deployment with public URL (no setup required)
- Professional UI polish (hockey-themed, responsive)
- Working AI features demonstrable in minutes (semantic search, auto-tagging, recommendations)
- Clean codebase architecture (TypeScript + Python, proper patterns)
- Complete feature set (not half-implemented)
- Documentation of critical technical decisions (field names, backend contract)

### Journey Requirements Summary

The two user journeys reveal distinct but complementary capability areas:

**Kohl's Journey (Primary User - Coaching Workflow):**
1. **Content Discovery & Capture** - Discord bot integration for URL submission with guided metadata collection
2. **Intelligent Search** - Semantic search understanding coaching context, not just keywords
3. **AI-Enhanced Organization** - LLM auto-tagging that augments user knowledge, similar drill recommendations
4. **Efficient Filtering** - Combinable filters (tags, difficulty, age group) for precise drill discovery
5. **Rich Drill Details** - Full metadata view with tags, descriptions, similar drills
6. **Visual Library Interface** - Grid of drill cards with thumbnails, responsive design

**Sarah's Journey (Secondary User - Portfolio Evaluation):**
1. **Production Deployment** - Live, accessible URL with no setup friction
2. **Professional UI** - Hockey-themed design, responsive layout, smooth UX
3. **Demonstrable AI Features** - Working semantic search, auto-tagging, recommendations within minutes of exploration
4. **Code Quality Signals** - Clean architecture visible in public repo, proper TypeScript/Python patterns
5. **Technical Documentation** - Clear README, documented critical decisions (field names, backend contract)
6. **Complete Feature Set** - All three core AI capabilities functional and integrated

**Cross-Cutting Requirements:**
- **Data Model:** `drill_tags` (array), `drill_description` (string), `difficulty`, `age_group`, `equipment`
- **Backend Contract:** PascalCase enums (`'YouTube'`), snake_case fields (`drill_tags`, `drill_description`)
- **Technology Stack:** React + TypeScript frontend, FastAPI + Python backend, vector embeddings, LLM APIs
- **Integration:** Discord bot → database → web UI workflow
- **Performance:** Fast semantic search, real-time filtering, responsive UI across devices

## Innovation & Novel Patterns

### Detected Innovation Areas

**Domain-Specific Innovation in Goalie Coaching:**
While the MVP leverages proven AI techniques (vector embeddings, LLM tagging, semantic search), the broader vision for Coaching-content-library introduces capabilities that don't currently exist in the hockey goalie coaching domain.

**Innovation in MVP (Solid Execution):**
The MVP represents thoughtful application of established AI technologies to solve a real coaching problem:
- **Semantic search** for position-specific coaching content (proven technology, novel application)
- **LLM-powered auto-tagging** augmenting coach expertise (established technique, coaching-specific context)
- **Recommendation engine** based on content similarity (proven approach, goalie drill focus)

**Breakthrough Innovation in Post-MVP:**

**1. Natural Language Lesson Planning (Phase 2)**
No existing hockey coaching platform offers chat-based lesson planning that understands position-specific nuances and suggests multi-drill progressions. The vision: "Show me drills for building a lesson on butterfly mechanics for intermediate goalies" → receives curated drill sequence with progression logic.

**Innovation:** Combining agentic AI workflows with coach-curated knowledge to generate contextually appropriate lesson plans. Goes beyond simple search to orchestrate complex lesson design.

**2. Individualized Coaching Intelligence (Phase 5)**
Personalized tracking of each goalie's development journey with AI-powered progress monitoring and skill gap analysis doesn't exist in the goalie coaching space.

**Innovation:** Per-athlete AI recommendations that understand:
- Individual goalie's current skill level and development trajectory
- Which drills they've already worked on and how they responded
- Skill gaps and optimal next steps for progression
- Multi-goalie session optimization for group training

**3. Goalie-Specific AI Understanding**
Training AI models to understand the nuances of goalie coaching (butterfly recovery vs. lateral tracking vs. post integration, age-appropriate progression, skill interdependencies) at a level that informs intelligent recommendations.

**Innovation:** Domain-specific AI that understands position coaching context, not generic sports training.

### Market Context & Competitive Landscape

**Existing Solutions in Coaching:**
- **Social Media Platforms (TikTok, Instagram, YouTube):** Excel at content discovery, fail catastrophically at retrieval
- **Generic Productivity Tools (Notion, Pocket):** Require manual organization, no video understanding, no coaching intelligence
- **Coaching Platforms (TeamSnap, CoachNow):** Focus on team management and communication, not AI-enhanced content organization and lesson planning
- **Generic AI (ChatGPT):** Doesn't know which drills the coach trusts, lacks persistent curated library, no personalized coaching per goalie

**Gap in Market:**
No solution combines coach-curated content library + AI-enhanced organization + position-specific understanding + personalized athlete tracking. Existing coaching tools focus on scheduling and communication; existing AI tools lack coach-specific knowledge and persistent libraries.

**Why This Innovation Matters:**
Goalie coaching is highly specialized (different from player coaching), and coaches build personal drill libraries through years of experience. Existing solutions treat all coaching content generically. This project creates AI that understands the position-specific nuances and learns from the coach's curation decisions.

### Validation Approach

**MVP Validation (Proven Techniques):**
- **Semantic search quality:** Subjective assessment - "Are results contextually appropriate?"
- **Auto-tagging accuracy:** Subjective validation - "Do added tags make sense?"
- **Recommendation relevance:** "Do similar drills feel genuinely related?"
- **User adoption:** 50 drills in 90 days, planning time reduced to 15-30 minutes

**Post-MVP Innovation Validation:**

**Phase 2 (Chat Interface) Validation:**
- **Lesson plan quality:** Coach subjectively evaluates suggested drill sequences - "Does this progression make sense?"
- **Context understanding:** AI grasps intent from natural language queries about specific skills and levels
- **Usage preference:** Coach chooses chat interface over manual search for lesson planning

**Phase 5 (Individualized Coaching) Validation:**
- **Progress tracking accuracy:** AI correctly identifies skill gaps and development trajectory
- **Recommendation effectiveness:** Suggested drills lead to measurable goalie improvement
- **Goalie outcomes:** Observable performance improvements in practices and games

**Validation Philosophy:**
Start with proven AI techniques in MVP to validate core retrieval problem is solved. Layer innovative features (chat, personalization) only after demonstrating users trust and adopt the base system.

### Risk Mitigation

**MVP Risks (Low - Proven Techniques):**
- **Risk:** Semantic search doesn't understand coaching context well enough
- **Mitigation:** Start with text-based search, refine embeddings based on usage patterns, add video transcription in Phase 3 if needed

- **Risk:** LLM auto-tagging adds irrelevant tags
- **Mitigation:** Tags augment (never replace) user tags, easy tag removal, continuous refinement based on which tags users keep vs. delete

**Post-MVP Innovation Risks (Higher - Novel Features):**

**Chat Interface (Phase 2) Risks:**
- **Risk:** Agentic workflow generates poor lesson suggestions, coach loses trust
- **Mitigation:** Start with simple chat queries, show drill sources clearly, allow manual override of suggestions, track which suggestions coaches actually use

**Individualized Coaching (Phase 5) Risks:**
- **Risk:** AI incorrectly assesses goalie skill level or progress
- **Mitigation:** Coach maintains final authority on all assessments, AI provides suggestions not mandates, transparent reasoning for recommendations

**Domain Understanding Risks:**
- **Risk:** AI doesn't grasp position-specific nuances (e.g., confuses butterfly recovery with general recovery)
- **Mitigation:** Leverage coach-curated tags and descriptions to train/refine understanding, start conservative with proven techniques before layering complex understanding

**Fallback Strategy:**
If innovative post-MVP features don't meet quality bar, MVP still provides substantial value solving the core retrieval problem. Innovation is additive, not foundational to product value.

## Web App Specific Requirements

### Project-Type Overview

Coaching-content-library is a web application providing browser-based access to an AI-enhanced goalie drill library. The architecture prioritizes development speed and simplicity, with a React-based frontend connecting to a FastAPI backend and SQLite database.

### Technical Architecture Considerations

**Frontend Architecture:**
- **Current Implementation:** React 19.2.0 + TypeScript 5.9.3 single-page application (SPA)
- **Flexibility:** Architecture may evolve to multi-page application (MPA) or hybrid approach based on pragmatic implementation needs
- **Build Tool:** Vite 7.2.4 for fast development and optimized production builds
- **State Management:** TanStack Query 5.90.16 for server state, React hooks for UI state
- **Routing:** React Router DOM 7.11.0
- **Styling:** Tailwind CSS 4.1.18 with custom hockey-themed design system

**Backend Architecture:**
- **Framework:** FastAPI 0.104.0+ (Python 3.12)
- **Database:** SQLite for main data storage (drill metadata, tags, descriptions, user data)
- **Vector Storage:** Dedicated vector database for embeddings (ChromaDB or FAISS) for semantic search
- **API Design:** RESTful endpoints with Pydantic models for request/response validation
- **Integration:** Discord bot → SQLite → FastAPI → React web UI workflow

**Database Strategy:**
- **Primary Database:** SQLite
  - Single-user personal tool (no multi-user concurrency concerns)
  - Simple deployment (single file database)
  - Fast performance for expected dataset size (hundreds of drills)
  - Easy backup and portability
- **Vector Database:** Separate vector store for embeddings
  - ChromaDB (preferred - can use SQLite backend) or FAISS
  - Handles semantic similarity search for drill descriptions and tags
  - Stores drill embeddings for recommendation engine
- **Future Consideration:** Re-evaluate if scaling beyond personal use or encountering performance bottlenecks

### Browser Support & Compatibility

**Target Browsers:**
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

**Compatibility Approach:**
- Modern evergreen browsers only - no legacy browser support
- ES6+ JavaScript features without polyfills
- CSS Grid and Flexbox for layouts
- Native fetch API for HTTP requests

**Not Supported:**
- Internet Explorer
- Legacy browser versions (> 2 years old)

### Responsive Design Requirements

**Breakpoints:**
- **Mobile:** < 768px (single column drill grid)
- **Tablet:** 768px - 1024px (2-column drill grid)
- **Desktop:** > 1024px (3-4 column drill grid)

**Layout Approach:**
- Mobile-first responsive design
- Tailwind CSS responsive utilities
- Flexible grid layouts that adapt to screen size
- Touch-friendly interface elements on mobile/tablet

**Key Views:**
- Library grid with drill cards (responsive columns)
- Drill detail sheet/modal (full-screen on mobile, drawer on desktop)
- Search and filter interface (collapsible on mobile)
- Hockey-themed color palette: deep blue (#1e3a5f), ice blue (#38bdf8)

### Performance Targets

**Performance Philosophy:**
"Fast enough for personal use" - prioritize development speed over micro-optimizations.

**Acceptable Performance Targets:**
- **Initial page load:** < 3 seconds on broadband
- **Semantic search response:** < 2 seconds for typical queries
- **Filter application:** < 500ms (real-time feel)
- **Drill detail view:** Instant (client-side navigation)
- **Image/thumbnail loading:** Progressive with lazy loading

**Optimization Strategy:**
- Start simple, optimize if performance becomes noticeable issue
- Lazy load images/thumbnails
- Cache API responses with TanStack Query
- Code splitting for route-based chunks (Vite default)

### SEO & Discoverability

**SEO Requirements:**
- Not needed - this is a personal tool and portfolio piece
- Drill library content does not need to be discoverable via search engines
- Portfolio showcase: README and project description provide context for employers

**Implications:**
- No server-side rendering (SSR) required
- No sitemap or robots.txt needed
- No meta tags for social sharing (unless desired for portfolio presentation)
- Client-side routing acceptable (no SEO penalty concerns)

### Real-Time Features

**Real-Time Requirements:**
- Not needed for MVP
- Discord bot saves → database → visible on next page load/refresh acceptable
- No WebSockets, Server-Sent Events, or polling required

**Future Consideration:**
If real-time updates become desirable (e.g., seeing drill appear immediately after Discord bot save), can add lightweight polling or WebSocket connection in post-MVP.

### Accessibility Requirements

**WCAG Compliance:**
- No formal WCAG compliance required for MVP
- Personal tool, not public-facing product

**Basic Accessibility:**
- Semantic HTML elements where natural
- Keyboard navigation for interactive elements
- Sufficient color contrast for readability (hockey theme already uses dark blue + light blue)
- Alt text on images where present

**Accessibility Philosophy:**
Build with reasonable accessibility practices by default (semantic HTML, keyboard support), but formal WCAG audit/compliance not in scope.

### Implementation Considerations

**Development Priorities:**
1. **Speed to MVP:** Choose pragmatic solutions over perfect architecture
2. **Simplicity:** SQLite over Postgres, React SPA over complex SSR, straightforward deployment
3. **Portfolio Quality:** Clean code, good architecture, demonstrable features over micro-optimizations
4. **Personal Use First:** Optimize for single-user experience, not enterprise scale

**Deployment Requirements:**
- Static frontend hosting (Vercel, Netlify, or similar)
- Backend hosting with SQLite support (Railway, Fly.io, or similar)
- Public URL for portfolio presentation
- Simple deployment process (not complex Kubernetes/Docker orchestration)

**Technology Stack Summary:**
- **Frontend:** React 19.2.0, TypeScript 5.9.3, Vite 7.2.4, TanStack Query 5.90.16, Tailwind CSS 4.1.18
- **Backend:** FastAPI 0.104.0+, Python 3.12, Pydantic 2.0+, SQLAlchemy 2.0+
- **Database:** SQLite (main data), ChromaDB or FAISS (vector embeddings)
- **Integration:** Discord bot (discord.py 2.3.0+)
- **AI:** Vector embeddings, LLM APIs for auto-tagging

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP

The MVP is designed to solve a specific, well-defined problem: coaches can't find saved drill content when they actually need it. Success means reducing lesson planning time from 30-60 minutes to 15-30 minutes by enabling fast, contextual retrieval of curated drills.

**Timeline:** 1-2 months with full-time focus

**Resource:** Solo developer (Kohl)

**Strategic Rationale:**

1. **Discord Bot Already Complete** - The content capture workflow is working and deployed, providing a significant head start and de-risking the timeline.

2. **Proven AI Techniques** - MVP leverages established technologies (vector embeddings for semantic search, LLM APIs for tagging, similarity algorithms for recommendations) rather than experimental approaches. This reduces technical risk while still demonstrating sophisticated AI integration.

3. **Clear Value Proposition** - Solves a personal pain point the developer experiences multiple times per week. Immediate validation: "Does this make my coaching easier?"

4. **Portfolio-Ready** - Demonstrates practical AI engineering capabilities to employers: semantic search, LLM integration, recommendation systems, clean architecture, complete feature set.

5. **Foundation for Innovation** - MVP proves the core retrieval problem can be solved before layering more innovative features (chat interface, individualized coaching) in post-MVP phases.

**Success Criteria:**
- All three AI features functional and demonstrable in live deployment
- Planning time measurably reduced (subjective validation: "This is faster than hunting through Instagram")
- 50 drills saved within first 90 days (proving capture workflow integrates seamlessly)
- Code quality demonstrates best practices for portfolio presentation

### MVP Feature Set (Phase 1)

**Must-Have Capabilities:**

**1. Content Capture & Storage** ✅ (Already Complete)
- Discord bot integration for drill URL submission
- Guided metadata collection during capture: `drill_tags`, `drill_description`, `difficulty`, `age_group`, `equipment`
- Support for YouTube, TikTok, Instagram, Reddit sources
- URL storage with automatic metadata extraction where available
- SQLite database storage

**2. LLM-Powered Auto-Tagging**
- Automatic tag enhancement that augments (never replaces) user-provided `drill_tags`
- Triggers on save with rate limiting (max: 1 per 5 minutes to manage API costs)
- Analyzes drill description and available content metadata to suggest relevant tags
- Tags added without removing user-provided tags (augmentation model)
- Quality threshold: subjectively validated by user as "relevant and useful"
- Easy tag removal if auto-generated tags aren't helpful

**3. Semantic Search**
- Text-based semantic search (no video content analysis in MVP)
- Searches across `drill_description` and `drill_tags` fields
- Returns contextually relevant drills based on meaning, not just keyword matching
- Example: "butterfly recovery" finds relevant drills regardless of exact wording
- Quality threshold: results feel contextually appropriate to search intent
- Search bar in web UI with real-time results

**4. Similar Drill Recommendations**
- Recommendation engine based on two complementary factors:
  - Tag similarity (shared tags between drills)
  - Semantic similarity of drill descriptions (vector embeddings)
- Shown in drill detail view ("Drills Like This")
- Quality threshold: "interesting suggestions" that feel genuinely related
- Exposes drill variety the coach might not have thought to search for

**5. Advanced Filtering**
- Filter library by multiple criteria:
  - Tags (including special "group drill" tag)
  - Difficulty level (beginner, intermediate, advanced)
  - Age group (mite, squirt, peewee, bantam, midget, junior, adult)
  - Equipment requirements
- Combinable filters for precise drill discovery
- Real-time filter application with responsive UI
- Filter state preserved during session

**6. Group Drill Support**
- Special "group drill" tag to identify drills suitable for 3-4 goalie sessions
- Filterable to quickly find group-specific content
- Addresses specific coaching challenge: keeping multiple goalies engaged simultaneously
- Critical for Kohl's regular 3-4 goalie group sessions

**7. Professional Web UI**
- Clean, hockey-themed design system
  - Primary: deep blue (#1e3a5f)
  - Accent: ice blue (#38bdf8)
  - Source-specific colors (YouTube: red, TikTok: cyan, Instagram: pink, Reddit: orange)
  - Difficulty badges (beginner: green, intermediate: amber, advanced: red)
- Responsive layout (mobile, tablet, desktop)
- Key views:
  - Library grid with drill cards (thumbnail, title, tags, difficulty)
  - Drill detail sheet/modal (full metadata, similar drills, edit/delete)
  - Search and filter interface (collapsible on mobile)
  - Add drill modal (if adding via web UI instead of Discord)
- Portfolio-ready polish for employer presentation
- Modern React 19.2.0 + TypeScript 5.9.3 + Tailwind CSS 4.1.18 implementation

**Explicitly Out of MVP Scope:**

The following features are deferred to post-MVP phases to maintain aggressive 1-2 month timeline:
- Chat interface for natural language lesson planning
- Individual goalie tracking and progress monitoring
- Practice plan creation, saving, and export
- Video transcription integration (Whisper API)
- Semantic clustering of drill library
- Visual/video content analysis
- Multi-user support or sharing features
- Mobile app (web app responsive design only)

**MVP Success Criteria:**
- ✅ Discord bot → database → web UI workflow functioning reliably
- ✅ Semantic search returns contextually relevant results (subjective: "This understands what I meant")
- ✅ Auto-tagging adds genuinely useful tags (subjective: coach keeps most auto-generated tags)
- ✅ Similar drill recommendations feel related and expose drill variety
- ✅ Filtering system enables precise drill discovery across tags, difficulty, age group
- ✅ Clean, responsive UI with professional polish
- ✅ Live deployment with public URL
- ✅ Code quality demonstrates software engineering best practices
- ✅ Planning time reduced to 15-30 minutes (from 30-60 minutes)
- ✅ 50 drills saved within 90 days (proving capture workflow adoption)

### Post-MVP Features

**Phase 2: Intelligent Lesson Planning** (2-3 months after MVP)

**Chat Interface for Natural Language Queries:**
- Natural language drill queries: "Show me drills for building a lesson on butterfly mechanics for intermediate goalies"
- Multi-drill suggestions organized by lesson progression (warmup → main → game situation)
- Agentic workflow demonstrating complex AI orchestration
- Query understanding: skill focus, difficulty level, lesson structure, drill variety

**Benefits:**
- Faster lesson planning through conversational interface
- Exposes drill combinations coach wouldn't have thought to search
- Demonstrates advanced AI engineering (agentic workflows, complex query handling)

**Innovation:** This doesn't exist in hockey coaching platforms. Combining coach-curated knowledge with agentic AI to generate contextually appropriate lesson plans is novel in the domain.

---

**Phase 3: Enhanced Content Understanding** (3-4 months after MVP)

**Video Transcription Integration:**
- Whisper API integration for automatic video transcription
- Richer semantic search incorporating spoken content from drill videos
- Automatic drill description generation from video transcripts
- Improved auto-tagging accuracy with full video content context

**Benefits:**
- Search finds drills based on what's said in the video, not just titles/descriptions
- Reduced manual metadata entry (auto-generated descriptions)
- Better semantic understanding of drill content

**Note:** Deferred from MVP to reduce complexity and timeline. Text-based search proves the concept; video transcription enhances it.

---

**Phase 4: Smart Organization** (4-5 months after MVP)

**Semantic Clustering:**
- Automatically group related drills into clusters
- Visual drill library with clustered organization
- Discovery of drill patterns and progressions coach hadn't explicitly organized
- "Drills like this" expanded to cluster-based navigation

**Benefits:**
- Surfaces implicit structure in drill library
- Discover drill progressions (beginner → intermediate → advanced versions of same skill)
- Portfolio showcase: demonstrates unsupervised learning and clustering algorithms

---

**Phase 5: Personalized Coaching** (5-6 months after MVP)

**Individual Goalie Tracking:**
- Per-athlete profiles with skill level, development goals, session history
- Track which drills each goalie has worked on and how they responded
- Skill gap analysis and suggested focus areas per athlete
- Personalized lesson planning: "Show me drills for John Doe's next session based on his progress"

**Multi-Goalie Session Optimization:**
- Suggest drills that work for group sessions with goalies at different skill levels
- Optimize drill selection to keep all goalies engaged

**Benefits:**
- Transforms tool from content library to comprehensive coaching assistant
- Longitudinal tracking of goalie development
- Demonstrates complex personalization and multi-agent optimization

**Innovation:** Individualized goalie coaching intelligence doesn't exist in current coaching platforms. Most tools focus on team management, not individual athlete development with AI-powered recommendations.

---

**Phase 6: Complete Lesson Builder** (Future - 1-2 years)

**Practice Plan Creation:**
- Full lesson plan builder with drill sequencing
- Drag-and-drop drill ordering for lesson progression
- Plan templates for common lesson types (butterfly mechanics, lateral movement, etc.)
- Export to PDF, docs, or coaching platforms
- Session notes and post-lesson feedback capture

**Benefits:**
- End-to-end lesson planning workflow
- Shareable lesson plans with other coaches
- Complete coaching productivity suite

### Risk Mitigation Strategy

**Technical Risks:**

**1. Semantic Search Quality**
- **Risk:** Vector embeddings don't understand coaching context well enough; search results feel generic or miss nuance
- **Likelihood:** Low-Medium (proven technology, but domain-specific application)
- **Impact:** High (core value proposition)
- **Mitigation:**
  - Start with text-based semantic search using proven embedding models (OpenAI, Sentence Transformers)
  - Validate search quality subjectively during development: "Does this understand what I meant?"
  - Refine embeddings based on usage patterns and feedback
  - Phase 3 adds video transcription if text-only search proves insufficient
  - Fallback: Tag-based search still provides value even if semantic search underperforms

**2. LLM Auto-Tagging Accuracy**
- **Risk:** Auto-generated tags are irrelevant, confusing, or detract from user-provided tags
- **Likelihood:** Low (LLMs excel at content analysis and tagging)
- **Impact:** Medium (nice-to-have feature, not critical)
- **Mitigation:**
  - Tags augment (never replace) user-provided tags
  - Easy tag removal if auto-generated tags aren't useful
  - Rate limiting (1 per 5 minutes) manages API costs during experimentation
  - Continuous refinement based on which tags users keep vs. delete
  - Fallback: Disable auto-tagging if quality doesn't meet threshold; manual tags still work

**3. Vector Database Integration**
- **Risk:** ChromaDB or FAISS integration proves complex or unstable
- **Likelihood:** Low (mature libraries with good documentation)
- **Impact:** Medium (blocks semantic search and recommendations)
- **Mitigation:**
  - Start with ChromaDB (simpler, can use SQLite backend)
  - FAISS as fallback if ChromaDB has issues
  - Decouple vector operations from main database (can develop incrementally)
  - Extensive testing before deployment

**Market Risks:**

**1. Portfolio Value**
- **Risk:** Employers don't find project compelling or representative of AI engineering skills
- **Likelihood:** Very Low (project demonstrates practical AI integration solving real problem)
- **Impact:** High (primary business goal)
- **Mitigation:**
  - Focus on demonstrable features: semantic search, auto-tagging, recommendations all visible in minutes
  - Clean codebase with clear architecture (TypeScript + Python best practices)
  - Live deployment with public URL (no setup friction for employers)
  - Technical documentation explaining architecture decisions
  - README highlights: problem solved, AI techniques used, tech stack

**2. Adoption (Personal Use)**
- **Risk:** Tool doesn't integrate into actual coaching workflow; planning time doesn't improve
- **Likelihood:** Low (solving personal pain point, Discord bot already in use)
- **Impact:** Medium (reduces credibility of "real problem" narrative)
- **Mitigation:**
  - Capture workflow already proven (Discord bot in active use)
  - Iterative development: build feature → test in real lesson planning → refine
  - Success metrics clear: 15-30 min planning time, 50 drills in 90 days
  - Fallback: Even if personal adoption wavers, still demonstrates technical AI capabilities for portfolio

**Resource Risks:**

**1. Timeline Pressure**
- **Risk:** 1-2 months proves too aggressive; features incomplete or quality suffers
- **Likelihood:** Low-Medium (solo developer, full-time focus, Discord bot already complete)
- **Impact:** High (delays portfolio presentation, job applications)
- **Mitigation:**
  - MVP scope tightly defined with explicit out-of-scope features
  - Discord bot completion provides head start
  - Proven technologies reduce experimentation time
  - Clear success criteria prevent scope creep
  - Fallback: Extend timeline slightly if needed; prioritize working features over perfect polish

**2. Quality vs. Speed Trade-off**
- **Risk:** Rushing to meet timeline results in poor code quality, bugs, or incomplete features
- **Likelihood:** Medium (inherent tension in aggressive timeline)
- **Impact:** High (code quality critical for portfolio evaluation)
- **Mitigation:**
  - Use established patterns and libraries (React + TanStack Query, FastAPI patterns)
  - Focus on clean architecture from start (easier to maintain velocity)
  - Incremental testing: validate each AI feature before moving to next
  - Definition of "done" includes code cleanup, not just "feature works"

**3. Deployment Complexity**
- **Risk:** Deployment proves more complex than expected; live URL delayed
- **Likelihood:** Low (straightforward static frontend + backend with SQLite)
- **Impact:** Medium (delays portfolio presentation)
- **Mitigation:**
  - Choose simple deployment: Vercel/Netlify (frontend), Railway/Fly.io (backend)
  - Test deployment early in development cycle
  - SQLite simplifies backend deployment (no separate database service)
  - Fallback: Local demo if deployment blocked, but prioritize fixing deployment issues

**Overall Risk Assessment:**

**Low Risk:** MVP leverages proven AI techniques (embeddings, LLM APIs, similarity algorithms) applied to well-defined problem with clear success criteria. Discord bot completion de-risks timeline significantly.

**Highest Risks:** Timeline pressure and quality trade-offs. Mitigate by tightly scoping MVP, using established technologies, and maintaining clear definition of "done" including code quality.

**Post-MVP Innovation Risks:** Higher for Phases 2-5 (chat interface, individualized coaching) because these introduce novel capabilities. MVP success validates core retrieval problem is solved before layering innovation.

## Functional Requirements

### Content Capture & Ingestion

- **FR1:** Coaches can submit drill URLs via Discord bot for automatic capture
- **FR2:** System can ingest content from YouTube, TikTok, Instagram, and Reddit sources
- **FR3:** System can extract available metadata from URL sources (title, author, thumbnail, view counts)
- **FR4:** Coaches can provide drill description during capture via Discord bot
- **FR5:** Coaches can specify drill tags during capture via Discord bot
- **FR6:** Coaches can specify difficulty level during capture (beginner, intermediate, advanced)
- **FR7:** Coaches can specify age group during capture (mite, squirt, peewee, bantam, midget, junior, adult)
- **FR8:** Coaches can specify equipment requirements during capture
- **FR9:** System can store captured drills with all metadata in persistent storage

### Content Management

- **FR10:** Coaches can view full drill details including all metadata
- **FR11:** Coaches can edit drill metadata after capture (description, tags, difficulty, age group, equipment)
- **FR12:** Coaches can delete drills from their library
- **FR13:** Coaches can add tags to existing drills
- **FR14:** Coaches can remove tags from existing drills
- **FR15:** System can track when each drill was captured (saved_at timestamp)

### Content Discovery & Search

- **FR16:** Coaches can search drill library using natural language queries
- **FR17:** System can perform semantic search across drill descriptions and tags
- **FR18:** System can return contextually relevant search results based on query meaning (not just keyword matching)
- **FR19:** Coaches can filter drill library by tags
- **FR20:** Coaches can filter drill library by difficulty level
- **FR21:** Coaches can filter drill library by age group
- **FR22:** Coaches can filter drill library by equipment requirements
- **FR23:** Coaches can combine multiple filters simultaneously
- **FR24:** Coaches can identify group drills using special "group drill" tag filter
- **FR25:** System can apply filters in real-time with responsive feedback

### AI-Enhanced Organization

- **FR26:** System can analyze drill content and automatically suggest relevant tags
- **FR27:** System can augment user-provided tags with AI-generated tags (never replacing user tags)
- **FR28:** System can trigger auto-tagging on drill save with rate limiting (max 1 per 5 minutes)
- **FR29:** Coaches can review and accept/reject auto-generated tags
- **FR30:** System can calculate similarity between drills based on tag overlap
- **FR31:** System can calculate semantic similarity between drills based on description embeddings
- **FR32:** System can recommend similar drills when viewing drill details
- **FR33:** System can combine tag similarity and semantic similarity for recommendations

### Content Viewing & Browsing

- **FR34:** Coaches can view drill library as a grid of drill cards
- **FR35:** System can display drill thumbnails in library grid
- **FR36:** System can display drill title, author, source, and key metadata on drill cards
- **FR37:** Coaches can navigate to original drill URL
- **FR38:** Coaches can view drill details in expandable sheet/modal interface
- **FR39:** System can display all drill metadata in detail view (title, author, source, description, tags, difficulty, age group, equipment, statistics)
- **FR40:** System can display similar drill recommendations in drill detail view
- **FR41:** Coaches can access the library on mobile, tablet, and desktop devices with responsive layout

### Metadata Management

- **FR42:** System can store drill descriptions as free text
- **FR43:** System can store drill tags as an array of strings
- **FR44:** System can store difficulty level as enumerated value (beginner, intermediate, advanced)
- **FR45:** System can store age group as enumerated value (mite, squirt, peewee, bantam, midget, junior, adult)
- **FR46:** System can store equipment requirements as free text
- **FR47:** System can store source platform as enumerated value (YouTube, TikTok, Instagram, Reddit)
- **FR48:** System can store drill statistics from source platform (view count, like count, comment count)
- **FR49:** System can track when each drill was published on source platform (published_at)
- **FR50:** System can track when each drill was fetched into the system (fetched_at)

## Non-Functional Requirements

### Performance

**Target Philosophy:** "Fast enough for personal use" - prioritize development speed over micro-optimizations while ensuring responsive user experience.

**Performance Targets:**

- **NFR1:** Initial page load completes within 3 seconds on broadband connection
- **NFR2:** Semantic search returns results within 2 seconds for typical queries
- **NFR3:** Filter application completes within 500ms (real-time feel)
- **NFR4:** Drill detail view opens instantly via client-side navigation
- **NFR5:** Images and thumbnails load progressively with lazy loading

**Performance Optimization Strategy:**

- Cache API responses using TanStack Query
- Code splitting for route-based chunks (Vite default)
- Lazy load images/thumbnails
- Optimize only if performance becomes noticeable issue (pragmatic approach)

**Performance Testing:**

- Subjective validation: "Does this feel responsive enough for lesson planning?"
- No formal performance testing required for MVP
- Monitor and optimize based on actual usage patterns

### Integration

**External Platform APIs:**

- **NFR6:** System can reliably integrate with YouTube API for metadata extraction
- **NFR7:** System can reliably integrate with TikTok for content ingestion (limited auto-fetch)
- **NFR8:** System can reliably integrate with Instagram for content ingestion (limited auto-fetch)
- **NFR9:** System can reliably integrate with Reddit API (PRAW) for metadata extraction
- **NFR10:** System gracefully handles API failures or rate limits from platform providers
- **NFR11:** System accepts user-provided metadata when platform auto-fetch fails (fallback for Instagram/TikTok)

**AI Service Integrations:**

- **NFR12:** System integrates with LLM API for auto-tagging with rate limiting (max 1 request per 5 minutes)
- **NFR13:** System integrates with embedding API for semantic search and similarity calculations
- **NFR14:** System handles AI API failures gracefully without blocking core functionality
- **NFR15:** System manages AI API costs through rate limiting and efficient request patterns

**Discord Bot Integration:**

- **NFR16:** System maintains reliable connection between Discord bot and backend database
- **NFR17:** Drills captured via Discord bot appear in web UI on next page load/refresh (real-time sync not required)
- **NFR18:** Discord bot → database → web UI workflow functions reliably end-to-end

**Integration Error Handling:**

- **NFR19:** All external API calls include timeout handling
- **NFR20:** Failed integrations provide clear error messages to coaches
- **NFR21:** System logs integration failures for debugging and monitoring

### Reliability

**Deployment Reliability:**

- **NFR22:** Live deployment maintains public URL accessibility for portfolio presentation
- **NFR23:** System remains available during employer demo periods (no planned downtime during job search)
- **NFR24:** Database backups prevent data loss of curated drill library

**Feature Reliability:**

- **NFR25:** All three core AI features (semantic search, auto-tagging, recommendations) function reliably and consistently
- **NFR26:** Discord bot capture workflow functions without data loss
- **NFR27:** Filtering and search operations return consistent results across sessions

**Data Integrity:**

- **NFR28:** Drill metadata is stored persistently and reliably (SQLite database integrity)
- **NFR29:** User-provided tags and descriptions are never lost or overwritten by AI operations
- **NFR30:** Backend contract integrity maintained (PascalCase enums, snake_case fields) throughout system

**Reliability Philosophy:**

- Portfolio-ready deployment that works when employers visit
- Personal use reliability: "I can trust my drill library won't disappear"
- Graceful degradation: Core functionality (browsing, filtering) works even if AI features temporarily fail

### Security

**Basic Security Requirements:**

- **NFR31:** API credentials stored securely in environment variables (never hardcoded or committed)
- **NFR32:** Backend validates all user input to prevent injection attacks
- **NFR33:** HTTPS enforced for all production traffic
- **NFR34:** No logging or exposure of API keys or sensitive credentials

**Data Protection:**

- **NFR35:** Drill library data is private to the coach (no public sharing in MVP)
- **NFR36:** Discord bot authentication prevents unauthorized access

**Security Philosophy:**

- Basic security best practices, not enterprise-grade security
- No sensitive user data, no payment processing, no compliance requirements
- Focus on protecting API credentials and preventing common vulnerabilities

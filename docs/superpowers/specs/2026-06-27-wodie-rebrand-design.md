# WODie Rebrand & Sport-Technical UI Design

**Date:** June 27, 2026
**Status:** Design Phase
**Scope:** Product name rebrand, UI/UX redesign, developer documentation

---

## 1. Executive Summary

Three coordinated improvements to WODie:

1. **Name rebrand:** Woodie → WODie (clever WOD pun, stronger brand identity)
2. **UI redesign:** Minimal → Sport-Technical (scoreboard/Whoop/Peloton energy while maintaining dark gym aesthetic)
3. **Developer documentation:** New README targeting developers and contributors

---

## 2. Name Rebrand: Woodie → WODie

### Rationale

WODie is a natural linguistic bridge between "WOD" (Workout of the Day—the CrossFit standard) and personality (the suffix "-ie"). It's:
- Immediately clear about domain (CrossFit/WODs)
- Memorable and pronounceable
- Differentiates from generic fitness apps
- Enables brand consistency across all touchpoints

### Scope of Changes

**Files to update (all references):**
- `docs/index.html` — title, header, onboarding text, manifest reference
- `docs/manifest.json` — name, short_name, app title
- `DESIGN.md` — product name references (11 occurrences)
- `CLAUDE.md` — project title and references (4 occurrences)
- All inline comments and code comments referencing brand name
- All variable names that reference brand (e.g., config object keys, localStorage keys if applicable)

**Files NOT renamed (directory structure stable):**
- `/docs`, `/data`, `/scripts` remain unchanged
- Internal file structure unchanged to minimize git history confusion

**Result:** Zero breaking changes to the app structure, pure branding update.

---

## 3. Sport-Technical UI Redesign

### Current State → Target State

| Aspect | Current | Target | Why |
|---|---|---|---|
| Color depth | 2 colors (black, red) | 4 colors (blacks, red, cyan, amber) | Data hierarchy and block differentiation |
| Spacing | Tight (16px padding baseline) | Breathing room (24px sections, card gaps) | Premium feel, easier scanning |
| Section styling | Flat borders | Color-differentiated backgrounds | Visual grouping, data hierarchy |
| Timer display | Plain monospace | Glow effect + metric badges | Scoreboard intensity |
| Week grid | Dot array | Card-based with status badges | Better information density |
| Block colors | Monochrome | Color-coded by type (strength, metcon, mobility) | Scannable workout structure |
| Animation | Minimal | Smooth transitions + feedback states | Premium interaction feel |

### Design Specifications

#### **Color Palette**

```css
/* Core */
--black-darkest: #0a0a0a;      /* Background depth */
--black-base: #000000;          /* Primary background */
--black-light: #1a1a1a;         /* Section backgrounds */
--gray-card: #262626;           /* Card/block backgrounds */
--white: #ffffff;               /* Primary text */

/* Accents */
--red: #e63946;                 /* Critical actions, metcon */
--cyan: #00d9ff;                /* Data highlights, metrics */
--amber: #ffc409;               /* Strength block, loading data */
--gray: #666666;                /* Secondary text */
--gray-light: #cccccc;          /* Tertiary text */
```

#### **Typography**

- **System font stack:** keep existing (-apple-system, Segoe UI, sans-serif)
- **Weight hierarchy:**
  - 700: Major headings, block titles
  - 600: Section heads, labels, metric headers
  - 500: UI labels, button text
  - 400: Body text, descriptions
- **Letter-spacing:** 0.5px on uppercase labels (scoreboard effect)
- **Line-height:** 1.5 for body, 1.2 for display

#### **Spacing**

- **Vertical rhythm:** 24px base unit (sections), 16px for subsections, 8px for inline spacing
- **Padding:** Cards 24px, sections 16px, inline elements 8px
- **Gaps:** 12px between buttons, 8px between list items
- **Max-width:** 600px for content (maintains readability on wide screens)

#### **Session Week Grid**

Replace dot array with small card-based grid:

```
┌──┬──┬──┬──┬──┬──┬──┐
│1 │2 │3 │4 │5 │6 │7 │  (day numbers)
│✓ │✓ │● │ │  │  │ │  (status: completed, current, skipped, rest)
└──┴──┴──┴──┴──┴──┴──┘
```

Each day card:
- 40×40px minimum
- Status icon (✓, ●, skip, rest)
- Light background (#262626) with border
- Current day: cyan border, subtle glow
- Completed: red background with icon
- Rest day: darker gray background

#### **Block Color Coding**

Each workout block gets a left border accent:

- **Static Warmup:** Gray (#666666)
- **Active Warmup:** Cyan (#00d9ff)
- **Strength:** Amber (#ffc409)
- **Metcon:** Red (#e63946)
- **Cooldown:** Cyan (#00d9ff)

Border width: 3px, height: full block height

#### **Timer Display During Active Session**

Sport-technical timer with 8-segment display numerals and play/pause/reset controls:

```
┌─────────────────────────────────┐
│  STRENGTH • Set 3/4             │  (H3 heading in cyan)
│                                 │
│        ┌─────────────┐          │
│        │   12:34     │          │  (8-segment display)
│        └─────────────┘          │
│                                 │
│  ▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░  │  (progress bar)
│                                 │
│  [ ▶️ ] [ ⏸️ ] [ 🔄 ]          │  (play, pause, reset buttons)
│                                 │
│  Back Squat 75% 1RM             │  (movement info)
│  4 reps × 180s rest             │
│                                 │
│  Next: Metcon ────►             │  (preview)
└─────────────────────────────────┘
```

**Timer Styling Details:**

- **Block title (H3):** Cyan (#00d9ff), uppercase, letter-spacing 1px
- **Timer numerals:** 8-segment display font (CSS: use `font-family: 'DSEG7Classic', monospace` or similar; provide web font)
  - Size: 96px on mobile, scale responsively
  - Color: Cyan (#00d9ff) in normal state, amber (#ffc409) in final 20 seconds, red (#e63946) in final 10 seconds
  - Glow effect: `text-shadow: 0 0 30px rgba(0, 217, 255, 0.6)` (cyan glow)
  - Blink animation in final 10s (existing, keep)

- **Buttons:** 48×48px minimum, positioned below timer
  - Play (▶️): Enabled when paused, gray background, cyan on active
  - Pause (⏸️): Enabled when running, gray background, amber on active
  - Reset (🔄): Always enabled, gray background, red on active
  - Spacing: 12px between buttons
  - Border: 1px solid #666
  - On press: darker background (#1a1a1a), immediate state change

**8-Segment Display Font:**

Add to `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
```

Or use a dedicated 7/8-segment font like DSEG7 (open source, must be self-hosted in `/assets/fonts/`).

**Interaction Model:**

- Timer starts paused when session begins
- User taps Play to start countdown/EMOM
- Tapping Pause stops the clock (can resume with Play)
- Reset clears the display to 0:00 and pauses (does not advance to next block)
- Timer auto-advances to next block on completion (no user action needed)
- During auto-advance: 500ms pause, beep sound, visual flash, then next block loads
- User can skip forward/back to any block from a block navigation menu (separate from timer controls)

#### **Session Card Structure**

Reorganize for data hierarchy:

```
Session Header
├─ Title + Meta (Week X • Day Y)
├─ Periodization Badge ("Hypertrophy Week" in small caps)
│
Equipment Section (collapsible)
├─ Grouped by category (Barbell, Dumbbells, Cardio, Mobility)
│
Workout Blocks
├─ Block 1 (left-border accent color)
│  ├─ Block Title (uppercase)
│  ├─ Duration + round info
│  └─ Movement List
├─ Block 2 (same structure)
│  ...
│
Rationale Section (collapsible)
├─ Citation badges (inline, not full prose)
│  "Glassman 2002" • "Haff & Triplett"
│
Start Session Button
```

#### **Equipment List Reorganization**

Group by category instead of flat list:

```
BARBELL
• Barbell + Plates (20kg, 15kg, 10kg)
• Collars

GYMNASTICS
• Pull-up Bar
• Rings

CONDITIONING
• Rowing Machine
• Jump Rope
```

#### **Animation & Interaction**

- **Smooth transitions:** 0.2s ease on all state changes (button presses, section toggles, timer changes)
- **Button press state:** Darker background (#1a1a1a), not opacity fade
- **Section toggle:** Height expansion animation (not just show/hide)
- **Timer block transition:** Brief (100ms) color flash + beep
- **Timer final 10s:** Red blink animation + rapid beeps (existing, keep)

#### **Responsive Behavior**

- Preserve mobile-first approach
- On small screens (<480px): stack blocks vertically, reduce timer font to 56px
- On larger screens (>768px): consider side-by-side layout for timer + content (optional, v2)

---

## 4. Developer-Focused README

### Purpose

Provide developers and contributors with:
- Quick-start instructions for local generation
- Architecture overview (knowledge base → AI → JSON → static web)
- How to extend: new programs, new hard rules, new WOD categories
- GitHub Actions setup and scheduling
- Schema reference for all JSON types
- Contribution guidelines

### Sections

1. **Quick Start**
   - Clone repo
   - Install Python + dependencies
   - Set ANTHROPIC_API_KEY
   - Run generator example
   - Output format/location

2. **Project Architecture**
   - Knowledge pyramid (sources → hard rules → AI → JSON)
   - Generation flow diagram (local vs GitHub Actions)
   - Why static-only, no backend, offline-capable
   - Data schema overview

3. **Running the Generator**
   - CLI usage: `python generate.py --type program --name back-in-shape --weeks 3`
   - All argument options (--type, --weeks, --count, --category, --output-dir)
   - Output directory structure
   - Validation output format (success/failure per session)

4. **Extending: New Programs**
   - How to add program definition to data/programs.json or similar
   - How to ensure new program respects hard-rules.json
   - How to update knowledge-base/ if new concepts needed
   - Generator re-run and validation

5. **Extending: Hard Rules**
   - Editing data/hard-rules.json
   - Structure: time caps, loading %, weekly constraints, recovery windows
   - Re-running generator to validate changes
   - Common mistakes (e.g., invalid % ranges)

6. **GitHub Actions Pipeline**
   - Workflow file location (.github/workflows/generate.yml)
   - Setting up ANTHROPIC_API_KEY as repository secret
   - Cron schedule syntax (recommend weekly)
   - Manual trigger option
   - Commit message format (automated)

7. **Data Schema Reference**
   - Full JSON schema for Program, Session, Movement, WOD types
   - Example of each
   - Required fields vs optional
   - Validation rules (e.g., session duration ≤ 60 min)

8. **Contributing**
   - Code style (Python: PEP 8, JS: existing conventions)
   - Testing changes before committing
   - Documentation updates required (schema changes → README update)
   - PR expectations

9. **Troubleshooting**
   - "Generator fails with validation error"
   - "API key not recognized"
   - "Knowledge base concept not found in output"
   - "Hard rules constraint violated"

### Tone

Technical, reference-oriented, assumes Python/JSON familiarity. Code examples throughout. Link to DESIGN.md for product context.

---

## 5. Implementation Order

1. **Rebrand (quick wins):** Update all name references across files
2. **CSS redesign:** New color palette, spacing, animations
3. **HTML structure:** Reorganize equipment list, add block color accents, update timer glow
4. **README:** Write comprehensive dev guide
5. **Testing:** Manual verification of UI on mobile + desktop, generator works end-to-end
6. **Commit:** Single logical commit per change (rebrand, CSS, README, etc.)

---

## 6. Success Criteria

- [ ] All "Woodie" references replaced with "WODie" (app is functional, branded consistently)
- [ ] UI matches sport-technical aesthetic (color-coded blocks, breathing space, scoreboard timer)
- [ ] Timer uses 8-segment display font with cyan/amber/red color shifts
- [ ] Timer has functional play/pause/reset buttons with correct state management
- [ ] H1/H2/H3 headings are cyan (#00d9ff) throughout the app
- [ ] Developer README is complete and accurate (someone could clone repo and generate a program following only the README)
- [ ] No functionality broken (timer works, program loading works, WOD mode works)
- [ ] Looks good on iPhone SE (smallest reasonable viewport) and desktop

---

## 7. Out of Scope (This Phase)

- Video demonstrations or animation sequences
- Icon redesign (use existing icons, may upgrade in v2)
- Mobile navigation redesign (tab bar stays)
- Multi-language support
- Dark/light mode toggle (v1 is dark-only)

---

## 8. Open Questions for User Review

1. **Equipment grouping:** Should we show equipment quantities (e.g., "2x 20kg dumbbells") or just names? → Recommend: just names for simplicity
2. **Periodization badges:** Should we display training phase (e.g., "Strength", "Hypertrophy", "Power") or just week/day? → Recommend: week/day only, mention in rationale
3. **Citation display:** Should rationales show full prose or inline badges with expandable details? → Recommend: keep existing prose, make section collapsible

---

# WODie — Developer Guide

AI-powered CrossFit programming app. Static PWA hosted on GitHub Pages with zero runtime API calls. This guide is for developers and contributors.

**For users:** Visit [wodie.app](https://wodie.app) to use the app.

---

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/wodie.git
cd wodie
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Run the Generator

Generate a 3-week program:

```bash
cd scripts
python generate.py --type program --name back-in-shape --weeks 3
```

Output appears in `output/` directory as JSON + markdown preview.

Generate a set of WODs:

```bash
python generate.py --type wod --count 7 --category full-body
```

### 3. Validate Output

The generator validates all output against the schema. On success:

```
✓ Program generated: output/back-in-shape-3w.json
✓ Validated 15 sessions
✓ All rationales cited
```

---

## Project Architecture

### Knowledge Pyramid

The app builds workouts from a strict hierarchy—nothing is invented:

```
┌─────────────────────────────┐
│     AI GENERATION           │  assembles only
│   (Claude API via Python)   │
└──────────────┬──────────────┘
               ↑ constrained by
┌──────────────▼──────────────┐
│   HARD RULES (JSON)         │  time caps, % tables,
│   ├── time_caps             │  recovery constraints,
│   ├── loading_percentages   │  weekly limits
│   ├── weekly_constraints    │
│   └── allowed_sources       │
└──────────────┬──────────────┘
               ↑ derived from
┌──────────────▼──────────────┐
│  KNOWLEDGE BASE (Markdown)  │  curated sports science
│  ├── 01-energy-systems      │  real books, real papers
│  ├── 02-crossfit-methodol   │
│  ├── 03-periodization       │
│  ├── 04-recovery            │
│  └── 05-gymnastics          │
└──────────────┬──────────────┘
               ↑ validated by
┌──────────────▼──────────────┐
│   PRIMARY SCIENCE           │  energy systems,
│  (unchanging foundations)   │  motor learning,
└─────────────────────────────┘  biomechanics
```

### Offline-First Architecture

```
┌──────────────────────────────────────────────┐
│  GitHub Actions (Scheduled or Manual)        │
│  └─ runs generate.py locally                 │
│     ├─ reads knowledge-base/ documents       │
│     ├─ reads data/movement-library.json      │
│     ├─ reads data/hard-rules.json            │
│     ├─ calls Claude API                      │
│     └─ writes to docs/data/*.json            │
│                                              │
│  outputs: programs/, wods/ JSON files        │
│  commits to main, pushes to GitHub           │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  GitHub Pages (Static Hosting)               │
│  └─ serves docs/ folder as website           │
│     ├─ index.html (app shell)                │
│     ├─ manifest.json (PWA config)            │
│     ├─ sw.js (service worker)                │
│     └─ data/ (generated JSON)                │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  User's Browser                              │
│  └─ fetches static JSON                      │
│  └─ renders workout                          │
│  └─ runs timer                               │
│  └─ stores progress in localStorage          │
│     (NO API calls, fully offline capable)    │
└──────────────────────────────────────────────┘
```

**Why this approach?**
- Scales to unlimited users at zero cost
- Works fully offline
- No server maintenance
- No backend vulnerabilities
- Fast load times (static files + local storage)

---

## Running the Generator

### Basic Syntax

```bash
python generate.py --type <type> [options]
```

### Options

#### Program Generation

```bash
python generate.py --type program \
  --name back-in-shape \
  --weeks 3
```

**Arguments:**
- `--name`: Program identifier (lowercase, hyphens OK, maps to `data/programs.json` entry)
- `--weeks`: Duration in weeks (2, 3, or 4)
- `--output-dir`: Where to write output (default: `../output/`)

**Output:**
- `output/<name>-<weeks>w.json` — program data
- `output/<name>-<weeks>w.md` — human-readable preview

---

#### WOD Generation

```bash
python generate.py --type wod \
  --count 7 \
  --category full-body
```

**Arguments:**
- `--count`: Number of WODs to generate
- `--category`: One of: `full-body`, `upper-body`, `lower-body`, `cardio`, `strength`
- `--output-dir`: Where to write output (default: `../output/`)

**Output:**
- `output/wods-<category>.json` — WOD pool
- `output/wods-<category>.md` — preview

---

### Full Example Workflow

```bash
cd scripts

# Generate a complete program suite
python generate.py --type program --name back-in-shape --weeks 2
python generate.py --type program --name back-in-shape --weeks 3
python generate.py --type program --name back-in-shape --weeks 4

# Generate WOD pools (4 weeks of content each)
python generate.py --type wod --count 28 --category full-body
python generate.py --type wod --count 28 --category upper-body
python generate.py --type wod --count 28 --category lower-body
python generate.py --type wod --count 28 --category strength
python generate.py --type wod --count 28 --category cardio

# Output is ready in ../output/ for review or deployment
```

---

## Adding New Programs

### 1. Define the Program

Edit `data/programs.json` (create if it doesn't exist):

```json
{
  "programs": [
    {
      "id": "back-in-shape",
      "name": "Back in Shape",
      "description": "Progressive return to training for general fitness",
      "focus": "general",
      "supported_durations": [2, 3, 4]
    },
    {
      "id": "gymnastics-base",
      "name": "Gymnastics Base",
      "description": "30-minute skill cycle focused on body control",
      "focus": "gymnastics",
      "supported_durations": [4]
    }
  ]
}
```

### 2. Update Knowledge Base if Needed

If your program requires new concepts, add them to `knowledge-base/`:
- `knowledge-base/*.md` files are the source of truth
- Citation sources must be in `data/hard-rules.json → allowed_sources`
- The generator cannot use concepts not in the knowledge base

### 3. Generate

```bash
python generate.py --type program --name gymnastics-base --weeks 4
```

### 4. Validate

Check `output/` for JSON and markdown preview. Verify:
- All sessions are ≤60 min (or ≤30 for skill cycles)
- All rationales cite real sources
- All loading percentages respect hard rules
- No Olympic lifting on consecutive days

---

## Editing Hard Rules

Hard rules enforce constraints that the generator must respect. They live in `data/hard-rules.json`:

```json
{
  "time_caps": {
    "full_session_minutes": 60,
    "skill_session_minutes": 30,
    "metcon_max_minutes": 20,
    "warmup_static_minutes": 5,
    "warmup_active_minutes": 5
  },
  "loading_percentages": {
    "week_1": {"min": 70, "max": 75},
    "week_2": {"min": 75, "max": 80},
    "week_3": {"min": 80, "max": 85},
    "week_4_deload": {"min": 60, "max": 65}
  },
  "weekly_constraints": {
    "max_consecutive_olympic_days": 1,
    "max_heavy_lower_days_per_week": 2,
    "min_aerobic_sessions_per_week": 1,
    "max_consecutive_high_cns_sessions": 1,
    "min_push_pull_ratio": 1.0
  },
  "allowed_sources": [
    "Glassman 2002 - CrossFit Journal",
    "Haff & Triplett - NSCA Essentials 4th ed",
    "... more sources"
  ]
}
```

**After editing:**

1. Re-run the generator to validate changes
2. If validation fails, you've violated a hard rule—fix the JSON
3. Common mistakes:
   - Loading % ranges that overlap or leave gaps
   - Time caps that are too tight
   - Missing source citations in `allowed_sources`

---

## GitHub Actions Pipeline

The workflow automatically regenerates content on a schedule and pushes to `docs/data/`.

### Setup

1. **Create workflow file:** `.github/workflows/generate.yml`

```yaml
name: Generate WODie Content

on:
  schedule:
    # Run every Sunday at midnight UTC
    - cron: '0 0 * * 0'
  workflow_dispatch:  # Allow manual trigger

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install anthropic

      - name: Generate content
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd scripts
          python generate.py --type program --name back-in-shape --weeks 2
          python generate.py --type program --name back-in-shape --weeks 3
          python generate.py --type program --name back-in-shape --weeks 4
          python generate.py --type wod --count 28 --category full-body
          python generate.py --type wod --count 28 --category upper-body
          python generate.py --type wod --count 28 --category lower-body
          python generate.py --type wod --count 28 --category strength
          python generate.py --type wod --count 28 --category cardio

          # Copy outputs to docs/data/
          mkdir -p ../docs/data/programs
          mkdir -p ../docs/data/wods
          cp ../output/back-in-shape-*.json ../docs/data/programs/
          cp ../output/wods-*.json ../docs/data/wods/

      - name: Commit and push
        run: |
          git config user.name "WODie Bot"
          git config user.email "bot@wodie.app"
          git add docs/data/
          git commit -m "chore: regenerate WOD and program content" || true
          git push
```

2. **Set the API key secret:**
   - Go to Settings → Secrets and variables → Actions
   - Create `ANTHROPIC_API_KEY` secret
   - Paste your Claude API key

3. **Configure the schedule:**
   - Edit the `cron` expression in the workflow file
   - `0 0 * * 0` = every Sunday at midnight UTC
   - Use [crontab.guru](https://crontab.guru) to experiment

---

## Data Schema Reference

### Program

```json
{
  "id": "back-in-shape-3w",
  "name": "Back in Shape",
  "weeks": 3,
  "focus": "general",
  "description": "...",
  "sessions": [
    { "week": 1, "day": 1, "..." }
  ]
}
```

### Session

```json
{
  "id": "day-1",
  "week": 1,
  "day": 1,
  "title": "Squat + Short Metcon",
  "durationMinutes": 60,
  "equipment": ["barbell", "plates", "pull-up bar"],
  "blocks": {
    "staticWarmup": { "durationMinutes": 5, "content": [] },
    "activeWarmup": { "durationMinutes": 5, "content": [] },
    "strength": { "durationMinutes": 22, "content": [] },
    "metcon": { "durationMinutes": 15, "format": "AMRAP", "timeCap": 12, "content": [] },
    "cooldown": { "durationMinutes": 8, "content": [] }
  },
  "rationale": {
    "session": { "text": "...", "source": "...", "url": "..." },
    "movement": { "text": "...", "source": "...", "url": "..." },
    "loading": { "text": "...", "source": "...", "url": "..." }
  }
}
```

### Movement (within a block)

```json
{
  "name": "Back Squat",
  "sets": 4,
  "reps": 5,
  "load": "75% 1RM",
  "restSeconds": 180,
  "notes": "Pause 2 seconds in the hole",
  "scaling": "Goblet squat with KB if barbell unavailable"
}
```

### WOD

```json
{
  "id": "wod-14",
  "title": "Grace-style",
  "category": ["full-body", "strength"],
  "equipment": ["barbell", "plates"],
  "durationMinutes": 60,
  "blocks": { },
  "rationale": { }
}
```

---

## Contributing

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where practical
- Test locally before committing

**JavaScript:**
- Use const/let, not var
- Template literals for strings
- Arrow functions preferred

### Before Committing

1. **Test the generator:**
   ```bash
   python generate.py --type program --name back-in-shape --weeks 2
   ```

2. **Verify output:**
   ```bash
   # Check that output/back-in-shape-2w.json is valid
   # Read output/back-in-shape-2w.md for sanity
   ```

3. **Update docs if you change schemas:**
   - Modify `README.md` Data Schema Reference section
   - Update any examples that are now outdated

4. **Commit message:**
   ```
   feat: add new program definition

   - Added "Advanced Lifting" program to data/programs.json
   - Updated knowledge base with Olympic lifting methodology
   - Generator tested with 4-week variant
   ```

---

## Troubleshooting

### "API key not recognized"

```bash
# Make sure the key is exported correctly
export ANTHROPIC_API_KEY=sk-ant-...

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### "Generator fails with validation error"

Output will show which session failed. Common issues:

1. **Session > 60 minutes:**
   ```
   ✗ Day 3: Session is 65 minutes, max is 60
   ```
   Solution: Reduce block durations in the prompt or hard rules.

2. **Missing source citation:**
   ```
   ✗ Day 1: "Rationale" cites unknown source "Smith 2020"
   ```
   Solution: Add the source to `data/hard-rules.json → allowed_sources`.

3. **Loading percentage out of range:**
   ```
   ✗ Day 2: Loading 90% exceeds week 1 max (75%)
   ```
   Solution: Adjust `hard-rules.json → loading_percentages`.

### "Knowledge base concept not in output"

The generator has strict rules:
- Only uses concepts from `knowledge-base/` documents
- Only cites sources from `data/hard-rules.json`
- Cannot invent or generalize

**Solution:** If a concept is missing, add it to the appropriate knowledge base file with citations, then re-run.

### "Hard rules constraint violated"

Example error:
```
✗ Week 1: Olympic lifting on days 1 and 2 (consecutive days)
```

Solution: Check `data/hard-rules.json` and the generator prompt for conflicting rules. The generator is correctly enforcing the constraint—adjust your program design.

---

## Repository Structure

```
wodie/
├── CLAUDE.md                    ← project context for Claude Code
├── DESIGN.md                    ← full product design document
├── README.md                    ← this file (developer guide)
│
├── knowledge-base/              ← source of truth (curated sports science)
│   ├── 01-energy-systems.md
│   ├── 02-crossfit-methodology.md
│   ├── 03-periodization.md
│   ├── 04-recovery.md
│   └── 05-gymnastics.md
│
├── data/                        ← constraints and movement library
│   ├── movement-library.json    ← 68 movements across 6 categories
│   ├── programs.json            ← program definitions
│   └── hard-rules.json          ← time caps, % tables, weekly limits
│
├── scripts/                     ← generation code (not deployed)
│   ├── generate.py              ← main CLI script
│   └── render_md.py             ← markdown renderer for previews
│
├── output/                      ← generated content (git-ignored during dev)
│   ├── *.json                   ← program and WOD data
│   └── *.md                     ← human-readable previews
│
├── docs/                        ← GitHub Pages root (the app)
│   ├── index.html               ← app shell
│   ├── manifest.json            ← PWA config
│   ├── sw.js                    ← service worker
│   ├── assets/
│   │   ├── css/app.css          ← sport-technical styling
│   │   ├── js/app.js            ← frontend app logic
│   │   └── icons/               ← PWA icons (iOS + Android)
│   └── data/                    ← committed generated content
│       ├── programs/            ← program JSON files
│       └── wods/                ← WOD JSON files
│
└── .github/workflows/
    └── generate.yml             ← GitHub Actions regeneration workflow
```

---

## Further Reading

- **[DESIGN.md](./DESIGN.md)** — full product design with UI/UX details
- **[CLAUDE.md](./CLAUDE.md)** — project context and constraints
- **[Anthropic API Docs](https://docs.anthropic.com)** — Claude API reference

---

**Last updated:** June 2026
**Maintainer:** WODie Project
**License:** MIT

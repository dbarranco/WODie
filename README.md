# WODie 🏋️

**AI-Powered CrossFit Programming at Your Fingertips**

Your personal AI coach that delivers science-backed workout programs tailored to your goals. Every session is pre-planned, equipment-optimized, and rooted in sports science research.

## 🚀 Get Started

Visit **[wodie.app](https://wodie.app)** to use WODie now. Install it on your phone like any other app — no subscription required.

---

## What Is WODie?

WODie is a Progressive Web App (PWA) that gives you:

- **Smart Programs** — Structured 2, 3, or 4-week training plans with progressive loading that gets you stronger safely
- **Daily WODs** — Rotating pool of workouts across all categories: full-body, upper-body, lower-body, strength, and cardio
- **Science-Backed** — Every movement, set, and load percentage is grounded in peer-reviewed sports science
- **Equipment Aware** — Knows what you need before you start; never surprises you mid-workout
- **Built-in Timer** — Pre-configured for your workout format (AMRAP, EMOM, For Time); runs offline
- **Zero Cost, Zero Ads** — Completely free. No API calls. No tracking. No server costs.

### Why WODie?

Most fitness apps make real-time API calls, track your data, and require subscriptions. WODie is different:

- ✅ **Works Offline** — All content is generated offline and served as static files
- ✅ **Lightning Fast** — No server delays; your workout starts instantly
- ✅ **Always Available** — Hosted on GitHub Pages; scales to unlimited users at zero cost
- ✅ **Privacy First** — Everything happens in your browser; no data collection
- ✅ **Transparent** — Open-source; see exactly how your workouts are built

---

## How WODie Works

### For Users

1. **Open the app** on [wodie.app](https://wodie.app) or install it to your home screen
2. **Choose your mode:**
   - **Program Mode** — Pick a structured 2/3/4-week program; it guides you day-by-day with progressive loading
   - **WOD Mode** — Pick a category (or random); get a single workout with built-in timer
3. **See your workout** — Equipment list, warmup, main work, metcon, cooldown — all planned
4. **Tap "Start Session"** — Timer runs, clock auto-advances through blocks, beeps at transitions
5. **Track your session** — App remembers your progress (stored locally on your device)

### For Tech Enthusiasts

WODie uses a unique offline-first architecture:

```
[AI Generation (Python)]    [Static Hosting]        [Your Browser]
  ↓ writes JSON             (GitHub Pages)           ↓
docs/data/programs/         ← served as static files
docs/data/wods/             ← zero runtime API calls
                            ← works fully offline
```

All workout content is pre-generated using Claude AI and curated sports science, then committed as static JSON. Your browser fetches and renders it. No servers, no runtime costs, no tracking.

---

## Features

### Program Mode
- **Periodized Training** — Progressive 2/3/4-week blocks with built-in deload weeks
- **Customizable Loads** — Input your 1RMs; the app auto-calculates percentages
- **Session Tracking** — See which days you've completed; pick up where you left off
- **Scientific Rationale** — Every program explains the "why" behind movement selection, loading patterns, and recovery

### WOD Mode
- **5 Categories** — Full-body, Upper, Lower, Strength, Cardio
- **Random or Filtered** — Pick a workout or get a surprise
- **Adaptive Timer** — Pre-configured for AMRAP, EMOM, or For Time
- **Scaling Suggestions** — Every movement includes options for different fitness levels

### Built-in Timer
- **Auto-Advancing Blocks** — Transitions automatically; beeps alert you
- **Final 10-Second Alert** — Red screen + rapid beeps to signal the end
- **Wake Lock** — Screen stays on during active timer (if your device supports it)
- **Works Offline** — No internet required once the app is loaded

### Dark Mode by Default
- **Designed for the Gym** — Easy on the eyes under bright fluorescent lighting
- **Battery Efficient** — Minimizes power drain on your phone

---

## Session Structure

Every full session is exactly 60 minutes, carefully structured:

| Block | Time | What Happens |
|-------|------|---|
| Static Warmup | 5 min | Stretching, mobility, joint prep |
| Active Warmup | 5 min | Movement-specific activation |
| Strength/Skill | 20–25 min | Main work (barbell, gymnastics, etc.) |
| Metcon | 10–20 min | High-intensity metabolic conditioning |
| Cooldown | 5–10 min | Static stretch, foam roll, recovery |

**Skill cycles** (pure gymnastics) are 30 minutes — no metcon.

---

## Science Behind Every Workout

WODie doesn't invent workouts. Every program is built from:

- **Energy Systems Research** — Glassman, Gastin, CrossFit Journal
- **Strength Science** — Haff, Zatsiorsky, Schoenfeld, NSCA guidelines
- **Periodization** — Bompa, proven progressive loading models
- **Gymnastics Methodology** — Sommer, CrossFit Gymnastics Course
- **Recovery Science** — Kreher, Behm, evidence-based rest protocols

Your workouts cite sources. Tap the "Why?" button to read the research.

---

## Install as an App

### iPhone / iPad
1. Open Safari and go to [wodie.app](https://wodie.app)
2. Tap the Share button
3. Tap "Add to Home Screen"
4. Tap "Add"

### Android
1. Open Chrome and go to [wodie.app](https://wodie.app)
2. Tap the menu (⋮)
3. Tap "Install app"
4. Tap "Install"

Now WODie lives on your home screen like a native app.

---

## FAQ

**Can I use it without WiFi?**
Yes! Once loaded, WODie works completely offline. Your workouts are pre-generated and stored locally.

**Will my data be sold?**
No. WODie runs entirely in your browser. No data leaves your device. No trackers, no servers, no accounts.

**How often is content updated?**
WODie regenerates new programs and WODs weekly. Updates are rolled out automatically; nothing to do on your end.

**Can I sync across devices?**
Not yet. Your progress is stored locally on each device. We're exploring optional cross-device sync.

**What if I don't have a barbell?**
Every movement includes scaling options. The app shows alternatives like dumbbells, kettlebells, or bodyweight.

**Is there a cost?**
No. WODie is free and always will be.

---

## Contributing

WODie is open-source. Developers can contribute to:
- **Frontend improvements** — UI/UX, timer logic, offline sync
- **Knowledge base** — Sports science, movement libraries, periodization models
- **Automation** — GitHub Actions workflows, content generation

See [CLAUDE.md](./CLAUDE.md) for developer setup and architecture details.

---

## Quick Start for Developers

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/wodie.git
cd wodie
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Run the Generator

```bash
cd scripts
python generate.py --type program --name back-in-shape --weeks 3
```

### 3. Validate Output

Check `output/` for generated JSON and markdown preview.

---

```
wodie/
├── README.md                    ← you are here
├── CLAUDE.md                    ← project context for developers
├── DESIGN.md                    ← full product design
│
├── knowledge-base/              ← curated sports science
│   ├── 01-energy-systems.md
│   ├── 02-crossfit-methodology.md
│   ├── 03-periodization.md
│   ├── 04-recovery.md
│   └── 05-gymnastics.md
│
├── data/                        ← constraints and movement library
│   ├── movement-library.json
│   ├── programs.json
│   └── hard-rules.json
│
├── scripts/                     ← generation code
│   ├── generate.py
│   └── render_md.py
│
├── output/                      ← generated content (local)
│   ├── *.json
│   └── *.md
│
├── docs/                        ← GitHub Pages (the live app)
│   ├── index.html
│   ├── manifest.json
│   ├── sw.js
│   ├── assets/
│   └── data/
│
└── .github/workflows/
    └── generate.yml
```

---

## License

MIT

---

**Questions?** [Open an issue](https://github.com/yourusername/wodie/issues) or check out [CLAUDE.md](./CLAUDE.md) for developer documentation.

Built with ❤️ using Claude AI and sports science.

# KB Alignment Validation Guide

The KB Alignment Validator checks that generated WODs and programs follow the decision logic documented in the KB Decision Flowcharts.

## Quick Start

```bash
# Validate a single WOD
python scripts/validate-kb-alignment.py --wod output/my-wod.json

# Validate a full program
python scripts/validate-kb-alignment.py --program output/my-program.json

# Get detailed output
python scripts/validate-kb-alignment.py --program output/my-program.json --verbose
```

## How It Works

The validator checks three decision flowcharts:

### Flowchart 1: Energy System → Metcon Format
Validates that the metcon format matches the stated energy system goal.

**Example:**
- If rationale says "Glycolytic system focus"
- Then format must be AMRAP or For Time
- And time cap must be 7–15 minutes

**Why:** Phosphocreatine (ATP-PC) training needs full recovery intervals (EMOM format). Glycolytic training works with continuous effort. Oxidative (aerobic) training needs sustained long efforts.

**Rules:**
- Phosphocreatine (0–10s): EMOM/E2MOM/E3MOM only, 8–12 min cap
- Glycolytic (10s–2m): AMRAP or For Time, 7–15 min cap
- Oxidative (>2m): AMRAP only, 15–20 min cap

### Flowchart 2: Week → Loading Intensity
Validates that loading parameters (intensity %, reps, rest) match the program week.

**Example:**
- Week 1: 70–75% 1RM, 5×5 or 4×5 reps, 180–300s rest
- Week 3 (peak): 80–85% 1RM, 4×3 or 5×2 reps, 180–300s rest

**Why:** Periodization follows a 4-week cycle (baseline → build → peak → deload). Each week has specific adaptation targets.

**Week-by-week breakdown:**
- Week 1 (baseline): 70–75%, 5x5/4x5 reps
- Week 2 (build): 75–80%, 4x4/4x3 reps
- Week 3 (peak): 80–85%, 4x3/5x2 reps
- Week 4 (deload): 60–65%, 3x5/3x3 reps

### Flowchart 3: Weekly Sequencing
Validates that sessions are ordered to minimize interference between adaptations.

**Rules:**
- No Olympic lifting on consecutive days (neural fatigue)
- No heavy lower body on consecutive days (glycogen depletion + CNS fatigue)
- No high-CNS sessions back-to-back (recovery)
- Minimum 1 aerobic session per week (aerobic base development)

**Why:** Concurrent training (strength + endurance in same week) creates interference. Strategic sequencing minimizes this.

## Interpreting Results

**✓ PASS:** All sessions/WODs follow all KB rules. Generator is working correctly.

**⚠ PARTIAL:** Some sessions pass, some fail. Check `--verbose` output for details.

**✗ FAIL:** Sessions violate KB rules. Debug the generator prompt or KB modules.

### Example Output

```
✓ PASS — Program Validation: back-in-shape-3w

  ✓ session_w1d1_energy_system_stated
      Rationale states glycolytic goal
  ✓ session_w1d1_format_for_glycolytic
      Format AMRAP is in allowed list ['AMRAP', 'For Time'] for glycolytic
  ✓ session_w1d1_time_cap_for_glycolytic
      Time cap 12min is in range 7-15min for glycolytic
  ✓ session_w1d1_intensity_week_1
      Intensity 72% is in range 70-75% for week 1
  ✓ session_w1d1_rep_scheme_week_1
      Rep scheme 5x5 is in allowed list ['5x5', '4x5'] for week 1
```

### Common Failures

**✗ energy_system_stated**
- Generator did not include energy system keyword in session rationale
- Fix: Update generator prompt to be explicit about energy system goal

**✗ format_for_ENERGY_SYSTEM**
- Metcon format (AMRAP, For Time, EMOM) doesn't match energy system
- Example: EMOM for glycolytic (should be AMRAP/For Time)
- Fix: Check generator prompt rules for energy system → format mapping

**✗ time_cap_for_ENERGY_SYSTEM**
- Metcon time cap is outside valid range for this energy system
- Example: 20-minute oxidative session (should be 15-20 max)
- Fix: Ensure generator enforces time cap ranges per energy system

**✗ intensity_week_N**
- Loading intensity (% 1RM) is outside week-specific range
- Example: Week 1 at 80% (should be 70-75%)
- Fix: Check KB 03 Periodization periodization rules and update generator

**✗ no_consecutive_olympic_wN**
- Olympic lifts (snatch, clean, jerk) scheduled on consecutive days
- Fix: Add rest day or move one Olympic session to non-consecutive day

**✗ no_consecutive_heavy_lower_wN**
- Heavy lower body (squat, deadlift >75%) on consecutive days
- Fix: Space out heavy lower days by at least one recovery day

**✗ no_consecutive_high_cns_wN**
- Two high-CNS sessions (Olympic + heavy strength + For Time metcons) back-to-back
- Fix: Insert aerobic or skill-focused session between them

**✗ min_aerobic_wN**
- Week has zero aerobic sessions
- Fix: Add at least one AMRAP 15+min or explicitly aerobic session per week

## Maintenance

When the KB changes:
1. Update the flowchart spec (`docs/superpowers/specs/2026-06-29-kb-decision-flowcharts-design.md`)
2. Update the validator rules in `scripts/validate-kb-alignment.py` to match
3. Re-validate existing programs to ensure they still align

When generator output diverges:
1. Run validator with `--verbose` on the divergent WOD/session
2. Trace which flowchart failed (Flowchart 1, 2, or 3)
3. Check if the issue is in:
   - Generator prompt (should be more explicit about KB rule)
   - KB module (rule is unclear or incorrect)
   - hard-rules.json (constraint is missing or outdated)
4. Fix the root cause and re-generate

## Next Steps

After validating a sample, generate the full WOD pool:

```bash
cd scripts
python generate.py --type wod --count 7 --category full-body
python generate.py --type wod --count 7 --category upper-body
python generate.py --type wod --count 7 --category lower-body
python generate.py --type wod --count 7 --category strength
python generate.py --type wod --count 7 --category cardio

# Validate all outputs
python validate-kb-alignment.py --program output/back-in-shape-3w.json --verbose
```

## Script Help

For detailed help:

```bash
python scripts/validate-kb-alignment.py --help
```

This will show all available options, flowchart descriptions, and example usage.

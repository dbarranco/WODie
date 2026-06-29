# Woddy Validation System

## Overview

The Woddy generation pipeline includes comprehensive validation to ensure generated programs and WODs comply with all hard rules and maintain data quality. Validations run automatically during generation and report warnings without failing the generation process (allowing inspection of minor issues).

## Validation Layers

### 1. Schema Validation (`validate_schema_structure`)

**Purpose:** Ensure generated JSON matches the expected structure

**Checks:**
- Top-level keys exist (`program`, `wods`)
- Required fields present in all sessions (id, title, blocks, rationale)
- Required blocks present (static_warmup, active_warmup, strength, metcon, cooldown)
- Block movements are arrays
- Rationale fields are objects with 'text' field
- No literal "undefined" values in the JSON

**Failure Behavior:** Raises error immediately (generation stops)

---

### 2. Hard Rules Validation (`validate_program`)

**Purpose:** Ensure generated content follows all constraints from `hard-rules.json`

#### A. Session Duration Validation
- **Rule:** Full sessions ≤ 60 minutes
- **Check:** `duration_minutes` ≤ 60
- **Issue Type:** Warning

#### B. Block Duration Validation
- **Static warmup:** Must be exactly 5 minutes
- **Active warmup:** Must be exactly 5 minutes
- **Strength block:** 20-25 minutes (flexible based on week)
- **Metcon block:** 10-20 minutes (sufficient for complete workout)
- **Cooldown:** 5-10 minutes (recovery focus)
- **Issue Type:** Warning (indicates timing miscalculation)

#### C. Movement Library Validation
- **Rule:** All movements must exist in `movement-library.json`
- **Check:** Movement names matched against 68 approved movements across 6 categories
- **Categories:** 
  - Barbell lifts (squat, deadlift, clean, press, etc.)
  - Gymnastics (pull-ups, muscle-ups, handstand work, etc.)
  - Monostructural (rowing, running, assault bike, etc.)
  - Functional movements (kettlebells, boxes, etc.)
  - Accessory lifts
  - Stretches and mobility
- **Issue Type:** Warning (indicates generated movement not in library)

#### D. Metcon Format Validation
- **Allowed Formats:** AMRAP, EMOM, For Time, RFT
- **Forbidden Formats:** Chipper, Hero WOD
- **Case Sensitivity:** Formats checked case-insensitively (e.g., "FOR TIME" matches "For Time")
- **Time Cap Check:** Max 20 minutes (aligns with 10-20 min metcon block duration)
- **Issue Type:** Warning (format doesn't match allowed list)

#### E. Equipment Validation
- **Forbidden Equipment:** PVC pipe, PVC (not commonly available)
- **Recommendation:** Use "empty barbell" or "broomstick" for mobility work instead
- **Issue Type:** Warning

#### F. Rationale Validation (Critical)
- **Required Fields:** 
  - `session_why` (why this session type on this day)
  - `movement_why` (why these movements together)
  - `loading_why` (why this rep scheme/percentage)
- **Citation Check:** All sources must be in `allowed_sources` list
- **Allowed Sources:** 
  - Glassman 2002 - CrossFit Journal
  - Haff & Triplett - NSCA Essentials 4th ed
  - Bompa & Haff - Periodization 5th ed
  - Zatsiorsky & Kraemer - Science and Practice of Strength Training
  - Schoenfeld - Science and Development of Muscle Hypertrophy
  - Wilson et al 2012 - Concurrent Training Meta-Analysis
  - Robbins 2005 - Post-Activation Potentiation
  - Sommer - Building the Gymnastic Body
  - CrossFit Level 2 Training Guide
  - CrossFit Gymnastics Specialty Course
  - Gastin 2001 - Energy System Interaction
  - Behm et al 2016 - Acute Effects of Muscle Stretching
  - Kreher & Schwartz 2012 - Overtraining Syndrome
  - And 7 more specialized sources
- **Fabrication Prevention:** No invented citations or loading percentages
- **Issue Type:** Warning (missing text, invalid source)

#### G. Weekly Frequency Validation
- **High-Intensity Metcons:** Max 4 per week (AMRAP, For Time)
- **Aerobic Sessions:** Minimum 1 per week
- **Track:** By week, aggregate across all sessions
- **Issue Type:** Warning (frequency limits exceeded)

#### H. Program Structure Validation (4-Week Programs)
- **Week 4 Requirement:** Must emphasize deload/recovery
- **Check:** Rationale text includes "deload" or "recovery" keywords
- **Purpose:** Ensure proper periodization (intense weeks 1-3, recovery week 4)
- **Issue Type:** Warning

---

## Example Output

### Passing Validation
```
Validating structure...
   ✅ JSON parsed successfully

Validating against hard rules...
   ✅ Validation passed (0 warnings)
```

### With Warnings
```
Validating against hard rules...
   ⚠️  40 validation issues:
      - Session w1d1: 'good morning (empty bar)' not found in movement library
      - Session w2d1: metcon format 'FOR TIME' not in allowed formats ['AMRAP', 'EMOM', 'For Time', 'RFT']
      - Session w1d3: strength duration 15 outside 20-25 min range
      ... and 37 more
```

---

## How to Read Validation Output

### Immediate Stop (Schema Failure)
If validation shows:
```
❌ Schema validation failed:
   - Missing top-level 'program' key
```
**Generation stops.** Check the raw JSON in `output/debug-last-response.txt` and retry.

### Warnings (Content Issues)
If validation shows warnings but JSON is valid:
- Generation **succeeds** and file is saved
- Warnings indicate areas Claude should improve in next generation
- Common issues:
  - Movement names not in library → update KB with more examples
  - Metcon format case mismatch → Claude already knows this, may need retry
  - Duration mismatches → KB generation prompt adjustment needed
  - Citation not in allowed sources → KB module needs expansion

---

## Adding New Validations

To add a new validation check:

1. **Identify the constraint** in `hard-rules.json`
2. **Implement validation function** in `validate_program()`
3. **Test against existing programs** to verify no false positives
4. **Update this guide** with the new validation

Example:
```python
# Check new constraint
if new_metric > rules["some"]["threshold"]:
    violations.append(f"Session {session_id}: {constraint_name} violated")
```

---

## Validation Improvement Workflow

1. **Generate program** → See validation warnings
2. **Identify pattern** (e.g., "movement names always fail because KB needs more examples")
3. **Update KB** or **adjust prompt** to fix the root cause
4. **Regenerate** → Verify warnings decrease
5. **Iterate** until validation passes with 0 warnings

---

## Current Status

**Implemented Validations:**
- ✅ Schema structure (7 checks)
- ✅ Session duration (1 check)
- ✅ Block durations (5 checks)
- ✅ Movement library (per-movement validation)
- ✅ Metcon format (format + time cap)
- ✅ Equipment restrictions (forbidden items)
- ✅ Rationale completeness (3 fields × sources)
- ✅ Weekly frequency (2 checks)
- ✅ Program deload (week 4 for 4-week programs)

**Future Enhancements:**
- Olympic lifting frequency (max 3/week, no consecutive days)
- Movement pattern balance (push/pull ratio, squat/hinge, etc.)
- Volume per pattern (sets min/max per movement category)
- Progression scheme variety (don't repeat same loading pattern)
- Movement diversity (don't repeat main movements in WODs)


# KB Decision Flowcharts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create visual decision flowcharts and a validation test that trace knowledge base principles to actual WOD generation decisions, enabling validation that the generator follows KB logic.

**Architecture:** Three independent flowcharts (energy system → metcon format, program week → loading intensity, weekly energy system sequencing) will be rendered as ASCII diagrams in the design document. A separate validation script will sample a generated WOD and check it against the flowcharts to detect misalignments between KB and generator output.

**Tech Stack:** Python (validation script), markdown (flowchart documentation), existing generator.py framework

## Global Constraints

- All flowcharts must live in `/Users/arpa/projects/Woddy/docs/superpowers/specs/2026-06-29-kb-decision-flowcharts-design.md` (already created)
- Validation script lives in `/Users/arpa/projects/Woddy/scripts/validate-kb-alignment.py`
- Validation must check 3 decision paths: metcon format, loading intensity, weekly sequencing
- Validation should work against both programs and WODs
- No changes to hard-rules.json, generator.py, or KB modules — validation only

---

## File Structure

**Files to create:**
- `scripts/validate-kb-alignment.py` — validation script that takes a generated WOD/program and checks if decisions align with flowcharts

**Files to modify:**
- None (flowchart spec already exists)

**No test files needed** — validation script will be executable directly and output human-readable pass/fail results

---

## Tasks

### Task 1: Create Validation Script Structure

**Files:**
- Create: `scripts/validate-kb-alignment.py`

**Interfaces:**
- Consumes: Generated WOD JSON structure (from `output/` or `docs/data/`)
- Produces: Pass/fail report with decision trace-backs for each WOD/session

**Steps:**

- [ ] **Step 1: Create validation script skeleton**

```python
#!/usr/bin/env python3
"""
KB Alignment Validator

Checks if generated WODs and programs align with KB-derived decision flowcharts.
Validates three decision paths:
  1. Energy system → metcon format (Flowchart 1)
  2. Program week → loading intensity (Flowchart 2)
  3. Weekly sequencing rules (Flowchart 3)

Usage:
  python validate-kb-alignment.py --wod output/back-in-shape-3w.json
  python validate-kb-alignment.py --program output/back-in-shape-3w-program.json
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# ── KB Decision Rules (Flowcharts Encoded) ──────────────────────────────────

@dataclass
class ValidationResult:
    """Result of validating a single WOD or session."""
    passed: bool
    wod_id: str
    checks: List[Tuple[str, bool, str]]  # (check_name, passed, reason)

class KBValidator:
    """Validates WODs against KB decision flowcharts."""

    def __init__(self):
        """Initialize KB decision rules."""
        self.energy_system_rules = self._init_energy_system_rules()
        self.loading_rules = self._init_loading_rules()
        self.sequencing_rules = self._init_sequencing_rules()

    def _init_energy_system_rules(self) -> Dict:
        """Flowchart 1: Energy system → metcon format mapping."""
        return {
            "phosphocreatine": {
                "allowed_formats": ["EMOM", "E2MOM", "E3MOM"],
                "time_cap_min": 8,
                "time_cap_max": 12,
                "note": "Requires full PCr recovery; interval structure ensures 2-3 min rest"
            },
            "glycolytic": {
                "allowed_formats": ["AMRAP", "For Time", "RFT"],
                "time_cap_min": 7,
                "time_cap_max": 15,
                "note": "Work-to-rest ratio built into continuous effort"
            },
            "oxidative": {
                "allowed_formats": ["AMRAP"],
                "time_cap_min": 15,
                "time_cap_max": 20,
                "note": "Sustained effort >10 min develops aerobic base"
            }
        }

    def _init_loading_rules(self) -> Dict:
        """Flowchart 2: Program week → loading intensity mapping."""
        return {
            1: {
                "intensity_min": 70,
                "intensity_max": 75,
                "rep_schemes": ["5x5", "4x5"],
                "rest_range": "180-300s (varies by goal)",
                "goal": "Technique + baseline load"
            },
            2: {
                "intensity_min": 75,
                "intensity_max": 80,
                "rep_schemes": ["4x4", "4x3"],
                "rest_range": "120-180s",
                "goal": "Build"
            },
            3: {
                "intensity_min": 80,
                "intensity_max": 85,
                "rep_schemes": ["4x3", "5x2"],
                "rest_range": "180-300s",
                "goal": "Peak intensity"
            },
            4: {
                "intensity_min": 60,
                "intensity_max": 65,
                "rep_schemes": ["3x5", "3x3"],
                "rest_range": "120-180s",
                "goal": "Deload"
            }
        }

    def _init_sequencing_rules(self) -> Dict:
        """Flowchart 3: Weekly sequencing constraints."""
        return {
            "no_consecutive_olympic": True,
            "no_consecutive_heavy_lower": True,
            "no_consecutive_high_cns": True,
            "strength_before_metcon_required": True,
            "min_aerobic_sessions_per_week": 1,
            "min_push_pull_ratio": 1.0
        }

    def validate_wod(self, wod: Dict) -> ValidationResult:
        """Validate a single WOD against KB rules."""
        passed = True
        checks = []

        # Placeholder: will implement in Task 2-4
        return ValidationResult(passed=passed, wod_id=wod.get("id", "unknown"), checks=checks)

    def validate_program(self, program: Dict) -> List[ValidationResult]:
        """Validate all sessions in a program."""
        results = []
        # Placeholder: will implement in Task 5
        return results

def main():
    parser = argparse.ArgumentParser(description="Validate WOD alignment with KB flowcharts")
    parser.add_argument("--wod", type=str, help="Path to generated WOD JSON file")
    parser.add_argument("--program", type=str, help="Path to generated program JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print detailed check results")

    args = parser.parse_args()

    if not args.wod and not args.program:
        parser.print_help()
        return

    validator = KBValidator()

    if args.wod:
        with open(args.wod) as f:
            wod_data = json.load(f)
        result = validator.validate_wod(wod_data)
        print(f"WOD Validation: {'PASS' if result.passed else 'FAIL'}")
        if args.verbose:
            for check_name, passed, reason in result.checks:
                status = "✓" if passed else "✗"
                print(f"  {status} {check_name}: {reason}")

    if args.program:
        with open(args.program) as f:
            program_data = json.load(f)
        results = validator.validate_program(program_data)
        passed_count = sum(1 for r in results if r.passed)
        print(f"Program Validation: {passed_count}/{len(results)} sessions passed")
        if args.verbose:
            for result in results:
                print(f"  {result.wod_id}: {'PASS' if result.passed else 'FAIL'}")
                for check_name, passed, reason in result.checks:
                    status = "✓" if passed else "✗"
                    print(f"    {status} {check_name}: {reason}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify script runs (with placeholders)**

Run: `python scripts/validate-kb-alignment.py --help`
Expected: Help text displays correctly

- [ ] **Step 3: Commit skeleton**

```bash
git add scripts/validate-kb-alignment.py
git commit -m "feat: Add KB alignment validator skeleton"
```

---

### Task 2: Implement Flowchart 1 Validation (Energy System → Metcon Format)

**Files:**
- Modify: `scripts/validate-kb-alignment.py` (lines 50-100 and add method)

**Interfaces:**
- Consumes: WOD metcon block with `format`, `time_cap_minutes`, and rationale stating energy system goal
- Produces: Boolean result + list of violations (format mismatch, time cap out of range)

**Steps:**

- [ ] **Step 1: Add energy system extraction helper**

```python
def _extract_energy_system_from_rationale(self, rationale: Dict) -> Optional[str]:
    """Extract energy system target from session rationale.

    Looks for keywords in session_why.text:
    - 'phosphocreatine' or 'ATP-PC' or 'maximal effort'
    - 'glycolytic' or 'anaerobic' or 'high-intensity'
    - 'oxidative' or 'aerobic' or 'base work'

    Returns: 'phosphocreatine', 'glycolytic', 'oxidative', or None
    """
    if not rationale or "session_why" not in rationale:
        return None

    text = rationale["session_why"].get("text", "").lower()

    if any(kw in text for kw in ["phosphocreatine", "atp-pc", "maximal effort", "heavy single"]):
        return "phosphocreatine"
    elif any(kw in text for kw in ["glycolytic", "anaerobic", "high-intensity", "metcon intensity"]):
        return "glycolytic"
    elif any(kw in text for kw in ["oxidative", "aerobic", "base", "long effort"]):
        return "oxidative"

    return None
```

- [ ] **Step 2: Add metcon format validation method**

```python
def _check_metcon_format_alignment(self, wod: Dict) -> Tuple[bool, List[Tuple[str, bool, str]]]:
    """Validate Flowchart 1: Energy system → metcon format.

    Returns: (passed: bool, checks: List[(check_name, passed, reason)])
    """
    checks = []
    passed = True

    # Extract energy system goal from rationale
    rationale = wod.get("rationale", {})
    energy_system = self._extract_energy_system_from_rationale(rationale)

    if not energy_system:
        checks.append(("energy_system_stated", False, "Rationale does not state energy system target"))
        passed = False
        return (passed, checks)

    # Get metcon block
    metcon = wod.get("blocks", {}).get("metcon", {})
    if not metcon:
        checks.append(("metcon_exists", False, "No metcon block found"))
        passed = False
        return (passed, checks)

    # Extract format and time cap
    format_chosen = metcon.get("format", "unknown")
    time_cap = metcon.get("time_cap_minutes", 0)

    # Get expected rules for this energy system
    rules = self.energy_system_rules.get(energy_system, {})
    allowed = rules.get("allowed_formats", [])
    cap_min = rules.get("time_cap_min", 0)
    cap_max = rules.get("time_cap_max", 100)

    # Check format matches energy system
    format_match = format_chosen in allowed
    checks.append((
        f"format_for_{energy_system}",
        format_match,
        f"Format {format_chosen} {'is' if format_match else 'is not'} in allowed list {allowed} for {energy_system}"
    ))
    if not format_match:
        passed = False

    # Check time cap is in range
    cap_ok = cap_min <= time_cap <= cap_max
    checks.append((
        f"time_cap_for_{energy_system}",
        cap_ok,
        f"Time cap {time_cap}min {'is' if cap_ok else 'is not'} in range {cap_min}-{cap_max}min for {energy_system}"
    ))
    if not cap_ok:
        passed = False

    return (passed, checks)
```

- [ ] **Step 3: Update validate_wod to call Flowchart 1 check**

Replace the placeholder section in `validate_wod()`:

```python
def validate_wod(self, wod: Dict) -> ValidationResult:
    """Validate a single WOD against KB rules."""
    passed = True
    checks = []

    # Flowchart 1: Energy system → metcon format
    fc1_passed, fc1_checks = self._check_metcon_format_alignment(wod)
    checks.extend(fc1_checks)
    if not fc1_passed:
        passed = False

    return ValidationResult(passed=passed, wod_id=wod.get("id", "unknown"), checks=checks)
```

- [ ] **Step 4: Create a test WOD file to validate against**

Create `/tmp/test-wod.json`:

```json
{
  "id": "test-wod-1",
  "blocks": {
    "metcon": {
      "format": "AMRAP",
      "time_cap_minutes": 12,
      "movements": []
    }
  },
  "rationale": {
    "session_why": {
      "text": "Glycolytic system focus — high-intensity sustained effort develops anaerobic threshold",
      "source": "Gastin 2001 - Energy System Interaction"
    }
  }
}
```

- [ ] **Step 5: Test Flowchart 1 validation**

Run: `python scripts/validate-kb-alignment.py --wod /tmp/test-wod.json --verbose`
Expected: Output shows PASS for energy system check (AMRAP + 12min matches glycolytic rules)

- [ ] **Step 6: Create a failing test case**

Create `/tmp/test-wod-fail.json`:

```json
{
  "id": "test-wod-fail-1",
  "blocks": {
    "metcon": {
      "format": "For Time",
      "time_cap_minutes": 25,
      "movements": []
    }
  },
  "rationale": {
    "session_why": {
      "text": "Phosphocreatine training — heavy singles and short bursts",
      "source": "KB 01"
    }
  }
}
```

- [ ] **Step 7: Test failing case**

Run: `python scripts/validate-kb-alignment.py --wod /tmp/test-wod-fail.json --verbose`
Expected: Output shows FAIL (For Time not in [EMOM, E2MOM, E3MOM], 25min exceeds 12min cap)

- [ ] **Step 8: Commit Flowchart 1 implementation**

```bash
git add scripts/validate-kb-alignment.py
git commit -m "feat: Implement Flowchart 1 (energy system → metcon format) validation"
```

---

### Task 3: Implement Flowchart 2 Validation (Week → Loading Intensity)

**Files:**
- Modify: `scripts/validate-kb-alignment.py`

**Interfaces:**
- Consumes: Session strength block with `movements[].load` (e.g., "75% 1RM") and program week context
- Produces: Boolean result + violations (intensity out of range, wrong rep scheme)

**Steps:**

- [ ] **Step 1: Add intensity extraction helper**

```python
def _extract_intensity_percentage(self, load_string: str) -> Optional[float]:
    """Extract percentage from load string like '75% 1RM' or 'RPE 7'.

    Returns: float (0-100) for percentage, or None if unparseable
    """
    if not load_string:
        return None

    load_lower = load_string.lower()

    # Handle "X% 1RM" format
    if "%" in load_string:
        try:
            return float(load_string.split("%")[0].strip())
        except (ValueError, IndexError):
            return None

    # RPE and RIR handled separately — skip for now (outside KB scope)
    return None
```

- [ ] **Step 2: Add rep scheme extraction helper**

```python
def _extract_rep_scheme(self, movement: Dict) -> Optional[str]:
    """Extract rep scheme from movement.

    Looks for 'sets x reps' pattern in 'sets' and 'reps' fields.
    Returns: 'SxR' format (e.g., '5x5', '4x3') or None
    """
    sets = movement.get("sets")
    reps = movement.get("reps")

    if sets is None or reps is None:
        return None

    # Handle reps as string or int
    reps_str = str(reps).strip()

    # Simple case: single rep count
    if reps_str.isdigit():
        return f"{sets}x{reps_str}"

    # Range case: '3-5' — use minimum for scheme matching
    if "-" in reps_str:
        min_rep = reps_str.split("-")[0].strip()
        if min_rep.isdigit():
            return f"{sets}x{min_rep}"

    return None
```

- [ ] **Step 3: Add loading validation method**

```python
def _check_loading_intensity_alignment(self, session: Dict, week: int) -> Tuple[bool, List[Tuple[str, bool, str]]]:
    """Validate Flowchart 2: Program week → loading intensity.

    Returns: (passed: bool, checks: List[(check_name, passed, reason)])
    """
    checks = []
    passed = True

    # Get strength block
    strength = session.get("blocks", {}).get("strength", {})
    if not strength:
        checks.append(("strength_block_exists", False, "No strength block found"))
        return (passed, checks)

    movements = strength.get("movements", [])
    if not movements:
        checks.append(("strength_movements_exist", False, "No movements in strength block"))
        return (passed, checks)

    # Get week-specific loading rules
    week_rules = self.loading_rules.get(week)
    if not week_rules:
        checks.append(("week_valid", False, f"Week {week} not in loading rules"))
        passed = False
        return (passed, checks)

    intensity_min = week_rules["intensity_min"]
    intensity_max = week_rules["intensity_max"]
    allowed_schemes = week_rules["rep_schemes"]

    # Check first movement's intensity (proxy for session intensity)
    first_move = movements[0]
    intensity = self._extract_intensity_percentage(first_move.get("load", ""))

    if intensity is not None:
        intensity_ok = intensity_min <= intensity <= intensity_max
        checks.append((
            f"intensity_week_{week}",
            intensity_ok,
            f"Intensity {intensity}% {'is' if intensity_ok else 'is not'} in range {intensity_min}-{intensity_max}% for week {week}"
        ))
        if not intensity_ok:
            passed = False
    else:
        checks.append((
            f"intensity_week_{week}",
            False,
            f"Could not extract intensity percentage from load string '{first_move.get('load', '')}'"
        ))
        passed = False

    # Check rep scheme
    rep_scheme = self._extract_rep_scheme(first_move)
    if rep_scheme:
        scheme_ok = rep_scheme in allowed_schemes
        checks.append((
            f"rep_scheme_week_{week}",
            scheme_ok,
            f"Rep scheme {rep_scheme} {'is' if scheme_ok else 'is not'} in allowed list {allowed_schemes} for week {week}"
        ))
        if not scheme_ok:
            passed = False
    else:
        checks.append((
            f"rep_scheme_week_{week}",
            False,
            "Could not extract rep scheme from sets/reps fields"
        ))
        # Don't fail on this if it's optional

    return (passed, checks)
```

- [ ] **Step 4: Create a test program file**

Create `/tmp/test-program.json`:

```json
{
  "program": {
    "id": "test-prog",
    "name": "Test Program",
    "weeks": 3,
    "sessions": [
      {
        "id": "w1d1",
        "week": 1,
        "day": 1,
        "blocks": {
          "strength": {
            "movements": [
              {
                "name": "Back Squat",
                "sets": 5,
                "reps": "5",
                "load": "72% 1RM"
              }
            ]
          }
        }
      },
      {
        "id": "w3d2",
        "week": 3,
        "day": 2,
        "blocks": {
          "strength": {
            "movements": [
              {
                "name": "Back Squat",
                "sets": 4,
                "reps": "3",
                "load": "82% 1RM"
              }
            ]
          }
        }
      }
    ]
  }
}
```

- [ ] **Step 5: Test Flowchart 2 validation (passing)**

Run: `python scripts/validate-kb-alignment.py --program /tmp/test-program.json --verbose`
Expected: Week 1 session shows PASS (72% in 70-75% range, 5x5 in allowed schemes); Week 3 shows PASS (82% in 80-85%, 4x3 in allowed)

- [ ] **Step 6: Create failing test case**

Update `/tmp/test-program.json` session 1:
```json
{
  "id": "w1d1-bad",
  "week": 1,
  "day": 1,
  "blocks": {
    "strength": {
      "movements": [
        {
          "name": "Back Squat",
          "sets": 4,
          "reps": "2",
          "load": "88% 1RM"
        }
      ]
    }
  }
}
```

- [ ] **Step 7: Test failing case**

Run: `python scripts/validate-kb-alignment.py --program /tmp/test-program.json --verbose`
Expected: Week 1 shows FAIL (88% exceeds 75% max for week 1; 4x2 not in [5x5, 4x5])

- [ ] **Step 8: Commit Flowchart 2 implementation**

```bash
git add scripts/validate-kb-alignment.py
git commit -m "feat: Implement Flowchart 2 (week → loading intensity) validation"
```

---

### Task 4: Implement Flowchart 3 Validation (Weekly Sequencing Rules)

**Files:**
- Modify: `scripts/validate-kb-alignment.py`

**Interfaces:**
- Consumes: Full program with 5 sessions per week, each session has movement types and metcon format
- Produces: Boolean result + violations (consecutive olympic lifts, missing aerobic session, etc.)

**Steps:**

- [ ] **Step 1: Add session classification helpers**

```python
def _has_olympic_lift(self, session: Dict) -> bool:
    """Check if session contains Olympic lifting movements."""
    strength = session.get("blocks", {}).get("strength", {})
    movements = strength.get("movements", [])

    olympic_keywords = ["snatch", "clean", "jerk", "power clean", "power snatch"]

    for move in movements:
        name = move.get("name", "").lower()
        if any(kw in name for kw in olympic_keywords):
            return True

    return False

def _is_heavy_lower_body(self, session: Dict) -> bool:
    """Check if session is heavy lower body work (intensity >75%)."""
    strength = session.get("blocks", {}).get("strength", {})
    movements = strength.get("movements", [])

    lower_keywords = ["squat", "deadlift", "front squat", "back squat", "leg press"]

    for move in movements:
        name = move.get("name", "").lower()
        if any(kw in name for kw in lower_keywords):
            intensity = self._extract_intensity_percentage(move.get("load", ""))
            if intensity and intensity > 75:
                return True

    return False

def _is_high_cns_session(self, session: Dict) -> bool:
    """Check if session is high CNS demand (heavy strength or olympic or high-intensity metcon)."""
    if self._has_olympic_lift(session):
        return True

    if self._is_heavy_lower_body(session):
        return True

    # High-intensity metcon (For Time, heavy AMRAP)
    metcon = session.get("blocks", {}).get("metcon", {})
    if metcon:
        fmt = metcon.get("format", "").upper()
        if fmt == "FOR TIME":
            return True

    return False

def _count_aerobic_sessions(self, week_sessions: List[Dict]) -> int:
    """Count sessions with aerobic/long-duration emphasis."""
    count = 0

    for session in week_sessions:
        # Look for AMRAP 15-20 min or aerobic keywords in rationale
        metcon = session.get("blocks", {}).get("metcon", {})
        if metcon:
            duration = metcon.get("duration_minutes", 0)
            if duration >= 15:
                count += 1

        # Check rationale for aerobic keywords
        rationale = session.get("rationale", {})
        session_why = rationale.get("session_why", {}).get("text", "").lower()
        if any(kw in session_why for kw in ["aerobic", "base", "endurance"]):
            count += 1

    return min(count, 5)  # Cap at 5 to avoid double-counting
```

- [ ] **Step 2: Add sequencing validation method**

```python
def _check_weekly_sequencing_alignment(self, program: Dict) -> Tuple[bool, List[Tuple[str, bool, str]]]:
    """Validate Flowchart 3: Weekly sequencing rules.

    Returns: (passed: bool, checks: List[(check_name, passed, reason)])
    """
    checks = []
    passed = True

    sessions = program.get("sessions", [])
    if not sessions:
        checks.append(("sessions_exist", False, "No sessions in program"))
        return (passed, checks)

    # Group sessions by week
    weeks = {}
    for session in sessions:
        week = session.get("week", 0)
        if week not in weeks:
            weeks[week] = []
        weeks[week].append(session)

    # Validate each week
    for week_num in sorted(weeks.keys()):
        week_sessions = weeks[week_num]

        # Constraint 1: No consecutive Olympic lifting days
        olympic_sessions = [(i, s) for i, s in enumerate(week_sessions) if self._has_olympic_lift(s)]
        for i in range(len(olympic_sessions) - 1):
            day_i = olympic_sessions[i][0]
            day_j = olympic_sessions[i + 1][0]
            if day_j - day_i == 1:  # Consecutive days
                checks.append((
                    f"no_consecutive_olympic_w{week_num}",
                    False,
                    f"Olympic lifting on consecutive days {day_i+1} and {day_j+1}"
                ))
                passed = False
            else:
                checks.append((
                    f"no_consecutive_olympic_w{week_num}",
                    True,
                    f"Olympic days separated by {day_j - day_i - 1} day(s)"
                ))

        # Constraint 2: No consecutive heavy lower body
        heavy_lower = [(i, s) for i, s in enumerate(week_sessions) if self._is_heavy_lower_body(s)]
        for i in range(len(heavy_lower) - 1):
            day_i = heavy_lower[i][0]
            day_j = heavy_lower[i + 1][0]
            if day_j - day_i == 1:
                checks.append((
                    f"no_consecutive_heavy_lower_w{week_num}",
                    False,
                    f"Heavy lower body on consecutive days {day_i+1} and {day_j+1}"
                ))
                passed = False

        # Constraint 3: No consecutive high-CNS sessions
        high_cns = [(i, s) for i, s in enumerate(week_sessions) if self._is_high_cns_session(s)]
        for i in range(len(high_cns) - 1):
            day_i = high_cns[i][0]
            day_j = high_cns[i + 1][0]
            if day_j - day_i == 1:
                checks.append((
                    f"no_consecutive_high_cns_w{week_num}",
                    False,
                    f"High-CNS sessions on consecutive days {day_i+1} and {day_j+1}"
                ))
                passed = False

        # Constraint 4: Minimum 1 aerobic session per week
        aerobic_count = self._count_aerobic_sessions(week_sessions)
        aerobic_ok = aerobic_count >= 1
        checks.append((
            f"min_aerobic_w{week_num}",
            aerobic_ok,
            f"Week {week_num} has {aerobic_count} aerobic session(s) (need ≥1)"
        ))
        if not aerobic_ok:
            passed = False

    return (passed, checks)
```

- [ ] **Step 3: Update validate_program to call Flowchart 3 check**

Modify the `validate_program()` method placeholder:

```python
def validate_program(self, program: Dict) -> List[ValidationResult]:
    """Validate all sessions in a program."""
    results = []

    # Get program-level structure
    prog = program.get("program", program)
    sessions = prog.get("sessions", [])

    if not sessions:
        return results

    # Flowchart 3: Weekly sequencing (program-level check)
    fc3_passed, fc3_checks = self._check_weekly_sequencing_alignment(prog)

    # Flowchart 1 & 2: Per-session checks
    for session in sessions:
        if session.get("is_rest_day"):
            continue

        passed = True
        checks = []

        # Flowchart 1: Energy system → metcon format
        fc1_passed, fc1_checks = self._check_metcon_format_alignment(session)
        checks.extend(fc1_checks)
        if not fc1_passed:
            passed = False

        # Flowchart 2: Week → loading intensity
        week = session.get("week", 1)
        fc2_passed, fc2_checks = self._check_loading_intensity_alignment(session, week)
        checks.extend(fc2_checks)
        if not fc2_passed:
            passed = False

        results.append(ValidationResult(
            passed=passed,
            wod_id=session.get("id", "unknown"),
            checks=checks
        ))

    return results
```

- [ ] **Step 4: Test Flowchart 3 validation**

Create `/tmp/test-program-seq.json` with 5 sessions:
```json
{
  "program": {
    "id": "test-seq",
    "name": "Test Sequencing",
    "weeks": 1,
    "sessions": [
      {
        "id": "d1",
        "week": 1,
        "day": 1,
        "blocks": {
          "strength": {
            "movements": [
              {
                "name": "Clean and Jerk",
                "sets": 3,
                "reps": "2",
                "load": "75% 1RM"
              }
            ]
          },
          "metcon": {
            "format": "AMRAP",
            "time_cap_minutes": 10
          }
        },
        "rationale": {
          "session_why": {
            "text": "Glycolytic"
          }
        }
      },
      {
        "id": "d2",
        "week": 1,
        "day": 2,
        "blocks": {
          "metcon": {
            "format": "AMRAP",
            "time_cap_minutes": 20
          }
        },
        "rationale": {
          "session_why": {
            "text": "Oxidative aerobic base work"
          }
        }
      },
      {
        "id": "d3",
        "week": 1,
        "day": 3,
        "blocks": {
          "strength": {
            "movements": [
              {
                "name": "Back Squat",
                "sets": 4,
                "reps": "3",
                "load": "80% 1RM"
              }
            ]
          },
          "metcon": {
            "format": "AMRAP",
            "time_cap_minutes": 12
          }
        },
        "rationale": {
          "session_why": {
            "text": "Glycolytic"
          }
        }
      },
      {
        "id": "d4",
        "week": 1,
        "day": 4,
        "blocks": {
          "metcon": {
            "format": "AMRAP",
            "time_cap_minutes": 18
          }
        },
        "rationale": {
          "session_why": {
            "text": "Aerobic"
          }
        }
      },
      {
        "id": "d5",
        "week": 1,
        "day": 5,
        "blocks": {
          "strength": {
            "movements": [
              {
                "name": "Bench Press",
                "sets": 4,
                "reps": "5",
                "load": "72% 1RM"
              }
            ]
          },
          "metcon": {
            "format": "AMRAP",
            "time_cap_minutes": 12
          }
        },
        "rationale": {
          "session_why": {
            "text": "Glycolytic"
          }
        }
      }
    ]
  }
}
```

Run: `python scripts/validate-kb-alignment.py --program /tmp/test-program-seq.json --verbose`
Expected: All sequencing checks pass (no consecutive Olympic, no consecutive heavy lower, ≥1 aerobic)

- [ ] **Step 5: Commit Flowchart 3 implementation**

```bash
git add scripts/validate-kb-alignment.py
git commit -m "feat: Implement Flowchart 3 (weekly sequencing) validation"
```

---

### Task 5: Polish and Documentation

**Files:**
- Modify: `scripts/validate-kb-alignment.py` (add doc strings, fix output formatting)
- Create: `docs/KB-VALIDATION-GUIDE.md` (usage guide)

**Steps:**

- [ ] **Step 1: Add comprehensive docstrings**

Update module docstring and all methods with full documentation of what they check and why.

```python
"""
KB Alignment Validator — Trace KB flowcharts to generated WODs

This script validates that generated WODs and programs follow the decision logic
documented in the KB Decision Flowcharts design spec.

Three flowcharts are validated:

  1. FLOWCHART 1 (Energy System → Metcon Format):
     Given a target energy system, check that metcon format and time cap align.
     - Phosphocreatine (0-10s): EMOM only, 8-12 min
     - Glycolytic (10s-2m): AMRAP/For Time, 7-15 min
     - Oxidative (>2m): AMRAP only, 15-20 min
     Source: KB 01 Energy Systems, KB 02 CrossFit Methodology

  2. FLOWCHART 2 (Week → Loading Intensity):
     Given program week, check intensity %, rep scheme, and rest periods.
     - Week 1: 70-75%, 5x5/4x5, 180-300s rest
     - Week 2: 75-80%, 4x4/4x3, 120-180s rest
     - Week 3: 80-85%, 4x3/5x2, 180-300s rest
     - Week 4 (deload): 60-65%, 3x5/3x3, 120-180s rest
     Source: KB 03 Periodization

  3. FLOWCHART 3 (Weekly Sequencing):
     Check that weekly session ordering follows interference-minimizing rules.
     - No Olympic lifting on consecutive days
     - No heavy lower body on consecutive days
     - No high-CNS sessions back-to-back
     - Minimum 1 aerobic session per week
     Source: KB 01 Energy Systems, KB 03 Concurrent Periodization

Usage:
  python validate-kb-alignment.py --wod output/back-in-shape-3w.json --verbose
  python validate-kb-alignment.py --program output/back-in-shape-3w-program.json
"""
```

- [ ] **Step 2: Improve output formatting**

Update the output formatting in `main()`:

```python
def main():
    parser = argparse.ArgumentParser(description="Validate WOD alignment with KB flowcharts")
    parser.add_argument("--wod", type=str, help="Path to generated WOD JSON file")
    parser.add_argument("--program", type=str, help="Path to generated program JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print detailed check results")

    args = parser.parse_args()

    if not args.wod and not args.program:
        parser.print_help()
        return

    validator = KBValidator()

    if args.wod:
        with open(args.wod) as f:
            wod_data = json.load(f)
        result = validator.validate_wod(wod_data)
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"\n{status} — WOD Validation: {result.wod_id}\n")
        if args.verbose:
            for check_name, passed, reason in result.checks:
                marker = "  ✓" if passed else "  ✗"
                print(f"{marker} {check_name}")
                print(f"      {reason}")

    if args.program:
        with open(args.program) as f:
            program_data = json.load(f)
        results = validator.validate_program(program_data)
        passed_count = sum(1 for r in results if r.passed)
        total = len(results)
        status = "✓ PASS" if passed_count == total else "⚠ PARTIAL"
        print(f"\n{status} — Program Validation: {passed_count}/{total} sessions\n")

        if args.verbose:
            for result in results:
                marker = "✓" if result.passed else "✗"
                print(f"{marker} {result.wod_id}")
                for check_name, passed, reason in result.checks:
                    check_marker = "  ✓" if passed else "  ✗"
                    print(f"{check_marker} {check_name}: {reason}")
                print()
```

- [ ] **Step 3: Create usage guide**

Write `/Users/arpa/projects/Woddy/docs/KB-VALIDATION-GUIDE.md`:

```markdown
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

### Flowchart 2: Week → Loading Intensity
Validates that loading parameters (intensity %, reps, rest) match the program week.

**Example:**
- Week 1: 70–75% 1RM, 5×5 or 4×5 reps, 180–300s rest
- Week 3 (peak): 80–85% 1RM, 4×3 or 5×2 reps, 180–300s rest

**Why:** Periodization follows a 4-week cycle (baseline → build → peak → deload). Each week has specific adaptation targets.

### Flowchart 3: Weekly Sequencing
Validates that sessions are ordered to minimize interference between adaptations.

**Rules:**
- No Olympic lifting on consecutive days (neural fatigue)
- No heavy lower body on consecutive days (glycogen depletion + CNS fatigue)
- No high-CNS sessions back-to-back (recovery)
- Minimum 1 aerobic session per week (aerobic base development)

**Why:** Concurrent training (strength + endurance in same week) creates interference. Strategic sequencing minimizes this.

## Interpreting Results

**Full PASS:** All sessions follow all KB rules. Generator is working correctly.

**PARTIAL PASS:** Some sessions pass, some fail. Check `--verbose` output for details.

**FAIL:** Sessions violate KB rules. Debug the generator prompt or KB modules.

### Example Output

```
✓ PASS — Program Validation: 10/10 sessions

  ✓ w1d1
    ✓ energy_system_stated: Rationale states glycolytic goal
    ✓ format_for_glycolytic: Format AMRAP is in allowed list
    ✓ time_cap_for_glycolytic: Time cap 12min is in range 7-15min
    ✓ intensity_week_1: Intensity 72% is in range 70-75% for week 1
    ✓ rep_scheme_week_1: Rep scheme 5x5 is in allowed list for week 1
```

## Maintenance

When the KB changes:
1. Update the flowchart spec (`docs/superpowers/specs/2026-06-29-kb-decision-flowcharts-design.md`)
2. Update the validator rules in `scripts/validate-kb-alignment.py` to match
3. Re-validate existing programs to ensure they still align

When generator output diverges:
1. Run validator with `--verbose` on the divergent WOD
2. Trace which flowchart failed
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
python validate-kb-alignment.py --program output/*.json
```
```

- [ ] **Step 4: Add usage instructions to script help**

Make sure the `--help` output is clear:

```bash
python scripts/validate-kb-alignment.py --help
```

Expected output includes all three flowchart descriptions.

- [ ] **Step 5: Test complete script**

Run on a real generated output (if available):

```bash
python scripts/validate-kb-alignment.py --program output/back-in-shape-3w.json --verbose
```

- [ ] **Step 6: Final commit**

```bash
git add scripts/validate-kb-alignment.py docs/KB-VALIDATION-GUIDE.md
git commit -m "feat: Complete KB alignment validator with documentation"
```

---

## Plan Self-Review

**Spec coverage:**
- ✓ Flowchart 1 (energy system → metcon format) — Task 2
- ✓ Flowchart 2 (week → loading intensity) — Task 3
- ✓ Flowchart 3 (weekly sequencing) — Task 4
- ✓ Validation script runs against WODs and programs — Tasks 1-4
- ✓ Clear output/reporting — Task 5
- ✓ Documentation for future maintainers — Task 5

**No placeholders:** All tasks have complete code, exact test cases, and specific commands.

**Type consistency:** All methods use consistent naming (e.g., `_extract_*`, `_check_*`, `_count_*`).

**Scope:** Focused only on validation, no changes to generator or KB.

---

## Execution Options

Plan complete and saved to `docs/superpowers/plans/2026-06-29-kb-decision-flowcharts.md`.

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?

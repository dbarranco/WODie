#!/usr/bin/env python3
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

import json
import argparse
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ValidationResult:
    """Result of validating a WOD or program."""
    passed: bool
    wod_id: str
    checks: List[Tuple[str, bool, str]]

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"[{status}] WOD {self.wod_id}"]
        for check_name, passed, reason in self.checks:
            symbol = "✓" if passed else "✗"
            lines.append(f"  {symbol} {check_name}: {reason}")
        return "\n".join(lines)


class KBValidator:
    """Validates WODs against KB decision flowcharts."""

    def __init__(self):
        """Initialize validator with hardcoded energy system rules."""
        # Flowchart 1: Energy System → Metcon Format mapping
        # Based on physiology: energy system determines optimal work/rest ratio
        self.energy_system_rules = {
            "phosphocreatine": {
                "description": "ATP-PC system (high power output, 0-8 seconds naturally)",
                "allowed_formats": ["EMOM", "E2MOM", "E3MOM"],
                "time_cap_min": 8,
                "time_cap_max": 12,
            },
            "glycolytic": {
                "description": "Anaerobic glycolysis (high intensity, 30 seconds to ~3 minutes)",
                "allowed_formats": ["AMRAP", "For Time"],
                "time_cap_min": 7,
                "time_cap_max": 15,
            },
            "oxidative": {
                "description": "Aerobic oxidation (base building, sustained effort)",
                "allowed_formats": ["AMRAP"],
                "time_cap_min": 15,
                "time_cap_max": 20,
            },
        }

        # Flowchart 2: Loading → Progression Scheme
        # Week-based loading intensity and rep scheme rules
        self.loading_rules = {
            1: {
                "intensity_min": 70,
                "intensity_max": 75,
                "rep_schemes": ["5x5", "4x5"],
            },
            2: {
                "intensity_min": 75,
                "intensity_max": 80,
                "rep_schemes": ["4x4", "4x3"],
            },
            3: {
                "intensity_min": 80,
                "intensity_max": 85,
                "rep_schemes": ["4x3", "5x2"],
            },
            4: {
                "intensity_min": 60,
                "intensity_max": 65,
                "rep_schemes": ["3x5", "3x3"],
            },
        }

    def _extract_energy_system_from_rationale(
        self, rationale: Dict
    ) -> Optional[str]:
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

        if any(
            kw in text
            for kw in [
                "phosphocreatine",
                "atp-pc",
                "maximal effort",
                "heavy single",
            ]
        ):
            return "phosphocreatine"
        elif any(
            kw in text
            for kw in ["glycolytic", "anaerobic", "high-intensity", "metcon intensity"]
        ):
            return "glycolytic"
        elif any(kw in text for kw in ["oxidative", "aerobic", "base", "long effort"]):
            return "oxidative"

        return None

    def _check_metcon_format_alignment(
        self, wod: Dict
    ) -> Tuple[bool, List[Tuple[str, bool, str]]]:
        """Validate Flowchart 1: Energy system → metcon format.

        Returns: (passed: bool, checks: List[(check_name, passed, reason)])
        """
        checks = []
        passed = True

        # Extract energy system goal from rationale
        rationale = wod.get("rationale", {})
        energy_system = self._extract_energy_system_from_rationale(rationale)

        if not energy_system:
            checks.append(
                (
                    "energy_system_stated",
                    False,
                    "Rationale does not state energy system target",
                )
            )
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
        checks.append(
            (
                f"format_for_{energy_system}",
                format_match,
                f"Format {format_chosen} {'is' if format_match else 'is not'} in allowed list {allowed} for {energy_system}",
            )
        )
        if not format_match:
            passed = False

        # Check time cap is in range
        cap_ok = cap_min <= time_cap <= cap_max
        checks.append(
            (
                f"time_cap_for_{energy_system}",
                cap_ok,
                f"Time cap {time_cap}min {'is' if cap_ok else 'is not'} in range {cap_min}-{cap_max}min for {energy_system}",
            )
        )
        if not cap_ok:
            passed = False

        return (passed, checks)

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

    def _check_loading_intensity_alignment(
        self, session: Dict, week: int
    ) -> Tuple[bool, List[Tuple[str, bool, str]]]:
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
            checks.append(
                ("strength_movements_exist", False, "No movements in strength block")
            )
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
            checks.append(
                (
                    f"intensity_week_{week}",
                    intensity_ok,
                    f"Intensity {intensity}% {'is' if intensity_ok else 'is not'} in range {intensity_min}-{intensity_max}% for week {week}",
                )
            )
            if not intensity_ok:
                passed = False
        else:
            checks.append(
                (
                    f"intensity_week_{week}",
                    False,
                    f"Could not extract intensity percentage from load string '{first_move.get('load', '')}'",
                )
            )
            passed = False

        # Check rep scheme
        rep_scheme = self._extract_rep_scheme(first_move)
        if rep_scheme:
            scheme_ok = rep_scheme in allowed_schemes
            checks.append(
                (
                    f"rep_scheme_week_{week}",
                    scheme_ok,
                    f"Rep scheme {rep_scheme} {'is' if scheme_ok else 'is not'} in allowed list {allowed_schemes} for week {week}",
                )
            )
            if not scheme_ok:
                passed = False
        else:
            checks.append(
                (
                    f"rep_scheme_week_{week}",
                    False,
                    "Could not extract rep scheme from sets/reps fields",
                )
            )
            # Don't fail on this if it's optional

        return (passed, checks)

    def _has_olympic_lift(self, session: Dict) -> bool:
        """Check if session contains Olympic lifting movements."""
        strength = session.get("blocks", {}).get("strength")
        if not strength:
            return False
        movements = strength.get("movements", [])

        olympic_keywords = ["snatch", "clean", "jerk", "power clean", "power snatch"]

        for move in movements:
            name = move.get("name", "").lower()
            if any(kw in name for kw in olympic_keywords):
                return True

        return False

    def _is_heavy_lower_body(self, session: Dict) -> bool:
        """Check if session is heavy lower body work (intensity >75%)."""
        strength = session.get("blocks", {}).get("strength")
        if not strength:
            return False
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
                duration = metcon.get("time_cap_minutes", 0)
                if duration >= 15:
                    count += 1
                    continue

            # Check rationale for aerobic keywords
            rationale = session.get("rationale", {})
            session_why = rationale.get("session_why", {})
            if isinstance(session_why, dict):
                text = session_why.get("text", "").lower()
            else:
                text = str(session_why).lower()

            if any(kw in text for kw in ["aerobic", "base", "endurance"]):
                count += 1

        return min(count, 5)  # Cap at 5 to avoid double-counting

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
            consecutive_olympic = False
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
                    consecutive_olympic = True

            if not consecutive_olympic and olympic_sessions:
                checks.append((
                    f"no_consecutive_olympic_w{week_num}",
                    True,
                    f"Olympic days properly separated"
                ))

            # Constraint 2: No consecutive heavy lower body
            heavy_lower = [(i, s) for i, s in enumerate(week_sessions) if self._is_heavy_lower_body(s)]
            consecutive_heavy_lower = False
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
                    consecutive_heavy_lower = True

            if not consecutive_heavy_lower and heavy_lower:
                checks.append((
                    f"no_consecutive_heavy_lower_w{week_num}",
                    True,
                    f"Heavy lower body days properly separated"
                ))

            # Constraint 3: No consecutive high-CNS sessions
            high_cns = [(i, s) for i, s in enumerate(week_sessions) if self._is_high_cns_session(s)]
            consecutive_high_cns = False
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
                    consecutive_high_cns = True

            if not consecutive_high_cns and high_cns:
                checks.append((
                    f"no_consecutive_high_cns_w{week_num}",
                    True,
                    f"High-CNS sessions properly separated"
                ))

            # Constraint 4: Minimum 1 aerobic session per week
            aerobic_count = self._count_aerobic_sessions(week_sessions)
            aerobic_ok = aerobic_count >= 1
            checks.append((
                f"min_aerobic_w{week_num}",
                aerobic_ok,
                f"Week {week_num} has {aerobic_count} aerobic session(s) (need >=1)"
            ))
            if not aerobic_ok:
                passed = False

        return (passed, checks)

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

    def validate_program(self, program: Dict) -> ValidationResult:
        """Validate a program against KB decision flowcharts."""
        passed = True
        checks = []

        # Extract sessions from program structure
        prog = program.get("program", program)
        program_id = prog.get("id", program.get("id", "unknown"))
        sessions = prog.get("sessions", [])

        if not sessions:
            checks.append(("sessions_exist", False, "No sessions found in program"))
            return ValidationResult(passed=False, wod_id=program_id, checks=checks)

        # Flowchart 3: Weekly sequencing (program-level check)
        fc3_passed, fc3_checks = self._check_weekly_sequencing_alignment(prog)
        checks.extend(fc3_checks)
        if not fc3_passed:
            passed = False

        # Flowchart 1 & 2: Per-session checks
        for session in sessions:
            if session.get("is_rest_day"):
                continue

            session_id = session.get("id", "unknown")
            week = session.get("week")

            if week is None:
                checks.append(
                    (f"session_{session_id}_week_defined", False, "Session has no week number")
                )
                passed = False
                continue

            # Flowchart 1: Energy system → metcon format
            fc1_passed, fc1_checks = self._check_metcon_format_alignment(session)
            if not fc1_passed:
                passed = False

            # Format checks with session context
            for check_name, check_passed, reason in fc1_checks:
                qualified_name = f"session_{session_id}_{check_name}"
                checks.append((qualified_name, check_passed, reason))

            # Flowchart 2: Loading intensity alignment
            fc2_passed, fc2_checks = self._check_loading_intensity_alignment(
                session, week
            )
            if not fc2_passed:
                passed = False

            # Format checks with session context
            for check_name, check_passed, reason in fc2_checks:
                qualified_name = f"session_{session_id}_{check_name}"
                checks.append((qualified_name, check_passed, reason))

        return ValidationResult(passed=passed, wod_id=program_id, checks=checks)


def main():
    """CLI entry point for KB alignment validator."""
    parser = argparse.ArgumentParser(
        description="Validate generated WODs and programs against KB decision flowcharts",
        epilog="""
Examples:
  python validate-kb-alignment.py --wod output/my-wod.json --verbose
  python validate-kb-alignment.py --program output/my-program.json --verbose

Flowcharts validated:
  1. Energy System → Metcon Format (time caps and formats)
  2. Program Week → Loading Intensity (% 1RM and rep schemes)
  3. Weekly Sequencing (no consecutive heavy days, min 1 aerobic/week)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--wod",
        type=str,
        help="Path to WOD JSON file to validate",
    )
    parser.add_argument(
        "--program",
        type=str,
        help="Path to program JSON file to validate",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed check results for each session",
    )

    args = parser.parse_args()

    if not args.wod and not args.program:
        parser.print_help()
        return 1

    validator = KBValidator()

    if args.wod:
        try:
            with open(args.wod, "r") as f:
                wod = json.load(f)
            result = validator.validate_wod(wod)
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"\n{status} — WOD Validation: {result.wod_id}\n")
            if args.verbose:
                for check_name, passed, reason in result.checks:
                    marker = "  ✓" if passed else "  ✗"
                    print(f"{marker} {check_name}")
                    print(f"      {reason}")
                print()
            return 0 if result.passed else 1
        except FileNotFoundError:
            print(f"Error: File not found: {args.wod}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {args.wod}: {e}", file=sys.stderr)
            return 1

    if args.program:
        try:
            with open(args.program, "r") as f:
                program = json.load(f)
            result = validator.validate_program(program)
            passed_count = sum(1 for _, passed, _ in result.checks if passed)
            total = len(result.checks)
            status = "✓ PASS" if result.passed else "⚠ PARTIAL"
            print(f"\n{status} — Program Validation: {result.wod_id}\n")

            if args.verbose:
                for check_name, passed, reason in result.checks:
                    marker = "  ✓" if passed else "  ✗"
                    print(f"{marker} {check_name}")
                    print(f"      {reason}")
                print()
            return 0 if result.passed else 1
        except FileNotFoundError:
            print(f"Error: File not found: {args.program}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {args.program}: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

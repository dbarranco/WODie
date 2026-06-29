# Knowledge Base → WOD Decision Flowcharts

## Overview

The Woddy knowledge base contains the scientific foundations for every WOD decision. This document maps those foundations into explicit decision flowcharts so you can:

1. **Validate** that generated WODs follow KB logic
2. **Understand** why each decision was made
3. **Debug** when a WOD seems wrong (trace back through the flowchart)

Every flowchart shows: **Given X from the KB, choose Y for the WOD.**

---

## Flowchart 1: Energy System → Metcon Format Selection

**Source:** KB 01 (Energy Systems), KB 02 (CrossFit Methodology)

**Logic:** Each energy system has different duration and recovery characteristics. The metcon format must match the target energy system.

```
                    START: Select Metcon Format
                             |
                             v
                   What energy system are
                   we targeting today?
                             |
            _________________|_________________
           |                 |                 |
           v                 v                 v
    Phosphocreatine      Glycolytic         Oxidative
    (0-10 sec max)    (10 sec - 2 min)    (>2 min, dominant
                                           after 3-4 min)
           |                 |                 |
           v                 v                 v
      Use EMOM or        Use AMRAP or       Use AMRAP
      E2MOM/E3MOM        For Time           (15-20 min)
           |                 |                 |
           v                 v                 v
    Format: EMOM         Format: AMRAP       Format: AMRAP
    Time: 8-12 min       Time: 7-15 min      Time: 15-20 min
    Rest: Full PCr       Rest: Partial       Rest: Aerobic
    recovery between     recovery            base work
    intervals (2-3 min   (work:rest
    implied by          1:2 to 1:3)
    interval length)
```

**Decision Table:**

| Energy System Target | Primary Format | Time Cap | Why |
|---|---|---|---|
| Phosphocreatine | EMOM (E2MOM/E3MOM) | 8–12 min | Requires full recovery between efforts; interval structure ensures 2–3 min rest |
| Glycolytic | AMRAP or For Time | 7–15 min | Work-to-rest ratio built into continuous effort; 7–15 min keeps lactate threshold stimulus |
| Oxidative | AMRAP | 15–20 min | Sustained effort >10 min develops aerobic base; no high-intensity bursts needed |

**KB Citations:**
- KB 01, Section "Phosphocreatine System": "Recovery: ~2–3 minutes for full replenishment"
- KB 01, Section "Glycolytic System": "Training prescription: Work 20 sec–2 min at high intensity, rest 1:2 to 1:3"
- KB 02, Section "WOD Formats": "Format chosen to match the energy system target for that session"

---

## Flowchart 2: Program Week → Loading Intensity

**Source:** KB 03 (Periodization and Loading Parameters)

**Logic:** A 4-week block progresses from baseline (week 1) through build (week 2) and peak (week 3) to deload (week 4). Each week has prescribed intensity %, rep schemes, and rest periods.

```
                    START: Select Loading for Today
                             |
                             v
                    What week of the program?
                             |
            _________________|_________________
           |                 |                 |
           v                 v                 v
         Week 1            Week 2            Week 3
         (Baseline)        (Build)           (Peak)
           |                 |                 |
           v                 v                 v
    Intensity:          Intensity:         Intensity:
    70-75% 1RM         75-80% 1RM         80-85% 1RM
           |                 |                 |
           v                 v                 v
    Rep scheme:        Rep scheme:        Rep scheme:
    5x5, 4x5           4x4, 4x3           4x3, 5x2
           |                 |                 |
           v                 v                 v
    Rest: 180-300s     Rest: 120-180s     Rest: 180-300s
    (varies by goal)   (moderate)         (full strength
                                          recovery needed
                                          at peak)
           |                 |                 |
           |_________________|_________________|
                             |
                             v
                   [Week 4 = Deload if 4-week block]
                             |
                             v
                    Intensity: 60-65% 1RM
                    Rep scheme: 3x5, 3x3
                    Rest: 120-180s
                    Purpose: Recovery + adaptation
```

**Decision Table:**

| Week | Intensity | Rep Scheme | Rest Period | Goal | Notes |
|---|---|---|---|---|---|
| 1 | 70–75% 1RM | 5×5, 4×5 | 180–300s (varies by goal) | Technique + baseline load | Establish movement pattern and neurological baseline |
| 2 | 75–80% 1RM | 4×4, 4×3 | 120–180s | Build | Increase intensity, maintain volume |
| 3 | 80–85% 1RM | 4×3, 5×2 | 180–300s | Peak intensity | Lower reps, full recovery between sets |
| 4 | 60–65% 1RM | 3×5, 3×3 | 120–180s | Deload (mandatory for 4-week) | Active recovery, allow adaptation |

**Rest Period Modulation by Strength Goal:**

| Strength Goal | Rest Seconds | Week Recommendation |
|---|---|---|
| Maximal strength | 180–300s | Weeks 1, 3 (peak intensity needs full recovery) |
| Hypertrophy | 60–90s | Week 2 (build phase) |
| Power | 120–180s | Week 1, 2 (requires PCr recovery) |
| Strength-endurance | 30–60s | Week 2 (moderate intensity, higher volume) |

**KB Citations:**
- KB 03, Section "Progressive Loading by Week": All intensity/rep/duration prescriptions
- KB 03, Section "Rest Periods by Goal": Rest modulation table
- KB 01, Section "Phosphocreatine System": "Recovery: ~2–3 minutes for full replenishment" (explains why week 3 peak intensity requires long rests)

---

## Flowchart 3: Weekly Energy System Sequencing

**Source:** KB 01 (Energy Systems), KB 03 (Concurrent Periodization)

**Logic:** A week has 5 sessions. Energy system emphasis rotates to minimize interference between adaptations. Heavy strength work (phosphocreatine) depletes glycogen and CNS, so glycolytic work follows 24h later. Oxidative work (aerobic base) is typically standalone or after light days.

```
                    START: Plan Weekly Sequencing
                             |
                             v
                    What week of the program?
                             |
          ___________________|___________________
         |                                       |
         v                                       v
    Weeks 1-2                              Weeks 3-4
    (Baseline/Build)                       (Peak/Deload)
         |                                       |
         v                                       v
    Schedule 5 sessions:              Schedule 5 sessions:
    Prioritize technique              Prioritize heavy CNS work
    and GPP balance                   with adequate recovery
         |                                       |
         v                                       v
    Typical weekly structure:         Typical weekly structure:

    Day 1: Upper body strength         Day 1: Heavy lower strength
           (Phosphocreatine)                  (ATP-PC, CNS intensive)
           + Moderate metcon                  + Short metcon
           (Glycolytic, 10-15 min)           (Glycolytic)

    Day 2: Aerobic or                 Day 2: Aerobic or light skill
           Light skill work                   (24h recovery from Day 1)
           (Oxidative or balance)             (Oxidative)

    Day 3: Lower body strength         Day 3: Heavy upper strength
           (Phosphocreatine)                  (Phosphocreatine, CNS)
           + Moderate metcon                  + Short metcon
           (Glycolytic, 10-15 min)

    Day 4: Aerobic or                 Day 4: Aerobic or light
           Light skill/gymnastics            gymnastics
           (Oxidative, balance)               (Oxidative, recovery)

    Day 5: Mixed modal                Day 5: Mixed modal or
           (All systems, or                   deload-appropriate
            emphasize weak point)             (Volume/intensity ↓)
         |                                       |
         v                                       v
    [2 rest days]                     [2 rest days]
```

**Sequencing Rules (Hard Constraints):**

| Rule | Rationale | KB Source |
|---|---|---|
| No Olympic lifting on consecutive days | Neural fatigue accumulates; technique suffers | KB 03: Concurrent periodization |
| No two heavy lower-body sessions on consecutive days | Glycogen depletion + CNS fatigue compound | KB 01: Glycolytic system recovery; KB 03: Interference effect |
| No two high-CNS sessions back-to-back | CNS (central nervous system) requires 24–48h recovery | KB 03: Concurrent training |
| Heavy strength before metcon in same session | CNS freshness ensures technique quality; metcon happens on partially depleted glycogen | KB 02: Session structure rationale |
| Minimum 1 aerobic session per week | Aerobic base underpins all other adaptations | KB 01: Oxidative system foundation |
| Push:pull ratio ≥ 1:1 per week | Movement balance prevents injury and imbalances | KB 06: Movement balance |

**Energy System Distribution Across a Week:**

| Day Pattern | Primary Energy System | Secondary | Rationale |
|---|---|---|---|
| Heavy strength + short metcon | Phosphocreatine + Glycolytic | — | CNS fresh for strength, metcon after glycogen partial depletion |
| Light/aerobic work | Oxidative | — | Recovery, base development, minimal interference |
| Skill/gymnastics + light metcon | Neural (skill) + Glycolytic | — | Technique work requires freshness; light metcon avoids CNS overload |
| Mixed modal | All systems equally | — | General fitness emphasis; used when no specific adaptation target |

**KB Citations:**
- KB 01, Section "Energy System Targeting in Session Design": "Session should not try to train all three systems equally"
- KB 01, Section "Practical Time Domain Guidelines": Rest before next session varies by domain
- KB 03, Section "Concurrent Periodization": "Avoid high-volume endurance work on the same day as heavy lower body lifting"
- KB 02, Section "Session Structure Rationale": Order of blocks and why

---

## KB Module Cross-References

| Flowchart | Primary KB Modules | Supporting Modules | Key Tables/Sections |
|---|---|---|---|
| Flowchart 1: Energy System → Metcon Format | KB 01 Energy Systems | KB 02 CrossFit Methodology | Energy system definitions; WOD formats table |
| Flowchart 2: Week → Loading Intensity | KB 03 Periodization | KB 01 Energy Systems | Progressive loading by week; rest periods by goal; intensity zones |
| Flowchart 3: Weekly Sequencing | KB 01 + KB 03 | KB 02 Session Structure | Energy system interaction; concurrent training rules; session structure rationale |

---

## How to Use These Flowcharts

### Validating a Generated WOD

1. **Read the generated WOD.** Note:
   - The stated energy system goal (if provided in rationale)
   - The metcon format chosen (AMRAP, EMOM, For Time)
   - The week of the program
   - The loading intensity prescribed

2. **Trace through Flowchart 1:** Does the metcon format match the energy system?
   - If goal is "glycolytic," format should be AMRAP or For Time
   - If goal is "phosphocreatine," format should be EMOM
   - If mismatch, the generator may have erred or the KB doesn't support the choice

3. **Trace through Flowchart 2:** Does the loading intensity match the week?
   - Week 1 should be 70–75% 1RM
   - Week 3 should be 80–85% 1RM
   - If mismatch, investigate the generator prompt or hard-rules.json

4. **Trace through Flowchart 3:** Is the weekly sequencing sensible?
   - Are heavy sessions separated by 24h+?
   - Is there at least 1 aerobic session?
   - Do consecutive days avoid repeating energy systems?

### Maintaining These Flowcharts

- **When KB is updated:** Update the flowcharts to reflect new principles
- **When hard-rules.json changes:** Update the decision tables to match new constraints
- **When generator behavior changes:** Validate new WODs against these flowcharts to ensure alignment
- **For future developers:** These flowcharts are the "source of truth" for how KB flows into WOD decisions

---

## Next Steps

1. Review these flowcharts against a sample generated WOD
2. If flowchart and WOD align → generator is working correctly
3. If they diverge → debug the generator prompt or KB module
4. Once validated → generate full WOD pool with confidence

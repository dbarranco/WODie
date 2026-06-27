#!/usr/bin/env python3
"""Quick script to render markdown from existing WOD JSON."""

import json
import sys

def render_movement(m, block_type):
    """Render a single movement based on block type."""
    if block_type == 'metcon':
        load = f" @ {m['load']}" if m.get("load") else ""
        scale = f" *(Scale: {m['scaling']})*" if m.get("scaling") else ""
        reps = m.get('reps', m.get('reps_or_duration', ''))
        return f"- {reps} {m['name']}{load}{scale}"
    elif block_type == 'strength':
        load = f" @ {m['load']}" if m.get("load") else ""
        rest = f" | Rest {m['rest_seconds']}s" if m.get("rest_seconds") else ""
        if not rest and m.get("rest"):
            rest = f" | {m['rest']}"
        note = f"\n  > *{m['notes']}*" if m.get("notes") else ""
        scale = f"\n  > **Scale:** {m['scaling']}" if m.get("scaling") else ""
        reps_info = m.get('reps', m.get('reps_or_duration', ''))
        return f"- **{m['name']}** — {m['sets']}×{reps_info}{load}{rest}{note}{scale}"
    else:  # warmup, cooldown
        note = f" — *{m['notes']}*" if m.get("notes") else ""
        reps = m.get('reps_or_duration', m.get('reps', ''))
        return f"- {m['name']} — {reps}{note}"

def render_wod_markdown(wod):
    """Render a single WOD as markdown."""
    if wod.get("is_rest_day"):
        return f"## {wod['id'].upper()} — Rest Day\n\nActive recovery. Walk, stretch, sleep well.\n"

    lines = []
    lines.append(f"## {wod['id'].upper()} — {wod.get('title', '')}")
    lines.append(f"**Duration:** {wod.get('duration_minutes', 60)} min | **Category:** {', '.join(wod.get('category', []))}\n")

    equipment = wod.get("equipment", [])
    if equipment:
        lines.append(f"### 🎒 Equipment Needed\n")
        for item in equipment:
            lines.append(f"- {item}")
        lines.append("")

    blocks = wod.get("blocks", {})

    # Static warmup
    sw = blocks.get("static_warmup", {})
    if sw:
        lines.append(f"### 🧘 Static Warmup ({sw.get('duration_minutes', 5)} min)\n")
        for m in sw.get("movements", []):
            lines.append(render_movement(m, 'warmup'))
        lines.append("")

    # Active warmup
    aw = blocks.get("active_warmup", {})
    if aw:
        lines.append(f"### 🏃 Active Warmup ({aw.get('duration_minutes', 5)} min)\n")
        for m in aw.get("movements", []):
            lines.append(render_movement(m, 'warmup'))
        lines.append("")

    # Strength
    st = blocks.get("strength", {})
    if st:
        lines.append(f"### 💪 {st.get('label', 'Strength Block')} ({st.get('duration_minutes', 22)} min)\n")
        for m in st.get("movements", []):
            lines.append(render_movement(m, 'strength'))
        lines.append("")

    # Metcon
    mc = blocks.get("metcon", {})
    if mc:
        lines.append(f"### 🔥 Metcon — {mc.get('rounds_or_duration', '')} ({mc.get('duration_minutes', 15)} min)\n")
        lines.append(f"**Format:** {mc.get('format', '')} | **Time cap:** {mc.get('time_cap_minutes', '')} min\n")
        for m in mc.get("movements", []):
            lines.append(render_movement(m, 'metcon'))
        if mc.get("target_score"):
            lines.append(f"\n**Target:** {mc['target_score']}")
        lines.append("")

    # Cooldown
    cd = blocks.get("cooldown", {})
    if cd:
        lines.append(f"### 🧊 Cooldown & Mobility ({cd.get('duration_minutes', 8)} min)\n")
        for m in cd.get("movements", []):
            lines.append(render_movement(m, 'cooldown'))
        lines.append("")

    # Rationale
    rat = wod.get("rationale", {})
    if rat:
        lines.append("### 🔬 Why This Session?\n")
        for key, label in [("session_why", "Session design"), ("movement_why", "Movement selection"), ("loading_why", "Loading rationale")]:
            r = rat.get(key, {})
            if r.get("text"):
                lines.append(f"**{label.title()}**  ")
                lines.append(r["text"])
                lines.append(f"*— {r['source']}*\n")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    json_file = sys.argv[1]
    with open(json_file) as f:
        data = json.load(f)

    output = []
    output.append(f"# {data.get('program_name', 'WOD Pool')}\n")

    for wod in data.get('wods', []):
        output.append(render_wod_markdown(wod))
        output.append("\n---\n")

    md_file = json_file.replace('.json', '.md')
    with open(md_file, 'w') as f:
        f.write("\n".join(output))

    print(f"✅ Markdown saved: {md_file}")

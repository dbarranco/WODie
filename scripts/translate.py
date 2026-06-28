#!/usr/bin/env python3
"""
Translate generated English programs and WODs to Spanish.
Reads from docs/data/ and writes to docs/data-es/

Usage:
  python3 scripts/translate.py --language es
"""

import json
import os
import sys
import argparse
from pathlib import Path
import anthropic

# Initialize Anthropic client
client = anthropic.Anthropic()

def load_knowledge_base():
    """Load knowledge base for context."""
    kb_files = [
        'knowledge-base/01-energy-systems.md',
        'knowledge-base/02-crossfit-methodology.md',
        'knowledge-base/03-periodization.md',
        'knowledge-base/04-recovery.md',
        'knowledge-base/05-gymnastics.md',
    ]

    content = ""
    for file in kb_files:
        path = f'../{file}'
        if os.path.exists(path):
            with open(path, 'r') as f:
                content += f.read() + "\n\n"

    return content

def load_hard_rules():
    """Load hard rules for context."""
    with open('../data/hard-rules.json', 'r') as f:
        return json.load(f)

def translate_json_content(content_str, language):
    """Call Claude to translate JSON content to target language."""
    system_prompt = [
        {
            "type": "text",
            "text": """You are an expert CrossFit coach and translator. Your task is to translate workout programs and WODs from English to the target language.

CRITICAL REQUIREMENTS:
1. Translate ALL text fields naturally (movement names, descriptions, rationales, session titles)
2. Keep acronyms in English (AMRAP, EMOM, RPE, etc.) - this is standard in fitness
3. Keep numerical values, percentages, and loading schemes UNCHANGED
4. Preserve JSON structure exactly - only translate string values
5. Maintain technical accuracy for all exercise descriptions
6. Preserve all citations and sources as-is
7. Return ONLY valid JSON, no explanations

Target language: Spanish (es)

Translate all text while preserving the exact JSON schema.""",
            "cache_control": {"type": "ephemeral"}
        }
    ]

    user_message = f"""Translate this JSON to Spanish. Keep all structure, IDs, numbers, and JSON formatting identical. Only translate the text content.

{content_str}"""

    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.content[0].text

def translate_file(input_path, output_path):
    """Translate a single JSON file."""
    print(f"Translating: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        # Translate via Claude
        translated_str = translate_json_content(content, 'es')

        # Parse and validate JSON
        translated_json = json.loads(translated_str)

        # Write to output
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translated_json, f, ensure_ascii=False, indent=2)

        print(f"  ✅ Translated to: {output_path}")
        return True

    except json.JSONDecodeError as e:
        print(f"  ❌ JSON parse error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Translate generated content to Spanish')
    parser.add_argument('--language', default='es', choices=['es'], help='Target language')
    args = parser.parse_args()

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print(f"🌍 Translating to {args.language}")
    print("=" * 50)

    # Source and target directories
    src_base = '../docs/data'
    tgt_base = f'../docs/data-{args.language}'

    success_count = 0
    fail_count = 0

    # Translate programs
    programs_dir = os.path.join(src_base, 'programs')
    if os.path.exists(programs_dir):
        print("\n📋 PROGRAMS")
        for filename in os.listdir(programs_dir):
            if filename.endswith('.json'):
                src_path = os.path.join(programs_dir, filename)
                tgt_path = os.path.join(tgt_base, 'programs', filename)
                if translate_file(src_path, tgt_path):
                    success_count += 1
                else:
                    fail_count += 1

    # Translate WODs
    wods_dir = os.path.join(src_base, 'wods')
    if os.path.exists(wods_dir):
        print("\n💪 WODS")
        for filename in os.listdir(wods_dir):
            if filename.endswith('.json'):
                src_path = os.path.join(wods_dir, filename)
                tgt_path = os.path.join(tgt_base, 'wods', filename)
                if translate_file(src_path, tgt_path):
                    success_count += 1
                else:
                    fail_count += 1

    print("\n" + "=" * 50)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")

    if fail_count == 0:
        print(f"\n🎉 All files translated to {args.language}!")

    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())

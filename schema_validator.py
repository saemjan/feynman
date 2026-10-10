#!/usr/bin/env python3
"""
Pre-flight Schema and CSV Spec Validator.
Ensures compliance with extended Feynman & PYQ schema structure.
"""

import csv
import sys


def validate_csv(filepath: str):
    print(f"[INFO] Validating schema for {filepath}...")
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required_fields = {"video_id", "concept_type", "header_title", "audio_script"}
            if not required_fields.issubset(reader.fieldnames or []):
                print(f"[FATAL] Missing required CSV columns. Found: {reader.fieldnames}")
                sys.exit(1)

            row_count = 0
            for row in reader:
                row_count += 1
                words = row["audio_script"].split()
                word_count = len(words)
                if not (90 <= word_count <= 160):
                    print(f"[WARN] Row {row_count} ({row['video_id']}): Script word count ({word_count}) outside optimal range.")
        print(f"[SUCCESS] Schema validation passed for {row_count} rows.")
    except Exception as e:
        print(f"[FATAL] CSV validation crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "content_batch.csv"
    validate_csv(target)

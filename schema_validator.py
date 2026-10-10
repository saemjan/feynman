#!/usr/bin/env python3
"""
Pre-flight CSV & Schema Validation Script.
Ensures data integrity before parallel GitHub Actions workers execute.
"""

import os
import csv
import json
import sys

REQUIRED_COLUMNS = [
    "video_id", "concept_type", "header_title", "tagline",
    "question_text", "option_a", "option_b", "option_c", "option_d",
    "correct_answer", "equations_json", "visual_data_json", "audio_script"
]

def validate_csv(file_path):
    print(f"[INFO] Validating schema for: {file_path}")
    if not os.path.exists(file_path):
        print(f"::error file={file_path}::CSV file missing.")
        sys.exit(1)

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # 1. Check Columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in fieldnames]
        if missing_cols:
            print(f"::error::Missing required columns in CSV: {missing_cols}")
            sys.exit(1)

        row_count = 0
        for i, row in enumerate(reader, start=1):
            row_count += 1
            vid = row.get("video_id", f"row_{i}")

            # 2. Validate Equations JSON
            eq_str = row.get("equations_json", "[]")
            try:
                json.loads(eq_str)
            except json.JSONDecodeError as e:
                print(f"::error::Invalid JSON in 'equations_json' at row {i} ({vid}): {e}")
                sys.exit(1)

            # 3. Validate Visual Data JSON
            vis_str = row.get("visual_data_json", "[]")
            try:
                json.loads(vis_str)
            except json.JSONDecodeError as e:
                print(f"::error::Invalid JSON in 'visual_data_json' at row {i} ({vid}): {e}")
                sys.exit(1)

            # 4. Check Audio Script length
            script = row.get("audio_script", "")
            if len(script.split()) < 10:
                print(f"::warning::Audio script for {vid} is very short ({len(script.split())} words).")

    print(f"[SUCCESS] Pre-flight checklist passed! Validated {row_count} rigorous physics specifications.")

if __name__ == "__main__":
    csv_target = os.environ.get("TARGET_CSV", "feynman_batch1.csv")
    validate_csv(csv_target)

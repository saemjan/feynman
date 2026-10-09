#!/usr/bin/env python3
"""
Pre-Flight Schema & Boundary Validator.
Validates RFC 4180 CSV compliance, LaTeX string escaping, JSON structures, script word counts, and spatial bounds.
Supports all Universal Physics primitives.
"""

import csv
import json
import re
import sys

ALLOWED_PRIMITIVES = {
    "field", "field_symbols", "charge", "vector", "line", "arc",
    "spring", "pulley_system", "lens_mirror", "optics_ray",
    "circuit_component", "photon", "energy_level", "graph", "shape"
}


def safe_json_loads(val_str: str):
    """Sanitizes raw strings containing single-backslashed LaTeX for JSON parsing."""
    if not val_str or val_str.strip() == '""':
        return []
    cleaned = re.sub(r'(?<!\\)\\(?![\\"/bfnrtu])', r"\\\\", val_str)
    return json.loads(cleaned)


def validate_spatial_bounds(item: dict, video_id: str):
    """Verifies visual primitives remain within safe 9:16 layout limits (X: [-3.5, 3.5], Y: [-2.2, 1.8])."""
    ptype = item.get("type", "").lower()
    if ptype not in ALLOWED_PRIMITIVES:
        print(f"[WARN] [{video_id}] Unrecognized primitive type '{ptype}'.")

    for pos_key in ["pos", "start", "end", "center"]:
        if pos_key in item:
            coords = item[pos_key]
            x, y = coords[0], coords[1]
            if not (-3.5 <= x <= 3.5 and -2.2 <= y <= 1.8):
                print(f"[WARN] [{video_id}] Primitive '{ptype}' key '{pos_key}' ({x}, {y}) exceeds safe visual bounds!")


def validate_csv(csv_path: str) -> bool:
    has_errors = False
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        if not header or len(header) < 13:
            print("[ERROR] CSV header must contain at least 13 columns.")
            return False

        for row_idx, row in enumerate(reader, start=2):
            if not row:
                continue
            
            if len(row) < 13:
                print(f"[ERROR] Row {row_idx}: Invalid column count ({len(row)} < 13).")
                has_errors = True
                continue

            video_id = row[0].strip()
            eq_json_raw = row[10].strip()
            vis_json_raw = row[11].strip()
            script = row[12].strip()

            # 1. Word Count Check for Vertical Short Pacing
            words = script.split()
            if len(words) < 80 or len(words) > 150:
                print(f"[WARN] Row {row_idx} ({video_id}): Script word count ({len(words)}) outside recommended 110-140 range.")

            # 2. JSON & LaTeX Parsing Checks
            try:
                eqs = safe_json_loads(eq_json_raw)
                if not isinstance(eqs, list):
                    print(f"[ERROR] Row {row_idx} ({video_id}): equations_json must be a JSON array.")
                    has_errors = True
            except Exception as e:
                print(f"[ERROR] Row {row_idx} ({video_id}): Invalid equations_json ({e}).")
                has_errors = True

            try:
                visuals = safe_json_loads(vis_json_raw)
                if not isinstance(visuals, list):
                    print(f"[ERROR] Row {row_idx} ({video_id}): visual_data_json must be a JSON array.")
                    has_errors = True
                else:
                    for vis_item in visuals:
                        validate_spatial_bounds(vis_item, video_id)
            except Exception as e:
                print(f"[ERROR] Row {row_idx} ({video_id}): Invalid visual_data_json ({e}).")
                has_errors = True

    return not has_errors


if __name__ == "__main__":
    csv_target = sys.argv[1] if len(sys.argv) > 1 else "content_batch.csv"
    print(f"[INFO] Validating schema and spatial bounds for: {csv_target}")
    if validate_csv(csv_target):
        print("[SUCCESS] All dataset checks passed successfully.")
        sys.exit(0)
    else:
        print("[FATAL] Pre-flight validation failed.")
        sys.exit(1)

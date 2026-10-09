#!/usr/bin/env python3
"""
Master Orchestration Engine.
Reads content_batch.csv, validates script constraints, triggers audio synthesis & Manim render,
and stitches final video with FFmpeg.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from wave import open as wave_open
from schema_validator import validate_csv, safe_json_loads


def get_wav_duration(wav_path: str) -> float:
    """Calculates exact duration in seconds of a WAV file."""
    with wave_open(wav_path, 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def sanitize_filename(name: str) -> str:
    """Removes unsafe filesystem characters."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '', name)


def parse_csv_file(csv_file: str):
    """Parses input CSV file supporting 13 and 15 column variations robustly."""
    rows = []
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 13:
                continue
            
            row_dict = {
                "video_id": row[0].strip(),
                "concept_type": row[1].strip(),
                "header_title": row[2].strip(),
                "tagline": row[3].strip(),
                "question_text": row[4].strip(),
                "option_a": row[5].strip(),
                "option_b": row[6].strip(),
                "option_c": row[7].strip(),
                "option_d": row[8].strip(),
                "correct_answer": row[9].strip(),
                "equations_json": row[10].strip(),
                "visual_data_json": row[11].strip(),
                "audio_script": row[12].strip(),
            }
            rows.append(row_dict)
    return rows


def run_pipeline_for_row(row: dict, output_dir: str, dry_run: bool = False):
    video_id = sanitize_filename(row["video_id"])
    script = row["audio_script"]
    word_count = len(script.split())

    print(f"\n==================================================")
    print(f" Processing: {video_id} ({word_count} words)")
    print(f" Header: {row['header_title']}")
    print(f"==================================================")

    if dry_run:
        safe_json_loads(row["equations_json"])
        safe_json_loads(row["visual_data_json"])
        print("[DRY-RUN] Syntax validated.")
        return True

    os.makedirs(output_dir, exist_ok=True)
    temp_audio = os.path.join(output_dir, f"{video_id}_audio.wav")
    temp_video = os.path.join(output_dir, f"{video_id}_raw.mp4")
    final_output = os.path.join(output_dir, f"{video_id}.mp4")

    # Step 1: Synthesize Audio
    audio_cmd = [
        sys.executable, "generate_audio.py",
        "--video_id", video_id,
        "--script", script,
        "--output", temp_audio
    ]
    subprocess.run(audio_cmd, check=True)
    duration = get_wav_duration(temp_audio) + 2.0  # Add 2s end-card pause

    # Step 2: Extract Options Array
    options_arr = [row[f"option_{ch}"] for ch in ["a", "b", "c", "d"] if row[f"option_{ch}"]]

    # Step 3: Render Manim Visuals
    render_cmd = [
        sys.executable, "render_universal.py",
        "--video_id", video_id,
        "--header_title", row["header_title"],
        "--tagline", row["tagline"],
        "--question_text", row["question_text"],
        "--options_json", json.dumps(options_arr),
        "--correct_answer", row["correct_answer"],
        "--equations_json", row["equations_json"],
        "--visual_data_json", row["visual_data_json"],
        "--duration", str(duration),
        "--output", temp_video
    ]
    subprocess.run(render_cmd, check=True)

    # Step 4: FFmpeg Audio-Video Stitching
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", temp_audio,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output
    ]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for temp_f in [temp_audio, temp_video]:
        if os.path.exists(temp_f):
            os.remove(temp_f)

    print(f"[COMPLETE] Final short generated: {final_output}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch Pipeline Runner")
    parser.add_argument("--csv", default="content_batch.csv", help="Input CSV file")
    parser.add_argument("--output_dir", default="dist", help="Output directory for MP4s")
    parser.add_argument("--dry-run", action="store_true", help="Validate CSV and JSON schemas without rendering")
    parser.add_argument("--only", help="Comma-separated list of video_ids to process")
    parser.add_argument("--shard-index", type=int, default=0, help="Matrix worker index (0-N)")
    parser.add_argument("--shard-total", type=int, default=1, help="Total matrix workers")
    args = parser.parse_args()

    if not validate_csv(args.csv):
        print("[FATAL] CSV validation failed. Aborting pipeline execution.", file=sys.stderr)
        sys.exit(1)

    rows = parse_csv_file(args.csv)

    if args.only:
        target_ids = set(args.only.split(","))
        rows = [r for r in rows if r["video_id"] in target_ids]

    if args.shard_total > 1:
        rows = [r for idx, r in enumerate(rows) if idx % args.shard_total == args.shard_index]

    print(f"[INFO] Loaded {len(rows)} video jobs for worker {args.shard_index + 1}/{args.shard_total}.")

    success_count = 0
    failed_count = 0
    for row in rows:
        try:
            if run_pipeline_for_row(row, args.output_dir, dry_run=args.dry_run):
                success_count += 1
        except Exception as e:
            failed_count += 1
            print(f"[ERROR] Job failed for {row.get('video_id')}: {e}", file=sys.stderr)

    print(f"\n[FINISHED] Processed {success_count}/{len(rows)} videos successfully.")
    if failed_count > 0:
        print(f"[FATAL] {failed_count} job(s) failed during execution.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

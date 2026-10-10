#!/usr/bin/env python3
"""
Parallel Shard Batch Runner.
Distributes video rendering across worker shards and compiles output shorts.
"""

import argparse
import csv
import json
import os
import subprocess
import sys


def run_job(row: dict, output_path: str):
    video_id = row["video_id"]
    title = row["header_title"]
    script = row["audio_script"]

    print(f"\n========================================")
    print(f"Processing: {video_id} ({len(script.split())} words)")
    print(f"Header: {title}")
    print(f"========================================")

    audio_wav = f"{output_path}_audio.wav"
    
    # 1. Generate Voiceover
    audio_cmd = [
        sys.executable, "generate_audio.py",
        "--video_id", video_id,
        "--script", script,
        "--output", audio_wav
    ]
    subprocess.run(audio_cmd, check=True)

    # 2. Render Manim Animation
    env = os.environ.copy()
    env["CURRENT_VIDEO_ID"] = video_id
    env["CURRENT_TITLE"] = title
    env["EQUATIONS_JSON"] = row.get("equations_json", "[]")
    env["VISUAL_DATA_JSON"] = row.get("visual_data_json", "[]")

    manim_cmd = [
        sys.executable, "-m", "manim",
        "render_universal.py", "ElitePhysicsScene",
        "-ql", "--media_dir", "media"
    ]
    subprocess.run(manim_cmd, env=env, check=True)
    print(f"[SUCCESS] Completed job for {video_id}")


def main():
    parser = argparse.ArgumentParser(description="Batch Worker Runner")
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-total", type=int, required=True)
    parser.add_argument("--output_dir", default="dist")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    jobs = []
    with open("content_batch.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append(row)

    shard_jobs = [job for i, job in enumerate(jobs) if i % args.shard_total == args.shard_index]
    print(f"[INFO] Loaded {len(shard_jobs)} video jobs for worker {args.shard_index + 1}/{args.shard_total}.")

    for job in shard_jobs:
        out_base = os.path.join(args.output_dir, job["video_id"])
        run_job(job, out_base)

    print(f"[FINISHED] Processed {len(shard_jobs)} videos successfully.")


if __name__ == "__main__":
    main()

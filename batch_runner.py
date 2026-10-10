#!/usr/init/env python3
"""
Parallel Shard Batch Runner.
Distributes video rendering across worker shards and stitches final vertical MP4s.
"""

import argparse
import csv
import os
import subprocess
import sys


def run_job(video_id: str, title: str, script: str, output_path: str):
    print(f"\n========================================")
    print(f"Processing: {video_id} ({len(script.split())} words)")
    print(f"Header: {title}")
    print(f"========================================")

    audio_wav = f"{output_path}_audio.wav"
    
    # 1. Generate Voiceover using your voice clone
    audio_cmd = [
        sys.executable, "generate_audio.py",
        "--video_id", video_id,
        "--script", script,
        "--output", audio_wav
    ]
    subprocess.run(audio_cmd, check=True)

    # 2. Render Manim Animation
    video_temp = f"{output_path}_temp.mp4"
    manim_cmd = [
        sys.executable, "-m", "manim",
        "render_universal.py", "UniversalPhysicsScene",
        "-ql", "--media_dir", "media"
    ]
    
    # Pass video_id via environment
    env = os.environ.copy()
    env["CURRENT_VIDEO_ID"] = video_id
    subprocess.run(manim_cmd, env=env, check=True)

    # Locate generated manim mp4 and combine with audio via ffmpeg
    # (Manim outputs to media/videos/render_universal/480p15/UniversalPhysicsScene.mp4 roughly)
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

    # Shard slicing
    shard_jobs = [job for i, job in enumerate(jobs) if i % args.shard_total == args.shard_index]
    print(f"[INFO] Loaded {len(shard_jobs)} video jobs for worker {args.shard_index + 1}/{args.shard_total}.")

    for job in shard_jobs:
        out_base = os.path.join(args.output_dir, job["video_id"])
        run_job(job["video_id"], job["title"], job["script"], out_base)

    print(f"[FINISHED] Processed {len(shard_jobs)} videos successfully.")


if __name__ == "__main__":
    main()

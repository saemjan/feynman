#!/usr/bin/env python3
"""
Parallel Shard Batch Runner.
Compiles Manim animations, synthesizes voiceovers, and muxes video/audio via FFmpeg.
"""

import argparse
import csv
import glob
import os
import subprocess
import sys


def run_job(row: dict, output_dir: str):
    video_id = row["video_id"]
    title = row["header_title"]
    script = row["audio_script"]

    print(f"\n========================================")
    print(f"Processing: {video_id} ({len(script.split())} words)")
    print(f"Header: {title}")
    print(f"========================================")

    os.makedirs(output_dir, exist_ok=True)
    audio_wav = os.path.join(output_dir, f"{video_id}_audio.wav")
    final_output_mp4 = os.path.join(output_dir, f"{video_id}.mp4")
    
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

    # 3. Locate Manim's rendered output file
    search_pattern = os.path.join("media", "videos", "**", "*.mp4")
    rendered_files = glob.glob(search_pattern, recursive=True)
    
    if not rendered_files:
        raise FileNotFoundError(f"Manim failed to generate any output mp4 files for {video_id}")

    latest_video = max(rendered_files, key=os.path.getmtime)

    # 4. Mux Video and Audio via FFmpeg
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", latest_video,
        "-i", audio_wav,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output_mp4
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    print(f"[SUCCESS] Compiled final short at: {final_output_mp4}")


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
        run_job(job, args.output_dir)

    print(f"[FINISHED] Processed {len(shard_jobs)} videos successfully.")


if __name__ == "__main__":
    main()

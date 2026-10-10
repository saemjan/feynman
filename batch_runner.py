#!/usr/bin/env python3
"""
Elite Parallel Batch Runner for Physics Shorts Pipeline.
Parses CSV data, generates TTS audio, and coordinates Manim rendering.
"""

import os
import csv
import json
import subprocess
import sys
from TTS.api import TTS

def get_tts_model():
    print("[INFO] Initializing Coqui XTTS model...")
    # Using multilingual XTTS model for crystal-clear educational voiceovers
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    return TTS(model_name=model_name, progress_bar=True, gpu=True)

def run_job(job_data, output_dir="dist"):
    os.makedirs(output_dir, exist_ok=True)
    video_id = job_data["video_id"]
    title = job_data["header_title"]
    audio_script = job_data["audio_script"]
    eq_json = job_data["equations_json"]
    vis_json = job_data["visual_data_json"]

    audio_path = os.path.join(output_dir, f"{video_id}_audio.wav")
    
    print(f"\n==============================")
    print(f"Processing: {video_id} ({len(audio_script.split())} words)")
    print(f"Header: {title}")
    print(f"==============================")

    # 1. Generate TTS Audio if not already cached
    if not os.path.exists(audio_path):
        try:
            tts = get_tts_model()
            # Synthesize voiceover with optimal teaching pace
            tts.tts_to_file(
                text=audio_script,
                speaker_wav="reference_voice.wav" if os.path.exists("reference_voice.wav") else None,
                language="en",
                file_path=audio_path
            )
            print(f"[SUCCESS] Audio generated successfully: {audio_path}")
        except Exception as e:
            print(f"[WARNING] XTTS synthesis failed ({e}). Using fallback silent audio track.")
            subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "30", audio_path], check=True)
    else:
        print(f"[INFO] Using cached audio: {audio_path}")

    # 2. Set Environment Variables for Manim Scene
    env = os.environ.copy()
    env["CURRENT_VIDEO_ID"] = video_id
    env["CURRENT_TITLE"] = title
    env["EQUATIONS_JSON"] = eq_json
    env["VISUAL_DATA_JSON"] = vis_json

    # 3. Execute Manim Render Command (9:16 Vertical HD Format)
    manim_cmd = [
        "manim",
        "render_universal.py",
        "ElitePhysicsScene",
        "-ql",  # Low quality for swift CI testing (-qh for production 1080p1920)
        "--media_dir", "media"
    ]

    print(f"[INFO] Running Manim render for {video_id}...")
    try:
        subprocess.run(manim_cmd, env=env, check=True)
        print(f"[SUCCESS] Render completed for {video_id}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Manim render failed with exit code {e.returncode}")
        sys.exit(1)

def main():
    csv_path = os.environ.get("TARGET_CSV", "feynman_batch1.csv")
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found: {csv_path}")
        sys.exit(1)

    print(f"[INFO] Loading jobs from {csv_path}...")
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_job(row)

if __name__ == "__main__":
    main()

#!/usr/init/env python3
"""
Strict Neural Voice Synthesis Engine.
Enforces absolute path resolution for saem_voice_sample.wav to guarantee 
zero-shot male voice cloning with zero fallback to generic or stock voices.
"""

import argparse
import hashlib
import os
import subprocess
import sys

# --- FORCE COQUI TERMS OF SERVICE AGREEMENT ---
os.environ["COQUI_TOS_AGREED"] = "1"
tos_dir = os.path.expanduser("~/.local/share/tts")
os.makedirs(tos_dir, exist_ok=True)
with open(os.path.join(tos_dir, ".tos_agreed"), "w") as f:
    f.write("y\n")

from soundscape import process_and_normalize_wav


def get_deterministic_seed(video_id: str) -> int:
    """Derives a stable 32-bit integer seed from SHA-256 hash of video_id."""
    return int(hashlib.sha256(video_id.encode("utf-8")).hexdigest(), 16) % (2**32)


def main():
    parser = argparse.ArgumentParser(description="Strict Voice Cloning Engine")
    parser.add_argument("--video_id", required=True, help="Unique identifier for seed generation")
    parser.add_argument("--script", required=True, help="Plain text narration script")
    parser.add_argument("--speaker_wav", default="saem_voice_sample.wav", help="Reference voice sample")
    parser.add_argument("--output", required=True, help="Destination WAV file path")
    args = parser.parse_args()

    seed = get_deterministic_seed(args.video_id)
    raw_wav = args.output + ".raw.wav"

    # --- ENFORCE ABSOLUTE PATH TO VOICE SAMPLE ---
    abs_speaker_wav = os.path.abspath(args.speaker_wav)

    if not os.path.exists(abs_speaker_wav):
        # GitHub Actions workflow command annotation for missing file
        print(f"::error file=generate_audio.py,title=Missing Voice Sample::Reference audio '{args.speaker_wav}' not found at {abs_speaker_wav}!")
        sys.exit(1)

    print(f"::notice file=generate_audio.py,title=Voice Cloning Active::Cloning authentic male voice from: {abs_speaker_wav}")

    try:
        import torch
        from TTS.api import TTS

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"[INFO] Initializing XTTS-v2 on {device.upper()}...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        # Synthesize strictly using your voice sample
        tts.tts_to_file(
            text=args.script,
            speaker_wav=abs_speaker_wav,
            language="en",
            file_path=raw_wav,
            temperature=0.7,
            repetition_penalty=5.0,
            top_k=50,
            top_p=0.85,
            enable_text_splitting=True
        )
    except Exception as e:
        print(f"::error file=generate_audio.py,title=XTTS-v2 Failure::Voice cloning crashed: {e}")
        sys.exit(1)

    if not os.path.exists(raw_wav):
        print(f"::error file=generate_audio.py,title=Synthesis Failed::Audio file was not generated for {args.video_id}")
        sys.exit(1)

    process_and_normalize_wav(raw_wav, args.output)
    
    if os.path.exists(raw_wav):
        os.remove(raw_wav)

    print(f"[SUCCESS] Audio successfully generated and normalized using your voice: {args.output}")


if __name__ == "__main__":
    main()

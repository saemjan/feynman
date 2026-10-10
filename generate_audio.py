#!/usr/bin/env python3
"""
Strict Neural Voice Synthesis Engine.
Pre-authorizes Coqui TOS and clones the authentic voice from saem_voice_sample.wav.
"""

import argparse
import hashlib
import os
import sys

# Pre-authorize Coqui TOS agreement to prevent interactive hangs in CI/CD
os.environ["COQUI_TOS_AGREED"] = "1"
tos_dir = os.path.expanduser("~/.local/share/tts")
os.makedirs(tos_dir, exist_ok=True)
with open(os.path.join(tos_dir, ".tos_agreed"), "w") as f:
    f.write("y\n")

from soundscape import process_and_normalize_wav


def get_deterministic_seed(video_id: str) -> int:
    return int(hashlib.sha256(video_id.encode("utf-8")).hexdigest(), 16) % (2**32)


def main():
    parser = argparse.ArgumentParser(description="Strict Voice Synthesis Engine")
    parser.add_argument("--video_id", required=True)
    parser.add_argument("--script", required=True)
    parser.add_argument("--speaker_wav", default="saem_voice_sample.wav")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    seed = get_deterministic_seed(args.video_id)
    raw_wav = args.output + ".raw.wav"
    abs_speaker_wav = os.path.abspath(args.speaker_wav)

    if not os.path.exists(abs_speaker_wav):
        print(f"::error file=generate_audio.py,title=Missing Voice Sample::'{args.speaker_wav}' not found at {abs_speaker_wav}!")
        sys.exit(1)

    try:
        import torch
        from TTS.api import TTS

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"[INFO] Initializing XTTS-v2 on {device.upper()}...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

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
        print(f"::error file=generate_audio.py,title=XTTS-v2 Failed::Voice cloning error: {e}")
        sys.exit(1)

    if not os.path.exists(raw_wav):
        print(f"::error file=generate_audio.py,title=Fatal::Audio output missing.")
        sys.exit(1)

    process_and_normalize_wav(raw_wav, args.output)
    if os.path.exists(raw_wav):
        os.remove(raw_wav)

    print(f"[SUCCESS] Audio generated successfully: {args.output}")


if __name__ == "__main__":
    main()

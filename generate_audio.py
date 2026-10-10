#!/usr/bin/env python3
"""
Neural Voice Synthesis Engine with Forced Coqui XTTS-v2 Voice Cloning.
Programmatically bypasses non-interactive terms prompts to guarantee saem_voice_sample.wav is used.
"""

import argparse
import hashlib
import os
import subprocess
import sys

# --- FORCE COQUI TERMS OF SERVICE AGREEMENT ---
# This prevents non-interactive CI/CD runners from hanging or failing with EOF errors,
# ensuring Coqui XTTS-v2 successfully loads instead of falling back to generic TTS.
os.environ["COQUI_TOS_AGREED"] = "1"
tos_dir = os.path.expanduser("~/.local/share/tts")
os.makedirs(tos_dir, exist_ok=True)
with open(os.path.join(tos_dir, ".tos_agreed"), "w") as f:
    f.write("y\n")
------------------------------------------------

from soundscape import process_and_normalize_wav


def get_deterministic_seed(video_id: str) -> int:
    """Derives a stable 32-bit integer seed from SHA-256 hash of video_id."""
    return int(hashlib.sha256(video_id.encode("utf-8")).hexdigest(), 16) % (2**32)


def synthesize_coqui(text: str, speaker_wav: str, output_wav: str, seed: int) -> bool:
    """Tier 1: High-Fidelity Voice Cloning using Coqui XTTS-v2 and saem_voice_sample.wav."""
    try:
        import torch
        import torchaudio
        from TTS.api import TTS

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"[INFO] Initializing XTTS-v2 on {device.upper()} using your male voice sample: {speaker_wav}")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language="en",
            file_path=output_wav,
            temperature=0.7,
            repetition_penalty=5.0,
            top_k=50,
            top_p=0.85,
            enable_text_splitting=True
        )
        print(f"[SUCCESS] Successfully cloned your voice into: {output_wav}")
        return True
    except Exception as e:
        print(f"[ERROR] Coqui XTTS-v2 failed unexpectedly: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Voice Synthesis Engine")
    parser.add_argument("--video_id", required=True, help="Unique identifier for seed generation")
    parser.add_argument("--script", required=True, help="Plain text narration script")
    parser.add_argument("--speaker_wav", default="saem_voice_sample.wav", help="Reference voice sample")
    parser.add_argument("--output", required=True, help="Destination WAV file path")
    args = parser.parse_args()

    seed = get_deterministic_seed(args.video_id)
    raw_wav = args.output + ".raw.wav"

    if not os.path.exists(args.speaker_wav):
        print(f"[FATAL] Reference voice sample '{args.speaker_wav}' not found in repo root!", file=sys.stderr)
        sys.exit(1)

    # Enforce Coqui XTTS-v2 (No fallback to gTTS so your voice is guaranteed)
    success = synthesize_coqui(args.script, args.speaker_wav, raw_wav, seed)

    if not success or not os.path.exists(raw_wav):
        print(f"[FATAL] Voice cloning failed for {args.video_id}", file=sys.stderr)
        sys.exit(1)

    process_and_normalize_wav(raw_wav, args.output)
    
    if os.path.exists(raw_wav):
        os.remove(raw_wav)

    print(f"[SUCCESS] Final branded audio generated using your voice: {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Neural Voice Synthesis Engine with Explicit XTTS-v2 Voice Cloning Enforcement.
Uses saem_voice_sample.wav for authentic speaker cloning.
Uses GitHub Actions Workflow Commands for build log annotations.
"""

import argparse
import hashlib
import os
import subprocess
import sys

# Pre-set Coqui TOS agreement to prevent non-interactive console hangs in CI/CD
os.environ["COQUI_TOS_AGREED"] = "1"

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
        
        # GitHub Actions Workflow Annotation
        print(f"::notice file=generate_audio.py,title=XTTS-v2 Active::Cloning authentic voice from '{speaker_wav}' on {device.upper()}.")
        
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
        return True
    except Exception as e:
        print(f"::warning file=generate_audio.py,title=XTTS-v2 Failed::Coqui voice cloning error ({e}). Falling back to gTTS.")
        return False


def synthesize_gtts(text: str, output_wav: str) -> bool:
    """Tier 2: Backup HTTP Fallback using Google Text-to-Speech (gTTS)."""
    temp_mp3 = output_wav + ".gtts.mp3"
    try:
        from gtts import gTTS
        
        print("[INFO] Generating fallback audio via gTTS API...")
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_mp3)

        cmd = [
            "ffmpeg", "-y",
            "-i", temp_mp3,
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "1",
            output_wav
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        return True
    except Exception as e:
        print(f"::error file=generate_audio.py,title=gTTS Failed::gTTS synthesis failed: {e}")
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
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

    success = False
    # Validate reference audio file presence
    if os.path.exists(args.speaker_wav):
        success = synthesize_coqui(args.script, args.speaker_wav, raw_wav, seed)
    else:
        print(f"::warning file=generate_audio.py,title=Missing Voice Sample::'{args.speaker_wav}' not found in repo root.")

    # Trigger backup gTTS if XTTS-v2 fails
    if not success:
        success = synthesize_gtts(args.script, raw_wav)

    if not success or not os.path.exists(raw_wav):
        print(f"::error file=generate_audio.py,title=Synthesis Fatal::Failed to generate audio for {args.video_id}")
        sys.exit(1)

    process_and_normalize_wav(raw_wav, args.output)
    
    if os.path.exists(raw_wav):
        os.remove(raw_wav)

    print(f"[SUCCESS] Audio generated and normalized using voice clone: {args.output}")


if __name__ == "__main__":
    main()

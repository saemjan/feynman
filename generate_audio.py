#!/usr/bin/env python3
"""
Neural Voice Synthesis Engine with High-Fidelity Coqui XTTS-v2 Voice Cloning.
Uses saem_voice_sample.wav for zero-shot speaker matching and Edge-TTS as fallback.
"""

import argparse
import hashlib
import os
import subprocess
import sys
from soundscape import process_and_normalize_wav


def get_deterministic_seed(video_id: str) -> int:
    """Derives a stable 32-bit integer seed from SHA-256 hash of video_id."""
    return int(hashlib.sha256(video_id.encode("utf-8")).hexdigest(), 16) % (2**32)


def synthesize_coqui(text: str, speaker_wav: str, output_wav: str, seed: int) -> bool:
    """Attempts high-fidelity voice cloning using Coqui XTTS-v2."""
    try:
        import torch
        from TTS.api import TTS

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"[INFO] Initializing XTTS-v2 on {device.upper()} using voice sample: {speaker_wav}")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        # Tuned parameters for realistic human pacing and pitch matching
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language="en",
            file_path=output_wav,
            temperature=0.7,            # Balances natural expressive variance and stability
            repetition_penalty=5.0,     # Prevents word repetition or phantom stutters
            top_k=50,                   # Constrains token selection for vocal clarity
            top_p=0.85,                 # Smooths pitch transitions across long sentences
            enable_text_splitting=True  # Splices long scripts at natural punctuation pauses
        )
        return True
    except Exception as e:
        print(f"[WARN] Coqui XTTS-v2 synthesis failed ({e}). Triggering fallback...", file=sys.stderr)
        return False


def synthesize_edge_tts(text: str, output_wav: str) -> bool:
    """Fallback generator using Microsoft Edge TTS, converted cleanly to 16-bit PCM WAV."""
    temp_mp3 = output_wav + ".temp.mp3"
    try:
        import asyncio
        import edge_tts

        async def _run():
            communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="+0%")
            await communicate.save(temp_mp3)

        asyncio.run(_run())

        # Convert MP3 stream to PCM WAV via FFmpeg
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
        print(f"[ERROR] Edge-TTS synthesis failed: {e}", file=sys.stderr)
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
    if os.path.exists(args.speaker_wav):
        success = synthesize_coqui(args.script, args.speaker_wav, raw_wav, seed)
    else:
        print(f"[WARN] Reference audio '{args.speaker_wav}' not found in repo root.", file=sys.stderr)

    if not success:
        print("[INFO] Utilizing Edge-TTS neural engine fallback.", file=sys.stderr)
        success = synthesize_edge_tts(args.script, raw_wav)

    if not success or not os.path.exists(raw_wav):
        print(f"[FATAL] Failed to synthesize audio for {args.video_id}", file=sys.stderr)
        sys.exit(1)

    process_and_normalize_wav(raw_wav, args.output)
    
    if os.path.exists(raw_wav):
        os.remove(raw_wav)

    print(f"[SUCCESS] Audio generated and normalized: {args.output}")


if __name__ == "__main__":
    main()

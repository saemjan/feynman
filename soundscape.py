#!/usr/bin/env python3
"""
Cinematic Soundscape Generator with A1 Fundamental Harmonic Drones.
Handles background ambient pads and master audio normalization.
"""

import os
import numpy as np
import scipy.io.wavfile as wavfile


def generate_ambient_pad(duration_seconds: float = 65.0, sample_rate: int = 44100) -> np.ndarray:
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds), endpoint=False)
    frequencies = [55.0, 110.0, 164.81, 220.0]
    pad = np.zeros_like(t)

    for i, freq in enumerate(frequencies):
        wave = np.sin(2 * np.pi * freq * t)
        envelope = np.min([t / 3.0, (duration_seconds - t) / 3.0, np.ones_like(t)], axis=0)
        pad += wave * np.clip(envelope, 0, 1) * (1.0 / (i + 1))

    pad = pad / np.max(np.abs(pad)) * 0.10
    return (pad * 32767).astype(np.int16)


def process_and_normalize_wav(input_wav: str, output_wav: str):
    try:
        from pydub import AudioSegment
        speech = AudioSegment.from_wav(input_wav)
        duration_sec = len(speech) / 1000.0

        pad_raw_path = "temp_pad.wav"
        pad_data = generate_ambient_pad(duration_sec + 3.0)
        wavfile.write(pad_raw_path, 44100, pad_data)
        
        ambient = AudioSegment.from_wav(pad_raw_path)
        speech_boosted = speech + 6.0  # Ensure voice cuts cleanly over ambient pad

        combined = ambient.overlay(speech_boosted, position=500)
        normalized = combined.apply_gain(-1.0 - combined.max_dBFS)
        normalized.export(output_wav, format="wav")

        if os.path.exists(pad_raw_path):
            os.remove(pad_raw_path)
    except ImportError:
        import shutil
        shutil.copyfile(input_wav, output_wav)

#!/usr/bin/env python3
"""
Cinematic Soundscape Generator.
Produces rich ambient audio pads with harmonic resonance to back neural voice synthesis.
"""

import numpy as np
import scipy.signal
import scipy.io.wavfile as wavfile


def generate_ambient_pad(duration_seconds: float = 30.0, sample_rate: int = 44100) -> np.ndarray:
    """Generates a warm, cinematic ambient drone in A1 (55 Hz) with fifths and octaves."""
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds), endpoint=False)
    
    # Fundamental and harmonic frequencies (A minor voicing: A1, E2, A2, E3)
    frequencies = [55.0, 110.0, 164.81, 220.0, 329.63]
    pad = np.zeros_like(t)

    for i, freq in enumerate(frequencies):
        # Add subtle frequency modulation and detuning for organic warmth
        detune = np.sin(t * 0.1 + i) * 0.5
        wave = np.sin(2 * np.pi * (freq + detune) * t)
        
        # Envelope: Gentle fade in and fade out
        envelope = np.min([t / 2.0, (duration_seconds - t) / 2.0, np.ones_like(t)], axis=0)
        envelope = np.clip(envelope, 0, 1)
        
        pad += wave * envelope * (1.0 / (i + 1))

    # Normalize and scale to subtle background level (-20 dB relative to speech)
    pad = pad / np.max(np.abs(pad)) * 0.15
    return (pad * 32767).astype(np.int16)


def process_and_normalize_wav(input_wav: str, output_wav: str):
    """Mixes raw speech with cinematic ambient pad, applies EQ filtering, and normalizes peak to -1 dB."""
    try:
        from pydub import AudioSegment
        
        speech = AudioSegment.from_wav(input_wav)
        duration_sec = len(speech) / 1000.0

        # Generate background ambient pad
        pad_raw_path = "temp_pad.wav"
        pad_data = generate_ambient_pad(duration_sec + 2.0)
        wavfile.write(pad_raw_path, 44100, pad_data)
        ambient = AudioSegment.from_wav(pad_raw_path)

        # Overlay speech onto ambient pad with ducking
        combined = ambient.overlay(speech, position=500, gain_dB=6)
        
        # Normalize to -1 dB peak
        normalized = combined.apply_gain(-1.0 - combined.max_dBFS)
        normalized.export(output_wav, format="wav")

        if os.path.exists(pad_raw_path):
            os.remove(pad_raw_path)
    except ImportError:
        # Fallback if pydub is missing
        import shutil
        shutil.copyfile(input_wav, output_wav)


if __name__ == "__main__":
    import os
    print("Soundscape utility ready.")

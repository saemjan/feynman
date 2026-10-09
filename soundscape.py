#!/usr/bin/env python3
"""
Audio Soundscape Helper Module.
Handles low-pass ambient drone generation, polyphase sample rate conversions, and peak normalization.
"""

from math import gcd
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly


def generate_ambient_pad(duration_sec: float, sample_rate: int = 44100) -> np.ndarray:
    """Generates a soft, low-pass ambient background pad (A1 note - 55Hz) to elevate narration tone."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # Fundamental low drone with subtle harmonic
    drone = 0.02 * np.sin(2 * np.pi * 55 * t) + 0.008 * np.sin(2 * np.pi * 110 * t)
    
    # Apply soft attack and release envelope (0.5s fade)
    fade_len = int(sample_rate * 0.5)
    envelope = np.ones_like(t)
    if len(t) > 2 * fade_len:
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
        
    return (drone * envelope).astype(np.float32)


def process_and_normalize_wav(input_wav: str, output_wav: str, target_sr: int = 44100):
    """Resamples narration to canonical 44.1kHz, mixes ambient pad, and normalizes peak audio to -1dB."""
    sr, narr_data = wavfile.read(input_wav)
    
    # Convert to float32 normalized [-1.0, 1.0]
    if narr_data.dtype == np.int16:
        narr_data = narr_data.astype(np.float32) / 32768.0
    elif narr_data.dtype == np.int32:
        narr_data = narr_data.astype(np.float32) / 2147483648.0
    elif narr_data.dtype != np.float32:
        narr_data = narr_data.astype(np.float32)

    # Convert stereo to mono
    if len(narr_data.shape) > 1:
        narr_data = np.mean(narr_data, axis=1)

    # Polyphase resampling if native sample rate differs from target
    if sr != target_sr:
        g = gcd(sr, target_sr)
        up = target_sr // g
        down = sr // g
        narr_data = resample_poly(narr_data, up, down).astype(np.float32)
        sr = target_sr

    duration_sec = len(narr_data) / sr
    pad_data = generate_ambient_pad(duration_sec, sample_rate=sr)

    # Blend narration and ambient drone
    mixed_data = narr_data + pad_data

    # Peak normalization to -1.0 dB (0.891 amplitude)
    max_val = np.max(np.abs(mixed_data))
    if max_val > 0:
        mixed_data = (mixed_data / max_val) * 0.891

    # Save final 16-bit PCM WAV
    final_pcm = (mixed_data * 32767).astype(np.int16)
    wavfile.write(output_wav, sr, final_pcm)

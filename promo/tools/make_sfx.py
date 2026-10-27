"""Synthesize the promo's motion sound effects from scratch (no third-party samples,
so no licence questions), record each file's measured peak, and lay them on the
beat grid as a preview cue track.

Usage: python3 -I promo/tools/make_sfx.py
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sfx"
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env(dur, attack, release, curve=2.0):
    """Rise to 1 at `attack` seconds, then fall to 0 by `dur`."""
    t = t_axis(dur)
    up = np.clip(t / attack, 0, 1) ** curve
    down = np.clip((dur - t) / release, 0, 1) ** curve
    return np.minimum(up, down)


def swept_band(noise, lo, hi, q=1.2, steps=48):
    """Band-pass noise whose centre glides from lo to hi (Hz) across the clip."""
    out = np.zeros_like(noise)
    n = len(noise)
    edges = np.linspace(0, n, steps + 1).astype(int)
    win = np.hanning(2 * (edges[1] - edges[0]) + 2)
    for i in range(steps):
        f = lo * (hi / lo) ** (i / (steps - 1))
        bw = f / q
        sos = butter(2, [max(20, f - bw / 2), min(SR / 2 - 100, f + bw / 2)], "band", fs=SR, output="sos")
        a, b = max(0, edges[i] - (edges[1] - edges[0])), min(n, edges[i + 1] + (edges[1] - edges[0]))
        seg = sosfilt(sos, noise[a:b])
        w = np.interp(np.arange(a, b), [a, (a + b) / 2, b], [0, 1, 0])
        out[a:b] += seg * w
    return out


def whoosh(dur, lo, hi, attack, q=1.0):
    n = rng.standard_normal(int(dur * SR))
    return swept_band(n, lo, hi, q) * env(dur, attack, dur - attack)


def click(freq=2200, dur=0.07):
    t = t_axis(dur)
    tick = np.zeros_like(t)
    tick[:48] = rng.standard_normal(48) * np.linspace(1, 0, 48)
    tone = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.012)
    return sosfilt(butter(2, 900, "high", fs=SR, output="sos"), tick * 0.6 + tone * 0.5)


def thump(freq=58, dur=0.9, drop=0.6):
    t = t_axis(dur)
    f = freq * (1 + drop * np.exp(-t / 0.03))
    phase = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(phase) * np.exp(-t / 0.28)
    attack = np.minimum(t / 0.004, 1)
    return body * attack


def swell(freqs, dur, peak_at):
    t = t_axis(dur)
    tone = sum(np.sin(2 * np.pi * f * t) / (i + 1) for i, f in enumerate(freqs))
    e = np.where(t < peak_at, (t / peak_at) ** 2, np.exp(-(t - peak_at) / (dur - peak_at) * 4))
    return tone * e


def stereo(x, width=0.0):
    """Mono to stereo with an optional few-ms Haas offset for air."""
    d = int(width * SR)
    r = np.concatenate([np.zeros(d), x])[: len(x)] if d else x
    return np.stack([x, r], axis=1)


def norm(x, peak_db):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)


def peak_time(x):
    """Peak of the 10 ms RMS envelope: the moment the ear hears as the hit."""
    mono = x if x.ndim == 1 else x.mean(axis=1)
    w = int(0.01 * SR)
    rms = np.sqrt(np.convolve(mono ** 2, np.ones(w) / w, mode="same"))
    return float(np.argmax(rms) / SR)


SOUNDS = {
    # Bar 1, 4, 8: a soft air swish under each masked word reveal.
    "word_swish": lambda: stereo(norm(whoosh(0.32, 1800, 5200, 0.16, q=0.9), -6), 0.004),
    # Bar 2: the hook word melting into the UI.
    "morph": lambda: stereo(norm(whoosh(0.7, 400, 2600, 0.42, q=0.7), -6), 0.008),
    # Bar 2: cursor clicks (select files, pick WEBP, press convert).
    "ui_click": lambda: stereo(norm(click(), -4)),
    # Bar 2 -> 3: the circle opening out of the button, peaking on the drop.
    "riser": lambda: stereo(norm(whoosh(0.55, 300, 7000, 0.53, q=0.6), -5), 0.006),
    # Bar 3 downbeat: low body under the music's own drop.
    "drop_sub": lambda: stereo(norm(thump(52, 1.1, 0.8) + 0.15 * whoosh(1.1, 120, 400, 0.01), -3)),
    # Bar 3: scan line travelling down the clip wall.
    "scan": lambda: stereo(norm(whoosh(1.0, 3000, 900, 0.5, q=2.5), -12), 0.01),
    # Bar 3: each winner locking in.
    "lock": lambda: stereo(norm(click(3400, 0.09) + 0.4 * swell([1700], 0.09, 0.005), -6)),
    # Bar 4, 6: match cuts between shapes.
    "match": lambda: stereo(norm(whoosh(0.5, 600, 3200, 0.3, q=0.8), -6), 0.006),
    # Bar 5: the carousel turning.
    "carousel": lambda: stereo(norm(whoosh(1.5, 250, 1400, 1.0, q=0.6), -9), 0.012),
    # Bar 5: whip onto the hero clip.
    "whip": lambda: stereo(norm(whoosh(0.36, 700, 6000, 0.2, q=0.6), -3), 0.004),
    # Bar 6: the panel flipping over to the results.
    "flip": lambda: stereo(norm(np.concatenate([click(1400, 0.05), np.zeros(int(0.05 * SR))]) + 0.5 * whoosh(0.1, 1500, 4000, 0.04), -5)),
    # Bar 7: push cuts between stats.
    "push": lambda: stereo(norm(thump(70, 0.35, 0.5) + 0.6 * np.pad(whoosh(0.22, 900, 3000, 0.2), (0, int(0.13 * SR))), -4), 0.004),
    # Bar 9: logo reveal, a quiet tonal swell.
    "logo": lambda: stereo(norm(swell([392, 587.3, 784], 1.6, 0.45), -9), 0.01),
    # Bar 10: air falling away into black.
    "outro": lambda: stereo(norm(whoosh(1.4, 2400, 300, 0.12, q=0.7), -10), 0.012),
}

# (time on the beat grid in seconds, sound, gain dB). Mirrors promo/STORYBOARD.md.
CUES = [
    (0.0, "word_swish", -4), (0.5, "word_swish", -4), (1.0, "word_swish", -4), (1.5, "word_swish", -4),
    (2.0, "morph", -2), (2.5, "ui_click", -3), (3.0, "ui_click", -3), (3.5, "ui_click", 0),
    (4.0, "riser", -3), (4.0, "drop_sub", -6), (4.5, "scan", 0),
    (4.5, "lock", -2), (5.0, "lock", -2), (5.5, "lock", -2),
    (6.0, "match", -2), (6.0, "word_swish", -5), (6.5, "word_swish", -5), (7.0, "word_swish", -3),
    (9.0, "carousel", 0), (9.5, "whip", 0),
    (10.0, "match", -3), (11.0, "flip", 0),
    (12.0, "push", 0), (13.0, "push", 0),
    (14.0, "word_swish", -4), (14.5, "word_swish", -4), (15.0, "word_swish", -2),
    (16.0, "logo", 0),
    (18.5, "outro", 0),
]
LENGTH = 20.0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta, clips = {}, {}
    for name, make in SOUNDS.items():
        x = make().astype(np.float32)
        clips[name] = x
        meta[name] = {"file": f"{name}.wav", "duration": round(len(x) / SR, 4), "peak": round(peak_time(x), 4)}
        wavfile.write(OUT / f"{name}.wav", SR, x)
    (OUT / "sfx.json").write_text(json.dumps(meta, indent=2) + "\n")

    # Preview track: each sound placed so its measured peak, not its start, sits on the cue.
    mix = np.zeros((int(LENGTH * SR) + SR, 2), np.float32)
    for at, name, gain in CUES:
        x = clips[name] * 10 ** (gain / 20)
        start = int(round((at - meta[name]["peak"]) * SR))
        if start < 0:
            x, start = x[-start:], 0
        mix[start:start + len(x)] += x[: len(mix) - start]
    # Beat-grid metronome, very quiet, so the cue preview can be judged against the grid.
    for b in range(int(LENGTH * 2)):
        s = int(b * 0.5 * SR)
        tick = click(1000 if b % 4 else 1600, 0.03)[:, None] * (0.08 if b % 4 else 0.14)
        mix[s:s + len(tick)] += tick
    mix = mix[: int(LENGTH * SR)]
    mix *= 0.89 / np.max(np.abs(mix))
    wav = OUT / "cue_preview.wav"
    wavfile.write(wav, SR, mix)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "192k", str(OUT / "cue_preview.m4a")], check=True)
    wav.unlink()
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()

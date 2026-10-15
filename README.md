# GitSentinel EDR — Universal Threat Detection & Remediation System

GitSentinel is a next-generation Host-Based Endpoint Detection and Response (EDR) agent that protects developer workstations and enterprise systems from **Ransomware (WannaCry-style)**, **AI Sandbox & Runtime Escapes**, **"CTRL"-style Spyware & Surveillance**, **Network Worms**, **Binary Viruses**, and **Unauthorized Git/PR Tampering**.

---

## 🌟 Key Features

1. **Real-Time Behavioral Telemetry**: Continuous auditing of process lifecycle, parent trees, TTY status, and socket connections without heavy kernel modifications.
2. **Universal Threat Taxonomy**: Evaluates behavioral indicators across 8 core malware archetypes.
3. **Mutation & Zero-Day Detection**: Detects mutated or rebranded threats by analyzing *behavioral TTPs* rather than relying solely on static file signatures.
4. **Active vs. Passive Threat Profiler**: Differentiates active attacks (encryption bursts, subshell spawning) from passive surveillance (keylogging, screen capture).
5. **Automated Remediation Playbooks**: Provides step-by-step emergency disablement instructions and 1-click process quarantine (`SIGKILL`).
6. **Cross-Platform Compatibility**: Native desktop apps for **macOS, Windows, and Linux**, plus touch-optimized mobile web app for **iOS and Android**.

---

## 🚀 Quick Start

### 🍏 On macOS
Double-click `GitSentinel.app` or run:
```bash
python3 src/desktop_main.py
```

### 🪟 On Windows
Double-click `run_app.bat` or run:
```cmd
python src\desktop_main.py
```

### 🐧 On Linux
```bash
python3 src/desktop_main.py
```

### 🌐 Universal Web Dashboard & GUI
To start the web server accessible to any device on your Wi-Fi:
```bash
python3 Antigravity/run_gui.py
```
Open `http://localhost:5050` or the network IP printed in the terminal.

---

## 🔬 Benchmark & Test Suite
To simulate AI Sandbox Escapes, WannaCry Ransomware, Network Worms, and "CTRL" Spyware:
```bash
python3 Antigravity/test_universal_threats.py
```

---
*Created by Vatsal Agarwal | Academic Research & Engineering 2026-2027*

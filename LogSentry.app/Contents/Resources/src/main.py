"""
main.py - Universal Threat Detection & Remediation Engine.
Monitors system events, classifies Active vs Passive threats, identifies mutations,
and generates step-by-step remediation advice for Ransomware, Worms, Viruses, Spyware, AI Escapes, and C2.
"""
import sys
import os
import json
from typing import Dict, Any

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.profiler.behavior_engine import BehaviorEngine
from src.profiler.archetype_matcher import ArchetypeMatcher
from src.remediation.playbook_generator import PlaybookGenerator

class SentinelEngine:
    def __init__(self):
        self.behavior_engine = BehaviorEngine()
        self.archetype_matcher = ArchetypeMatcher()
        self.playbook_generator = PlaybookGenerator()

    def inspect_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inspects an event through the 3-stage intelligence pipeline:
        1. Behavior Profiler: Active vs Passive & Indicators
        2. Threat Classification & Mutation Matcher
        3. Step-by-Step Remediation Advisory
        """
        # Stage 1: Behavioral Profiling
        analysis = self.behavior_engine.analyze_event(event)

        # Early Warning Alert check
        if analysis["is_suspicious"]:
            print(f"\n[⚠️ EARLY WARNING ALERT] Suspicious system activity detected on PID {event.get('pid')} (Mode: {analysis['operational_mode']})")

        # Stage 2: Archetype & Mutation Matching
        classification = self.archetype_matcher.classify_threat(analysis, event)

        # Stage 3: Remediation Playbook Generation
        advisory_text = ""
        if classification["identified"]:
            advisory_text = self.playbook_generator.generate_advisory(classification, event)

        return {
            "behavior_analysis": analysis,
            "threat_classification": classification,
            "advisory_text": advisory_text
        }

if __name__ == "__main__":
    print("Log Sentry Universal Threat Detection & Remediation Engine initialized.")
    print("Ready to process system log streams and real-time telemetry.")

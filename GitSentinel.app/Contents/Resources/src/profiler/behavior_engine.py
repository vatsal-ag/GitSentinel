"""
behavior_engine.py - Core Behavioral Profiler for Universal Threat Detection.
Analyzes telemetry events, categorizes Active vs Passive threats, and extracts security indicators.
"""
from typing import Dict, List, Any

class BehaviorEngine:
    def __init__(self):
        # Indicators categorized into Active and Passive
        self.active_weights = {
            "file_encryption_burst": 35,
            "canary_tampered": 40,
            "shadow_copy_deletion": 30,
            "rapid_port_scanning": 40,
            "memory_injection": 45,
            "host_socket_tampering": 40,
            "unauthorized_subshell": 35,
            "reverse_shell_spawn": 45
        }
        self.passive_weights = {
            "credential_store_access": 35,
            "screen_or_input_capture": 35,
            "headless_browser_dump": 30,
            "periodic_beaconing": 25,
            "hidden_background_execution": 20
        }

    def analyze_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a raw system telemetry event.
        Returns:
            - matched_indicators: list of matched indicators
            - operational_mode: 'ACTIVE' or 'PASSIVE' or 'BENIGN'
            - initial_risk_score: 0-100
            - raw_context: extracted context (PID, binary, parent, path)
        """
        matched = []
        active_score = 0
        passive_score = 0

        cmd = str(event.get("cmd", "")).lower()
        path = str(event.get("path", "")).lower()
        parent = str(event.get("parent", "")).lower()
        is_interactive = event.get("is_interactive", True)

        # 1. Ransomware / Canary Checks
        if event.get("canary_tampered", False):
            matched.append("canary_tampered")
            active_score += self.active_weights["canary_tampered"]

        if event.get("file_write_rate", 0) > 10 or ".encrypted" in path or ".locked" in path:
            matched.append("file_encryption_burst")
            active_score += self.active_weights["file_encryption_burst"]

        if any(term in cmd for term in ["vssadmin", "tmutil delete", "wbadmin", "bcdedit"]):
            matched.append("shadow_copy_deletion")
            active_score += self.active_weights["shadow_copy_deletion"]

        # 2. Worm / Port Scanning Checks
        if event.get("connections_per_sec", 0) > 6 or any(term in cmd for term in ["masscan", "nmap -p 445", "smbclient"]):
            matched.append("rapid_port_scanning")
            active_score += self.active_weights["rapid_port_scanning"]

        # 3. AI Sandbox Escape Checks
        if any(sock in path or sock in cmd for sock in ["docker.sock", "host.docker.internal", "/proc/sys"]):
            matched.append("host_socket_tampering")
            active_score += self.active_weights["host_socket_tampering"]

        if any(p in parent for p in ["python", "node", "llm", "agent", "ollama"]) and any(sh in cmd for sh in ["bash -i", "/bin/sh", "powershell"]):
            if not is_interactive:
                matched.append("unauthorized_subshell")
                active_score += self.active_weights["unauthorized_subshell"]

        # 4. Reverse Shell / C2 Checks
        if any(pat in cmd for pat in ["/dev/tcp/", "nc -e", "bash -i >&", "powershell -nop -w hidden -enc"]):
            matched.append("reverse_shell_spawn")
            active_score += self.active_weights["reverse_shell_spawn"]

        # 5. Spyware / Infostealer Checks
        if any(target in path or target in cmd for target in [".ssh/id_rsa", "login data", "cookies", "keychains"]):
            matched.append("credential_store_access")
            passive_score += self.passive_weights["credential_store_access"]

        if any(api in cmd for api in ["screencapture", "coregraphics", "getasynckeystate", "setwindowshookex"]):
            matched.append("screen_or_input_capture")
            passive_score += self.passive_weights["screen_or_input_capture"]

        if not is_interactive:
            passive_score += self.passive_weights["hidden_background_execution"]

        total_score = min(100, active_score + passive_score)

        if active_score >= passive_score and active_score > 0:
            mode = "ACTIVE"
        elif passive_score > 0:
            mode = "PASSIVE"
        else:
            mode = "BENIGN"

        return {
            "matched_indicators": matched,
            "operational_mode": mode,
            "risk_score": total_score,
            "is_suspicious": total_score >= 30,
            "event_summary": {
                "pid": event.get("pid"),
                "cmd": event.get("cmd"),
                "parent": event.get("parent"),
                "user": event.get("user")
            }
        }

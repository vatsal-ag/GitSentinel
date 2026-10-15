"""
playbook_generator.py - Generates concrete, step-by-step remediation advice tailored to the specific threat.
"""
import platform
from typing import Dict, Any, List

class PlaybookGenerator:
    def __init__(self):
        self.os_type = platform.system().lower()  # 'darwin' (macOS) or 'windows' or 'linux'

    def generate_advisory(self, classification: Dict[str, Any], event: Dict[str, Any]) -> str:
        """
        Formats an emergency actionable response advisory for the user.
        """
        pid = event.get("pid", "UNKNOWN_PID")
        cmd = event.get("cmd", "Unknown Command")
        parent = event.get("parent", "Unknown Parent")
        family = classification.get("candidate_family", "Generic Threat")
        mode = classification.get("operational_mode", "ACTIVE")
        confidence = classification.get("confidence_percent", 0)
        is_mutated = classification.get("is_mutated", False)

        is_mac = (self.os_type == "darwin")

        # Specific kill command
        kill_cmd = f"kill -9 {pid}" if is_mac else f"taskkill /F /PID {pid}"
        freeze_cmd = f"kill -STOP {pid}" if is_mac else f"powershell Stop-Process -Id {pid}"

        mutation_badge = "⚠️ MUTATED / ZERO-DAY VARIANT (Behaviorally matched)" if is_mutated else "IDENTIFIED SIGNATURE"

        lines = [
            "==================================================================",
            f"🚨 EMERGENCY SECURITY ALERT: {family.upper()}",
            "==================================================================",
            f"• Threat Category:     {classification.get('threat_name')}",
            f"• Operational Mode:    {mode} THREAT ({'Actively executing system modifications' if mode == 'ACTIVE' else 'Passive stealth surveillance'})",
            f"• Confidence Score:    {confidence}%",
            f"• Mutation Status:     {mutation_badge}",
            f"• Offending PID:       {pid}",
            f"• Parent Process:      {parent}",
            f"• Executing Command:   {cmd}",
            "------------------------------------------------------------------",
            "🛡️ STEP-BY-STEP REMEDIATION & DISABLEMENT ADVISORY:",
            "------------------------------------------------------------------"
        ]

        # Add immediate 1-click command recommendation
        lines.append(f"[IMMEDIATE ACTION 1] FREEZE OR TERMINATE PROCESS:")
        lines.append(f"   macOS / Linux Terminal : {kill_cmd}")
        lines.append(f"   Windows PowerShell     : {kill_cmd}")
        lines.append("")

        # Add specific playbook steps from the archetype
        steps = classification.get("remediation_steps", [])
        for step in steps:
            lines.append(f"   {step}")

        lines.append("------------------------------------------------------------------")
        lines.append("ℹ️ Log Sentry Defense Agent has logged this forensic incident to sentinel.db")
        lines.append("==================================================================")

        return "\n".join(lines)

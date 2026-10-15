"""
archetype_matcher.py - Matches behavioral indicators against the Universal Threat Database.
Detects mutated malware, estimates family similarity, and links remediation playbooks.
"""
import os
import json
from typing import Dict, Any, List

class ArchetypeMatcher:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to config/threat_db.json
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_dir, "config", "threat_db.json")

        self.db_path = db_path
        self.threat_db = self._load_db()

    def _load_db(self) -> Dict[str, Any]:
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                return json.load(f).get("archetypes", {})
        return {}

    def classify_threat(self, analysis_result: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes output from BehaviorEngine and maps it to Threat Archetypes & Families.
        """
        matched_indicators = set(analysis_result.get("matched_indicators", []))
        op_mode = analysis_result.get("operational_mode", "BENIGN")

        if not matched_indicators or analysis_result.get("risk_score", 0) < 25:
            return {
                "identified": False,
                "threat_name": "BENIGN / NORMAL ACTIVITY",
                "archetype_id": "BENIGN",
                "confidence_percent": 0,
                "is_mutated": False,
                "remediation_steps": []
            }

        best_match = None
        highest_score = 0
        match_details = {}

        for arc_id, arc_data in self.threat_db.items():
            db_indicators = arc_data.get("indicators", {})
            overlap_weight = 0
            total_possible_weight = 0

            for ind_key, ind_info in db_indicators.items():
                w = ind_info.get("weight", 20)
                total_possible_weight += w
                if ind_key in matched_indicators:
                    overlap_weight += w

            # Mode alignment bonus
            if arc_data.get("mode") == op_mode:
                overlap_weight += 15
                total_possible_weight += 15

            score_pct = int((overlap_weight / max(1, total_possible_weight)) * 100)

            if score_pct > highest_score:
                highest_score = score_pct
                best_match = arc_id
                match_details = arc_data

        if not best_match or highest_score < 30:
            return {
                "identified": True,
                "threat_name": "GENERIC UNKNOWN SUSPICIOUS THREAT",
                "archetype_id": "UNKNOWN",
                "confidence_percent": highest_score,
                "is_mutated": True,
                "remediation_steps": [
                    "1. Terminate the suspicious process PID immediately.",
                    "2. Quarantine the executable file.",
                    "3. Review system logs for unexpected child processes."
                ]
            }

        # Mutation check: If behavior strongly matches a known archetype (e.g. Ransomware),
        # but the binary name is unfamiliar or randomized (not in standard known list)
        cmd = str(event.get("cmd", "")).lower()
        known_families = match_details.get("known_families", [])
        is_known_family_name = any(fam.lower() in cmd for fam in known_families)
        
        # If behavior is high-confidence but binary name is non-standard, it's flagged as mutated/upgraded
        is_mutated = (highest_score >= 60 and not is_known_family_name)

        primary_family = known_families[0] if known_families else match_details.get("name")
        display_name = f"{primary_family} (Mutated / Variant)" if is_mutated else f"{primary_family} Family"

        return {
            "identified": True,
            "archetype_id": best_match,
            "threat_name": match_details.get("name"),
            "candidate_family": display_name,
            "operational_mode": op_mode,
            "confidence_percent": min(100, highest_score),
            "is_mutated": is_mutated,
            "description": match_details.get("description"),
            "remediation_steps": match_details.get("remediation_playbook", [])
        }

"""
src/privacy/log_sanitizer.py - Log Redaction, PII Scrubber & Screenshot Processor.
Masks secrets, tokens, passwords, and API credentials before logs are processed,
and extracts forensic metadata from uploaded screenshots.
"""
import re
import os
import base64
from io import BytesIO
from PIL import Image

SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey|secret|token|password|passwd|auth)[\s:=]+['\"]?([A-Za-z0-9_\-\.]{8,})['\"]?", r"\1: [REDACTED_SECRET]"),
    (r"(ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})", "[REDACTED_GITHUB_TOKEN]"),
    (r"(AKIA[0-9A-Z]{16})", "[REDACTED_AWS_KEY]"),
    (r"bearer\s+([A-Za-z0-9_\-\.]{15,})", "Bearer [REDACTED_AUTH_TOKEN]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "[REDACTED_EMAIL]")
]

def sanitize_log_text(raw_text: str) -> dict:
    """Sanitizes sensitive information from raw log text."""
    redacted_count = 0
    clean_text = raw_text
    
    for pattern, repl in SECRET_PATTERNS:
        matches = re.findall(pattern, clean_text)
        if matches:
            redacted_count += len(matches)
            clean_text = re.sub(pattern, repl, clean_text)
            
    return {
        "sanitized_text": clean_text,
        "redactions_made": redacted_count,
        "original_length": len(raw_text),
        "clean_length": len(clean_text)
    }

def process_screenshot_data(filename: str, file_bytes: bytes) -> dict:
    """Extracts forensic metadata and validates screenshot image files."""
    try:
        img = Image.open(BytesIO(file_bytes))
        width, height = img.size
        format_name = img.format or "PNG"
        
        # Check suspicious keywords in filename
        suspicious_tags = []
        name_lower = filename.lower()
        if any(k in name_lower for k in ["error", "alert", "wannacry", "escape", "spy", "ctrl", "ransom", "dockersock"]):
            suspicious_tags.append("KEYWORD_FLAGGED_FILENAME")
            
        # Convert to base64 thumbnail for preview
        thumb = img.copy()
        thumb.thumbnail((240, 240))
        buf = BytesIO()
        thumb.save(buf, format="JPEG", quality=85)
        thumb_b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
        
        return {
            "filename": filename,
            "valid": True,
            "width": width,
            "height": height,
            "format": format_name,
            "size_bytes": len(file_bytes),
            "size_kb": round(len(file_bytes) / 1024, 1),
            "thumbnail_b64": thumb_b64,
            "suspicious_tags": suspicious_tags
        }
    except Exception as e:
        return {
            "filename": filename,
            "valid": False,
            "error": str(e)
        }

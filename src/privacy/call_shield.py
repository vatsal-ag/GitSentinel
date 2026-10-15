"""
src/privacy/call_shield.py - Anti-Screen Sharing & Call Privacy Shield.
Detects active voice/video calls (Zoom, Meet, Teams, FaceTime, Discord, Skype)
and screen capture tools (OBS, QuickTime, screencapture, AnyDesk), and enforces
DRM-grade screen blackout (similar to Netflix and UPI/banking applications).
"""
import os
import sys
import platform
import subprocess
import threading
import time

CALL_PROCESSES = {
    "zoom.us": "Zoom Video Conference",
    "teams": "Microsoft Teams",
    "ms-teams": "Microsoft Teams",
    "skype": "Skype",
    "facetime": "Apple FaceTime",
    "discord": "Discord Voice/Video",
    "slack": "Slack Huddle/Call",
    "webex": "Cisco Webex",
    "anydesk": "AnyDesk Remote Control",
    "teamviewer": "TeamViewer Remote Desktop",
    "obs": "OBS Studio Screen Recorder",
    "obs64": "OBS Studio (64-bit)",
    "screencapture": "macOS Screen Capture",
    "quicktime player": "QuickTime Screen Recorder"
}

class CallPrivacyShield:
    def __init__(self):
        self.enabled = True
        self.manual_override = False
        self.active_call_detected = False
        self.detected_call_tool = None
        self.last_check_time = 0
        self.subscribers = []
        
        # Start background monitor daemon
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def _check_running_processes(self):
        """Scans local processes for active calling or screen capture software."""
        detected = []
        current_os = platform.system().lower()
        
        try:
            if current_os in ["darwin", "linux"]:
                cmd = ["ps", "-eo", "comm="]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2).decode("utf-8", errors="ignore")
                lines = [line.strip().lower() for line in output.splitlines()]
                
                for line in lines:
                    base = os.path.basename(line)
                    for key, name in CALL_PROCESSES.items():
                        if key in base or key in line:
                            detected.append(name)
                            break
            elif current_os == "windows":
                cmd = ["tasklist", "/fo", "csv", "/nh"]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2).decode("utf-8", errors="ignore")
                for line in output.splitlines():
                    lower_line = line.lower()
                    for key, name in CALL_PROCESSES.items():
                        if key in lower_line:
                            detected.append(name)
                            break
        except Exception:
            pass
            
        return list(set(detected))

    def _monitor_loop(self):
        """Periodically checks for active call software."""
        while self._running:
            if self.enabled:
                detected_apps = self._check_running_processes()
                was_active = self.active_call_detected
                
                if detected_apps or self.manual_override:
                    self.active_call_detected = True
                    self.detected_call_tool = detected_apps[0] if detected_apps else "Simulated Secure Call"
                else:
                    self.active_call_detected = False
                    self.detected_call_tool = None
                    
                # Apply native macOS Cocoa window sharing type if on macOS
                if platform.system() == "Darwin" and was_active != self.active_call_detected:
                    self.apply_macos_native_drm(not self.active_call_detected)
                    
            time.sleep(2.0)

    def apply_macos_native_drm(self, allow_sharing=True):
        """
        Uses macOS AppKit NSWindowSharingNone (0) to render the window
        completely black in all screen recordings, AirPlay, Zoom, Meet, and screenshots.
        """
        if platform.system() != "Darwin":
            return False
            
        try:
            from AppKit import NSApplication, NSWindowSharingNone, NSWindowSharingReadOnly
            sharing_type = NSWindowSharingReadOnly if allow_sharing else NSWindowSharingNone
            
            # Execute on main thread if possible
            app = NSApplication.sharedApplication()
            windows = app.windows()
            for win in windows:
                win.setSharingType_(sharing_type)
            return True
        except Exception as e:
            # Fallback gracefully
            return False

    def toggle_manual_simulation(self):
        """Toggles a simulated online call to test the black screen privacy curtain."""
        self.manual_override = not self.manual_override
        if self.manual_override:
            self.active_call_detected = True
            self.detected_call_tool = "Simulated UPI / Banking Call"
            self.apply_macos_native_drm(False)
        else:
            self.active_call_detected = False
            self.detected_call_tool = None
            self.apply_macos_native_drm(True)
        return self.get_status()

    def get_status(self):
        return {
            "shield_enabled": self.enabled,
            "call_detected": self.active_call_detected,
            "active_call_tool": self.detected_call_tool,
            "blackout_active": self.enabled and self.active_call_detected,
            "native_drm_supported": platform.system() == "Darwin",
            "mode": "DRM_WINDOW_BLACKOUT_NETFLIX_STANDARD"
        }

# Global singleton
call_shield = CallPrivacyShield()

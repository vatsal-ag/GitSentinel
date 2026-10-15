"""
Antigravity/run_gui.py - One-Click Launcher for the Universal GUI Dashboard.
Launches the server and automatically opens the browser.
Accessible on macOS, Windows, Linux, Android, and iOS.
"""
import sys
import os
import socket
import webbrowser
import threading
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.gui.app import app

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_browser(port):
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"\n🌐 Opening web browser at {url}...")
    webbrowser.open(url)

if __name__ == "__main__":
    port = 5050
    local_ip = get_local_ip()

    print("=" * 70)
    print("🛡️  GITSENTINEL UNIVERSAL THREAT GUI & EDR DASHBOARD")
    print("=" * 70)
    print("Cross-Platform Accessibility:")
    print(f"  • macOS / Windows / Linux (Local):  http://localhost:{port}")
    print(f"  • Mobile (Android / iOS on Wi-Fi):  http://{local_ip}:{port}")
    print("=" * 70)

    # Launch browser in a background thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # Run server
    app.run(host="0.0.0.0", port=port, debug=False)

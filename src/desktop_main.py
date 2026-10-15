"""
desktop_main.py - Native Desktop Window Launcher for GitSentinel.
Uses native WebKit on macOS and WebView2 on Windows to run as a standalone desktop application.
"""
import sys
import os
import time
import threading
import webview

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.gui.app import app

def start_server():
    # Run backend server silently on localhost:5050
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)

def launch_native_app():
    # Start Flask API in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(0.8)

    # Launch Native App Window
    window = webview.create_window(
        title="GitSentinel - Universal Threat Detection & Remediation EDR",
        url="http://127.0.0.1:5050",
        width=1280,
        height=850,
        min_size=(900, 600),
        text_select=True,
        confirm_close=False
    )
    webview.start()

if __name__ == "__main__":
    launch_native_app()

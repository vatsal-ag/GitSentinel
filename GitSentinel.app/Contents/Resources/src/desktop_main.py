"""
src/desktop_main.py - Native Desktop Window Launcher for GitSentinel.
Uses native WebKit on macOS and WebView2 on Windows to run as a standalone desktop application.
"""
import sys
import os
import time
import socket
import threading
import webview

# Locate project root dynamically
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.gui.app import app

def find_free_port(start_port=5050):
    """Finds an open localhost port starting from start_port."""
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return 5050

def start_server(port):
    """Run backend Flask server silently on localhost."""
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

def launch_native_app():
    port = find_free_port(5050)
    
    # Start Flask API in daemon thread
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()
    
    # Give server a brief moment to bind
    time.sleep(0.6)

    # Launch Native App Window pointing directly to the EDR dashboard
    target_url = f"http://127.0.0.1:{port}/dashboard"
    print(f"[*] GitSentinel Desktop running on {target_url}")

    window = webview.create_window(
        title="GitSentinel EDR — Universal Behavioral Defense",
        url=target_url,
        width=1320,
        height=880,
        min_size=(960, 640),
        text_select=True,
        confirm_close=False
    )
    webview.start()

if __name__ == "__main__":
    launch_native_app()

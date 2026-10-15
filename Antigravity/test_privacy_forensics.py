#!/usr/bin/env python3
"""
Test Suite for Log Sentry Privacy Call Shield & Screenshot Forensic Ingestion
"""
import sys
import os
import base64

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.gui.app import app

def run_tests():
    client = app.test_client()

    # 1. Telemetry / Status
    res = client.get('/api/status')
    assert res.status_code == 200, f'Status endpoint: {res.status_code}'
    print('[✓] Status endpoint OK')

    # 2. Privacy Status
    res = client.get('/api/privacy/status')
    assert res.status_code == 200
    data = res.get_json()
    assert 'shield_enabled' in data and 'call_detected' in data
    print(f"[✓] Privacy status OK: enabled={data['shield_enabled']}, call_detected={data['call_detected']}")

    # 3. Log Sanitizer
    test_log = '2026-10-15 ERROR Failed auth token ghp_ABC1234567890abcdefghijklmnopqrstuv for user john@company.com with key AKIA1234567890ABCDEF'
    res = client.post('/api/logs/sanitize', json={'raw_logs': test_log})
    assert res.status_code == 200
    san_data = res.get_json()
    assert san_data['redactions_made'] >= 3
    assert 'ghp_' not in san_data['sanitized_text']
    assert 'AKIA' not in san_data['sanitized_text']
    print(f"[✓] Log Sanitizer OK: {san_data['redactions_made']} secrets redacted")

    # 4. Screenshot Upload
    from PIL import Image
    from io import BytesIO
    test_img = Image.new("RGB", (100, 80), color=(16, 24, 40))
    buf = BytesIO()
    test_img.save(buf, format="PNG")
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    data_uri = f'data:image/png;base64,{b64_str}'
    res = client.post('/api/logs/upload-screenshot', json={'image_b64': data_uri, 'filename': 'evidence.png'})
    assert res.status_code == 200
    sc_data = res.get_json()
    assert sc_data['valid'] is True
    print(f"[✓] Screenshot Forensics Upload OK: dimensions={sc_data['width']}x{sc_data['height']}, format={sc_data['format']}")

    # 5. Auto-collect host logs
    res = client.post('/api/logs/auto-collect')
    assert res.status_code == 200
    auto_data = res.get_json()
    assert len(auto_data['logs']) > 50
    print(f"[✓] Auto-collect logs OK: {len(auto_data['logs'])} chars collected")

    # 6. Export forensic bundle
    res = client.post('/api/logs/export-bundle', json={
        'logs': san_data['sanitized_text'],
        'screenshots': [sc_data],
        'verdict': {'threat_archetype': 'Benign', 'risk_score': 0}
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['success'] is True
    bundle = res_data['bundle']
    assert 'timestamp' in bundle and 'status' in bundle
    print(f"[✓] Forensic bundle export OK: status={bundle['status']}, timestamp={bundle['timestamp']}")

    print("\n[SUCCESS] ALL PRIVACY & FORENSIC SUITE TESTS PASSED 100%!")

if __name__ == '__main__':
    run_tests()

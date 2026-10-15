#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Starting Log Sentry Universal EDR Desktop App..."
python3 src/desktop_main.py || python src/desktop_main.py

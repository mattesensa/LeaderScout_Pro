#!/bin/bash
# Script di avvio automatico per macOS
cd "$(dirname "$0")"
echo "=================================================="
echo "  [LeadScout PRO] Avvio in corso..."
echo "=================================================="

# Installazione/verifica delle dipendenze
python3 -m pip install -r requirements.txt --quiet

# Avvio del launcher
python3 desktop_launcher.py

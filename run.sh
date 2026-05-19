#!/bin/bash

echo ""
echo "===================================="
echo " Cyber Recon Toolkit Launcher"
echo "===================================="
echo ""

if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv venv
fi

echo "[+] Activating virtual environment..."
source venv/bin/activate

echo "[+] Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "[+] Launching Cyber Recon Toolkit..."
echo ""

python3 toolkit.py
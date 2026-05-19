#!/bin/bash

echo ""
echo "===================================="
echo " Cyber Recon Toolkit Launcher"
echo "===================================="
echo ""

# Create virtual environment if missing
if [ ! -d "venv" ]; then

    echo "[+] Creating virtual environment..."

    python3 -m venv venv

fi

# Activate virtual environment
echo "[+] Activating virtual environment..."

source venv/bin/activate

# Install requirements
echo "[+] Checking dependencies..."

pip install -q -r requirements.txt

echo ""
echo "[+] Launching Cyber Recon Toolkit..."
echo ""

python toolkit.py
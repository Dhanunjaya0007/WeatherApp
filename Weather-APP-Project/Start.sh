#!/bin/bash
# ═══════════════════════════════════════════
#  WeatherGlass - Mac & Linux Launcher
#  HOW TO RUN:
#  1. Open Terminal in this folder
#  2. chmod +x start.sh   (only once)
#  3. ./start.sh
# ═══════════════════════════════════════════

clear
echo ""
echo "  ======================================="
echo "    WeatherGlass — Starting..."
echo "  ======================================="
echo ""

# ── Go to script's own folder ──
cd "$(dirname "$0")"

# ── Check Python ──
echo "  [1/3] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &>/dev/null; then
    PYTHON=python
    PIP=pip
else
    echo ""
    echo "  ERROR: Python not found."
    echo "  Install from: https://python.org"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi
echo "  Python found: $($PYTHON --version)"

# ── Install dependencies ──
echo ""
echo "  [2/3] Installing dependencies..."
$PIP install flask flask-cors requests --quiet
echo "  Dependencies ready."

# ── Open browser after 2 seconds ──
echo ""
echo "  [3/3] Starting server..."
echo ""
echo "  ======================================="
echo "    Running at: http://localhost:5000"
echo "    Press CTRL+C to stop"
echo "  ======================================="
echo ""

# Open browser after 2 second delay (background)
sleep 2 && open "http://localhost:5000" 2>/dev/null || \
sleep 2 && xdg-open "http://localhost:5000" 2>/dev/null &

# Start Flask
$PYTHON server.py
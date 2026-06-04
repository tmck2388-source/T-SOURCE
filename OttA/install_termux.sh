#!/bin/bash
# OttA Installation Script for Termux
# Handles dependencies and environment setup

set -e

echo "🚀 OttA Termux Installation"
echo "=============================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Update package manager
echo -e "${YELLOW}[1/5] Updating package manager...${NC}"
pkg update -y > /dev/null 2>&1 || true

# Step 2: Install system dependencies
echo -e "${YELLOW}[2/5] Installing system dependencies...${NC}"
pkg install -y python git curl wget > /dev/null 2>&1 || true

# Step 3: Create virtual environment (optional but recommended)
echo -e "${YELLOW}[3/5] Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
else
    source venv/bin/activate
fi

# Step 4: Upgrade pip
echo -e "${YELLOW}[4/5] Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Step 5: Install OttA dependencies (no binary wheels)
echo -e "${YELLOW}[5/5] Installing OttA dependencies...${NC}"
pip install \
    requests==2.31.0 \
    duckduckgo-search==3.9.11 \
    colorama==0.4.6 \
    prompt-toolkit==3.0.43 \
    python-dotenv==1.0.0 \
    aiohttp==3.9.1 \
    --no-binary :all: 2>&1 | grep -E "Successfully|ERROR|WARNING" || true

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Download Ollama: https://ollama.ai"
echo "2. Run: ollama serve"
echo "3. In another terminal, run: python main.py"
echo ""

#!/bin/bash
# Termux Ollama Setup & Diagnosis

echo "🔍 Checking Ollama in Termux..."
echo "=================================="
echo ""

# Check if ollama is installed
if command -v ollama &> /dev/null; then
    echo "✓ Ollama executable found"
    OLLAMA_PATH=$(which ollama)
    echo "  Location: $OLLAMA_PATH"
else
    echo "✗ Ollama not in PATH"
    echo "  Trying common Termux locations..."
    
    if [ -f "$HOME/.local/bin/ollama" ]; then
        echo "  ✓ Found at: $HOME/.local/bin/ollama"
        echo "  Add to PATH: export PATH=\$HOME/.local/bin:\$PATH"
    elif [ -f "$PREFIX/bin/ollama" ]; then
        echo "  ✓ Found at: $PREFIX/bin/ollama"
    fi
fi

echo ""
echo "📁 Looking for Ollama models..."

# Check model directory
if [ -d "$HOME/.ollama/models" ]; then
    echo "✓ Found models at: $HOME/.ollama/models"
    echo "  Available models:"
    ls -lh "$HOME/.ollama/models" 2>/dev/null | grep -E '^d' | awk '{print "    -", $NF}'
elif [ -d "$PREFIX/opt/ollama/models" ]; then
    echo "✓ Found models at: $PREFIX/opt/ollama/models"
    echo "  Available models:"
    ls -lh "$PREFIX/opt/ollama/models" 2>/dev/null | grep -E '^d' | awk '{print "    -", $NF}'
else
    echo "✗ Models directory not found"
fi

echo ""
echo "🚀 To use OttA with your existing Ollama:"
echo ""
echo "1. In ONE Termux window, start Ollama:"
echo "   ollama serve"
echo ""
echo "2. In ANOTHER Termux window, run OttA:"
echo "   cd T-SOURCE/OttA"
echo "   python main.py"
echo ""
echo "OttA will automatically detect your Ollama and available models!"
echo ""

"""
Find and diagnose Ollama installation
"""
import subprocess
import os
from pathlib import Path

def find_ollama_executable():
    """Find Ollama executable in common locations"""
    possible_paths = [
        "/usr/bin/ollama",
        "/usr/local/bin/ollama",
        "/opt/ollama/bin/ollama",
        os.path.expanduser("~/.local/bin/ollama"),
        os.path.expanduser("~/ollama/bin/ollama"),
        "/data/data/com.termux/files/usr/bin/ollama",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found Ollama at: {path}")
            return path
    
    return None

def find_ollama_models():
    """Find Ollama models directory and list models"""
    possible_paths = [
        os.path.expanduser("~/.ollama/models"),
        os.path.expanduser("~/.local/share/ollama/models"),
        "/data/data/com.termux/files/home/.ollama/models",
        os.getenv("OLLAMA_HOME", os.path.expanduser("~/.ollama")),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found Ollama models at: {path}")
            models = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            if models:
                print(f"  Models available: {models}")
            return path
    
    return None

def check_ollama_running():
    """Check if Ollama is running"""
    import requests
    
    hosts = [
        "http://localhost:11434",
        "http://127.0.0.1:11434",
        "http://0.0.0.0:11434",
    ]
    
    for host in hosts:
        try:
            response = requests.get(f"{host}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                print(f"✓ Ollama is running at: {host}")
                if models:
                    print(f"  Available models:")
                    for model in models:
                        print(f"    - {model.get('name')}")
                return host
        except:
            pass
    
    return None

def diagnose_ollama():
    """Run full Ollama diagnostic"""
    print("\n" + "="*60)
    print("OLLAMA DIAGNOSTIC")
    print("="*60 + "\n")
    
    print("1. Looking for Ollama executable...")
    exe = find_ollama_executable()
    if not exe:
        print("✗ Ollama executable not found")
    
    print("\n2. Looking for Ollama models...")
    models_dir = find_ollama_models()
    if not models_dir:
        print("✗ Ollama models directory not found")
    
    print("\n3. Checking if Ollama is running...")
    running = check_ollama_running()
    if not running:
        print("✗ Ollama is not running")
        print("\nTo start Ollama in Termux:")
        print("  1. Open a new terminal")
        print("  2. Run: ollama serve")
    
    print("\n" + "="*60)
    if exe and models_dir and running:
        print("✓ All good! Ollama is ready to use")
    else:
        print("⚠ Some issues found - see above")
    print("="*60 + "\n")

if __name__ == "__main__":
    diagnose_ollama()
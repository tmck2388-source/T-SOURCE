"""
OttA Configuration Management
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

# Ensure directories exist
for directory in [CONFIG_DIR, TEMPLATES_DIR, DATA_DIR]:
    directory.mkdir(exist_ok=True)

# AI/Model Configuration
# Try multiple Ollama paths (Termux, Linux, macOS, Windows)
OLLAMA_PATHS = [
    "http://localhost:11434",  # Default
    os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "http://127.0.0.1:11434",
    "http://0.0.0.0:11434",
]

# For Termux specifically
if os.path.exists("/data/data/com.termux"):
    OLLAMA_PATHS.insert(0, "http://127.0.0.1:11434")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", OLLAMA_PATHS[0])
# Use mistral or qwen2.5-coder if available, fallback to dolphin
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
USE_LOCAL_OLLAMA = os.getenv("USE_LOCAL_OLLAMA", "True").lower() == "true"

# Web Search Configuration
DUCKDUCKGO_ENABLED = True
WEB_SEARCH_TIMEOUT = 10

# UI Configuration
ENABLE_COLORS = True
AUTO_SAVE_HISTORY = True
HISTORY_FILE = DATA_DIR / "history.json"

# Feature Flags
FEATURES = {
    "lyric_generation": True,
    "code_assistant": True,
    "web_search": True,
    "template_engine": True,
    "semi_autonomous": True,
    "learning_mode": True,
}

# Application Info
APP_NAME = "OttA"
APP_VERSION = "0.1.0"
AUTHOR = "tmck2388"

class Settings:
    """Central settings management"""
    def __init__(self):
        self.settings_file = CONFIG_DIR / "settings.json"
        self.load_settings()
    
    def load_settings(self):
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "theme": "dark",
                "model": OLLAMA_MODEL,
                "language": "en",
                "auto_learn": True,
                "ollama_host": OLLAMA_HOST,
            }
            self.save_settings()
    
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        self.save_settings()

# Global settings instance
settings = Settings()
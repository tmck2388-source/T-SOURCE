# OttA - AI Assistant & Creative Tool

> Your personal AI companion for music, code, and web-powered creativity

## Features
- 🎵 **Lyric Generation** - Create explicit music lyrics with custom BPM/beat syncing
- 💻 **Code Assistant** - Generate, fix, and learn code with semi-autonomous experiments
- 🔍 **Web Search** - DuckDuckGo integration for real-time learning
- 🎨 **Templates** - Pre-built templates for quick project scaffolding
- 📱 **Cross-Platform** - Works on PowerShell (Windows), Termux (Android), and Linux

## Quick Start

### Prerequisites
- Python 3.8+
- Ollama (optional, for local AI models)
- DuckDuckGo API access

### Installation

**Windows (PowerShell):**
```powershell
git clone https://github.com/tmck2388-source/T-SOURCE.git
cd T-SOURCE/OttA
python -m pip install -r requirements.txt
python main.py
```

**Termux:**
```bash
pkg install python git
git clone https://github.com/tmck2388-source/T-SOURCE.git
cd T-SOURCE/OttA
pip install -r requirements.txt
python main.py
```

## Project Structure
```
OttA/
├── main.py              # Core application entry point
├── requirements.txt     # Python dependencies
├── config.py           # Configuration & settings
├── ai_core/
│   ├── ollama_client.py
│   ├── web_search.py
│   └── learning_engine.py
├── features/
│   ├── lyric_generator.py
│   ├── code_assistant.py
│   └── template_engine.py
├── ui/
│   ├── cli_interface.py
│   └── commands.py
└── templates/
    ├── music_template.json
    └── code_template.json
```

## Status
🚀 In Development - Personal Testing Phase
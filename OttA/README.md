# OttA - AI Assistant & Creative Tool

> Your personal AI companion for music, code, and web-powered creativity

## ✨ What is OttA?

OttA is a **conversational AI assistant** that works like chatting with a friend. She helps you:
- 🎵 **Write lyrics** - Create original music with any theme, style, or beat
- 💻 **Code together** - Generate, debug, and improve code with explanations  
- 🧠 **Brainstorm** - Get creative ideas and improvements
- 📚 **Learn** - Understand where code went wrong and how to fix it
- 💾 **Remember** - Save conversations and pick up where you left off

## 🎯 Key Features

### 🗣️ Natural Conversation
Just chat naturally! OttA understands context and adapts:
```
You: "Write me a drill beat about street life"
OttA: [Generates lyrics with that vibe]

You: "Make it more explicit"
OttA: [Adapts the existing lyrics]

You: "Now help me code a music player for it"
OttA: [Generates Python code]

You: "Fix this error: [error]"
OttA: [Debugs and explains]
```

### 🧠 Conversation Memory
- Remembers your style and preferences
- Keeps context across messages
- Learns from past conversations
- Saves work for later retrieval

### 🎯 Multi-Task in One Conversation
Switch seamlessly between lyrics, code, ideas, and debugging - all in natural conversation.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- **Ollama** (REQUIRED - for conversational AI)

### Setup

**1. Install Ollama**
```bash
# Download from https://ollama.ai
# Then run in a terminal:
ollama serve

# In another terminal, pull a model:
ollama pull dolphin-mixtral
```

**2. Install OttA**
```bash
# Clone the repo
git clone https://github.com/tmck2388-source/T-SOURCE.git
cd T-SOURCE/OttA

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**3. Run OttA**
```bash
# Make sure Ollama is running (step 1)
python main.py
```

## 📖 Quick Start

```bash
$ python main.py

╔══════════════════════════════════════════════════════════╗
║       🤖 OttA - Your AI Creative Companion 🎵       ║
║    Let's create, code, and explore together!       ║
╚══════════════════════════════════════════════════════════╝

You > Write me a rap verse about overcoming struggle

OttA > [Creates original rap lyrics with attitude]

You > Make it more explicit and add some slang

OttA > [Adapts the lyrics with your style]

You > Now write Python code that analyzes these lyrics

OttA > [Generates analyzing code with explanations]

You > save "Rap Analysis Project"

OttA > ✓ Conversation saved!
```

## 💬 Commands

| Command | Purpose |
|---------|----------|
| `help` | Show help menu and commands |
| `save [name]` | Save current conversation |
| `load [id]` | Load a previous conversation |
| `memory` | List all saved conversations |
| `clear` | Start fresh conversation |
| `status` | Show memory & context stats |
| `exit` | Save and exit |

## 🎤 What You Can Ask

### 🎵 Music & Lyrics
```
"Write a trap beat about making money"
"Generate drill lyrics - more aggressive"
"Create a hook for my song about [topic]"
"Make these lyrics more explicit"
"Adjust this to fit a 140 BPM beat"
"How would you improve these lyrics?"
```

### 💻 Coding
```
"Write Python code to [description]"
"Fix this error: [error + code]"
"How can I improve this code?"
"Explain what this does"
"Generate a web scraper for [site]"
"Debug this: [describe the problem]"
```

### 🧠 Brainstorming
```
"What's a cool project idea?"
"How would you structure this?"
"What are best practices for [topic]?"
"Give me 3 ways to improve this"
"Let's work on [idea] together"
```

## 🧠 How It Works

1. **You chat naturally** - OttA understands context
2. **She remembers** - Keeps track of conversation
3. **She adapts** - Learns your preferences and style
4. **Multi-task seamlessly** - Switch between lyrics, code, ideas
5. **Save your work** - Never lose a conversation

## 💾 Memory & Context

OttA's memory lives in `~/.otta/memory/`:
- `conversations.json` - Your saved conversations
- `context.json` - Current context
- `learned.json` - Learned patterns

You can:
- Save any conversation with a custom name
- Load previous conversations by ID
- Export as JSON, TXT, or Markdown
- Clear context for a fresh start

## 📦 Requirements

- `requests` - HTTP library
- `duckduckgo-search` - Web search
- `colorama` - Terminal colors
- `prompt-toolkit` - Interactive prompt with history
- `python-dotenv` - Environment config
- `aiohttp` - Async HTTP

## 🔧 Troubleshooting

### "Ollama not running"
```bash
# In another terminal:
ollama serve
```

### "pydantic-core failed" (Termux)
Already fixed! Just run:
```bash
bash install_termux.sh
```

### "Context near limit" warning
Save your conversation:
```
save "my awesome work"
clear
```

## 💡 Tips for Best Results

1. **Be specific** - Describe what you want clearly
2. **Provide context** - Paste code/lyrics when asking for fixes
3. **Iterate** - Say "make it more..." and OttA adapts
4. **Save often** - Don't lose your work
5. **Build on it** - Continue conversations from previous sessions

## 📂 Project Structure

```
OttA/
├── main.py                           # Entry point
├── config.py                         # Configuration
├── requirements.txt                  # Dependencies
├── ai_core/
│   ├── ollama_client.py             # Ollama connection
│   ├── web_search.py                # DuckDuckGo search
│   ├── memory_system.py             # Conversation memory
│   └── fallback_ai.py               # Template fallback
├── features/
│   ├── lyric_generator.py           # Lyric generation
│   ├── code_assistant.py            # Code assistance
│   └── interactive_builder.py       # Project builder
├── ui/
│   └── conversational_interface.py  # Main conversation UI
└── templates/
    ├── music_template.json
    └── code_template.json
```

## 🔐 Privacy

All conversations are stored **locally** in `~/.otta/`. Nothing is uploaded anywhere. Your work is yours alone.

## 🚀 Example Workflow

```
> Write me a chill trap beat about late nights
OttA: [Generates lyrics]

> Add more references to specific things I like
OttA: [Adapts with personal touches]

> Now write Python code to make a music app
OttA: [Writes complete music app code]

> Fix this bug I found: [paste error]
OttA: [Debugs and explains the issue]

> How would you improve the design?
OttA: [Gives architectural improvements]

> save "Late Night Music Project"
OttA: ✓ Saved!

> load late_night_music_id (from memory list)
OttA: ✓ Loaded! Ready to continue...
```

## 👤 Created by Tommy (tmck2388)

OttA - Making creative AI personal, conversational, and genuinely helpful.

---

**Ready to create? Run `python main.py` and start chatting! 🚀**

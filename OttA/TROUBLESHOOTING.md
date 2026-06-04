# OttA Troubleshooting Guide

## 🔴 Installation Issues

### Termux: "pydantic-core failed to build"
**Problem:** Cargo/Rust compilation fails  
**Solution:** 
```bash
# Clean everything
rm -rf ~/.cache/pip
pip cache purge

# Install dependencies manually (in order)
pip install requests==2.31.0
pip install colorama==0.4.6  
pip install prompt-toolkit==3.0.43
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install duckduckgo-search==3.9.11

# Run setup script
bash install_termux.sh
```

### Termux: "pkg: command not found"
**Problem:** Package manager not available  
**Solution:**
```bash
apt update && apt install -y python git
python -m pip install --upgrade pip
```

---

## 🟡 Runtime Issues

### "Ollama not detected"
**Problem:** Ollama server isn't running  
**Solution:**
```bash
# Download Ollama from https://ollama.ai
# Then run in another terminal:
ollama serve

# In OttA, you can still:
- Use web search (search command)
- Access memory (memory commands)
- Get limited code suggestions
```

### "Module not found" errors
**Problem:** Missing dependency  
**Solution:**
```bash
# Reinstall everything
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --force-reinstall
```

### CLI crashes on empty input
**Solution:** Already fixed in latest version - update with:
```bash
git pull origin main
```

---

## 🟢 Memory Issues

### "Context near limit" warning
**Problem:** Too many messages in current session  
**Solution:**
```
memory save "my work name"    # Save your work
memory clear                  # Fresh start
memory load id                # Load previous work
```

### Can't find saved conversation
**Problem:** Wrong conversation ID  
**Solution:**
```
memory list              # See all saved conversations
memory export conv_id    # Export to view contents
```

---

## 📝 Getting Help

Check these files:
- `README.md` - Overview & quick start
- `requirements.txt` - Dependency list
- `config.py` - Configuration options

Try these commands in OttA:
```
help              # Show all commands
memory stats      # Check system status
search python     # Test web search (no Ollama needed)
```

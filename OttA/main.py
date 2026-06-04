#!/usr/bin/env python3
"""
OttA - AI Assistant & Creative Tool
Main application entry point with conversational AI

Usage:
  python main.py          # Start interactive conversation
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_core.ollama_client import ollama
from ai_core.web_search import web_engine
from ai_core.memory_system import memory
from ui.conversational_interface import ConversationalInterface
from config import APP_NAME, APP_VERSION
from colorama import Fore, Style

def check_requirements():
    """Check if all dependencies are available"""
    missing = []
    
    deps = {
        'requests': 'requests library',
        'duckduckgo_search': 'DuckDuckGo search',
        'colorama': 'terminal colors',
        'prompt_toolkit': 'interactive prompt'
    }
    
    for module, desc in deps.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(f"{module} ({desc})")
    
    if missing:
        print(f"{Fore.RED}❌ Missing dependencies:{Style.RESET_ALL}")
        for dep in missing:
            print(f"  - {dep}")
        print(f"\n{Fore.YELLOW}Install with:{Style.RESET_ALL}")
        print(f"  pip install -r requirements.txt")
        return False
    
    return True

def initialize_app():
    """Initialize OttA application"""
    print(f"\n{Fore.CYAN}Initializing {APP_NAME} v{APP_VERSION}...{Style.RESET_ALL}")
    
    # Check Ollama connection - REQUIRED
    if not ollama.check_connection():
        print(f"\n{Fore.RED}❌ CRITICAL: Ollama is not running!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}OttA requires Ollama to have real conversations.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}To fix:{Style.RESET_ALL}")
        print(f"  1. Download from: https://ollama.ai")
        print(f"  2. Install and run: ollama serve")
        print(f"  3. In another terminal: ollama pull dolphin-mixtral")
        print(f"  4. Run this script again\n")
        return False
    
    models = ollama.list_models()
    print(f"{Fore.GREEN}✓ Ollama connected - {len(models)} models available{Style.RESET_ALL}")
    if models:
        print(f"  Models: {', '.join([m.split(':')[0] for m in models[:3]])}...")
    
    # Initialize memory
    print(f"{Fore.CYAN}Loading memory system...{Style.RESET_ALL}")
    stats = memory.get_context_stats()
    print(f"{Fore.GREEN}✓ Memory loaded - {stats['total_saved_conversations']} conversations saved{Style.RESET_ALL}")
    
    return True

def main():
    """Main application entry point"""
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    
    # Initialize app
    if not initialize_app():
        sys.exit(1)
    
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    
    # Start conversational interface
    try:
        interface = ConversationalInterface(
            ollama=ollama,
            web_search=web_engine,
            memory=memory
        )
        interface.run()
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Conversation saved. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
#!/usr/bin/env python3
"""
OttA - AI Assistant & Creative Tool
Main application entry point

Usage:
  python main.py          # Start interactive CLI
  python main.py lyrics   # Start lyric generation
  python main.py code     # Start code assistant
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
from features.lyric_generator import LyricGenerator
from features.code_assistant import CodeAssistant
from ui.cli_interface import OttaCLI
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
    
    # Check Ollama connection
    if ollama.check_connection():
        models = ollama.list_models()
        print(f"{Fore.GREEN}✓ Ollama connected - {len(models)} models available{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Ollama not available - web search & code features limited{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   Download from: https://ollama.ai{Style.RESET_ALL}")
    
    # Initialize memory
    print(f"{Fore.CYAN}Loading memory system...{Style.RESET_ALL}")
    stats = memory.get_context_stats()
    print(f"{Fore.GREEN}✓ Memory loaded - {stats['total_saved_conversations']} conversations saved{Style.RESET_ALL}")
    
    # Initialize features
    lyric_gen = LyricGenerator(ollama)
    code_asst = CodeAssistant(ollama, web_engine)
    
    return lyric_gen, code_asst

def main():
    """Main application entry point"""
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    print(f"{Fore.CYAN}═" * 50 + f"{Style.RESET_ALL}")
    
    # Initialize app
    try:
        lyric_gen, code_asst = initialize_app()
    except Exception as e:
        print(f"{Fore.RED}❌ Initialization error: {e}{Style.RESET_ALL}")
        print(f"Make sure all files are in place and readable.")
        sys.exit(1)
    
    print(f"{Fore.CYAN}═" * 50 + f"{Style.RESET_ALL}")
    
    # Handle command-line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'lyrics':
            print(f"{Fore.MAGENTA}🎵 Lyric Generation Mode{Style.RESET_ALL}")
        elif command == 'code':
            print(f"{Fore.GREEN}💻 Code Assistant Mode{Style.RESET_ALL}")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: lyrics, code")
            sys.exit(1)
    else:
        # Start interactive CLI with all components
        try:
            cli = OttaCLI(memory=memory, ollama=ollama, web_search=web_engine)
            cli.run()
        except Exception as e:
            print(f"{Fore.RED}❌ CLI Error: {e}{Style.RESET_ALL}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

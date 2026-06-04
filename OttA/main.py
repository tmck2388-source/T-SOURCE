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
    try:
        import requests
        import duckduckgo_search
        import colorama
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        return False

def initialize_app():
    """Initialize OttA application"""
    print(f"{Fore.CYAN}Initializing {APP_NAME} v{APP_VERSION}...{Style.RESET_ALL}")
    
    # Check Ollama connection
    if ollama.check_connection():
        models = ollama.list_models()
        print(f"{Fore.GREEN}✓ Ollama connected - {len(models)} models available{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Ollama not available - some features may be limited{Style.RESET_ALL}")
    
    # Initialize memory
    print(f"{Fore.CYAN}Loading memory system...{Style.RESET_ALL}")
    stats = memory.get_context_stats()
    print(f"{Fore.GREEN}✓ Memory loaded - {stats['total_saved_conversations']} conversations, {stats['learned_patterns']} patterns{Style.RESET_ALL}")
    
    # Initialize features
    lyric_gen = LyricGenerator(ollama)
    code_asst = CodeAssistant(ollama, web_engine)
    
    return lyric_gen, code_asst

def main():
    """Main application entry point"""
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Initialize app
    lyric_gen, code_asst = initialize_app()
    
    # Handle command-line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'lyrics':
            print(f"{Fore.MAGENTA}🎵 Lyric Generation Mode{Style.RESET_ALL}")
            # Interactive lyric generation
        elif command == 'code':
            print(f"{Fore.GREEN}💻 Code Assistant Mode{Style.RESET_ALL}")
            # Interactive code assistance
        else:
            print(f"Unknown command: {command}")
            print("Available commands: lyrics, code")
            sys.exit(1)
    else:
        # Start interactive CLI with all components
        cli = OttaCLI(memory=memory, ollama=ollama, web_search=web_engine)
        cli.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
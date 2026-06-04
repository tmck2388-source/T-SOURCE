"""
CLI Interface for OttA
Cross-platform command-line interface for PowerShell and Termux
"""
from colorama import Fore, Back, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import sys
import os

init(autoreset=True)

class OttaCLI:
    """Main CLI interface for OttA"""
    
    def __init__(self):
        self.session = PromptSession()
        self.commands = {
            'lyrics': 'Generate music lyrics',
            'code': 'Generate or fix code',
            'search': 'Search the web',
            'build': 'Build a project autonomously',
            'help': 'Show help information',
            'exit': 'Exit OttA'
        }
        self.completer = WordCompleter(list(self.commands.keys()))
    
    def display_banner(self):
        """Display OttA banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════╗
║{Fore.MAGENTA}    🤖 OttA - AI Assistant 🎵{Fore.CYAN}    ║
║{Fore.WHITE}  Lyric Generator • Code Master   {Fore.CYAN}║
╚═══════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def display_help(self):
        """Display help menu"""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
"""
        for cmd, description in self.commands.items():
            help_text += f"  {Fore.GREEN}{cmd:<10}{Style.RESET_ALL} - {description}\n"
        print(help_text)
    
    def process_command(self, command: str):
        """Process user command"""
        cmd = command.strip().lower().split()[0]
        
        if cmd == 'help':
            self.display_help()
        elif cmd == 'exit':
            print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
            return False
        elif cmd == 'lyrics':
            print(f"{Fore.MAGENTA}🎵 Lyric Generation Mode{Style.RESET_ALL}")
            # Placeholder for lyric generation
        elif cmd == 'code':
            print(f"{Fore.GREEN}💻 Code Assistant Mode{Style.RESET_ALL}")
            # Placeholder for code assistance
        elif cmd == 'search':
            print(f"{Fore.BLUE}🔍 Web Search Mode{Style.RESET_ALL}")
            # Placeholder for web search
        elif cmd == 'build':
            print(f"{Fore.YELLOW}🔨 Building Project Mode{Style.RESET_ALL}")
            # Placeholder for building
        else:
            print(f"{Fore.RED}Unknown command: {cmd}{Style.RESET_ALL}")
        
        return True
    
    def run(self):
        """Start the CLI interface"""
        self.display_banner()
        self.display_help()
        
        while True:
            try:
                prompt_text = f"{Fore.CYAN}OttA > {Style.RESET_ALL}"
                command = self.session.prompt(prompt_text, completer=self.completer)
                
                if not self.process_command(command):
                    break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
            except EOFError:
                break

def main():
    """Main entry point"""
    cli = OttaCLI()
    cli.run()

if __name__ == "__main__":
    main()
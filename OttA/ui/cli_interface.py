"""
CLI Interface for OttA
Cross-platform command-line interface for PowerShell and Termux
"""
from colorama import Fore, Back, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import sys
import os
from pathlib import Path

init(autoreset=True)

class OttaCLI:
    """Main CLI interface for OttA"""
    
    def __init__(self, memory=None, ollama=None, web_search=None):
        self.session = PromptSession()
        self.memory = memory
        self.ollama = ollama
        self.web_search = web_search
        
        self.commands = {
            'lyrics': 'Generate music lyrics',
            'code': 'Generate or fix code',
            'search': 'Search the web',
            'build': 'Build a project autonomously',
            'memory': 'Manage memory and conversations',
            'help': 'Show help information',
            'exit': 'Exit OttA'
        }
        self.completer = WordCompleter(list(self.commands.keys()))
    
    def display_banner(self):
        """Display OttA banner"""
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════╗
║{Fore.MAGENTA}    🤖 OttA - AI Assistant 🎵{Fore.CYAN}    ║
║{Fore.WHITE}  Lyric Generator • Code Master • Memory Keeper{Fore.CYAN}   ║
╚════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def display_help(self):
        """Display help menu"""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
"""
        for cmd, description in self.commands.items():
            help_text += f"  {Fore.GREEN}{cmd:<10}{Style.RESET_ALL} - {description}\n"
        
        if self.memory:
            stats = self.memory.get_context_stats()
            help_text += f"\n{Fore.YELLOW}Memory Status:{Style.RESET_ALL}\n"
            help_text += f"  Context: {stats['context_buffer_size']}/{stats['context_limit']} "
            if stats['context_near_limit']:
                help_text += f"{Fore.RED}⚠️ NEAR LIMIT{Style.RESET_ALL}"
            else:
                help_text += f"{Fore.GREEN}✓{Style.RESET_ALL}"
            help_text += f"\n  Conversations: {stats['total_saved_conversations']}\n"
        
        print(help_text)
    
    def handle_memory_command(self, args: list):
        """Handle memory-related commands"""
        if not self.memory:
            print(f"{Fore.RED}Memory system not initialized{Style.RESET_ALL}")
            return
        
        if not args or args[0] == 'help':
            print(f"""
{Fore.CYAN}Memory Commands:{Style.RESET_ALL}
  memory list          - List all conversations
  memory save [name]   - Save current conversation
  memory load [id]     - Load a conversation
  memory delete [id]   - Delete a conversation
  memory stats         - Show memory statistics
  memory clear         - Clear current context (fresh start)
  memory export [id]   - Export conversation
            """)
        elif args[0] == 'list':
            convs = self.memory.list_conversations()
            if not convs:
                print(f"{Fore.YELLOW}No saved conversations{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}Saved Conversations:{Style.RESET_ALL}")
                for conv in convs:
                    print(f"  {Fore.GREEN}{conv['id']}{Style.RESET_ALL} - {conv['name']} ({conv['message_count']} messages)")
        
        elif args[0] == 'save':
            name = ' '.join(args[1:]) if len(args) > 1 else None
            conv_id = self.memory.save_conversation(name)
            print(f"{Fore.GREEN}✓ Conversation saved: {conv_id}{Style.RESET_ALL}")
        
        elif args[0] == 'load':
            if len(args) < 2:
                print(f"{Fore.RED}Usage: memory load [id]{Style.RESET_ALL}")
                return
            conv = self.memory.load_conversation(args[1])
            if conv:
                print(f"{Fore.GREEN}✓ Conversation loaded ({len(conv)} messages){Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Conversation not found{Style.RESET_ALL}")
        
        elif args[0] == 'delete':
            if len(args) < 2:
                print(f"{Fore.RED}Usage: memory delete [id]{Style.RESET_ALL}")
                return
            if self.memory.delete_conversation(args[1]):
                print(f"{Fore.GREEN}✓ Conversation deleted{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Conversation not found{Style.RESET_ALL}")
        
        elif args[0] == 'stats':
            stats = self.memory.get_context_stats()
            print(f"""
{Fore.CYAN}Memory Statistics:{Style.RESET_ALL}
  Current Conversation Messages: {stats['current_conversation_messages']}
  Context Buffer Size: {stats['context_buffer_size']}/{stats['context_limit']}
  Total Saved Conversations: {stats['total_saved_conversations']}
  Learned Patterns: {stats['learned_patterns']}
  Status: {Fore.GREEN if not stats['context_near_limit'] else Fore.RED}{'OK' if not stats['context_near_limit'] else 'NEAR LIMIT'}{Style.RESET_ALL}
            """)
        
        elif args[0] == 'clear':
            self.memory.clear_current_context()
            print(f"{Fore.YELLOW}✓ Context cleared - fresh start{Style.RESET_ALL}")
        
        elif args[0] == 'export':
            if len(args) < 2:
                print(f"{Fore.RED}Usage: memory export [id]{Style.RESET_ALL}")
                return
            export = self.memory.export_conversation(args[1], format="txt")
            if export:
                print(export)
            else:
                print(f"{Fore.RED}✗ Conversation not found{Style.RESET_ALL}")
    
    def process_command(self, command: str) -> bool:
        """Process user command"""
        # Handle empty command
        parts = command.strip().split()
        if not parts:
            return True
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self.display_help()
        elif cmd == 'exit':
            print(f"{Fore.YELLOW}Saving memory and exiting... 👋{Style.RESET_ALL}")
            if self.memory:
                self.memory.save_conversation("Session Exit Auto-Save")
            return False
        elif cmd == 'lyrics':
            print(f"{Fore.MAGENTA}🎵 Lyric Generation Mode{Style.RESET_ALL}")
            if self.ollama:
                self.memory.add_to_conversation("user", f"Generate lyrics: {' '.join(args)}")
                print(f"{Fore.YELLOW}[Lyric generation not yet interactive - coming soon!]{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Ollama not available{Style.RESET_ALL}")
        elif cmd == 'code':
            print(f"{Fore.GREEN}💻 Code Assistant Mode{Style.RESET_ALL}")
            if self.ollama:
                self.memory.add_to_conversation("user", f"Code assistance: {' '.join(args)}")
                print(f"{Fore.YELLOW}[Code assistance not yet interactive - coming soon!]{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Ollama not available{Style.RESET_ALL}")
        elif cmd == 'search':
            if args:
                query = ' '.join(args)
                print(f"{Fore.BLUE}🔍 Searching: {query}{Style.RESET_ALL}")
                if self.web_search:
                    results = self.web_search.search(query, max_results=3)
                    if results:
                        for i, result in enumerate(results, 1):
                            print(f"\n{Fore.CYAN}{i}. {result.get('title', 'No title')}{Style.RESET_ALL}")
                            print(f"   {result.get('body', 'No description')[:100]}...")
                        self.memory.add_to_conversation("user", f"Searched: {query}")
                    else:
                        print(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Web search not available{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Usage: search [query]{Style.RESET_ALL}")
        elif cmd == 'build':
            print(f"{Fore.YELLOW}🔨 Building Project Mode{Style.RESET_ALL}")
            if self.ollama:
                self.memory.add_to_conversation("user", f"Build project: {' '.join(args)}")
                print(f"{Fore.YELLOW}[Semi-autonomous build not yet interactive - coming soon!]{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Ollama not available{Style.RESET_ALL}")
        elif cmd == 'memory':
            self.handle_memory_command(args)
        else:
            print(f"{Fore.RED}Unknown command: {cmd}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")
        
        return True
    
    def run(self):
        """Start the CLI interface"""
        self.display_banner()
        self.display_help()
        
        print(f"{Fore.GREEN}Ready to assist! Type 'help' for commands.{Style.RESET_ALL}\n")
        
        while True:
            try:
                prompt_text = f"{Fore.CYAN}OttA > {Style.RESET_ALL}"
                command = self.session.prompt(prompt_text, completer=self.completer)
                
                if not self.process_command(command):
                    break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted. Type 'exit' to quit or 'help' for commands.{Style.RESET_ALL}")
            except EOFError:
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def main():
    """Main entry point"""
    cli = OttaCLI()
    cli.run()

if __name__ == "__main__":
    main()
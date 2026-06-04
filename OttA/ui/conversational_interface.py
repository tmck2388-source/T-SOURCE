"""
Conversational Interface - True dialogue with OttA
Natural conversation flow with ability to pivot to any task
"""
from colorama import Fore, Back, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from pathlib import Path
from datetime import datetime
import json

init(autoreset=True)

class ConversationalInterface:
    """Natural conversation interface with OttA"""
    
    def __init__(self, ollama=None, web_search=None, memory=None):
        self.ollama = ollama
        self.web_search = web_search
        self.memory = memory
        
        # Setup conversation history file
        history_dir = Path.home() / ".otta" / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        history_file = history_dir / "conversation.txt"
        
        self.session = PromptSession(history=FileHistory(str(history_file)))
        
        # Conversation context for multi-turn dialogue
        self.conversation_context = []
        self.max_context = 10  # Keep last 10 messages for context
        
        # Load previous conversation if available
        self.load_last_conversation()
    
    def load_last_conversation(self):
        """Load the last conversation from memory"""
        if self.memory and self.memory.context_buffer:
            # Start with some context from previous conversations
            self.conversation_context = self.memory.context_buffer[-5:]
    
    def display_banner(self):
        """Display welcome banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║{Fore.MAGENTA}       🤖 OttA - Your AI Creative Companion 🎵{Fore.CYAN}       ║
║{Fore.WHITE}    Let's create, code, and explore together!{Fore.CYAN}       ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}💡 Just chat naturally! I can:
  🎵 Write lyrics or songs
  💻 Code with you and fix bugs  
  🔍 Search the web
  🧠 Remember our conversation
  📚 Brainstorm and improve ideas{Style.RESET_ALL}

{Fore.YELLOW}Type 'help' for commands or just start chatting!{Style.RESET_ALL}
        """
        print(banner)
    
    def display_help(self):
        """Display help and command reference"""
        help_text = f"""
{Fore.CYAN}╔ COMMANDS ╗{Style.RESET_ALL}

{Fore.GREEN}help{Style.RESET_ALL}          - Show this help menu
{Fore.GREEN}memory{Style.RESET_ALL}        - See saved conversations
{Fore.GREEN}save [name]{Style.RESET_ALL}   - Save current conversation
{Fore.GREEN}load [id]{Style.RESET_ALL}     - Load a previous conversation
{Fore.GREEN}clear{Style.RESET_ALL}         - Start fresh conversation
{Fore.GREEN}status{Style.RESET_ALL}        - Show memory & context stats
{Fore.GREEN}exit{Style.RESET_ALL}          - Exit OttA

{Fore.CYAN}╔ NATURAL CONVERSATION ╗{Style.RESET_ALL}

Just ask naturally! Examples:
  • "Write me a rap verse about hustling"
  • "Fix this Python code: [code]"
  • "How do I make a web scraper?"
  • "Generate song lyrics for a trap beat"
  • "Help me debug this error"
  • "Let's brainstorm a project idea"

{Fore.YELLOW}I'll understand context and adapt!{Style.RESET_ALL}
        """
        print(help_text)
    
    def add_to_context(self, role: str, content: str):
        """Add message to conversation context"""
        self.conversation_context.append({
            "role": role,
            "content": content
        })
        
        # Keep only recent context
        if len(self.conversation_context) > self.max_context:
            self.conversation_context = self.conversation_context[-self.max_context:]
        
        # Save to memory
        if self.memory:
            self.memory.add_to_conversation(role, content)
    
    def get_context_prompt(self) -> str:
        """Build context for OttA to understand conversation"""
        context = """You are OttA, a creative AI assistant. You are:
- Natural and conversational, like talking to a friend
- Knowledgeable about music, coding, and creative projects
- Able to help brainstorm, create, and fix things
- Willing to pivot between tasks naturally
- Remembering the conversation context
- Offering suggestions and improvements

When users ask for:
- LYRICS: Create original, explicit content with flow and rhythm
- CODE: Write clean, commented code with explanations
- HELP: Debug and suggest fixes with explanations
- BRAINSTORMING: Offer creative ideas and improvements
- ANYTHING: Have natural dialogue, ask clarifying questions if needed

Keep responses conversational but helpful. Be concise but complete."""
        
        return context
    
    def get_ollama_response(self, user_message: str) -> str:
        """Get response from Ollama with conversation context"""
        
        # Build messages for Ollama
        messages = [
            {
                "role": "system",
                "content": self.get_context_prompt()
            }
        ]
        
        # Add conversation context
        for msg in self.conversation_context[-5:]:  # Last 5 messages
            messages.append(msg)
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Ollama
        try:
            response = self.ollama.chat(messages)
            return response
        except Exception as e:
            return f"❌ Error getting response: {e}"
    
    def process_command(self, user_input: str) -> bool:
        """Process commands or pass to conversation"""
        
        command = user_input.strip().lower()
        
        # Commands
        if command == 'help':
            self.display_help()
            return True
        
        elif command == 'exit':
            print(f"\n{Fore.YELLOW}Saving conversation...{Style.RESET_ALL}")
            if self.memory:
                self.memory.save_conversation(f"Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print(f"{Fore.GREEN}✓ Saved!{Style.RESET_ALL}")
            return False
        
        elif command == 'clear':
            self.conversation_context = []
            if self.memory:
                self.memory.clear_current_context()
            print(f"{Fore.YELLOW}✓ Fresh start! Let's begin again.{Style.RESET_ALL}")
            return True
        
        elif command == 'status':
            if self.memory:
                stats = self.memory.get_context_stats()
                print(f"""
{Fore.CYAN}Current Status:{Style.RESET_ALL}
  Context Messages: {len(self.conversation_context)}/{self.max_context}
  Total Conversations Saved: {stats['total_saved_conversations']}
  Memory Buffer: {stats['context_buffer_size']}/{stats['context_limit']}
                """)
            return True
        
        elif command == 'memory':
            if self.memory:
                convs = self.memory.list_conversations()
                if convs:
                    print(f"\n{Fore.CYAN}Your Conversations:{Style.RESET_ALL}")
                    for conv in convs[-10:]:  # Show last 10
                        print(f"  {Fore.GREEN}{conv['id']}{Style.RESET_ALL} - {conv['name']}")
                else:
                    print(f"{Fore.YELLOW}No saved conversations yet{Style.RESET_ALL}")
            return True
        
        elif command.startswith('save '):
            name = command[5:].strip()
            if self.memory:
                conv_id = self.memory.save_conversation(name or None)
                print(f"{Fore.GREEN}✓ Conversation saved!{Style.RESET_ALL}")
            return True
        
        elif command.startswith('load '):
            conv_id = command[5:].strip()
            if self.memory:
                conv = self.memory.load_conversation(conv_id)
                if conv:
                    self.conversation_context = conv[-self.max_context:]
                    print(f"{Fore.GREEN}✓ Conversation loaded!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Conversation not found{Style.RESET_ALL}")
            return True
        
        # Not a command - treat as conversation
        return None
    
    def run(self):
        """Run the conversational interface"""
        self.display_banner()
        
        print(f"{Fore.CYAN}Starting conversation...{Style.RESET_ALL}\n")
        
        while True:
            try:
                # Prompt
                prompt_text = f"{Fore.MAGENTA}You{Style.RESET_ALL} > "
                user_input = self.session.prompt(prompt_text)
                
                if not user_input.strip():
                    continue
                
                # Check if it's a command
                result = self.process_command(user_input)
                if result is False:
                    break
                elif result is True:
                    continue
                
                # It's a conversation - get response from OttA
                print(f"{Fore.CYAN}OttA{Style.RESET_ALL} is thinking...", end=" ", flush=True)
                
                response = self.get_ollama_response(user_input)
                
                print(f"\r{' ' * 30}\r", end="")  # Clear "thinking" message
                
                # Display response
                print(f"{Fore.CYAN}OttA{Style.RESET_ALL} > {response}\n")
                
                # Add to context
                self.add_to_context("user", user_input)
                self.add_to_context("assistant", response)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Type 'exit' to save and quit, or continue chatting.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
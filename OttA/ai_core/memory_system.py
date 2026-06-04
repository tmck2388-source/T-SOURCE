"""
Memory & Context Management System
Handles conversation history, context persistence, and memory recall for OttA
"""
import json
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import hashlib

class MemorySystem:
    """Persistent memory for conversations and context"""
    
    def __init__(self, memory_dir: Path = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".otta" / "memory"
        
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.conversations_file = self.memory_dir / "conversations.json"
        self.context_file = self.memory_dir / "context.json"
        self.learned_file = self.memory_dir / "learned.json"
        
        self.current_conversation = []
        self.context_buffer = []
        self.learned_patterns = {}
        self.context_limit = 50  # Lines before refresh needed
        
        self.load_all()
    
    def load_all(self):
        """Load all memory files"""
        if self.conversations_file.exists():
            with open(self.conversations_file, 'r') as f:
                self.conversations = json.load(f)
        else:
            self.conversations = []
        
        if self.context_file.exists():
            with open(self.context_file, 'r') as f:
                self.context_buffer = json.load(f)
        
        if self.learned_file.exists():
            with open(self.learned_file, 'r') as f:
                self.learned_patterns = json.load(f)
    
    def add_to_conversation(self, role: str, content: str, metadata: Dict = None):
        """
        Add message to current conversation
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (timestamp, tokens, etc)
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.current_conversation.append(message)
        self.context_buffer.append(message)
        
        # Check if context needs refresh
        if len(self.context_buffer) > self.context_limit:
            self.refresh_context()
    
    def refresh_context(self):
        """
        Refresh context to prevent terminal/memory overload
        Summarizes old context and keeps recent messages
        """
        if len(self.context_buffer) <= self.context_limit:
            return
        
        # Keep only recent messages, discard old ones
        keep_count = int(self.context_limit * 0.7)  # Keep 70% as recent context
        old_messages = self.context_buffer[:-keep_count]
        
        # Create summary of what was discussed
        summary = self._create_summary(old_messages)
        
        # Reset buffer with summary + recent
        self.context_buffer = [
            {
                "role": "system",
                "content": f"[CONTEXT SUMMARY]\n{summary}",
                "timestamp": datetime.now().isoformat()
            }
        ] + self.context_buffer[-keep_count:]
    
    def _create_summary(self, messages: List[Dict]) -> str:
        """Create a summary of messages"""
        if not messages:
            return "No previous context"
        
        summary_items = []
        for i, msg in enumerate(messages[-5:]):  # Summarize last 5
            if msg['role'] == 'user':
                summary_items.append(f"User asked: {msg['content'][:100]}")
            else:
                summary_items.append(f"Assistant responded: {msg['content'][:100]}")
        
        return "\n".join(summary_items)
    
    def get_context_for_model(self, max_messages: int = 20) -> List[Dict]:
        """
        Get formatted context for AI model
        
        Args:
            max_messages: Maximum messages to include
        
        Returns:
            List of messages suitable for model input
        """
        return self.context_buffer[-max_messages:]
    
    def save_conversation(self, name: str = None) -> str:
        """
        Save current conversation to memory
        
        Args:
            name: Optional conversation name
        
        Returns:
            Conversation ID
        """
        if not self.current_conversation:
            return None
        
        conv_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        conversation_data = {
            "id": conv_id,
            "name": name or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "timestamp": datetime.now().isoformat(),
            "messages": self.current_conversation,
            "message_count": len(self.current_conversation)
        }
        
        self.conversations.append(conversation_data)
        self._persist_conversations()
        
        return conv_id
    
    def load_conversation(self, conv_id: str) -> Optional[List[Dict]]:
        """
        Load a saved conversation
        
        Args:
            conv_id: Conversation ID to load
        
        Returns:
            List of messages or None if not found
        """
        for conv in self.conversations:
            if conv['id'] == conv_id:
                self.current_conversation = conv['messages']
                self.context_buffer = conv['messages'].copy()
                return conv['messages']
        return None
    
    def list_conversations(self) -> List[Dict]:
        """List all saved conversations"""
        return [
            {
                "id": c['id'],
                "name": c['name'],
                "timestamp": c['timestamp'],
                "message_count": c['message_count']
            }
            for c in self.conversations
        ]
    
    def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation"""
        for i, conv in enumerate(self.conversations):
            if conv['id'] == conv_id:
                self.conversations.pop(i)
                self._persist_conversations()
                return True
        return False
    
    def store_learned_pattern(self, pattern_name: str, pattern_data: Dict):
        """Store a learned pattern for reuse"""
        self.learned_patterns[pattern_name] = {
            "data": pattern_data,
            "timestamp": datetime.now().isoformat(),
            "usage_count": 0
        }
        self._persist_learned()
    
    def get_learned_pattern(self, pattern_name: str) -> Optional[Dict]:
        """Retrieve a learned pattern"""
        if pattern_name in self.learned_patterns:
            self.learned_patterns[pattern_name]["usage_count"] += 1
            self._persist_learned()
            return self.learned_patterns[pattern_name]["data"]
        return None
    
    def list_learned_patterns(self) -> List[str]:
        """List all learned patterns"""
        return list(self.learned_patterns.keys())
    
    def get_context_stats(self) -> Dict:
        """Get statistics about current context"""
        return {
            "current_conversation_messages": len(self.current_conversation),
            "context_buffer_size": len(self.context_buffer),
            "context_limit": self.context_limit,
            "context_near_limit": len(self.context_buffer) >= (self.context_limit * 0.8),
            "total_saved_conversations": len(self.conversations),
            "learned_patterns": len(self.learned_patterns)
        }
    
    def clear_current_context(self):
        """Clear current conversation/context (fresh start)"""
        self.current_conversation = []
        self.context_buffer = []
    
    def _persist_conversations(self):
        """Save conversations to disk"""
        with open(self.conversations_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    def _persist_learned(self):
        """Save learned patterns to disk"""
        with open(self.learned_file, 'w') as f:
            json.dump(self.learned_patterns, f, indent=2)
    
    def export_conversation(self, conv_id: str, format: str = "json") -> Optional[str]:
        """
        Export a conversation in different formats
        
        Args:
            conv_id: Conversation ID
            format: 'json', 'txt', or 'md'
        
        Returns:
            Formatted string or None
        """
        conv = None
        for c in self.conversations:
            if c['id'] == conv_id:
                conv = c
                break
        
        if not conv:
            return None
        
        if format == "json":
            return json.dumps(conv, indent=2)
        elif format == "txt":
            output = f"Conversation: {conv['name']}\n"
            output += f"Date: {conv['timestamp']}\n"
            output += "=" * 50 + "\n\n"
            for msg in conv['messages']:
                output += f"{msg['role'].upper()}:\n{msg['content']}\n\n"
            return output
        elif format == "md":
            output = f"# {conv['name']}\n\n"
            output += f"**Date:** {conv['timestamp']}\n\n"
            for msg in conv['messages']:
                output += f"## {msg['role'].upper()}\n\n{msg['content']}\n\n"
            return output
        
        return None

# Global instance
memory = MemorySystem()
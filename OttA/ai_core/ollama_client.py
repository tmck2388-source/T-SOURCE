"""
Ollama AI Client
Handles connections to local Ollama instances for unrestricted model inference
"""
import requests
import json
from typing import Optional, List
import sys
from colorama import Fore, Style

class OllamaClient:
    """Interface with local Ollama AI models"""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = None):
        self.host = host
        self.model = model  # Will be set automatically
        self.is_connected = False
        self.available_models = []
        self.check_connection()
        self.auto_select_model()
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            self.is_connected = response.status_code == 200
            if self.is_connected:
                # Get available models
                self.available_models = [m["name"] for m in response.json().get("models", [])]
            return self.is_connected
        except requests.exceptions.ConnectionError:
            print(f"{Fore.YELLOW}⚠️  Ollama not detected at {self.host}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}ℹ️  Make sure Ollama is running: ollama serve{Style.RESET_ALL}")
            self.is_connected = False
            return False
    
    def auto_select_model(self):
        """Automatically select best available model"""
        if not self.is_connected or not self.available_models:
            return
        
        # Priority order: mistral > qwen > dolphin > anything
        priority_models = ["mistral", "qwen2.5-coder", "dolphin-mixtral"]
        
        for priority_model in priority_models:
            for available in self.available_models:
                if priority_model in available:
                    self.model = available
                    print(f"{Fore.GREEN}✓ Using model: {self.model}{Style.RESET_ALL}")
                    return
        
        # If nothing matches, use first available
        if self.available_models:
            self.model = self.available_models[0]
            print(f"{Fore.GREEN}✓ Using model: {self.model}{Style.RESET_ALL}")
    
    def list_models(self) -> List[str]:
        """List available models on Ollama"""
        if not self.is_connected:
            return []
        
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except Exception as e:
            print(f"{Fore.RED}❌ Error listing models: {e}{Style.RESET_ALL}")
            return []
    
    def set_model(self, model_name: str):
        """Set the active model"""
        if model_name in self.available_models:
            self.model = model_name
            print(f"{Fore.GREEN}✓ Model changed to: {self.model}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Model not found: {model_name}{Style.RESET_ALL}")
            print(f"Available: {self.available_models}")
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: Input prompt
            stream: Whether to stream the response
        
        Returns:
            Generated text
        """
        if not self.is_connected:
            return f"{Fore.RED}❌ Ollama connection failed. Please ensure Ollama is running.{Style.RESET_ALL}"
        
        if not self.model:
            return f"{Fore.RED}❌ No model selected.{Style.RESET_ALL}"
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream
                },
                timeout=60
            )
            
            if response.status_code == 200:
                if stream:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            full_response += data.get("response", "")
                            if not data.get("done"):
                                sys.stdout.write(data.get("response", ""))
                                sys.stdout.flush()
                    return full_response
                else:
                    return response.json().get("response", "")
            else:
                return f"{Fore.RED}❌ Error: {response.status_code}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}❌ Generation failed: {e}{Style.RESET_ALL}"
    
    def chat(self, messages: List[dict]) -> str:
        """
        Chat with the model
        
        Args:
            messages: List of message dicts with 'role' and 'content'
        
        Returns:
            Model response
        """
        if not self.is_connected:
            return f"{Fore.RED}❌ Ollama connection failed.{Style.RESET_ALL}"
        
        if not self.model:
            return f"{Fore.RED}❌ No model selected.{Style.RESET_ALL}"
        
        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "")
            else:
                return f"{Fore.RED}❌ Error: {response.status_code}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}❌ Chat failed: {e}{Style.RESET_ALL}"

# Global instance - auto-detects and connects
ollama = OllamaClient()

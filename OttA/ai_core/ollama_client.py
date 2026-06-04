"""
Ollama AI Client
Handles connections to local Ollama instances for unrestricted model inference
"""
import requests
import json
from typing import Optional, List
import sys

class OllamaClient:
    """Interface with local Ollama AI models"""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.model = "dolphin-mixtral"  # Unrestricted model
        self.is_connected = False
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            self.is_connected = response.status_code == 200
            return self.is_connected
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Ollama not detected at {self.host}")
            print("ℹ️  Make sure Ollama is running: ollama serve")
            self.is_connected = False
            return False
    
    def list_models(self) -> List[str]:
        """List available models on Ollama"""
        if not self.is_connected:
            return []
        
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []
    
    def set_model(self, model_name: str):
        """Set the active model"""
        self.model = model_name
    
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
            return "❌ Ollama connection failed. Please ensure Ollama is running."
        
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
                return f"❌ Error: {response.status_code}"
        except Exception as e:
            return f"❌ Generation failed: {e}"
    
    def chat(self, messages: List[dict]) -> str:
        """
        Chat with the model
        
        Args:
            messages: List of message dicts with 'role' and 'content'
        
        Returns:
            Model response
        """
        if not self.is_connected:
            return "❌ Ollama connection failed."
        
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
                return f"❌ Error: {response.status_code}"
        except Exception as e:
            return f"❌ Chat failed: {e}"

# Global instance
ollama = OllamaClient()
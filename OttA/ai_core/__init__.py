"""OttA AI Core Module"""
from .ollama_client import OllamaClient, ollama
from .web_search import WebSearchEngine, web_engine

__all__ = ['OllamaClient', 'ollama', 'WebSearchEngine', 'web_engine']
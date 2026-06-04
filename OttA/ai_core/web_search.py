"""
Web Search Integration - DuckDuckGo
Provides real-time internet search capabilities for learning and content creation
"""
from duckduckgo_search import DDGS
import json
from typing import List, Dict
import time

class WebSearchEngine:
    """Handle all web search operations"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.search_history = []
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a DuckDuckGo search
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with title, body, and href
        """
        try:
            with DDGS(timeout=self.timeout) as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            
            # Store in history
            self.search_history.append({
                "query": query,
                "timestamp": time.time(),
                "results_count": len(results)
            })
            
            return results
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def search_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for news related to query"""
        try:
            with DDGS(timeout=self.timeout) as ddgs:
                results = list(ddgs.news(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"❌ News search failed: {e}")
            return []
    
    def search_images(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for images related to query"""
        try:
            with DDGS(timeout=self.timeout) as ddgs:
                results = list(ddgs.images(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"❌ Image search failed: {e}")
            return []
    
    def get_search_history(self) -> List[Dict]:
        """Retrieve search history for learning analysis"""
        return self.search_history
    
    def clear_history(self):
        """Clear search history"""
        self.search_history = []

# Global instance
web_engine = WebSearchEngine()
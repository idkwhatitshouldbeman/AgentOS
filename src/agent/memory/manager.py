"""
Memory Manager for AgentOS.
Handles short-term (working) memory and long-term (vector/database) memory.
"""

import time
import uuid
from typing import List, Optional, Dict, Any

from ..types import MemoryEntry

class MemoryManager:
    def __init__(self):
        self.short_term: List[MemoryEntry] = []
        self.long_term: List[MemoryEntry] = []  # Placeholder for vector DB
        
    def add(self, content: str, metadata: Dict[str, Any] = None):
        """Add a new memory entry."""
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            content=content,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        self.short_term.append(entry)
        # TODO: Asynchronously embed and add to long_term storage
        
    def search(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """
        Search memory.
        For now, just simple keyword matching on short-term memory.
        Later, semantic search on long-term memory.
        """
        results = []
        query_terms = query.lower().split()
        
        for entry in reversed(self.short_term):
            if any(term in entry.content.lower() for term in query_terms):
                results.append(entry)
                if len(results) >= limit:
                    break
                    
        return results

    def get_context_window(self, max_tokens: int = 2000) -> str:
        """Get recent context formatted for LLM."""
        # Simple implementation: just return last N entries
        # Real implementation needs token counting
        context = []
        current_len = 0
        
        for entry in reversed(self.short_term):
            text = f"[{time.ctime(entry.timestamp)}] {entry.content}"
            if current_len + len(text) > max_tokens * 4: # Rough char approx
                break
            context.insert(0, text)
            current_len += len(text)
            
        return "\n".join(context)

"""
Enhanced Conversation Management
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from backend.core.memory import MemoryManager

@dataclass
class ChatMessage:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: Optional[str] = None

class ConversationManager:
    def __init__(self):
        self.memory = MemoryManager()
        self.current_session = None
        self.context_limit = 20  # Number of messages to keep in context
    
    def start_new_session(self) -> str:
        """Start a new conversation session"""
        self.current_session = self.memory.create_session()
        return self.current_session
    
    def set_session(self, session_id: str) -> None:
        """Set current session"""
        self.current_session = session_id
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to current conversation"""
        if not self.current_session:
            self.start_new_session()
        
        self.memory.save_message(self.current_session, role, content)
        
        # Extract and save important information
        if role == "user":
            self._extract_user_info(content)
    
    def get_context_messages(self) -> List[ChatMessage]:
        """Get recent messages for LLM context"""
        if not self.current_session:
            return []
        
        history = self.memory.get_conversation_history(
            self.current_session, 
            limit=self.context_limit
        )
        
        return [
            ChatMessage(
                role=msg["role"],
                content=msg["content"],
                timestamp=msg["timestamp"]
            )
            for msg in history
        ]
    
    def get_enhanced_context(self) -> List[ChatMessage]:
        """Get context with relevant memories"""
        messages = self.get_context_messages()
        
        # Add system message with relevant memories
        memories = self.memory.get_memories(limit=5)
        if memories:
            memory_text = "اطلاعات مهم که باید به خاطر داشته باشی:\n"
            for mem in memories:
                memory_text += f"- {mem['key']}: {mem['value']}\n"
            
            system_message = ChatMessage(
                role="system",
                content=memory_text
            )
            messages.insert(0, system_message)
        
        return messages
    
    def get_conversations_list(self) -> List[Dict]:
        """Get list of recent conversations"""
        return self.memory.get_recent_conversations()
    
    def search_history(self, query: str) -> List[Dict]:
        """Search in conversation history"""
        return self.memory.search_conversations(query)
    
    def save_user_preference(self, key: str, value: str) -> None:
        """Save user preference"""
        self.memory.save_memory(key, value, "preference", importance=8)
    
    def _extract_user_info(self, content: str) -> None:
        """Extract and save important user information"""
        content_lower = content.lower()
        
        # Simple keyword-based extraction
        if "اسم من" in content_lower or "نام من" in content_lower:
            # Extract name (very basic)
            words = content.split()
            for i, word in enumerate(words):
                if word in ["اسم", "نام"] and i + 2 < len(words):
                    name = words[i + 2]
                    self.memory.save_memory("user_name", name, "preference", 9)
        
        if "دوست دارم" in content_lower:
            self.memory.save_memory("user_likes", content, "preference", 6)
        
        if "متنفرم" in content_lower or "دوست ندارم" in content_lower:
            self.memory.save_memory("user_dislikes", content, "preference", 6)

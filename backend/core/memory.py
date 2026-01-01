"""
Memory Management System
"""
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.database.models import Conversation, Message, Memory, get_db, create_tables

class MemoryManager:
    def __init__(self):
        create_tables()
        self.db = next(get_db())  # Keep database session
    
    def create_session(self) -> str:
        """Create new conversation session"""
        session_id = str(uuid.uuid4())
        db = next(get_db())
        
        conversation = Conversation(
            session_id=session_id,
            title="مکالمه جدید"
        )
        db.add(conversation)
        db.commit()
        db.close()
        
        return session_id
    
    def save_message(self, session_id: str, role: str, content: str) -> None:
        """Save message to database"""
        db = next(get_db())
        
        # Get or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            conversation = Conversation(
                session_id=session_id,
                title=self._generate_title(content)
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save message
        message = Message(
            conversation_id=conversation.id,
            role=role,
            content=content,
            tokens=len(content.split())
        )
        db.add(message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        if not conversation.title or conversation.title == "مکالمه جدید":
            conversation.title = self._generate_title(content)
        
        db.commit()
        db.close()
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        db = next(get_db())
        
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            db.close()
            return []
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp.desc()).limit(limit).all()
        
        result = [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in reversed(messages)
        ]
        
        db.close()
        return result
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        db = next(get_db())
        
        conversations = db.query(Conversation).filter(
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        result = [
            {
                "session_id": conv.session_id,
                "title": conv.title,
                "updated_at": conv.updated_at.isoformat(),
                "message_count": db.query(Message).filter(
                    Message.conversation_id == conv.id
                ).count()
            }
            for conv in conversations
        ]
        
        db.close()
        return result
    
    def save_memory(self, key: str, value: str, category: str = "fact", importance: int = 5) -> None:
        """Save important information to memory"""
        db = next(get_db())
        
        # Check if memory exists
        existing = db.query(Memory).filter(Memory.key == key).first()
        
        if existing:
            existing.value = value
            existing.importance = importance
            existing.created_at = datetime.utcnow()
        else:
            memory = Memory(
                key=key,
                value=value,
                category=category,
                importance=importance
            )
            db.add(memory)
        
        db.commit()
        db.close()
    
    def get_memories(self, category: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get stored memories"""
        db = next(get_db())
        
        query = db.query(Memory)
        if category:
            query = query.filter(Memory.category == category)
        
        memories = query.order_by(
            Memory.importance.desc(),
            Memory.created_at.desc()
        ).limit(limit).all()
        
        result = [
            {
                "key": mem.key,
                "value": mem.value,
                "category": mem.category,
                "importance": mem.importance
            }
            for mem in memories
        ]
        
        db.close()
        return result
    
    def search_conversations(self, query: str, limit: int = 10) -> List[Dict]:
        """Search in conversation history"""
        db = next(get_db())
        
        messages = db.query(Message).filter(
            Message.content.contains(query)
        ).order_by(Message.timestamp.desc()).limit(limit).all()
        
        result = []
        for msg in messages:
            conversation = db.query(Conversation).filter(
                Conversation.id == msg.conversation_id
            ).first()
            
            result.append({
                "session_id": conversation.session_id,
                "title": conversation.title,
                "content": msg.content[:200] + "..." if len(msg.content) > 200 else msg.content,
                "timestamp": msg.timestamp.isoformat()
            })
        
        db.close()
        return result
    
    def _generate_title(self, content: str) -> str:
        """Generate conversation title from first message"""
        words = content.split()[:5]
        title = " ".join(words)
        return title if len(title) > 10 else "مکالمه جدید"

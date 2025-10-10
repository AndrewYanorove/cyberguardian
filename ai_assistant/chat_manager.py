# chat_manager.py
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class ChatManager:
    def __init__(self):
        self.chats: Dict[str, dict] = {}
        self.user_sessions: Dict[str, List[str]] = {}  # user_id -> list of chat_ids
    
    def create_chat(self, user_id: str, title: str = "Новый чат") -> str:
        """Создает новый чат"""
        chat_id = str(uuid.uuid4())
    
        self.chats[chat_id] = {
            'id': chat_id,
            'user_id': user_id,
            'title': title,
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'token_count': 0
        }
    
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
    
        self.user_sessions[user_id].append(chat_id)
    
        print(f"✅ Создан чат {chat_id} для пользователя {user_id}")
        return chat_id
    
    def get_user_chats(self, user_id: str) -> List[dict]:
        """Возвращает все чаты пользователя"""
        if user_id not in self.user_sessions:
            return []
        
        chats = []
        for chat_id in self.user_sessions[user_id]:
            if chat_id in self.chats:
                chats.append(self.chats[chat_id])
        
        # Сортируем по времени обновления (новые сверху)
        chats.sort(key=lambda x: x['updated_at'], reverse=True)
        return chats
    
    def get_chat(self, chat_id: str) -> Optional[dict]:
        """Возвращает чат по ID"""
        return self.chats.get(chat_id)
    
    def add_message(self, chat_id: str, role: str, content: str, tokens: int = 0):
        """Добавляет сообщение в чат"""
        if chat_id not in self.chats:
            return
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'tokens': tokens
        }
        
        self.chats[chat_id]['messages'].append(message)
        self.chats[chat_id]['updated_at'] = datetime.now().isoformat()
        self.chats[chat_id]['token_count'] += tokens
        
        # Автоматически генерируем заголовок если это первое сообщение
        if len(self.chats[chat_id]['messages']) == 1 and role == 'user':
            self.chats[chat_id]['title'] = content[:30] + "..." if len(content) > 30 else content
    
    def delete_chat(self, user_id: str, chat_id: str) -> bool:
        """Удаляет чат"""
        if user_id in self.user_sessions and chat_id in self.user_sessions[user_id]:
            self.user_sessions[user_id].remove(chat_id)
        
        if chat_id in self.chats:
            del self.chats[chat_id]
            return True
        
        return False
    
    def rename_chat(self, chat_id: str, new_title: str) -> bool:
        """Переименовывает чат"""
        if chat_id in self.chats:
            self.chats[chat_id]['title'] = new_title
            self.chats[chat_id]['updated_at'] = datetime.now().isoformat()
            return True
        return False
    
    def clear_user_chats(self, user_id: str) -> bool:
        """Очищает все чаты пользователя"""
        if user_id in self.user_sessions:
            for chat_id in self.user_sessions[user_id]:
                if chat_id in self.chats:
                    del self.chats[chat_id]
            self.user_sessions[user_id] = []
            return True
        return False

# Глобальный менеджер чатов
chat_manager = ChatManager()
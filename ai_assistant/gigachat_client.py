# gigachat_client.py
import os
import requests
import time
import json
import hashlib
from typing import Optional, Dict

requests.packages.urllib3.disable_warnings()

class OptimizedGigaChatClient:
    def __init__(self):
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1"
        
        # Credentials для получения нового токена
        self.authorization_key = "MDE5OWNmNGUtZDc0Mi03NmNlLTljNDUtNDYwNTEzNDRhZTljOjhmYzUwMjgwLWMzZmMtNGUyOS1hMDhjLTIyOGY3MTQyZTEyNA=="
        self.rq_uid = "f96baca0-307d-44e3-9834-ab3bc45a2ebb"
        
        # Изначально токена нет - получим при первом запросе
        self.access_token = None
        self.token_expires_at = 0
        
        # Кэш ответов
        self.response_cache: Dict[str, dict] = {}
        self.cache_duration = 3600
        
        # Статистика
        self.usage_stats = {
            'total_requests': 0,
            'cached_responses': 0,
            'token_refreshes': 0,
            'tokens_used': 0
        }
        
        print("✅ GigaChat клиент инициализирован")
    
    def _get_access_token(self):
        """Получает новый access token"""
        try:
            print("🔄 Получаем новый access token...")
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': self.rq_uid,
                'Authorization': f'Basic {self.authorization_key}'
            }
            
            payload = {'scope': 'GIGACHAT_API_PERS'}
            
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=payload,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                # Токен живет 30 минут (1800 секунд)
                self.token_expires_at = time.time() + 1800 - 300  # -5 минут запаса
                self.usage_stats['token_refreshes'] += 1
                
                print(f"✅ Новый токен получен! Действует до: {time.ctime(self.token_expires_at)}")
                return True
            else:
                print(f"❌ Ошибка получения токена: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка подключения при получении токена: {e}")
            return False
    
    def _ensure_valid_token(self):
        """Убеждается что токен валиден"""
        # Если токена нет или он истек - получаем новый
        if not self.access_token or time.time() >= self.token_expires_at:
            return self._get_access_token()
        return True
    
    def _get_cache_key(self, message: str) -> str:
        """Создает ключ кэша на основе сообщения"""
        normalized_msg = ' '.join(message.lower().split())
        return hashlib.md5(normalized_msg.encode()).hexdigest()
    
    def _get_cached_response(self, message: str) -> Optional[str]:
        """Проверяет кэш для данного сообщения"""
        cache_key = self._get_cache_key(message)
        
        if cache_key in self.response_cache:
            cache_data = self.response_cache[cache_key]
            if time.time() - cache_data['timestamp'] < self.cache_duration:
                self.usage_stats['cached_responses'] += 1
                return cache_data['response']
        
        return None
    
    def _cache_response(self, message: str, response: str):
        """Сохраняет ответ в кэш"""
        cache_key = self._get_cache_key(message)
        self.response_cache[cache_key] = {
            'response': response,
            'timestamp': time.time(),
            'message': message
        }
        
        # Ограничиваем размер кэша
        if len(self.response_cache) > 1000:
            oldest_key = min(self.response_cache.keys(), 
                           key=lambda k: self.response_cache[k]['timestamp'])
            del self.response_cache[oldest_key]
    
    def _optimize_prompt(self, message: str) -> tuple[str, int]:
        """Оптимизирует промпт для экономии токенов"""
        # Только самые базовые ответы без API вызова
        quick_responses = {
            "привет": "👋 Привет!",
            "как дела": "🤖 Нормально!",
            "спасибо": "🙏 Пожалуйста!",
            "пока": "👋 Пока!",
        }
        
        msg_lower = message.lower().strip()
        
        for key in quick_responses:
            if key == msg_lower:  # Только точное совпадение
                return quick_responses[key], 0
        
        # Для всех остальных запросов используем API
        optimized_system_prompt = """Ты эксперт по кибербезопасности , программированию и психологии.Используй только свежие данные . Отвечай подробно и внятно. 
        Используй эмодзи для наглядности. Давай практические советы."""
        
        return optimized_system_prompt, 1
    
    def get_response(self, message: str) -> str:
        """Получение ответа от GigaChat"""
        self.usage_stats['total_requests'] += 1
        
        # 1. Проверяем кэш
        cached_response = self._get_cached_response(message)
        if cached_response:
            print("💾 Используем кэшированный ответ")
            return cached_response
        
        # 2. Проверяем быстрые ответы (только точные совпадения)
        quick_response, needs_api = self._optimize_prompt(message)
        if not needs_api:
            print("⚡ Используем быстрый ответ")
            self._cache_response(message, quick_response)
            return quick_response
        
        # 3. Получаем/обновляем токен
        if not self._ensure_valid_token():
            error_msg = "❌ Не удалось получить access token. Проверьте credentials."
            print(error_msg)
            return self._get_demo_response(message)
        
        # 4. Делаем запрос к GigaChat API
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            system_prompt, _ = self._optimize_prompt(message)
            
            payload = {
                "model": "GigaChat-Max",  # ⚡ ИЗМЕНЕНО: GigaChat-Max вместо GigaChat
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": message
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            print(f"📤 Отправляем запрос к GigaChat-Max: {message[:50]}...")
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                print(f"✅ Получен ответ от GigaChat-Max: {ai_response[:50]}...")
                
                # Сохраняем в кэш
                self._cache_response(message, ai_response)
                
                # Обновляем статистику токенов
                if 'usage' in result:
                    tokens_used = result['usage'].get('total_tokens', 0)
                    self.usage_stats['tokens_used'] += tokens_used
                    print(f"🪙 Использовано токенов: {tokens_used}")
                
                return ai_response
            else:
                error_msg = f"❌ GigaChat API error: {response.status_code} - {response.text}"
                print(error_msg)
                
                # Если ошибка авторизации, сбрасываем токен
                if response.status_code in [401, 403]:
                    self.access_token = None
                    self.token_expires_at = 0
                
                demo_response = self._get_demo_response(message)
                self._cache_response(message, demo_response)
                return demo_response
                
        except Exception as e:
            error_msg = f"❌ GigaChat request error: {e}"
            print(error_msg)
            demo_response = self._get_demo_response(message)
            self._cache_response(message, demo_response)
            return demo_response
    
    def _get_demo_response(self, message: str) -> str:
        """Демо-ответы если GigaChat не доступен"""
        demo_responses = {
            "пароль": "🔐 **Надежный пароль:**\n• 12+ символов\n• Буквы, цифры, спецсимволы\n• Уникальные пароли\n• Менеджер паролей\n• 2FA",
            "фишинг": "🎣 **Защита от фишинга:**\n• Проверяйте отправителя\n• Не переходите по ссылкам\n• Внимание к грамматике\n• Антифишинг расширения",
            "wifi": "📡 **Безопасность Wi-Fi:**\n• WPA3 шифрование\n• Смените пароль роутера\n• Отключите WPS\n• Скрытый SSID",
        }
        
        msg_lower = message.lower()
        for key in demo_responses:
            if key in msg_lower:
                return f"🤖 Демо-режим: {demo_responses[key]}"
        
        return "🤖 GigaChat-Max временно недоступен. Используется демо-режим. Попробуйте спросить о:\n• Паролях\n• Фишинге\n• Wi-Fi безопасности"
    
    def get_usage_stats(self) -> dict:
        """Возвращает статистику использования"""
        return {
            **self.usage_stats,
            'cache_size': len(self.response_cache),
            'cache_hit_rate': round(
                (self.usage_stats['cached_responses'] / self.usage_stats['total_requests'] * 100) 
                if self.usage_stats['total_requests'] > 0 else 0, 
                1
            ),
            'token_expires_in': max(0, int(self.token_expires_at - time.time())) if self.access_token else 0,
            'has_valid_token': bool(self.access_token and time.time() < self.token_expires_at)
        }
    
    def clear_cache(self):
        """Очищает кэш"""
        self.response_cache.clear()
        print("🧹 Кэш очищен")

# Создаем глобальный экземпляр
gigachat_client = OptimizedGigaChatClient()
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
        
        # Используем готовый токен (действует 30 минут)
        self.access_token = "-"
        
        # Токен действует 30 минут (1800 секунд), ставим время истечения
        self.token_expires_at = time.time() + 1800 - 300  # -5 минут запаса
        
        # Ваши credentials для обновления токена (если понадобится)
        self.authorization_key = "MDE5OWNmNGUtZDc0Mi03NmNlLTljNDUtNDYwNTEzNDRhZTljOjhmYzUwMjgwLWMzZmMtNGUyOS1hMDhjLTIyOGY3MTQyZTEyNA=="
        self.rq_uid = "f96baca0-307d-44e3-9834-ab3bc45a2ebb"
        
        # Кэш ответов для часто задаваемых вопросов
        self.response_cache: Dict[str, dict] = {}
        self.cache_duration = 3600  # 1 час кэширования
        
        # Статистика использования
        self.usage_stats = {
            'total_requests': 0,
            'cached_responses': 0,
            'token_refreshes': 0,
            'tokens_used': 0
        }
        
        print("✅ GigaChat: Используется готовый токен")
    
    def _refresh_token_if_needed(self):
        """Обновляет токен только если он истек"""
        if time.time() >= self.token_expires_at:
            print("🔄 GigaChat: Токен истек, обновляем...")
            self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в GigaChat (только при необходимости)"""
        try:
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
                # Устанавливаем время истечения с запасом в 5 минут
                self.token_expires_at = time.time() + token_data['expires_in'] - 300
                self.usage_stats['token_refreshes'] += 1
                print("✅ GigaChat: Токен успешно обновлен")
            else:
                print(f"❌ GigaChat: Ошибка аутентификации - {response.status_code}")
                print(f"Ответ: {response.text}")
                self.access_token = None
                
        except Exception as e:
            print(f"❌ GigaChat: Ошибка подключения - {e}")
            self.access_token = None
    
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
        quick_responses = {
            "привет": "👋 Привет! Я GigaChat помощник по кибербезопасности. Задайте вопрос о защите данных, паролях, фишинге и т.д.",
            "как дела": "🤖 У меня всё отлично! Готов помочь с вопросами кибербезопасности.",
            "спасибо": "🙏 Пожалуйста! Обращайтесь ещё, если будут вопросы по кибербезопасности.",
            "пока": "👋 До свидания! Будьте осторожны в сети!",
        }
        
        msg_lower = message.lower().strip()
        
        for key in quick_responses:
            if key in msg_lower:
                return quick_responses[key], 0
        
        optimized_system_prompt = """Ты эксперт по кибербезопасности. Отвечай кратко и по делу. 
        Используй эмодзи для наглядности. Давай практические советы."""
        
        return optimized_system_prompt, 1
    
    def get_response(self, message: str) -> str:
        """Получение ответа от GigaChat с оптимизацией токенов"""
        self.usage_stats['total_requests'] += 1
        
        # 1. Проверяем кэш
        cached_response = self._get_cached_response(message)
        if cached_response:
            return cached_response
        
        # 2. Проверяем быстрые ответы
        quick_response, needs_api = self._optimize_prompt(message)
        if not needs_api:
            self._cache_response(message, quick_response)
            return quick_response
        
        # 3. Проверяем токен только если нужен API вызов
        self._refresh_token_if_needed()
        
        if not self.access_token:
            return self._get_demo_response(message)
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            system_prompt, _ = self._optimize_prompt(message)
            
            payload = {
                "model": "GigaChat",
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
                "max_tokens": 400,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=False,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Сохраняем в кэш
                self._cache_response(message, ai_response)
                
                # Обновляем статистику токенов
                if 'usage' in result:
                    self.usage_stats['tokens_used'] += result['usage'].get('total_tokens', 0)
                
                return ai_response
            else:
                print(f"❌ GigaChat API error: {response.status_code} - {response.text}")
                demo_response = self._get_demo_response(message)
                self._cache_response(message, demo_response)
                return demo_response
                
        except Exception as e:
            print(f"❌ GigaChat request error: {e}")
            demo_response = self._get_demo_response(message)
            self._cache_response(message, demo_response)
            return demo_response
    
    def _get_demo_response(self, message: str) -> str:
        """Демо-ответы если GigaChat не доступен"""
        demo_responses = {
            "пароль": "🔐 **Надежный пароль:**\n• 12+ символов\n• Буквы, цифры, спецсимволы\n• Уникальные пароли\n• Менеджер паролей\n• 2FA",
            "фишинг": "🎣 **Защита от фишинга:**\n• Проверяйте отправителя\n• Не переходите по ссылкам\n• Внимание к грамматике\n• Антифишинг расширения",
            "wifi": "📡 **Безопасность Wi-Fi:**\n• WPA3 шифрование\n• Смените пароль роутера\n• Отключите WPS\n• Скрытый SSID",
            "антивирус": "🛡️ **Антивирусы:**\n• Windows Defender\n• Kaspersky/ESET\n• Регулярные обновления",
            "взлом": "🚨 **Если взломали:**\n• Смените пароли\n• Включите 2FA\n• Проверьте устройства\n• Сообщите в поддержку",
            "vpn": "🔒 **VPN:**\n• Используйте для публичных сетей\n• Проверяйте no-log политику\n• Избегайте бесплатных VPN",
        }
        
        msg_lower = message.lower()
        for key in demo_responses:
            if key in msg_lower:
                return demo_responses[key]
        
        return "🤖 GigaChat помощник по кибербезопасности. Спросите о:\n• Паролях\n• Фишинге\n• Wi-Fi\n• Антивирусах\n• VPN\n• Взломе"
    
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
            'token_expires_in': max(0, int(self.token_expires_at - time.time()))
        }
    
    def clear_cache(self):
        """Очищает кэш"""
        self.response_cache.clear()
        print("🧹 Кэш очищен")

# Создаем глобальный экземпляр
gigachat_client = OptimizedGigaChatClient()
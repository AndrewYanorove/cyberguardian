import os
import openai
from flask import current_app

class AIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        if self.api_key and self.api_key != 'your-openai-api-key-here':
            openai.api_key = self.api_key
            self.client = openai
        else:
            print("⚠️ OpenAI API ключ не настроен. Используется демо-режим.")
    
    def get_response(self, message):
        """Получение ответа от ИИ или демо-ответов"""
        try:
            # Демо-режим если API ключ не настроен
            if not self.client:
                return self.get_demo_response(message)
            
            # Реальный запрос к OpenAI
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """Ты эксперт по кибербезопасности. Отвечай на вопросы четко, профессионально, 
                        но доступным языком. Давай практические советы и рекомендации. 
                        Если вопрос не по теме, вежливо отклони ответ."""
                    },
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message['content'].strip()
            
        except Exception as e:
            print(f"Ошибка OpenAI: {e}")
            return self.get_demo_response(message)
    
    def get_demo_response(self, message):
        """Демо-ответы для презентации"""
        demo_responses = {
            "привет": "Привет! Я ваш ИИ-помощник по кибербезопасности. Чем могу помочь?",
            "как создать надежный пароль": "💡 Для надежного пароля:\n• Используйте 12+ символов\n• Комбинируйте буквы, цифры, спецсимволы\n• Не используйте личную информацию\n• Используйте разные пароли для разных сервисов\n• Рассмотрите менеджер паролей",
            "что такое фишинг": "🎣 Фишинг - это мошеннические рассылки, маскирующиеся под легитимные организации. \nПризнаки фишинга:\n• Срочные требования действий\n• Подозрительные ссылки\n• Грамматические ошибки\n• Незнакомые отправители",
            "как защитить wifi": "📡 Защита Wi-Fi:\n• Используйте WPA3 шифрование\n• Смените пароль роутера\n• Отключите WPS\n• Скрытие SSID\n• Регулярное обновление прошивки",
            "что такое двухфакторная аутентификация": "🔐 2FA - это дополнительный уровень безопасности:\n• Пароль + код из приложения\n• Пароль + SMS\n• Пароль + биометрия\nРекомендуется для всех важных аккаунтов!",
            "какой антивирус выбрать": "🛡️ Рекомендации по антивирусам:\n• Для Windows: Windows Defender + здравый смысл\n• Платные: Kaspersky, ESET, Bitdefender\n• Бесплатные: Avast, AVG\n• Главное - регулярные обновления!"
        }
        
        message_lower = message.lower()
        for key in demo_responses:
            if key in message_lower:
                return demo_responses[key]
        
        return "🤖 В демо-режиме. Для полного функционала настройте OPENAI_API_KEY в .env файле.\n\nНо я могу сказать: для кибербезопасности важно:\n• Регулярно обновлять ПО\n• Использовать надежные пароли\n• Включать 2FA\n• Остерегаться фишинга\n• Делать резервные копии"

# Глобальный экземпляр клиента
ai_client = AIClient()

import re
import html
from typing import Dict, Any

class SecurityUtils:
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Очистка пользовательского ввода"""
        if not text:
            return ""
        
        # Удаление потенциально опасных конструкций
        text = html.escape(text)
        text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+=\s*".*?"', '', text)
        
        return text.strip()
    
    @staticmethod
    def detect_question_complexity(question: str) -> str:
        """Определение сложности вопроса"""
        question_lower = question.lower()
        
        expert_keywords = ['apt', 'zero-day', 'siem', 'soar', 'ids/ips', 'soc', 'ndr', 'edr']
        advanced_keywords = ['firewall', 'vpn', 'encryption', 'malware', 'ransomware', 'ddos']
        
        if any(keyword in question_lower for keyword in expert_keywords):
            return "expert"
        elif any(keyword in question_lower for keyword in advanced_keywords):
            return "advanced"
        else:
            return "basic"

class ResponseFormatter:
    @staticmethod
    def format_ai_response(text: str) -> str:
        """Форматирование ответа AI для красивого отображения"""
        # Заменяем маркеры на эмодзи
        replacements = {
            '•': '•',
            '**': '<strong>',
            '__': '<strong>',
            '\n-': '\n•',
            '\n*': '\n•',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Форматируем списки
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip().startswith('•'):
                formatted_lines.append(f'<div class="list-item">{line}</div>')
            elif line.strip().startswith('🔐') or line.strip().startswith('🎣') or line.strip().startswith('📡'):
                formatted_lines.append(f'<div class="section-title">{line}</div>')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
"""
🛡️ МОДУЛЬ ЗАЩИТЫ ОТ XSS И CSRF АТАК
CyberGuardian - Максимальная защита от веб-атак
"""

import re
import html
import bleach
from typing import List, Dict, Optional, Union
from flask import request, g, session, abort, jsonify, make_response
from markupsafe import Markup, escape
from datetime import datetime, timedelta
import hashlib
import secrets

class XSSProtection:
    """🔒 Защита от XSS (Cross-Site Scripting) атак"""
    
    def __init__(self):
        # Разрешенные HTML теги и атрибуты
        self.allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
            'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        })
        
        self.allowed_attributes = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            'a': ['href', 'title', 'target'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'p': ['class'],
            'div': ['class', 'id'],
            'span': ['class', 'id'],
            'h1': ['class'], 'h2': ['class'], 'h3': ['class'], 'h4': ['class'], 'h5': ['class'], 'h6': ['class']
        }
        
        # Запрещенные паттерны
        self.malicious_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'data:',
            r'file:',
            r'ftp:',
            r'on\w+\s*=\s*["\'][^"\']*["\']',
            r'<\s*iframe[^>]*>',
            r'<\s*object[^>]*>',
            r'<\s*embed[^>]*>',
            r'<\s*form[^>]*action\s*=\s*["\'][^"\']*["\']',
            r'document\.cookie',
            r'document\.location',
            r'window\.location',
            r'eval\(',
            r'alert\(',
            r'confirm\(',
            r'prompt\(',
            r'setTimeout\(',
            r'setInterval\(',
            r'XMLHttpRequest',
            r'fetch\(',
            r'$.get\(',
            r'$.post\(',
            r'axios\.',
            r'fetch\('
        ]
    
    def sanitize_html(self, text: str, allowed_tags: Optional[set] = None, allowed_attrs: Optional[dict] = None) -> str:
        """Санитация HTML контента"""
        if not text:
            return ""
        
        # Применяем bleach для базовой санитации
        clean_text = bleach.clean(
            text,
            tags=allowed_tags or self.allowed_tags,
            attributes=allowed_attrs or self.allowed_attributes,
            protocols=['http', 'https', 'mailto'],
            strip=True
        )
        
        # Дополнительная проверка на вредоносные паттерны
        for pattern in self.malicious_patterns:
            if re.search(pattern, clean_text, re.IGNORECASE):
                # Если найден вредоносный паттерн, полностью очищаем HTML
                return html.escape(text)
        
        return clean_text
    
    def sanitize_input(self, text: str, max_length: int = 1000) -> str:
        """Санитация пользовательского ввода"""
        if not text:
            return ""
        
        # Ограничиваем длину
        text = text[:max_length]
        
        # Удаляем потенциально опасные символы
        text = re.sub(r'[<>"\'\\]', '', text)
        
        # Экранируем HTML
        return html.escape(text)
    
    def is_safe_url(self, url: str) -> bool:
        """Проверка безопасности URL"""
        if not url:
            return False
        
        # Разрешенные протоколы
        allowed_protocols = ['http:', 'https:', 'mailto:', 'tel:']
        
        # Проверяем, что URL начинается с разрешенного протокола
        for protocol in allowed_protocols:
            if url.startswith(protocol):
                return True
        
        # Проверяем относительные ссылки
        if url.startswith('/') or url.startswith('./') or url.startswith('../'):
            return True
        
        # Проверяем якоря
        if url.startswith('#'):
            return True
        
        return False

class CSRFProtection:
    """🛡️ Защита от CSRF (Cross-Site Request Forgery) атак"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or "cyberguardian-csrf-secret-2024"
        self.token_timeout = 3600  # 1 час
        
    def generate_csrf_token(self) -> str:
        """Генерация CSRF токена"""
        timestamp = str(datetime.now().timestamp())
        token_data = f"{session.get('session_id', '')}{timestamp}{self.secret_key}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        return token
    
    def get_csrf_token(self) -> str:
        """Получение CSRF токена из сессии"""
        if 'csrf_token' not in session or self.is_token_expired():
            session['csrf_token'] = self.generate_csrf_token()
            session['csrf_token_time'] = datetime.now().isoformat()
        return session['csrf_token']
    
    def is_token_expired(self) -> bool:
        """Проверка истечения токена"""
        if 'csrf_token_time' not in session:
            return True
        
        try:
            token_time = datetime.fromisoformat(session['csrf_token_time'])
            return (datetime.now() - token_time).seconds > self.token_timeout
        except:
            return True
    
    def validate_csrf_token(self, token: str) -> bool:
        """Валидация CSRF токена"""
        session_token = session.get('csrf_token')
        if not session_token or not token:
            return False
        
        # Проверяем соответствие токенов
        if secrets.compare_digest(session_token, token):
            return True
        
        return False
    
    def csrf_protect(self):
        """CSRF защита для POST/PUT/DELETE запросов"""
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            # Проверяем CSRF токен
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            
            if not token or not self.validate_csrf_token(token):
                abort(403, description='CSRF токен недействителен')
    
    def get_csrf_form_field(self) -> str:
        """Получение HTML поля для CSRF токена"""
        token = self.get_csrf_token()
        return f'<input type="hidden" name="csrf_token" value="{token}">'

class SecurityHeaders:
    """🔒 Управление заголовками безопасности"""
    
    @staticmethod
    def set_security_headers(response):
        """Установка заголовков безопасности"""
        # X-Content-Type-Options
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options
        response.headers['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Strict-Transport-Security (для HTTPS)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' https:; "
            "frame-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "upgrade-insecure-requests"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "accelerometer=(), "
            "gyroscope=(), "
            "magnetometer=()"
        )
        
        return response

class InputValidator:
    """🔍 Валидация входных данных"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Валидация email адреса"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Валидация имени пользователя"""
        if not username:
            return False
        
        # Только буквы, цифры и подчеркивания, от 3 до 30 символов
        pattern = r'^[a-zA-Z0-9_]{3,30}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, Union[bool, List[str]]]:
        """Валидация пароля"""
        if not password:
            return {'valid': False, 'errors': ['Пароль обязателен']}
        
        errors = []
        
        # Проверяем длину
        if len(password) < 8:
            errors.append('Пароль должен содержать минимум 8 символов')
        
        if len(password) > 128:
            errors.append('Пароль слишком длинный')
        
        # Проверяем сложность
        if not re.search(r'[a-z]', password):
            errors.append('Пароль должен содержать строчные буквы')
        
        if not re.search(r'[A-Z]', password):
            errors.append('Пароль должен содержать заглавные буквы')
        
        if not re.search(r'\d', password):
            errors.append('Пароль должен содержать цифры')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Пароль должен содержать специальные символы')
        
        # Проверяем на общие пароли
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in common_passwords:
            errors.append('Пароль слишком простой')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_file_upload(file, allowed_extensions: List[str] = None, max_size: int = 5 * 1024 * 1024) -> Dict[str, Union[bool, str]]:
        """Валидация загружаемых файлов"""
        if not file or not file.filename:
            return {'valid': False, 'error': 'Файл не выбран'}
        
        # Проверяем размер
        file.seek(0, 2)  # Переходим в конец файла
        file_size = file.tell()
        file.seek(0)  # Возвращаемся в начало
        
        if file_size > max_size:
            return {'valid': False, 'error': f'Размер файла превышает {max_size // (1024*1024)}MB'}
        
        # Проверяем расширение
        if allowed_extensions:
            file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if file_ext not in allowed_extensions:
                return {'valid': False, 'error': f'Тип файла не поддерживается. Разрешены: {", ".join(allowed_extensions)}'}
        
        # Проверяем имя файла на безопасность
        if not re.match(r'^[a-zA-Z0-9._-]+$', file.filename):
            return {'valid': False, 'error': 'Некорректное имя файла'}
        
        return {'valid': True, 'error': None}
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Санитация имени файла"""
        if not filename:
            return 'unnamed_file'
        
        # Удаляем опасные символы
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        
        # Ограничиваем длину
        filename = filename[:255]
        
        return filename

# Создаем глобальные экземпляры
xss_protection = XSSProtection()
csrf_protection = CSRFProtection()
input_validator = InputValidator()

def security_validation_middleware():
    """Middleware для валидации и защиты"""
    try:
        # CSRF защита
        csrf_protection.csrf_protect()
        
        # Валидация входных данных
        if request.method in ['POST', 'PUT', 'PATCH']:
            validate_request_data()
        
        # Добавляем информацию о проверке в g
        g.security_validated = True
        
    except Exception as e:
        print(f"❌ Ошибка в security validation: {e}")

def validate_request_data():
    """Валидация данных запроса"""
    # Валидация JSON данных
    if request.is_json:
        data = request.get_json()
        if data:
            for key, value in data.items():
                if isinstance(value, str):
                    # Санитация строковых данных
                    sanitized = xss_protection.sanitize_input(value)
                    if sanitized != value:
                        print(f"⚠️ Санитизированы данные в поле {key}")
    
    # Валидация form данных
    if request.form:
        for key, value in request.form.items():
            if isinstance(value, str):
                # Санитация form данных
                sanitized = xss_protection.sanitize_input(value)
                if sanitized != value:
                    print(f"⚠️ Санитизированы form данные в поле {key}")

def get_security_form_field():
    """Получение поля CSRF токена для форм"""
    return csrf_protection.get_csrf_form_field()

def safe_render_template(template_name, **context):
    """Безопасный рендеринг шаблона с автоматической санитацией"""
    from flask import render_template_string
    
    # Автоматически санитизируем контекст
    safe_context = {}
    for key, value in context.items():
        if isinstance(value, str):
            safe_context[key] = xss_protection.sanitize_input(value)
        else:
            safe_context[key] = value
    
    return render_template_string(template_name, **safe_context)

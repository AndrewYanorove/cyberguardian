"""
🔐 СИСТЕМА ШИФРОВАНИЯ И ЗАЩИТЫ ДАННЫХ
CyberGuardian - Защита конфиденциальной информации
"""

import os
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import InvalidToken
from typing import Dict, Optional, Tuple, Union
import base64
import json
import sqlite3
from datetime import datetime
from flask import request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

class DataEncryption:
    """🔒 Шифрование конфиденциальных данных"""
    
    def __init__(self, master_key: str = None):
        self.master_key = master_key or os.getenv('ENCRYPTION_MASTER_KEY', self._generate_master_key())
        self.key_salt = os.getenv('ENCRYPTION_SALT', base64.urlsafe_b64encode(os.urandom(16)).decode())
        self._setup_encryption()
    
    def _generate_master_key(self) -> str:
        """Генерация мастер-ключа"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    def _setup_encryption(self):
        """Настройка шифрования"""
        try:
            # Создаем производный ключ
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.key_salt.encode(),
                iterations=100000,
                backend=default_backend()
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            self.fernet = Fernet(key)
            
        except Exception as e:
            print(f"❌ Ошибка настройки шифрования: {e}")
            self.fernet = None
    
    def encrypt_data(self, data: str) -> Optional[str]:
        """Шифрование данных"""
        if not self.fernet or not data:
            return None
        
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"❌ Ошибка шифрования: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Расшифровка данных"""
        if not self.fernet or not encrypted_data:
            return None
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except InvalidToken:
            print("❌ Недействительный токен для расшифровки")
            return None
        except Exception as e:
            print(f"❌ Ошибка расшифровки: {e}")
            return None
    
    def hash_sensitive_data(self, data: str, salt: str = None) -> str:
        """Хеширование чувствительных данных"""
        if not salt:
            salt = secrets.token_hex(16)
        
        # Комбинируем данные с солью
        salted_data = data + salt
        hash_object = hashlib.sha256(salted_data.encode())
        return hash_object.hexdigest()
    
    def verify_hash(self, data: str, hash_value: str, salt: str) -> bool:
        """Проверка хеша"""
        expected_hash = self.hash_sensitive_data(data, salt)
        return secrets.compare_digest(expected_hash, hash_value)

class SecurePasswordManager:
    """🔐 Безопасное управление паролями"""
    
    def __init__(self):
        self.min_length = 8
        self.max_length = 128
        self.require_special_chars = True
        self.require_numbers = True
        self.require_uppercase = True
        self.require_lowercase = True
    
    def validate_password_strength(self, password: str) -> Dict[str, Union[bool, str, int]]:
        """Валидация силы пароля"""
        if not password:
            return {'valid': False, 'error': 'Пароль не может быть пустым'}
        
        errors = []
        score = 0
        
        # Проверяем длину
        if len(password) < self.min_length:
            errors.append(f'Минимум {self.min_length} символов')
        elif len(password) > self.max_length:
            errors.append(f'Максимум {self.max_length} символов')
        else:
            score += 20
        
        # Проверяем наличие заглавных букв
        if not any(c.isupper() for c in password):
            errors.append('Должна быть хотя бы одна заглавная буква')
        else:
            score += 20
        
        # Проверяем наличие строчных букв
        if not any(c.islower() for c in password):
            errors.append('Должна быть хотя бы одна строчная буква')
        else:
            score += 20
        
        # Проверяем наличие цифр
        if not any(c.isdigit() for c in password):
            errors.append('Должна быть хотя бы одна цифра')
        else:
            score += 20
        
        # Проверяем наличие специальных символов
        special_chars = '!@#$%^&*(),.?":{}|<>'
        if not any(c in special_chars for c in password):
            errors.append(f'Должен быть хотя бы один специальный символ ({special_chars})')
        else:
            score += 20
        
        # Проверяем на общие пароли
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            'dragon', 'sunshine', 'princess', 'football', 'login'
        ]
        
        if password.lower() in common_passwords:
            errors.append('Пароль слишком распространен')
            score = 0
        
        # Проверяем на последовательности
        sequential_patterns = ['123', 'abc', 'qwe', 'asd', 'zxc']
        for pattern in sequential_patterns:
            if pattern in password.lower():
                errors.append('Пароль содержит легко угадываемые последовательности')
                score -= 10
                break
        
        return {
            'valid': len(errors) == 0 and score >= 60,
            'errors': errors,
            'score': max(0, score),
            'strength': self._get_password_strength(score)
        }
    
    def _get_password_strength(self, score: int) -> str:
        """Определение уровня сложности пароля"""
        if score >= 80:
            return 'very_strong'
        elif score >= 60:
            return 'strong'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'weak'
        else:
            return 'very_weak'
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Проверка пароля"""
        return check_password_hash(password_hash, password)
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Генерация безопасного пароля"""
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        digits = '0123456789'
        special = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Гарантируем наличие всех типов символов
        password = [
            secrets.choice(uppercase),
            secrets.choice(lowercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Дополняем до нужной длины
        all_chars = uppercase + lowercase + digits + special
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))
        
        # Перемешиваем
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

class FileProtection:
    """📁 Защита файлов и директорий"""
    
    def __init__(self):
        self.allowed_extensions = {
            'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
            'document': ['pdf', 'doc', 'docx', 'txt', 'rtf'],
            'archive': ['zip', 'rar', '7z', 'tar', 'gz'],
            'video': ['mp4', 'avi', 'mov', 'wmv', 'flv'],
            'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg']
        }
        
        self.max_file_sizes = {
            'image': 10 * 1024 * 1024,  # 10MB
            'document': 50 * 1024 * 1024,  # 50MB
            'archive': 100 * 1024 * 1024,  # 100MB
            'video': 500 * 1024 * 1024,  # 500MB
            'audio': 100 * 1024 * 1024  # 100MB
        }
        
        self.dangerous_extensions = [
            'exe', 'bat', 'cmd', 'com', 'pif', 'scr', 'vbs', 'js', 'jar',
            'php', 'asp', 'aspx', 'jsp', 'sh', 'ps1', 'msi', 'dll'
        ]
    
    def validate_file_upload(self, file, file_type: str = 'document') -> Dict[str, Union[bool, str]]:
        """Валидация загружаемого файла"""
        if not file or not file.filename:
            return {'valid': False, 'error': 'Файл не выбран'}
        
        # Проверяем размер файла
        file.seek(0, 2)  # Переходим в конец файла
        file_size = file.tell()
        file.seek(0)  # Возвращаемся в начало
        
        max_size = self.max_file_sizes.get(file_type, 10 * 1024 * 1024)
        if file_size > max_size:
            return {'valid': False, 'error': f'Размер файла превышает {max_size // (1024*1024)}MB'}
        
        # Проверяем расширение
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if not file_ext:
            return {'valid': False, 'error': 'Файл должен иметь расширение'}
        
        # Проверяем на опасные расширения
        if file_ext in self.dangerous_extensions:
            return {'valid': False, 'error': f'Тип файла {file_ext} не разрешен'}
        
        # Проверяем на разрешенные расширения
        allowed_exts = self.allowed_extensions.get(file_type, [])
        if allowed_exts and file_ext not in allowed_exts:
            return {'valid': False, 'error': f'Тип файла не поддерживается. Разрешены: {", ".join(allowed_exts)}'}
        
        # Проверяем имя файла на безопасность
        if not self._is_safe_filename(file.filename):
            return {'valid': False, 'error': 'Некорректное имя файла'}
        
        return {'valid': True, 'error': None}
    
    def _is_safe_filename(self, filename: str) -> bool:
        """Проверка безопасности имени файла"""
        # Запрещенные символы
        dangerous_chars = '<>:"/\\|?*'
        
        for char in dangerous_chars:
            if char in filename:
                return False
        
        # Проверяем длину
        if len(filename) > 255:
            return False
        
        # Проверяем на путь
        if '..' in filename or filename.startswith('.'):
            return False
        
        return True
    
    def sanitize_filename(self, filename: str) -> str:
        """Санитация имени файла"""
        if not filename:
            return 'unnamed_file'
        
        # Удаляем опасные символы
        safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        safe_filename = ''.join(c if c in safe_chars else '_' for c in filename)
        
        # Ограничиваем длину
        safe_filename = safe_filename[:255]
        
        # Убираем множественные подчеркивания
        while '__' in safe_filename:
            safe_filename = safe_filename.replace('__', '_')
        
        return safe_filename or 'unnamed_file'
    
    def secure_file_path(self, base_path: str, filename: str) -> str:
        """Создание безопасного пути к файлу"""
        safe_filename = self.sanitize_filename(filename)
        return os.path.join(base_path, safe_filename)

class DatabaseProtection:
    """🗄️ Защита базы данных"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._setup_database_protection()
    
    def _setup_database_protection(self):
        """Настройка защиты базы данных"""
        try:
            # Включаем WAL режим для лучшей производительности и безопасности
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('PRAGMA journal_mode=WAL')
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.execute('PRAGMA secure_delete=ON')
            cursor.execute('PRAGMA temp_store=memory')
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Ошибка настройки защиты БД: {e}")
    
    def create_secure_table(self, table_name: str, columns: Dict[str, str]):
        """Создание защищенной таблицы"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Создаем SQL запрос
            columns_sql = ', '.join([f'"{col}" {col_type}' for col, col_type in columns.items()])
            sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})'
            
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Ошибка создания таблицы {table_name}: {e}")
    
    def encrypt_sensitive_column(self, table_name: str, column_name: str):
        """Шифрование чувствительного столбца"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Добавляем зашифрованный столбец
            encrypted_column = f"{column_name}_encrypted"
            cursor.execute(f'''
                ALTER TABLE "{table_name}" ADD COLUMN "{encrypted_column}" TEXT
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Ошибка шифрования столбца {column_name}: {e}")

# Создаем глобальные экземпляры
data_encryption = DataEncryption()
password_manager = SecurePasswordManager()
file_protection = FileProtection()

def encrypt_sensitive_data(data: str) -> str:
    """Удобная функция шифрования"""
    return data_encryption.encrypt_data(data)

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Удобная функция расшифровки"""
    return data_encryption.decrypt_data(encrypted_data)

def validate_file_security(file, file_type: str = 'document') -> Dict[str, Union[bool, str]]:
    """Удобная функция валидации файла"""
    return file_protection.validate_file_upload(file, file_type)

def generate_secure_password(length: int = 16) -> str:
    """Удобная функция генерации пароля"""
    return password_manager.generate_secure_password(length)

def validate_password_strength(password: str) -> Dict[str, Union[bool, str, int]]:
    """Удобная функция проверки пароля"""
    return password_manager.validate_password_strength(password)

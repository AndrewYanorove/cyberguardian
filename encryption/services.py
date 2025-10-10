# encryption/services.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime
import base64
import os

class EncryptionService:
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def encrypt_aes(text: str, password: str) -> dict:
        salt = os.urandom(16)
        key, salt = EncryptionService.derive_key(password, salt)
        fernet = Fernet(key)
        
        encrypted = fernet.encrypt(text.encode())
        return {
            'encrypted_text': base64.urlsafe_b64encode(encrypted).decode(),
            'salt': base64.urlsafe_b64encode(salt).decode()
        }

    @staticmethod
    def decrypt_aes(encrypted_text: str, password: str, salt: str) -> str:
        try:
            salt = base64.urlsafe_b64decode(salt.encode())
            encrypted = base64.urlsafe_b64decode(encrypted_text.encode())
            
            key, _ = EncryptionService.derive_key(password, salt)
            fernet = Fernet(key)
            
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            raise ValueError("Неверный пароль или поврежденные данные")

    @staticmethod
    def caesar_cipher(text: str, shift: int, encrypt: bool = True) -> str:
        result = []
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                shifted = (ord(char) - shift_base + (shift if encrypt else -shift)) % 26
                result.append(chr(shifted + shift_base))
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def xor_cipher(text: str, key: str) -> str:
        result = []
        key_length = len(key)
        for i, char in enumerate(text):
            result.append(chr(ord(char) ^ ord(key[i % key_length])))
        return ''.join(result)
    @staticmethod
    def obfuscate_metadata(encrypted_text: str, algorithm: str, salt: str = '') -> str:
        """Скрываем метаданные в зашифрованном тексте"""
        import hashlib
        import base64
        
        # Создаем скрытые маркеры для каждого алгоритма
        markers = {
            'AES': 'f1a2',      # Случайные hex-метки
            'Caesar': 'c3b4', 
            'XOR': 'x5y6'
        }
        
        # Преобразуем алгоритм в код
        algo_code = markers.get(algorithm.split(' ')[0], 'u7v8')
        
        # Для Caesar извлекаем shift
        if algorithm.startswith('Caesar'):
            shift = algorithm.split('shift ')[1].split(')')[0]
            algo_code += f"s{shift.zfill(2)}"
        
        # Собираем все данные в одну строку
        data_string = f"{algo_code}:{salt}:{encrypted_text}" if salt else f"{algo_code}::{encrypted_text}"
        
        # Кодируем в base64 для маскировки
        obfuscated = base64.b85encode(data_string.encode()).decode()
        
        return obfuscated
    
    @staticmethod
    def deobfuscate_metadata(obfuscated_text: str) -> tuple:
        """Извлекаем метаданные из обфусцированного текста"""
        import base64
        
        try:
            # Декодируем base85
            decoded = base64.b85decode(obfuscated_text.encode()).decode()
            parts = decoded.split(':', 2)
            
            if len(parts) != 3:
                raise ValueError("Неверный формат файла")
            
            algo_code, salt, encrypted_text = parts
            
            # Определяем алгоритм по коду
            markers = {
                'f1a2': 'AES',
                'c3b4': 'Caesar', 
                'x5y6': 'XOR'
            }
            
            algorithm_base = markers.get(algo_code[:4], 'Unknown')
            
            # Для Caesar извлекаем shift из кода
            if algorithm_base == 'Caesar' and len(algo_code) > 4:
                shift = int(algo_code[4:])
                algorithm = f'Caesar (shift {shift})'
            else:
                algorithm = algorithm_base
            
            # Если соль пустая, убираем ее
            salt = salt if salt else ''
            
            return encrypted_text, algorithm, salt
            
        except Exception as e:
            raise ValueError(f"Ошибка деобфускации: {str(e)}")
    
    @staticmethod
    def create_stealth_file(encrypted_text: str, algorithm: str, salt: str = '', original_filename: str = "document.txt") -> bytes:
        """Создает файл, который выглядит как обычный текстовый документ"""
        import random
        
        # Обфусцируем данные
        obfuscated = EncryptionService.obfuscate_metadata(encrypted_text, algorithm, salt)
        
        # Создаем "прикрытие" - файл выглядит как обычный документ
        stealth_content = f"""
# Этот файл был автоматически сгенерирован системой
# Document: {original_filename}
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 
# Содержимое документа:

{''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=') for _ in range(50))}
{obfuscated}
{''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=') for _ in range(50))}

# Конец документа
        """.strip()
        
        return stealth_content.encode('utf-8')
    
    @staticmethod
    def extract_from_stealth_file(file_content: bytes) -> tuple:
        """Извлекает зашифрованные данные из stealth-файла - УПРОЩЕННАЯ ВЕРСИЯ"""
        try:
            content = file_content.decode('utf-8')
            lines = content.split('\n')
        
            print(f"🔍 Анализируем файл, строк: {len(lines)}")  # Для отладки
        
            # Ищем строку с обфусцированными данными
            for i, line in enumerate(lines):
                line = line.strip()
                # Base85 строка обычно длинная и содержит специфические символы
                if len(line) > 50:  # Увеличиваем минимальную длину
                    print(f"📄 Строка {i}: {line[:50]}...")  # Для отладки
                
                    # Пробуем декодировать каждую длинную строку
                    try:
                        encrypted_text, algorithm, salt = EncryptionService.deobfuscate_metadata(line)
                        print(f"✅ Найдены данные: алгоритм={algorithm}")  # Для отладки
                        return encrypted_text, algorithm, salt
                    except Exception as e:
                        print(f"❌ Не подошла строка {i}: {str(e)}")  # Для отладки
                        continue
        
        # Если не нашли - пробуем найти по маркерам
            print("🔍 Пробуем поиск по маркерам...")
            full_text = content
            if 'f1a2:' in full_text or 'c3b4:' in full_text or 'x5y6:' in full_text:
            # Ищем начало base85 данных
                import re
                base85_pattern = r'([0-9A-Za-z!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]{50,})'
                matches = re.findall(base85_pattern, full_text)
            
                for match in matches:
                    try:
                        encrypted_text, algorithm, salt = EncryptionService.deobfuscate_metadata(match)
                        print(f"✅ Найдены данные через regex: алгоритм={algorithm}")
                        return encrypted_text, algorithm, salt
                    except:
                        continue
        
            raise ValueError("Не удалось найти зашифрованные данные в файле")
        
        except Exception as e:
            print(f"❌ Критическая ошибка: {str(e)}")  # Для отладки
            raise ValueError(f"Ошибка чтения stealth-файла: {str(e)}")
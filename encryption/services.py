# encryption/services.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from datetime import datetime

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

    # ПРОСТОЙ МЕТОД ДЛЯ ФАЙЛОВ
    @staticmethod
    def create_encrypted_file(encrypted_text: str, algorithm: str, salt: str = '', original_filename: str = "document.txt") -> bytes:
        """Создает JSON файл с зашифрованными данными"""
        file_data = {
            'version': '1.0',
            'algorithm': algorithm,
            'encrypted_text': encrypted_text,
            'salt': salt,
            'timestamp': datetime.now().isoformat(),
            'original_filename': original_filename,
            'created_by': 'CyberGuardian'
        }
        
        return json.dumps(file_data, indent=2, ensure_ascii=False).encode('utf-8')

    @staticmethod
    def extract_from_encrypted_file(file_content: bytes) -> tuple:
        """Извлекает данные из JSON файла"""
        try:
            content = file_content.decode('utf-8')
            file_data = json.loads(content)
            
            encrypted_text = file_data['encrypted_text']
            algorithm = file_data['algorithm']
            salt = file_data.get('salt', '')
            
            return encrypted_text, algorithm, salt
            
        except Exception as e:
            raise ValueError(f"Ошибка чтения файла: {str(e)}")
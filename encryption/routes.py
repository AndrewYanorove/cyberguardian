# encryption/routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from database import db  # Импортируем из корня проекта
from .models import EncryptionHistory
from .services import EncryptionService
from flask import send_file
from datetime import datetime
import json
from io import BytesIO

# Импортируем blueprint из __init__.py
from . import encryption_bp

def add_to_history(user_id, operation_type, algorithm, original_text, processed_text):
    record = EncryptionHistory(
        user_id=user_id,
        operation_type=operation_type,
        algorithm=algorithm,
        original_text=original_text,
        processed_text=processed_text
    )
    db.session.add(record)
    db.session.commit()
    return record

def get_user_history(user_id):
    return EncryptionHistory.query.filter_by(user_id=user_id).order_by(
        EncryptionHistory.timestamp.desc()
    ).all()

# Роуты (остальной код без изменений)
@encryption_bp.route('/')
def encryption_tools():
    return render_template('encryption/tools.html')

@encryption_bp.route('/text', methods=['GET', 'POST'])
def text_encryption():
    if request.method == 'POST':
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            password = data.get('password', '').strip()
            algorithm = data.get('algorithm', 'aes')
            
            if not text or not password:
                return jsonify({'error': 'Текст и пароль обязательны'}), 400
            
            if algorithm == 'aes':
                result = EncryptionService.encrypt_aes(text, password)
                encrypted_text = result['encrypted_text']
                salt = result['salt']
                
                if current_user.is_authenticated:
                    add_to_history(current_user.id, 'encrypt', 'AES', text, encrypted_text)
                
                return jsonify({
                    'success': True,
                    'encrypted_text': encrypted_text,
                    'salt': salt,
                    'algorithm': 'AES'
                })
                
            elif algorithm == 'caesar':
                shift = int(data.get('shift', 3))
                encrypted_text = EncryptionService.caesar_cipher(text, shift, True)
                
                if current_user.is_authenticated:
                    add_to_history(current_user.id, 'encrypt', f'Caesar (shift {shift})', text, encrypted_text)
                
                return jsonify({
                    'success': True,
                    'encrypted_text': encrypted_text,
                    'algorithm': f'Caesar (shift {shift})'
                })
                
            elif algorithm == 'xor':
                encrypted_text = EncryptionService.xor_cipher(text, password)
                
                if current_user.is_authenticated:
                    add_to_history(current_user.id, 'encrypt', 'XOR', text, encrypted_text)
                
                return jsonify({
                    'success': True,
                    'encrypted_text': encrypted_text,
                    'algorithm': 'XOR'
                })
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('encryption/text.html')

@encryption_bp.route('/decrypt', methods=['POST'])
def decrypt_text():
    try:
        data = request.get_json()
        encrypted_text = data.get('encrypted_text', '').strip()
        password = data.get('password', '').strip()
        algorithm = data.get('algorithm', '')
        salt = data.get('salt', '')
        
        if not encrypted_text or not password:
            return jsonify({'error': 'Текст и пароль обязательны'}), 400
        
        if algorithm.startswith('AES'):
            if not salt:
                return jsonify({'error': 'Соль обязательна для AES'}), 400
            
            decrypted_text = EncryptionService.decrypt_aes(encrypted_text, password, salt)
            
        elif algorithm.startswith('Caesar'):
            shift = int(algorithm.split('(')[1].split(')')[0].replace('shift', '').strip())
            decrypted_text = EncryptionService.caesar_cipher(encrypted_text, shift, False)
            
        elif algorithm == 'XOR':
            decrypted_text = EncryptionService.xor_cipher(encrypted_text, password)
            
        else:
            return jsonify({'error': 'Неизвестный алгоритм'}), 400
        
        if current_user.is_authenticated:
            add_to_history(current_user.id, 'decrypt', algorithm, encrypted_text, decrypted_text)
        
        return jsonify({
            'success': True,
            'decrypted_text': decrypted_text
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Ошибка дешифрования'}), 500

@encryption_bp.route('/history')
@login_required
def encryption_history():
    history = get_user_history(current_user.id)
    return render_template('encryption/history.html', history=history)

@encryption_bp.route('/api/history')
@login_required
def api_history():
    history = get_user_history(current_user.id)
    return jsonify({'history': [h.to_dict() for h in history]})


@encryption_bp.route('/file', methods=['GET', 'POST'])
def file_encryption():
    if request.method == 'POST':
        try:
            # Обработка загрузки файла для дешифровки
            if 'encrypted_file' in request.files:
                file = request.files['encrypted_file']
                password = request.form.get('password', '').strip()
                
                if not file or file.filename == '':
                    return jsonify({'error': 'Файл не выбран'}), 400
                
                if not password:
                    return jsonify({'error': 'Пароль обязателен'}), 400
                
                try:
                    # Читаем stealth-файл и извлекаем данные
                    file_content = file.read()
                    encrypted_text, algorithm, salt = EncryptionService.extract_from_stealth_file(file_content)
                    
                except Exception as e:
                    return jsonify({'error': f'Неверный формат файла: {str(e)}'}), 400
                
                # Дешифруем
                if algorithm.startswith('AES'):
                    if not salt:
                        return jsonify({'error': 'Для AES шифрования требуется соль'}), 400
                    decrypted_text = EncryptionService.decrypt_aes(encrypted_text, password, salt)
                elif algorithm.startswith('Caesar'):
                    try:
                        shift = int(algorithm.split('(')[1].split(')')[0].replace('shift', '').strip())
                        decrypted_text = EncryptionService.caesar_cipher(encrypted_text, shift, False)
                    except:
                        return jsonify({'error': 'Неверный формат алгоритма Caesar'}), 400
                elif algorithm == 'XOR':
                    decrypted_text = EncryptionService.xor_cipher(encrypted_text, password)
                else:
                    return jsonify({'error': 'Неизвестный алгоритм шифрования'}), 400
                
                if current_user.is_authenticated:
                    add_to_history(current_user.id, 'decrypt', algorithm, encrypted_text, decrypted_text)
                
                return jsonify({
                    'success': True,
                    'decrypted_text': decrypted_text,
                    'algorithm': algorithm
                })
            
            # Обработка шифрования текста и скачивания
            elif request.form.get('action') == 'encrypt_and_download':
                text = request.form.get('text', '').strip()
                password = request.form.get('password', '').strip()
                algorithm = request.form.get('algorithm', 'aes')
                filename = request.form.get('filename', 'document').strip()
                
                if not text or not password:
                    return jsonify({'error': 'Текст и пароль обязательны'}), 400
                
                # Шифруем текст
                if algorithm == 'aes':
                    result = EncryptionService.encrypt_aes(text, password)
                    encrypted_text = result['encrypted_text']
                    salt = result['salt']
                    algorithm_name = 'AES'
                elif algorithm == 'caesar':
                    shift = int(request.form.get('shift', 3))
                    encrypted_text = EncryptionService.caesar_cipher(text, shift, True)
                    salt = ''
                    algorithm_name = f'Caesar (shift {shift})'
                elif algorithm == 'xor':
                    encrypted_text = EncryptionService.xor_cipher(text, password)
                    salt = ''
                    algorithm_name = 'XOR'
                else:
                    return jsonify({'error': 'Неизвестный алгоритм'}), 400
                
                # Создаем stealth-файл
                file_content = EncryptionService.create_stealth_file(
                    encrypted_text, 
                    algorithm_name, 
                    salt, 
                    f"{filename}.txt"
                )
                
                if current_user.is_authenticated:
                    add_to_history(current_user.id, 'encrypt', algorithm_name, text, encrypted_text)
                
                # Создаем файл для скачивания
                output = BytesIO()
                output.write(file_content)
                output.seek(0)
                
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=f"{filename}.txt",  # Обычный .txt файл!
                    mimetype='text/plain'
                )
                
        except Exception as e:
            return jsonify({'error': f'Ошибка обработки файла: {str(e)}'}), 500
    
    return render_template('encryption/file.html')
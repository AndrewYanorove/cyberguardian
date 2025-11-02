from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Абсолютные импорты
from auth.models import db, User

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_password_strength(password):
    """Просто показываем силу пароля, но не блокируем регистрацию"""
    strength = 0
    feedback = []
    
    if len(password) >= 8:
        strength += 25
    else:
        feedback.append("минимум 8 символов")
    
    if re.search(r"[A-Z]", password):
        strength += 25
    else:
        feedback.append("заглавные буквы")
    
    if re.search(r"[a-z]", password):
        strength += 25
    else:
        feedback.append("строчные буквы")
    
    if re.search(r"\d", password):
        strength += 15
    else:
        feedback.append("цифры")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 10
    else:
        feedback.append("спецсимволы")
    
    return strength, feedback

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Валидация
        errors = []
        
        # Валидация имени пользователя
        if not username or len(username) < 3:
            errors.append('Имя пользователя должно содержать минимум 3 символа')
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Имя пользователя может содержать только буквы, цифры и подчеркивания')
        
        # Валидация email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Некорректный email адрес')
        
        # Проверка совпадения паролей
        if password != confirm_password:
            errors.append('Пароли не совпадают')
        
        # Проверка уникальности
        if User.query.filter_by(username=username).first():
            errors.append('Имя пользователя уже занято')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email уже зарегистрирован')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html', 
                                 username=username, 
                                 email=email)
        
        # Создание пользователя
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            # Автоматический вход после регистрации
            login_user(user)
            flash('Регистрация успешна! Добро пожаловать в CyberGuardian!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации. Попробуйте позже.', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = db.func.now()
            db.session.commit()
            
            flash(f'Добро пожаловать обратно, {username}!', 'success')
            
            # Перенаправление на запрошенную страницу или dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'Вы вышли из системы. Возвращайтесь, {username}!', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/check_username')
def check_username():
    """AJAX проверка доступности имени пользователя"""
    username = request.args.get('username', '')
    if len(username) < 3:
        return jsonify({'available': False, 'message': 'Минимум 3 символа'})
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'available': False, 'message': 'Имя занято'})
    else:
        return jsonify({'available': True, 'message': 'Доступно'})

@auth_bp.route('/check_email')
def check_email():
    """AJAX проверка email"""
    email = request.args.get('email', '')
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'valid': False, 'message': 'Некорректный email'})
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'valid': False, 'message': 'Email уже используется'})
    else:
        return jsonify({'valid': True, 'message': 'Email доступен'})

@auth_bp.route('/check_password', methods=['POST'])
def check_password():
    """AJAX проверка сложности пароля"""
    password = request.form.get('password', '')
    strength, feedback = get_password_strength(password)
    return jsonify({'strength': strength, 'feedback': feedback})

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
    login_manager.login_message_category = 'warning'

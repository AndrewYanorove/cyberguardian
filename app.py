from flask import Flask, render_template, jsonify, request , redirect, url_for , session
from flask_compress import Compress
from dotenv import load_dotenv
from flask import send_from_directory
import os
from datetime import datetime
import json
import sqlite3

# Загрузка переменных окружения
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'cyberguardian-super-secret-2024')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # 🔒 АБСОЛЮТНАЯ ЗАЩИТА БАЗЫ ДАННЫХ
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    db_path = os.path.join(os.path.abspath('instance'), 'cyberguardian.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Добавляем сжатие GZIP
    app.config['COMPRESS_ALGORITHM'] = 'gzip'
    app.config['COMPRESS_LEVEL'] = 6
    app.config['COMPRESS_MIN_SIZE'] = 500
    Compress(app)
    
    # Инициализация базы данных
    from database import db
    db.init_app(app)
    
    # Инициализация Flask-Login
    from auth.routes import init_login_manager
    init_login_manager(app)
    
    # Регистрируем blueprint'ы
    from auth.routes import auth_bp
    from education.routes import education_bp
    from passwords.routes import passwords_bp
    from encryption.routes import encryption_bp
    from ai_assistant.routes import ai_bp
    from threat_monitor.routes import threat_bp
    from security_scanner.routes import scanner_bp
    from cyber_games.routes import games_bp
    from templates.simulators.routes import simulators_bp
    from ddos_simulator.routes import ddos_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(education_bp, url_prefix='/education')
    app.register_blueprint(passwords_bp, url_prefix='/passwords')
    app.register_blueprint(encryption_bp, url_prefix='/encryption')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(threat_bp, url_prefix='/threats')
    app.register_blueprint(scanner_bp, url_prefix='/scanner')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(simulators_bp, url_prefix='/simulators')
    app.register_blueprint(ddos_bp, url_prefix='/ddos')

    # Контекстный процессор для глобальных переменных
    @app.context_processor
    def inject_global_vars():
        return {
            'current_year': datetime.now().year,
            'app_name': 'CyberGuardian',
            'app_version': '2.0.0',
            'user_count': 1500,
            'lessons_completed': 12500
        }
    
    # Главные маршруты
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/yandex_e87f9664d2590c4e.html')
    def yandex_verify():
        return """
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head>
        <body>Verification: e87f9664d2590c4e</body>
        </html>
        """
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'services': ['auth', 'education', 'encryption', 'ai', 'threats', 'scanner', 'games']
        })
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/sitemap.xml')
    def sitemap():
        return app.send_static_file('sitemap.xml')
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/admin', methods=['GET', 'POST'])
    def admin_panel():
        """Админ-панель с паролем в коде"""
        
        # Пароль прямо здесь - легко поменять!
        ADMIN_PASSWORD = "16795"  # 🔑 Ваш пароль
        
        # Выход из системы
        if request.args.get('logout'):
            session.pop('admin_authenticated', None)
            return redirect('/admin')
        
        # Проверка аутентификации
        authenticated = session.get('admin_authenticated', False)
        
        # Обработка формы входа
        if request.method == 'POST':
            password = request.form.get('admin_password', '')
            if password == ADMIN_PASSWORD:
                session['admin_authenticated'] = True
                session['admin_login_time'] = datetime.now().isoformat()
                authenticated = True
            else:
                return render_template('admin_panel.html', 
                                    authenticated=False, 
                                    error=True)
        
        # Если не аутентифицирован, показать форму входа
        if not authenticated:
            return render_template('admin_panel.html', 
                                authenticated=False, 
                                error=False)
        
        # Получение данных для админ-панели
        try:
            from auth.models import User
            from education.models import UserProgress
            from encryption.models import EncryptionHistory
            
            users = User.query.all()
            
            # Подготовка данных пользователей
            users_data = []
            for user in users:
                lessons_completed = UserProgress.query.filter_by(
                    user_id=user.id, 
                    completed=True
                ).count()
                
                encryption_count = EncryptionHistory.query.filter_by(
                    user_id=user.id
                ).count()
                
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at,
                    'lessons_completed': lessons_completed,
                    'encryption_count': encryption_count
                })
            
            # Общая статистика
            stats = {
                'total_users': len(users),
                'total_lessons': UserProgress.query.filter_by(completed=True).count(),
                'total_encryptions': EncryptionHistory.query.count(),
                'active_users': len([u for u in users_data if u['encryption_count'] > 0 or u['lessons_completed'] > 0])
            }
            
            return render_template('admin_panel.html',
                                authenticated=True,
                                users=users_data,
                                stats=stats)
            
        except Exception as e:
            return f"Ошибка загрузки данных: {str(e)}", 500

    # API для статистики
    @app.route('/api/stats')
    def get_stats():
        return jsonify({
            'users_online': 47,
            'active_threats': 3,
            'lessons_today': 128,
            'encryptions_today': 89,
            'ai_questions': 56
        })
    
    # Обработчик 404 ошибок
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    # Обработчик 500 ошибок
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    # Добавляем кэширование для всех ответов
    @app.after_request
    def add_cache_headers(response):
        if 'static' in request.path:
            response.headers['Cache-Control'] = 'public, max-age=31536000'
        elif response.content_type and 'text/html' in response.content_type:
            response.headers['Cache-Control'] = 'public, max-age=300'
        elif response.content_type and 'application/json' in response.content_type:
            response.headers['Cache-Control'] = 'public, max-age=30'
        
        return response
    
    # 🔒 УЛУЧШЕННАЯ ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ
    with app.app_context():
        try:
            from auth.models import User
            
            # Проверяем существует ли файл БД
            db_file = 'instance/cyberguardian.db'
            db_exists = os.path.exists(db_file)
            
            print(f"🔍 Проверка БД: {db_file}")
            print(f"📁 Файл БД существует: {db_exists}")
            
            if db_exists:
                # 🔒 ВАЖНО: НЕ пересоздаем таблицы если БД уже существует!
                # Только добавляем недостающие таблицы
                db.create_all()
                
                # Проверяем что данные на месте
                user_count = User.query.count()
                print(f"👤 Пользователей в БД: {user_count}")
                
                if user_count == 0:
                    print("⚠️ БД существует но пустая, создаем демо-данные...")
                    create_demo_data()
            else:
                # Создаем новую БД только если файла нет
                print("🆕 Создаем новую базу данных...")
                db.create_all()
                create_demo_data()
                
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")
            # НЕ пересоздаем БД, просто логируем ошибку
    
    return app

def create_demo_data():
    """Создание демо-данных только для ПУСТОЙ БД"""
    from database import db
    from auth.models import User
    from education.models import UserProgress
    from encryption.models import EncryptionHistory
    
    try:
        # Проверяем, есть ли уже пользователи
        if User.query.count() == 0:
            demo_user = User(
                username='demo',
                email='demo@cyberguardian.ru'
            )
            demo_user.set_password('demo123')
            
            db.session.add(demo_user)
            db.session.commit()
            print("👤 Демо-пользователь создан: demo / demo123")
            
    except Exception as e:
        print(f"⚠️ Ошибка создания демо-данных: {e}")
        db.session.rollback()

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    print("🚀 CyberGuardian 2.0 запускается...")
    print("🛡️ РЕЖИМ ПОЛНОЙ ЗАЩИТЫ ДАННЫХ АКТИВИРОВАН!")
    
    # СУПЕР-ПРОВЕРКА БАЗЫ ДАННЫХ
    try:
        from check_db import check_database_integrity, backup_database
        
        print("🔍 Проверяем целостность базы данных...")
        if check_database_integrity():
            print("✅ База данных готова к работе!")
        else:
            print("⚠️ Обнаружены проблемы с БД!")
            
        # Создаем резервную копию при КАЖДОМ запуске
        print("💾 Создаем резервную копию БД...")
        backup_database()
        
    except Exception as e:
        print(f"⚠️ Не удалось проверить БД: {e}")
    
    print("🎯 Новые функции: Threat Monitor, Security Scanner, Cyber Games!")
    print("📖 Документация: http://localhost:5000")
    print("🔧 Health check: http://localhost:5000/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
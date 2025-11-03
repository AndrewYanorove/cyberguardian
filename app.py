from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_compress import Compress
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import sqlite3
import shutil

# Загрузка переменных окружения
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'cyberguardian-super-secret-2024')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # 🔒 АВТОМАТИЧЕСКАЯ ЗАЩИТА БАЗЫ ДАННЫХ ДЛЯ RENDER
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # 🔥 ВАЖНО: Используем абсолютный путь для Render
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
    from forum.routes import forum_bp
    
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
    app.register_blueprint(forum_bp, url_prefix='/forum')

    # 🔥 АВТОМАТИЧЕСКАЯ ЗАЩИТА ДАННЫХ ПРИ КАЖДОМ ЗАПУСКЕ
    with app.app_context():
        auto_protect_database(app)

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
        """Админ-панель с защитой от ошибок БД"""
        
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
        
        # 🔥 ЗАЩИЩЕННАЯ ЗАГРУЗКА ДАННЫХ
        try:
            from auth.models import User
            from education.models import UserProgress
            from encryption.models import EncryptionHistory
            
            users = User.query.all()
            
            # Подготовка данных пользователей
            users_data = []
            for user in users:
                try:
                    lessons_completed = UserProgress.query.filter_by(
                        user_id=user.id, 
                        completed=True
                    ).count()
                except:
                    lessons_completed = 0
                
                try:
                    encryption_count = EncryptionHistory.query.filter_by(
                        user_id=user.id
                    ).count()
                except:
                    encryption_count = 0
                
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at,
                    'lessons_completed': lessons_completed,
                    'encryption_count': encryption_count
                })
            
            # Общая статистика
            try:
                total_lessons = UserProgress.query.filter_by(completed=True).count()
            except:
                total_lessons = 0
                
            try:
                total_encryptions = EncryptionHistory.query.count()
            except:
                total_encryptions = 0
            
            stats = {
                'total_users': len(users),
                'total_lessons': total_lessons,
                'total_encryptions': total_encryptions,
                'active_users': len([u for u in users_data if u['encryption_count'] > 0 or u['lessons_completed'] > 0])
            }
            
            return render_template('admin_panel.html',
                                authenticated=True,
                                users=users_data,
                                stats=stats)
            
        except Exception as e:
            return render_template('admin_panel.html',
                                authenticated=True,
                                users=[],
                                stats={'total_users': 0, 'total_lessons': 0, 'total_encryptions': 0, 'active_users': 0},
                                error_message=f"Временные проблемы с базой данных: {str(e)}")

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
    
    # 🔥 АВТОМАТИЧЕСКИЙ БЭКАП ЧЕРЕЗ API
    @app.route('/api/auto-backup', methods=['POST'])
    def auto_backup():
        """Автоматическое создание бэкапа (для cron jobs)"""
        try:
            if create_automatic_backup():
                return jsonify({'status': 'success', 'message': 'Backup created'})
            else:
                return jsonify({'status': 'error', 'message': 'Backup failed'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
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
    
    return app

def auto_protect_database(app):
    """Автоматическая защита базы данных при каждом запуске"""
    from database import db
    import sqlite3
    
    print("🛡️ АВТОМАТИЧЕСКАЯ ЗАЩИТА БАЗЫ ДАННЫХ...")
    
    db_path = 'instance/cyberguardian.db'
    persistent_backup = 'backups/persistent_backup.db'
    
    # 1. Создаем папки если их нет
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # 2. Если есть постоянный бэкап - восстанавливаем из него
    if os.path.exists(persistent_backup):
        print("💾 Обнаружен постоянный бэкап, восстанавливаем...")
        shutil.copy2(persistent_backup, db_path)
        print("✅ Данные восстановлены из постоянного бэкапа")
    
    # 3. Проверяем текущую БД
    db_exists = os.path.exists(db_path)
    print(f"📁 Текущая БД существует: {db_exists}")
    
    try:
        if db_exists:
            # Проверяем целостность существующей БД
            if check_database_integrity(db_path):
                print("✅ Текущая БД цела, обновляем структуру...")
                db.create_all()  # Только обновляем структуру
                
                # Создаем бэкап успешной БД
                create_automatic_backup()
            else:
                print("⚠️ Текущая БД повреждена, восстанавливаем...")
                restore_from_backup_or_create_new(db_path, persistent_backup, db)
        else:
            print("🆕 БД не существует, создаем новую...")
            db.create_all()
            create_demo_data()
            create_automatic_backup()
            
        # 4. Всегда создаем постоянный бэкап после успешной инициализации
        if os.path.exists(db_path):
            shutil.copy2(db_path, persistent_backup)
            print("💾 Создан постоянный бэкап для следующего деплоя")
            
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        # Пробуем восстановить
        restore_from_backup_or_create_new(db_path, persistent_backup, db)

def check_database_integrity(db_path):
    """Проверяет целостность базы данных"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем целостность
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        # Проверяем основные таблицы
        required_tables = ['user', 'user_progress', 'encryption_history']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Проверяем что все нужные таблицы существуют
        for table in required_tables:
            if table not in existing_tables:
                print(f"❌ Отсутствует таблица: {table}")
                return False
        
        conn.close()
        return result[0] == 'ok'
        
    except Exception as e:
        print(f"❌ Ошибка проверки целостности: {e}")
        return False

def restore_from_backup_or_create_new(db_path, backup_path, db):
    """Восстанавливает из бэкапа или создает новую БД"""
    if os.path.exists(backup_path):
        print("🔥 Восстанавливаем из бэкапа...")
        shutil.copy2(backup_path, db_path)
        db.create_all()  # Обновляем структуру
        print("✅ Восстановлено из бэкапа")
    else:
        print("💥 Бэкапа нет, создаем чистую БД...")
        db.create_all()
        create_demo_data()

def create_automatic_backup():
    """Создает автоматический бэкап"""
    try:
        source = 'instance/cyberguardian.db'
        if not os.path.exists(source):
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backups/auto_backup_{timestamp}.db'
        
        shutil.copy2(source, backup_file)
        
        # Сохраняем также как постоянный бэкап
        persistent_backup = 'backups/persistent_backup.db'
        shutil.copy2(source, persistent_backup)
        
        print(f"💾 Автоматический бэкап создан: {backup_file}")
        return True
        
    except Exception as e:
        print(f"⚠️ Ошибка создания бэкапа: {e}")
        return False

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
    print("🛡️ АВТОМАТИЧЕСКАЯ ЗАЩИТА ДАННЫХ АКТИВИРОВАНА!")
    print("🎯 Данные сохранятся при следующем деплое!")
    print("📖 Документация: http://localhost:5000")
    print("🔧 Health check: http://localhost:5000/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
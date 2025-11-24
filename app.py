from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_compress import Compress
from flask_caching import Cache
from dotenv import load_dotenv
import os
from datetime import datetime
import sqlite3
import shutil

# Загрузка переменных окружения
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'cyberguardian-super-secret-2024')
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Оптимизации для production
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 год для статических файлов
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # Минифицированный JSON
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB максимум
    
    # Создаем папки для базы данных и бэкапов
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # Путь к базе данных
    db_path = os.path.join(os.path.abspath('instance'), 'cyberguardian.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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

    # 🔥 УМНАЯ ЗАЩИТА ДАННЫХ ПРИ ЗАПУСКЕ
    with app.app_context():
        smart_database_protection(app)

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
        return render_template('yandex_verify.html')
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'database': os.path.exists('instance/cyberguardian.db')
        })
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/api/ping')
    def ping_service():
        """Простой пинг для мониторинга"""
        return jsonify({
            'status': 'alive',
            'timestamp': datetime.now().isoformat(),
            'service': 'CyberGuardian',
            'version': '2.0.0',
            'uptime': 'running'
        })

    @app.route('/api/health-deep')
    def deep_health_check():
        """Глубокий пинг с проверкой всех систем"""
        from database import db
        from auth.models import User
        
        checks = {
            'web_server': True,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Проверяем базу данных
            user_count = User.query.count()
            checks['database'] = True
            checks['user_count'] = user_count
        except Exception as e:
            checks['database'] = False
            checks['database_error'] = str(e)
        
        # Проверяем файловую систему
        try:
            checks['static_files'] = os.path.exists('static')
            checks['templates'] = os.path.exists('templates')
        except Exception as e:
            checks['filesystem_error'] = str(e)
        
        status_code = 200 if all(v for k, v in checks.items() if k in ['web_server', 'database']) else 500
        
        return jsonify(checks), status_code

    @app.route('/api/bot-friendly')
    def bot_friendly():
        """Очень легкий эндпоинт для ботов"""
        return "OK", 200
    
    @app.route('/sitemap.xml')
    def sitemap():
        return app.send_static_file('sitemap.xml')
    
    @app.route('/robots.txt')
    def robots():
        return app.send_static_file('robots.txt')
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/admin', methods=['GET', 'POST'])
    def admin_panel():
        """Админ-панель с защитой от ошибок БД"""
        try:
            ADMIN_PASSWORD = "16795"

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
                    return render_template('admin_panel.html', authenticated=False, error=True)

            # Если не аутентифицирован, показать форму входа
            if not authenticated:
                return render_template('admin_panel.html', authenticated=False, error=False)

            # Загрузка данных для админ-панели с оптимизацией
            def get_admin_stats():
                try:
                    from auth.models import User
                    from education.models import UserProgress
                    from encryption.models import EncryptionHistory

                    # Оптимизированные запросы с пагинацией
                    page = request.args.get('page', 1, type=int)
                    per_page = 20
                    users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
                    users = users_pagination.items

                    users_data = []
                    for user in users:
                        # Используем более эффективные запросы
                        lessons_completed = db.session.query(db.func.count(UserProgress.id)).filter_by(user_id=user.id, completed=True).scalar() or 0
                        encryption_count = db.session.query(db.func.count(EncryptionHistory.id)).filter_by(user_id=user.id).scalar() or 0

                        users_data.append({
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'created_at': user.created_at,
                            'lessons_completed': lessons_completed,
                            'encryption_count': encryption_count
                        })

                    # Общая статистика с кэшированием
                    total_users = User.query.count()
                    total_lessons = db.session.query(db.func.count(UserProgress.id)).filter_by(completed=True).scalar() or 0
                    total_encryptions = EncryptionHistory.query.count()

                    stats = {
                        'total_users': total_users,
                        'total_lessons': total_lessons,
                        'total_encryptions': total_encryptions,
                        'active_users': len([u for u in users_data if u['encryption_count'] > 0 or u['lessons_completed'] > 0])
                    }

                    return users_data, stats, users_pagination

                except Exception as e:
                    return [], {'total_users': 0, 'total_lessons': 0, 'total_encryptions': 0, 'active_users': 0}, None

            users_data, stats, users_pagination = get_admin_stats()

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

    # API для бэкапов
    @app.route('/api/backup-status')
    def backup_status():
        """API для проверки статуса бэкапов"""
        status = get_backup_status()
        return jsonify({
            'status': 'success',
            'data': status,
            'timestamp': datetime.now().isoformat()
        })

    @app.route('/api/create-backup-now', methods=['POST'])
    def create_backup_now():
        """Принудительное создание бэкапа"""
        try:
            create_persistent_backup()
            return jsonify({
                'status': 'success',
                'message': 'Backup created successfully',
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

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
    
    # Обработчик ошибок
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    # Оптимизированное кэширование
    @app.after_request
    def add_cache_headers(response):
        if 'static' in request.path:
            # Агрессивное кэширование статических файлов (1 год)
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            response.headers['Expires'] = 'Mon, 01 Jan 2030 00:00:00 GMT'
        elif response.content_type and 'text/html' in response.content_type:
            # Кэширование HTML на 5 минут
            response.headers['Cache-Control'] = 'public, max-age=300'
        elif response.content_type and 'application/json' in response.content_type:
            # Кэширование API ответов на 1 минуту
            response.headers['Cache-Control'] = 'public, max-age=60'

        # Дополнительные оптимизации
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    
    return app

def smart_database_protection(app):
    """ПРОСТАЯ защита - всегда использует текущие данные"""
    from database import db
    
    print("🔄 ПРОСТАЯ ЗАЩИТА ДАННЫХ...")
    
    try:
        # ВСЕГДА создаем/обновляем структуру БД
        db.create_all()
        print("✅ Структура БД обновлена")
        
        from education.progress_service import ProgressService
        ProgressService.initialize_course_data()
        
        # Проверяем, нужно ли добавить демо-данные
        try:
            from auth.models import User
            if User.query.count() == 0:
                create_demo_data()
                print("👤 Добавлены демо-данные")
        except:
            print("⚠️ Не удалось проверить пользователей")
        
        # ВСЕГДА создаем бэкап текущего состояния
        create_persistent_backup()
        print("💾 Создан бэкап текущих данных")
        
        print("🎯 Данные защищены!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        # Пробуем просто создать БД
        db.create_all()

def check_database_integrity(db_path):
    """Проверяет целостность базы данных"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем целостность
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        # Проверяем основные таблицы
        required_tables = ['user', 'user_progress', 'encryption_history', 'story_comments']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Проверяем что все нужные таблицы существуют
        for table in required_tables:
            if table not in existing_tables:
                print(f"❌ Отсутствует таблица: {table}")
                conn.close()
                return False
        
        conn.close()
        integrity_ok = result[0] == 'ok'
        print(f"🔍 Целостность БД: {integrity_ok}")
        return integrity_ok
        
    except Exception as e:
        print(f"❌ Ошибка проверки целостности: {e}")
        return False

def create_persistent_backup():
    """Создает постоянный бэкап"""
    try:
        source = 'instance/cyberguardian.db'
        if not os.path.exists(source):
            return False
            
        backup_file = 'backups/persistent_backup.db'
        shutil.copy2(source, backup_file)
        
        # Также создаем бэкап с timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        auto_backup = f'backups/auto_backup_{timestamp}.db'
        shutil.copy2(source, auto_backup)
        
        print(f"💾 Бэкап создан: {backup_file}")
        return True
        
    except Exception as e:
        print(f"⚠️ Ошибка создания бэкапа: {e}")
        return False

def get_backup_status():
    """Возвращает статус бэкапов"""
    status = {
        'current_db_exists': os.path.exists('instance/cyberguardian.db'),
        'persistent_backup_exists': os.path.exists('backups/persistent_backup.db'),
        'current_db_size': 0,
        'backup_size': 0,
        'auto_backups_count': 0
    }
    
    if status['current_db_exists']:
        status['current_db_size'] = os.path.getsize('instance/cyberguardian.db')
    
    if status['persistent_backup_exists']:
        status['backup_size'] = os.path.getsize('backups/persistent_backup.db')
    
    # Считаем авто-бэкапы
    if os.path.exists('backups'):
        status['auto_backups_count'] = len([
            f for f in os.listdir('backups') 
            if f.startswith('auto_backup_') and f.endswith('.db')
        ])
    
    return status

def create_demo_data():
    """Создание демо-данных только для ПУСТОЙ БД"""
    from database import db
    from auth.models import User
    
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
    print("🛡️ УМНАЯ СИСТЕМА ЗАЩИТЫ ДАННЫХ АКТИВИРОВАНА!")
    print("💾 Бэкапы создаются автоматически при каждом запуске")
    print("📖 Документация: http://localhost:8006")
    print("🔧 Health check: http://localhost:5000/health")
    print("🔍 Backup status: http://localhost:5000/api/backup-status")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8006)
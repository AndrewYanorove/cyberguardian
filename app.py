from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
from datetime import datetime
import json

# Загрузка переменных окружения
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'cyberguardian-super-secret-2024')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cyberguardian.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
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
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
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
    
    # Создаем таблицы при запуске
    with app.app_context():
        try:
            db.create_all()
            print("✅ База данных инициализирована успешно!")
            print("🔄 Создаем демо-данные...")
            create_demo_data()
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")
    
    return app

def create_demo_data():
    """Создание демо-данных при первом запуске"""
    from database import db
    from auth.models import User
    from education.models import UserProgress
    from encryption.models import EncryptionHistory
    
    try:
        # Проверяем, есть ли уже пользователи
        if User.query.count() == 0:
            demo_user = User(
                username='demo',
                email='demo@cyberguardian.ru',
                password_hash='pbkdf2:sha256:260000$abc123$def456'
            )
            demo_user.set_password('demo123')  # Для реального использования
            
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
    print("🎯 Новые функции: Threat Monitor, Security Scanner, Cyber Games!")
    print("📖 Документация: http://localhost:5000")
    print("🔧 Health check: http://localhost:5000/health")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
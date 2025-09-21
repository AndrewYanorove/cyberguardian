from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
from auth.models import db
from auth.routes import init_login_manager  # Добавляем импорт
from encryption.routes import encryption_bp
# Загрузка переменных окружения
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cyberguardian.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Инициализация базы данных
    db.init_app(app)
    
    # Инициализация Flask-Login
    init_login_manager(app)  # Добавляем эту строку
    
    # Импортируем и регистрируем blueprint'ы
    from auth.routes import auth_bp
    from education.routes import education_bp
    from passwords.routes import passwords_bp
    from encryption.routes import encryption_bp
    from ai_assistant.routes import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(education_bp, url_prefix='/education')
    app.register_blueprint(passwords_bp, url_prefix='/passwords')
    app.register_blueprint(encryption_bp, url_prefix='/encryption')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    
    @app.route('/')
    def index():
        return render_template('index.html', current_year=datetime.now().year)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
    
    # Добавь в app.py после главной страницы
    @app.route('/about')
    def about():
        return render_template('about.html', current_year=datetime.now().year)
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html', current_year=datetime.now().year)
    
    # Создаем таблицы при первом запуске
    with app.app_context():
        db.create_all()
    
    return app

# Создаем экземпляр приложения
app = create_app()

if __name__ == '__main__':
    print("🚀 CyberGuardian запущен на http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
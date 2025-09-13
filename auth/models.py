from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Прогресс пользователя
    completed_lessons = db.Column(db.Text, default='[]')  # JSON список пройденных уроков
    password_strength_score = db.Column(db.Integer, default=0)
    encryption_usage = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_completed_lesson(self, lesson_id):
        lessons = json.loads(self.completed_lessons)
        if lesson_id not in lessons:
            lessons.append(lesson_id)
            self.completed_lessons = json.dumps(lessons)
    
    def get_progress(self):
        lessons = json.loads(self.completed_lessons)
        return {
            'completed_lessons': len(lessons),
            'password_score': self.password_strength_score,
            'encryption_usage': self.encryption_usage
        }
    
    # Методы, необходимые для Flask-Login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
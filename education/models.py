from database import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(50))
    estimated_time = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0.0)
    students_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.String(100), primary_key=True)
    course_id = db.Column(db.String(100), db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    difficulty = db.Column(db.String(50))
    estimated_time = db.Column(db.String(50))
    order_index = db.Column(db.Integer, default=0)

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.String(100), primary_key=True)
    module_id = db.Column(db.String(100), db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, default=0)  # в минутах
    content = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    order_index = db.Column(db.Integer, default=0)
    has_quiz = db.Column(db.Boolean, default=False)
    has_practice = db.Column(db.Boolean, default=False)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(100), nullable=False)
    module_id = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # в секундах
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Убираем ForeignKey к lesson чтобы избежать циклических зависимостей
    # lesson_id = db.Column(db.String(100), db.ForeignKey('lessons.id'), nullable=False)
    
    # Уникальный constraint для прогресса пользователя по уроку
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'module_id': self.module_id,
            'lesson_id': self.lesson_id,
            'completed': self.completed,
            'score': self.score,
            'time_spent': self.time_spent,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat()
        }

class CourseCertificate(db.Model):
    __tablename__ = 'course_certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(100), nullable=False)
    certificate_id = db.Column(db.String(100), unique=True)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_name = db.Column(db.String(200), nullable=False)
    achievement_description = db.Column(db.Text)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)
    icon = db.Column(db.String(100))
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json


class User(db.Model):
    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)


    # Безопасность и блокировка
    user_is_active = db.Column(db.Boolean, default=True)
    banned_reason = db.Column(db.Text, nullable=True)
    banned_at = db.Column(db.DateTime, nullable=True)
    banned_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Прогресс пользователя
    completed_lessons = db.Column(db.Text, default="[]")
    password_strength_score = db.Column(db.Integer, default=0)
    encryption_usage = db.Column(db.Integer, default=0)

    def set_password(self, password):
        if not password or len(password.strip()) == 0:
            raise ValueError("Пароль не может быть пустым")
        if len(password) < 3:
            raise ValueError("Пароль должен содержать минимум 3 символа")
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
            "completed_lessons": len(lessons),
            "password_score": self.password_strength_score,
            "encryption_usage": self.encryption_usage,
        }


    # Методы, необходимые для Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.user_is_active and self.banned_reason is None

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"

    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        # Простая проверка - можно расширить системой ролей
        admin_emails = [
            "admin@cyberguardian.ru",
            "your-email@example.com",
        ]  # Добавьте email админов
        return self.email in admin_emails


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )  # ИЗМЕНИТЕ 'user.id' на 'users.id'
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="RUB")
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default="pending")
    transaction_id = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Связь с пользователем
    user = db.relationship("User", backref=db.backref("donations", lazy=True))

    purpose = db.Column(db.String(200), default="general")
    is_monthly = db.Column(db.Boolean, default=False)
    is_anonymous = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Donation {self.id} {self.amount} {self.status}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_anonymous": self.is_anonymous,
        }

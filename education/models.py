from database import db
from datetime import datetime

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'lesson_id': self.lesson_id,
            'completed': self.completed,
            'score': self.score,
            'time_spent': self.time_spent,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
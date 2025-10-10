# encryption/models.py
from database import db  # Импортируем из корня проекта
from datetime import datetime

class EncryptionHistory(db.Model):
    __tablename__ = 'encryption_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    operation_type = db.Column(db.String(20), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    processed_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'operation_type': self.operation_type,
            'algorithm': self.algorithm,
            'original_text': self.original_text,
            'processed_text': self.processed_text,
            'timestamp': self.timestamp.isoformat()
        }
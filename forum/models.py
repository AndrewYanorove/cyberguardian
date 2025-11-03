# [file name]: forum/models.py
from database import db
from datetime import datetime
import json

class ForumStory(db.Model):
    __tablename__ = 'forum_stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='scam')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # УБИРАЕМ is_approved - пока не нужно
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200))
    
    author = db.relationship('User', backref=db.backref('stories', lazy=True))
    comments = db.relationship('StoryComment', backref='story', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('StoryLike', backref='story', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author.username,
            'created_at': self.created_at.isoformat(),
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'tags': self.tags.split(',') if self.tags else [],
            'comment_count': len(self.comments)
        }

class StoryComment(db.Model):
    __tablename__ = 'story_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('forum_stories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # УБИРАЕМ is_approved и parent_comment_id - упрощаем
    # is_approved = db.Column(db.Boolean, default=True)
    # parent_comment_id = db.Column(db.Integer, db.ForeignKey('story_comments.id'), nullable=True)
    
    author = db.relationship('User', backref=db.backref('story_comments', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.isoformat(),
        }

class StoryLike(db.Model):
    __tablename__ = 'story_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('forum_stories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('story_likes', lazy=True))
# [file name]: forum/routes.py (упрощенная версия)
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from database import db
from forum.models import ForumStory, StoryComment, StoryLike
from datetime import datetime

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')

@forum_bp.route('/')
def forum_home():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    
    # Упрощаем запрос - убираем фильтр по is_approved
    query = ForumStory.query
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    stories = query.order_by(ForumStory.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    categories = [
        {'id': 'scam', 'name': 'Мошенничество', 'count': ForumStory.query.filter_by(category='scam').count()},
        {'id': 'phishing', 'name': 'Фишинг', 'count': ForumStory.query.filter_by(category='phishing').count()},
        {'id': 'social', 'name': 'Социальная инженерия', 'count': ForumStory.query.filter_by(category='social').count()},
        {'id': 'other', 'name': 'Другие случаи', 'count': ForumStory.query.filter_by(category='other').count()}
    ]
    
    return render_template('forum/forum_home.html', 
                         stories=stories,
                         categories=categories,
                         current_category=category)

@forum_bp.route('/story/<int:story_id>')
def story_detail(story_id):
    story = ForumStory.query.get_or_404(story_id)
    
    # Увеличиваем счетчик просмотров
    story.views_count += 1
    db.session.commit()
    
    return render_template('forum/story_detail.html', story=story)

@forum_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_story():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'scam')
        tags = request.form.get('tags', '').strip()
        
        if not title or not content:
            flash('Заполните все обязательные поля', 'danger')
            return render_template('forum/create_story.html')
        
        story = ForumStory(
            title=title,
            content=content,
            category=category,
            author_id=current_user.id,
            tags=tags
        )
        
        db.session.add(story)
        db.session.commit()
        
        flash('Ваша история успешно опубликована!', 'success')
        return redirect(url_for('forum.story_detail', story_id=story.id))
    
    return render_template('forum/create_story.html')

@forum_bp.route('/story/<int:story_id>/comment', methods=['POST'])
@login_required
def add_comment(story_id):
    story = ForumStory.query.get_or_404(story_id)
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Комментарий не может быть пустым', 'danger')
        return redirect(url_for('forum.story_detail', story_id=story_id))
    
    comment = StoryComment(
        content=content,
        author_id=current_user.id,
        story_id=story_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Комментарий добавлен', 'success')
    return redirect(url_for('forum.story_detail', story_id=story_id))

@forum_bp.route('/story/<int:story_id>/like', methods=['POST'])
@login_required
def like_story(story_id):
    story = ForumStory.query.get_or_404(story_id)
    
    existing_like = StoryLike.query.filter_by(
        user_id=current_user.id,
        story_id=story_id
    ).first()
    
    if existing_like:
        db.session.delete(existing_like)
        story.likes_count -= 1
        liked = False
    else:
        like = StoryLike(user_id=current_user.id, story_id=story_id)
        db.session.add(like)
        story.likes_count += 1
        liked = True
    
    db.session.commit()
    
    return jsonify({
        'liked': liked,
        'likes_count': story.likes_count
    })

# API для статистики
@forum_bp.route('/api/stats')
def forum_stats():
    total_stories = ForumStory.query.count()
    total_comments = StoryComment.query.count()
    total_views = db.session.query(db.func.sum(ForumStory.views_count)).scalar() or 0
    
    return jsonify({
        'total_stories': total_stories,
        'total_comments': total_comments,
        'total_views': total_views,
        'stories_today': ForumStory.query.filter(
            ForumStory.created_at >= datetime.utcnow().date()
        ).count()
    })

# АДМИН-РОУТЫ - ДОБАВЬ ЭТО В КОНЕЦ ФАЙЛА

@forum_bp.route('/admin')
def admin_panel():
    """Панель модерации"""
    stories = ForumStory.query.order_by(ForumStory.created_at.desc()).all()
    total_comments = StoryComment.query.count()
    total_views = db.session.query(db.func.sum(ForumStory.views_count)).scalar() or 0
    stories_today = ForumStory.query.filter(
        ForumStory.created_at >= datetime.utcnow().date()
    ).count()
    
    return render_template('forum/admin_panel.html', 
                         stories=stories,
                         total_comments=total_comments,
                         total_views=total_views,
                         stories_today=stories_today)

@forum_bp.route('/admin/story/<int:story_id>/delete', methods=['POST'])
def delete_story(story_id):
    """Удаление истории"""
    story = ForumStory.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    
    flash('История удалена', 'success')
    return redirect(url_for('forum.admin_panel'))

@forum_bp.route('/admin/story/<int:story_id>/edit', methods=['GET', 'POST'])
def edit_story(story_id):
    """Редактирование истории"""
    story = ForumStory.query.get_or_404(story_id)
    
    if request.method == 'POST':
        story.title = request.form.get('title')
        story.content = request.form.get('content')
        story.category = request.form.get('category')
        story.tags = request.form.get('tags')
        
        db.session.commit()
        flash('История обновлена', 'success')
        return redirect(url_for('forum.admin_panel'))
    
    return render_template('forum/edit_story.html', story=story)

# API для получения всех историй (для админки)
@forum_bp.route('/api/stories')
def get_all_stories():
    stories = ForumStory.query.order_by(ForumStory.created_at.desc()).all()
    return jsonify([{
        'id': story.id,
        'title': story.title,
        'author': story.author.username,
        'created_at': story.created_at.strftime('%d.%m.%Y %H:%M'),
        'views_count': story.views_count,
        'likes_count': story.likes_count,
        'content_preview': story.content[:100] + '...' if len(story.content) > 100 else story.content
    } for story in stories])


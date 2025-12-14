"""
Маршруты админ-панели CyberGuardian
Безопасное управление пользователями и системой
"""

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from datetime import datetime, timedelta
from functools import wraps



# Импортируем blueprint из модуля
from . import admin_bp


# Импорты из основного приложения
from database import db
from auth.models import User
from education.models import UserProgress
from encryption.models import EncryptionHistory
from forum.models import ForumStory

# Импорты системы безопасности
from security.web_protection import csrf_protection, xss_protection, input_validator, SecurityHeaders
from security.auth_security import rate_limiter, brute_force_protection, session_security, session_security_check, rate_limit
from security.intrusion_prevention import security_middleware, threat_detector, get_security_stats, force_block_ip, unblock_ip

# Константа для пароля администратора
ADMIN_PASSWORD = "16795"

def admin_required(f):
    """Декоратор для проверки аутентификации администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated', False):
            if request.is_json:
                return jsonify({'error': 'Требуется аутентификация администратора'}), 403
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/', methods=['GET', 'POST'])
@rate_limit('general')
@session_security_check
def admin_panel():
    """Главная страница админ-панели с полным управлением безопасностью"""
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # Выход из системы
        if request.args.get('logout'):
            session_security.invalidate_session(session.get('session_id', ''))
            session.clear()
            return redirect('/admin')

        # Проверка аутентификации
        authenticated = session.get('admin_authenticated', False)

        # Обработка формы входа
        if request.method == 'POST':
            password = request.form.get('admin_password', '')
            if password == ADMIN_PASSWORD:
                session['admin_authenticated'] = True
                session['admin_login_time'] = datetime.now().isoformat()
                session['admin_ip'] = ip
                session_security.store_session_fingerprint(session['session_id'], request)
                
                # Записываем успешную попытку
                brute_force_protection.record_successful_attempt(ip)
                authenticated = True
            else:
                # Записываем неудачную попытку
                brute_force_protection.record_failed_attempt(ip)
                return render_template('admin_panel.html', authenticated=False, error=True)

        # Если не аутентифицирован, показать форму входа
        if not authenticated:
            # Генерируем CSRF токен для формы входа
            csrf_token = csrf_protection.get_csrf_token()
            return render_template('admin_panel.html', authenticated=False, error=False, csrf_token=csrf_token)

        # Загрузка данных для админ-панели с безопасностью
        def get_admin_stats():
            try:
                # Безопасная пагинация
                page = request.args.get('page', 1, type=int)
                per_page = 20
                page = max(1, min(page, 100))  # Ограничиваем страницу
                
                users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
                users = users_pagination.items

                users_data = []
                for user in users:
                    # Санитизируем данные пользователя
                    safe_username = xss_protection.sanitize_input(user.username, max_length=50)
                    safe_email = xss_protection.sanitize_input(user.email, max_length=100)
                    
                    lessons_completed = db.session.query(db.func.count(UserProgress.id)).filter_by(user_id=user.id, completed=True).scalar() or 0
                    encryption_count = db.session.query(db.func.count(EncryptionHistory.id)).filter_by(user_id=user.id).scalar() or 0

                    users_data.append({
                        'id': user.id,
                        'username': safe_username,
                        'email': safe_email,
                        'created_at': user.created_at,
                        'lessons_completed': lessons_completed,
                        'encryption_count': encryption_count,
                        'is_active': user.is_active  # Используем property is_active
                    })

                # Статистика с проверкой безопасности
                total_users = User.query.count()
                total_lessons = db.session.query(db.func.count(UserProgress.id)).filter_by(completed=True).scalar() or 0
                total_encryptions = EncryptionHistory.query.count()

                # Получаем статистику безопасности
                security_stats = get_security_stats()

                stats = {
                    'total_users': total_users,
                    'total_lessons': total_lessons,
                    'total_encryptions': total_encryptions,
                    'active_users': len([u for u in users_data if u['encryption_count'] > 0 or u['lessons_completed'] > 0]),
                    'security_stats': security_stats,
                    'blocked_ips_count': len(threat_detector.blocked_ips),
                    'threats_last_24h': security_stats.get('threats_last_24h', 0)
                }

                return users_data, stats, users_pagination

            except Exception as e:
                return [], {
                    'total_users': 0, 
                    'total_lessons': 0, 
                    'total_encryptions': 0, 
                    'active_users': 0,
                    'security_stats': {},
                    'blocked_ips_count': 0,
                    'threats_last_24h': 0
                }, None


        users_data, stats, users_pagination = get_admin_stats()
        
        # Получаем CSRF токен для JS запросов
        csrf_token = csrf_protection.get_csrf_token()

        return render_template('admin_panel.html',
                            authenticated=True,
                            users=users_data,
                            stats=stats,
                            users_pagination=users_pagination,
                            csrf_token=csrf_token)

    except Exception as e:
        return render_template('admin_panel.html',
                            authenticated=True,
                            users=[],
                            stats={'total_users': 0, 'total_lessons': 0, 'total_encryptions': 0, 'active_users': 0, 'security_stats': {}, 'blocked_ips_count': 0, 'threats_last_24h': 0},
                            error_message=f"Временные проблемы с базой данных: {str(e)}")

@admin_bp.route('/delete-user', methods=['POST'])
@rate_limit('api')
@admin_required
def delete_user_api():
    """Удаление пользователя администратором"""
    try:
        # Поддерживаем как JSON, так и form данные
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'ID пользователя обязателен'}), 400
        
        user_id = data['user_id']
        
        # Проверяем валидность ID
        try:
            user_id = int(user_id)
            if user_id <= 0:
                return jsonify({'error': 'Некорректный ID пользователя'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'ID пользователя должен быть числом'}), 400
        
        # Находим пользователя
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        # Защищаем от удаления самого себя
        if session.get('admin_user_id') == user_id:
            return jsonify({'error': 'Нельзя удалить самого себя'}), 400
        
        # Удаляем связанные данные
        try:
            # Удаляем прогресс обучения
            UserProgress.query.filter_by(user_id=user_id).delete()
            
            # Удаляем историю шифрования
            EncryptionHistory.query.filter_by(user_id=user_id).delete()
            
            # Удаляем самого пользователя
            username = user.username
            db.session.delete(user)
            db.session.commit()
            
            print(f"🗑️ Администратор удалил пользователя: {username} (ID: {user_id})")
            
            return jsonify({
                'success': True,
                'message': f'Пользователь {username} успешно удален',
                'deleted_user_id': user_id,
                'deleted_username': username
            })
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка при удалении пользователя {user_id}: {e}")
            return jsonify({'error': f'Ошибка базы данных: {str(e)}'}), 500
            
    except Exception as e:
        print(f"❌ Общая ошибка при удалении пользователя: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@admin_bp.route('/ban-user', methods=['POST'])
@rate_limit('api')
@admin_required
def ban_user_api():
    """Блокировка пользователя администратором"""
    try:
        # Поддерживаем как JSON, так и form данные
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'ID пользователя обязателен'}), 400
        
        user_id = data['user_id']
        ban_reason = data.get('reason', 'Заблокирован администратором')
        
        try:
            user_id = int(user_id)
            if user_id <= 0:
                return jsonify({'error': 'Некорректный ID пользователя'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'ID пользователя должен быть числом'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        # Заблокировать пользователя
        user.user_is_active = False  # Используем column user_is_active
        user.banned_reason = ban_reason
        user.banned_at = datetime.now()
        db.session.commit()
        
        print(f"🔒 Администратор заблокировал пользователя: {user.username}")
        
        return jsonify({
            'success': True,
            'message': f'Пользователь {user.username} заблокирован',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при блокировке пользователя: {str(e)}'}), 500

@admin_bp.route('/unban-user', methods=['POST'])
@rate_limit('api')
@admin_required
def unban_user_api():
    """Разблокировка пользователя администратором"""
    try:
        # Поддерживаем как JSON, так и form данные
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'ID пользователя обязателен'}), 400
        
        user_id = data['user_id']
        
        try:
            user_id = int(user_id)
            if user_id <= 0:
                return jsonify({'error': 'Некорректный ID пользователя'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'ID пользователя должен быть числом'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        # Разблокировать пользователя
        user.user_is_active = True  # Используем column user_is_active
        user.banned_reason = None
        user.banned_at = None
        db.session.commit()
        
        print(f"✅ Администратор разблокировал пользователя: {user.username}")
        
        return jsonify({
            'success': True,
            'message': f'Пользователь {user.username} разблокирован',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при разблокировке пользователя: {str(e)}'}), 500

@admin_bp.route('/users-stats', methods=['GET'])
@rate_limit('api')
@admin_required
def get_users_stats_api():
    """Получение расширенной статистики пользователей"""
    try:
        # Общая статистика
        total_users = User.query.count()
        active_users = User.query.filter_by(user_is_active=True).count()  # Используем column
        banned_users = User.query.filter_by(user_is_active=False).count()  # Используем column
        
        # Статистика активности
        users_with_lessons = db.session.query(User.id).join(UserProgress).filter(UserProgress.completed==True).distinct().count()
        users_with_encryption = db.session.query(User.id).join(EncryptionHistory).distinct().count()
        
        # Новые пользователи за последние 7 дней
        week_ago = datetime.now() - timedelta(days=7)
        new_users_week = User.query.filter(User.created_at >= week_ago).count()
        
        # Топ активных пользователей
        top_users = db.session.query(
            User.username,
            User.email,
            db.func.count(UserProgress.id).label('lessons_count'),
            db.func.count(EncryptionHistory.id).label('encryption_count')
        ).outerjoin(UserProgress).outerjoin(EncryptionHistory).group_by(User.id).order_by(
            db.func.count(UserProgress.id) + db.func.count(EncryptionHistory.id)
        ).limit(10).all()
        

        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'banned_users': banned_users,
                'users_with_lessons': users_with_lessons,
                'users_with_encryption': users_with_encryption,
                'new_users_week': new_users_week,
                'top_users': [
                    {
                        'username': user.username,
                        'email': user.email,
                        'lessons_count': user.lessons_count or 0,
                        'encryption_count': user.encryption_count or 0
                    } for user in top_users
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения статистики: {str(e)}'}), 500

# === Управление историями пользователей ===

@admin_bp.route('/get-user-stories/<int:user_id>', methods=['GET'])
@admin_required
def get_user_stories_api(user_id):
    """Получение всех историй конкретного пользователя"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
            
        stories = ForumStory.query.filter_by(author_id=user_id).order_by(ForumStory.created_at.desc()).all()
        
        stories_data = []
        for story in stories:
            stories_data.append({
                'id': story.id,
                'title': story.title,
                'content': story.content[:100] + '...' if len(story.content) > 100 else story.content,
                'category': story.category,
                'created_at': story.created_at.strftime('%d.%m.%Y %H:%M'),
                'views': story.views_count,
                'likes': story.likes_count
            })
            
        return jsonify({
            'success': True,
            'username': user.username,
            'stories': stories_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при получении историй: {str(e)}'}), 500

@admin_bp.route('/get-story/<int:story_id>', methods=['GET'])
@admin_required
def get_story_api(story_id):
    """Получение одной истории для редактирования"""
    try:
        story = ForumStory.query.get(story_id)
        if not story:
            return jsonify({'error': 'История не найдена'}), 404
            
        return jsonify({
            'success': True,
            'story': {
                'id': story.id,
                'title': story.title,
                'content': story.content,
                'category': story.category
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при получении истории: {str(e)}'}), 500

@admin_bp.route('/update-story', methods=['POST'])
@rate_limit('api')
@admin_required
def update_story_api():
    """Обновление истории"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        if not data or 'story_id' not in data:
            return jsonify({'error': 'ID истории обязателен'}), 400
            
        story_id = data['story_id']
        title = data.get('title')
        content = data.get('content')
        
        story = ForumStory.query.get(story_id)
        if not story:
            return jsonify({'error': 'История не найдена'}), 404
            
        if title:
            story.title = xss_protection.sanitize_input(title)
        if content:
            story.content = xss_protection.sanitize_input(content, max_length=10000)
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'История успешно обновлена'
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при обновлении истории: {str(e)}'}), 500

@admin_bp.route('/delete-story', methods=['POST'])
@rate_limit('api')
@admin_required
def delete_story_api():
    """Удаление истории"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        if not data or 'story_id' not in data:
            return jsonify({'error': 'ID истории обязателен'}), 400
            
        story_id = data['story_id']
        
        story = ForumStory.query.get(story_id)
        if not story:
            return jsonify({'error': 'История не найдена'}), 404
            
        db.session.delete(story)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'История успешно удалена'
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка при удалении истории: {str(e)}'}), 500

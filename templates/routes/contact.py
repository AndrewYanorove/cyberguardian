from flask import Blueprint, render_template, request, jsonify, flash
from flask_mail import Mail, Message
from app import app

contact_bp = Blueprint('contact', __name__)

# Конфигурация email (заглушка)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Отправка email (заглушка)
            msg = Message(
                subject=f"Новое сообщение от {name}",
                sender=email,
                recipients=['your-email@gmail.com'],
                body=f"Имя: {name}\nEmail: {email}\n\nСообщение:\n{message}"
            )
            
            mail.send(msg)
            flash('Сообщение успешно отправлено!', 'success')
            
        except Exception as e:
            flash('Ошибка при отправке сообщения', 'danger')
    
    return render_template('contact.html')
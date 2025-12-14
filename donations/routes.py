from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    current_app,
)
from flask_login import login_required, current_user
from datetime import datetime
import uuid
from database import db  # ✅ Импортируем из database.py
from auth.models import User, Donation  # ✅ Импортируем модели
from . import donations_bp


@donations_bp.route("/")
def donate():
    """Страница пожертвований"""
    return render_template("donations/donate.html")


@donations_bp.route("/support")
def support():
    """Страница поддержки проекта"""
    return render_template("donations/support.html")


@donations_bp.route("/process", methods=["POST"])
@login_required
def process_donation():
    """Обработка пожертвования"""
    try:
        amount = float(request.form.get("amount", 0))
        currency = request.form.get("currency", "RUB")
        payment_method = request.form.get("payment_method", "card")
        is_anonymous = request.form.get("is_anonymous") == "true"
        purpose = request.form.get("purpose", "general")

        if amount < 10:
            flash("Минимальная сумма пожертвования - 10 рублей", "danger")
            return redirect(url_for("donations.donate"))

        # Генерируем ID транзакции
        transaction_id = (
            f"don_{uuid.uuid4().hex[:16]}_{int(datetime.utcnow().timestamp())}"
        )

        # Создаем запись о пожертвовании
        donation = Donation(
            user_id=None if is_anonymous else current_user.id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status="completed",  # Для демо сразу отмечаем как выполненное
            purpose=purpose,
            is_anonymous=is_anonymous,
        )

        db.session.add(donation)
        db.session.commit()

        flash(
            "Спасибо за ваше пожертвование! Проект будет развиваться благодаря вам.",
            "success",
        )
        return redirect(url_for("donations.thank_you", donation_id=donation.id))

    except Exception as e:
        current_app.logger.error(f"Donation error: {e}")
        db.session.rollback()
        flash(
            "Произошла ошибка при обработке пожертвования. Пожалуйста, попробуйте позже.",
            "danger",
        )
        return redirect(url_for("donations.donate"))


@donations_bp.route("/thank-you/<int:donation_id>")
@login_required
def thank_you(donation_id):
    """Страница благодарности после пожертвования"""
    donation = Donation.query.get_or_404(donation_id)

    # Проверяем, что пользователь имеет доступ к этому пожертвованию
    if donation.user_id != current_user.id and not current_user.is_admin():
        flash("Доступ запрещен", "danger")
        return redirect(url_for("donations.donate"))

    return render_template("donations/thank_you.html", donation=donation)


@donations_bp.route("/stats")
def donation_stats():
    """Статистика пожертвований"""
    total_donations = (
        db.session.query(db.func.sum(Donation.amount))
        .filter(Donation.status == "completed")
        .scalar()
        or 0
    )

    total_donors = (
        db.session.query(db.func.count(db.func.distinct(Donation.user_id)))
        .filter(Donation.status == "completed", Donation.user_id.isnot(None))
        .scalar()
        or 0
    )

    recent_donations = (
        Donation.query.filter(Donation.status == "completed")
        .order_by(Donation.created_at.desc())
        .limit(5)
        .all()
    )

    return jsonify(
        {
            "total_amount": float(total_donations),
            "total_donors": total_donors,
            "recent_donations": [
                {
                    "amount": d.amount,
                    "currency": d.currency,
                    "date": d.created_at.strftime("%d.%m.%Y %H:%M"),
                    "anonymous": d.is_anonymous,
                    "username": (
                        "Аноним"
                        if d.is_anonymous
                        else (d.user.username if d.user else "Пользователь")
                    ),
                }
                for d in recent_donations
            ],
        }
    )


@donations_bp.route("/leaderboard")
def leaderboard():
    """Таблица лидеров по пожертвованиям"""
    # Используем JOIN для получения имен пользователей
    top_donors = (
        db.session.query(
            User.username,
            db.func.sum(Donation.amount).label("total_donated"),
            db.func.count(Donation.id).label("donation_count"),
        )
        .join(Donation, User.id == Donation.user_id)
        .filter(Donation.status == "completed", Donation.is_anonymous == False)
        .group_by(User.id)
        .order_by(db.desc("total_donated"))
        .limit(20)
        .all()
    )

    return render_template(
        "donations/leaderboard.html",
        top_donors=[
            {
                "username": username,
                "total_donated": float(total_donated),
                "donation_count": donation_count,
            }
            for username, total_donated, donation_count in top_donors
        ],
    )


@donations_bp.route("/my-donations")
@login_required
def my_donations():
    """История пожертвований пользователя"""
    donations = (
        Donation.query.filter(Donation.user_id == current_user.id)
        .order_by(Donation.created_at.desc())
        .all()
    )

    total_donated = sum(d.amount for d in donations if d.status == "completed")

    return render_template(
        "donations/my_donations.html", donations=donations, total_donated=total_donated
    )


@donations_bp.route("/webhook/payment", methods=["POST"])
def payment_webhook():
    """Вебхук для обработки платежей (заглушка)"""
    # Здесь будет интеграция с платежной системой
    return jsonify({"status": "ok", "message": "Webhook received"})

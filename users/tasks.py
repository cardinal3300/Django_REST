from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from courses.models import Course
from users.models import Subscription

Users = get_user_model()


@shared_task
def send_course_update_mail(course_id):
    """Задача отправления письма после обновления курса."""

    course = Course.objects.get(id=course_id)

    subscriptions = Subscription.objects.filter(course=course).select_related("user")

    emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not emails:
        return "No subscribers"

    send_mail(
        subject=f"Обновление курса «{course.title}»",
        message=(
            f"Курс «{course.title}» был обновлён.\n\n"
            f"Зайдите в личный кабинет, чтобы посмотреть изменения."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )

    return f"Sent {len(emails)} emails"


@shared_task
def deactivate_inactive_users():
    """Задача блокировки пользователей, которые не заходили более 30 дней."""
    print("RUN deactivate_inactive_users")

    threshold_date = timezone.now() - timedelta(days=30)

    users_to_deactivate = Users.objects.filter(
        last_login__lt=threshold_date,
        is_active=True,
    )

    count = users_to_deactivate.update(is_active=False)

    return f"Deactivated {count} users"

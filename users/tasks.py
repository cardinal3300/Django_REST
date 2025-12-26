from celery import shared_task
from django.core.mail import send_mail

from config import settings
from courses.models import Course
from users.models import Subscription


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

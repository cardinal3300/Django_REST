from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from users.models import Payment
from courses.models import Course
from lessons.models import Lesson


User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет таблицу платежей тестовыми данными'

    def handle(self, *args, **options):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user or not course or not lesson:
            self.stdout.write(
                self.style.ERROR('Недостаточно данных для создания платежей')
            )
            return

        Payment.objects.create(
            user=user,
            course=course,
            amount=5000,
            payment_method=Payment.PAYMENT_METHOD_CHOICES
        )

        Payment.objects.create(
            user=user,
            lesson=lesson,
            amount=1000,
            payment_method=Payment.PAYMENT_METHOD_CHOICES
        )

        self.stdout.write(
            self.style.SUCCESS('Платежи успешно созданы')
        )

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

from users.models import Payment
from courses.models import Course
from lessons.models import Lesson

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет таблицу Payment тестовыми данными'

    def handle(self, *args, **options):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR('Нет пользователей для создания платежей'))
            return

        if not courses.exists() and not lessons.exists():
            self.stdout.write(self.style.ERROR('Нет курсов или уроков для оплаты'))
            return

        payment_methods = [Payment.CASH, Payment.TRANSFER]

        for i in range(5):  # создаём 5 платежей
            user = random.choice(users)

            # либо курс, либо урок
            if random.choice([True, False]) and courses.exists():
                course = random.choice(courses)
                lesson = None
                amount = random.randint(1000, 10000)
            elif lessons.exists():
                lesson = random.choice(lessons)
                course = None
                amount = random.randint(100, 5000)
            else:
                continue

            payment = Payment.objects.create(
                user=user,
                payment_date=timezone.now(),
                course=course,
                lesson=lesson,
                amount=amount,
                payment_method=random.choice(payment_methods)
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Создан платеж: {payment.user} — {payment.amount} ({payment.payment_method})'
                )
            )

        self.stdout.write(self.style.SUCCESS('Все платежи успешно созданы!'))

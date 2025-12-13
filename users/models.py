from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course
from lessons.models import Lesson


class UserManager(BaseUserManager):
    """Кастомный менеджер пользователей"""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель Платежи"""

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = ((CASH, "Наличные"), (TRANSFER, "Перевод на счет"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    def __str__(self):
        return (
            f"{self.payment_date}: {self.user} — {self.amount} ({self.payment_method})"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

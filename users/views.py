from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.permissions import IsModerator, IsOwner
from users.serializers import (PaymentSerializer, UserRegisterSerializer,
                               UserSerializer)

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация(доступна без авторизации)."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(ModelViewSet):
    """CRUD пользователей (только авторизованные)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class PaymentListApiView(generics.ListAPIView):
    """Получение платежей с сортировкой и фильтрациями."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "course",
        "lesson",
        "payment_method",
    ]  # фильтры по курсу, уроку и способу оплаты
    ordering_fields = ["payment_date"]  # сортировка по дате
    ordering = ["-payment_date"]  # сортировка по умолчанию (по убыванию)

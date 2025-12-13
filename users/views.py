from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListApiView(generics.ListAPIView):
    """Получение платежей с сортировкой и фильтрациями"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "course",
        "lesson",
        "payment_method",
    ]  # фильтры по курсу, уроку и способу оплаты
    ordering_fields = ["payment_date"]  # сортировка по дате
    ordering = ["-payment_date"]  # сортировка по умолчанию (по убыванию)

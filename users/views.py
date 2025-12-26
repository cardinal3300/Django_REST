from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from paginators import MyPaginator
from users.models import Payment, Subscription
from users.permissions import IsOwner
from users.serializers import PaymentSerializer, UserRegisterSerializer, UserSerializer
from users.services.stripe import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)

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
    pagination_class = MyPaginator


class PaymentCreateApiView(APIView):
    """Создание платежа. Основная бизнес точка."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(user=self.request.user)

        # 1. Создаем продукт
        product = create_stripe_product(payment)

        # 2. Создаем цену
        price = create_stripe_price(
            product=product, unit_amount=payment.unit_amount * 100
        )

        # 3. Создаем сессию
        session = create_stripe_session(price_id=price.id)

        # 4. Сохраняем ссылку на оплату
        payment.payment_link = session.url
        payment.save(update_fields=["payment_link"])

        return Response(
            {
                "payment_id": payment.id,
                "payment_link": session.url,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentListApiView(generics.ListAPIView):
    """Получение платежей с сортировкой и фильтрациями."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = MyPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "course",
        "lesson",
        "payment_method",
    ]  # фильтры по курсу, уроку и способу оплаты
    ordering_fields = ["payment_date"]  # сортировка по дате
    ordering = ["-payment_date"]  # сортировка по умолчанию (по убыванию)


class SubscriptionAPIView(APIView):
    """Управление подпиской (добавить / удалить)."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Подписка / отписка от курса",
        operation_description="Создает или удаляет подписку пользователя на курс",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса"
                )
            },
        ),
        responses={
            200: openapi.Response("Успешно"),
            401: openapi.Response("Не авторизован"),
        },
    )
    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        subs_qs = Subscription.objects.filter(user=user, course=course)

        if subs_qs.exists():
            subs_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})

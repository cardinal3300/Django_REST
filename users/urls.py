from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentCreateApiView,
    PaymentListApiView,
    SubscriptionAPIView,
    UserRegisterAPIView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("payments/", PaymentListApiView.as_view(), name="payments-list"),
    path("payments/create/", PaymentCreateApiView.as_view(), name="payment-create"),
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
]

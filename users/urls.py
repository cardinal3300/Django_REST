from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentListApiView, UserViewSet, UserRegisterAPIView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

app_name = UsersConfig.name

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegisterAPIView.as_view(), name='register'),
    path("payments/", PaymentListApiView.as_view(), name="payments-list"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

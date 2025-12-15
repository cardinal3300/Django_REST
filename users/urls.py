from django.urls import path

from users.views import PaymentListApiView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListApiView.as_view(), name="payments-list"),
]

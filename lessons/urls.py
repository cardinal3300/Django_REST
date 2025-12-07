from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LessonListCreateAPIView, LessonRetrieveUpdateDeleteAPIView


app_name = "lessons"

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lessons-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDeleteAPIView.as_view(), name='lesson-detail'),
]

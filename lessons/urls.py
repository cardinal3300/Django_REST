from django.urls import path

from lessons.views import (
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = "lessons"

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve-list"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons-update"),
    path("lessons/destroy/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-destroy")
]

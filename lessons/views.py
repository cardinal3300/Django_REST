from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from paginators import MyPaginator
from users.permissions import IsModerator, IsNotModerator, IsOwner
from users.tasks import send_course_update_mail


class LessonCreateAPIView(CreateAPIView):
    """Создание урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Получение списка уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MyPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    """Получение одного урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):

        lesson = serializer.save()
        course = lesson.course

        now = timezone.now()
        four_hours_ago = now - timedelta(hours=4)

        if course.updated_at < four_hours_ago:
            send_course_update_mail.delay(course.id)
            course.save(update_fields=["updated_at"])


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Lesson
from lessons.serializers import LessonSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Получение списка и создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lessons = serializer.save()
        new_lessons.owner = self.request.user
        new_lessons.save()


class LessonRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, изменение, удаление одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lessons = serializer.save()
        new_lessons.owner = self.request.user
        new_lessons.save()

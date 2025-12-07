from rest_framework import generics
from lessons.models import Lesson
from lessons.serializers import LessonSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Получение списка и создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, изменение, удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

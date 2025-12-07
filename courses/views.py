from rest_framework.viewsets import ModelViewSet
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    """CRUD для курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

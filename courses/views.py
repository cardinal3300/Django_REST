from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseSerializer
from paginators import MyPaginator
from users.permissions import IsModerator, IsOwner
from users.tasks import send_course_update_mail


class CourseViewSet(ModelViewSet):
    """CRUD для курса."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPaginator

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]

        else:  # list, retrieve
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_mail.delay(course.id)

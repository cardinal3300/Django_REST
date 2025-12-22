from rest_framework import serializers

from courses.models import Course
from lessons.serializers import LessonSerializer
from users.models import Subscription


class CourseSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()

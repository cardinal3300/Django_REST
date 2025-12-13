from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()

from rest_framework import serializers

from lessons.models import Lesson
from lessons.validators import TitleValidator, VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            TitleValidator(field="title"),
            VideoLinkValidator(field="video_url"),
            serializers.UniqueTogetherValidator(
                fields=["title"], queryset=Lesson.objects.all()
            ),
        ]

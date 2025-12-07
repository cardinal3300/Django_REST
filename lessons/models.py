from django.db import models
from courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return f"{self.title} ({self.course.title})"

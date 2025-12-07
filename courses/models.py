from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.title

import re
from rest_framework.serializers import ValidationError


class TitleValidator:
    """Разрешает определенный ввод в поле 'title'."""

    def __init__(self, field):
        self.filed = field

    def __call__(self, value):
        reg = re.compile(r'^[a-zA-Z0-9.\- ]+$')

        if not reg.match(value.get(self.filed)):
            raise ValidationError(
                'Поле может содержать только латиницу в нижнем, верхнем регистре, цифры, точку, дефис и пробел'
            )


class VideoLinkValidator:
    """Разрешает ссылки только на YouTube."""

    YOUTUBE_REGEX = re.compile(
        r'^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w\-]+'
    )

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get(self.field)

        if not link:
            return

        if not self.YOUTUBE_REGEX.match(link):
            raise ValidationError(
                {self.field: 'Разрешены только ссылки на youtube.com'}
            )

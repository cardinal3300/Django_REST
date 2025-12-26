from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from lessons.models import Lesson

User = get_user_model()


class LessonApiTest(APITestCase):

    def setUp(self):
        """Создание:
        -обычного пользователя,
        -второго пользователя,
        -модератора,
        -курс,
        -урок."""

        # группы
        self.moderators_group = Group.objects.create(name="moderators")

        # пользователи
        self.owner = User.objects.create_user(email="owner@test.com", password="123456")

        self.other_user = User.objects.create_user(
            email="other@test.com", password="123456"
        )

        self.moderator = User.objects.create_user(
            email="moder@test.com", password="123456"
        )
        self.moderator.groups.add(self.moderators_group)

        # курс
        self.course = Course.objects.create(
            title="Test course", description="Test desc", owner=self.owner
        )

        # урок
        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="Test desc",
            course=self.course,
            owner=self.owner,
            video_url="https://youtube.com/watch?v=123",
        )

    def test_owner_can_create_lesson(self):
        """Тест создание урока (owner)."""

        self.client.force_authenticate(user=self.owner)

        data = {
            "title": "New lesson",
            "description": "Desc",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=456",
        }

        response = self.client.post("/api/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_moderator_cannot_create_lesson(self):
        """Тест создание урока модератором (запрещено)."""

        self.client.force_authenticate(user=self.moderator)

        data = {
            "title": "New lesson",
            "description": "Desc",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=456",
        }

        response = self.client.post("/api/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_lesson(self):
        """Тест обновление урока владельцем."""

        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f"/api/lessons/update/{self.lesson.id}/", data={"title": "Updated title"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_update_any_lesson(self):
        """Тест обновление урока модератором."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.patch(
            f"/api/lessons/update/{self.lesson.id}/",
            data={"title": "Updated by moderator"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_cannot_delete_lesson(self):
        """Тест удаление урока модератором (запрещено)."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(f"/api/lessons/destroy/{self.lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_delete_lesson(self):
        """Тест удаление урока не владельцем (запрещено)."""

        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(f"/api/lessons/destroy/{self.lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

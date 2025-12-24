from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from lessons.models import Lesson
from users.models import Subscription

User = get_user_model()


class UserApiTest(APITestCase):

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

    def test_user_can_subscribe(self):
        """Тест подписки на курс."""

        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            "/api/subscribe/", data={"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.owner, course=self.course).exists()
        )

    def test_user_can_unsubscribe(self):
        """Тест повторный POST — отписка."""

        Subscription.objects.create(user=self.owner, course=self.course)

        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            "/api/subscribe/", data={"course_id": self.course.id}
        )

        self.assertFalse(
            Subscription.objects.filter(user=self.owner, course=self.course).exists()
        )

    def test_course_serializer_subscription_flag(self):
        """Тест проверка is_subscribed в курсе."""

        Subscription.objects.create(user=self.owner, course=self.course)

        self.client.force_authenticate(user=self.owner)

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertTrue(response.data["is_subscribed"])

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses.views import CourseViewSet


app_name = "courses"

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]

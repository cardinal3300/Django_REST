from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка, что пользователь состоит в группе Moderators."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsNotModerator(BasePermission):
    """Запрещает модераторам создавать объекты."""

    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.groups.filter(name="moderators").exists()
        return True


class IsOwner(BasePermission):
    """Проверка, что пользователь владелец."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка, что пользователь состоит в группе Moderators"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):
    """Проверка, что пользователь владелец"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

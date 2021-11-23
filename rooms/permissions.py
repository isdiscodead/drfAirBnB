from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    # .has_object_permission(self, request, view, obj)은 단일 object
    # .has_permission(self, request, view)은 리스트 또는 개별 object
    def has_object_permission(self, request, view, room):
        return room.user == request.user

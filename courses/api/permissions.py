from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, obj):
        return obj.students.filter(id=request.user.id).exists()

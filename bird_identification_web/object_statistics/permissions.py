from rest_framework.permissions import BasePermission

class CanUploadPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('object_statistics.add_loggedobject')

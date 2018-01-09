from rest_framework import permissions

class IsAthleteOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, athlete):
        if request.user:
            return athlete == request.user
        return False

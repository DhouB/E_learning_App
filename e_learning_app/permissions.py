from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Student'

class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Tutor'

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Administrator'

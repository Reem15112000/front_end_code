from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "doctor_profile")

class IsPatientOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or hasattr(request.user, "patient")
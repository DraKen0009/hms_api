from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from api.models import User


class DoctorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.role == User.Role.DOCTOR or request.user.is_superuser):
            return True
        return False


class PatientsOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.role == User.Role.DOCTOR or request.user.is_superuser):
            return True
        return False


class DoctorSpecific(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (obj == request.user or request.user.is_superuser):
            return True
        return False


class PatientSpecific(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (obj == request.user or request.user.is_superuser):
            return True
        return False


class DoctorsPatientSpecific(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                (obj.patient == request.user or request.user.is_superuser) or request.user.role == User.Role.DOCTOR):
            return True
        return False


class DepartmentDoctor(BasePermission):
    def has_permission(self, request, view):
        if not view.get_queryset().first():
            return Response()
        if request.user.is_authenticated and ((request.user in view.get_queryset()) or request.user.is_superuser):
            return True
        return False


class DepartmentPatient(BasePermission):
    def has_permission(self, request, view):
        if view.get_queryset().first():
            return Response({'msg': 'Department is empty', })
        if request.user.is_authenticated and (
                request.user.department == view.get_queryset().first().department or request.user.is_superuser):
            return True
        return False

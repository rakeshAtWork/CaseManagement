from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_401_UNAUTHORIZED
from .models import UserRole, RolePermission


class Unauthorized(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication credentials were not valid'
    default_code = 'Unauthorized'


def check_user_permissions(permissions, user):
    for permission in permissions:
        roles = UserRole.objects.filter(user=user).values_list("role", flat=True)
        if RolePermission.objects.filter(role__in=roles, privilege__privilege_name=permission.privilege_name).exists():
            return True
    raise PermissionDenied(_('Insufficient permissions.'))


class CozentusPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise Unauthorized()
        required_permissions = getattr(
            view, 'case_management_object_permissions', {}
        ).get(request.method, None)
        # TODO modify for role privilege
        if required_permissions and 0:
            try:
                check_user_permissions(
                    permissions=required_permissions, user=request.user
                )
            except PermissionDenied:
                raise PermissionDenied({"message": "You don't have permission to perform this task", })
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise Unauthorized()
        # Reteriving the request permissions
        required_permissions = getattr(
            view, 'case_management_object_permissions', {}
        ).get(request.method, None)
        # TODO modify for role privilege
        # TODO make sure permissions should be checked when live
        if required_permissions and 0:
            try:
                check_user_permissions(
                    permissions=required_permissions, user=request.user
                )
            except PermissionDenied:
                raise PermissionDenied({"message": "You don't have permission to perform this task", })
            else:
                return True
        else:
            return True

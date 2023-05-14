from rest_framework import permissions

'''
level 1 : admin
level 2 : staff
'''
class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsStaffPermission(permissions.DjangoModelPermissions):
    """
    Allows access only to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsReadOnly(permissions.BasePermission):
    """
    Allows access only to read-only requests.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

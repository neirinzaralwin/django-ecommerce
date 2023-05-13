from rest_framework import permissions

'''
level 1 : admin
level 2 : staff
'''

class IsStaffPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False
        return super().has_permission(request, view)
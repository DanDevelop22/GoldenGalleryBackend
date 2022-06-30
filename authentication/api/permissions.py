from rest_framework import permissions
from rest_framework.authtoken.models import Token

class UpdateOwnProfile(permissions.BasePermission):
    """Permite a usuarios editar su propio perfil"""

    def has_object_permission(self, request, view, obj):
        """Chequear el usuario tiene permisos sobre su propio perfil"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            #El metodo no es seguro
            return obj.id == request.user.id
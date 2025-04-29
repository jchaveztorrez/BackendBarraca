from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsAutenticaion import SucursalViewSet, RolViewSet, PermisoViewSet, UsuarioViewSet, UsuarioRolSucursalViewSet, RolPermisoViewSet, LoginView, LogoutView, ChangePasswordView

from . import viewsAutenticaion

ruter = DefaultRouter()
ruter.register(r'sucursal', SucursalViewSet)
ruter.register(r'rol', RolViewSet)
ruter.register(r'permiso', PermisoViewSet)
ruter.register(r'usuario', UsuarioViewSet)
ruter.register(r'usuario_rol_sucursal', UsuarioRolSucursalViewSet)
ruter.register(r'rol_permiso', RolPermisoViewSet)
urlpatterns = [
    path('', include(ruter.urls)),
]
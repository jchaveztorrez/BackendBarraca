
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsAutenticaion import  ProductoMaderaViewSet, SucursalViewSet, RolViewSet, PermisoViewSet, UsuarioViewSet, UsuarioRolSucursalViewSet, RolPermisoViewSet


from . import viewsAutenticaion

ruter = DefaultRouter()
ruter.register(r'sucursal', SucursalViewSet)
ruter.register(r'rol', RolViewSet)
ruter.register(r'permiso', PermisoViewSet)
ruter.register(r'usuario', UsuarioViewSet)
ruter.register(r'usuariorolsucursal', UsuarioRolSucursalViewSet)
ruter.register(r'rolpermiso', RolPermisoViewSet)

ruter.register(r'productoMadera', ProductoMaderaViewSet)

ruter.register(r'ventas', VentasViewSet)
ruter.register(r'detallesventas', DetallesVentasViewSet) 



urlpatterns = [
    path('', include(ruter.urls)),

]
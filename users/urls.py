from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsAutenticaion import SucursalViewSet, RolViewSet, PermisoViewSet, UsuarioViewSet, UsuarioRolSucursalViewSet, RolPermisoViewSet
from .viewsProductos import UsuarioForestalViewSet, TransporteViewSet, RomaneoViewSet, InventarioViewSet, DetalleRomaneoViewSet, VentaViewSet, DetalleVentaViewSet

from . import viewsAutenticaion, viewsProductos

ruter = DefaultRouter()
ruter.register(r'sucursal', SucursalViewSet)
ruter.register(r'rol', RolViewSet)
ruter.register(r'permiso', PermisoViewSet)
ruter.register(r'usuario', UsuarioViewSet)
ruter.register(r'usuariorolsucursal', UsuarioRolSucursalViewSet)
ruter.register(r'rolpermiso', RolPermisoViewSet)

ruter.register(r'usuarioForestal', UsuarioForestalViewSet)
ruter.register(r'transporte', TransporteViewSet)
ruter.register(r'romaneo', RomaneoViewSet)
ruter.register(r'inventario', InventarioViewSet)    
ruter.register(r'detalleRomaneo', DetalleRomaneoViewSet)
ruter.register(r'venta', VentaViewSet)
ruter.register(r'detalleVenta', DetalleVentaViewSet)

urlpatterns = [
    path('', include(ruter.urls)),
]